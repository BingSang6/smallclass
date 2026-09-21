# -*- coding: utf-8 -*-
"""gen_english_words_add.py — v3.20 英语·单词主库段位重构（g1/g4 难度层，对齐 v3.18 标准）
1) 重分层：g1/g4 现有题只有两种格式——「X 是什么意思？」(词义认读 180 题)→L1、「的英文是」
   (拼写产出 179 题)→L2（id 不变，wrongPool 不失效）；2/3/5/6 保持主题段位不动。
2) 回填：全库补 dif(=level)/tp/src 元数据（题面不动）。
3) ADD：g1/g4 各 +63（L3 情景应答 20 / L4 句型运用 20 / L5 综合挑战 20 + L1 判断 3），
   新题型=情景应答/句型运用/形近词辨析/语境选词/判断题；内容取公共词表与通用日常表达，
   不引教材课文原文。id=ex{g}-{n}，幂等（先清 ex 再追加）。
出题纪律：唯一答案断言（含近义双答检查的设计要求）、干扰项不重复、判断题 2 选项、每层 ≥20。
"""
import json, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'banks', 'english-words.json')

# ADD[grade] = [(q, a, [干扰×2], why, tp, lv)]
ADD = {
 1: [
  # L1 判断（低年级友好）
  ('判断：family 的意思是「家庭」。', '正确', ['错误'], 'family=家；家庭', '判断', 1),
  ('判断：cat 的意思是「狗」。', '错误', ['正确'], 'cat=猫，dog 才是狗', '判断', 1),
  ('判断：red 是一种颜色。', '正确', ['错误'], 'red=红色', '判断', 1),
  # L3 情景应答（口语交际一上 + 日常礼貌用语）
  ('早上见到老师，你应该说？', 'Good morning!', ['Good night!', 'Goodbye!'], '早上问好用 Good morning', '情景', 3),
  ('「下午好」用英语说？', 'Good afternoon!', ['Good morning!', 'Good night.'], '下午好用 afternoon', '情景', 3),
  ('别人帮了你，要说？', 'Thank you!', ['Sorry!', 'Hello!'], '感谢用 Thank you', '情景', 3),
  ('「What is your name?」在问什么？', '你叫什么名字', ['你几岁', '你在哪里'], 'name=名字', '情景', 3),
  ('别人问你 How are you?，你可以回答？', "I'm fine, thank you.", ['My name is Ann.', 'This is a pen.'], '问候答身体好', '情景', 3),
  ('把东西递给别人，说？', 'Here you are.', ['How are you?', 'What is it?'], '递东西说 Here you are', '情景', 3),
  ('「Nice to meet you.」怎么回答？', 'Nice to meet you, too.', ['Good morning.', 'See you.'], 'too=也', '情景', 3),
  ('做错事向别人道歉，说？', 'Sorry.', ['Thank you.', 'OK.'], '道歉用 Sorry', '情景', 3),
  ('「Stand up, please.」是什么意思？', '请起立', ['请坐下', '请举手'], 'stand up=起立', '情景', 3),
  ('「Sit down, please.」是什么意思？', '请坐下', ['请起立', '请出去'], 'sit down=坐下', '情景', 3),
  ('放学和同学道别，说？', 'Goodbye!', ['Good morning!', 'Hello!'], '道别用 Goodbye', '情景', 3),
  ('「How old are you?」在问什么？', '你几岁', ['你叫什么名字', '你身体好吗'], 'old=岁', '情景', 3),
  ('介绍自己「我是安」，说？', 'I am Ann.', ['You are Ann.', 'This is Ann.'], '介绍自己用 I am', '情景', 3),
  ('「What is it?」是什么意思？', '它是什么', ['它是猫', '它在哪里'], 'What is it?=它是什么', '情景', 3),
  ('夸别人的东西好看，说？', "It's nice!", ["It's not good.", "I don't like it."], '夸奖用 nice', '情景', 3),
  ('「Let\'s play!」是什么意思？', '我们一起玩吧', ['我们一起睡觉吧', '他一个人玩'], "Let's=让我们一起", '情景', 3),
  ('「Open the door, please.」是什么意思？', '请开门', ['请关门', '请开窗'], 'open=打开', '情景', 3),
  ('「What colour is it?」在问什么？', '它是什么颜色', ['它几岁', '它叫什么'], 'colour=颜色', '情景', 3),
  ('「I like the dog.」是什么意思？', '我喜欢这只狗', ['我不喜欢狗', '我有一只狗'], 'like=喜欢', '情景', 3),
  ('别人对你说 Happy birthday!，你回答？', 'Thank you!', ['Happy New Year!', 'Merry Christmas!'], '别人祝你生日，说谢谢', '情景', 3),
  # L4 句型运用（I am / This is / I can / 疑问词）
  ('I ___ a boy.（我是一个男孩）选词填空', 'am', ['is', 'are'], 'I 配 am', '句型', 4),
  ('You ___ my friend.（你是我的朋友）', 'are', ['am', 'is'], 'you 配 are', '句型', 4),
  ('This ___ my mother.（这是我的妈妈）', 'is', ['am', 'are'], 'this 配 is', '句型', 4),
  ('I can ___.（跑步）', 'run', ['runs', 'ran'], 'can 后面用动词原形', '句型', 4),
  ('I like ___.（猫）', 'cats', ['cat', 'catt'], 'like 后名词用复数', '句型', 4),
  ('「我有一个书包」说？', 'I have a schoolbag.', ['I am a schoolbag.', 'This is a schoolbag.'], '有=have', '句型', 4),
  ('What is ___?（它）', 'it', ['he', 'she'], '它=it', '句型', 4),
  ('___ you Ann?（你是安吗）', 'Are', ['Am', 'Is'], 'you 配 are', '句型', 4),
  ('「这是我的铅笔」说？', 'This is my pencil.', ['I am a pencil.', 'That is your pencil.'], 'this is=这是', '句型', 4),
  ('I ___ six.（我六岁）', 'am', ['is', 'are'], 'I 配 am', '句型', 4),
  ('Look ___ me!（看着我）', 'at', ['on', 'in'], 'look at=看着', '句型', 4),
  ('「我们一起唱歌吧」说？', "Let's sing!", ['Let me sing.', 'I can dance.'], "Let's=让我们一起", '句型', 4),
  ('___ your name?（你叫什么名字）', "What's", ["Where's", "Who's"], '问名字用 what', '句型', 4),
  ('She ___ my sister.（她是我的姐姐）', 'is', ['am', 'are'], 'she 配 is', '句型', 4),
  ('「我能看到一只鸟」说？', 'I can see a bird.', ['I am see a bird.', 'I can a bird.'], 'can+动词原形', '句型', 4),
  ('It ___ a long nose.（它有长鼻子）', 'has', ['have', 'is'], 'it 单数用 has', '句型', 4),
  ('How ___ you?（你好吗）', 'are', ['am', 'is'], 'you 配 are', '句型', 4),
  ('「给你」递东西时说？', 'Here you are.', ['Here are you.', 'You are here.'], '固定说法 Here you are', '句型', 4),
  ('Is this a cat?（肯定回答）', 'Yes, it is.', ['Yes, I am.', 'No, it is.'], 'Is this...? 答 Yes, it is', '句型', 4),
  ('「它是什么颜色」问？', 'What colour is it?', ['What is colour?', 'How colour is it?'], '问颜色用 what colour', '句型', 4),
  # L5 综合挑战（形近词 + 语境 + 判断）
  ('cat 和 cap，哪个是「帽子」？', 'cap', ['cat', 'cup'], 'cap=帽子，cat=猫', '综合', 5),
  ('pen 和 pet，哪个是「宠物」？', 'pet', ['pen', 'pig'], 'pet=宠物，pen=钢笔', '综合', 5),
  ('哪个单词是「书」？', 'book', ['look', 'cook'], 'book=书', '综合', 5),
  ('哪个单词是「十」？', 'ten', ['pen', 'hen'], 'ten=十', '综合', 5),
  ('sad 的意思是「伤心」，bad 的意思是？', '坏的；不好的', ['伤心的', '高兴的'], 'bad=坏', '综合', 5),
  ('ball 的意思是？', '球', ['tall', 'small'], 'ball=球', '综合', 5),
  ('big 的反义词是？', 'small', ['tall', 'long'], 'big 小 反 small', '综合', 5),
  ('hot（热）的反义词是？', 'cold', ['big', 'long'], 'hot 反 cold', '综合', 5),
  ('口渴了要喝？', 'water', ['bread', 'rice'], '水=water', '综合', 5),
  ('「两本书」说？', 'two books', ['two book', 'book two'], '两本书 books 复数', '综合', 5),
  ('I have ___ orange.（一个橙子）', 'an', ['a', 'two'], '元音开头用 an', '综合', 5),
  ('「一只猫和两只狗」说？', 'one cat and two dogs', ['one cats and two dog', 'one cat and two dog'], '两只狗 dogs 复数', '综合', 5),
  ('早上见到老师问好，完整说？', 'Good morning, teacher!', ['Good night, teacher!', 'Goodbye, teacher!'], '早上问好用 morning', '综合', 5),
  ('打招呼说 Hello，对方回答？', 'Hello!', ['Good night!', 'Sorry!'], 'Hello 回 Hello', '综合', 5),
  ('判断：dog 和 cat 都是动物。', '正确', ['错误'], '狗和猫都是动物', '判断', 5),
  ('判断：one, two, three 都是数字。', '正确', ['错误'], '三个都是数字', '判断', 5),
  ('判断：apple 的意思是「香蕉」。', '错误', ['正确'], 'apple=苹果，banana 才是香蕉', '判断', 5),
  ('判断：I am a pupil. 意思是「我是一名小学生」。', '正确', ['错误'], 'pupil=小学生', '判断', 5),
  ('判断：Good night 是早上打招呼用语。', '错误', ['正确'], 'Good night 是晚安', '判断', 5),
  ('判断：blue 是「黄色」的意思。', '错误', ['正确'], 'blue=蓝色，yellow 才是黄色', '判断', 5),
 ],
 4: [
  # L1 判断
  ('判断：kitchen 的意思是「厨房」。', '正确', ['错误'], 'kitchen=厨房', '判断', 1),
  ('判断：library 是「图书馆」。', '正确', ['错误'], 'library=图书馆', '判断', 1),
  ('判断：museum 的意思是「医院」。', '错误', ['正确'], 'museum=博物馆，hospital 才是医院', '判断', 1),
  # L3 情景应答（沪教四上主题：住所/购物/季节/道路安全/祖辈与职业）
  ('店员问 Can I help you?，他在说什么？', '你要买什么', ['你叫什么名字', '几点了'], '购物场景：为您服务', '情景', 3),
  ('买东西问「多少钱」？', 'How much is it?', ['How many is it?', 'How old is it?'], '问价格用 how much', '情景', 3),
  ('询问别人住在哪里，问？', 'Where do you live?', ['What do you live?', 'Where are you live?'], '问地点用 where', '情景', 3),
  ('「我住在一栋高楼里」说？', 'I live in a tall building.', ['I live on a tall building.', 'I am live in a building.'], 'live in=住在', '情景', 3),
  ('别人说 Thank you so much!，你回答？', "You're welcome.", ["I'm sorry.", 'How are you?'], '不用谢 You are welcome', '情景', 3),
  ('向别人问路，先说？', 'Excuse me.', ['See you.', 'Good night.'], '打扰别人先说 Excuse me', '情景', 3),
  ('红灯亮了，你应该？', 'Stop and wait.', ['Run fast.', 'Keep walking.'], '红灯停', '情景', 3),
  ('绿灯亮了才能？', 'Cross the road.', ['Play on the road.', 'Stop.'], '绿灯行', '情景', 3),
  ('过马路要先？', 'Look left and right first.', ['Close your eyes.', 'Run quickly.'], '先看左右', '情景', 3),
  ('问「深圳秋天天气怎么样」？', 'How is the weather in autumn?', ['What season do you like?', 'How old are you?'], '问天气用 how is the weather', '情景', 3),
  ('「我最喜欢的季节是夏天」说？', 'My favourite season is summer.', ["My favourite season is winter.", "I don't like seasons."], 'favourite=最喜欢的', '情景', 3),
  ('问「那是你奶奶吗」？', 'Is that your grandma?', ['Is that my grandma?', 'Are that your grandma?'], 'that 配 is', '情景', 3),
  ('介绍职业「他是一个医生」？', 'He is a doctor.', ['He is doctor.', 'He are a doctor.'], '职业前加 a', '情景', 3),
  ('问「她是做什么工作的」？', 'What does she do?', ['What is she do?', 'What she does?'], '问职业 what does...do', '情景', 3),
  ('想买三个苹果，对店员说？', "I'd like three apples.", ["I'd like three apple.", "I'd like an apples."], '三个苹果加 s', '情景', 3),
  ('收银员说 Here you are.，是什么意思？', '给你', ['谢谢', '多少钱'], '递东西说 Here you are', '情景', 3),
  ('「Can I try it on?」是什么意思？', '我能试穿吗', ['我能买下吗', '我能退货吗'], 'try on=试穿', '情景', 3),
  ('植物需要什么才能生长？', 'Plants need water and sun.', ['Plants need candy.', 'Plants need toys.'], '植物需要水和阳光', '情景', 3),
  ('「熊住在哪里」怎么问？', 'Where do bears live?', ['What do bears live?', 'Where do bears live on?'], '问地点用 where', '情景', 3),
  ('别人祝你 Happy New Year!，你回答？', 'The same to you!', ['You are happy.', 'Happy birthday!'], '同祝用 the same to you', '情景', 3),
  # L4 句型运用（there be / 三单 / how many-much / 进行时）
  ('There ___ a book on the desk.', 'is', ['are', 'am'], '单数配 is', '句型', 4),
  ('There ___ two cats under the bed.', 'are', ['is', 'be'], '复数配 are', '句型', 4),
  ('He ___ to school by bus.', 'goes', ['go', 'going'], '三单加 es', '句型', 4),
  ('She ___ like fish.', "doesn't", ["don't", "isn't"], '三单否定用 doesn\'t', '句型', 4),
  ('___ there any milk in the glass?（杯里有牛奶吗）', 'Is', ['Are', 'Do'], 'milk 不可数配 is', '句型', 4),
  ('How ___ students are there in your class?', 'many', ['much', 'old'], '可数用 how many', '句型', 4),
  ('How ___ is the T-shirt?', 'much', ['many', 'old'], '问价格用 how much', '句型', 4),
  ('The cat is ___ the chair.（在椅子下面）', 'under', ['on', 'in'], '下面=under', '句型', 4),
  ('I can ___ very fast.（跑得快）', 'run', ['runs', 'running'], 'can+动词原形', '句型', 4),
  ('My grandma ___ TV every evening.', 'watches', ['watch', 'watchs'], '三单加 es', '句型', 4),
  ('___ you like pandas?（一般疑问句）', 'Do', ['Does', 'Are'], 'you 配 do', '句型', 4),
  ('Where ___ your parents live?', 'do', ['does', 'is'], 'parents 复数配 do', '句型', 4),
  ('Look! The children ___ playing football.', 'are', ['is', 'am'], 'children 复数配 are', '句型', 4),
  ("It's cold. ___ the window, please.（关上窗户）", 'Close', ['Open', 'Closing'], '关=close', '句型', 4),
  ('I have ___ uncle.（一个叔叔）', 'an', ['a', 'two'], 'uncle 元音开头用 an', '句型', 4),
  ('We ___ have school on Sunday.（星期天不上学）', "don't", ["doesn't", "aren't"], 'we 配 don\'t', '句型', 4),
  ('「她正在读书」说？', 'She is reading a book.', ['She read a book.', 'She is read a book.'], '正在做=be+doing', '句型', 4),
  ('选择疑问词：___ do you go to school? — By bus.', 'How', ['Where', 'What'], '问方式用 how', '句型', 4),
  ('___ is your father? — He is a driver.（问职业）', 'What', ['How', 'Who'], '问职业用 what', '句型', 4),
  ('The duck can ___.（游泳）', 'swim', ['swims', 'swimming'], 'can+动词原形', '句型', 4),
  # L5 综合挑战（形近/易混词 + 语境 + 判断）
  ('there 和 their，哪个表示「他们的」？', 'their', ['there', 'they'], 'their=他们的', '综合', 5),
  ('wear 和 where，哪个是「穿；戴」？', 'wear', ['where', 'were'], 'wear=穿', '综合', 5),
  ('quiet 和 quite，哪个是「安静的」？', 'quiet', ['quite', 'quick'], 'quiet=安静', '综合', 5),
  ('「看电影」哪个搭配对？', 'see a film', ['read a film', 'look a film'], '看电影用 see', '综合', 5),
  ('how much 问什么？', '价格或不可数的量', ['只能问数量', '只能问价格'], 'how much 价格/不可数', '综合', 5),
  ('I want to ___ TV.（看电视）', 'watch', ['see', 'look'], '看电视用 watch', '综合', 5),
  ('hospital 和 museum，哪个是「博物馆」？', 'museum', ['hospital', 'hotel'], 'museum=博物馆', '综合', 5),
  ('grandpa 和 grandma，哪个是「爷爷」？', 'grandpa', ['grandma', 'grandson'], 'grandpa=爷爷', '综合', 5),
  ('想给妈妈买礼物，对店员说？', 'I want to buy a gift for my mum.', ['I want buy a gift.', 'I want to buying a gift.'], 'want to+动词原形', '综合', 5),
  ('妈妈问 Where is your schoolbag?，她在问？', '你的书包在哪里', ['书包是什么颜色', '书包是谁的'], 'where 问地点', '综合', 5),
  ('The leaves turn ___ in autumn.（树叶变黄）', 'yellow', ['blue', 'red'], '秋天树叶变黄', '综合', 5),
  ('夏天很热，妈妈说 Let\'s go ___.（游泳）', 'swimming', ['swim', 'swims'], 'go swimming 固定搭配', '综合', 5),
  ('植树节「种树」用英语说？', 'plant trees', ['plants tree', 'tree plant'], '种树 plant trees', '综合', 5),
  ('在图书馆里应该？', 'Keep quiet.', ['Shout loudly.', 'Run around.'], '图书馆要保持安静', '综合', 5),
  ('判断：season 的意思是「季节」。', '正确', ['错误'], 'season=季节', '判断', 5),
  ('判断：How many 用来问不可数名词的数量。', '错误', ['正确'], 'how many 问可数，how much 问不可数', '判断', 5),
  ('判断：crosswalk（斑马线）是过马路的安全地方。', '正确', ['错误'], '走斑马线安全', '判断', 5),
  ('判断：farmer 的意思是「农场」。', '错误', ['正确'], 'farmer=农民，farm 才是农场', '判断', 5),
  ('判断：Turn left 是「向右转」。', '错误', ['正确'], 'turn left=左转', '判断', 5),
  ('判断：植物生长需要阳光和水。', '正确', ['错误'], '阳光和水缺一不可', '判断', 5),
 ],
}

