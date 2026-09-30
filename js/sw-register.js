/* sw-register.js — 注册 Service Worker（离线可用 + 新版本接管后自动刷新一次） */
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    // updateViaCache:'none'——检查 sw.js 更新时绕过 HTTP 缓存（v3.21.1，
    // 否则浏览器可能拿缓存的旧 sw.js 认为「没有新版本」，设备一直卡旧版）
    navigator.serviceWorker.register('./sw.js', { updateViaCache: 'none' }).catch(() => {});
    // 新 SW 激活接管时，当前页面还是旧资源 → 刷新一次载入新版（防循环：只刷一次）
    let reloaded = false;
    navigator.serviceWorker.addEventListener('controllerchange', () => {
      if (reloaded) return;
      reloaded = true;
      location.reload();
    });
    // 页面开着也每小时主动查一次更新（v3.21.1：PWA 长时间不关也能拿到新版+自动刷新）
    setInterval(() => {
      navigator.serviceWorker.getRegistration()
        .then(r => r && r.update()).catch(() => {});
    }, 3600000);
  });
}
