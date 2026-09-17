# -*- coding: utf-8 -*-
"""gen_english_units.py — 沪教版英语 1~6 年级上册单元题库（v3.9 / v3.11 / v3.12）
题源：沪教版义务教育教科书·英语（深圳用书）
  一上 / 二上（2025 新教材《英语（口语交际）》各 6 单元·v3.12 对齐深圳现行课本）
  三上 2024 秋版 / 四上 2025 秋版 / 五上 2026 秋版（各 8 单元）
  六上 2026 秋版（6 单元）
题目类型：单元主题理解（英文标题）、核心功能句型、主题词汇归类、情景应答
版权规则：只出事实性/通用课程内容（单元标题、功能句型、常用词汇），不引用课文原文
产出：data/banks/english-units.json（q.unit = '第X单元 主题'，q.grade = 1~6，level 0）
"""

UNITS = {
1: [
  ('第一单元 家庭', [
    ('介绍家人「这是我妈妈。」说？', 'This is my mum.', ['This is your mum.', 'I am mum.'], 'This is my + 家人'),
    ('grandpa 是？', '爷爷；外公', ['奶奶；外婆', '兄；弟'], 'grandpa 是祖辈男性'),
    ('magic noodles 是？', '魔法面条', ['普通米饭', '魔法帽子'], 'magic 魔法 + noodles 面条'),
    ('brother 和 sister 的区别是？', 'brother 是兄弟，sister 是姐妹', ['两个都是姐妹', '两个都是兄弟'], 'brother 兄弟，sister 姐妹'),
    ('yarn 的意思是？', '毛线', ['面条', '魔法'], 'yarn = 毛线'),
  ]),
  ('第二单元 感觉', [
    ('「我饿了。」用英语说？', "I'm hungry.", ["I'm cold.", 'I hungry.'], 'I am + 形容词'),
    ('「口渴的」英文是？', 'thirsty', ['cold', 'hot'], 'thirsty = 口渴的'),
    ('hot 的意思是？', '热的', ['冷的', '渴的'], 'hot 热 ↔ cold 冷'),
    ('冷的时候可以说？', "I'm cold.", ["I'm hot.", "I'm thirsty."], 'cold = 冷的'),
  ]),
  ('第三单元 数字与文具', [
    ('「三」的英文是？', 'three', ['two', 'four'], 'three 3，two 2，four 4'),
    ('eraser 是什么文具？', '橡皮', ['铅笔', '直尺'], 'eraser = 橡皮'),
    ('one, two, ____, four，缺的数是？', 'three', ['five', 'six'], '数数顺序 1 2 3 4'),
    ('ruler 的意思是？', '直尺', ['铅笔盒', '橡皮'], 'ruler = 直尺'),
    ('pencil case 是？', '铅笔盒', ['书包', '玩具店'], 'pencil 铅笔 + case 盒'),
  ]),
  ('第四单元 动作', [
    ('「我会跳舞。」说？', 'I can dance.', ['I can draw.', 'I am dance.'], 'can + 动词原形'),
    ('read 是做什么？', '阅读；读', ['画画', '写字'], 'read 读，draw 画，write 写'),
    ('sing 的意思是？', '唱歌', ['跳舞', '画画'], 'sing 唱歌，dance 跳舞'),
    ('write 是？', '写；书写', ['阅读', '唱歌'], 'write = 写字'),
  ]),
  ('第五单元 宠物', [
    ('hamster 是？', '仓鼠', ['乌龟', '猫'], 'hamster 是圆圆的小宠物'),
    ('tortoise 的意思是？', '乌龟', ['鸟', '鱼'], 'tortoise = 乌龟'),
    ('dog 和 cat 分别是？', '狗和猫', ['猫和狗', '鸟和鱼'], 'dog 狗，cat 猫'),
    ('「鱼」的英文是？', 'fish', ['bird', 'cat'], 'fish 鱼，bird 鸟'),
  ]),
  ('第六单元 颜色', [
    ('red 是？', '红色', ['蓝色', '绿色'], 'red 红，blue 蓝，green 绿'),
    ('black 的意思是？', '黑色', ['白色', '黄色'], 'black 黑，white 白'),
    ('香蕉通常是？', 'yellow（黄色）', ['blue（蓝色）', 'black（黑色）'], '香蕉是黄色的'),
    ('小草是？', 'green（绿色）', ['red（红色）', 'white（白色）'], '小草是绿色的'),
  ]),
],
2: [
  ('第一单元 五感', [
    ('用眼睛看，英文是？', 'see', ['hear', 'smell'], 'see = 看见'),
    ('hear 的意思是？', '听见', ['闻到', '尝一尝'], 'hear = 听见'),
    ('「闻一闻」用英语说？', 'smell', ['taste', 'feel'], 'smell = 闻到'),
    ('taste 是？', '尝一尝', ['看一看', '听一听'], 'taste = 尝'),
    ('feel 的意思是？', '感觉到', ['看见', '听见'], 'feel = 感觉到'),
  ]),
  ('第二单元 亲属', [
    ('uncle 是？', '叔叔；舅舅', ['阿姨；姑姑', '堂（表）兄弟姐妹'], 'uncle 是长辈男性'),
    ('aunt 的意思是？', '阿姨；姑姑', ['叔叔；舅舅', '奶奶；外婆'], 'aunt 是长辈女性'),
    ('cousin 是？', '堂（表）兄弟姐妹', ['爸爸', '爷爷'], 'cousin 是同辈亲戚'),
    ('young 的反义词是？', 'old', ['cute', 'small'], 'young 年轻 ↔ old 年老'),
  ]),
  ('第三单元 玩具', [
    ('robot 是？', '机器人', ['洋娃娃', '拼图'], 'robot = 机器人'),
    ('jigsaw puzzle 的意思是？', '拼图', ['玩具飞机', '玩具熊'], 'puzzle = 拼图'),
    ('doll 是？', '洋娃娃', ['球', '机器人'], 'doll = 洋娃娃'),
    ('toy bear 是？', '玩具熊', ['玩具飞机', '玩具店'], 'toy 玩具 + bear 熊'),
  ]),
  ('第四单元 场所', [
    ('看电影去哪里？', 'cinema（电影院）', ['zoo（动物园）', 'park（公园）'], 'cinema = 电影院'),
    ('看动物去？', 'zoo（动物园）', ['fruit shop（水果店）', 'cinema（电影院）'], 'zoo = 动物园'),
    ('pet shop 是？', '宠物店', ['玩具店', '水果店'], 'pet 宠物 + shop 商店'),
    ('park 的意思是？', '公园', ['电影院', '宠物店'], 'park = 公园'),
  ]),
  ('第五单元 农场动物', [
    ('cow 是？', '奶牛', ['鸭子', '小鸡'], 'cow = 奶牛'),
    ('sheep 的意思是？', '羊', ['猪', '奶牛'], 'sheep = 羊'),
    ('chick 是？', '小鸡', ['鸡', '鸭子'], 'chick 小鸡，chicken 鸡'),
    ('pig 是？', '猪', ['奶牛', '羊'], 'pig = 猪'),
  ]),
  ('第六单元 节日', [
    ('中秋节我们吃？', 'mooncakes（月饼）', ['dumplings（饺子）', 'zongzi（粽子）'], '中秋吃月饼'),
    ('play with lanterns 是？', '玩灯笼', ['看月亮', '猜谜语'], 'lantern 灯笼'),
    ('solve riddles 的意思是？', '猜谜语', ['看月亮', '吃月饼'], 'riddle 谜语'),
    ('look at the moon 是？', '看月亮', ['玩灯笼', '猜谜语'], 'moon 月亮'),
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
