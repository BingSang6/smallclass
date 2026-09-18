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
      // v3.4 全年级单元巩固：北师大版上册 1~6 年级单元题库（gen_units_all.py）
      // v3.8 对齐 2026 新教材：一年级=2024秋版、四年级=2026秋版（其余年级待后续对齐）
      unitsBank: 'data/banks/math-units.json',
      units: {
        1: ['第一单元 生活中的数', '第二单元 5以内数加与减', '综合实践 介绍我的教室',
            '第三单元 整理与分类', '第四单元 10以内数加与减', '数学好玩 一起做游戏',
            '第五单元 有趣的立体图形', '综合实践 记录我的一天'],
        2: ['第一单元 100以内的加与减', '第二单元 购物（人民币）', '第三单元 数一数与乘法', '第四单元 图形的变化',
            '第五单元 2~5的乘法口诀', '第六单元 测量', '第七单元 分一分与除法', '第八单元 6~9的乘法口诀', '第九单元 除法'],
        3: ['第一单元 混合运算', '第二单元 观察物体', '第三单元 加与减', '第四单元 乘与除',
            '第五单元 周长', '第六单元 乘法', '第七单元 年月日', '第八单元 认识小数'],
        4: ['第一单元 认识更大的数', '综合实践 编码', '第二单元 线与角', '第三单元 整数乘法（二）',
            '第四单元 我们生活的空间（二）', '第五单元 运算律', '数学好玩 数图形的学问', '第六单元 图形的奥秘',
            '第七单元 运用数量关系解决问题', '第八单元 数据的表示和分析（一）', '综合实践 导航给的时间准吗'],
        5: ['第一单元 小数除法', '第二单元 轴对称和平移', '第三单元 倍数与因数', '第四单元 多边形的面积',
            '第五单元 分数的意义', '第六单元 组合图形的面积', '第七单元 可能性'],
        6: ['第一单元 圆', '第二单元 分数混合运算', '第三单元 观察物体', '第四单元 百分数',
            '第五单元 数据处理', '第六单元 比的认识', '第七单元 百分数的应用']
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
      // v3.5 语文单元巩固：部编版上册 1~6 年级（gen_chinese_units.py）
      // v3.8 对齐 2026 新教材：一年级=2024秋版、四年级=2026秋版（其余年级待后续对齐）
      unitsBank: 'data/banks/chinese-units.json',
      units: {
        1: ['第一单元 识字', '第二单元 汉语拼音（一）', '第三单元 汉语拼音（二）', '第四单元 汉语拼音（三）',
            '第五单元 阅读（一）', '第六单元 识字（二）', '第七单元 阅读（二）', '第八单元 阅读（三）'],
        2: ['第一单元 大自然的秘密', '第二单元 识字', '第三单元 儿童生活', '第四单元 家乡',
            '第五单元 思维方法', '第六单元 伟人', '第七单元 想象', '第八单元 相处'],
        3: ['第一单元 学校生活', '第二单元 金秋时节', '第三单元 童话世界', '第四单元 预测策略',
            '第五单元 观察（习作单元）', '第六单元 祖国河山', '第七单元 大自然（我与自然）', '第八单元 美好品质'],
        4: ['第一单元 自然之美', '第二单元 提问策略', '第三单元 连续观察', '第四单元 中外神话',
            '第五单元 习作单元（把事情写清楚）', '第六单元 中国的世界文化遗产', '第七单元 童年成长', '第八单元 家国情怀'],
        5: ['第一单元 一花一鸟总关情', '第二单元 阅读要有一定的速度', '第三单元 民间故事', '第四单元 爱国情怀',
            '第五单元 习作单元（说明文）', '第六单元 舐犊之情', '第七单元 四时景物皆成趣', '第八单元 读书明智'],
        6: ['第一单元 感受自然', '第二单元 重温革命岁月', '第三单元 阅读好时光（有目的地阅读）', '第四单元 小说的魅力',
            '第五单元 成长的快乐（习作单元）', '第六单元 珍爱我们的家园', '第七单元 艺术的魅力', '第八单元 走近鲁迅']
      },
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
      // v3.18 必背古诗全集单元巩固（g1 13 首 / g4 28 首，题目带 unit 字段，见 gen_poems_textbook.py）
      units: {
        1: ['一上·咏鹅', '一上·画', '一上·悯农（其二）', '一上·风', '一上·江南', '一上·古朗月行（节选）',
            '一下·春晓', '一下·赠汪伦', '一下·静夜思', '一下·寻隐者不遇', '一下·池上', '一下·小池', '一下·画鸡'],
        4: ['四上·暮江吟', '四上·题西林壁', '四上·雪梅', '四上·出塞', '四上·凉州词', '四上·夏日绝句',
            '四下·宿新市徐公店', '四下·清平乐·村居', '四下·芙蓉楼送辛渐', '四下·塞下曲', '四下·墨梅', '四下·独坐敬亭山',
            '回顾·登鹳雀楼', '回顾·望庐山瀑布', '回顾·江雪', '回顾·敕勒歌', '回顾·小儿垂钓', '回顾·悯农（其一）',
            '回顾·所见', '回顾·山行', '回顾·望天门山', '回顾·饮湖上初晴后雨', '回顾·望洞庭', '回顾·绝句',
            '回顾·晓出净慈寺送林子方', '回顾·赠刘景文', '回顾·夜书所见', '回顾·采莲曲']
      },
      levelDesc: {
        // v3.18 一/四年级段位 = 题型难度层（豆包难度锁死规则：青铜禁赏析，逐层解锁）
        1: ['背诵默写', '字音常识', '字词句意', '道理情感', '对比综合', '大乱斗'],
        2: ['五言启蒙', '乐府民歌', '咏物诗', '写景名句', '七言绝句', '名句运用'],
        3: ['山水田园', '送别诗', '边塞诗', '哲理诗', '律诗名篇', '名句运用'],
        4: ['背诵默写', '字音常识', '字词句意', '道理情感', '对比综合', '大乱斗'],
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
      // v3.9 英语单元巩固：沪教版上册 3~6 年级（gen_english_units.py）
      // v3.12 一、二年级对齐深圳 2025 新教材《英语（口语交际）》上册（各 6 单元）
      unitsBank: 'data/banks/english-units.json',
      units: {
        1: ['第一单元 家庭', '第二单元 感觉', '第三单元 数字与文具',
            '第四单元 动作', '第五单元 宠物', '第六单元 颜色'],
        2: ['第一单元 五感', '第二单元 亲属', '第三单元 玩具',
            '第四单元 场所', '第五单元 农场动物', '第六单元 节日'],
        3: ['第一单元 感受与情绪', '第二单元 家庭', '第三单元 外貌', '第四单元 玩乐',
            '第五单元 食物', '第六单元 小动物', '第七单元 天气', '第八单元 生日'],
        4: ['第一单元 住所', '第二单元 动物栖息地', '第三单元 数字', '第四单元 购物',
            '第五单元 季节', '第六单元 植物', '第七单元 道路安全', '第八单元 祖辈与职业'],
        5: ['第一单元 周末活动', '第二单元 保持健康', '第三单元 不同的国家', '第四单元 有趣的假日',
            '第五单元 生物', '第六单元 爱护地球', '第七单元 庆祝节日', '第八单元 音乐与感受'],
        6: ['第一单元 搬到新地方', '第二单元 艺术创作', '第三单元 保护自己', '第四单元 物体的运动',
            '第五单元 发明改变生活', '第六单元 城市']
      },
      levels: LEVELS, medals: MEDALS,
      levelDesc: {
        1: ['家庭', '感觉', '数字与文具', '动作', '宠物', '颜色'],
        2: ['五感', '亲属', '玩具', '场所', '农场动物', '节日'],
        3: ['食物饮品', '一日三餐', '时间', '动作', '读写画', '综合'],
        4: ['场所', '学科', '星期', '天气', '四季', '综合'],
        5: ['职业', '交通工具', '方位', '情绪感觉', '方位情绪', '综合'],
        6: ['形容词', '买卖清洁', '观看旅行', '书报刊物', '网络节目', '综合']
      },
      // v3.10 英语专题训练：跨单元语法专项（gen_english_topics.py）
      topicsBank: 'data/banks/english-topics.json',
      topics: {
        3: ['专题·疑问词', '专题·be动词'],
        4: ['专题·人称代词', '专题·方位介词'],
        5: ['专题·一般现在时', '专题·可数与不可数'],
        6: ['专题·一般过去时', '专题·比较级']
      },
    }
  };

  // 学科大厅分组：语数英三大学科（语文内含 字词+古诗 两个分支）
  const GROUPS = [
    { key: 'math', name: '数学', icon: '🦁', subs: ['math'], desc: '口算 · 单元巩固' },
    { key: 'chinese', name: '语文', icon: '📖', subs: ['chinese', 'poem', 'guwen'], desc: '字词 · 古诗 · 小古文' },
    { key: 'english', name: '英语', icon: '🔤', subs: ['english'], desc: '单词 · 单元巩固' }
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
      if (!s.pet.decos) s.pet.decos = []; if (s.pet.wearing === undefined) s.pet.wearing = null;
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
      pet: { growth: 0, fedToday: 0, lastFeed: '', decos: [], wearing: null, name: '' },   // 宠物成长值 + 装扮
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

    /** v3.16 金币入账：同时累计 coinsEarned（里程碑装扮用，只增不减） */
    earn(stu, n) {
      if (!n) return;
      stu.coins = (stu.coins || 0) + n;
      stu.coinsEarned = (stu.coinsEarned || 0) + n;
    },

    /** v3.7 装扮商店；v3.16 加里程碑专属装扮（mile = 累计赚取金币解锁，免费领取） */
    DECOS: [
      { id: 'hat', name: '小礼帽', icon: '🎩', price: 20 },
      { id: 'crown', name: '王冠', icon: '👑', price: 50 },
      { id: 'scarf', name: '红围巾', icon: '🧣', price: 20 },
      { id: 'glasses', name: '墨镜', icon: '🕶️', price: 30 },
      { id: 'bow', name: '蝴蝶结', icon: '🎀', price: 15 },
      { id: 'flower', name: '小花', icon: '🌸', price: 15 },
      { id: 'halo', name: '天使光环', icon: '😇', price: 0, mile: 100 },
      { id: 'rocket', name: '小火箭', icon: '🚀', price: 0, mile: 300 },
      { id: 'rainbow', name: '彩虹', icon: '🌈', price: 0, mile: 600 }
    ],
    buyDeco(stu, id) {
      const d = this.DECOS.find(x => x.id === id);
      if (!d) return { ok: false, msg: '没有这个装扮' };
      if (stu.pet.decos.indexOf(id) >= 0) return { ok: false, msg: '已经买过啦' };
      if (d.mile) {
        if ((stu.coinsEarned || 0) < d.mile) return { ok: false, msg: '累计赚满 ' + d.mile + ' 金币才能解锁哦（已累计 ' + (stu.coinsEarned || 0) + '）' };
        stu.pet.decos.push(id); stu.pet.wearing = id;
        return { ok: true, msg: '🏆 里程碑达成！领到了【' + d.name + '】' + d.icon + '，已经戴上啦！' };
      }
      if ((stu.coins || 0) < d.price) return { ok: false, msg: '金币不够（还差 ' + (d.price - stu.coins) + ' 🪙），去答题赚吧！' };
      stu.coins -= d.price; stu.pet.decos.push(id); stu.pet.wearing = id;
      return { ok: true, msg: '🛍 买到了【' + d.name + '】' + d.icon + '，已经戴上啦！' };
    },
    equipDeco(stu, id) { stu.pet.wearing = (stu.pet.wearing === id) ? null : id; },
    namePet(stu, name) {
      name = (name || '').trim().slice(0, 6);
      if (!name) return { ok: false, msg: '名字不能为空' };
      stu.pet.name = name;
      return { ok: true, msg: '它现在叫【' + name + '】啦！' };
    },
    petEmoji(stu) {
      const st = this.petStage(stu.pet.growth);
      const deco = this.DECOS.find(x => x.id === stu.pet.wearing);
      return st.name.split(' ')[0] + (deco ? deco.icon : '');
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
