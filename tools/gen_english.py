# -*- coding: utf-8 -*-
"""gen_english.py — 英语·单词题库生成器
题源（唯一事实源）：primary-tutor-skill/knowledge-bases/english-primary-shenzhen-oxford.md
  （沪教牛津深圳版 1~6 年级核心词汇，每年级 6 主题；词汇表为事实性内容，无版权问题）
题型：英文选中文意思 / 中文选英文
产出：data/banks/english-words.json（每词 2 题，按年级分 6 段位 level 1~6）
用法：python tools/gen_english.py [KB路径]   （默认用下方 KB_PATH）
改词表请改知识库 md，不要改本脚本。
"""
import json, os, re, random, sys
random.seed(20260820)

KB_PATH = r'C:\Users\zego01\.zcode\workspace\default\primary-tutor-skill\knowledge-bases\english-primary-shenzhen-oxford.md'
if len(sys.argv) > 1:
    KB_PATH = sys.argv[1]

GRADES = {'一年级': 1, '二年级': 2, '三年级': 3, '四年级': 4, '五年级': 5, '六年级': 6}


def parse_kb(path):
    """解析知识库：# X年级 段落下的 | 主题 | 单词 | 中文 | 表格行"""
    with open(path, encoding='utf-8') as f:
        text = f.read()
    words = {}   # grade -> [(en, zh, topic)]
    grade = None
    for line in text.splitlines():
        m = re.match(r'^#\s*([一二三四五六])年级', line.strip())
        if m:
            grade = GRADES[m.group(1) + '年级']
            words.setdefault(grade, [])
            continue
        if grade is None:
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        # 表头行 / 分隔行跳过；数据行：主题 | 单词 | 中文
        if len(cells) == 3 and cells[1] and cells[2] and cells[1] != '单词' and not set(cells[1]) <= set('-— '):
            words[grade].append((cells[1], cells[2], cells[0]))
    return words


WORDS = parse_kb(KB_PATH)
assert all(len(v) >= 20 for v in WORDS.values()), '每年级词表应 ≥20 词：' + \
    str({g: len(v) for g, v in WORDS.items()})

out = []
for grade in sorted(WORDS):
    ws = WORDS[grade]
    n = len(ws)
    # 按词表顺序分 6 段位（level 1~6，与闯关 p.level+1 对应）
    levels = [min(6, 1 + i * 6 // n) for i in range(n)]
    zh_pool = [z for _, z, _ in ws]
    en_pool = [e for e, _, _ in ws]
    for i, (en, zh, topic) in enumerate(ws):
        lv = levels[i]
        # 英文选中文
        dz = random.sample([x for x in zh_pool if x != zh], 2)
        out.append({
            'q': en + ' 是什么意思？', 'a': zh, 'options': dz,
            'wrongReasons': [en + ' = ' + zh, '多读几遍，连着中文意思一起记'],
            'grade': grade, 'level': lv, 'tag': '英语单词·' + topic,
            'speak': en + ' 是什么意思', 'id': 'e%d-%03d' % (grade, len(out))
        })
        # 中文选英文
        de = random.sample([x for x in en_pool if x != en], 2)
        out.append({
            'q': '「' + zh + '」的英文是？', 'a': en, 'options': de,
            'wrongReasons': [zh + ' = ' + en, '注意拼写，跟着读音记'],
            'grade': grade, 'level': lv, 'tag': '英语单词·' + topic,
            'speak': zh + '的英文是', 'id': 'e%d-%03d' % (grade, len(out))
        })

path = os.path.join(os.path.dirname(__file__), '..', 'data', 'banks', 'english-words.json')
with open(path, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print('题源 KB:', KB_PATH)
print('生成', len(out), '道英语题 →', os.path.normpath(path))
for g in sorted(WORDS):
    topics = []
    for _, _, t in WORDS[g]:
        if t not in topics:
            topics.append(t)
    print('  %d年级: %d 词 / %d 题 / 主题: %s' % (g, len(WORDS[g]),
          sum(1 for x in out if x['grade'] == g), '、'.join(topics)))
