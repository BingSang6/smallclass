# -*- coding: utf-8 -*-
"""自动化测试：设置学生→闯关→答对/答错→结算→贴纸册→家长设置导出错题本"""
from playwright.sync_api import sync_playwright

BASE = 'http://localhost:8765'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append('PAGEERROR: ' + str(e)))
    page.on('console', lambda m: errors.append('CONSOLE: ' + m.text) if m.type == 'error' else None)

    page.goto(BASE)
    page.wait_for_load_state('networkidle')
    page.screenshot(path='shots/01-setup.png')

    # 设置学生
    page.click('#btn-add-student')
    page.fill('#inp-name', '测试娃')
    page.click('.grade-btn[data-g="4"]')
    page.click('#btn-create')
    page.wait_for_timeout(500)
    page.screenshot(path='shots/02-hub.png')
    print('hub:', page.locator('#hub-name').inner_text(), '|', page.locator('#hub-sub').inner_text())
    # 进入数学学科
    page.locator('.subject-card').first.click()
    page.wait_for_timeout(300)
    print('home:', page.locator('#hello-name').inner_text(), '|', page.locator('#hello-info').inner_text())

    # 开始闯关
    page.click('#btn-go')
    page.wait_for_selector('#question-text')
    page.wait_for_timeout(300)
    q1 = page.locator('#question-text').inner_text()
    print('question 1:', q1)
    page.screenshot(path='shots/03-quiz.png')

    # 点第一个选项
    page.locator('.opt-btn').first.click()
    page.wait_for_timeout(500)
    # 答错会弹 wrong-overlay；答对自动下一题
    if page.locator('#wrong-overlay').is_visible():
        print('wrong overlay shown:', page.locator('#wrong-reason').inner_text()[:40])
        page.screenshot(path='shots/04-wrong.png')
        page.click('#btn-wrong-ok')
    page.wait_for_timeout(1000)
    print('question 2:', page.locator('#question-text').inner_text())

    # 制造错题数据：人为写入 wrongPool 以测导出
    page.evaluate("""() => {
      const d = JSON.parse(localStorage.getItem('smallclass.v1'));
      d.students[d.current].wrongPool = ['g4-l1-0', 'g4-l1-3'];
      localStorage.setItem('smallclass.v1', JSON.stringify(d));
    }""")

    # 回首页 → 贴纸册
    page.evaluate("TTS.stop()")
    page.goto(BASE)
    page.wait_for_load_state('networkidle')
    page.click("#btn-album2")
    page.wait_for_timeout(300)
    page.screenshot(path='shots/05-album.png')

    # 家长设置 → 导出错题本
    page.goto(BASE)
    page.wait_for_load_state('networkidle')
    page.evaluate("document.getElementById('btn-settings').click()")
    page.wait_for_timeout(300)
    report = page.locator('#export-ta').input_value()
    print('--- 导出错题本 ---')
    print(report)
    page.screenshot(path='shots/06-settings.png')

    print('JS errors:', errors if errors else 'none')
    browser.close()

