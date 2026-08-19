/* quiz.js — 闯关流程：选题、乱序、即时反馈、错题重现 */
(function () {
  'use strict';

  const PER_ROUND = 5;   // 每关 5 题
  const REVIEW_MAX = 8;  // 今日复习每次最多 8 题
  const banks = {};      // 各学科题库缓存 {subject: [...]}
  let subject = 'math';  // 当前学科
  let mode = 'round';    // round=闯关 / review=今日复习
  let queue = [];        // 本关题目队列（错题会追加）
  let queueTotal = 0;    // 复习模式总题数（用于进度条）
  let cur = null;        // 当前题
  let streak = 0;        // 连对数
  let correct = 0, total = 0;
  let onEnd = null, onUI = null;   // 回调

  function bank(sub) { return banks[sub || subject] || []; }

  function loadBankOf(sub, done) {
    if (banks[sub] && banks[sub].length) return done();
    fetch(Store.SUBJECTS[sub].bank)
      .then(r => r.json())
      .then(j => { banks[sub] = j; done(); })
      .catch(() => { alert('题库加载失败，请刷新页面'); });
  }
  function loadBank(done) { loadBankOf(subject, done); }
  function loadAll(done) {
    const subs = Object.keys(Store.SUBJECTS);
    let n = 0;
    subs.forEach(s => loadBankOf(s, () => { if (++n === subs.length) done(); }));
  }

  /** 今日复习：跨学科收集到期错题（需先 loadAll） */
  function dueList(stu) {
    const today = Store.day();
    const list = [];
    Object.keys(Store.SUBJECTS).forEach(sub => {
      const p = Store.subj(stu, sub);
      Object.keys(p.review || {}).forEach(id => {
        const r = p.review[id];
        if (r.due <= today) {
          const q = bank(sub).find(x => x.id === id);
          if (q) list.push({ q, subject: sub });
        }
      });
    });
    return list;
  }

  function pickQuestions(stu, n) {
    const p = Store.subj(stu, subject);
    const lv = p.level + 1;   // 学生段位 0~5 ↔ 题库 level 1~6
    const pool = bank().filter(q => q.grade === stu.grade && q.level === lv);
    const wrongIds = p.wrongPool || [];
    // 错题 tag 出题权重 ×2（自适应：薄弱点更多练）
    const wrongTags = {};
    pool.forEach(q => { if (wrongIds.indexOf(q.id) >= 0) wrongTags[q.tag] = (wrongTags[q.tag] || 0) + 1; });
    const weighted = [];
    pool.forEach(q => { weighted.push(q); if (wrongTags[q.tag]) weighted.push(q); });

    // 1) 错题池优先（同 tag 换题重现，最多 2 题）
    let qs = [];
    Object.keys(wrongTags).slice(0, 2).forEach(t => {
      const cand = weighted.filter(q => q.tag === t && (p.recentQs || []).indexOf(q.id) < 0);
      if (cand.length) qs.push(cand[Math.floor(Math.random() * cand.length)]);
    });
    // 2) 加权随机补足（避开最近出过的）
    const recent = p.recentQs || [];
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
    if (Store.autoRead()) TTS.speak(cur.speak || cur.q);
  }

  function answer(stu, val) {
    total++;
    const ok = (String(val) === String(cur.a));
    const tag = cur.tag;
    const subjKey = mode === 'review' ? cur.subject : subject;
    const p = Store.subj(stu, subjKey);
    if (mode === 'review') {
      if (ok) {
        correct++; streak++;
        TTS.praise();
        Store.updateCurrent(s => advanceReview(s, subjKey, cur.id));
      } else {
        streak = 0;
        TTS.speak('再想一想。' + (cur.wrongReasons && cur.wrongReasons[0] ? cur.wrongReasons[0] : ''));
        queue.push(cur);   // 复习答错：当场再问一次
        Store.updateCurrent(s => resetReview(s, subjKey, cur.id));
      }
      onUI(cur, null, { ok, val: val === null ? null : String(val) });
      return;
    }
    const isMastery = (p.wrongPool || []).some(id => id === cur.id) ||
                      bank().some(q => q.grade === stu.grade && q.level === p.level + 1 &&
                                       q.tag === tag && p.wrongPool.indexOf(q.id) >= 0);
    if (ok) {
      correct++; streak++;
      TTS.praise();
      // 精通出池：错题 tag 连对 2 次 → 该 tag 全部移出错题池（含复习队列）
      if (isMastery) {
        Store.updateCurrent(s => {
          const sp = Store.subj(s, subject);
          sp.tagStreaks[tag] = (sp.tagStreaks[tag] || 0) + 1;
          if (sp.tagStreaks[tag] >= 2) {
            const idsOfTag = bank().filter(q => q.grade === s.grade && q.level === sp.level + 1 && q.tag === tag)
                                   .map(q => q.id);
            sp.wrongPool = (sp.wrongPool || []).filter(id => idsOfTag.indexOf(id) < 0);
            idsOfTag.forEach(id => delete sp.review[id]);
            delete sp.tagStreaks[tag];
          }
        });
      }
    } else {
      streak = 0;
      TTS.speak('再想一想。' + (cur.wrongReasons && cur.wrongReasons[0] ? cur.wrongReasons[0] : ''));
      // 错题当场换数字重现：同 tag 下一题插到队尾
      const pool = bank().filter(q => q.grade === stu.grade && q.level === p.level + 1 && q.tag === tag && q.id !== cur.id);
      if (pool.length) queue.push(pool[Math.floor(Math.random() * pool.length)]);
      // 记入待巩固池 + 排入复习计划（明天到期）
      Store.updateCurrent(s => resetReview(s, subject, cur.id, true));
    }
    onUI(cur, null, { ok, val: val === null ? null : String(val) });
  }

  /** 复习答对：升一盒；升出第 5 盒 = 精通，移出错题池和复习队列 */
  function advanceReview(s, subjKey, id) {
    const p = Store.subj(s, subjKey);
    const r = (p.review || {})[id];
    if (!r) return;
    r.box++;
    if (r.box >= Store.REVIEW_BOXES.length) {
      delete p.review[id];
      p.wrongPool = (p.wrongPool || []).filter(x => x !== id);
    } else {
      r.due = Store.day() + Store.REVIEW_BOXES[r.box - 1];
    }
  }
  /** 答错/新错题：回盒底，明天到期 */
  function resetReview(s, subjKey, id, newWrong) {
    const p = Store.subj(s, subjKey);
    p.review = p.review || {};
    p.review[id] = { box: 0, due: Store.day() + 1 };
    if (newWrong) {
      p.wrongPool = (p.wrongPool || []).filter(x => x !== id);
      p.wrongPool.push(id);
      if (p.wrongPool.length > 30) {
        const drop = p.wrongPool.shift();
        delete p.review[drop];
      }
      const tag = (bank(subjKey).find(q => q.id === id) || {}).tag;
      if (tag) p.tagStreaks[tag] = 0;
    }
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

  function reset() { queue = []; cur = null; streak = 0; correct = 0; total = 0; queueTotal = 0; }

  const Quiz = {
    start(stu, subjName, ui, end) {
      mode = 'round';
      subject = subjName;
      loadBank(() => {
        reset();
        onUI = ui; onEnd = end;
        queue = pickQuestions(stu, PER_ROUND);
        // recentQs 记录
        Store.updateCurrent(s => {
          const p = Store.subj(s, subject);
          p.recentQs = queue.map(q => q.id);
        });
        showQuestion(stu);
      });
    },
    /** 今日复习：跨学科混合，最多 REVIEW_MAX 题 */
    startReview(stu, ui, end) {
      mode = 'review';
      loadAll(() => {
        reset();
        onUI = ui; onEnd = end;
        const due = dueList(stu);
        // 打乱后截取，学科交错
        for (let i = due.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i + 1));
          [due[i], due[j]] = [due[j], due[i]];
        }
        queue = due.slice(0, REVIEW_MAX).map(x => Object.assign({}, x.q, { subject: x.subject }));
        queueTotal = queue.length;
        if (!queueTotal) { if (onEnd) onEnd({ correct: 0, total: 0, passed: true, review: true }); reset(); return; }
        showQuestion(stu);
      });
    },
    /** 预加载全部题库并回调到期题数（大厅卡片用） */
    dueCount(stu, cb) {
      loadAll(() => cb(dueList(stu).length));
    },
    answer(stu, val) { answer(stu, val); },
    next(stu) { next(stu); },
    get current() { return cur; },
    get PER_ROUND() { return PER_ROUND; },
    get TOTAL() { return mode === 'review' ? queueTotal : PER_ROUND; },
    get mode() { return mode; }
  };

  window.Quiz = Quiz;
})();
