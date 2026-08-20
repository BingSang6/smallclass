/* sw.js — 离线缓存（cache-first，版本号升级时更新） */
const CACHE = 'smallclass-v10';
const ASSETS = [
  './', './index.html', './manifest.webmanifest',
  './css/style.css',
  './js/storage.js', './js/tts.js', './js/quiz.js', './js/app.js',
  './data/banks/math-oral.json', './data/banks/chinese-words.json', './data/banks/math-g4-units.json', './data/banks/poems.json',
  './icons/icon-192.png', './icons/icon-512.png'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys =>
    Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
  ).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  e.respondWith(caches.match(e.request).then(r => r || fetch(e.request)));
});