def test_v11():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        errs = []
        page.on('pageerror', lambda e: errs.append(str(e)))
        page.goto(BASE); page.wait_for_load_state('networkidle')
        # 清空重来
        page.evaluate("localStorage.clear()")
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.click('#btn-add-student'); page.fill('#inp-name', '星娃')
        page.click('.grade-btn[data-g="3"]'); page.click('#btn-create')
        page.wait_for_timeout(400)
        # 模拟打一轮全对：直接改档案验证星级展示与解锁
        page.evaluate("""() => {
          const d = JSON.parse(localStorage.getItem('smallclass.v1'));
          d.students[0].sub.math.levelStars = [1, 0, 0, 0, 0, 0];
          localStorage.setItem('smallclass.v1', JSON.stringify(d));
        }""")
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.locator('.subject-card').first.click()
        page.wait_for_timeout(300)
        info = page.locator('#hello-info').inner_text()
        print('home info:', info)
        assert '★' in info and '☆' in info, 'stars not shown'
        # 白银应已解锁（青铜1星）
        locked = page.locator('.level-card.locked').count()
        print('locked cards (expect 4):', locked)
        assert locked == 4, 'unlock rule wrong'
        # 家长开启全部解锁
        page.evaluate("document.getElementById('btn-settings').click()")
        page.wait_for_timeout(200)
        page.click("text=全部解锁：关")
        page.wait_for_timeout(200)
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.click('.subject-card')   # 进入数学
        page.wait_for_timeout(200)
        locked2 = page.locator('.level-card.locked').count()
        print('locked after unlockAll (expect 0):', locked2)
        assert locked2 == 0, 'unlockAll not working'
        # 点黄金段位开局
        page.locator('.level-card').nth(2).click()
        page.wait_for_selector('#question-text'); page.wait_for_timeout(300)
        print('gold tier question:', page.locator('#question-text').inner_text())
        page.screenshot(path='shots/07-v11-gold.png')
        # ---- v2: 学科大厅 + 语文字词 ----
        page.goto(BASE); page.wait_for_load_state('networkidle')
        cards = page.locator('.subject-card').count()
        print('subject cards (expect 4):', cards)
        assert cards == 4, 'hub cards wrong'
        page.screenshot(path='shots/09-hub.png')
        page.locator('.subject-card').nth(1).click()   # 语文·字词
        page.wait_for_timeout(300)
        print('chinese home title:', page.locator('#hello-name').inner_text())
        assert '语文' in page.locator('#hello-name').inner_text()
        page.screenshot(path='shots/10-chinese-home.png')
        page.click('#btn-go')
        page.wait_for_selector('#question-text'); page.wait_for_timeout(300)
        cq = page.locator('#question-text').inner_text()
        print('chinese question:', cq)
        opts = page.locator('.opt-btn').count()
        print('chinese options (expect 3):', opts)
        assert opts == 3
        page.screenshot(path='shots/11-chinese-quiz.png')
        # 挑战模式：设为白银，回首页点挑战
        page.evaluate("""() => {
          const d = JSON.parse(localStorage.getItem('smallclass.v1'));
          d.students[0].sub.math.level = 1;
          localStorage.setItem('smallclass.v1', JSON.stringify(d));
        }""")
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.locator('.subject-card').first.click()
        page.wait_for_timeout(300)
        assert page.locator('#btn-challenge').is_visible(), 'challenge btn hidden'
        page.click('#btn-challenge')
        page.wait_for_selector('#question-text'); page.wait_for_timeout(500)
        timer = page.locator('#quiz-timer')
        print('challenge timer visible:', timer.is_visible(), '|', timer.inner_text())
        assert timer.is_visible(), 'timer not shown'
        page.screenshot(path='shots/08-challenge.png')
        # ---- v2.5: 今日复习 ----
        # 造一条昨天答错的题（due 已过期）
        page.evaluate("""async () => {
          const d = JSON.parse(localStorage.getItem('smallclass.v1'));
          const p = d.students[0].sub.math;
          let id = p.wrongPool && p.wrongPool[0];
          if (!id) {
            const bank = await fetch('data/banks/math-oral.json').then(r => r.json());
            const q = bank.find(x => x.grade === d.students[0].grade && x.level === p.level + 1);
            id = q.id;
            p.wrongPool = [id];
          }
          p.review[id] = { box: 0, due: 0 };
          localStorage.setItem('smallclass.v1', JSON.stringify(d));
        }""")
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.wait_for_timeout(600)   # 等题库加载后刷新复习卡片
        rb = page.locator('#btn-review')
        print('review card visible:', rb.is_visible(), '|', rb.inner_text())
        assert rb.is_visible(), 'review card not shown'
        rb.click()
        page.wait_for_selector('#question-text'); page.wait_for_timeout(300)
        assert '复习' in page.locator('#quiz-level').inner_text()
        print('review question:', page.locator('#question-text').inner_text())
        page.screenshot(path='shots/12-review.png')
        # 答对第一题（点正确答案）→ 升盒，明天到期
        page.evaluate("""() => {
          const q = window.Quiz && Quiz.current;
          const btns = [...document.querySelectorAll('.opt-btn')];
          const b = btns.find(x => x.textContent === String(q.a));
          b.click();
        }""")
        page.wait_for_timeout(400)
        sched = page.evaluate("""() => {
          const d = JSON.parse(localStorage.getItem('smallclass.v1'));
          const p = d.students[0].sub.math;
          return JSON.stringify(p.review);
        }""")
        print('review schedule after correct:', sched)
        assert '"box":1' in sched, 'box not advanced'
        page.screenshot(path='shots/13-review-result.png')
        # ---- v2.6: 单元巩固（四年级才有单元题库） ----
        page.evaluate("""() => {
          const d = JSON.parse(localStorage.getItem('smallclass.v1'));
          d.students[0].grade = 4;
          localStorage.setItem('smallclass.v1', JSON.stringify(d));
        }""")
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.locator('.subject-card').first.click()   # 数学
        page.wait_for_timeout(300)
        assert page.locator('#btn-units').is_visible(), 'units btn hidden (grade4)'
        page.click('#btn-units')
        page.wait_for_timeout(200)
        n_units = page.locator('#unit-list button').count()
        print('unit list (expect 13 = 11单元+2专题, 2026新版+综合实践导航):', n_units)
        assert n_units == 13
        page.screenshot(path='shots/14-units.png')
        # v3.2 专题训练：点「🎯 解决问题」（按钮文本带 emoji，去掉“专题·”前缀）
        page.locator('#unit-list button', has_text='🎯 解决问题').click()
        page.wait_for_selector('#question-text'); page.wait_for_timeout(300)
        tq = page.locator('#question-text').inner_text()
        print('topic question:', tq)
        assert '专题·解决问题' in page.locator('#quiz-level').inner_text()
        page.screenshot(path='shots/14b-topic-quiz.png')
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.locator('.subject-card').first.click(); page.wait_for_timeout(300)
        page.click('#btn-units'); page.wait_for_timeout(200)
        page.locator('#unit-list button', has_text='第五单元 运算律').click()
        page.wait_for_selector('#question-text'); page.wait_for_timeout(300)
        uq = page.locator('#question-text').inner_text()
        print('unit question:', uq)
        assert '运算律' in page.locator('#quiz-level').inner_text() or '第四' in page.locator('#quiz-level').inner_text()
        uopts = page.locator('.opt-btn').count()
        print('unit options (expect 3):', uopts)
        assert uopts == 3
        page.screenshot(path='shots/15-unit-quiz.png')
        # 答错一题 → 应进入明日复习队列（review due = 明天）
        page.evaluate("""() => {
          const q = Quiz.current;
          const btns = [...document.querySelectorAll('.opt-btn')];
          const b = btns.find(x => x.textContent !== String(q.a));
          b.click();
        }""")
        page.wait_for_timeout(300)
        sched2 = page.evaluate("""() => {
          const d = JSON.parse(localStorage.getItem('smallclass.v1'));
          return JSON.stringify(d.students[0].sub.math.review);
        }""")
        print('review after unit wrong:', sched2)
        assert 'ua4-' in sched2, 'unit wrong not scheduled'
        # ---- v3.4: 全年级单元库（三年级学生应看到 8 个单元 + 4 个专题） ----
        page.evaluate("""() => {
          const d = JSON.parse(localStorage.getItem('smallclass.v1'));
          d.students[0].grade = 3;
          localStorage.setItem('smallclass.v1', JSON.stringify(d));
        }""")
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.locator('.subject-card').first.click(); page.wait_for_timeout(300)
        assert page.locator('#btn-units').is_visible(), 'units btn hidden (grade3)'
        page.click('#btn-units'); page.wait_for_timeout(200)
        n3 = page.locator('#unit-list button').count()
        print('grade3 unit list (expect 12 = 8单元+4专题):', n3)
        assert n3 == 12
        page.locator('#unit-list button', has_text='周长').click()
        page.wait_for_selector('#question-text'); page.wait_for_timeout(300)
        print('grade3 unit question:', page.locator('#question-text').inner_text())
        assert '周长' in page.locator('#quiz-level').inner_text()
        page.screenshot(path='shots/15b-grade3-units.png')
        # 一年级也应有单元（v3.8：2024 新版 7 个单元）
        page.evaluate("""() => {
          const d = JSON.parse(localStorage.getItem('smallclass.v1'));
          d.students[0].grade = 1;
          localStorage.setItem('smallclass.v1', JSON.stringify(d));
        }""")
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.locator('.subject-card').first.click(); page.wait_for_timeout(300)
        assert page.locator('#btn-units').is_visible(), 'units btn hidden (grade1)'
        page.click('#btn-units'); page.wait_for_timeout(200)
        n1 = page.locator('#unit-list button').count()
        print('grade1 unit list (expect 8, 2024新版+数学好玩):', n1)
        assert n1 == 8
        page.locator('#unit-list button', has_text='记录我的一天').click()
        page.wait_for_selector('#question-text'); page.wait_for_timeout(300)
        assert '综合实践' in page.locator('#quiz-level').inner_text()
        page.screenshot(path='shots/15c-grade1-units.png')
        # 还原年级为 3（后续测试基于三年级）
        page.evaluate("""() => {
          const d = JSON.parse(localStorage.getItem('smallclass.v1'));
          d.students[0].grade = 3;
          localStorage.setItem('smallclass.v1', JSON.stringify(d));
        }""")
        # ---- v3.5: 语文单元巩固（部编版全年级）+ 古诗大池（不分年级） ----
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.locator('.subject-card', has_text='语文').first.click(); page.wait_for_timeout(400)
        page.locator('.tab-btn', has_text='字词').click(); page.wait_for_timeout(300)
        assert page.locator('#btn-units').is_visible(), 'chinese units btn hidden'
        page.click('#btn-units'); page.wait_for_timeout(200)
        n_cu = page.locator('#unit-list button').count()
        print('chinese unit list (expect 8):', n_cu)
        assert n_cu == 8
        page.locator('#unit-list button', has_text='美好品质').click()
        page.wait_for_selector('#question-text'); page.wait_for_timeout(300)
        print('chinese unit question:', page.locator('#question-text').inner_text())
        assert '美好品质' in page.locator('#quiz-level').inner_text()
        page.screenshot(path='shots/23-chinese-units.png')
        # ---- v3.8: 2026 新教材（语文四上新 8 单元 + 英语四上新主题） ----
        page.evaluate("""() => {
          const d = JSON.parse(localStorage.getItem('smallclass.v1'));
          d.students[0].grade = 4;
          localStorage.setItem('smallclass.v1', JSON.stringify(d));
        }""")
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.locator('.subject-card', has_text='语文').first.click(); page.wait_for_timeout(400)
        page.locator('.tab-btn', has_text='字词').click(); page.wait_for_timeout(300)
        page.click('#btn-units'); page.wait_for_timeout(200)
        n_cu4 = page.locator('#unit-list button').count()
        print('chinese g4 unit list (expect 8, 2026新版):', n_cu4)
        assert n_cu4 == 8
        page.locator('#unit-list button', has_text='中国的世界文化遗产').click()
        page.wait_for_selector('#question-text'); page.wait_for_timeout(300)
        assert '中国的世界文化遗产' in page.locator('#quiz-level').inner_text()
        page.screenshot(path='shots/23b-chinese-g4-2026.png')
        # 英语四上：沪教新版单元主题词已入库
        en_tags = page.evaluate("""async () => {
          const r = await fetch('data/banks/english-words.json');
          const bank = await r.json();
          return bank.filter(q => q.grade === 4).map(q => q.tag);
        }""")
        uniq_tags = sorted(set(en_tags))
        print('english g4 tags:', uniq_tags)
        assert '英语单词·道路安全' in uniq_tags and '英语单词·祖辈与职业' in uniq_tags, 'english g4 new themes missing'
        # ---- v3.9: 英语单元巩固（沪教版 3~6 年级；当前年级=4，应见 8 单元 + 2 专题(v3.10) = 10） ----
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.locator('.subject-card', has_text='英语').first.click(); page.wait_for_timeout(400)
        assert page.locator('#btn-units').is_visible(), 'english units btn hidden (grade4)'
        page.click('#btn-units'); page.wait_for_timeout(200)
        n_eu = page.locator('#unit-list button').count()
        print('english g4 unit list (expect 10 = 8单元+2专题):', n_eu)
        assert n_eu == 10
        page.screenshot(path='shots/28-english-units.png')
        # v3.10 专题训练：点「方位介词」
        page.locator('#unit-list button', has_text='方位介词').click()
        page.wait_for_selector('#question-text'); page.wait_for_timeout(300)
        print('english topic question:', page.locator('#question-text').inner_text())
        assert '方位介词' in page.locator('#quiz-level').inner_text()
        assert page.locator('.opt-btn').count() == 3
        page.screenshot(path='shots/28a-english-topic.png')
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.locator('.subject-card', has_text='英语').first.click(); page.wait_for_timeout(400)
        page.click('#btn-units'); page.wait_for_timeout(200)
        page.locator('#unit-list button', has_text='道路安全').click()
        page.wait_for_selector('#question-text'); page.wait_for_timeout(300)
        print('english unit question:', page.locator('#question-text').inner_text())
        assert '道路安全' in page.locator('#quiz-level').inner_text()
        assert page.locator('.opt-btn').count() == 3
        # 答对一题 → 单元题正确计分（review 不新增）
        page.evaluate("""() => {
          const q = Quiz.current;
          const btns = [...document.querySelectorAll('.opt-btn')];
          btns.find(x => x.textContent.trim() === String(q.a)).click();
        }""")
        page.wait_for_timeout(300)
        page.screenshot(path='shots/28b-english-unit-quiz.png')
        # v3.12 一年级英语单元（深圳新教材《英语（口语交际）》一上 6 单元）
        page.evaluate("""() => {
          const d = JSON.parse(localStorage.getItem('smallclass.v1'));
          d.students[0].grade = 1;
          localStorage.setItem('smallclass.v1', JSON.stringify(d));
        }""")
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.locator('.subject-card', has_text='英语').first.click(); page.wait_for_timeout(400)
        assert page.locator('#btn-units').is_visible(), 'english units btn hidden (grade1, v3.12)'
        page.click('#btn-units'); page.wait_for_timeout(200)
        n_eu1 = page.locator('#unit-list button').count()
        print('english g1 unit list (expect 6):', n_eu1)
        assert n_eu1 == 6
        page.screenshot(path='shots/28c-english-g1-units.png')
        page.locator('#unit-list button', has_text='家庭').click()
        page.wait_for_selector('#question-text'); page.wait_for_timeout(300)
        print('english g1 unit question:', page.locator('#question-text').inner_text())
        assert '家庭' in page.locator('#quiz-level').inner_text()
        assert page.locator('.opt-btn').count() == 3
        page.screenshot(path='shots/28d-english-g1-quiz.png')
        # 还原年级为 3
        page.evaluate("""() => {
          const d = JSON.parse(localStorage.getItem('smallclass.v1'));
          d.students[0].grade = 3;
          localStorage.setItem('smallclass.v1', JSON.stringify(d));
        }""")
        # 古诗大池：一年级进古诗也应有大量题（grade 0 通用）
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.evaluate("""() => {
          const d = JSON.parse(localStorage.getItem('smallclass.v1'));
          d.students[0].grade = 1;
          localStorage.setItem('smallclass.v1', JSON.stringify(d));
        }""")
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.locator('.subject-card', has_text='语文').first.click(); page.wait_for_timeout(400)
        page.locator('.tab-btn', has_text='古诗').click(); page.wait_for_timeout(300)
        page.click('#btn-go')
        page.wait_for_selector('#question-text'); page.wait_for_timeout(300)
        pq1 = page.locator('#question-text').inner_text()
        print('grade1 poem question:', pq1)
        assert '接下句' in pq1 or '接上句' in pq1 or '出自' in pq1 or '作者' in pq1 or '"' in pq1 or '《' in pq1   # v3.17 课内理解题也算
        # 连续两轮抽题应很少重复（v3.17 起一年级走课内小池，靠 recentQs 防重）
        ids = [page.evaluate('() => Quiz.current.id')]
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.locator('.subject-card', has_text='语文').first.click(); page.wait_for_timeout(400)
        page.locator('.tab-btn', has_text='古诗').click(); page.wait_for_timeout(300)
        page.click('#btn-go'); page.wait_for_selector('#question-text'); page.wait_for_timeout(300)
        ids.append(page.evaluate('() => Quiz.current.id'))
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.locator('.subject-card', has_text='语文').first.click(); page.wait_for_timeout(400)
        page.locator('.tab-btn', has_text='古诗').click(); page.wait_for_timeout(300)
        page.click('#btn-go'); page.wait_for_selector('#question-text'); page.wait_for_timeout(300)
        ids.append(page.evaluate('() => Quiz.current.id'))
        print('poem sample ids:', ids)
        assert len(set(ids)) == len(ids), 'poem repeats across rounds'
        page.screenshot(path='shots/24-poems-big-pool.png')
        # ---- v3.6: 练习卷生成（单元/期中/期末，可打印）→ v3.8 用四上 2026 新版（10 单元+期中期末=12）----
        page.evaluate("""() => {
          const d = JSON.parse(localStorage.getItem('smallclass.v1'));
          d.students[0].grade = 4;
          localStorage.setItem('smallclass.v1', JSON.stringify(d));
        }""")
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.evaluate("document.getElementById('btn-settings').click()")
        page.wait_for_timeout(500)
        page.locator('button', has_text='生成练习卷').click()
        page.wait_for_timeout(300)
        assert page.locator('#screen-paper').is_visible(), 'paper screen not shown'
        n_scopes = page.locator('#paper-scope option').count()
        print('paper scopes (expect 2+11=13, 四上2026新版+综合实践导航):', n_scopes)
        assert n_scopes == 13
        page.click('#btn-paper-gen')
        page.wait_for_timeout(500)
        nq = page.locator('.paper-questions li').count()
        print('paper questions (expect 20):', nq)
        assert nq == 20
        assert '参考答案' in page.locator('#paper-area').inner_text()
        page.select_option('#paper-scope', 'final')
        page.click('#btn-paper-gen'); page.wait_for_timeout(500)
        print('final paper questions:', page.locator('.paper-questions li').count())
        page.screenshot(path='shots/25-paper.png')
        # ---- v3.9/v3.11: 英语练习卷（v3.11 起覆盖 1~6 年级；当前年级=4：范围 = 期中期末 + 8 单元 = 10） ----
        page.select_option('#paper-subject', 'english')
        page.wait_for_timeout(300)
        n_eg = page.locator('#paper-grade option').count()
        print('english paper grades (expect 6, i.e. 1~6):', n_eg)
        assert n_eg == 6
        n_escopes = page.locator('#paper-scope option').count()
        print('english paper scopes (expect 2+8=10):', n_escopes)
        assert n_escopes == 10
        page.click('#btn-paper-gen'); page.wait_for_timeout(500)
        neq = page.locator('.paper-questions li').count()
        print('english paper questions (expect 20):', neq)
        assert neq == 20
        assert '英语' in page.locator('.paper-title').inner_text(), 'paper title should say 英语'
        page.screenshot(path='shots/25b-english-paper.png')
        # v3.12 一年级英语卷：范围 = 期中期末 + 6 单元 = 8；期末全册抽 20 题
        page.select_option('#paper-grade', '1')
        page.wait_for_timeout(300)
        n_g1scopes = page.locator('#paper-scope option').count()
        print('english g1 paper scopes (expect 2+6=8):', n_g1scopes)
        assert n_g1scopes == 8
        page.select_option('#paper-scope', 'final')
        page.click('#btn-paper-gen'); page.wait_for_timeout(500)
        neq1 = page.locator('.paper-questions li').count()
        print('english g1 paper questions (expect 20):', neq1)
        assert neq1 == 20
        page.screenshot(path='shots/25c-english-g1-paper.png')
        # ---- v3.7: 装扮商店 + 起名 ----
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.evaluate("""() => {
          const d = JSON.parse(localStorage.getItem('smallclass.v1'));
          d.students[0].coins = 60;
          localStorage.setItem('smallclass.v1', JSON.stringify(d));
        }""")
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.click('#btn-pet'); page.wait_for_timeout(300)
        n_deco = page.locator('.deco-item').count()
        print('deco items (expect 6):', n_deco)
        assert n_deco == 9   # v3.16：6 常规 + 3 里程碑装扮
        page.screenshot(path='shots/26-deco-shop.png')
        # 买 20 币的礼帽
        page.locator('.deco-item', has_text='小礼帽').locator('button').click()
        page.wait_for_timeout(300)
        state = page.evaluate("""() => {
          const d = JSON.parse(localStorage.getItem('smallclass.v1'));
          return d.students[0].coins + '|' + d.students[0].pet.decos.join(',') + '|' + d.students[0].pet.wearing;
        }""")
        print('after buy (coins|decos|wearing):', state)
        assert state == '40|hat|hat', state
        # 大厅宠物卡应显示装扮
        page.goto(BASE); page.wait_for_load_state('networkidle'); page.wait_for_timeout(300)
        emoji = page.locator('#pet-emoji').inner_text()
        print('hub pet emoji:', emoji)
        assert '🎩' in emoji
        # 起名
        page.click('#btn-pet'); page.wait_for_timeout(300)
        page.fill('#inp-pet-name', '跳跳')
        page.click('#btn-pet-name'); page.wait_for_timeout(300)
        assert page.locator('#pet-title').inner_text() == '跳跳'
        page.screenshot(path='shots/27-pet-named.png')
        # 还原年级为 3（后续测试基于三年级）
        page.evaluate("""() => {
          const d = JSON.parse(localStorage.getItem('smallclass.v1'));
          d.students[0].grade = 3;
          localStorage.setItem('smallclass.v1', JSON.stringify(d));
        }""")
        print('all errors:', errs if errs else 'none')
        # ---- v3.0: 语数英三科大厅 + 语文分支 tab ----
        page.goto(BASE); page.wait_for_load_state('networkidle')
        cards = page.locator('.subject-card').count()
        print('subject cards now (expect 4):', cards)
        assert cards == 4
        names = page.locator('.sc-name').all_inner_texts()
        print('subjects:', names)
        assert names[:3] == ['数学', '语文', '英语'], 'group names wrong: ' + str(names)
        # 英语卡片 → 英语·单词
        page.locator('.subject-card').nth(2).click()
        page.wait_for_timeout(400)
        assert '英语' in page.locator('#hello-name').inner_text()
        assert page.locator('#subject-tabs').is_hidden(), 'english should have no tabs'
        page.screenshot(path='shots/16-english-home.png')
        page.click('#btn-go')
        page.wait_for_selector('#question-text'); page.wait_for_timeout(300)
        eq = page.locator('#question-text').inner_text()
        print('english question:', eq)
        assert ('什么意思' in eq or '的英文是' in eq)
        assert page.locator('.opt-btn').count() == 3
        page.screenshot(path='shots/17-english-quiz.png')
        # 语文卡片 → 字词/古诗 tab 切换
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.locator('.subject-card').nth(1).click()   # 语文（默认字词）
        page.wait_for_timeout(400)
        assert '语文' in page.locator('#hello-name').inner_text()
        tabs = page.locator('#subject-tabs .tab-btn')
        print('chinese tabs:', tabs.all_inner_texts())
        assert tabs.count() == 3, 'chinese should have 3 tabs'
        page.screenshot(path='shots/18-chinese-tabs.png')
        # v3.2：小古文 tab（第 3 个）
        tabs.nth(2).click()
        page.wait_for_timeout(400)
        assert '小古文' in page.locator('#hello-name').inner_text()
        page.screenshot(path='shots/19b-guwen-home.png')
        page.click('#btn-go')
        page.wait_for_selector('#question-text'); page.wait_for_timeout(300)
        wq = page.locator('#question-text').inner_text()
        print('guwen question:', wq)
        assert ('接下句' in wq or '接上句' in wq or '的意思' in wq or '出自哪一篇' in wq)
        assert page.locator('.opt-btn').count() == 3
        page.screenshot(path='shots/19c-guwen-quiz.png')
        # 回语文 tab 切古诗
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.locator('.subject-card').nth(1).click(); page.wait_for_timeout(300)
        tabs = page.locator('#subject-tabs .tab-btn')
        tabs.nth(1).click()   # 切到古诗
        page.wait_for_timeout(400)
        assert '古诗' in page.locator('#hello-name').inner_text()
        page.screenshot(path='shots/19-poem-home.png')
        page.click('#btn-go')
        page.wait_for_selector('#question-text'); page.wait_for_timeout(300)
        pq = page.locator('#question-text').inner_text()
        print('poem question:', pq)
        assert ('接下句' in pq or '接上句' in pq or '作者是谁' in pq or '出自哪首诗' in pq)
        assert page.locator('.opt-btn').count() == 3
        page.screenshot(path='shots/20-poem-quiz.png')
        print('v3.0 errors:', errs if errs else 'none')
        # ---- v2.9: 任务条 / 宠物 / 人机PK ----
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.wait_for_timeout(400)
        n_tasks = page.locator('.task-item').count()
        print('task items (expect 3):', n_tasks)
        assert n_tasks == 3
        print('pet card:', page.locator('#pet-name').inner_text(), '| streak:', page.locator('#hub-streak').inner_text())
        # 宠物喂食：给 10 金币
        page.evaluate("""() => {
          const d = JSON.parse(localStorage.getItem('smallclass.v1'));
          d.students[0].coins = 10;
          localStorage.setItem('smallclass.v1', JSON.stringify(d));
        }""")
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.click('#btn-pet')
        page.wait_for_timeout(200)
        page.click('#btn-feed')
        page.wait_for_timeout(200)
        growth = page.evaluate("""() => {
          const d = JSON.parse(localStorage.getItem('smallclass.v1'));
          return d.students[0].pet.growth + '/' + d.students[0].coins;
        }""")
        print('after feed (growth/coins expect 1/0):', growth)
        assert growth == '1/0'
        page.screenshot(path='shots/18-pet.png')
        # 人机 PK
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.wait_for_timeout(300)
        pk = page.locator('.pk-card')
        assert pk.is_visible(), 'pk card not shown'
        pk.click()
        page.wait_for_selector('#question-text'); page.wait_for_timeout(300)
        print('pk question:', page.locator('#question-text').inner_text(), '| score:', page.locator('#quiz-progress').inner_text())
        assert ': ' in page.locator('#quiz-progress').inner_text() or ' : ' in page.locator('#quiz-progress').inner_text()
        page.evaluate("""() => {
          const q = Quiz.current;
          const b = [...document.querySelectorAll('.opt-btn')].find(x => x.textContent === String(q.a));
          b.click();
        }""")
        page.wait_for_timeout(400)
        print('pk score after correct:', page.locator('#quiz-progress').inner_text())
        assert '1' in page.locator('#quiz-progress').inner_text()
        page.screenshot(path='shots/19-pk.png')
        # 任务进度：PK 答对过 1 题 → 答对10题任务应显示 1/10
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.wait_for_timeout(400)
        t3 = page.locator('.task-item').nth(2).inner_text()
        print('task3 progress:', t3)
        assert '/10）' in t3 and '0/10' not in t3, 'correct counter not tracked'
        page.screenshot(path='shots/20-hub-v29.png')
        # ---- v2.9.1: 喂食反馈 + 答题页宠物 ----
        # 喂食成功要显示提示文案（回归：修复提示被清空的 bug）
        page.evaluate("""() => {
          const d = JSON.parse(localStorage.getItem('smallclass.v1'));
          d.students[0].coins = 30;
          localStorage.setItem('smallclass.v1', JSON.stringify(d));
        }""")
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.click('#btn-pet'); page.wait_for_timeout(200)
        page.click('#btn-feed'); page.wait_for_timeout(300)
        feedmsg = page.locator('#pet-msg').inner_text()
        print('feed msg:', feedmsg)
        assert '好吃' in feedmsg, 'feed feedback missing'
        # 答题页宠物：闯关答对后应有 jump/glow 动画类
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.wait_for_timeout(300)
        page.locator('.subject-card').first.click()
        page.wait_for_timeout(200)
        page.click('#btn-go')
        page.wait_for_selector('#question-text'); page.wait_for_timeout(300)
        pet = page.locator('#quiz-pet')
        assert pet.is_visible(), 'quiz pet not shown'
        print('quiz pet:', pet.inner_text())
        page.evaluate("""() => {
          const q = Quiz.current;
          const b = [...document.querySelectorAll('.opt-btn')].find(x => x.textContent === String(q.a));
          b.click();
        }""")
        page.wait_for_timeout(300)
        cls = page.evaluate("() => document.getElementById('quiz-pet').className")
        print('pet classes after correct:', cls)
        assert 'jump' in cls or 'glow' in cls, 'pet animation missing'
        page.screenshot(path='shots/21-quiz-pet.png')
        print('v2.9.1 errors:', errs if errs else 'none')
        # ---- v2.7: 混合挑战（交错练习） ----
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.wait_for_timeout(300)
        assert page.locator('#btn-mixed').is_visible(), 'mixed btn hidden'
        page.click('#btn-mixed')
        page.wait_for_selector('#question-text'); page.wait_for_timeout(400)
        assert '混合挑战' in page.locator('#quiz-level').inner_text()
        mq = page.locator('#question-text').inner_text()
        print('mixed question 1:', mq)
        # 连答几题看学科是否交错（math 配额 4，前两题同为 math 属正常，取 4 个样本）
        subs = [page.evaluate('() => Quiz.current.subject')]
        for _ in range(4):
            page.evaluate("""() => {
              const q = Quiz.current;
              const b = [...document.querySelectorAll('.opt-btn')].find(x => x.textContent === String(q.a));
              if (b) b.click();
            }""")
            page.wait_for_timeout(1200)
            s = page.evaluate('() => Quiz.current ? Quiz.current.subject : null')
            if s: subs.append(s)
        print('mixed subjects seen:', subs)
        assert len(set(subs)) > 1 or subs[0] != subs[1], 'mixed not interleaved'
        page.screenshot(path='shots/22-mixed.png')
        print('v2.7 errors:', errs if errs else 'none')
        print('v2.9 errors:', errs if errs else 'none')
        browser.close()

