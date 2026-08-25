# -*- coding: utf-8 -*-
"""
gen_bank.py — 生成口算题库 data/banks/math-oral.json
年级 1~6 × 段位 1~6（青铜→白银→黄金→铂金→钻石→王者），每格约 30 题，
含陷阱选项与错因提示。运行: python tools/gen_bank.py
"""
import json, random, os
from math import gcd

random.seed(2026)

def fr_str(x):
    """小数转最简分数字符串；除不尽保留原样"""
    for den in range(2, 101):
        if abs(x * den - round(x * den)) < 1e-9:
            n, d = round(x * den), den
            g = gcd(abs(n), d)
            n, d = n // g, d // g
            return str(n) if d == 1 else f"{n}/{d}"
    return str(round(x, 4))

def ok_frac(x):
    """结果能用分母 ≤ 100 的分数精确表示"""
    return any(abs(x * d - round(x * d)) < 1e-9 for d in range(1, 101))

WRONGS = {
    "add": ["是不是忘记进位了？先算个位，满了10要向十位进1。", "再算一遍，个位加个位，十位加十位。"],
    "sub": ["是不是忘记退位了？个位不够减，要向十位借1当10。", "再算一遍，先看个位够不够减。"],
    "mul": ["乘法口诀再背一背，想一想这句口诀的得数。", "是不是口诀串记了？慢慢想这句口诀。"],
    "div": ["用乘法口诀反过来想：几乘除数等于被除数？", "除法就是乘法的反过来，想想口诀。"],
    "rem": ["余数一定要比除数小，想一想商几、余几。", "先想口诀找最接近又不超过的，再算余数。"],
    "mix": ["两步计算要先算乘除，再算加减，别抢着算。", "分两步想：先算乘除部分，再加或减。"],
    "dec": ["小数点对齐了吗？先对齐再加减。", "数一数小数位数，别把小数点弄丢啦。"],
    "frac": ["分母相同才能直接加减，分子相加减、分母不变。", "约分了吗？结果要化成最简分数。"],
    "conv": ["想一想分数、小数、百分数之间是怎么互化的。", "先化成分母是100的分数再看一看。"],
    "est": ["估算要先四舍五入到整十、整百，再算。", "先把数看成接近的整十整百数。"],
}

def fmt(x):
    if isinstance(x, float) and x == int(x):
        return int(x)
    return round(x, 4)

def uniq_opts(ans, traps, n=3):
    opts, seen = [], {str(fmt(ans))}
    for t in traps:
        t = fmt(t)
        if isinstance(t, (int, float)) and t < 0:
            continue
        if str(t) not in seen:
            opts.append(str(t)); seen.add(str(t))
        if len(opts) >= n: break
    k = 1
    while len(opts) < n:
        for c in [ans + k, ans - k, ans + 10 * k]:
            c = fmt(c)
            if c >= 0 and str(c) not in seen:
                opts.append(str(c)); seen.add(str(c)); break
        k += 1
    return opts

