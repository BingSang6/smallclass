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
        print('unit list (expect 10 = 8单元+2专题):', n_units)
        assert n_units == 10
        page.screenshot(path='shots/14-units.png')
        # v3.2 专题训练：点「解决问题」
        page.locator('#unit-list button', has_text='解决问题').click()
        page.wait_for_selector('#question-text'); page.wait_for_timeout(300)
        tq = page.locator('#question-text').inner_text()
        print('topic question:', tq)
        assert '专题·解决问题' in page.locator('#quiz-level').inner_text()
        page.screenshot(path='shots/14b-topic-quiz.png')
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.locator('.subject-card').first.click(); page.wait_for_timeout(300)
        page.click('#btn-units'); page.wait_for_timeout(200)
        page.locator('#unit-list button').nth(3).click()   # 第四单元 运算律
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
        assert 'u4-' in sched2, 'unit wrong not scheduled'
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
        # 一年级也应有单元（回归：按钮可见性）
        page.evaluate("""() => {
          const d = JSON.parse(localStorage.getItem('smallclass.v1'));
          d.students[0].grade = 1;
          localStorage.setItem('smallclass.v1', JSON.stringify(d));
        }""")
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.locator('.subject-card').first.click(); page.wait_for_timeout(300)
        assert page.locator('#btn-units').is_visible(), 'units btn hidden (grade1)'
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
        assert '接下句' in pq1 or '接上句' in pq1 or '出自' in pq1 or '作者' in pq1
        # 连续两轮抽题应很少重复（池 1800+）
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
        # ---- v3.6: 练习卷生成（单元/期中/期末，可打印） ----
        page.goto(BASE); page.wait_for_load_state('networkidle')
        page.evaluate("document.getElementById('btn-settings').click()")
        page.wait_for_timeout(500)
        page.locator('button', has_text='生成练习卷').click()
        page.wait_for_timeout(300)
        assert page.locator('#screen-paper').is_visible(), 'paper screen not shown'
        n_scopes = page.locator('#paper-scope option').count()
        print('paper scopes (expect 2+8=10):', n_scopes)
        assert n_scopes == 10
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