test_v11()

def test_unit_coins():
    """v3.14 单元闯关金币：及格（≥60%）才有；答对1题1币、全对+3、首次通关+5、每单元每日前3关产币"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        errs = []
        page.on('pageerror', lambda e: errs.append('PAGEERROR: ' + str(e)))
        page.on('console', lambda m: errs.append('CONSOLE: ' + m.text) if m.type == 'error' else None)
        page.goto(BASE); page.wait_for_load_state('networkidle')
        # 新学生（四年级，数学 g4 有「第五单元 运算律」）
        page.click('#btn-add-student')
        page.fill('#inp-name', '金币娃')
        page.click('.grade-btn[data-g="4"]')
        page.click('#btn-create')
        page.wait_for_timeout(500)
        page.evaluate("""() => {
          const d = JSON.parse(localStorage.getItem('smallclass.v1'));
          d.students[d.current].coins = 20;
          localStorage.setItem('smallclass.v1', JSON.stringify(d));
        }""")

        def enter_unit_round():
            page.goto(BASE); page.wait_for_load_state('networkidle')
            page.locator('.subject-card').first.click(); page.wait_for_timeout(400)
            page.click('#btn-units'); page.wait_for_timeout(300)
            page.locator('#unit-list button', has_text='第五单元 运算律').click()
            page.wait_for_selector('#question-text'); page.wait_for_timeout(300)

        def coins_and_uc():
            return page.evaluate("""() => {
              const s = JSON.parse(localStorage.getItem('smallclass.v1')).students[0];
              const uc = s.unitCoins && s.unitCoins['math|第五单元 运算律'];
              return [s.coins, uc ? (uc.n + ',' + uc.c) : 'none'];
            }""")

        def answer_correct():
            page.evaluate("""() => {
              const q = Quiz.current;
              const b = [...document.querySelectorAll('.opt-btn')].find(x => x.textContent === String(q.a));
              b.click();
            }""")
            page.wait_for_timeout(1100)   # 答对 900ms 后自动进入下一题

        def answer_wrong():
            page.evaluate("""() => {
              const q = Quiz.current;
              const b = [...document.querySelectorAll('.opt-btn')].find(x => x.textContent !== String(q.a));
              b.click();
            }""")
            page.wait_for_timeout(300)
            page.click('#btn-wrong-ok')
            page.wait_for_timeout(300)

        # ---- 第 1 轮：5/5 全对 → 5题×1币 + 全对3 + 首通5 + 每日任务(round)5 = 18 ----
        enter_unit_round()
        for _ in range(5): answer_correct()
        page.wait_for_selector('#result-title'); page.wait_for_timeout(400)
        c1, u1 = coins_and_uc()
        print('round1 (5/5) coins:', c1, 'unitCoins(n,c):', u1)
        assert c1 - 20 >= 18, 'round1 expected >= 38, got %d' % c1
        assert u1 == '1,1', u1

        # ---- 第 2 轮：再全对 → 5+3（首通已领；当天第10次答对触发 correct10 +5）----
        enter_unit_round()
        for _ in range(5): answer_correct()
        page.wait_for_selector('#result-title'); page.wait_for_timeout(400)
        c2, u2 = coins_and_uc()
        print('round2 (5/5) coins:', c2, 'unitCoins(n,c):', u2)
        assert c2 - c1 >= 8, 'round2 expected +>=8, got +%d' % (c2 - c1)
        assert u2 == '2,1', u2

        # ---- 第 3 轮：每题先错后对 → 5/10 = 50% 不及格 → 0 币，n 不再增长 ----
        enter_unit_round()
        for _ in range(5): answer_wrong()      # 单元模式答错会排到队尾重问
        for _ in range(5): answer_correct()
        page.wait_for_selector('#result-title'); page.wait_for_timeout(400)
        c3, u3 = coins_and_uc()
        print('round3 (5/10 fail-gate) coins:', c3, 'unitCoins(n,c):', u3)
        assert c3 == c2, 'round3 should earn 0 coins, +%d' % (c3 - c2)
        assert u3 == '2,1', u3

        page.screenshot(path='shots/28-unit-coins.png')
        print('v3.14 unit-coin errors:', errs if errs else 'none')
        assert not errs, errs
        browser.close()

test_unit_coins()

def test_v315():
    """v3.15：英语单元扩容（g1/g4 每单元≥12题）+ 微自适应（连对3升/连错2降）+ 错题变式重现"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        errs = []
        page.on('pageerror', lambda e: errs.append('PAGEERROR: ' + str(e)))
        page.on('console', lambda m: errs.append('CONSOLE: ' + m.text) if m.type == 'error' else None)
        page.goto(BASE); page.wait_for_load_state('networkidle')

        # ---- ① 英语单元银行：g1 6 单元 / g4 8 单元，每单元 ≥12 题 ----
        en = page.evaluate("""() => fetch('data/banks/english-units.json').then(r => r.json())""")
        cnt = {}
        for q in en:
            if q['grade'] in (1, 4):
                cnt[(q['grade'], q['unit'])] = cnt.get((q['grade'], q['unit']), 0) + 1
        print('english units g1:', sum(1 for k in cnt if k[0] == 1), '/ g4:', sum(1 for k in cnt if k[0] == 4))
        assert sum(1 for k in cnt if k[0] == 1) == 6 and sum(1 for k in cnt if k[0] == 4) == 8
        for k, n in cnt.items():
            assert n >= 12, ('english unit <12', k, n)
        print('english per-unit counts all >=12:', sum(cnt.values()), 'questions in g1+g4')

        # ---- ② 微自适应：连对 3 题升层、连错 2 题降层 ----
        page.click('#btn-add-student')
        page.fill('#inp-name', '自适应娃')
        page.click('.grade-btn[data-g="4"]')
        page.click('#btn-create')
        page.wait_for_timeout(500)

        def enter_unit(name):
            page.goto(BASE); page.wait_for_load_state('networkidle')
            page.locator('.subject-card').first.click(); page.wait_for_timeout(400)
            page.click('#btn-units'); page.wait_for_timeout(300)
            page.locator('#unit-list button', has_text=name).click()
            page.wait_for_selector('#question-text'); page.wait_for_timeout(300)

        def click_ok():
            page.evaluate("""() => {
              const q = Quiz.current;
              const b = [...document.querySelectorAll('.opt-btn')].find(x => x.textContent === String(q.a));
              b.click();
            }""")
            page.wait_for_timeout(1100)

        def click_wrong():
            page.evaluate("""() => {
              const q = Quiz.current;
              const b = [...document.querySelectorAll('.opt-btn')].find(x => x.textContent !== String(q.a));
              b.click();
            }""")
            page.wait_for_timeout(300)
            page.click('#btn-wrong-ok')
            page.wait_for_timeout(300)

        enter_unit('第五单元 运算律')
        assert page.evaluate('() => Quiz.difLevel') == 2, 'start dif should be 2'
        click_ok(); click_ok()
        assert page.evaluate('() => Quiz.difLevel') == 2
        click_ok()
        assert page.evaluate('() => Quiz.difLevel') == 3, '3 连对应升到 3 层'
        click_ok(); click_ok()   # 打完第 1 关（5/5）
        page.wait_for_selector('#result-title'); page.wait_for_timeout(300)

        # 第 2 关应优先抽 3 层（挑战）题
        enter_unit('第五单元 运算律')
        d = page.evaluate('() => (Quiz.current && Quiz.current.dif) || 2')
        print('round2 first question dif (expect 3):', d)
        assert d == 3, 'round2 should pick dif-3 questions'
        # 连错 2 题 → 降到 1 层
        click_wrong()
        assert page.evaluate('() => Quiz.difLevel') == 3
        click_wrong()
        assert page.evaluate('() => Quiz.difLevel') == 2, '2 连错应降一层'
        # 收尾打完这一关
        for _ in range(8):
            if page.locator('#result-title').is_visible():
                break
            click_ok()
        page.wait_for_timeout(300)

        # ---- ③ 错题变式重现：答错 vt 题后，同模板不同题号再现 ----
        page.evaluate("""() => {
          const d = JSON.parse(localStorage.getItem('smallclass.v1'));
          const s = d.students[d.current];
          s.sub.math.recentQs = [];   // 清近期记录，避免干扰
          localStorage.setItem('smallclass.v1', JSON.stringify(d));
        }""")
        mbank = page.evaluate("""() => fetch('data/banks/math-units.json').then(r => r.json())""")
        enter_unit('第三单元 整数乘法（二）')
        wrong_vt = wrong_id = None
        for _ in range(8):
            info = page.evaluate("""() => Quiz.current && {id: Quiz.current.id, vt: Quiz.current.vt || null}""")
            if info and info['vt'] and sum(1 for x in mbank if x.get('vt') == info['vt']) >= 2:
                wrong_vt, wrong_id = info['vt'], info['id']
                click_wrong()
                break
            click_ok()
        assert wrong_vt, 'no vt question encountered'
        seen = []
        for _ in range(12):
            if page.locator('#result-title').is_visible():
                break
            info = page.evaluate("""() => Quiz.current && {id: Quiz.current.id, vt: Quiz.current.vt || null}""")
            if info:
                seen.append(info)
            click_ok()
        hits = [s for s in seen if s['vt'] == wrong_vt and s['id'] != wrong_id]
        print('variant requeue: wronged %s (%s), later same-vt questions: %d' % (wrong_id, wrong_vt, len(hits)))
        assert hits, 'variant of wronged question should reappear'

        page.screenshot(path='shots/29-v315-adaptive.png')
        print('v3.15 errors:', errs if errs else 'none')
        assert not errs, errs
        browser.close()

