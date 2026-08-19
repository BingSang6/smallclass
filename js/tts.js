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
        if (zh.length) u.voice = zh.find(v => / Ting |^Ting |Ting$/i.test(v.name)) || zh[0];
        speechSynthesis.speak(u);
      } catch (e) { /* 语音失败不影响答题 */ }
    },
    stop() { try { speechSynthesis.cancel(); } catch (e) {} },
    praise() {
      const words = ['太棒了！', '答对啦！', '真厉害！', '完全正确！', '你真是口算小达人！'];
      this.speak(words[Math.floor(Math.random() * words.length)]);
    }
  };

  // iOS Safari 需要用户首次交互后激活语音
  document.addEventListener('touchend', () => {
    try { speechSynthesis.getVoices(); } catch (e) {}
  }, { once: true, passive: true });

  window.TTS = TTS;
})();
