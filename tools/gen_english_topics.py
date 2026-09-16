# -*- coding: utf-8 -*-
"""gen_english_topics.py — 英语·专题训练题库生成器（v3.10）
专题 = 跨单元的语法/功能专项（沪教版小学英语通用语法点，按年级分层）：
  三年级：疑问词、be 动词
  四年级：人称代词、方位介词
  五年级：一般现在时、可数与不可数
  六年级：一般过去时、比较级
产出：data/banks/english-topics.json（q.unit = '专题·xxx'，复用单元巩固流程；level 0 不进段位池）
通用语法知识，无版权问题。
"""

# (专题名, 年级, [(题面, 答案, [干扰1, 干扰2], 错因解释), ...])
TOPICS = [
  ('专题·疑问词', 3, [
    ('问「是什么东西」用哪个疑问词？', 'What', ['Where', 'Who'], 'What 问事物，Where 问地点，Who 问人'),
    ('（　）is your bag? — It\'s on the desk. 选哪个疑问词？', 'Where', ['What', 'How many'], '回答是地点，用 Where 问地点'),
    ('（　）is that girl? — She\'s my sister. 选哪个疑问词？', 'Who', ['What', 'Where'], '回答是人，用 Who 问人'),
    ('（　）books do you have? — Five. 选哪个疑问词？', 'How many', ['How old', 'What'], '回答是数量，用 How many 问数量'),
    ('How old 用来问什么？', '年龄', ['数量', '地点'], 'How old = 多大年纪'),
  ]),
  ('专题·be动词', 3, [
    ('I （　） a student. 选哪个 be 动词？', 'am', ['is', 'are'], 'I 永远搭配 am'),
    ('She （　） my English teacher. 选哪个？', 'is', ['am', 'are'], 'she/he/it 等单数用 is'),
    ('We （　） good friends. 选哪个？', 'are', ['is', 'am'], 'we/you/they 复数用 are'),
    ('The cats （　） on the sofa. 选哪个？', 'are', ['is', 'am'], 'cats 是复数，用 are'),
    ('am / is / are 分别搭配谁？', 'I 用 am，单数用 is，复数用 are', ['I 用 is，复数用 am', '可以随意换用'], '口诀：我用 am，单三 is，复数 are'),
  ]),
  ('专题·人称代词', 4, [
    ('「她」做主语时用哪个词？', 'she', ['her', 'hers'], 'she 是主格，做主语'),
    ('（　） is my best friend.（他） 选哪个词？', 'He', ['Him', 'His'], '做主语用主格 He'),
    ('This is （　） ruler.（我的） 选哪个词？', 'my', ['me', 'I'], '名词前面用 my（我的）'),
    ('him 是什么意思？', '他（宾格，做宾语）', ['他的（形容词性物主代词）', '他自己（反身代词）'], 'him 是 he 的宾格，用在动词/介词后'),
    ('Look at （　）!（看我） 选哪个词？', 'me', ['I', 'my'], '介词 at 后面用宾格 me'),
  ]),
  ('专题·方位介词', 4, [
    ('The cat is （　） the box.（在盒子里）', 'in', ['on', 'under'], 'in = 在…里面'),
    ('The book is （　） the desk.（在桌面上）', 'on', ['in', 'under'], 'on = 在…上面（表面有接触）'),
    ('under 的意思是？', '在…下面', ['在…旁边', '在…后面'], 'under = 在…正下方'),
    ('「在…旁边」用哪个词组？', 'next to', ['next on', 'next in'], 'next to = 紧挨着、在旁边'),
    ('The ball is behind the door. behind 是？', '在…后面', ['在…前面', '在…里面'], 'behind 后面；in front of 前面'),
  ]),
  ('专题·一般现在时', 5, [
    ('He （　） to school at seven every day. 选哪个？', 'goes', ['go', 'going'], '主语是三单 he，动词加 es'),
    ('She （　） TV every evening. 选哪个？', 'watches', ['watch', 'watchs'], '以 ch 结尾的三单动词加 es（没有 watchs 这个词）'),
    ('I （　） football on Sundays. 选哪个？', 'play', ['plays', 'playing'], '主语是 I，动词用原形'),
    ('主语是第三人称单数时，一般现在时的动词要？', '加 -s 或 -es', ['加 -ing', '加 -ed'], '三单规则：一般加 s，ch/sh/o 结尾加 es'),
    ('every day / yesterday 哪个是一般现在时的时间标志？', 'every day', ['yesterday', 'tomorrow'], 'every day 表示经常发生，用一般现在时'),
  ]),
  ('专题·可数与不可数', 5, [
    ('water（水）是可数名词还是不可数名词？', '不可数', ['可数', '既是可数又是不可数'], '水不可数，不能说 a water / two waters'),
    ('不可数名词问「多少」用？', 'How much', ['How many', 'How old'], 'How much + 不可数，How many + 可数复数'),
    ('可数名词复数问「多少」用？', 'How many', ['How much', 'What'], 'How many + 可数复数'),
    ('apple 的复数形式是？', 'apples', ['applees', 'apple'], '多数可数名词直接加 s'),
    ('bread（面包）是？', '不可数名词', ['可数名词', '动词'], '面包不可数，一片说 a piece of bread'),
  ]),
  ('专题·一般过去时', 6, [
    ('go 的过去式是？', 'went', ['goed', 'goes'], 'go 是不规则动词，过去式 went'),
    ('I （　） a film last night. 选哪个？', 'watched', ['watch', 'watching'], 'last night 是过去时间，动词用过去式'),
    ('eat 的过去式是？', 'ate', ['eated', 'eats'], 'eat 不规则变化：eat → ate'),
    ('yesterday 是哪个时态的时间标志？', '一般过去时', ['一般现在时', '现在进行时'], 'yesterday 昨天 → 过去的事'),
    ('一般过去时的否定句用什么？', "didn't + 动词原形", ["don't + 动词原形", "didn't + 动词过去式"], "过去时否定用 didn't，后面动词还原成原形"),
  ]),
  ('专题·比较级', 6, [
    ('tall 的比较级是？', 'taller', ['tall', 'tallest'], '单音节形容词直接加 -er'),
    ('big 的比较级是？', 'bigger', ['biger', 'biggest'], '重读闭音节双写 g 再加 -er'),
    ('「A 比 B 高」中的「比」用哪个词？', 'than', ['then', 'that'], '比较级后面用 than 连接（then 是“那时”）'),
    ('good 的比较级是？', 'better', ['gooder', 'more good'], 'good/better/best 是不规则变化'),
    ('This pen is （　） than that one.（更长）', 'longer', ['long', 'longest'], '两样东西比较用比较级 longer'),
  ]),
]


def main():
    import json, os
    out = []
    for uname, grade, qs in TOPICS:
        for q, a, wrongs, why in qs:
            out.append({
                'q': q, 'a': str(a), 'options': [str(w) for w in wrongs],
                'wrongReasons': [why, '再想想这个专题的语法规则'],
                'grade': grade, 'level': 0, 'tag': '英语专题·' + uname.split('·', 1)[1],
                'unit': uname,
                'speak': q.replace('？', '').replace('（　）', '哪个'),
                'id': 'et-%03d' % len(out)
            })
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'banks', 'english-topics.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print('生成', len(out), '道英语专题题')
    for uname, grade, qs in TOPICS:
        print('  %d年级 %-10s %d 题' % (grade, uname, len(qs)))


if __name__ == '__main__':
    main()
