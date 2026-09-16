# -*- coding: utf-8 -*-
"""v3.11 一、二年级英语词库重建：对齐沪教牛津版（深圳）一年级上册 / 二年级上册。

背景：深圳英语为一年级起点（部分学校开设），教材为上海教育出版社《英语》
（沪教牛津深圳版）。此前 g1/g2 词库为泛用启蒙词，本次按教材 12 单元分主题重建。
词表来源：教材配套分单元单词表（公共词汇事实，无课文原文）。

运行：python tools/gen_english_words_g12.py
（读取 data/banks/english-words.json，仅替换 grade 1/2 的题目，3~6 年级保持不变）
"""
import json
import random

OUT = 'data/banks/english-words.json'

# 单元主题词表：(主题tag, [(英文, 中文), ...])，按教材单元顺序
G1 = [
    ('打招呼',   [('hello', '你好'), ('hi', '嗨'), ('goodbye', '再见'), ('morning', '早上'),
                 ('afternoon', '下午'), ('school', '学校'), ('day', '一天')]),
    ('同学与文具', [('book', '书'), ('ruler', '尺子'), ('pencil', '铅笔'), ('rubber', '橡皮'),
                 ('please', '请'), ('thank', '谢谢'), ('give', '给'), ('you', '你'),
                 ('Sunday', '星期天'), ('nice', '美好的')]),
    ('我的五官', [('face', '脸'), ('mouth', '嘴巴'), ('nose', '鼻子'), ('eye', '眼睛'),
                 ('ear', '耳朵'), ('touch', '摸'), ('picture', '图画'), ('look', '看'),
                 ('my', '我的'), ('your', '你的')]),
    ('我会做',   [('sing', '唱歌'), ('dance', '跳舞'), ('read', '读'), ('draw', '画画'), ('can', '能')]),
    ('我的家人', [('father', '爸爸'), ('mother', '妈妈'), ('grandmother', '奶奶（外婆）'),
                 ('grandfather', '爷爷（外公）'), ('she', '她'), ('he', '他'), ('who', '谁')]),
    ('我的朋友', [('tall', '高的'), ('short', '矮的'), ('fat', '胖的'), ('thin', '瘦的'),
                 ('classmate', '同学'), ('friend', '朋友')]),
    ('数一数',   [('one', '一'), ('two', '二'), ('three', '三'), ('four', '四'), ('five', '五'),
                 ('six', '六'), ('count', '数数'), ('how many', '多少')]),
    ('买水果',   [('apple', '苹果'), ('pear', '梨'), ('peach', '桃子'), ('orange', '桔子'),
                 ('supermarket', '超市')]),
    ('买食物',   [('pie', '果馅饼'), ('hamburger', '汉堡包'), ('pizza', '比萨饼'),
                 ('cake', '蛋糕'), ('snack', '点心'), ('bar', '小吃部')]),
    ('农场动物', [('cow', '奶牛'), ('chick', '小鸡'), ('duck', '鸭子'), ('pig', '猪'), ('that', '那')]),
    ('动物园',   [('monkey', '猴子'), ('bear', '熊'), ('panda', '熊猫'), ('tiger', '老虎')]),
    ('公园与颜色', [('colour', '颜色'), ('yellow', '黄色'), ('red', '红色'), ('blue', '蓝色'),
                 ('green', '绿色'), ('big', '大的'), ('small', '小的')]),
]
G1_CORE = {'hello', 'book', 'face', 'sing', 'mother', 'friend', 'three',
           'apple', 'cake', 'cow', 'panda', 'red'}  # 核心词双向各出一题

G2 = [
    ('日常问候', [('evening', '晚上'), ('night', '夜晚'), ('today', '今天'), ('mum', '妈妈'),
                 ('morning', '早晨'), ('afternoon', '下午')]),
    ('自我介绍', [('boy', '男孩'), ('girl', '女孩'), ('big', '大的'), ('small', '小的'),
                 ('name', '名字')]),
    ('你是谁',   [('sorry', '对不起'), ('seven', '七'), ('eight', '八'), ('nine', '九'),
                 ('ten', '十'), ('elephant', '大象')]),
    ('我会运动', [('swim', '游泳'), ('run', '跑'), ('write', '写字'), ('fly', '飞'),
                 ('ride a bicycle', '骑自行车'), ('giraffe', '长颈鹿')]),
    ('我的家庭', [('family', '家庭'), ('brother', '弟弟'), ('sister', '姐姐（妹妹）'),
                 ('young', '年轻的'), ('old', '年老的'), ('insect', '昆虫'), ('jellyfish', '水母')]),
    ('外貌特征', [('hair', '头发'), ('head', '头'), ('long', '长的'), ('now', '现在'),
                 ('kangaroo', '袋鼠'), ('lion', '狮子')]),
    ('游乐场',   [('playground', '操场'), ('slide', '滑梯'), ('swing', '秋千'), ('seesaw', '跷跷板')]),
    ('我的房间', [('room', '房间'), ('bag', '包'), ('box', '箱子'), ('chair', '椅子'),
                 ('desk', '书桌'), ('car', '小汽车'), ('pencil case', '铅笔盒'), ('sleep', '睡觉')]),
    ('晚餐',     [('dinner', '晚饭'), ('plate', '盘子'), ('chopsticks', '筷子'), ('bowl', '碗'),
                 ('spoon', '勺子'), ('ready', '准备好的')]),
    ('天空',     [('sky', '天空'), ('moon', '月亮'), ('sun', '太阳'), ('star', '星星'),
                 ('bright', '明亮的'), ('snake', '蛇')]),
    ('森林动物', [('forest', '森林'), ('fox', '狐狸'), ('hippo', '河马'), ('grass', '草'),
                 ('animal', '动物'), ('cute', '可爱的'), ('dove', '鸽子'), ('swan', '天鹅'),
                 ('white', '白色的')]),
    ('爱护花草', [('street', '大街'), ('flower', '花'), ('climb', '爬'), ('tree', '树'),
                 ('park', '公园'), ('beautiful', '美丽的'), ('cry', '哭'), ('zebra', '斑马')]),
]
G2_CORE = {'night', 'name', 'ten', 'swim', 'family', 'hair', 'chair',
           'dinner', 'moon', 'forest', 'flower', 'beautiful'}

rng = random.Random(20260916)


def unit_level(u_idx):
    """单元顺序 → 段位 1~6（前易后难）。"""
    return min(6, u_idx // 2 + 1)


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
