# -*- coding: utf-8 -*-
"""gen_english_units.py — 沪教版英语 1~6 年级上册单元题库（v3.9 / v3.11）
题源：沪教版义务教育教科书·英语（深圳用书）
  一上 / 二上（沪教牛津深圳版 12 单元·v3.11 增补，深圳为英语一年级起始地区）
  三上 2024 秋版 / 四上 2025 秋版 / 五上 2026 秋版（各 8 单元）
  六上 2026 秋版（6 单元）
题目类型：单元主题理解（英文标题）、核心功能句型、主题词汇归类、情景应答
版权规则：只出事实性/通用课程内容（单元标题、功能句型、常用词汇），不引用课文原文
产出：data/banks/english-units.json（q.unit = '第X单元 主题'，q.grade = 1~6，level 0）
"""

UNITS = {
1: [
  ('第一单元 打招呼', [
    ('早上见到老师，打招呼说？', 'Good morning!', ['Good night!', 'Goodbye!'], '早上用 Good morning 问好'),
    ('hello 的意思是？', '你好', ['再见', '谢谢'], 'hello = 你好'),
    ('和别人分开时说？', 'Goodbye!', ['Hello!', 'Good morning!'], '分开时说再见'),
    ('Good afternoon 是什么时候问好？', '下午', ['早上', '晚上'], 'afternoon = 下午'),
  ]),
  ('第二单元 同学与文具', [
    ('「书」的英文是？', 'book', ['ruler', 'pencil'], 'book 书，ruler 尺子'),
    ('rubber 是什么文具？', '橡皮', ['铅笔', '书'], 'rubber = 橡皮'),
    ('ruler 的意思是？', '尺子', ['橡皮', '铅笔'], 'ruler = 尺子'),
    ('得到帮助时说？', 'Thank you.', ['Hello.', 'Goodbye.'], '感谢别人说 Thank you'),
  ]),
  ('第三单元 我的五官', [
    ('Touch your nose. 是让你做什么？', '摸摸你的鼻子', ['摸摸你的耳朵', '看看你的眼睛'], 'nose 鼻子，ear 耳朵'),
    ('eye 是？', '眼睛', ['嘴巴', '鼻子'], 'eye 眼睛，mouth 嘴巴，nose 鼻子'),
    ('「这是我的脸。」说？', 'This is my face.', ['This is your face.', 'This is my nose.'], 'my 我的 + face 脸'),
    ('ear 的意思是？', '耳朵', ['眼睛', '头发'], 'ear = 耳朵'),
  ]),
  ('第四单元 我会做', [
    ('「我会唱歌。」用英语说？', 'I can sing.', ['I can dance.', 'I am sing.'], 'can + 动词 表示会做'),
    ('draw 是做什么？', '画画', ['读书', '跳舞'], 'draw = 画画'),
    ('dance 是？', '跳舞', ['唱歌', '读书'], 'dance 跳舞，sing 唱歌，read 读书'),
    ('can 的意思是？', '能；会', ['想；要', '喜欢'], 'can 表示会做某事'),
  ]),
  ('第五单元 我的家人', [
    ('介绍「这是我妈妈」说？', 'This is my mother.', ['This is my father.', 'I am mother.'], 'mother 妈妈，father 爸爸'),
    ('grandmother 是？', '奶奶（外婆）', ['爷爷（外公）', '哥哥'], 'grandmother 是祖辈女性'),
    ('father 的意思是？', '爸爸', ['妈妈', '姐姐'], 'father = 爸爸'),
    ('he 和 she 的区别是？', 'he 是他，she 是她', ['he 是她，she 是他', '两个都是它'], 'he 指男生，she 指女生'),
  ]),
  ('第六单元 我的朋友', [
    ('friend 的意思是？', '朋友', ['同学', '老师'], 'friend = 朋友'),
    ('tall 的反义词是？', 'short', ['fat', 'thin'], 'tall 高 ↔ short 矮'),
    ('fat 是？', '胖的', ['瘦的', '高的'], 'fat 胖 ↔ thin 瘦'),
    ('classmate 是？', '同学', ['朋友', '家人'], 'class 同班 + mate 伙伴'),
  ]),
  ('第七单元 数一数', [
    ('how many 是问什么？', '多少', ['多高', '多远'], 'how many 问数量'),
    ('「三」的英文是？', 'three', ['two', 'four'], 'three 三，two 二，four 四'),
    ('one, two, ____, four，缺的数是？', 'three', ['five', 'six'], '数数顺序 1 2 3 4'),
    ('five 是数字几？', '5', ['4', '6'], 'five = 5'),
  ]),
  ('第八单元 买水果', [
    ('apple 是？', '苹果', ['梨', '桃子'], 'apple 苹果，pear 梨，peach 桃子'),
    ('买水果时「请给我苹果。」说？', 'Apples, please.', ['Pears, please.', 'Apples, goodbye.'], '名词 + please 礼貌请求'),
    ('peach 的意思是？', '桃子', ['桔子', '苹果'], 'peach = 桃子'),
    ('supermarket 是？', '超市', ['学校', '公园'], 'supermarket = 超市'),
  ]),
  ('第九单元 买食物', [
    ('想吃蛋糕时说？', 'May I have a cake?', ['May I have a pie?', 'I am cake.'], 'May I have...? 请求得到某物'),
    ('hamburger 是？', '汉堡包', ['比萨饼', '蛋糕'], 'hamburger 汉堡，pizza 比萨'),
    ('pizza 的意思是？', '比萨饼', ['汉堡包', '点心'], 'pizza = 比萨饼'),
    ('snack 是？', '点心', ['尺子', '橡皮'], 'snack = 小吃点心'),
  ]),
  ('第十单元 农场动物', [
    ('cow 是？', '奶牛', ['鸭子', '小鸡'], 'cow 奶牛，duck 鸭子，chick 小鸡'),
    ('pig 的意思是？', '猪', ['牛', '鸡'], 'pig = 猪'),
    ('chick 是？', '小鸡', ['鸭子', '猪'], 'chick = 小鸡'),
    ('duck 是？', '鸭子', ['奶牛', '小鸡'], 'duck = 鸭子'),
  ]),
  ('第十一单元 动物园', [
    ('monkey 是？', '猴子', ['熊猫', '老虎'], 'monkey 猴子，panda 熊猫，tiger 老虎'),
    ('panda 的意思是？', '熊猫', ['熊', '老虎'], 'panda 是我们的国宝'),
    ('tiger 是？', '老虎', ['熊', '猴子'], 'tiger = 老虎'),
    ('bear 的意思是？', '熊', ['熊猫', '老虎'], 'bear = 熊'),
  ]),
  ('第十二单元 公园与颜色', [
    ('red 是？', '红色', ['蓝色', '绿色'], 'red 红，blue 蓝，green 绿'),
    ('yellow 的意思是？', '黄色', ['红色', '蓝色'], 'yellow = 黄色'),
    ('blue 是？', '蓝色', ['绿色', '黄色'], 'blue = 蓝色'),
    ('big 的反义词是？', 'small', ['tall', 'long'], 'big 大 ↔ small 小'),
  ]),
],
2: [
  ('第一单元 日常问候', [
    ('晚上见面问好说？', 'Good evening!', ['Good morning!', 'Good night!'], 'evening = 晚上'),
    ('睡觉前说？', 'Good night!', ['Good afternoon!', 'Good morning!'], '睡前固定用语 Good night'),
    ('today 的意思是？', '今天', ['明天', '昨天'], 'today = 今天'),
    ('回答 How are you? 可以说？', 'Very well, thank you.', ['How are you?', 'Good night.'], 'very well = 很好'),
  ]),
  ('第二单元 自我介绍', [
    ('介绍自己名字说？', "I'm Danny.", ['You are Danny.', 'He is Danny.'], "I'm = I am 我是"),
    ('boy 是？', '男孩', ['女孩', '妈妈'], 'boy 男孩，girl 女孩'),
    ('name 的意思是？', '名字', ['年龄', '班级'], 'name = 名字'),
    ('big 的反义词是？', 'small', ['long', 'tall'], 'big 大 ↔ small 小'),
  ]),
  ('第三单元 你是谁', [
    ('Are you Alice? 肯定回答是？', 'Yes, I am.', ['Yes, I is.', 'No, I am.'], 'Are you...? 用 Yes, I am 回答'),
    ('seven 是数字几？', '7', ['8', '9'], 'seven 7，eight 8，nine 9，ten 10'),
    ('ten 的意思是？', '十', ['九', '八'], 'ten = 10'),
    ('做错事时说？', 'Sorry.', ['Thank you.', 'Hello.'], '道歉说 Sorry'),
  ]),
  ('第四单元 我会运动', [
    ('「你会游泳吗？」怎么问？', 'Can you swim?', ['Are you swim?', 'You can swim?'], 'Can you + 动词'),
    ('run 是？', '跑', ['飞', '写'], 'run 跑，fly 飞，write 写'),
    ('ride a bicycle 是？', '骑自行车', ['开小汽车', '滑滑梯'], 'bicycle 自行车'),
    ("can't 的意思是？", '不能；不会', ['能；会', '想要'], "can't = cannot"),
  ]),
  ('第五单元 我的家庭', [
    ("That's my family. 是什么意思？", '那是我的家庭', ['这是我的朋友', '那是我的学校'], "That's = That is"),
    ('brother 是？', '弟弟；兄弟', ['姐姐；妹妹', '妈妈'], 'brother 兄弟，sister 姐妹'),
    ('sister 的意思是？', '姐姐；妹妹', ['弟弟', '爸爸'], 'sister = 姐妹'),
    ('young 的反义词是？', 'old', ['small', 'short'], 'young 年轻 ↔ old 年老'),
  ]),
  ('第六单元 外貌特征', [
    ('「我的头发长。」说？', 'My hair is long.', ['My hair is short.', 'My head is long.'], 'hair 头发，long 长'),
    ('hair 是？', '头发', ['头', '手'], 'hair 头发，head 头'),
    ('head 的意思是？', '头', ['头发', '脸'], 'head = 头'),
    ('long 的反义词是？', 'short', ['big', 'old'], 'long 长 ↔ short 短'),
  ]),
  ('第七单元 游乐场', [
    ('slide 是？', '滑梯', ['秋千', '跷跷板'], 'slide 滑梯，swing 秋千，seesaw 跷跷板'),
    ('swing 的意思是？', '秋千', ['滑梯', '操场'], 'swing = 秋千'),
    ('seesaw 是？', '跷跷板', ['秋千', '滑梯'], 'seesaw = 跷跷板'),
    ('playground 是？', '操场', ['房间', '大街'], 'play 玩 + ground 场地'),
  ]),
  ('第八单元 我的房间', [
    ('Put the book in the bag. 是让你做什么？', '把书放进书包里', ['把书放在椅子上', '把书扔掉'], 'put 放，in 里面'),
    ('chair 是？', '椅子', ['书桌', '床'], 'chair 椅子，desk 书桌'),
    ('desk 的意思是？', '书桌', ['椅子', '箱子'], 'desk = 书桌'),
    ('pencil case 是？', '铅笔盒', ['书包', '书桌'], 'pencil 铅笔 + case 盒'),
  ]),
  ('第九单元 晚餐', [
    ('Dinner is ready. 是什么意思？', '晚饭准备好了', ['该睡觉了', '该上学了'], 'dinner 晚饭，ready 准备好'),
    ('chopsticks 是？', '筷子', ['勺子', '碗'], 'chopsticks 常用复数'),
    ('bowl 的意思是？', '碗', ['盘子', '勺子'], 'bowl = 碗'),
    ('spoon 是？', '勺子', ['筷子', '盘子'], 'spoon = 勺子'),
  ]),
  ('第十单元 天空', [
    ('sky 是？', '天空', ['大海', '森林'], 'sky = 天空'),
    ('moon 的意思是？', '月亮', ['太阳', '星星'], 'moon 月亮，sun 太阳，star 星星'),
    ('sun 是？', '太阳', ['月亮', '天空'], 'sun = 太阳'),
    ('star 的意思是？', '星星', ['月亮', '太阳'], 'star = 星星'),
  ]),
  ('第十一单元 森林动物', [
    ('forest 是？', '森林', ['大街', '操场'], 'forest = 森林'),
    ('fox 是？', '狐狸', ['河马', '天鹅'], 'fox 狐狸，hippo 河马'),
    ('hippo 的意思是？', '河马', ['狐狸', '鸽子'], 'hippo = 河马'),
    ('swan 是？', '天鹅', ['鸽子', '鸭子'], 'swan 天鹅，dove 鸽子'),
  ]),
  ('第十二单元 爱护花草', [
    ("Don't pick the flowers. 是什么意思？", '不要摘花', ['不要种树', '快去摘花'], "don't + 动词 表示不要做"),
    ('flower 是？', '花', ['树', '草'], 'flower 花，tree 树，grass 草'),
    ('climb the tree 是？', '爬树', ['砍树', '种树'], 'climb = 爬'),
    ('beautiful 的意思是？', '美丽的', ['可爱的', '野生的'], 'beautiful = 美丽'),
  ]),
],
3: [
  ('第一单元 感受与情绪', [
    ('happy 的意思是？', '开心的', ['伤心的', '生气的'], 'How do we feel? 单元学表达感受'),
    ('How do we feel? 在问什么？', '我们的感受', ['我们的名字', '天气怎么样'], '这个单元的主题是感受'),
    ('「我很开心」用英语说？', "I'm happy.", ["I'm sad.", "I'm tired."], 'I am + 形容词表达感受'),
    ('tired 是什么感觉？', '累的', ['饿的', '兴奋的'], 'tired = 累'),
    ('别人问你 How are you? 可以回答？', "I'm fine, thank you.", ['How are you?', 'Good night.'], '问候语的固定回答'),
  ]),
  ('第二单元 家庭', [
    ('family 的意思是？', '家庭；家人', ['学校', '公园'], 'What\'s interesting about families? 单元主题是家庭'),
    ('介绍「这是我妈妈」说？', 'This is my mother.', ['This is my teacher.', 'I am mother.'], 'This is + 人物 介绍家人'),
    ('father 和 mother 分别是？', '爸爸和妈妈', ['妈妈和爸爸', '哥哥和姐姐'], 'father=爸爸，mother=妈妈'),
    ('brother 是指？', '兄弟', ['姐妹', '父母'], 'sister 才是姐妹'),
    ('How many people are in your family? 在问？', '你家有几口人', ['你几岁了', '你叫什么名字'], 'How many 问数量'),
  ]),
  ('第三单元 外貌', [
    ('tall 的反义词是？', 'short', ['long', 'big'], 'tall 高 ↔ short 矮'),
    ('描述「他个子高」说？', 'He is tall.', ['He is short.', 'He is long.'], '人物高矮用 tall/short'),
    ('long hair 是？', '长头发', ['短头发', '大眼睛'], 'long 长 + hair 头发'),
    ('What do you look like? 在问？', '你长什么样子', ['你喜欢什么', '你住在哪里'], 'look like 问外貌'),
    ('big eyes 是？', '大眼睛', ['小眼睛', '长头发'], 'big 大 + eyes 眼睛'),
  ]),
  ('第四单元 玩乐', [
    ('play 的意思是？', '玩', ['吃', '睡'], 'How do we have fun? 单元学玩乐活动'),
    ('「唱歌」用英语说？', 'sing', ['dance', 'draw'], 'sing 唱歌，dance 跳舞'),
    ('dance 是？', '跳舞', ['唱歌', '画画'], 'dance = 跳舞'),
    ('提议一起玩说？', "Let's play!", ["Let's eat.", "Let's go to bed."], "Let's + 动词 提议做某事"),
    ('swim 是？', '游泳', ['跑步', '跳绳'], 'swim 游泳，run 跑步'),
  ]),
  ('第五单元 食物', [
    ('rice 的意思是？', '米饭', ['面条', '面包'], 'What do we eat? 单元学食物'),
    ('noodles 是？', '面条', ['米饭', '鸡蛋'], 'noodles 常用复数形式'),
    ('问对方喜欢吃什么说？', 'What do you like eating?', ["What's your name?", 'How old are you?'], 'like eating 问喜欢吃什么'),
    ('fruit 是？', '水果', ['蔬菜', '肉'], 'vegetable 才是蔬菜'),
    ('「我喜欢苹果」说？', 'I like apples.', ['I am apple.', 'You like apples.'], 'like 后用名词复数'),
  ]),
  ('第六单元 小动物', [
    ('rabbit 是？', '兔子', ['猫', '狗'], 'What do we like about small animals? 单元学小动物'),
    ('问「你喜欢猫吗」说？', 'Do you like cats?', ['Are you cat?', 'You like cat.'], 'Do you like + 复数'),
    ('喜欢时回答？', 'Yes, I do.', ['Yes, it is.', 'No, I do.'], 'Do you...? 用 do 回答'),
    ('「小鸟」的英文是？', 'bird', ['fish', 'duck'], 'bird 鸟，fish 鱼'),
    ('small 的反义词是？', 'big', ['long', 'tall'], 'small 小 ↔ big 大'),
  ]),
  ('第七单元 天气', [
    ('sunny 的意思是？', '晴朗的', ['下雨的', '有风的'], 'What do we know about weather? 单元学天气'),
    ('问天气说？', "How's the weather?", ['How are you?', "What's this?"], '问天气的固定句型'),
    ('rainy 是？', '下雨的', ['下雪的', '晴朗的'], 'rain 雨 → rainy 下雨的'),
    ('snowy 是？', '下雪的', ['炎热的', '刮风的'], 'snow 雪 → snowy 下雪的'),
    ('windy 是？', '有风的', ['多云的', '潮湿的'], 'wind 风 → windy 有风的'),
  ]),
  ('第八单元 生日', [
    ('「生日快乐」说？', 'Happy birthday!', ['Happy New Year!', 'Good morning.'], 'Why do we like birthdays? 单元学生日'),
    ('present 是？', '礼物', ['蛋糕', '蜡烛'], 'present = 礼物'),
    ('candle 是？', '蜡烛', ['气球', '礼物'], '生日蛋糕上插蜡烛'),
    ('party 是？', '聚会', ['作业', '礼物'], '生日 party = 生日聚会'),
    ('「你几岁了？」用英语问？', 'How old are you?', ['How are you?', "What's your name?"], 'How old 问年龄'),
  ]),
],
4: [
  ('第一单元 住所', [
    ('Unit 1 标题 Where do people live? 在问什么？', '人们住在哪里', ['人们吃什么', '人们做什么工作'], '单元主题：住所'),
    ('live 的意思是？', '居住', ['吃', '玩'], 'live in + 地点 表示住在某地'),
    ('问对方住在哪里说？', 'Where do you live?', ['What do you live?', 'Where are you go?'], 'Where + do you + 动词'),
    ('回答「我住在深圳」说？', 'I live in Shenzhen.', ['I am Shenzhen.', 'I live Shenzhen.'], 'live in + 城市'),
    ('city 的意思是？', '城市', ['村庄', '农场'], 'city 城市，village 村庄'),
  ]),
  ('第二单元 动物栖息地', [
    ('Where do animals live? 在问什么？', '动物住在哪里', ['动物吃什么', '动物会飞吗'], '单元主题：动物的家园'),
    ('forest 是？', '森林', ['沙漠', '海洋'], '很多动物住在 forest'),
    ('鱼（fish）生活在哪里？', '在水里（河流和大海）', ['在树上', '在农场'], '鱼生活在水里'),
    ('monkey、tiger、elephant 属于哪一类？', '动物', ['植物', '职业'], '它们都是动物'),
    ('mountain 是？', '山', ['河流', '街道'], 'mountain 山，river 河'),
  ]),
  ('第三单元 数字', [
    ('How do we use numbers? 在问什么？', '我们怎样使用数字', ['现在几点了', '数字什么颜色'], '单元主题：数字的用处'),
    ('one hundred 是多少？', '100', ['1000', '10'], 'hundred 百，thousand 千'),
    ('one thousand 是多少？', '1000', ['100', '10000'], 'thousand = 千'),
    ('zero 是？', '零', ['一', '十'], 'zero = 0'),
    ('电话号码 110 读作？', 'one one zero', ['eleven zero', 'one ten'], '电话号码逐位读数字'),
  ]),
  ('第四单元 购物', [
    ('What do we buy? 在问什么？', '我们买什么', ['我们卖几件', '我们吃什么'], '单元主题：购物'),
    ('问价格说？', 'How much is it?', ['How many is it?', 'What time is it?'], '问价钱用 How much'),
    ('expensive 的意思是？', '昂贵的', ['便宜的', '免费的'], 'expensive 贵 ↔ cheap 便宜'),
    ('付钱时说？', "Here's the money.", ["Here's the food.", 'Give you money.'], '递钱的常用语'),
    ('shop 的意思是？', '商店', ['学校', '医院'], 'shop 商店，买东西的地方'),
  ]),
  ('第五单元 季节', [
    ('How are the seasons different? 在问什么？', '四季有什么不同', ['一年有几季', '哪个季节下雨'], '单元主题：四季的特点'),
    ('spring 是？', '春天', ['夏天', '秋天'], 'spring 春，summer 夏'),
    ('「冬天」的英文是？', 'winter', ['autumn', 'summer'], 'autumn 是秋天'),
    ('warm 是？', '温暖的', ['凉爽的', '炎热的'], 'warm 暖 ↔ cool 凉'),
    ('一年有几个季节？', '四个（four）', ['两个（two）', '三个（three）'], '春夏秋冬共四季'),
  ]),
  ('第六单元 植物', [
    ("What's amazing about plants? 在问什么？", '植物有什么神奇之处', ['植物卖多少钱', '植物几点开花'], '单元主题：神奇的植物'),
    ('leaf 的意思是？', '叶子', ['花', '根'], 'leaf 叶，flower 花'),
    ('seed 是？', '种子', ['果实', '叶子'], 'seed 种子能长成植物'),
    ('植物生长需要什么？', '阳光和水', ['糖和盐', '衣服和鞋'], 'sun and water 让植物 grow'),
    ('grow 的意思是？', '生长', ['缩小', '睡觉'], '植物会慢慢 grow'),
  ]),
  ('第七单元 道路安全', [
    ('How do we keep safe on the road? 在问什么？', '我们怎样在路上保证安全', ['我们怎样跑得快', '我们怎样骑车'], '单元主题：道路安全'),
    ('红灯亮了应该？', '停（Stop）', ['走（Go）', '跑（Run）'], '红灯停、绿灯行'),
    ('过马路应该走哪里？', '斑马线', ['马路中间', '草地'], '走斑马线才 safe'),
    ('careful 的意思是？', '小心的', ['粗心的', '快乐的'], 'Be careful! = 小心！'),
    ('traffic 是？', '交通', ['天气', '食物'], 'traffic light = 红绿灯'),
  ]),
  ('第八单元 祖辈与职业', [
    ('What do our grandparents do? 在问什么？', '我们的祖辈做什么（工作）', ['祖辈多大年纪', '祖辈住几楼'], '单元主题：祖辈的生活与职业'),
    ('grandfather 是？', '爷爷；外公', ['奶奶；外婆', '叔叔'], 'grandmother 是奶奶/外婆'),
    ('doctor 是？', '医生', ['司机', '厨师'], 'doctor 医生，在医院工作'),
    ('cook 表示职业时是？', '厨师', ['司机', '教师'], 'cook 名词 = 厨师'),
    ('driver 是？', '司机', ['医生', '厨师'], 'drive 开车 → driver 司机'),
  ]),
],
5: [
  ('第一单元 周末活动', [
    ('What do we do at the weekend? 在问什么？', '我们周末做什么', ['我们几点起床', '我们周末吃几顿'], '单元主题：周末活动'),
    ('weekend 是？', '周末', ['星期三', '生日'], 'Saturday + Sunday = weekend'),
    ('often 的意思是？', '经常', ['从不', '明天'], 'often 表示频率'),
    ('「我周末常踢足球」说？', 'I often play football at the weekend.', ['I am football weekend.', 'I often football play.'], 'often + 动词原形'),
    ('Saturday 和 Sunday 是？', '星期六和星期日', ['星期一和星期二', '星期五和星期六'], '周末两天'),
  ]),
  ('第二单元 保持健康', [
    ('How do we stay healthy? 在问什么？', '我们怎样保持健康', ['我们怎样变高', '我们怎样吃饭'], '单元主题：健康生活'),
    ('healthy 是？', '健康的', ['生病的', '疲倦的'], 'stay healthy = 保持健康'),
    ('exercise 的意思是？', '锻炼；运动', ['睡觉', '做作业'], '锻炼让身体 healthy'),
    ('多吃蔬菜水果会让我们？', '更健康', ['生病', '变懒'], '蔬菜水果有营养'),
    ('早睡早起是好习惯吗？', '是', ['不是', '只有周末是'], 'good habit 好习惯'),
  ]),
  ('第三单元 不同的国家', [
    ('What do you know about different countries? 在问什么？', '你对不同的国家了解什么', ['你去过几个国家', '国家有多少人口'], '单元主题：认识国家'),
    ('country 的复数是？', 'countries', ['countryes', 'country'], 'y 结尾变 ies'),
    ('China 是？', '中国', ['日本', '美国'], '我们住在 China'),
    ('different 的意思是？', '不同的', ['相同的', '便宜的'], 'different 不同的，same 相同的'),
    ('说汉语的国家人被称为？', 'Chinese', ['English', 'French'], 'China → Chinese'),
  ]),
  ('第四单元 有趣的假日', [
    ("What's interesting about holidays? 在问什么？", '假日有什么有趣之处', ['假日放几天', '假日作业多不多'], '单元主题：假日生活'),
    ('holiday 是？', '假日', ['作业', '课程'], 'summer holiday 暑假'),
    ('travel 的意思是？', '旅行', ['睡觉', '游泳'], 'holiday 时常去 travel'),
    ('beach 是？', '海滩', ['厨房', '教室'], '夏天去 beach 玩水'),
    ('summer holiday 是？', '暑假', ['寒假', '春假'], 'winter holiday 才是寒假'),
  ]),
  ('第五单元 生物', [
    ('What are living things? 在问什么？', '什么是生物', ['东西多少钱', '东西多重'], '单元主题：认识生物'),
    ('living things 是？', '生物', ['家具', '石头'], '动物和植物都是生物'),
    ('植物和动物都属于？', 'living things（生物）', ['toys（玩具）', 'food（食物）'], '生物会生长'),
    ('石头（stone）是生物吗？', '不是', ['是', '以前是'], '石头不会生长，不是生物'),
    ('生物的共同特征是会？', '生长（grow）', ['发光', '唱歌'], '生长是生物的特征'),
  ]),
  ('第六单元 爱护地球', [
    ('Why should we take care of the Earth? 在问什么？', '为什么我们要爱护地球', ['地球有多大', '地球离太阳多远'], '单元主题：保护地球'),
    ('Earth 是？', '地球', ['月亮', '太阳'], 'the Earth 我们的家'),
    ('take care of 的意思是？', '照顾；爱护', ['破坏', '忘记'], 'take care of the Earth 爱护地球'),
    ('节约用水的英语是？', 'save water', ['waste water', 'buy water'], 'save 节约'),
    ('water 是？', '水', ['空气', '火'], '地球上的水很宝贵'),
  ]),
  ('第七单元 庆祝节日', [
    ('How do we celebrate festivals? 在问什么？', '我们怎样庆祝节日', ['节日几点吃饭', '节日穿什么鞋'], '单元主题：节日文化'),
    ('festival 是？', '节日', ['星期', '月份'], 'Spring Festival 春节'),
    ('Spring Festival 是？', '春节', ['中秋节', '圣诞节'], '中国最重要的传统节日'),
    ('celebrate 的意思是？', '庆祝', ['打扫', '睡觉'], 'celebrate the festival 庆祝节日'),
    ('Mid-Autumn Festival 我们吃？', '月饼（mooncakes）', ['饺子（dumplings）', '粽子（zongzi）'], '中秋节吃月饼'),
  ]),
  ('第八单元 音乐与感受', [
    ('How does music make us feel? 在问什么？', '音乐让我们产生什么感受', ['音乐多少钱一张', '音乐几点开始'], '单元主题：音乐与情绪'),
    ('music 是？', '音乐', ['美术', '数学'], 'music class 音乐课'),
    ('sing a song 是？', '唱一首歌', ['画一幅画', '读一本书'], 'song 歌曲'),
    ('piano 是？', '钢琴', ['小提琴', '鼓'], '弹钢琴 play the piano'),
    ('好听的音乐让人？', '开心放松', ['生病', '生气'], '音乐让生活更美好'),
  ]),
],
6: [
  ('第一单元 搬到新地方', [
    ('Why do people move to new places? 在问什么？', '人们为什么搬到新地方', ['人们怎样搬家', '新地方有多远'], '单元主题：搬迁与新生活'),
    ('move 的意思是？', '搬家；移动', ['唱歌', '付款'], 'move to + 地点 搬到某地'),
    ('new 的反义词是？', 'old', ['tall', 'long'], 'new 新 ↔ old 旧'),
    ('city 和 village 哪个通常更大？', 'city（城市）', ['village（村庄）', '一样大'], '城市比村庄大、更热闹'),
    ('move to a new school 是？', '转到新学校', ['离开学校', '修理学校'], '转学就是搬去新学校'),
  ]),
  ('第二单元 艺术创作', [
    ('Why do we make art? 在问什么？', '我们为什么进行艺术创作', ['艺术要花多少钱', '艺术课几点上'], '单元主题：艺术'),
    ('art 是？', '艺术；美术', ['体育', '科学'], 'art class 美术课'),
    ('「画画」用英语说？', 'draw', ['sing', 'swim'], 'draw 画画，sing 唱歌'),
    ('picture 是？', '图画', ['音乐', '运动'], 'draw a picture 画一幅画'),
    ('红色 的英文是？', 'red', ['blue', 'green'], '画画要用各种颜色'),
  ]),
  ('第三单元 保护自己', [
    ('How should we protect ourselves? 在问什么？', '我们应该怎样保护自己', ['我们应该跑多快', '我们几岁学游泳'], '单元主题：自我保护'),
    ('protect 的意思是？', '保护', ['破坏', '忘记'], 'protect ourselves 保护自己'),
    ('danger 是？', '危险', ['安全', '快乐'], 'danger 危险 ↔ safety 安全'),
    ('遇到危险应该？', '求助（call for help）', ['躲起来不出声', '自己解决不告诉任何人'], '找警察或大人帮忙'),
    ('safe 的反义词是？', 'dangerous', ['good', 'fast'], 'safe 安全 ↔ dangerous 危险'),
  ]),
  ('第四单元 物体的运动', [
    ('What makes things move? 在问什么？', '什么让物体运动', ['物体有多重', '物体什么颜色'], '单元主题：运动与力'),
    ('move 是？', '移动', ['停止', '睡觉'], '风能让树叶 move'),
    ('风（wind）能让什么动起来？', '风车和树叶', ['石头和山', '桌子和书'], '风吹动物体'),
    ('push 和 pull 分别是？', '推和拉', ['拉和推', '扔和接'], 'push 推 ↔ pull 拉'),
    ('ball（球）放在斜坡上会？', '滚动（roll）', ['融化', '生长'], '球会滚'),
  ]),
  ('第五单元 发明改变生活', [
    ('How do inventions change our lives? 在问什么？', '发明怎样改变我们的生活', ['发明值多少钱', '发明家几岁成名'], '单元主题：发明'),
    ('invention 是？', '发明', ['疾病', '假期'], 'invent 动词发明 → invention 名词'),
    ('电话和汽车都属于？', 'inventions（发明）', ['vegetables（蔬菜）', 'animals（动物）'], '它们改变了生活'),
    ('发明让我们的生活？', '更方便', ['更困难', '更危险'], '手机让联系更方便'),
    ('computer 是？', '电脑', ['电话', '电视'], '电脑是重要发明'),
  ]),
  ('第六单元 城市', [
    ('What is a city? 在问什么？', '什么是城市', ['城市多大年纪', '城市什么颜色'], '单元主题：认识城市'),
    ('城市里通常有什么？', '高楼、街道和公园', ['只有田地', '只有森林'], 'building 街道 park'),
    ('street 是？', '街道', ['天空', '海洋'], '城市里有很多 street'),
    ('和村庄相比，城市？', '更大更热闹', ['更小更安静', '没有房子'], '城市人多、建筑多'),
    ('building 是？', '建筑物', ['动物', '水果'], '高楼是 tall building'),
  ]),
],
}

def main():
    import json, os
    out = []
    for grade, units in UNITS.items():
        for uname, qs in units:
            for q, a, wrongs, why in qs:
                out.append({
                    'q': q, 'a': str(a), 'options': [str(w) for w in wrongs],
                    'wrongReasons': [why, '再想想这个单元的单词和句型'],
                    'grade': grade, 'level': 0, 'tag': '单元·' + uname.split(' ', 1)[1],
                    'unit': uname,
                    'speak': q.replace('？', '').replace('（　）', ''),
                    'id': 'eu%d-%02d' % (grade, len(out))
                })
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'banks', 'english-units.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print('生成', len(out), '道英语单元题')
    for g in sorted(UNITS):
        n = sum(len(qs) for u, qs in UNITS[g])
        print('  %d年级: %d 单元 / %d 题' % (g, len(UNITS[g]), n))

if __name__ == '__main__':
    main()