test_v315()

def test_v316():
    """v3.16：语文单元扩容（g1/g4 每单元12题）+ 单元掌握度 🌱🌿🌳 + 金币里程碑装扮"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        errs = []
        page.on('pageerror', lambda e: errs.append('PAGEERROR: ' + str(e)))
        page.on('console', lambda m: errs.append('CONSOLE: ' + m.text) if m.type == 'error' else None)
        page.goto(BASE); page.wait_for_load_state('networkidle')

        # ---- ① 语文单元银行：g1/g4 各 8 单元，每单元 ≥12 题 ----
        cn = page.evaluate("""() => fetch('data/banks/chinese-units.json').then(r => r.json())""")
        cnt = {}
        for q in cn:
            if q['grade'] in (1, 4):
                cnt[(q['grade'], q['unit'])] = cnt.get((q['grade'], q['unit']), 0) + 1
        print('chinese units g1:', sum(1 for k in cnt if k[0] == 1), '/ g4:', sum(1 for k in cnt if k[0] == 4))
        assert sum(1 for k in cnt if k[0] == 1) == 8 and sum(1 for k in cnt if k[0] == 4) == 8
        for k, n in cnt.items():
            assert n >= 12, ('chinese unit <12', k, n)
        assert len(cn) == 360, len(cn)
        # 公版古诗填空抽查（出塞）
        mu = [q for q in cn if '秦时明月' in q['q']]
        assert mu and mu[0]['a'] == '万里长征人未还', 'gushi fill missing'
        print('chinese g1+g4 per-unit all >=12, total', len(cn))

        # ---- ② 单元掌握度 chips：注入 unitStats → 列表显示 🌱/🌿/🌳 ----
        page.click('#btn-add-student')
        page.fill('#inp-name', '里程碑娃')
        page.click('.grade-btn[data-g="4"]')
        page.click('#btn-create')
        page.wait_for_timeout(500)
        page.evaluate("""() => {
          const d = JSON.parse(localStorage.getItem('smallclass.v1'));
          const s = d.students[d.current];
          s.unitStats = {
            'chinese|第一单元 自然之美': { a: 5, c: 5 },
            'chinese|第二单元 提问策略': { a: 10, c: 9 },
            'chinese|第三单元 连续观察': { a: 20, c: 19 },
            'chinese|第四单元 中外神话': { a: 3, c: 3 }
          };
          localStorage.setItem('smallclass.v1', JSON.stringify(d));
        }""")
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.locator('.subject-card').nth(1).click(); page.wait_for_timeout(400)
        page.click('#btn-units'); page.wait_for_timeout(300)
        texts = page.locator('#unit-list button').all_text_contents()
        assert any('自然之美 🌱' in t for t in texts), texts[:4]
        assert any('提问策略 🌿' in t for t in texts), texts[:4]
        assert any('连续观察 🌳' in t for t in texts), texts[:4]
        assert not any('中外神话 🌱' in t or '中外神话 🌿' in t or '中外神话 🌳' in t for t in texts), texts[:4]
        print('mastery chips OK:', [t for t in texts if '单元' in t][:4])

        # ---- ③ 完成一关语文单元 → unitStats 自动累计 + coinsEarned 入账 ----
        page.locator('#unit-list button', has_text='第五单元').click()
        page.wait_for_selector('#question-text'); page.wait_for_timeout(300)
        for _ in range(8):
            if page.locator('#result-title').is_visible():
                break
            page.evaluate("""() => {
              const q = Quiz.current;
              const b = [...document.querySelectorAll('.opt-btn')].find(x => x.textContent === String(q.a));
              b.click();
            }""")
            page.wait_for_timeout(1100)
        page.wait_for_timeout(400)
        st = page.evaluate("""() => {
          const s = JSON.parse(localStorage.getItem('smallclass.v1')).students[
            JSON.parse(localStorage.getItem('smallclass.v1')).current];
          return { a: s.unitStats['chinese|第五单元 习作单元（把事情写清楚）'].a,
                   coins: s.coins || 0, earned: s.coinsEarned || 0 };
        }""")
        print('after 1 perfect chinese round:', st)
        assert st['a'] >= 5, st
        assert st['earned'] == 18 and st['coins'] == 18, st   # 5题5币+全对3+首通5+任务5，新档案初始0币

        # ---- ④ 金币里程碑装扮：锁定 → 解锁领取（免费） ----
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.click('#btn-pet'); page.wait_for_timeout(400)
        halo = page.locator('.deco-item', has_text='天使光环')
        assert halo.locator('button').is_disabled(), 'halo should be locked'
        assert '累计100' in halo.locator('button').text_content(), halo.locator('button').text_content()
        rocket = page.locator('.deco-item', has_text='小火箭')
        assert rocket.locator('button').is_disabled()
        page.evaluate("""() => {
          const d = JSON.parse(localStorage.getItem('smallclass.v1'));
          d.students[d.current].coinsEarned = 150;
          localStorage.setItem('smallclass.v1', JSON.stringify(d));
        }""")
        page.goto(BASE); page.wait_for_load_state('networkidle'); page.wait_for_timeout(400)
        page.click('#btn-pet'); page.wait_for_timeout(400)
        halo = page.locator('.deco-item', has_text='天使光环')
        btn = halo.locator('button')
        assert not btn.is_disabled() and '免费领取' in btn.text_content(), btn.text_content()
        coins0 = page.evaluate("""() => JSON.parse(localStorage.getItem('smallclass.v1')).students[
          JSON.parse(localStorage.getItem('smallclass.v1')).current].coins""")
        btn.click(); page.wait_for_timeout(400)
        st2 = page.evaluate("""() => {
          const s = JSON.parse(localStorage.getItem('smallclass.v1')).students[
            JSON.parse(localStorage.getItem('smallclass.v1')).current];
          return { coins: s.coins, decos: s.pet.decos, wearing: s.pet.wearing };
        }""")
        print('after claim halo:', st2, 'coins before:', coins0)
        assert 'halo' in st2['decos'] and st2['wearing'] == 'halo'
        assert st2['coins'] == coins0, 'milestone deco must be free'
        page.screenshot(path='shots/30-v316-milestone.png')

        print('v3.16 errors:', errs if errs else 'none')
        assert not errs, errs
        browser.close()

test_v316()

def test_v317():
    """v3.17 课本古诗：g1/g4 古诗只出课内必背 12 首；段位图显示篇目名；其他年级保持通用池"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        errs = []
        page.on('pageerror', lambda e: errs.append('PAGEERROR: ' + str(e)))
        page.on('console', lambda m: errs.append('CONSOLE: ' + m.text) if m.type == 'error' else None)
        page.goto(BASE); page.wait_for_load_state('networkidle')

        # ---- ① 题库：课本古诗带年级标，干扰项全课内 ----
        poems = page.evaluate("""() => fetch('data/banks/poems.json').then(r => r.json())""")
        tx = [q for q in poems if str(q['id']).startswith('ptx-')]
        g1 = [q for q in tx if q['grade'] == 1]
        g4 = [q for q in tx if q['grade'] == 4]
        print('textbook poems: g1 %d / g4 %d (bank %d)' % (len(g1), len(g4), len(poems)))
        assert len(g1) == 38 and len(g4) == 42
        t1 = set(q['tag'] for q in g1); t4 = set(q['tag'] for q in g4)
        assert t1 == set('古诗·' + t for t in ['咏鹅', '画', '悯农（其二）', '风', '江南', '古朗月行（节选）']), t1
        assert t4 == set('古诗·' + t for t in ['暮江吟', '题西林壁', '雪梅', '出塞', '凉州词', '夏日绝句']), t4
        for g, pool in ((1, g1), (4, g4)):
            for lv in range(1, 7):
                assert sum(1 for q in pool if q['level'] == lv) >= 5, (g, lv)

        def make_student(name, grade):
            page.goto(BASE); page.wait_for_load_state('networkidle')
            sw = page.locator('#btn-switch2')
            if sw.is_visible():
                sw.click(); page.wait_for_timeout(400)   # 回到选人页才能新建
            page.click('#btn-add-student')
            page.fill('#inp-name', name)
            page.click('.grade-btn[data-g="%d"]' % grade)
            page.click('#btn-create')
            page.wait_for_timeout(500)

        def enter_poem_and_play(grade):
            """进古诗 tab 打一关（全答对），返回本关全部题 tag / 首题信息"""
            page.goto(BASE); page.wait_for_load_state('networkidle')
            page.locator('.subject-card').nth(1).click(); page.wait_for_timeout(400)
            page.locator('.tab-btn', has_text='古诗').click(); page.wait_for_timeout(400)
            names = page.locator('#level-map button').all_text_contents()
            page.locator('#level-map button').first.click()
            page.wait_for_selector('#question-text'); page.wait_for_timeout(300)
            tags = []
            first = None
            for _ in range(10):
                info = page.evaluate("""() => Quiz.current && {id: Quiz.current.id, tag: Quiz.current.tag}""")
                if info and not first: first = info
                if info: tags.append(info['tag'])
                page.evaluate("""() => {
                  const q = Quiz.current;
                  const b = [...document.querySelectorAll('.opt-btn')].find(x => x.textContent === String(q.a));
                  b.click();
                }""")
                page.wait_for_timeout(1100)
                if page.locator('#result-title').is_visible():
                    break
            page.wait_for_timeout(300)
            return names, first, tags

        # ---- ② g1：只出课内 6 首，段位图=篇目名 ----
        make_student('古诗娃娃', 1)
        names, first, tags = enter_poem_and_play(1)
        print('g1 poem level map:', names[:6])
        print('g1 poem round tags:', set(tags))
        assert any('咏鹅' in n for n in names), names
        assert str(first['id']).startswith('ptx-'), first
        allowed = set('古诗·' + t for t in ['咏鹅', '画', '悯农（其二）', '风', '江南', '古朗月行（节选）'])
        assert set(tags) <= allowed, set(tags) - allowed

        # ---- ③ g4：只出课内 6 首 ----
        make_student('古诗哥哥', 4)
        names, first, tags = enter_poem_and_play(4)
        print('g4 poem level map:', names[:6])
        print('g4 poem round tags:', set(tags))
        assert any('暮江吟' in n for n in names), names
        assert str(first['id']).startswith('ptx-'), first
        allowed4 = set('古诗·' + t for t in ['暮江吟', '题西林壁', '雪梅', '出塞', '凉州词', '夏日绝句'])
        assert set(tags) <= allowed4, set(tags) - allowed4
        page.screenshot(path='shots/31-v317-poem.png')

        # ---- ④ g2：无年级题 → 走通用池（旧逻辑不变） ----
        make_student('古诗二年级', 2)
        names, first, tags = enter_poem_and_play(2)
        print('g2 poem first q:', first, '| level map head:', names[:2])
        assert str(first['id']).startswith('pt-'), first   # 通用池老题

        print('v3.17 errors:', errs if errs else 'none')
        assert not errs, errs
        browser.close()

test_v317()
