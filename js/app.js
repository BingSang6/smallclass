/* app.js — 界面路由与交互（与 index.html 的实际 ID 一一对应） */
(function () {
  'use strict';

  const $ = id => document.getElementById(id);

  /* ---------- 题库（导出错题本需要） ---------- */
  let bank = [];
  fetch('data/banks/math-oral.json').then(r => r.json()).then(j => { bank = j; }).catch(() => {});

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
      const b = document.createElement('button');
      b.className = 'btn student-btn' + (Store.db.current === i ? ' green' : '');
      b.textContent = '🦁 ' + s.name + '（' + s.grade + '年级·' + Store.LEVELS[s.level] + '）';
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

  /* ---------- 屏：首页 ---------- */
  function starStr(lvStars) {
    return '★'.repeat(lvStars) + '☆'.repeat(3 - lvStars);
  }
  // 段位解锁规则：已到达的 / 本段位拿到 1 星解锁下一段位 / 家长开「全部解锁」
  function unlocked(stu, lv) {
    if (Store.unlockAll()) return true;
    if (lv <= stu.level) return true;
    if (lv === stu.level + 1 && (stu.levelStars || [])[stu.level] >= 1) return true;
    return false;
  }

  function renderHome(stu) {
    $('hello-name').textContent = stu.name;
    $('hello-info').textContent = Store.MEDALS[stu.level] + ' ' + Store.LEVELS[stu.level] + starStr((stu.levelStars || [])[stu.level] || 0) +
      ' · ' + (stu.stars || 0) + '⭐';
    renderReadToggle();
    const map = $('level-map');
    map.innerHTML = '';
    Store.LEVELS.forEach((lname, lv) => {
      const desc = Store.LEVEL_DESC[stu.grade][lv];
      const open = unlocked(stu, lv);
      const b = document.createElement('button');
      b.className = 'level-card' + (open ? '' : ' locked') + (lv === stu.level ? ' sel' : '');
      b.innerHTML = '<div class="lv-badge">' + Store.MEDALS[lv] + '</div>' +
        '<div class="lv-name">' + lname + starStr((stu.levelStars || [])[lv] || 0) + '</div>' +
        '<div class="lv-desc">' + (open ? '' : '🔒 ') + desc + '</div>';
      if (open) b.onclick = () => startRound(lv);
      map.appendChild(b);
    });
  }
  function renderReadToggle() {
    $('btn-read-toggle').textContent = Store.autoRead() ? '🔊' : '🔇';
  }

  /* ---------- 闯关 ---------- */
  let restTimer = null;

  function startRestTimer() {
    clearInterval(restTimer);
    Store.updateCurrent(s => {
      const today = new Date().toISOString().slice(0, 10);
      if (s.lastDay !== today) { s.lastDay = today; s.todayMins = 0; }
    });
    const t0 = Date.now();
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
      $('quiz-progress').textContent = '⭐'.repeat(Math.max(0, idx - 1)) + '☆'.repeat(Math.max(0, Quiz.PER_ROUND - idx + 1));
      $('question-text').textContent = q.q;
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
      const box = $('options');
      box.querySelectorAll('.opt-btn').forEach(b => {
        if (b.textContent === String(q.a)) b.classList.add('correct');
        else if (b.textContent === result.val) b.classList.add('wrong');
      });
      if (result.ok) {
        const fb = $('feedback');
        fb.textContent = '✅ 太棒了！';
        fb.className = 'feedback ok';
        setTimeout(() => Quiz.next(Store.current()), 900);
      } else {
        // 错因弹层 + 错题当场重现已由 quiz.js 排队
        $('wrong-reason').innerHTML = q.q + ' = <b>' + q.a + '</b><br>' +
          (q.wrongReasons && q.wrongReasons[0] ? q.wrongReasons[0] : '再算一遍试试。') +
          '<br>稍后会再练一道类似的题哦';
        $('wrong-overlay').classList.remove('hidden');
      }
    }
  }

  function startRound(lv) {
    if (typeof lv === 'number') Store.updateCurrent(s => { s.level = lv; });
    const stu = Store.current();
    go('quiz');
    $('quiz-level').textContent = Store.MEDALS[stu.level] + ' ' + Store.LEVELS[stu.level] + starStr((stu.levelStars || [])[stu.level] || 0);
    $('wrong-overlay').classList.add('hidden');
    startRestTimer();
    let idx = 0;
    Quiz.start(stu,
      (q, opts, result) => { if (opts) idx++; roundUI(idx, q, opts, result); },
      r => {
        clearInterval(restTimer);
        // 得星：对 5 题得 2 星，对 4 题得 1 星
        const win = r.correct >= 4 ? (r.correct >= 5 ? 2 : 1) : 0;
        if (win > 0) {
          Store.updateCurrent(s => {
            s.levelStars = s.levelStars || [0, 0, 0, 0];
            s.levelStars[s.level] = Math.min(3, s.levelStars[s.level] + win);
            s.stars = (s.stars || 0) + r.correct;
            // 3 星升段
            if (s.levelStars[s.level] >= 3 && s.level < 3) s.level++;
            if (s.stickers.length < 60) s.stickers.push(String(s.level));
          });
          const s2 = Store.current();
          $('result-title').textContent = '🎉 过关！获得 ' + '⭐'.repeat(win);
          $('result-detail').textContent = '答对 ' + r.correct + ' / ' + r.total + ' 题' +
            (s2.level > stu.level ? '，升到' + Store.LEVELS[s2.level] + '段位啦！' : '，再得星就能升级哦');
          $('result-sticker').textContent = Store.MEDALS[s2.level];
        } else {
          $('result-title').textContent = '💪 快要过关啦！';
          $('result-detail').textContent = '答对 ' + r.correct + ' / ' + r.total + ' 题，再对一题就能得星，再试一次一定行！';
          $('result-sticker').textContent = '🌟';
        }
        go('result');
      }
    );
  }

  /* ---------- 结算 / 贴纸册 ---------- */
  $('btn-next').onclick = () => startRound(Store.current().level);   // 同段位再来一轮
  $('btn-home').onclick = () => init();
  $('btn-wrong-ok').onclick = () => {
    $('wrong-overlay').classList.add('hidden');
    Quiz.next(Store.current());
  };

  $('btn-album').onclick = () => {
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
  };
  $('btn-album-back').onclick = () => init();

  /* ---------- 其他按钮 ---------- */
  $('btn-go').onclick = () => startRound();
  $('btn-switch').onclick = () => { renderSetup(); go('setup'); };
  $('btn-read-toggle').onclick = () => { Store.setAutoRead(!Store.autoRead()); renderReadToggle(); };
  $('btn-speak').onclick = () => { const q = Quiz.current; if (q) TTS.speak(q.q); };
  $('btn-rest-ok').onclick = () => { $('rest-overlay').classList.add('hidden'); init(); };

  /* ---------- 家长设置（含 导出错题本） ---------- */
  function wrongReport() {
    const stu = Store.current();
    const lines = [];
    const byTag = {};
    (stu.wrongPool || []).forEach(id => {
      const q = bank.find(x => x.id === id);
      if (!q) return;
      (byTag[q.tag] = byTag[q.tag] || []).push(q);
    });
    lines.push('# 学生档案：' + stu.name);
    lines.push('- 年级: ' + stu.grade + '年级（口算 App 自动导出）');
    lines.push('- 当前段位: ' + Store.LEVELS[stu.level] + '（' + Store.LEVEL_DESC[stu.grade][stu.level] + '）');
    lines.push('- 累计星星: ' + (stu.stars || 0));
    lines.push('');
    lines.push('## 错题本（待巩固）');
    if (!Object.keys(byTag).length) lines.push('（暂无错题，状态很好！）');
    Object.keys(byTag).forEach(tag => {
      lines.push('');
      lines.push('### ' + tag + '（' + byTag[tag].length + ' 题）');
      byTag[tag].slice(-10).forEach(q => {
        lines.push('- ' + q.q + ' = ' + q.a + '　易错点：' + (q.wrongReasons && q.wrongReasons[0] || ''));
      });
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
      info.textContent = s.name + ' · ' + s.grade + '年级 · ' + Store.LEVELS[s.level] + ' · ' + (s.wrongPool || []).length + '题待巩固';
      row.appendChild(info);
      // 改年级
      const g = document.createElement('select');
      for (let x = 1; x <= 6; x++) {
        const o = document.createElement('option');
        o.value = x; o.textContent = x + '年级';
        if (s.grade === x) o.selected = true;
        g.appendChild(o);
      }
      g.onchange = () => { if (confirm('改年级会重置段位，确定？')) Store.setGrade(i, +g.value); init(); };
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
  $('btn-settings').onclick = () => { renderSettings(); go('settings'); };
  $('btn-settings-back').onclick = () => init();

  /* ---------- 入口 ---------- */
  function init() {
    const stu = Store.current();
    if (!stu) { renderSetup(); go('setup'); }
    else { renderHome(stu); go('home'); }
  }
  init();
})();
