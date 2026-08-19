/* storage.js — 多学生档案与进度存取（localStorage） */
(function () {
  'use strict';

  const KEY = 'smallclass.v1';
  const LEVELS = ['青铜', '白银', '黄金', '王者'];
  const MEDALS = ['🔤', '🥈', '🥇', '👑'];
  // 每个年级 4 个段位的口算范围描述（与题库一致）
  const LEVEL_DESC = {
    1: ['10以内加减', '20以内进退位', '50以内加减', '100以内加减'],
    2: ['100以内加减', '表内乘法', '表内除法', '乘除混合'],
    3: ['两位数加减', '口算乘法', '口算除法', '混合与估算'],
    4: ['大数口算', '整十乘除', '乘法估算', '简算凑整'],
    5: ['小数加减', '小数乘除', '简便运算', '混合口算'],
    6: ['分数加减', '分数乘除', '三数互化', '混合口算']
  };

  function migrate(d) {
    if (d.unlockAll === undefined) d.unlockAll = false;
    // 兼容 v1 旧档案
    d.students.forEach(s => {
      if (!s.levelStars) s.levelStars = [Math.min(3, s.level * 3), 0, 0, 0];
      if (!s.tagStreaks) s.tagStreaks = {};
    });
    return d;
  }
  function load() {
    try { return migrate(JSON.parse(localStorage.getItem(KEY)) || { students: [], current: -1, autoRead: true }); }
    catch (e) { return { students: [], current: -1, autoRead: true, unlockAll: false }; }
  }
  function save(db) { localStorage.setItem(KEY, JSON.stringify(db)); }

  function newStudent(name, grade) {
    return {
      name: name, grade: grade, level: 0,        // 0~3 段位
      levelStars: [0, 0, 0, 0],                  // 每段位星级 0~3（3 星升段）
      stars: 0,                                   // 累计星数（贴纸）
      stickers: [],                               // 贴纸 id 列表
      clearedTags: {},                            // 已攻克知识点 tag -> 连对次数
      wrongPool: [],                              // 待巩固题 id（最多 30 条）
      tagStreaks: {},                             // 错题 tag 连对计数（连对 2 次出池）
      recentQs: [],                               // 最近出过的题 id（避免重复）
      todayMins: 0, lastDay: ''                   // 当日学习分钟（20 分钟休息提醒）
    };
  }

  const Store = {
    get db() { return load(); },
    get LEVELS() { return LEVELS; },
    get MEDALS() { return MEDALS; },
    get LEVEL_DESC() { return LEVEL_DESC; },

    students() { return load().students; },
    current() { const d = load(); return d.current >= 0 ? d.students[d.current] : null; },
    setCurrent(i) { const d = load(); d.current = i; save(d); },

    addStudent(name, grade) {
      const d = load();
      d.students.push(newStudent(name, grade));
      d.current = d.students.length - 1;
      save(d);
    },
    removeStudent(i) {
      const d = load();
      d.students.splice(i, 1);
      if (d.current >= d.students.length) d.current = d.students.length - 1;
      save(d);
    },
    setGrade(i, grade) { const d = load(); d.students[i].grade = grade; d.students[i].level = 0; d.students[i].levelStars = [0,0,0,0]; save(d); },

    unlockAll() { return load().unlockAll; },
    setUnlockAll(v) { const d = load(); d.unlockAll = v; save(d); },

    /** 更新当前学生（传入修改函数） */
    updateCurrent(fn) { const d = load(); if (d.current >= 0) { fn(d.students[d.current]); save(d); } },

    autoRead() { return load().autoRead; },
    setAutoRead(v) { const d = load(); d.autoRead = v; save(d); },

    /** 进度码：base64 导出/导入 */
    exportCode() { return btoa(unescape(encodeURIComponent(JSON.stringify(load())))); },
    importCode(code) {
      const data = JSON.parse(decodeURIComponent(escape(atob(code.trim()))));
      if (!data.students) throw new Error('bad code');
      save(data);
    }
  };

  window.Store = Store;
})();
