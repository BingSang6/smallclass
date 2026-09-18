# -*- coding: utf-8 -*-
"""gen_poems_textbook.py — v3.17 课本必背古诗（g1/g4）
背景：poems.json v3.5 是《唐诗三百首》全量通用池（1837 题全 grade=0），
孩子抽到大量没学过的诗。本脚本把 1/4 年级课本必背篇目打上年级标追加到池尾：
  - g1 部编一上：咏鹅(园地)→画→悯农其二→风→江南(课文)→古朗月行(节选)
  - g4 部编四上：暮江吟→题西林壁→雪梅(第一单元古诗三首)、出塞→凉州词→夏日绝句(第七单元)
段位(1~6) = 篇目；题型：接下句/接上句/出自哪首诗/作者/名句理解；
干扰项全部取自同年级课内篇目（孩子认识）。古诗词公版，可全文引用。
追加到 poems.json 末尾（pt-id 接续，不动原 1837 题的 id）。
"""
import json, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# (title, author, [(前句, 后句)], level, 理解题 or None)
G1 = [
    ('咏鹅', '骆宾王', [('鹅，鹅，鹅', '曲项向天歌'), ('白毛浮绿水', '红掌拨清波')], 1, None),
    ('画', None, [('远看山有色', '近听水无声'), ('春去花还在', '人来鸟不惊')], 2,
     ('"人来鸟不惊"是因为？', '画里的鸟不会飞走', ['鸟睡着了', '鸟听不见'], '这是一幅画')),
    ('悯农（其二）', '李绅', [('锄禾日当午', '汗滴禾下土'), ('谁知盘中餐', '粒粒皆辛苦')], 3,
     ('"粒粒皆辛苦"告诉我们要？', '爱惜粮食', ['浪费粮食', '多吃零食'], '每粒米都来得辛苦')),
    ('风', '李峤', [('解落三秋叶', '能开二月花'), ('过江千尺浪', '入竹万竿斜')], 4, None),
    ('江南', '汉乐府', [('江南可采莲', '莲叶何田田'), ('鱼戏莲叶东', '鱼戏莲叶西'),
                     ('鱼戏莲叶南', '鱼戏莲叶北')], 5, None),
    ('古朗月行（节选）', '李白', [('小时不识月', '呼作白玉盘'), ('又疑瑶台镜', '飞在青云端')], 6, None),
]
G4 = [
    ('暮江吟', '白居易', [('一道残阳铺水中', '半江瑟瑟半江红'), ('可怜九月初三夜', '露似真珠月似弓')], 1,
     ('"半江瑟瑟半江红"写的是什么时候的江面？', '傍晚（残阳照射）', ['清晨', '深夜'], '残阳=傍晚的太阳')),
    ('题西林壁', '苏轼', [('横看成岭侧成峰', '远近高低各不同'), ('不识庐山真面目', '只缘身在此山中')], 2,
     ('《题西林壁》蕴含哲理的句子是？', '不识庐山真面目，只缘身在此山中',
      ['梅须逊雪三分白，雪却输梅一段香', '秦时明月汉时关，万里长征人未还'], '当局者迷，旁观者清')),
    ('雪梅', '卢钺', [('梅雪争春未肯降', '骚人阁笔费评章'), ('梅须逊雪三分白', '雪却输梅一段香')], 3,
     ('"梅须逊雪三分白，雪却输梅一段香"说明？', '各有所长（取长补短）', ['梅比雪好', '雪比梅好'], '人和事物各有长短')),
    ('出塞', '王昌龄', [('秦时明月汉时关', '万里长征人未还'), ('但使龙城飞将在', '不教胡马度阴山')], 4,
     ('"但使龙城飞将在"里的"飞将"指谁？', '李广（飞将军）', ['李白', '王昌龄'], '汉代飞将军李广')),
    ('凉州词', '王翰', [('葡萄美酒夜光杯', '欲饮琵琶马上催'), ('醉卧沙场君莫笑', '古来征战几人回')], 5,
     ('"古来征战几人回"表达的是？', '战争的残酷（战士的悲壮）', ['旅游的快乐', '丰收的喜悦'], '边塞诗的悲壮')),
    ('夏日绝句', '李清照', [('生当作人杰', '死亦为鬼雄'), ('至今思项羽', '不肯过江东')], 6,
     ('"生当作人杰"表达的是？', '做人要有英雄气节', ['贪生怕死', '吃喝玩乐'], '李清照赞项羽讽南宋')),
]

