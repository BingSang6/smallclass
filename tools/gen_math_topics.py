# -*- coding: utf-8 -*-
"""gen_math_topics.py — 数学·专题训练题库生成器（v3.2）
专题 1：单位换算（人民币/长度/质量/时间/面积/体积，按年级）
专题 2：解决问题（典型应用题模板随机出数，按年级）
产出：data/banks/math-topics.json（q.unit = 专题名，复用单元巩固流程；level 0 不进段位池）
通用数学事实，无版权问题。
"""
import json, os, random
random.seed(20260822)

out = []


def add(q, a, opts, unit, tag, wrong):
    out.append({
        'q': q, 'a': str(a), 'options': [str(x) for x in opts],
        'wrongReasons': wrong, 'grade': None, 'level': 0, 'tag': tag,
        'unit': unit, 'speak': q.replace('=', '等于').replace('？', '').replace('（　）', '多少'),
        'id': 'tp-%03d' % len(out)
    })


# ---------------- 专题 1：单位换算 ----------------
# (专题名, 年级, [(大单位, 小单位, 进率, 生成量范围)])
UNIT_SETS = [
    ('专题·人民币', 2, [('元', '角', 10, 5), ('角', '分', 10, 8), ('元', '分', 100, 4)]),
    ('专题·长度', 3, [('千米', '米', 1000, 8), ('米', '分米', 10, 9), ('分米', '厘米', 10, 8),
                      ('厘米', '毫米', 10, 7), ('米', '厘米', 100, 6)]),
    ('专题·质量', 3, [('吨', '千克', 1000, 6), ('千克', '克', 1000, 7)]),
    ('专题·时间', 3, [('时', '分', 60, 5), ('分', '秒', 60, 7)]),
    ('专题·面积', 4, [('平方千米', '公顷', 100, 5), ('平方米', '平方分米', 100, 6),
                      ('平方分米', '平方厘米', 100, 7), ('公顷', '平方米', 10000, 3)]),
    ('专题·体积与容积', 5, [('立方米', '立方分米', 1000, 4), ('立方分米', '升', 1, 9),
                            ('升', '毫升', 1000, 6), ('立方厘米', '毫升', 1, 8)]),
]
for unit, grade, defs in UNIT_SETS:
    for big, small, rate, hi in defs:
        for _ in range(5):
            n = random.randint(2, hi)
            ok_big = random.random() < 0.5
            if ok_big:   # 大化小
                a = n * rate
                q = '%d%s = （　）%s' % (n, big, small)
                wrongs = sorted({a * 10, a // 10 if a >= 10 else a + rate, n * (rate * 10), a + n})[:2]
            else:        # 小化大
                n2 = n * rate
                a = n
                q = '%d%s = （　）%s' % (n2, small, big)
                wrongs = sorted({a * 10, a + 10, n2})[:2]
            wrongs = [w for w in wrongs if w != a and w > 0][:2]
            while len(wrongs) < 2:
                wrongs.append(a + random.randint(1, 9))
            add(q, a, wrongs[:2], unit, '单位换算·' + big + small,
                ['相邻单位 %s→%s 进率是 %d，%d × %d = %d' % (big, small, rate, n, rate, a),
                 '先把进率记牢：' + big + '和' + small + '之间是 ' + str(rate)])
            out[-1]['grade'] = grade

# ---------------- 专题 2：解决问题（应用题模板） ----------------
APP_TEMPLATES = [
    # (专题名, 年级, tag, 模板函数 -> (q, a, 干扰[], 错因))
    ('专题·解决问题', 3, '倍数问题', lambda: (
        lambda a, b: ('果园里有 %d 棵苹果树，梨树的棵数是苹果树的 %d 倍。梨树有多少棵？（　）' % (a, b),
                      a * b, sorted({a * b + a, a + b, a * b - b}),
                      ['求一个数的几倍用乘法：%d × %d = %d' % (a, b, a * b)])
    )(*[random.randint(3, 12) for _ in range(1)], random.choice([2, 3, 4, 5]))),
    ('专题·解决问题', 3, '和差问题', lambda: (
        lambda x, b: ('哥哥和弟弟一共有 %d 张邮票，哥哥比弟弟多 %d 张。弟弟有多少张？（　）' % (2 * x + b, b),
                      x, sorted({x + b, (2 * x + b) // 2, x + 2 * b}),
                      ['和差问题：（和 − 差）÷ 2 = 小数。（%d − %d）÷ 2 = %d' % (2 * x + b, b, x)])
    )(random.randint(8, 30), random.randint(2, 6))),
    ('专题·解决问题', 4, '单价问题', lambda: (
        lambda a, b: ('一个书包 %d 元，买 %d 个这样的书包要多少元？（　）' % (a, b),
                      a * b, sorted({a * b + a, a + b, a * b - 10}),
                      ['单价 × 数量 = 总价：%d × %d = %d' % (a, b, a * b)])
    )(random.choice([35, 42, 48, 56, 68]), random.randint(3, 9))),
    ('专题·解决问题', 4, '路程问题', lambda: (
        lambda v, t: ('一辆汽车每小时行 %d 千米，行了 %d 小时，一共行了多少千米？（　）' % (v, t),
                      v * t, sorted({v * t + v, v + t, v * t - t}),
                      ['速度 × 时间 = 路程：%d × %d = %d' % (v, t, v * t)])
    )(random.choice([60, 70, 80, 90, 110]), random.randint(2, 6))),
    ('专题·解决问题', 4, '植树问题', lambda: (
        lambda n: ('一条小路长 %d 米，每隔 %d 米栽一棵树（两端都栽），一共要栽多少棵？（　）' % (n * 5, 5),
                   n + 1, sorted({n, n + 2, n * 2}),
                   ['两端都栽：棵数 = 间隔数 + 1。%d ÷ %d = %d 个间隔，加 1 = %d 棵' % (n * 5, 5, n, n + 1)])
    )(random.randint(8, 20))),
    ('专题·解决问题', 4, '除法应用', lambda: (
        lambda a, b: ('学校买来 %d 本图书，平均分给 %d 个班，每个班分到多少本？（　）' % (a * b, b),
                      a, sorted({a + b, a * b, a - 1 if a > 1 else a + 2}),
                      ['总数 ÷ 份数 = 每份数：%d ÷ %d = %d' % (a * b, b, a)])
    )(random.randint(12, 40), random.choice([3, 4, 5, 6]))),
    ('专题·解决问题', 5, '小数购物', lambda: (
        lambda a, b: ('一支笔 %.1f 元，一本笔记本 %.1f 元，买一支笔和一本笔记本一共多少元？（　）' % (a, b),
                      '%.1f' % (a + b), sorted({'%.1f' % (a + b + 1), '%.1f' % (a * b), '%.1f' % (abs(a - b))}),
                      ['小数加法：小数点对齐再相加。%.1f + %.1f = %.1f' % (a, b, a + b)])
    )(random.randint(15, 90) / 10, random.randint(20, 80) / 10)),
    ('专题·解决问题', 6, '分数应用', lambda: (
        lambda total, p, qn: ('一本书共 %d 页，第一天看了全书的 %d/%d，第一天看了多少页？（　）' % (total, p, qn),
                              total * p // qn, sorted({total * p // qn + total // qn, total - total * p // qn,
                                                       total * p // qn - p}),
                              ['求一个数的几分之几用乘法：%d × %d/%d = %d 页' % (total, p, qn, total * p // qn)])
    )(random.choice([40, 60, 80, 120, 160]), random.choice([1, 2, 3]), random.choice([4, 5, 6, 8]))),
]
for unit, grade, tag, fn in APP_TEMPLATES:
    for _ in range(8):
        q, a, wrongs, reason = fn()
        wrongs = [w for w in wrongs if str(w) != str(a)][:2]
        while len(wrongs) < 2:
            wrongs.append(int(a) + random.randint(1, 9) if isinstance(a, int) else '%.1f' % (float(a) + 1.5))
        add(q, a, wrongs[:2], unit, tag, [reason, '先想清楚数量关系，再列式计算'])
        out[-1]['grade'] = grade

path = os.path.join(os.path.dirname(__file__), '..', 'data', 'banks', 'math-topics.json')
with open(path, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
units = {}
for x in out:
    units.setdefault(x['unit'], [0, set()])[0]
    units[x['unit']][0] += 1
    units[x['unit']][1].add(x['grade'])
print('生成', len(out), '道专题题 →', os.path.normpath(path))
for u, (n, gs) in units.items():
    print('  %s: %d 题（年级 %s）' % (u, n, sorted(gs)))
