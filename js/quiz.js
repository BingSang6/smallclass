/* quiz.js — 闯关流程：选题、乱序、即时反馈、错题重现 */
(function () {
  'use strict';

  const PER_ROUND = 5;   // 每关 5 题
  let bank = [];         // 全部题目
  let queue = [];        // 本关题目队列（错题会追加）
  let cur = null;        // 当前题
  let streak = 0;        // 连对数
  let correct = 0, total = 0;
  let onEnd = null, onUI = null;   // 回调

  function loadBank(done) {
    if (bank.length) return done();
    fetch('data/banks/math-oral.json')
      .then(r => r.json())
      .then(j => { bank = j; done(); })
      .catch(() => { alert('题库加载失败，请刷新页面'); });
  }

  function pickQuestions(stu, n) {
    const lv = stu.level + 1;   // 学生段位 0~3 ↔ 题库 level 1~4
    const pool = bank.filter(q => q.grade === stu.grade && q.level === lv);
    const wrongIds = stu.wrongPool || [];
    // 错题 tag 出题权重 ×2（自适应：薄弱点更多练）
    const wrongTags = {};
    pool.forEach(q => { if (wrongIds.indexOf(q.id) >= 0) wrongTags[q.tag] = (wrongTags[q.tag] || 0) + 1; });
    const weighted = [];
    pool.forEach(q => { weighted.push(q); if (wrongTags[q.tag]) weighted.push(q); });

    // 1) 错题池优先（同 tag 换题重现，最多 2 题）
    let qs = [];
    Object.keys(wrongTags).slice(0, 2).forEach(t => {
      const cand = weighted.filter(q => q.tag === t && (stu.recentQs || []).indexOf(q.id) < 0);
      if (cand.length) qs.push(cand[Math.floor(Math.random() * cand.length)]);
    });
    // 2) 加权随机补足（避开最近出过的）
    const recent = stu.recentQs || [];
    let rest = weighted.filter(q => qs.indexOf(q) < 0 && recent.indexOf(q.id) < 0);
    if (rest.length < n - qs.length) rest = weighted.filter(q => qs.indexOf(q) < 0);
    while (qs.length < n && rest.length) {
      qs.push(rest.splice(Math.floor(Math.random() * rest.length), 1)[0]);
    }
    return qs.slice(0, n);
  }

  function showQuestion(stu) {
    cur = queue.shift();
    if (!cur) return finish(stu);
    // 选项乱序
    const opts = [String(cur.a)].concat(cur.options.map(String));
    for (let i = opts.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [opts[i], opts[j]] = [opts[j], opts[i]];
    }
    onUI(cur, opts);
    if (Store.autoRead()) TTS.speak(cur.q);
  }

  function answer(stu, val) {
    total++;
    const ok = (String(val) === String(cur.a));
    const tag = cur.tag;
    const isMastery = (stu.wrongPool || []).some(id => id === cur.id) ||
                      bank.some(q => q.id && stu.wrongPool && q.grade === stu.grade &&
                                     q.level === stu.level + 1 && q.tag === tag &&
                                     stu.wrongPool.indexOf(q.id) >= 0);
    if (ok) {
      correct++; streak++;
      TTS.praise();
      // 精通出池：错题 tag 连对 2 次 → 该 tag 全部移出错题池
      if (isMastery) {
        Store.updateCurrent(s => {
          s.tagStreaks[tag] = (s.tagStreaks[tag] || 0) + 1;
          if (s.tagStreaks[tag] >= 2) {
            const idsOfTag = bank.filter(q => q.grade === s.grade && q.level === s.level + 1 && q.tag === tag)
                                 .map(q => q.id);
            s.wrongPool = (s.wrongPool || []).filter(id => idsOfTag.indexOf(id) < 0);
            delete s.tagStreaks[tag];
          }
        });
      }
    } else {
      streak = 0;
      TTS.speak('再想一想。' + (cur.wrongReasons && cur.wrongReasons[0] ? cur.wrongReasons[0] : ''));
      // 错题当场换数字重现：同 tag 下一题插到队尾
      const pool = bank.filter(q => q.grade === stu.grade && q.level === stu.level + 1 && q.tag === tag && q.id !== cur.id);
      if (pool.length) queue.push(pool[Math.floor(Math.random() * pool.length)]);
      // 记入待巩固池 + 连对清零
      Store.updateCurrent(s => {
        s.wrongPool = (s.wrongPool || []).filter(id => id !== cur.id);
        s.wrongPool.push(cur.id);
        if (s.wrongPool.length > 30) s.wrongPool.shift();
        s.tagStreaks[tag] = 0;
      });
    }
    onUI(cur, null, { ok, val: String(val) });
  }

  /** 显示下一题（由 UI 的"继续"触发，或自动） */
  function next(stu) {
    showQuestion(stu);
  }

  function finish(stu) {
    const passed = correct >= 4;   // 对 4 题即过关（得星规则在 app 里算）
    if (onEnd) onEnd({ correct, total, passed });
    reset();
  }

  function reset() { queue = []; cur = null; streak = 0; correct = 0; total = 0; }

  const Quiz = {
    start(stu, ui, end) {
      loadBank(() => {
        reset();
        onUI = ui; onEnd = end;
        queue = pickQuestions(stu, PER_ROUND);
        // recentQs 记录
        Store.updateCurrent(s => {
          s.recentQs = queue.map(q => q.id);
        });
        showQuestion(stu);
      });
    },
    answer(stu, val) { answer(stu, val); },
    next(stu) { next(stu); },
    get current() { return cur; },
    get PER_ROUND() { return PER_ROUND; }
  };

  window.Quiz = Quiz;
})();
