# -*- coding: utf-8 -*-
"""
gen_bank.py — 生成口算题库 data/banks/math-oral.json
年级 1~6 × 段位 1~4，每格约 35 题，含陷阱选项与错因提示。
运行: python tools/gen_bank.py
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
    "dec": ["小数点对齐了吗？先对齐再加减。", "数一数小数位数，别把小数点弄丢啦。"],
    "frac": ["分母相同才能直接加减，分子相加减、分母不变。", "约分了吗？结果要化成最简分数。"],
    "est": ["估算要先四舍五入到整十、整百，再算。", "先把数看成接近的整十整百数。"],
    "conv": ["想一想分数、小数、百分数之间是怎么互化的。", "先化成分母是100的分数再看一看。"],
}

def fmt(x):
    if isinstance(x, float) and x == int(x):
        return int(x)
    return round(x, 4)

def uniq_opts(ans, traps, n=3, allow_neg=False):
    """答案 + 陷阱选项，去重、乱序，共 n 个选项（答案不在其中）"""
    opts, seen = [], {str(fmt(ans))}
    for t in traps:
        t = fmt(t)
        if not allow_neg and isinstance(t, (int, float)) and t < 0:
            continue
        if str(t) not in seen:
            opts.append(str(t)); seen.add(str(t))
        if len(opts) >= n: break
    # 不足则补 ans±1/±10
    k = 1
    while len(opts) < n:
        for c in [ans + k, ans - k, ans + 10 * k, ans - 10 * k]:
            c = fmt(c)
            if not allow_neg and c < 0:
                continue
            if str(c) not in seen:
                opts.append(str(c)); seen.add(str(c)); break
        k += 1
    return opts

def mk(q, a, kind, grade, level, tag):
    if kind == "frac":
        # 分数题：答案与选项都是最简分数字符串
        astr = a if isinstance(a, str) else fr_str(a)
        traps = []
        for t in [a * 2, a / 2, 1 - a, a * 3, a + 0.5, a + 0.25, a - 0.25]:
            if isinstance(t, (int, float)) and t >= 0 and ok_frac(t):
                s = fr_str(t)
                if s not in traps and s != astr:
                    traps.append(s)
        return {"q": q, "a": astr, "options": traps[:3], "wrongReasons": WRONGS[kind],
                "grade": grade, "level": level, "tag": tag}
    if kind == "conv":
        # 互化题：答案为数值，陷阱用 ×10 / ÷10 / +1 的典型错误
        astr = fmt(a)
        traps = [a * 10, a / 10, a + 1]
        opts, seen = [], {str(astr)}
        for t in traps:
            t = fmt(t)
            if str(t) not in seen:
                opts.append(str(t)); seen.add(str(t))
        return {"q": q, "a": astr, "options": opts[:3], "wrongReasons": WRONGS[kind],
                "grade": grade, "level": level, "tag": tag}
    traps = [a + 1, a - 1, a + 10, a - 10]
    if kind == "mul":
        traps = [a + a // 10 + 1, a - a // 10 - 1, a + 2]
    if kind in ("dec", "frac"):
        traps = [round(a * 10, 4) if a != 0 else a + 0.1, round(a / 10, 4), a + 0.1, a - 0.1]
    return {"q": q, "a": fmt(a) if not isinstance(a, str) else a,
            "options": uniq_opts(a if not isinstance(a, str) else float(a), traps),
            "wrongReasons": WRONGS[kind], "grade": grade, "level": level, "tag": tag}

def gen_cell(grade, level):
    qs = []
    def add(q, a, kind, tag):
        qs.append(mk(q, a, kind, grade, level, tag))

    if grade == 1:
        if level == 1:   # 10以内加减
            for _ in range(18):
                a, b = random.randint(1, 9), random.randint(1, 9)
                if a + b <= 10: add(f"{a} + {b}", a + b, "add", "10加")
                else: add(f"{max(a,b)} - {min(a,b)}", max(a, b) - min(a, b), "sub", "10减")
            for _ in range(12):
                a = random.randint(2, 10); b = random.randint(1, a - 1)
                add(f"{a} - {b}", a - b, "sub", "10减")
        elif level == 2: # 20以内进退位
            for _ in range(16):
                a = random.randint(4, 9); b = random.randint(2, 9)
                if a + b > 10: add(f"{a} + {b}", a + b, "add", "20进位加")
            for _ in range(16):
                a = random.randint(11, 18); b = random.randint(2, 9)
                if str(a)[1] < str(b): add(f"{a} - {b}", a - b, "sub", "20退位减")
        elif level == 3: # 50以内
            for _ in range(16):
                a, b = random.randint(10, 40), random.randint(5, 9)
                add(f"{a} + {b}", a + b, "add", "50加")
            for _ in range(16):
                a = random.randint(20, 50); b = random.randint(6, 19)
                add(f"{a} - {b}", a - b, "sub", "50减")
        else:            # 100以内
            for _ in range(16):
                a, b = random.randint(23, 68), random.randint(15, 31)
                add(f"{a} + {b}", a + b, "add", "100加")
            for _ in range(16):
                a = random.randint(42, 99); b = random.randint(17, 38)
                add(f"{a} - {b}", a - b, "sub", "100减")

    elif grade == 2:
        if level == 1:   # 100以内加减
            for _ in range(16):
                a, b = random.randint(28, 70), random.randint(15, 29)
                add(f"{a} + {b}", a + b, "add", "100加减")
            for _ in range(16):
                a = random.randint(51, 99); b = random.randint(24, 50)
                add(f"{a} - {b}", a - b, "sub", "100加减")
        elif level == 2: # 表内乘法
            for _ in range(18):
                a, b = random.randint(2, 9), random.randint(2, 9)
                add(f"{a} × {b}", a * b, "mul", "表内乘")
            for _ in range(14):
                a, b = random.randint(4, 9), random.randint(3, 9)
                add(f"{a} × {b}", a * b, "mul", "表内乘")
        elif level == 3: # 表内除法
            for _ in range(32):
                b, c = random.randint(2, 9), random.randint(2, 9)
                add(f"{b * c} ÷ {b}", c, "div", "表内除")
        else:            # 乘除混合
            for _ in range(16):
                b, c = random.randint(2, 9), random.randint(2, 9)
                add(f"{b * c} ÷ {b}", c, "div", "乘除混合")
            for _ in range(16):
                a, b = random.randint(2, 9), random.randint(2, 9)
                if (a * b) % max(2, min(a, b)) == 0:
                    add(f"{a} × {b} ÷ {max(2, min(a,b))}", a * b // max(2, min(a, b)), "div", "乘除混合")

    elif grade == 3:
        if level == 1:   # 两位数加减
            for _ in range(16):
                a, b = random.randint(23, 76), random.randint(17, 49)
                add(f"{a} + {b}", a + b, "add", "两位加减")
            for _ in range(16):
                a = random.randint(52, 98); b = random.randint(27, 51)
                add(f"{a} - {b}", a - b, "sub", "两位加减")
        elif level == 2: # 口算乘
            for _ in range(16):
                a, b = random.randint(12, 34), random.randint(2, 4)
                add(f"{a} × {b}", a * b, "mul", "口算乘")
            for _ in range(16):
                a, b = random.randint(2, 9) * 100, random.randint(2, 5)
                add(f"{a} × {b}", a * b, "mul", "整百乘")
        elif level == 3: # 口算除
            for _ in range(16):
                b, c = random.randint(11, 44), random.randint(2, 4)
                add(f"{b * c} ÷ {b}", c, "div", "口算除")
            for _ in range(16):
                b, c = random.randint(2, 9) * 100, random.randint(2, 8)
                add(f"{b * c // b * b} ÷ {b}", b * c // b, "div", "整百除")
        else:            # 混合与估算
            for _ in range(10):
                a = random.randint(21, 89); a -= a % 10
                b = random.randint(21, 79); b += 10 - b % 10
                add(f"{a} + {b} ≈ ?", (round(a / 100) + round(b / 100)) * 100 if a + b > 100 else round((a + b) / 10) * 10, "est", "估算")
            for _ in range(10):
                a, b = random.randint(12, 30), random.randint(3, 5)
                add(f"{a} × {b}", a * b, "mul", "口算乘")
            for _ in range(10):
                b, c = random.randint(12, 40), random.randint(2, 4)
                add(f"{b * c} ÷ {b}", c, "div", "口算除")

    elif grade == 4:
        if level == 1:   # 大数口算（万以内整十整百）
            for _ in range(16):
                a = random.randint(12, 80) * 100; b = random.randint(11, 60) * 100
                add(f"{a} + {b}", a + b, "add", "大数加减")
            for _ in range(16):
                a = random.randint(40, 99) * 100; b = random.randint(15, 39) * 100
                add(f"{a} - {b}", a - b, "sub", "大数加减")
        elif level == 2: # 整十乘除
            for _ in range(16):
                a, b = random.randint(2, 9) * 10, random.randint(2, 9) * 10
                add(f"{a} × {b}", a * b, "mul", "整十乘除")
            for _ in range(16):
                b, c = random.randint(2, 9) * 10, random.randint(2, 9)
                add(f"{b * c} ÷ {b}", c, "div", "整十乘除")
        elif level == 3: # 三位数×两位估算
            for _ in range(32):
                a = random.randint(105, 995); a -= a % 10
                b = random.randint(12, 98); b -= b % 10
                ans = round(a / 100) * 100 * round(b / 10) * 10 // 1000 * 1000
                add(f"{a} × {b} ≈ ?", ans, "est", "乘法估算")
        else:            # 简算凑整
            for _ in range(11):
                a = random.choice([98, 99, 97, 199, 298]); b = random.randint(35, 96)
                add(f"{a} + {b}", a + b, "add", "凑整加")
            for _ in range(10):
                a = random.choice([98, 99, 197, 299]); b = random.randint(35, 78)
                add(f"{a} - {b}", a - b, "sub", "凑整减")
            for _ in range(11):
                a, b = random.choice([(25, 4), (125, 8), (5, 2), (50, 2)]), random.randint(3, 9)
                add(f"{a[0]} × {b * a[1]}", a[0] * b * a[1], "mul", "凑整乘")

    elif grade == 5:
        if level == 1:   # 小数加减
            for _ in range(16):
                a = round(random.uniform(0.1, 0.9), 1); b = round(random.uniform(0.1, 0.9), 1)
                add(f"{a} + {b}", round(a + b, 2), "dec", "小数加")
            for _ in range(16):
                a = round(random.uniform(1.1, 9.9), 1); b = round(random.uniform(0.2, 0.9), 1)
                add(f"{a} - {b}", round(a - b, 2), "dec", "小数减")
        elif level == 2: # 小数乘除
            for _ in range(16):
                a = round(random.uniform(0.2, 9.5), 1); b = random.randint(2, 5)
                add(f"{a} × {b}", round(a * b, 2), "dec", "小数乘")
            for _ in range(16):
                b = random.randint(2, 9); c = round(random.uniform(0.5, 9.5), 1)
                add(f"{round(b * c, 1)} ÷ {b}", round(c, 2), "dec", "小数除")
        elif level == 3: # 简便运算
            pairs = [(0.25, 4), (1.25, 8), (2.5, 4), (0.5, 2)]
            for _ in range(32):
                p = random.choice(pairs); k = random.randint(2, 9)
                if random.random() < 0.5:
                    add(f"{p[0]} × {round(p[1] * k, 1)}", round(p[0] * p[1] * k, 2), "dec", "小数简算")
                else:
                    add(f"{round(p[0] * k, 2)} × {p[1]}", round(p[0] * p[1] * k, 2), "dec", "小数简算")
        else:            # 混合口算
            for _ in range(10):
                a = round(random.uniform(1.5, 9.9), 1); b = round(random.uniform(0.5, 4.5), 1)
                add(f"{a} - {b}", round(a - b, 2), "dec", "小数减")
            for _ in range(10):
                a = round(random.uniform(0.5, 9.9), 1); b = random.randint(2, 9)
                add(f"{a} × {b}", round(a * b, 2), "dec", "小数乘")
            for _ in range(10):
                b, c = random.randint(2, 9), round(random.uniform(0.5, 9.5), 1)
                add(f"{round(b * c, 1)} ÷ {b}", round(c, 2), "dec", "小数除")

    else:               # grade 6
        def frac_pair():
            """随机一对最简真分数，通分后分母 ≤ 36"""
            for _ in range(50):
                n1 = random.randint(1, 6); d1 = random.randint(2, 9)
                if n1 >= d1 or gcd(n1, d1) != 1: continue
                d2 = d1 * random.choice([1, 2, 3])
                if d2 > 36: continue
                n2 = random.randint(1, d2 - 1)
                if gcd(n2, d2) != 1: continue
                return n1, d1, n2, d2
            return 1, 2, 1, 4

        if level == 1:   # 分数加减（结果最简）
            for _ in range(40):
                n1, d1, n2, d2 = frac_pair()
                r = n1 / d1 + n2 / d2
                if ok_frac(r) and r < 2: add(f"{n1}/{d1} + {n2}/{d2}", r, "frac", "分数加")
            for _ in range(40):
                n1, d1, n2, d2 = frac_pair()
                v1, v2 = n1 / d1, n2 / d2
                if v1 <= v2: n1, d1, n2, d2 = n2, d2, n1, d1
                r = n1 / d1 - n2 / d2
                if r > 0 and ok_frac(r): add(f"{n1}/{d1} - {n2}/{d2}", r, "frac", "分数减")
        elif level == 2: # 分数乘除（都用最简分数）
            for _ in range(40):
                n1, d1, n2, d2 = frac_pair()
                r = (n1 * n2) / (d1 * d2)
                if ok_frac(r): add(f"{n1}/{d1} × {n2}/{d2}", r, "frac", "分数乘")
            for _ in range(40):
                n1, d1, n2, d2 = frac_pair()
                r = (n1 * d2) / (d1 * n2)
                if ok_frac(r) and r < 5: add(f"{n1}/{d1} ÷ {n2}/{d2}", r, "frac", "分数除")
        elif level == 3: # 三数互化：分数↔小数↔百分数
            fr = [(1, 2, 0.5, 50), (1, 4, 0.25, 25), (3, 4, 0.75, 75), (1, 5, 0.2, 20),
                  (2, 5, 0.4, 40), (3, 5, 0.6, 60), (4, 5, 0.8, 80), (1, 10, 0.1, 10),
                  (7, 10, 0.7, 70), (9, 10, 0.9, 90), (1, 8, 0.125, 12.5)]
            for _ in range(32):
                n, d, dec, pct = random.choice(fr)
                t = random.randint(0, 3)
                if t == 0:   add(f"{n}/{d} = ?（填小数）", dec, "conv", "互化")
                elif t == 1: add(f"{dec} = ?（填百分数）", pct, "conv", "互化")
                elif t == 2: add(f"{pct}% = ?（填小数）", dec, "conv", "互化")
                else:        add(f"{dec} = ?/100（填分子）", round(dec * 100, 4), "conv", "互化")
        else:            # 混合口算
            for _ in range(12):
                d = random.randint(3, 9); n = random.randint(2, d - 1)
                if gcd(n, d) == 1: add(f"1 - {n}/{d}", 1 - n / d, "frac", "分数减")
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

    # 去重（按题目文本）+ 截断 35
    seen, out = set(), []
    for q in qs:
        if q["q"] not in seen:
            q["id"] = f"g{grade}-l{level}-{len(out)}"
            out.append(q); seen.add(q["q"])
        if len(out) >= 35: break
    return out

def main():
    bank = []
    for g in range(1, 7):
        for lv in range(1, 5):
            bank.extend(gen_cell(g, lv))
    path = os.path.join(os.path.dirname(__file__), "..", "data", "banks", "math-oral.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(bank, f, ensure_ascii=False, indent=1)
    print(f"OK: {len(bank)} questions -> {os.path.normpath(path)}")

if __name__ == "__main__":
    main()