# 兜底干扰句：同年级同字数句不够时用（课标内公版名句，孩子大概率认识）
FALLBACK = {5: ['欲穷千里目', '更上一层楼', '春种一粒粟', '秋收万颗子'],
            7: ['两岸猿声啼不住', '明月何时照我还', '映日荷花别样红', '春风不度玉门关']}

def build(grade, poems):
    titles = [p[0] for p in poems]
    out = []
    for title, author, pairs, lv, understand in poems:
        others = [p for p in poems if p[0] != title]
        # 同年级、同字数的课内句做干扰项（孩子认识）；不够用课标名句兜底
        def wrong_for(text, which):
            cands = list(dict.fromkeys(
                (y if which == 'b' else x)
                for p in others for (x, y) in p[2]
                if len(y if which == 'b' else x) == len(text)))
            for fb in FALLBACK.get(len(text), []):
                if len(cands) >= 2:
                    break
                if fb != text and fb not in cands:
                    cands.append(fb)
            return cands[:2]
        for a, b in pairs:
            wl = wrong_for(b, 'b')
            out.append(('《%s》接下句：%s，（　）' % (title, a), b, wl, '背一背《%s》' % title, lv, title))
            wp = wrong_for(a, 'a')
            out.append(('《%s》接上句：（　），%s' % (title, b), a, wp, '背一背《%s》' % title, lv, title))
        # 出自哪首诗（每首取 1 联）
        first = pairs[0]
        wt = [t for t in titles if t != title][:2]
        out.append(('"%s，%s"出自哪首诗？' % (first[0], first[1]), title, wt, '想一想课本里的诗名', lv, title))
        # 作者（无名氏/汉乐府不出）
        if author and author != '汉乐府':
            wa = [p[1] for p in others if p[1] and p[1] != '汉乐府' and p[1] != author][:2]
            while len(wa) < 2:
                wa.append('杜甫' if '杜甫' not in wa else '白居易')
            out.append(('《%s》的作者是谁？' % title, author, wa, '《%s》作者是%s' % (title, author), lv, title))
        # 名句理解
        if understand:
            out.append((understand[0], understand[1], understand[2], understand[3], lv, title))
    return [(q, a, w, why, lv, grade, t) for (q, a, w, why, lv, t) in out]

def main():
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'banks', 'poems.json')
    bank = json.load(open(path, encoding='utf-8'))
    # 幂等：先清掉旧 ptx-（课本题）再追加，重复运行不膨胀
    bank = [q for q in bank if not str(q.get('id', '')).startswith('ptx-')]
    base = len(bank)
    assert len(set(q['id'] for q in bank)) == base, 'id 重复'
    assert all(q['id'].startswith('pt-') for q in bank), '意外前缀'
    added = build(1, G1) + build(4, G4)
    for i, (q, a, wrongs, why, lv, grade, title) in enumerate(added):
        assert len({str(a), str(wrongs[0]), str(wrongs[1])}) == 3, q
        bank.append({
            'q': q, 'a': str(a), 'options': [str(w) for w in wrongs],
            'wrongReasons': [why, '再背一背这首诗'],
            'grade': grade, 'level': lv, 'tag': '古诗·' + title,
            'speak': q.replace('？', '').replace('（　）', ''),
            'id': 'ptx-%d' % i
        })
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(bank, f, ensure_ascii=False, indent=1)
    print('追加课本古诗 %d 题（g1 %d / g4 %d），全库 %d' % (
        len(added), sum(1 for x in added if x[5] == 1), sum(1 for x in added if x[5] == 4), len(bank)))

if __name__ == '__main__':
    main()
