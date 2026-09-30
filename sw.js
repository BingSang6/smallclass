/* sw.js — 离线缓存（cache-first，版本号升级时更新） */
const CACHE = 'smallclass-v48';
const ASSETS = [
  './', './index.html', './manifest.webmanifest',
  './css/style.css',
  './js/storage.js', './js/tts.js', './js/quiz.js', './js/app.js', './js/sw-register.js',
  './data/banks/math-oral.json', './data/banks/chinese-words.json', './data/banks/math-units.json', './data/banks/poems.json', './data/banks/english-words.json', './data/banks/guwen.json', './data/banks/math-topics.json', './data/banks/chinese-units.json', './data/banks/english-units.json', './data/banks/english-topics.json',
  './icons/icon-192.png', './icons/icon-512.png'
];

/** 强制绕过 HTTP 缓存下载（cache:'reload'），失败自动重试 3 次（间隔递增）。
 *  v3.21.1：addAll 一个文件失败就整体失败——github.io 网络不稳时 SW 永远装不上，
 *  用户设备一直卡旧版本（v3.20 弹窗挥之不去的根因）。逐文件下载+重试大幅提升成功率 */
const fetchNew = (url, tries) => {
  tries = tries || 3;
  const attempt = i => fetch(url, { cache: 'reload' }).then(r => {
    if (!r.ok) throw new Error('HTTP ' + r.status + ' ' + url);
    return r;
  }).catch(err => {
    if (i >= tries) throw err;
    return new Promise(res => setTimeout(res, 600 * (i + 1))).then(() => attempt(i + 1));
  });
  return attempt(0);
};

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c =>
      Promise.all(ASSETS.map(u => fetchNew(u).then(r => c.put(u, r))))
    ).then(() => self.skipWaiting())
  );
});
self.addEventListener('activate', e => {
  // 立即接管页面（与原版一致，不挂长时间 waitUntil——那会被浏览器终止 SW，行为不可预期）
  e.waitUntil(clients.claim());
  // 旧缓存延迟 60s 再清（fire-and-forget）：接管瞬间正在加载的资源还可从旧缓存兜底，
  // 立刻删会在网络不稳时「半更新白屏」（v3.20.1 修复）；SW 提前被杀则留到下次 activate 再清，无害
  setTimeout(() => {
    caches.keys().then(keys => keys.filter(k => k !== CACHE).forEach(k => caches.delete(k)));
  }, 60000);
});
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  // cache-first，只查本版缓存（全局 caches.match 按创建时间搜，旧缓存会遮蔽新版资源！）
  // ignoreSearch：index.html 的 js/css 带 ?v= 版本参数，匹配时忽略它（v3.21.2）
  // 本版 miss → 走网络；网络失败 → 兜底翻所有版本缓存副本，避免半更新/离线白屏
  e.respondWith(
    caches.open(CACHE).then(c => c.match(e.request, { ignoreSearch: true })).then(r =>
      r || fetch(e.request).catch(() =>
        caches.match(e.request, { ignoreSearch: true }).then(m => m || Response.error()))));
});
