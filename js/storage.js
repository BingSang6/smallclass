/* storage.js — 多学生档案与进度存取（localStorage） */
(function () {
  'use strict';

  const KEY = 'smallclass.v1';
  const LEVELS = ['青铜', '白银', '黄金', '铂金', '钻石', '王者'];
  const MEDALS = ['🔤', '🥈', '🥇', '💠', '💎', '👑'];
  // 每个年级 6 个段位的口算范围描述（与题库一致）
  const LEVEL_DESC = {
    1: ['20以内加减', '50以内加减', '100以内加减', '100以内进退位', '200以内加减', '200以内进退位'],
    2: ['100以内加减', '表内乘法', '表内除法', '乘除混合', '有余数除法', '乘加减两步'],
    3: ['两位数加减', '几百几十加减', '多位乘一位', '多位除一位', '乘除混合', '估算'],
    4: ['大数口算', '整十乘除', '乘法估算', '简算凑整', '除两位数', '混合两步'],
    5: ['小数加减', '小数乘整数', '小数除整数', '小数点移动', '简便运算', '混合两步'],
    6: ['分数加减', '分数乘法', '分数除法', '倒数与互化', '三数互化', '混合口算']
  };
  const TIER_COUNT = 6;
  // SM-2 简化：记忆盒子间隔（天）——答对升一盒，答错回盒底；升出第 5 盒 = 精通出池
  const REVIEW_BOXES = [1, 3, 7, 14, 30];

  // 学科定义：名称、图标、题库文件、段位描述
  const SUBJECTS = {
    math: {
      name: '数学·口算', icon: '🦁', bank: 'data/banks/math-oral.json',
      levels: LEVELS, medals: MEDALS, levelDesc: LEVEL_DESC
    },
    chinese: {
      name: '语文·字词', icon: '📖', bank: 'data/banks/chinese-words.json',
      levels: LEVELS, medals: MEDALS,
      levelDesc: {
        1: ['会认字', '形近字', '多音字', '词语搭配', '近反义词', '四字词语'],
        2: ['会认字', '形近字', '多音字', '词语搭配', '近反义词', '四字词语'],
        3: ['会认字', '形近字', '多音字', '词语搭配', '近反义词', '成语运用'],
        4: ['易错字', '形近字', '多音字', '词语搭配', '近反义词', '成语运用'],
        5: ['易错字', '形近字', '多音字', '词语搭配', '近反义词', '成语运用'],
        6: ['易错字', '形近字', '多音字', '词语搭配', '近反义词', '成语运用']
      }
    }
  };

  function newSubj() {
    // review: 错题id -> {box: 0~5, due: 天数(自1970起)}
    return { level: 0, levelStars: [0, 0, 0, 0, 0, 0], wrongPool: [], tagStreaks: {}, recentQs: [], review: {} };
  }

  /** v2.5 迁移：没有 review 字段的旧档案 → wrongPool 全部视为今天到期（box 0） */
  function migrateReview(s) {
    Object.keys(s.sub).forEach(k => {
      const p = s.sub[k];
      if (!p.review) p.review = {};
      (p.wrongPool || []).forEach(id => {
        if (!p.review[id]) p.review[id] = { box: 0, due: 0 };
      });
    });
  }

  function migrate(d) {
    if (d.unlockAll === undefined) d.unlockAll = false;
    // 兼容 v1.x 旧档案（单学科字段 → sub.math）
    d.students.forEach(s => {
      if (!s.sub) {
        let ls = [0, 0, 0, 0, 0, 0];
        if (Array.isArray(s.levelStars) && s.levelStars.length === 4) {
          ls = [s.levelStars[0], s.levelStars[1], s.levelStars[2], 0, s.levelStars[3], 0];
        } else if (Array.isArray(s.levelStars)) {
          ls = s.levelStars;
        } else if (s.level) {
          ls = [Math.min(3, s.level * 3), 0, 0, 0, 0, 0];
        }
        let lv = s.level || 0;
        if (lv >= 3 && ls[5] === 0 && ls[4] === 0) lv = Math.min(4, lv + 1); // 王者→钻石
        s.sub = {
          math: { level: lv, levelStars: ls, wrongPool: s.wrongPool || [], tagStreaks: s.tagStreaks || {}, recentQs: s.recentQs || [] },
          chinese: newSubj()
        };
        delete s.level; delete s.levelStars; delete s.wrongPool; delete s.tagStreaks; delete s.recentQs;
      }
      migrateReview(s);
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
      name: name, grade: grade,
      sub: { math: newSubj(), chinese: newSubj() },   // 各学科进度
      stars: 0,                                   // 累计星数（贴纸）
      stickers: [],                               // 贴纸 id 列表
      clearedTags: {},                            // 已攻克知识点 tag -> 连对次数
      todayMins: 0, lastDay: ''                   // 当日学习分钟（20 分钟休息提醒）
    };
  }

  const Store = {
    get db() { return load(); },
    get LEVELS() { return LEVELS; },
    get MEDALS() { return MEDALS; },
    get LEVEL_DESC() { return LEVEL_DESC; },
    get SUBJECTS() { return SUBJECTS; },
    /** 取某学生的某学科进度（迁移保证存在） */
    subj(stu, subject) {
      if (!stu.sub) migrate({ students: [stu], unlockAll: false });
      if (!stu.sub[subject]) stu.sub[subject] = newSubj();
      if (!stu.sub[subject].review) migrateReview(stu);
      return stu.sub[subject];
    },
    get REVIEW_BOXES() { return REVIEW_BOXES; },
    /** 今天的天数序号（本地时区） */
    day() { return Math.floor(Date.now() / 86400000); },

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
    setGrade(i, grade) { const d = load(); const s = d.students[i]; s.grade = grade; s.sub = { math: newSubj(), chinese: newSubj() }; save(d); },

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
