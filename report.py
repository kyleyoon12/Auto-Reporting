from playwright.sync_api import Playwright, sync_playwright, expect
from selenium import webdriver
import re
import time

def screenshot(playwright: Playwright, url) -> None:

    try:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1440, "height": 2560})

        page = context.new_page()
        print("==============Taking Screenshot==============")

        page.goto(url, timeout=60000)
        page.wait_for_timeout(15000) #15초

        if 'http://' in url:
            url_go = re.sub(pattern='http://', repl='', string=url)
            page.screenshot(path=f'./screenshot/{url_go}.png', full_page=False)
            print('screenshot success! :', url_go)

        elif 'https://' in url:
            url_go = re.sub(pattern='https://', repl='', string=url)
            page.screenshot(path=f'./screenshot/{url_go}.png', full_page=False)
            print('screenshot success! :', url_go)

        else:
            print("링크 잘못됨")

        context.close()
        browser.close()

        return url_go

    except:
        try:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context(viewport={"width": 1440, "height": 2560})

            page = context.new_page()
            print("==============Taking Screenshot==============")

            page.goto(url, timeout=60000)
            page.wait_for_timeout(15000)  # 15초

            if 'http://' in url:
                url_go = re.sub(pattern='http://', repl='', string=url)
                page.screenshot(path=f'./screenshot/{url_go}.png', full_page=False)
                print('screenshot success! :', url_go)

            elif 'https://' in url:
                url_go = re.sub(pattern='https://', repl='', string=url)
                page.screenshot(path=f'./screenshot/{url_go}.png', full_page=False)
                print('screenshot success! :', url_go)

            else:
                print("링크 잘못됨")

            context.close()
            browser.close()

            return url_go

        except:
            try:
                browser = playwright.chromium.launch(headless=False)
                context = browser.new_context(viewport={"width": 1440, "height": 2560})

                page = context.new_page()
                print("==============Taking Screenshot==============")

                page.goto(url, timeout=60000)
                page.wait_for_timeout(15000)  # 15초

                if 'http://' in url:
                    url_go = re.sub(pattern='http://', repl='', string=url)
                    page.screenshot(path=f'./screenshot/{url_go}.png', full_page=False)
                    print('screenshot success! :', url_go)

                elif 'https://' in url:
                    url_go = re.sub(pattern='https://', repl='', string=url)
                    page.screenshot(path=f'./screenshot/{url_go}.png', full_page=False)
                    print('screenshot success! :', url_go)

                else:
                    print("링크 잘못됨")

                context.close()
                browser.close()

                return url_go

            except:
                print(url,"-not valid")

        # import traceback
        # traceback.print_exc()
        # pass

def reporting(url, url_go):

    try:
        reporting_url = "http://www.kocsc.or.kr/sec/rnc/iPinCert.do?preContent=+1.+%EB%AF%BC%EC%9B%90%EC%B7%A8%EC%A7%80+%0A-%0A2.+%EB%AF%BC%EC%9B%90%EB%82%B4%EC%9A%A9+%0A-&conText=%2Fmain&joinType=13&explain=true"

        options = webdriver.ChromeOptions()
        options.add_argument('window-size=1920x1080')
        options.add_argument('disable-gpu')
        options.add_argument('user-agent=Mozilla/5.0 (Linux; Android 11; SM-A102U) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/89.0.4389.72 Mobile Safari/537.36')
        options.add_argument('lang=ko_KR')
        driver = webdriver.Chrome('D:\chromedriver.exe', options=options)

        driver.get(reporting_url)

        a = input("a:")

        driver.find_element_by_css_selector("#login1").send_keys("윤호")
        driver.find_element_by_css_selector("#login2").send_keys("19940220")

        b = input("b:")

        driver.find_element_by_class_name("login-type-btn").click()

        c = input("c:")

        driver.find_element_by_class_name("in_box.in_length150").send_keys("ghgh220@@")
        driver.find_element_by_class_name("btn_t2").click()

        d = input("d:")

        driver.find_element_by_css_selector("#password").send_keys("ghgh220@@")
        driver.find_element_by_css_selector("#password_re").send_keys("ghgh220@@")
        driver.find_element_by_css_selector("#password_ca").send_keys("pink")
        driver.find_element_by_css_selector("#mobile2").send_keys("6394")
        driver.find_element_by_css_selector("#mobile3").send_keys("6391")
        driver.find_element_by_css_selector("#email1").send_keys("kyleyoon12")
        driver.find_element_by_css_selector("#email2").send_keys("gmail.com")

        e = input("e:")

        driver.find_element_by_class_name("btn_t3").click()
        driver.find_element_by_css_selector("#url").send_keys(url)
        driver.find_element_by_css_selector("#subject").send_keys("불법유해사이트 신고합니다_", url_go)
        driver.find_element_by_css_selector("#cont").send_keys("불법유해사이트 신고하오니 조치 부탁 드리겠습니다.")
        driver.find_element_by_css_selector("#ComFileUploader").send_keys("D:/Digital Forensics/2.저작권/8.자동신고시스템/screenshot/", url_go,".png")
        driver.find_element_by_css_selector("#agree").click()
        driver.find_element_by_css_selector("#board > div.js_tab_box.selected > p > a:nth-child(2)").click()

        f = input("f:")

        alert = driver.switch_to.alert
        alert.dismiss()
        #alert.accept()
        #alert.accept()

        time.sleep(10)

        driver.close()

        print(url, "- reporting succeeded")

    except:
        print(url, "- reporting failed")

def main():
    #urls = ["https://toonkor101.com", "https://wfwf202.com"]
    urls = ["https://toonkor101.com"]
    #urls = ["https://wfwf202.com"]

    try:
        for url in urls:
            with sync_playwright() as playwright:
                url_go = screenshot(playwright, url)

                if url_go != None:
                    reporting(url, url_go)

    except:
        print("error")

if __name__ == '__main__':
    main()