# -*- coding: utf-8 -*-
"""gen_poems.py — 古诗·背诵题库生成器
题源：primary-tutor-skill/knowledge-bases/chinese-primary-curriculum.md（必背古诗，公版）
题型：接下句 / 接上句 / 认作者 / 名句出处
产出：data/banks/poems.json（低/中/高学段映射到 1~6 年级）
"""
import json, os, re, random
random.seed(20260819)

# (题目, 作者, 学段1/2/3, 原文)
POEMS = [
    ('咏鹅', '骆宾王', 1, '鹅，鹅，鹅，曲项向天歌。白毛浮绿水，红掌拨清波。'),
    ('悯农（其二）', '李绅', 1, '锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。'),
    ('悯农（其一）', '李绅', 1, '春种一粒粟，秋收万颗子。四海无闲田，农夫犹饿死。'),
    ('江南', '汉乐府', 1, '江南可采莲，莲叶何田田。鱼戏莲叶间。'),
    ('画', '无名氏', 1, '远看山有色，近听水无声。春去花还在，人来鸟不惊。'),
    ('古朗月行（节选）', '李白', 1, '小时不识月，呼作白玉盘。又疑瑶台镜，飞在青云端。'),
    ('风', '李峤', 1, '解落三秋叶，能开二月花。过江千尺浪，入竹万竿斜。'),
    ('登鹳雀楼', '王之涣', 1, '白日依山尽，黄河入海流。欲穷千里目，更上一层楼。'),
    ('望庐山瀑布', '李白', 1, '日照香炉生紫烟，遥看瀑布挂前川。飞流直下三千尺，疑是银河落九天。'),
    ('江雪', '柳宗元', 1, '千山鸟飞绝，万径人踪灭。孤舟蓑笠翁，独钓寒江雪。'),
    ('敕勒歌', '北朝民歌', 1, '敕勒川，阴山下。天似穹庐，笼盖四野。天苍苍，野茫茫，风吹草低见牛羊。'),
    ('小儿垂钓', '胡令能', 1, '蓬头稚子学垂纶，侧坐莓苔草映身。路人借问遥招手，怕得鱼惊不应人。'),
    ('所见', '袁枚', 2, '牧童骑黄牛，歌声振林樾。意欲捕鸣蝉，忽然闭口立。'),
    ('山行', '杜牧', 2, '远上寒山石径斜，白云生处有人家。停车坐爱枫林晚，霜叶红于二月花。'),
    ('望天门山', '李白', 2, '天门中断楚江开，碧水东流至此回。两岸青山相对出，孤帆一片日边来。'),
    ('饮湖上初晴后雨', '苏轼', 2, '水光潋滟晴方好，山色空蒙雨亦奇。欲把西湖比西子，淡妆浓抹总相宜。'),
    ('望洞庭', '刘禹锡', 2, '湖光秋月两相和，潭面无风镜未磨。遥望洞庭山水翠，白银盘里一青螺。'),
    ('绝句', '杜甫', 2, '两个黄鹂鸣翠柳，一行白鹭上青天。窗含西岭千秋雪，门泊东吴万里船。'),
    ('晓出净慈寺送林子方', '杨万里', 2, '毕竟西湖六月中，风光不与四时同。接天莲叶无穷碧，映日荷花别样红。'),
    ('赠刘景文', '苏轼', 2, '荷尽已无擎雨盖，菊残犹有傲霜枝。一年好景君须记，最是橙黄橘绿时。'),
    ('夜书所见', '叶绍翁', 2, '萧萧梧叶送寒声，江上秋风动客情。知有儿童挑促织，夜深篱落一灯明。'),
    ('采莲曲', '王昌龄', 2, '荷叶罗裙一色裁，芙蓉向脸两边开。乱入池中看不见，闻歌始觉有人来。'),
    ('题西林壁', '苏轼', 2, '横看成岭侧成峰，远近高低各不同。不识庐山真面目，只缘身在此山中。'),
    ('暮江吟', '白居易', 2, '一道残阳铺水中，半江瑟瑟半江红。可怜九月初三夜，露似真珠月似弓。'),
    ('雪梅', '卢钺', 2, '梅雪争春未肯降，骚人阁笔费评章。梅须逊雪三分白，雪却输梅一段香。'),
    ('出塞', '王昌龄', 2, '秦时明月汉时关，万里长征人未还。但使龙城飞将在，不教胡马度阴山。'),
    ('凉州词', '王翰', 2, '葡萄美酒夜光杯，欲饮琵琶马上催。醉卧沙场君莫笑，古来征战几人回？'),
    ('夏日绝句', '李清照', 2, '生当作人杰，死亦为鬼雄。至今思项羽，不肯过江东。'),
    ('别董大', '高适', 2, '千里黄云白日曛，北风吹雁雪纷纷。莫愁前路无知己，天下谁人不识君？'),
    ('宿新市徐公店', '杨万里', 2, '篱落疏疏一径深，树头新绿未成阴。儿童急走追黄蝶，飞入菜花无处寻。'),
    ('四时田园杂兴（其二十五）', '范成大', 2, '梅子金黄杏子肥，麦花雪白菜花稀。日长篱落无人过，惟有蜻蜓蛱蝶飞。'),
    ('示儿', '陆游', 3, '死去元知万事空，但悲不见九州同。王师北定中原日，家祭无忘告乃翁。'),
    ('题临安邸', '林升', 3, '山外青山楼外楼，西湖歌舞几时休？暖风熏得游人醉，直把杭州作汴州。'),
    ('己亥杂诗', '龚自珍', 3, '九州生气恃风雷，万马齐喑究可哀。我劝天公重抖擞，不拘一格降人才。'),
    ('枫桥夜泊', '张继', 3, '月落乌啼霜满天，江枫渔火对愁眠。姑苏城外寒山寺，夜半钟声到客船。'),
    ('山居秋暝', '王维', 3, '空山新雨后，天气晚来秋。明月松间照，清泉石上流。竹喧归浣女，莲动下渔舟。'),
    ('观书有感（其一）', '朱熹', 3, '半亩方塘一鉴开，天光云影共徘徊。问渠那得清如许？为有源头活水来。'),
    ('村晚', '雷震', 3, '草满池塘水满陂，山衔落日浸寒漪。牧童归去横牛背，短笛无腔信口吹。'),
    ('从军行', '王昌龄', 3, '青海长云暗雪山，孤城遥望玉门关。黄沙百战穿金甲，不破楼兰终不还。'),
    ('秋夜将晓出篱门迎凉有感', '陆游', 3, '三万里河东入海，五千仞岳上摩天。遗民泪尽胡尘里，南望王师又一年。'),
    ('闻官军收河南河北', '杜甫', 3, '剑外忽传收蓟北，初闻涕泪满衣裳。却看妻子愁何在，漫卷诗书喜欲狂。白日放歌须纵酒，青春作伴好还乡。即从巴峡穿巫峡，便下襄阳向洛阳。'),
    ('芙蓉楼送辛渐', '王昌龄', 3, '寒雨连江夜入吴，平明送客楚山孤。洛阳亲友如相问，一片冰心在玉壶。'),
    ('塞下曲', '卢纶', 3, '月黑雁飞高，单于夜遁逃。欲将轻骑逐，大雪满弓刀。'),
    ('泊船瓜洲', '王安石', 3, '京口瓜洲一水间，钟山只隔数重山。春风又绿江南岸，明月何时照我还。'),
    ('游园不值', '叶绍翁', 3, '应怜屐齿印苍苔，小扣柴扉久不开。春色满园关不住，一枝红杏出墙来。'),
    ('竹石', '郑燮', 3, '咬定青山不放松，立根原在破岩中。千磨万击还坚劲，任尔东西南北风。'),
    ('石灰吟', '于谦', 3, '千锤万凿出深山，烈火焚烧若等闲。粉骨碎身浑不怕，要留清白在人间。'),
    ('春夜喜雨', '杜甫', 3, '好雨知时节，当春乃发生。随风潜入夜，润物细无声。野径云俱黑，江船火独明。晓看红湿处，花重锦官城。'),
    ('长歌行', '汉乐府', 3, '青青园中葵，朝露待日晞。阳春布德泽，万物生光辉。常恐秋节至，焜黄华叶衰。百川东到海，何时复西归？少壮不努力，老大徒伤悲。'),
    ('十五夜望月', '王建', 3, '中庭地白树栖鸦，冷露无声湿桂花。今夜月明人尽望，不知秋思落谁家。'),
]


