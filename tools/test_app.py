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
    print('hub:', page.locator('#hub-name').inner_text(), '|', page.locator('#hub-info').inner_text())
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
        print('unit list (expect 8):', n_units)
        assert n_units == 8
        page.screenshot(path='shots/14-units.png')
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
        print('all errors:', errs if errs else 'none')
        browser.close()

test_v11()
