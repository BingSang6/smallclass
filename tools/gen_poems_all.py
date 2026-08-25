# -*- coding: utf-8 -*-
"""gen_poems_all.py — 古诗大题库 v3.5（全年级通用池 + 段位分难度）
题源：chinese-poetry 开源库《唐诗三百首》（公版）+ 现有 KB 课标古诗
规则（家长需求）：
  - 不分年级：所有题目 grade=0（全年级通用），任何年级进古诗都是同一个大池
  - 按段位分难度：五言绝句→1~2 段位，七言绝句→2~3，五言律诗→3~4，七言律诗→4~6
产出：data/banks/poems.json（覆盖）
"""
import json, os, random, re
from zhconv import convert

random.seed(42)

SRC = os.path.join(os.path.dirname(__file__), 'tang300.json')  # 下载到 tools/ 下
OLD = os.path.join(os.path.dirname(__file__), '..', 'data', 'banks', 'poems.json')
OUT = OLD

# 体裁 → 段位范围
GENRE_LV = {'五言絕句': (1, 2), '五言唐詩': (1, 2), '七言絕句': (2, 3), '五言律詩': (3, 4), '七言律詩': (4, 6), '五言古詩': (3, 5), '七言古詩': (4, 6)}

def clean_sent(s):
    return re.sub(r'[（(].*?[)）]', '', s)

def split_lines(paragraphs):
    """把段落切成完整句（逗号/句号分隔），成对返回 [(前句, 后句)]"""
    lines = []
    for p in paragraphs:
        parts = [x for x in re.split(r'[，。？！]', clean_sent(p)) if x.strip()]
        for i in range(0, len(parts) - 1, 2):
            lines.append((parts[i].strip(), parts[i + 1].strip()))
    return lines

def main():
    raw = json.load(open(SRC, encoding='utf-8'))
    poems = []   # {title, author, genre, lv, lines}
    seen_titles = set()
    for ch in raw['content']:
        genre = ch['type']
        lo, hi = GENRE_LV.get(genre, (3, 5))
        items = ch['content']
        for i, it in enumerate(items):
            title = convert(it['chapter'], 'zh-cn')
            if title in seen_titles:
                continue
            seen_titles.add(title)
            author = convert(it.get('author') or '佚名', 'zh-cn')
            paras = [convert(p, 'zh-cn') for p in it['paragraphs']]
            lines = split_lines(paras)
            if len(lines) < 1:
                continue
            lv = lo + (hi - lo) * i // max(1, len(items))   # 体裁内由易到难
            poems.append({'title': title, 'author': author, 'genre': convert(genre, 'zh-cn'), 'lv': max(1, min(6, lv)), 'lines': lines, 'sents': [s for p in paras for s in re.split(r'[。？！]', clean_sent(p)) if s.strip()]})

    print('唐诗三百首解析：', len(poems), '首')

    # 干扰项池
    ALL_SENTS = [l[0] + '，' + l[1] for pm in poems for l in pm['lines']]
    ALL_TITLES = [pm['title'] for pm in poems]
    ALL_AUTHORS = list({pm['author'] for pm in poems})

    def pick_dist(exclude, pool, n=2):
        cands = [x for x in pool if x != exclude]
        random.shuffle(cands)
        return cands[:n]

    out = []
    def add(q, a, wrongs, lv, tag, why, title):
        out.append({'q': q, 'a': a, 'options': wrongs,
                    'wrongReasons': [why], 'grade': 0, 'level': lv, 'tag': tag,
                    'speak': q.replace('（　）', '').replace('《', '').replace('》', ''),
                    'id': 'pt-%d' % len(out)})

    for pm in poems:
        t, au, lv = pm['title'], pm['author'], pm['lv']
        tag = '古诗·' + t
        # 接下句 / 接上句（每首最多 2+2 句）
        for a, b in pm['lines'][:2]:
            add('《%s》接下句：%s，（　）' % (t, a), b,
                pick_dist(b, [l[1] for pm2 in poems for l in pm2['lines']]), lv, tag,
                '背一背《%s》：%s，%s' % (t, a, b), t)
        for a, b in pm['lines'][:2][::-1]:
            add('《%s》接上句：（　），%s' % (t, b), a,
                pick_dist(a, [l[0] for pm2 in poems for l in pm2['lines']]), lv, tag,
                '背一背《%s》：%s，%s' % (t, a, b), t)
        # 出处（首个完整句 → 诗名）
        if pm['sents']:
            s = pm['sents'][0]
            add('“%s”出自哪首诗？' % s, '《%s》' % t, ['《%s》' % x for x in pick_dist(t, ALL_TITLES)],
                min(6, lv + 1), tag, '《%s》，%s（%s）' % (t, pm['lines'][0][0] + '，' + pm['lines'][0][1], au), t)
        # 作者
        add('《%s》的作者是谁？' % t, au, pick_dist(au, ALL_AUTHORS), lv, tag,
            '《%s》是%s写的' % (t, au), t)

    # 合并旧 KB 题（课标古诗题保留，grade 改 0 全年级通用），按诗名去重（旧题优先保留出处/释义特色题）
    old = json.load(open(OLD, encoding='utf-8'))
    old_titles = set()
    for q in old:
        m = re.search(r'《(.+?)》', q['q'])
        if m:
            old_titles.add(m.group(1))
    dup = 0
    for q in old:
        q['grade'] = 0
        # 唐诗300 与旧题同一首 → 丢掉新库中重复首（直接跳过旧题更简单：保留旧题，其内容 KB 更贴合年级）
        if q['id'].startswith('po-'):
            out.append(q)
    # 去掉与旧题同首的新题
    final = []
    for q in out:
        m = re.search(r'《(.+?)》', q['q'])
        if m and m.group(1) in old_titles:
            dup += 1
            continue
        final.append(q)

    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(final, f, ensure_ascii=False, indent=1)
    from collections import Counter
    print('合并去重 %d 首重复' % dup)
    print('总计 %d 题（旧 KB %d + 唐诗三百首新增 %d）' % (len(final), len(old), len(final) - len(old)))
    print('按段位：', dict(sorted(Counter(q['level'] for q in final).items())))

if __name__ == '__main__':
    main()