def mk(q, a, kind, grade, level, tag):
    if kind == "rem":
        c, r = a  # (商, 余数)
        astr = f"{c} 余 {r}"
        cand = [f"{c} 余 {r+1}", f"{c+1} 余 {r}", f"{c-1} 余 {r}" if c > 1 else f"{c} 余 {r+2}", f"{c+1} 余 {r+1}"]
        opts, seen = [], {astr}
        for t in cand:
            if t not in seen:
                opts.append(t); seen.add(t)
            if len(opts) >= 3: break
        return {"q": q, "a": astr, "options": opts[:3], "wrongReasons": WRONGS[kind],
                "grade": grade, "level": level, "tag": tag}
    if kind == "frac":
        astr = a if isinstance(a, str) else fr_str(a)
        av = a if not isinstance(a, str) else (
            float(astr.split("/")[0]) / float(astr.split("/")[1]) if "/" in astr else float(astr))
        traps = []
        for t in [av * 2, av / 2, 1 - av, av * 3, av + 0.5, av + 0.25, av - 0.25]:
            if isinstance(t, (int, float)) and t >= 0 and ok_frac(t):
                s = fr_str(t)
                if s not in traps and s != astr:
                    traps.append(s)
        return {"q": q, "a": astr, "options": traps[:3], "wrongReasons": WRONGS[kind],
                "grade": grade, "level": level, "tag": tag}
    if kind == "conv":
        astr = fmt(a)
        opts, seen = [], {str(astr)}
        for t in [a * 10, a / 10, a + 1]:
            t = fmt(t)
            if str(t) not in seen:
                opts.append(str(t)); seen.add(str(t))
        return {"q": q, "a": astr, "options": opts[:3], "wrongReasons": WRONGS[kind],
                "grade": grade, "level": level, "tag": tag}
    traps = [a + 1, a - 1, a + 10, a - 10]
    if kind == "mul":
        traps = [a + a // 10 + 1, a - a // 10 - 1, a + 2]
    if kind == "dec":
        traps = [round(a * 10, 4) if a != 0 else a + 0.1, round(a / 10, 4), a + 0.1, a - 0.1]
    return {"q": q, "a": fmt(a), "options": uniq_opts(a, traps),
            "wrongReasons": WRONGS[kind], "grade": grade, "level": level, "tag": tag}

# ---------- 各年级 6 段位生成器 ----------

def add_sub(qs, grade, level, tags, alo, ahi, blo, bhi, add_n=15, sub_n=15):
    """加减混合生成：优先出进位/退位题（低段位也要有挑战），80 次尝试后放宽"""
    def pick(ok):
        for _ in range(80):
            a, b = random.randint(alo, ahi), random.randint(blo, bhi)
            if ok(a, b):
                return a, b
        return random.randint(alo, ahi), random.randint(blo, bhi)
    for _ in range(add_n):
        a, b = pick(lambda a, b: a % 10 + b % 10 > 10)
        qs.append(mk(f"{a} + {b}", a + b, "add", grade, level, tags[0]))
    for _ in range(sub_n):
        a, b = pick(lambda a, b: a > b and a % 10 < b % 10)
        if a <= b:
            a, b = max(a, b), min(a, b)
            if a == b:
                continue
        qs.append(mk(f"{a} - {b}", a - b, "sub", grade, level, tags[1]))

def gen_cell(grade, level):
    qs = []
    def add(q, a, kind, tag):
        qs.append(mk(q, a, kind, grade, level, tag))

    if grade == 1:
        # 每个段位都含进退位：1:20以内进退位 2:50以内加减 3:50以内进退位
        # 4:100以内加减 5:100以内进退位 6:200以内混合
        rng = {1: (5, 14, 5, 14), 2: (11, 45, 6, 39), 3: (21, 45, 17, 39),
               4: (23, 88, 15, 66), 5: (43, 88, 29, 66), 6: (55, 195, 35, 145)}[level]
        cap = {1: 20, 2: 50, 3: 50, 4: 100, 5: 100, 6: 200}[level]
        need = level in (1, 3, 5)   # 单数段位强制进退位
        def carry(a, b): return a % 10 + b % 10 > 10
        def borrow(a, b): return a % 10 < b % 10
        n = 0; tries = 0
        while n < 16 and tries < 400:
            tries += 1
            a = random.randint(rng[0], rng[1]); b = random.randint(rng[2], rng[3])
            if a + b > cap: continue
            if need and not carry(a, b): continue
            add(f"{a} + {b}", a + b, "add", "加法"); n += 1
        n = 0; tries = 0
        while n < 15 and tries < 400:
            tries += 1
            a = random.randint(rng[0], rng[1]); b = random.randint(rng[2], rng[3])
            if a <= b: continue
            if need and not borrow(a, b): continue
            add(f"{a} - {b}", a - b, "sub", "减法"); n += 1

    elif grade == 2:
        if level == 1:
            add_sub(qs, grade, level, ["100加减", "100加减"], 28, 80, 15, 40)
        elif level == 2:  # 表内乘法
            for _ in range(30):
                a, b = random.randint(2, 9), random.randint(2, 9)
                add(f"{a} × {b}", a * b, "mul", "表内乘")
        elif level == 3:  # 表内除法
            for _ in range(30):
                b, c = random.randint(2, 9), random.randint(2, 9)
                add(f"{b * c} ÷ {b}", c, "div", "表内除")
        elif level == 4:  # 乘除混合
            for _ in range(30):
                a, b = random.randint(2, 9), random.randint(2, 9)
                d = random.choice([x for x in range(2, 9) if (a * b) % x == 0])
                add(f"{a} × {b} ÷ {d}", a * b // d, "div", "乘除混合")
        elif level == 5:  # 有余数除法
            for _ in range(30):
                b = random.randint(3, 9); c = random.randint(2, 9)
                r = random.randint(1, b - 1)
                add(f"{b * c + r} ÷ {b} = ？（商几余几，选「商 余 数」）", (c, r), "rem", "有余数除")
        else:             # 乘加/乘减两步
            for _ in range(15):
                a, b = random.randint(2, 9), random.randint(2, 9)
                c = random.randint(3, 30)
                add(f"{a} × {b} + {c}", a * b + c, "mix", "两步计算")
            for _ in range(15):
                a, b = random.randint(2, 9), random.randint(2, 9)
                c = random.randint(2, a * b - 1)
                add(f"{a} × {b} - {c}", a * b - c, "mix", "两步计算")

    elif grade == 3:
        if level == 1:
            add_sub(qs, grade, level, ["两位加减", "两位加减"], 23, 88, 17, 55)
        elif level == 2:  # 几百几十加减
            for _ in range(15):
                a = random.randint(12, 68) * 10; b = random.randint(11, 29) * 10
                add(f"{a} + {b}", a + b, "add", "几百几十")
            for _ in range(15):
                a = random.randint(40, 98) * 10; b = random.randint(15, 39) * 10
                add(f"{a} - {b}", a - b, "sub", "几百几十")
        elif level == 3:  # 多位×一位
            for _ in range(15):
                a, b = random.randint(12, 34), random.randint(2, 4)
                add(f"{a} × {b}", a * b, "mul", "多位乘一位")
            for _ in range(15):
                a, b = random.randint(2, 9) * 100, random.randint(2, 5)
                add(f"{a} × {b}", a * b, "mul", "整百乘")
        elif level == 4:  # 多位÷一位
            for _ in range(15):
                b, c = random.randint(11, 44), random.randint(2, 4)
                add(f"{b * c} ÷ {b}", c, "div", "多位除一位")
            for _ in range(15):
                b, c = random.randint(2, 9) * 100, random.randint(2, 8)
                add(f"{b * c} ÷ {b}", c, "div", "整百除")
        elif level == 5:  # 乘除混合
            for _ in range(15):
                a, b = random.randint(2, 9), random.randint(2, 9)
                d = random.choice([x for x in range(2, 9) if (a * b) % x == 0])
                add(f"{a} × {b} ÷ {d}", a * b // d, "div", "乘除混合")
            for _ in range(15):
                a, b = random.randint(12, 30), random.randint(3, 5)
                add(f"{a} × {b}", a * b, "mul", "多位乘一位")
        else:             # 两步计算（原估算已按家长反馈移除）
            for _ in range(15):
                a, b = random.randint(3, 9), random.randint(3, 9)
                c = random.randint(20, 90)
                add(f"{a} × {b} + {c}", a * b + c, "mix", "两步计算")
            for _ in range(15):
                a, b = random.randint(12, 40), random.randint(3, 9)
                c = random.randint(10, a * b - 1)
                add(f"{a} × {b} - {c}", a * b - c, "mix", "两步计算")

    elif grade == 4:
        if level == 1:  # 大数口算
            for _ in range(15):
                a = random.randint(12, 80) * 100; b = random.randint(11, 60) * 100
                add(f"{a} + {b}", a + b, "add", "大数加减")
            for _ in range(15):
                a = random.randint(40, 99) * 100; b = random.randint(15, 39) * 100
                add(f"{a} - {b}", a - b, "sub", "大数加减")
        elif level == 2:  # 整十乘除
            for _ in range(15):
                a, b = random.randint(2, 9) * 10, random.randint(2, 9) * 10
                add(f"{a} × {b}", a * b, "mul", "整十乘除")
            for _ in range(15):
                b, c = random.randint(2, 9) * 10, random.randint(2, 9)
                add(f"{b * c} ÷ {b}", c, "div", "整十乘除")
        elif level == 3:  # 整百乘整十（原乘法估算已按家长反馈移除）
            for _ in range(30):
                a, b = random.randint(2, 9) * 100, random.randint(2, 9) * 10
                add(f"{a} × {b}", a * b, "mul", "整百乘整十")
        elif level == 4:  # 简算凑整
            for _ in range(10):
                a = random.choice([98, 99, 97, 199, 298]); b = random.randint(35, 96)
                add(f"{a} + {b}", a + b, "add", "凑整")
            for _ in range(10):
                a = random.choice([98, 99, 197, 299]); b = random.randint(35, 78)
                add(f"{a} - {b}", a - b, "sub", "凑整")
            for _ in range(10):
                a, b = random.choice([(25, 4), (125, 8), (5, 2), (50, 2)]), random.randint(3, 9)
                add(f"{a[0]} × {b * a[1]}", a[0] * b * a[1], "mul", "凑整")
        elif level == 5:  # 多位÷两位
            for _ in range(30):
                b = random.randint(11, 99); c = random.randint(2, 9)
                add(f"{b * c} ÷ {b}", c, "div", "除两位")
        else:             # 混合两步
            for _ in range(15):
                a, b = random.randint(12, 40), random.randint(2, 9)
                c = random.randint(15, 90)
                add(f"{a} × {b} + {c}", a * b + c, "mix", "两步计算")
            for _ in range(15):
                a, b = random.randint(12, 40), random.randint(2, 9)
                c = random.randint(10, a * b - 1)
                add(f"{a} × {b} - {c}", a * b - c, "mix", "两步计算")

    elif grade == 5:
        if level == 1:  # 小数加减
            for _ in range(15):
                a = round(random.uniform(0.1, 9.9), 1); b = round(random.uniform(0.1, 9.9), 1)
                if a + b <= 10: add(f"{a} + {b}", round(a + b, 2), "dec", "小数加减")
            for _ in range(15):
                a = round(random.uniform(2.0, 9.9), 1); b = round(random.uniform(0.2, 1.9), 1)
                add(f"{a} - {b}", round(a - b, 2), "dec", "小数加减")
        elif level == 2:  # 小数乘整数
            for _ in range(30):
                a = round(random.uniform(0.2, 9.5), 1); b = random.randint(2, 5)
                add(f"{a} × {b}", round(a * b, 2), "dec", "小数乘整数")
        elif level == 3:  # 小数除整数
            for _ in range(30):
                b = random.randint(2, 9); c = round(random.uniform(0.5, 9.5), 1)
                add(f"{round(b * c, 1)} ÷ {b}", round(c, 2), "dec", "小数除整数")
        elif level == 4:  # 小数点移动
            for _ in range(15):
                a = round(random.uniform(0.05, 9.9), 2)
                k = random.choice([10, 100])
                add(f"{a} × {k}", round(a * k, 4), "dec", "小数点移动")
            for _ in range(15):
                a = round(random.uniform(5, 99), 0)
                k = random.choice([10, 100])
                add(f"{a} ÷ {k}", round(a / k, 4), "dec", "小数点移动")
        elif level == 5:  # 简便运算
            pairs = [(0.25, 4), (1.25, 8), (2.5, 4), (0.5, 2)]
            for _ in range(30):
                p = random.choice(pairs); k = random.randint(2, 9)
                if random.random() < 0.5:
                    add(f"{p[0]} × {round(p[1] * k, 1)}", round(p[0] * p[1] * k, 2), "dec", "小数简算")
                else:
                    add(f"{round(p[0] * k, 2)} × {p[1]}", round(p[0] * p[1] * k, 2), "dec", "小数简算")
        else:             # 混合两步
            for _ in range(15):
                a = round(random.uniform(0.5, 5.5), 1); b = random.randint(2, 4)
                c = round(random.uniform(0.5, 3.5), 1)
                add(f"{a} × {b} + {c}", round(a * b + c, 2), "mix", "两步计算")
            for _ in range(15):
                b = random.randint(2, 9); c = round(random.uniform(0.5, 9.5), 1)
                d = round(random.uniform(0.5, 4.5), 1)
                add(f"{round(b * c, 1)} ÷ {b} + {d}", round(c + d, 2), "mix", "两步计算")

    else:               # grade 6
        def frac_pair():
            for _ in range(50):
                n1 = random.randint(1, 6); d1 = random.randint(2, 9)
                if n1 >= d1 or gcd(n1, d1) != 1: continue
                d2 = d1 * random.choice([1, 2, 3])
                if d2 > 36: continue
                n2 = random.randint(1, d2 - 1)
                if gcd(n2, d2) != 1: continue
                return n1, d1, n2, d2
            return 1, 2, 1, 4

        if level == 1:  # 分数加减
            for _ in range(40):
                n1, d1, n2, d2 = frac_pair()
                r = n1 / d1 + n2 / d2
                if ok_frac(r) and r < 2: add(f"{n1}/{d1} + {n2}/{d2}", r, "frac", "分数加减")
            for _ in range(40):
                n1, d1, n2, d2 = frac_pair()
                if n1 / d1 <= n2 / d2: n1, d1, n2, d2 = n2, d2, n1, d1
                r = n1 / d1 - n2 / d2
                if r > 0 and ok_frac(r): add(f"{n1}/{d1} - {n2}/{d2}", r, "frac", "分数加减")
        elif level == 2:  # 分数乘法
            for _ in range(40):
                n1, d1, n2, d2 = frac_pair()
                r = (n1 * n2) / (d1 * d2)
                if ok_frac(r): add(f"{n1}/{d1} × {n2}/{d2}", r, "frac", "分数乘")
            for _ in range(10):
                n, d = random.randint(1, 9), random.randint(2, 9)
                if gcd(n, d) != 1: continue
                k = random.randint(2, 9)
                r = n * k / d
                if ok_frac(r) and r < 9: add(f"{n}/{d} × {k}", r, "frac", "分数乘")
        elif level == 3:  # 分数除法
            for _ in range(50):
                n1, d1, n2, d2 = frac_pair()
                r = (n1 * d2) / (d1 * n2)
                if ok_frac(r) and r < 5: add(f"{n1}/{d1} ÷ {n2}/{d2}", r, "frac", "分数除")
        elif level == 4:  # 倒数与互化
            fr = [(1, 2, 0.5, 50), (1, 4, 0.25, 25), (3, 4, 0.75, 75), (1, 5, 0.2, 20),
                  (2, 5, 0.4, 40), (3, 5, 0.6, 60), (4, 5, 0.8, 80), (1, 10, 0.1, 10),
                  (7, 10, 0.7, 70), (9, 10, 0.9, 90), (1, 8, 0.125, 12.5)]
            for _ in range(15):
                n, d = random.randint(1, 9), random.randint(2, 9)
                if gcd(n, d) != 1: continue
                add(f"{n}/{d} 的倒数 = ？（填分数或整数）", fr_str(d / n), "frac", "倒数")
            for _ in range(15):
                n, d, dec, pct = random.choice(fr)
                add(f"{n}/{d} = ?（填小数）", dec, "conv", "互化")
                add(f"{dec} = ?（填百分数）", pct, "conv", "互化")
        elif level == 5:  # 分数小数百分数互化
            fr = [(1, 2, 0.5, 50), (1, 4, 0.25, 25), (3, 4, 0.75, 75), (1, 5, 0.2, 20),
                  (2, 5, 0.4, 40), (3, 5, 0.6, 60), (4, 5, 0.8, 80), (1, 10, 0.1, 10),
                  (7, 10, 0.7, 70), (9, 10, 0.9, 90), (1, 8, 0.125, 12.5), (3, 8, 0.375, 37.5)]
            for _ in range(32):
                n, d, dec, pct = random.choice(fr)
                t = random.randint(0, 3)
                if t == 0:   add(f"{n}/{d} = ?（填小数）", dec, "conv", "互化")
                elif t == 1: add(f"{dec} = ?（填百分数）", pct, "conv", "互化")
                elif t == 2: add(f"{pct}% = ?（填小数）", dec, "conv", "互化")
                else:        add(f"{dec} = ?/100（填分子）", round(dec * 100, 4), "conv", "互化")
        else:             # 混合口算
            for _ in range(12):
                d = random.randint(3, 9); n = random.randint(2, d - 1)
                if gcd(n, d) == 1: add(f"1 - {n}/{d}", 1 - n / d, "frac", "分数加减")
            for _ in range(12):
                n, d = random.randint(1, 9), random.randint(2, 9)
                if gcd(n, d) != 1: continue
                k = random.randint(2, 9)
                r = n * k / d
                if ok_frac(r) and r < 9: add(f"{n}/{d} × {k}", r, "frac", "分数乘")
            for _ in range(12):
                n, d = random.randint(2, 9), random.randint(2, 9)
                if gcd(n, d) != 1: continue
                k = random.randint(2, 9)
                r = n / (d * k)
                if ok_frac(r): add(f"{n}/{d} ÷ {k}", r, "frac", "分数除")

    # 去重 + 截断 32
    seen, out = set(), []
    for q in qs:
        if q["q"] not in seen:
            q["id"] = f"g{grade}-l{level}-{len(out)}"
            out.append(q); seen.add(q["q"])
        if len(out) >= 32: break
    return out

def main():
    bank = []
    for g in range(1, 7):
        for lv in range(1, 7):
            bank.extend(gen_cell(g, lv))
    path = os.path.join(os.path.dirname(__file__), "..", "data", "banks", "math-oral.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(bank, f, ensure_ascii=False, indent=1)
    print(f"OK: {len(bank)} questions -> {os.path.normpath(path)}")

if __name__ == "__main__":
    main()
