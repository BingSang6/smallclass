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
        print('v1.2 errors:', errs if errs else 'none')
        browser.close()

test_v11()
