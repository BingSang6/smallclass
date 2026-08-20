/* sw-register.js — 注册 Service Worker（离线可用 + 新版本接管后自动刷新一次） */
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./sw.js').catch(() => {});
    // 新 SW 激活接管时，当前页面还是旧资源 → 刷新一次载入新版（防循环：只刷一次）
    let reloaded = false;
    navigator.serviceWorker.addEventListener('controllerchange', () => {
      if (reloaded) return;
      reloaded = true;
      location.reload();
    });
  });
}