def units(text):
    """把原文切成"句"单元：按句末标点断句，短对仗句再按逗号拆开"""
    parts = [p.strip() for p in re.split(r'[。？！；]', text) if p.strip()]
    out = []
    for p in parts:
        segs = [s.strip() for s in p.split('，') if s.strip()]
        if len(segs) >= 2 and max(len(s) for s in segs) <= 9:
            for i, s in enumerate(segs):
                out.append(s + ('，' if i < len(segs) - 1 else '。'))
        else:
            out.append(p + '。')
    return out


def pick_distractors(a, pool):
    cands = list({u for u in pool if len(u) >= 4 and u != a and abs(len(u) - len(a)) <= 3 and u not in a and a not in u})
    if len(cands) < 2:
        return None
    random.shuffle(cands)
    return cands[:2]


poem_units = [(t, a, b, units(x)) for t, a, b, x in POEMS]
# 每学段内按 KB 顺序分配 6 个段位
band_count = {1: 0, 2: 0, 3: 0}
for _, _, b, _ in poem_units:
    band_count[b] += 1
assigned = {1: 0, 2: 0, 3: 0}
levels = []
for t, a, b, us in poem_units:
    levels.append(min(6, 1 + assigned[b] * 6 // band_count[b]))
    assigned[b] += 1

all_units = [(u, b) for (t, a, b, us), lv in zip(poem_units, levels) for u in us]

out = []
for grade in range(1, 7):
    band = 1 if grade <= 2 else (2 if grade <= 4 else 3)
    my = [(pu, lv) for pu, lv in zip(poem_units, levels) if pu[2] == band]
    band_titles = {t for (t, a, b, us) in poem_units if b == band}
    band_poets = {a for (t, a, b, us) in poem_units if b == band}
    band_units_pool = [u for u, b in all_units if b == band]

    def add(q, a, opts, reason, lv):
        shuffled = opts[:]
        random.shuffle(shuffled)
        out.append({
            'q': q, 'a': a, 'options': shuffled[:2],
            'wrongReasons': [reason, '多读几遍，想想起上一句或下一句'],
            'grade': grade, 'level': lv, 'tag': '古诗背诵',
            'id': 'p%d-%03d' % (grade, len(out))
        })

    for (title, author, _b, us), lv in my:
        # 1) 接下句 / 接上句
        for i in range(len(us) - 1):
            kind = 'next' if i == 0 else ('prev' if i == len(us) - 2 else random.choice(['next', 'prev']))
            if kind == 'next':
                q = '《%s》接下句：%s（　）' % (title, us[i])
                a, reason = us[i + 1], '背一背《%s》：%s%s' % (title, us[i], us[i + 1])
            else:
                q = '《%s》接上句：（　）%s' % (title, us[i + 1] if kind == 'prev' and i + 1 < len(us) else us[i])
                a, reason = us[i], '背一背《%s》：%s%s' % (title, us[i], us[i + 1] if i + 1 < len(us) else '')
            opts = pick_distractors(a, band_units_pool)
            if opts:
                add(q, a, opts, reason, lv)
        # 2) 认作者
        poets = list(band_poets - {author})
        if len(poets) >= 2:
            add('《%s》的作者是谁？' % title, author, random.sample(poets, 2),
                '《%s》——%s' % (title, author), lv)
    # 3) 名句出处（每学段前 6 首）
    for (title, author, _b, us), lv in my[:6]:
        if len(us) < 2:
            continue
        famous = us[-2] if len(us[-2]) <= 12 else us[0]
        others = list(band_titles - {title})
        if len(others) >= 2:
            add('“%s”出自哪首诗？' % famous.rstrip('，。？！'), title, random.sample(others, 2),
                '出自《%s》（%s）' % (title, author), lv)

# 校验：答案不在选项、选项不重复
bad = [x for x in out if x['a'] in x['options'] or len(set(x['options'])) < 2 or len(x['options']) < 2]
final = [x for x in out if x not in bad]

path = os.path.join(os.path.dirname(__file__), '..', 'data', 'banks', 'poems.json')
with open(path, 'w', encoding='utf-8') as f:
    json.dump(final, f, ensure_ascii=False, indent=1)
print('生成', len(final), '道古诗题（剔除无效', len(bad), '）→', os.path.normpath(path))
for g in range(1, 7):
    print('  %d年级: %d 题' % (g, sum(1 for x in final if x['grade'] == g)))
