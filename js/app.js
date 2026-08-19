/* app.js — 界面路由与交互（学科大厅 → 学科主页 → 闯关） */
(function () {
  'use strict';

  const $ = id => document.getElementById(id);

  let curSubject = 'math';   // 当前学科

  /* ---------- 屏幕路由 ---------- */
  function go(name) {
    document.querySelectorAll('.screen').forEach(s => s.classList.add('hidden'));
    $('screen-' + name).classList.remove('hidden');
  }

  /* ---------- 屏：欢迎/选学生 ---------- */
  function renderSetup() {
    const list = $('student-list');
    list.innerHTML = '';
    const stus = Store.students();
    if (!stus.length) {
      list.innerHTML = '<p class="sub">还没有同学，点下面的 ➕ 新同学 添加吧</p>';
    }
    stus.forEach((s, i) => {
      const m = Store.subj(s, 'math'), c = Store.subj(s, 'chinese');
      const b = document.createElement('button');
      b.className = 'btn student-btn' + (Store.db.current === i ? ' green' : '');
      b.textContent = '🦁 ' + s.name + '（' + s.grade + '年级·数学' + Store.LEVELS[m.level] +
        '·语文' + Store.LEVELS[c.level] + '）';
      b.onclick = () => { Store.setCurrent(i); init(); };
      list.appendChild(b);
    });
    $('add-form').classList.add('hidden');
  }

  // 年级选择器
  (function () {
    const p = $('grade-picker');
    for (let g = 1; g <= 6; g++) {
      const b = document.createElement('button');
      b.className = 'btn grade-btn';
      b.textContent = g + '年级';
      b.dataset.g = g;
      p.appendChild(b);
    }
  })();
  let pickedGrade = 0;
  $('grade-picker').addEventListener('click', e => {
    const b = e.target.closest('.grade-btn');
    if (!b) return;
    pickedGrade = +b.dataset.g;
    $('grade-picker').querySelectorAll('.grade-btn').forEach(x => x.classList.toggle('sel', x === b));
  });

  $('btn-add-student').onclick = () => {
    const f = $('add-form');
    f.classList.toggle('hidden');
    if (!f.classList.contains('hidden')) $('inp-name').focus();
  };
  $('btn-create').onclick = () => {
    const name = $('inp-name').value.trim();
    if (!name || !pickedGrade) { alert('请填写名字并选择年级'); return; }
    Store.addStudent(name, pickedGrade);
    $('inp-name').value = '';
    init();
  };

  /* ---------- 通用小组件 ---------- */
  function starStr(lvStars) {
    return '★'.repeat(lvStars) + '☆'.repeat(3 - Math.min(3, lvStars));
  }
  function unlocked(stu, sub, lv) {
    if (Store.unlockAll()) return true;
    const p = Store.subj(stu, sub);
    if (lv <= p.level) return true;
    if (lv === p.level + 1 && p.levelStars[p.level] >= 1) return true;
    return false;
  }

  /* ---------- 屏：学科大厅 ---------- */
  function renderHub(stu) {
    $('hub-name').textContent = stu.name;
    $('hub-info').textContent = (stu.stars || 0) + '⭐ · ' + (stu.stickers || []).length + ' 枚贴纸';
    // 🌅 今日复习卡片（到期错题 > 0 才显示）
    const rb = $('btn-review');
    Quiz.dueCount(stu, n => {
      if (n > 0) {
        rb.textContent = '🌅 今日复习 · ' + n + ' 题';
        rb.classList.remove('hidden');
      } else {
        rb.classList.add('hidden');
      }
    });
    const grid = $('subject-grid');
    grid.innerHTML = '';
    const extra = [
      { key: 'more', name: '更多学科', icon: '➕', desc: '敬请期待' }
    ];
    Object.keys(Store.SUBJECTS).concat(extra.map(e => e.key)).forEach(key => {
      const meta = Store.SUBJECTS[key] || extra.find(e => e.key === key);
      const b = document.createElement('button');
      if (Store.SUBJECTS[key]) {
        const p = Store.subj(stu, key);
        b.className = 'subject-card';
        b.innerHTML = '<div class="sc-icon">' + meta.icon + '</div>' +
          '<div class="sc-name">' + meta.name + '</div>' +
          '<div class="sc-desc">' + Store.LEVELS[p.level] + starStr(p.levelStars[p.level]) + '</div>';
        b.onclick = () => enterSubject(key);
      } else {
        b.className = 'subject-card locked';
        b.innerHTML = '<div class="sc-icon">' + meta.icon + '</div>' +
          '<div class="sc-name">' + meta.name + '</div>' +
          '<div class="sc-desc">🔒 ' + meta.desc + '</div>';
      }
      grid.appendChild(b);
    });
  }

  function enterSubject(sub) {
    curSubject = sub;
    renderHome(Store.current());
    go('home');
  }

  /* ---------- 屏：学科主页（段位地图） ---------- */
  function renderHome(stu) {
    const meta = Store.SUBJECTS[curSubject];
    const p = Store.subj(stu, curSubject);
    $('hello-avatar').textContent = meta.icon;
    $('hello-name').textContent = meta.name;
    $('hello-info').textContent = Store.MEDALS[p.level] + ' ' + Store.LEVELS[p.level] + starStr(p.levelStars[p.level]) +
      ' · ' + (stu.stars || 0) + '⭐';
    renderReadToggle();
    // 挑战模式：白银段位（level≥1）解锁
    $('btn-challenge').style.display = p.level >= 1 ? '' : 'none';
    // 单元巩固：该年级有单元题库才显示
    $('btn-units').style.display = meta.units && meta.units[stu.grade] ? '' : 'none';
    const map = $('level-map');
    map.innerHTML = '';
    const desc = meta.levelDesc[stu.grade];
    Store.LEVELS.forEach((lname, lv) => {
      const open = unlocked(stu, curSubject, lv);
      const b = document.createElement('button');
      b.className = 'level-card' + (open ? '' : ' locked') + (lv === p.level ? ' sel' : '');
      b.innerHTML = '<div class="lv-badge">' + Store.MEDALS[lv] + '</div>' +
        '<div class="lv-name">' + lname + starStr(p.levelStars[lv]) + '</div>' +
        '<div class="lv-desc">' + (open ? '' : '🔒 ') + desc[lv] + '</div>';
      if (open) b.onclick = () => startRound(lv);
      map.appendChild(b);
    });
  }
  function renderReadToggle() {
    $('btn-read-toggle').textContent = Store.autoRead() ? '🔊' : '🔇';
  }

  /* ---------- 闯关 ---------- */
  let restTimer = null;
  let challenge = false;      // 挑战模式：每题 10 秒倒计时
  let qTimer = null;          // 单题倒计时 interval
  let qT0 = 0;                // 本题开始时间（算⚡快）

  function stopQTimer() {
    clearInterval(qTimer);
    $('quiz-timer').classList.add('hidden');
    $('quiz-timer').classList.remove('urgent');
  }

  function startQTimer() {
    stopQTimer();
    if (!challenge) return;
    let left = 10;
    const el = $('quiz-timer');
    el.textContent = '⏱ ' + left;
    el.classList.remove('hidden');
    qTimer = setInterval(() => {
      left--;
      el.textContent = '⏱ ' + left;
      el.classList.toggle('urgent', left <= 3);
      if (left <= 0) {
        clearInterval(qTimer);
        document.querySelectorAll('.opt-btn').forEach(x => x.disabled = true);
        Quiz.answer(Store.current(), null);   // 超时算错
      }
    }, 1000);
  }

  function startRestTimer() {
    clearInterval(restTimer);
    Store.updateCurrent(s => {
      const today = new Date().toISOString().slice(0, 10);
      if (s.lastDay !== today) { s.lastDay = today; s.todayMins = 0; }
    });
    restTimer = setInterval(() => {
      Store.updateCurrent(s => { s.todayMins = (s.todayMins || 0) + 0.25; });
      const cur = Store.current();
      if (cur && (cur.todayMins || 0) >= 20) {
        $('rest-overlay').classList.remove('hidden');
        TTS.speak('你已经学了二十分钟啦，休息一下眼睛吧！');
        clearInterval(restTimer);
      }
    }, 15000);
  }

  function roundUI(idx, q, opts, result) {
    if (opts) {
      const tot = Quiz.TOTAL;
      $('quiz-progress').textContent = '⭐'.repeat(Math.max(0, idx - 1)) + '☆'.repeat(Math.max(0, tot - idx + 1));
      $('question-text').textContent = q.q;
      qT0 = Date.now();
      startQTimer();
      const box = $('options');
      box.innerHTML = '';
      $('feedback').classList.add('hidden');
      opts.forEach(o => {
        const b = document.createElement('button');
        b.className = 'opt-btn';
        b.textContent = o;
        b.onclick = () => {
          box.querySelectorAll('.opt-btn').forEach(x => x.disabled = true);
          Quiz.answer(Store.current(), o);
        };
        box.appendChild(b);
      });
    } else if (result) {
      stopQTimer();
      const box = $('options');
      box.querySelectorAll('.opt-btn').forEach(b => {
        if (b.textContent === String(q.a)) b.classList.add('correct');
        else if (result.val && b.textContent === result.val) b.classList.add('wrong');
      });
      if (result.ok) {
        const fast = challenge && (Date.now() - qT0) < 4000;
        const fb = $('feedback');
        fb.textContent = fast ? '⚡ 神速！答对啦！' : '✅ 太棒了！';
        fb.className = 'feedback ok';
        setTimeout(() => Quiz.next(Store.current()), 900);
      } else {
        $('wrong-reason').innerHTML = q.q + ' = <b>' + q.a + '</b><br>' +
          (result.val === null ? '时间到啦，没关系，下次算快一点。' : '') +
          (q.wrongReasons && q.wrongReasons[0] ? q.wrongReasons[0] : '再想一想哦。') +
          '<br>' + (Quiz.mode === 'review' ? '这题一会儿还会再问一次哦' : '稍后会再练一道类似的题哦');
        $('wrong-overlay').classList.remove('hidden');
      }
    }
  }

  function startRound(lv, isChallenge) {
    lastWasReview = false;
    lastWasUnit = false;
    challenge = !!isChallenge;
    if (typeof lv === 'number') Store.updateCurrent(s => { Store.subj(s, curSubject).level = lv; });
    const stu = Store.current();
    const p0 = Store.subj(stu, curSubject);
    const meta = Store.SUBJECTS[curSubject];
    go('quiz');
    $('quiz-level').textContent = (challenge ? '⏱挑战 ' : '') + meta.icon + Store.MEDALS[p0.level] + ' ' + Store.LEVELS[p0.level] + starStr(p0.levelStars[p0.level]);
    $('wrong-overlay').classList.add('hidden');
    startRestTimer();
    let idx = 0;
    Quiz.start(stu, curSubject,
      (q, opts, result) => { if (opts) idx++; roundUI(idx, q, opts, result); },
      r => {
        clearInterval(restTimer);
        stopQTimer();
        // 得星：对 5 题得 2 星，对 4 题得 1 星
        const win = r.correct >= 4 ? (r.correct >= 5 ? 2 : 1) : 0;
        if (win > 0) {
          Store.updateCurrent(s => {
            const p = Store.subj(s, curSubject);
            p.levelStars[p.level] = Math.min(3, p.levelStars[p.level] + win);
            s.stars = (s.stars || 0) + r.correct;
            if (p.levelStars[p.level] >= 3 && p.level < 5) p.level++;
            if (s.stickers.length < 60) s.stickers.push(String(p.level));
          });
          const s2 = Store.current();
          const p2 = Store.subj(s2, curSubject);
          $('result-title').textContent = '🎉 过关！获得 ' + '⭐'.repeat(win);
          $('result-detail').textContent = '答对 ' + r.correct + ' / ' + r.total + ' 题' +
            (p2.level > p0.level ? '，升到' + Store.LEVELS[p2.level] + '段位啦！' : '，再得星就能升级哦');
          $('result-sticker').textContent = Store.MEDALS[p2.level];
        } else {
          $('result-title').textContent = '💪 快要过关啦！';
          $('result-detail').textContent = '答对 ' + r.correct + ' / ' + r.total + ' 题，再对一题就能得星，再试一次一定行！';
          $('result-sticker').textContent = '🌟';
        }
        go('result');
      }
    );
  }

  /* ---------- 单元巩固（v2.6） ---------- */
  function renderUnits() {
    const stu = Store.current();
    const meta = Store.SUBJECTS[curSubject];
    const list = $('unit-list');
    list.innerHTML = '';
    meta.units[stu.grade].forEach(name => {
      const b = document.createElement('button');
      b.className = 'btn big-btn-list-item';
      b.textContent = name;
      b.onclick = () => startUnit(name);
      list.appendChild(b);
    });
    go('units');
  }
  $('btn-units').onclick = renderUnits;
  $('btn-units-back').onclick = () => enterSubject(curSubject);

  function startUnit(name) {
    lastWasReview = false;
    lastWasUnit = true;
    challenge = false;
    const stu = Store.current();
    go('quiz');
    $('quiz-level').textContent = '📚 ' + name;
    $('wrong-overlay').classList.add('hidden');
    startRestTimer();
    let idx = 0;
    Quiz.start(stu, curSubject,
      (q, opts, result) => { if (opts) idx++; roundUI(idx, q, opts, result); },
      r => {
        clearInterval(restTimer);
        stopQTimer();
        Store.updateCurrent(s => { s.stars = (s.stars || 0) + r.correct; });
        if (r.correct >= r.total - 1) {
          if (Store.current().stickers.length < 60) Store.updateCurrent(s => { s.stickers.push('U' + name.slice(1, 3)); });
          $('result-title').textContent = '🎉 这个单元掌握得很好！';
          $('result-sticker').textContent = '📚';
        } else {
          $('result-title').textContent = '💪 单元查漏完成！';
          $('result-sticker').textContent = '🔍';
        }
        $('result-detail').textContent = name + '：答对 ' + r.correct + ' / ' + r.total +
          ' 题。错的题明天会出现在「今日复习」里哦。';
        go('result');
      },
      { unit: name }
    );
  }

  /* ---------- 今日复习 ---------- */
  let lastWasReview = false;
  let lastWasUnit = false;

  function startReview() {
    lastWasReview = true;
    challenge = false;
    const stu = Store.current();
    go('quiz');
    $('quiz-level').textContent = '🌅 今日复习';
    $('wrong-overlay').classList.add('hidden');
    startRestTimer();
    let idx = 0;
    Quiz.startReview(stu,
      (q, opts, result) => { if (opts) idx++; roundUI(idx, q, opts, result); },
      r => {
        clearInterval(restTimer);
        stopQTimer();
        if (r.total === 0) { init(); return; }   // 没有到期题
        Store.updateCurrent(s => { s.stars = (s.stars || 0) + r.correct; });
        $('result-title').textContent = '🎉 复习完成！';
        $('result-detail').textContent = '复习了 ' + r.total + ' 题，记住 ' + r.correct + ' 题。记不牢的题明天还会再来哦。';
        $('result-sticker').textContent = '🌅';
        go('result');
      }
    );
  }
  $('btn-review').onclick = startReview;

  /* ---------- 结算 / 贴纸册 ---------- */
  $('btn-next').onclick = () => {
    if (lastWasReview) { init(); return; }   // 复习完回大厅
    if (lastWasUnit) { renderUnits(); return; }   // 单元巩固完回单元列表
    startRound(Store.subj(Store.current(), curSubject).level);   // 同段位再来一轮
  };
  $('btn-home').onclick = () => { lastWasReview ? init() : enterSubject(curSubject); };
  $('btn-wrong-ok').onclick = () => {
    $('wrong-overlay').classList.add('hidden');
    Quiz.next(Store.current());
  };

  function openAlbum() {
    const stu = Store.current();
    const grid = $('album-grid');
    grid.innerHTML = '';
    const icons = ['⭐', '🌟', '🏅', '🏆'];
    (stu.stickers || []).forEach((s, i) => {
      const d = document.createElement('div');
      d.className = 'sticker';
      d.textContent = icons[Math.min(3, +s || 0)];
      d.style.animationDelay = (i % 10) * 0.05 + 's';
      grid.appendChild(d);
    });
    if (!stu.stickers || !stu.stickers.length) {
      grid.innerHTML = '<p class="sub">还没有贴纸，闯关赢贴纸吧！</p>';
    }
    go('album');
  }
  $('btn-album').onclick = openAlbum;
  $('btn-album2').onclick = openAlbum;
  $('btn-album-back').onclick = () => init();

  /* ---------- 其他按钮 ---------- */
  $('btn-go').onclick = () => startRound();
  $('btn-challenge').onclick = () => startRound(Store.subj(Store.current(), curSubject).level, true);
  $('btn-switch').onclick = () => { renderSetup(); go('setup'); };
  $('btn-switch2').onclick = () => { renderSetup(); go('setup'); };
  $('btn-back-hub').onclick = () => init();
  $('btn-read-toggle').onclick = () => { Store.setAutoRead(!Store.autoRead()); renderReadToggle(); };
  $('btn-speak').onclick = () => { const q = Quiz.current; if (q) TTS.speak(q.speak || q.q); };
  $('btn-rest-ok').onclick = () => { $('rest-overlay').classList.add('hidden'); init(); };

  /* ---------- 家长设置（含 导出错题本） ---------- */
  function wrongReport() {
    const stu = Store.current();
    const lines = [];
    lines.push('# 学生档案：' + stu.name);
    lines.push('- 年级: ' + stu.grade + '年级（小课堂 App 自动导出）');
    lines.push('- 累计星星: ' + (stu.stars || 0));
    Object.keys(Store.SUBJECTS).forEach(sub => {
      const meta = Store.SUBJECTS[sub];
      const p = Store.subj(stu, sub);
      lines.push('');
      lines.push('## ' + meta.name + '（' + Store.LEVELS[p.level] + '·' + meta.levelDesc[stu.grade][p.level] + '）');
      const byTag = {};
      (p.wrongPool || []).forEach(id => {
        const meta2 = Store.SUBJECTS[sub];
        // 从缓存题库找不到就跳过（题库可能未加载）
        const q = (window.QuizBank && window.QuizBank[sub] || []).find(x => x.id === id);
        if (q) (byTag[q.tag] = byTag[q.tag] || []).push(q);
      });
      if (!Object.keys(byTag).length) {
        lines.push('- 错题本：暂无错题，状态很好！');
      } else {
        lines.push('### 错题本（待巩固）');
        Object.keys(byTag).forEach(tag => {
          lines.push('');
          lines.push('#### ' + tag + '（' + byTag[tag].length + ' 题）');
          byTag[tag].slice(-10).forEach(q => {
            lines.push('- ' + q.q + ' → ' + q.a + '　提示：' + (q.wrongReasons && q.wrongReasons[0] || ''));
          });
        });
      }
    });
    lines.push('');
    lines.push('<!-- 复制以上内容发给 AI 助教（primary-tutor-skill 环境）即可针对性讲解、生成打印卷 -->');
    return lines.join('\n');
  }

  function renderSettings() {
    const body = $('settings-body');
    body.innerHTML = '<h3>学生管理</h3>';
    Store.students().forEach((s, i) => {
      const row = document.createElement('div');
      row.className = 'settings-row';
      const info = document.createElement('span');
      const m = Store.subj(s, 'math'), c = Store.subj(s, 'chinese');
      info.textContent = s.name + ' · ' + s.grade + '年级 · 数学' + Store.LEVELS[m.level] +
        '·语文' + Store.LEVELS[c.level] + ' · 共' + ((m.wrongPool || []).length + (c.wrongPool || []).length) + '题待巩固';
      row.appendChild(info);
      // 改年级
      const g = document.createElement('select');
      for (let x = 1; x <= 6; x++) {
        const o = document.createElement('option');
        o.value = x; o.textContent = x + '年级';
        if (s.grade === x) o.selected = true;
        g.appendChild(o);
      }
      g.onchange = () => { if (confirm('改年级会重置全部学科段位，确定？')) { Store.setGrade(i, +g.value); init(); } };
      row.appendChild(g);
      // 删除
      const del = document.createElement('button');
      del.className = 'btn tiny';
      del.textContent = '🗑';
      del.onclick = () => { if (confirm('删除 ' + s.name + ' 的全部进度？')) { Store.removeStudent(i); init(); } };
      row.appendChild(del);
      body.appendChild(row);
    });

    // 段位全部解锁（家长开关）
    const h0 = document.createElement('h3');
    h0.textContent = '段位设置';
    body.appendChild(h0);
    const sw = document.createElement('button');
    sw.className = 'btn small' + (Store.unlockAll() ? ' green' : '');
    sw.textContent = Store.unlockAll() ? '🔓 全部解锁：开（点击关闭）' : '🔒 全部解锁：关（点击开启）';
    sw.onclick = () => { Store.setUnlockAll(!Store.unlockAll()); renderSettings(); };
    body.appendChild(sw);

    // 导出错题本
    const h = document.createElement('h3');
    h.textContent = '导出错题本（发给 AI 助教做针对性讲解/打印卷）';
    body.appendChild(h);
    const ta = document.createElement('textarea');
    ta.id = 'export-ta';
    ta.readOnly = true;
    ta.value = wrongReport();
    body.appendChild(ta);
    const cp = document.createElement('button');
    cp.className = 'btn small';
    cp.textContent = '📋 复制';
    cp.onclick = () => {
      ta.select();
      try { document.execCommand('copy'); cp.textContent = '✅ 已复制'; } catch (e) {}
      setTimeout(() => cp.textContent = '📋 复制', 1500);
    };
    body.appendChild(cp);
  }
  $('btn-settings').onclick = () => {
    // 先把两科题库都加载好，导出错题本才能带上题目内容
    Object.keys(Store.SUBJECTS).forEach(sub => {
      fetch(Store.SUBJECTS[sub].bank).then(r => r.json()).then(j => {
        window.QuizBank = window.QuizBank || {};
        window.QuizBank[sub] = j;
      }).catch(() => {});
    });
    renderSettings();
    go('settings');
  };
  $('btn-settings-back').onclick = () => init();

  /* ---------- 入口 ---------- */
  function init() {
    const stu = Store.current();
    if (!stu) { renderSetup(); go('setup'); }
    else { renderHub(stu); go('hub'); }
  }
  init();
})();
