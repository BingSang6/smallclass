/* storage.js — 多学生档案与进度存取（localStorage） */
(function () {
  'use strict';

  const KEY = 'smallclass.v1';
  const LEVELS = ['青铜', '白银', '黄金', '铂金', '钻石', '王者'];
  const MEDALS = ['🔤', '🥈', '🥇', '💠', '💎', '👑'];
  // 每个年级 6 个段位的口算范围描述（与题库一致）
  const LEVEL_DESC = {
    1: ['20以内进退位', '50以内加减', '50以内进退位', '100以内加减', '100以内进退位', '200以内混合'],
    2: ['100以内加减', '表内乘法', '表内除法', '乘除混合', '有余数除法', '乘加减两步'],
    3: ['两位数加减', '几百几十加减', '多位乘一位', '多位除一位', '乘除混合', '两步计算'],
    4: ['大数口算', '整十乘除', '整百乘整十', '简算凑整', '除两位数', '混合两步'],
    5: ['小数加减', '小数乘整数', '小数除整数', '小数点移动', '简便运算', '混合两步'],
    6: ['分数加减', '分数乘法', '分数除法', '倒数与互化', '三数互化', '混合口算']
  };
  const TIER_COUNT = 6;
  // SM-2 简化：记忆盒子间隔（天）——答对升一盒，答错回盒底；升出第 5 盒 = 精通出池
  const REVIEW_BOXES = [1, 3, 7, 14, 30];

  // 学科定义：名称、图标、题库文件、段位描述
  const SUBJECTS = {
    math: {
      name: '数学·口算', short: '口算', icon: '🦁', bank: 'data/banks/math-oral.json',
      levels: LEVELS, medals: MEDALS, levelDesc: LEVEL_DESC,
      // v2.6 单元巩固：按年级的单元题库 + 单元名（题源 primary-tutor-skill 知识库）
      unitsBank: 'data/banks/math-g4-units.json',
      units: {
        4: ['第一单元 认识更大的数', '第二单元 线与角', '第三单元 乘法', '第四单元 运算律',
            '第五单元 方向与位置', '第六单元 除法', '第七单元 生活中的负数', '第八单元 可能性']
      },
      // v3.2 专题训练：单位换算 + 解决问题（gen_math_topics.py，题名 = q.unit）
      topicsBank: 'data/banks/math-topics.json',
      topics: {
        2: ['专题·人民币'],
        3: ['专题·长度', '专题·质量', '专题·时间', '专题·解决问题'],
        4: ['专题·面积', '专题·解决问题'],
        5: ['专题·体积与容积', '专题·解决问题'],
        6: ['专题·解决问题']
      }
    },
    chinese: {
      name: '语文·字词', short: '字词', icon: '📖', bank: 'data/banks/chinese-words.json', group: '语文',
      levels: LEVELS, medals: MEDALS,
      levelDesc: {
        1: ['会认字', '形近字', '多音字', '词语搭配', '近反义词', '四字词语'],
        2: ['会认字', '形近字', '多音字', '词语搭配', '近反义词', '四字词语'],
        3: ['会认字', '形近字', '多音字', '词语搭配', '近反义词', '成语运用'],
        4: ['易错字', '形近字', '多音字', '词语搭配', '近反义词', '成语运用'],
        5: ['易错字', '形近字', '多音字', '词语搭配', '近反义词', '成语运用'],
        6: ['易错字', '形近字', '多音字', '词语搭配', '近反义词', '成语运用']
      }
    },
    poem: {   // 语文·古诗（题源 chinese-primary-curriculum.md，公版诗词）
      name: '古诗·背诵', short: '古诗', icon: '📜', bank: 'data/banks/poems.json', group: '语文',
      levels: LEVELS, medals: MEDALS,
      levelDesc: {
        1: ['五言启蒙', '乐府民歌', '咏物诗', '写景名句', '七言绝句', '名句运用'],
        2: ['五言启蒙', '乐府民歌', '咏物诗', '写景名句', '七言绝句', '名句运用'],
        3: ['山水田园', '送别诗', '边塞诗', '哲理诗', '律诗名篇', '名句运用'],
        4: ['山水田园', '送别诗', '边塞诗', '哲理诗', '律诗名篇', '名句运用'],
        5: ['爱国诗', '托物言志', '节令诗', '送别诗', '长诗名篇', '名句运用'],
        6: ['爱国诗', '托物言志', '节令诗', '送别诗', '长诗名篇', '名句运用']
      }
    },
    guwen: {   // 语文·小古文（题源 chinese-primary-curriculum.md 第三部分，11 篇公版小古文）
      name: '小古文', short: '小古文', icon: '🧧', bank: 'data/banks/guwen.json', group: '语文',
      levels: LEVELS, medals: MEDALS,
      levelDesc: {
        1: ['句意衔接', '字词释义', '认出处', '句意衔接', '字词释义', '综合'],
        2: ['句意衔接', '字词释义', '认出处', '句意衔接', '字词释义', '综合'],
        3: ['司马光', '守株待兔', '字词释义', '句意衔接', '认出处', '综合'],
        4: ['精卫填海', '王戎识李', '囊萤夜读', '铁杵成针', '字词释义', '综合'],
        5: ['自相矛盾', '杨氏之子', '字词释义', '句意衔接', '认出处', '综合'],
        6: ['学弈', '两小儿辩日', '伯牙鼓琴', '字词释义', '句意衔接', '综合']
      }
    },
    english: {   // 英语·单词（题源 english-primary-shenzhen-oxford.md 沪教牛津深圳版，公共词表）
      name: '英语·单词', short: '单词', icon: '🔤', bank: 'data/banks/english-words.json',
      levels: LEVELS, medals: MEDALS,
      levelDesc: {
        1: ['动物数字', '颜色', '水果食物', '动物数字', '颜色水果', '综合'],
        2: ['人物称呼', '身体部位', '自然植物', '人物称呼', '身体自然', '综合'],
        3: ['食物饮品', '一日三餐', '时间', '动作', '读写画', '综合'],
        4: ['场所', '学科', '星期', '天气', '四季', '综合'],
        5: ['职业', '交通工具', '方位', '情绪感觉', '方位情绪', '综合'],
        6: ['形容词', '买卖清洁', '观看旅行', '书报刊物', '网络节目', '综合']
      }
    }
  };

  // 学科大厅分组：语数英三大学科（语文内含 字词+古诗 两个分支）
  const GROUPS = [
    { key: 'math', name: '数学', icon: '🦁', subs: ['math'], desc: '口算 · 单元巩固' },
    { key: 'chinese', name: '语文', icon: '📖', subs: ['chinese', 'poem', 'guwen'], desc: '字词 · 古诗 · 小古文' },
    { key: 'english', name: '英语', icon: '🔤', subs: ['english'], desc: '单词' }
  ];

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
      // v2.9 激励体系字段兜底
      if (s.coins === undefined) s.coins = 0;
      if (!s.daily) s.daily = { day: '', review: false, round: false, correct10: false, correctToday: 0, bonus: false };
      if (s.streak === undefined) { s.streak = 0; s.streakDay = ''; }
      if (!s.pet) s.pet = { growth: 0, fedToday: 0, lastFeed: '' };
      if (s.pkLevel === undefined) { s.pkLevel = 0; s.pkWins = 0; }
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
      sub: { math: newSubj(), chinese: newSubj(), poem: newSubj(), guwen: newSubj() },   // 各学科进度
      stars: 0,                                   // 累计星数（贴纸）
      stickers: [],                               // 贴纸 id 列表
      clearedTags: {},                            // 已攻克知识点 tag -> 连对次数
      todayMins: 0, lastDay: '',                  // 当日学习分钟（20 分钟休息提醒）
      // v2.9 激励体系
      coins: 0,                                   // 🪙 金币（闯关/复习/任务产出，宠物消费）
      daily: { day: '', review: false, round: false, correct10: false, correctToday: 0, bonus: false },  // 每日任务
      streak: 0, streakDay: '',                   // 连续打卡天数
      pet: { growth: 0, fedToday: 0, lastFeed: '' },   // 宠物成长值
      pkLevel: 0, pkWins: 0                       // 人机 PK：机器人档位 / 累计胜场
    };
  }

  const Store = {
    get db() { return load(); },
    get LEVELS() { return LEVELS; },
    get MEDALS() { return MEDALS; },
    get LEVEL_DESC() { return LEVEL_DESC; },
    get SUBJECTS() { return SUBJECTS; },
    get GROUPS() { return GROUPS; },
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

    /* ---------- v2.9 激励体系 ---------- */
    today() { const n = new Date(); return n.getFullYear() + '-' + (n.getMonth() + 1) + '-' + n.getDate(); },
    /** 每日任务状态（跨天自动重置） */
    daily(stu) {
      const t = this.today();
      if (stu.daily.day !== t) stu.daily = { day: t, review: false, round: false, correct10: false, correctToday: 0, bonus: false };
      return stu.daily;
    },
    /** 完成一项任务 / 答对计数，返回获得的金币（任务 +5，全部完成奖励 +10，由调用方提示） */
    taskDone(stu, key) {
      const dl = this.daily(stu);
      let coins = 0;
      if (key === 'correct') {
        dl.correctToday++;
        if (!dl.correct10 && dl.correctToday >= 10) { dl.correct10 = true; coins += 5; }
      } else if (!dl[key]) {
        dl[key] = true; coins += 5;
      }
      coins += this.checkBonus(stu);
      return coins;
    },
    checkBonus(stu) {
      const dl = this.daily(stu);
      if (!dl.bonus && dl.review && dl.round && dl.correct10) {
        dl.bonus = true;
        this.bumpStreak(stu);
        return 10;
      }
      return 0;
    },
    /** 连续打卡：任务全完成当天记 1 天；断了不清零惩罚，从 1 重新数 */
    bumpStreak(stu) {
      const t = this.today();
      if (stu.streakDay === t) return;
      const y = new Date(Date.now() - 86400000);
      const ys = y.getFullYear() + '-' + (y.getMonth() + 1) + '-' + y.getDate();
      stu.streak = (stu.streakDay === ys) ? (stu.streak || 0) + 1 : 1;
      stu.streakDay = t;
    },
    /** 宠物阶段（成长值：嗂食+1，每嗂 10 金币） */
    PET_STAGES: ['🥚 神秘蛋', '🐣 破壳啦', '🐤 小绒球', '🐥 跳跳鸟', '🐦 飞行员', '🦅 大boss', '🦄 神话宠'],
    petStage(growth) {
      const th = [0, 3, 7, 12, 20, 30, 45];
      let i = 0; while (i < th.length - 1 && growth >= th[i + 1]) i++;
      return { index: i, name: this.PET_STAGES[i], next: th[i + 1] || null };
    },
    /** 嗂食：花 10 金币，成长 +1（每天限 3 次，防刷） */
    feedPet(stu) {
      const t = this.today();
      if (stu.pet.lastFeed !== t) { stu.pet.lastFeed = t; stu.pet.fedToday = 0; }
      if (stu.pet.fedToday >= 3) return { ok: false, msg: '今天吃太饱啦，明天再来喂～' };
      if ((stu.coins || 0) < 10) return { ok: false, msg: '金币不够啦，去做任务赚金币吧！' };
      stu.coins -= 10; stu.pet.fedToday++; stu.pet.growth++;
      return { ok: true, growth: stu.pet.growth };
    },

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
