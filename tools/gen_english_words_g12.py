# -*- coding: utf-8 -*-
"""v3.12 一、二年级英语词库重建：对齐深圳 2025 新教材《英语（口语交际）》。

背景：深圳 2025 秋起小一使用上海教育出版社《英语（口语交际）》（广东省审定，
沪教版新编），每年级上册 6 个单元、每单元一个主题（家庭/感觉/数字文具/…），
无字母起步、每单元末设 Letters 页。二年级上册同套新教材。
此前 v3.11 的经典版 12 单元词表（Hello/My classmates/…）已过时，本次整体替换。
词表来源：教材配套分单元单词表（公共词汇事实，无课文原文）。

运行：python tools/gen_english_words_g12.py
（读取 data/banks/english-words.json，仅替换 grade 1/2 的题目，3~6 年级保持不变）
"""
import json
import random

OUT = 'data/banks/english-words.json'

# 单元主题词表：(主题tag, [(英文, 中文), ...])，按教材单元顺序（6 单元）
G1 = [
    ('家庭',   [('family', '家；家庭'), ('grandpa', '爷爷；外公'), ('grandma', '奶奶；外婆'),
                 ('dad', '爸爸'), ('mum', '妈妈'), ('brother', '兄；弟'), ('sister', '姐；妹'),
                 ('This is my...', '这是我的……'), ('hungry', '饿的'),
                 ('magic', '魔法的'), ('noodles', '面条'), ('magic noodles', '魔法面条'),
                 ('yarn', '毛线')]),
    ('感觉',   [('cold', '冷的'), ('hot', '热的'), ('thirsty', '口渴的'), ('hungry', '饿的')]),
    ('数字与文具', [('one', '一'), ('two', '二'), ('three', '三'), ('four', '四'),
                 ('pencil case', '铅笔盒'), ('eraser', '橡皮'), ('pencil', '铅笔'), ('ruler', '直尺')]),
    ('动作',   [('draw', '画'), ('write', '写；书写'), ('read', '阅读'), ('sing', '唱歌'),
                 ('dance', '跳舞')]),
    ('宠物',   [('dog', '狗'), ('cat', '猫'), ('fish', '鱼'), ('bird', '鸟'),
                 ('hamster', '仓鼠'), ('tortoise', '乌龟')]),
    ('颜色',   [('red', '红色'), ('white', '白色'), ('yellow', '黄色'), ('green', '绿色'),
                 ('blue', '蓝色'), ('black', '黑色')]),
]
G1_CORE = {'family', 'hot', 'three', 'draw', 'dog', 'red'}  # 每单元核心词双向各出一题

G2 = [
    ('五感',   [('feel', '感觉到'), ('see', '看见'), ('smell', '闻到'), ('hear', '听见'),
                 ('taste', '尝一尝')]),
    ('亲属',   [('uncle', '叔叔；舅舅'), ('aunt', '阿姨；姑姑'), ('cousin', '堂（表）兄弟姐妹'),
                 ('old', '年纪大的'), ('young', '年轻的'), ('cute', '可爱的')]),
    ('玩具',   [('doll', '洋娃娃'), ('toy plane', '玩具飞机'), ('toy bear', '玩具熊'),
                 ('ball', '球'), ('robot', '机器人'), ('jigsaw puzzle', '拼图')]),
    ('场所',   [('pet shop', '宠物店'), ('fruit shop', '水果店'), ('cinema', '电影院'),
                 ('zoo', '动物园'), ('park', '公园'), ('toy shop', '玩具店')]),
    ('农场动物', [('cow', '奶牛'), ('sheep', '羊'), ('duck', '鸭子'), ('chick', '小鸡'),
                 ('chicken', '鸡'), ('pig', '猪')]),
    ('节日',   [('play with lanterns', '玩灯笼'), ('eat mooncakes', '吃月饼'),
                 ('solve riddles', '猜谜语'), ('look at the moon', '看月亮')]),
]
G2_CORE = {'see', 'uncle', 'robot', 'zoo', 'cow', 'eat mooncakes'}

rng = random.Random(20260916)


def unit_level(u_idx):
    """单元顺序 → 段位：新版每册 6 单元，一单元一段位（1~6）。"""
    return min(6, u_idx + 1)


def build(grade, units, core):
    words = [(en, zh, tag, unit_level(i)) for i, (tag, ws) in enumerate(units) for en, zh in ws]
    ens = [w[0] for w in words]
    zhs = [w[1] for w in words]
    out = []

    def add(en, zh, tag, level, to_en):
        if to_en:
            q = '「%s」的英文是？' % zh
            a = en
            pool = [e for e in ens if e != en and e.lower() != en.lower()]
            why = ['%s = %s' % (zh, en), '注意拼写，跟着读音记']
            speak = '%s的英文是' % zh
        else:
            q = '%s 是什么意思？' % en
            a = zh
            pool = [z for z in zhs if z != zh]
            why = ['%s = %s' % (en, zh), '多读几遍，连着中文意思一起记']
            speak = '%s 是什么意思' % en
        wrongs = rng.sample(pool, 2)
        out.append({
            'q': q, 'a': a, 'options': wrongs, 'wrongReasons': why,
            'grade': grade, 'level': level, 'tag': '英语单词·' + tag,
            'speak': speak, 'id': 'e%d-%03d' % (grade, len(out)),
        })

    for i, (en, zh, tag, level) in enumerate(words):
        add(en, zh, tag, level, to_en=(i % 2 == 1))   # 交替方向
        if en in core:                                 # 核心词补另一方向
            add(en, zh, tag, level, to_en=(i % 2 == 0))
    return out


def main():
    bank = json.load(open(OUT, encoding='utf-8'))
    kept = [q for q in bank if q['grade'] not in (1, 2)]        # 3~6 年级原样保留
    new = build(1, G1, G1_CORE) + build(2, G2, G2_CORE)
    merged = sorted(kept, key=lambda q: q['grade'])             # 按年级归位
    # 组装：g1, g2 在前，3~6 依次在后
    final = [q for q in new if q['grade'] == 1] + [q for q in new if q['grade'] == 2] + merged
    json.dump(final, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    ids = [q['id'] for q in final]
    assert len(ids) == len(set(ids)), 'duplicate ids'
    for q in final:
        assert len(q['options']) == 2 and q['a'] not in q['options']
    print('grade1:', sum(1 for q in final if q['grade'] == 1),
          'grade2:', sum(1 for q in final if q['grade'] == 2),
          'total:', len(final))


if __name__ == '__main__':
    main()