def main():
    bank = json.load(open(PATH, encoding='utf-8'))
    bank = [q for q in bank if not str(q['id']).startswith('ex')]   # 幂等：清旧 ex
    # ① g1/g4 重分层：词义题→L1，拼写题→L2（id 不变，wrongPool 不失效）；2/3/5/6 不动
    relevel = 0
    for q in bank:
        if q['grade'] in (1, 4):
            new_lv = 1 if q['q'].endswith('是什么意思？') else 2
            if q['level'] != new_lv:
                q['level'] = new_lv; relevel += 1
    # ② 回填纪律字段（全库，题面不动）
    for q in bank:
        q.setdefault('dif', q['level'])
        q.setdefault('tp', '词义' if q['q'].endswith('是什么意思？') else '拼写')
        q.setdefault('src', '沪教深圳·公共词表')
    # ③ 追加新题
    added = 0
    for g, rows in ADD.items():
        for i, (q, a, wrongs, why, tp, lv) in enumerate(rows):
            bank.append({
                'q': q, 'a': str(a), 'options': [str(w) for w in wrongs],
                'wrongReasons': [why, 'Read the question again and think!'],
                'grade': g, 'level': lv, 'dif': lv, 'tp': tp,
                'tag': '英语单词·综合', 'src': '通用语基',
                'speak': q.replace('（　）', '').replace('？', '').replace('___', ' what '),
                'id': 'ex%d-%03d' % (g, i)
            })
            added += 1
    # —— 自检（出题纪律）——
    for q in bank:
        opts = [str(o) for o in q['options']]
        assert str(q['a']) not in opts, '答案与干扰项冲突：%s' % q['id']
        assert len(set(opts)) == len(opts), '干扰项重复：%s' % q['id']
        assert len(opts) in (1, 2), '选项数异常：%s' % q['id']
        assert all(k in q for k in ('dif', 'tp', 'src')), '缺纪律字段：%s' % q['id']
        if q['tp'] == '判断':
            assert len(opts) == 1 and q['a'] in ('正确', '错误'), q['id']
    for g in (1, 4):
        for lv in range(1, 6):
            n = sum(1 for q in bank if q['grade'] == g and q['level'] == lv)
            assert n >= 20, 'g%d L%d 只有 %d 题（<20）' % (g, lv, n)
    with open(PATH, 'w', encoding='utf-8') as f:
        json.dump(bank, f, ensure_ascii=False, indent=1)
    print('英语单词全库 %d 题（重分层 %d，新增 %d）' % (len(bank), relevel, added))
    for g in (1, 4):
        cnt = [sum(1 for q in bank if q['grade'] == g and q['level'] == lv) for lv in range(1, 7)]
        print('  g%d 各层 %s' % (g, cnt))

if __name__ == '__main__':
    main()
