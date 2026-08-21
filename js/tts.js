/* tts.js — 中文语音读题（SpeechSynthesis） */
(function () {
  'use strict';

  function toSpeech(q) {
    let s = String(q);
    // 分数：a/b → "b 分之 a"（中文读法分母在前）
    s = s.replace(/(\d+)\/(\d+)/g, (m, n, d) => ' ' + d + ' 分之 ' + n + ' ');
    s = s.replace(/×/g, ' 乘 ').replace(/÷/g, ' 除以 ')
         .replace(/\+/g, ' 加 ').replace(/−|—|-/g, ' 减 ')
         .replace(/≈/g, ' 约等于 ').replace(/%/g, ' 百分之 ')
         .replace(/=/g, ' 等于几？');
    return s;
  }

  let unlocked = false;
  /** iOS/安卓必须由用户手势内真正 speak 过一次才能解锁音频通道 */
  function unlock() {
    if (unlocked || !('speechSynthesis' in window)) return;
    unlocked = true;
    try {
      const u = new SpeechSynthesisUtterance(' ');
      u.volume = 0;            // 无声占位，只为激活
      u.lang = 'zh-CN';
      speechSynthesis.speak(u);
      speechSynthesis.getVoices();   // 顺便触发声音列表加载
    } catch (e) {}
  }
  document.addEventListener('touchend', unlock, { once: true, passive: true });
  document.addEventListener('click', unlock, { once: true, passive: true });

  // 声音列表异步加载（部分安卓/iOS 首次为空）
  if ('speechSynthesis' in window) {
    speechSynthesis.getVoices();
    if (typeof speechSynthesis.onvoiceschanged !== 'undefined') {
      speechSynthesis.onvoiceschanged = () => speechSynthesis.getVoices();
    }
  }

  const TTS = {
    speak(text) {
      try {
        if (!('speechSynthesis' in window)) return;
        speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance(toSpeech(text));
        u.lang = 'zh-CN';
        u.rate = 0.85;           // 慢一点，孩子听得清
        u.pitch = 1.1;           // 稍微活泼
        const zh = speechSynthesis.getVoices().filter(v => v.lang && v.lang.indexOf('zh') === 0);
        if (zh.length) u.voice = zh.find(v => /Ting|Xiaoxiao|Yaoyao/i.test(v.name)) || zh[0];
        // iOS bug：cancel 后立刻 speak 会静音，稍等一拍
        setTimeout(() => { try { speechSynthesis.speak(u); } catch (e) {} }, 80);
      } catch (e) { /* 语音失败不影响答题 */ }
    },
    stop() { try { speechSynthesis.cancel(); } catch (e) {} },
    praise() {
      const words = ['太棒了！', '答对啦！', '真厉害！', '完全正确！', '你真是口算小达人！'];
      this.speak(words[Math.floor(Math.random() * words.length)]);
    }
  };

  window.TTS = TTS;
})();
