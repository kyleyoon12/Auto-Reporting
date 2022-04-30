from playwright.sync_api import Playwright, sync_playwright, expect
from selenium.webdriver.common.by import By
from selenium import webdriver
import sqlite3
import re

def fetch_urls():
    with sqlite3.connect("./illegals.db") as db_connection:
        cur = db_connection.cursor()
        cur.execute("SELECT main_url from illegal_sites where site_available IS NULL")
        row = cur.fetchall()
        url_raw = re.findall(
            'http[s]?://(?:[a-zA-Z-ㄱ-ㅣ가-힣]|[0-9]|[$\-@\.&+:/?=_&;]|[!*\(\),]|(?:%[0-9a-fA-F-ㄱ-ㅣ가-힣][0-9a-fA-F-ㄱ-ㅣ가-힣]))+',
            str(row))
        return url_raw

def fetch_expected_category(url):
    with sqlite3.connect("./illegals.db") as category_conn:
        cur = category_conn.cursor()
        sql = "SELECT " + "expected_category" + " from illegal_sites WHERE main_url = ?"
        cur.execute(sql, (url,))
        category_raw = cur.fetchone()
        category = re.sub('[-=+,‘|\(\)\'…》]','', str(category_raw))

        if category == 'adult':
            return '성인'
        elif category == 'gamble':
            return '도박'
        elif category == 'webtoon':
            return '웹툰'
        elif category == 'torrent':
            return '토렌트'
        elif category == 'prostitution':
            return '성매매'
        elif category == 'streaming':
            return '스트리밍'
        else:
            return '유해'

def reporting(url, url_go):
    category = fetch_expected_category(url)
    reporting_url = "http://www.kocsc.or.kr/sec/rnc/iPinCert.do?preContent=+1.+%EB%AF%BC%EC%9B%90%EC%B7%A8%EC%A7%80+%0A-%0A2.+%EB%AF%BC%EC%9B%90%EB%82%B4%EC%9A%A9+%0A-&conText=%2Fmain&joinType=13&explain=true"

    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1920x1080')
    options.add_argument('disable-gpu')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Linux; Android 11; SM-A102U) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/89.0.4389.72 Mobile Safari/537.36')
    options.add_argument('lang=ko_KR')
    driver = webdriver.Chrome('D:\chromedriver.exe', options=options)
    file_path = "C:\\Users\\taylor\\Desktop\\autoreportsystem\\filter\\filter_0427\\github\\Automation\\screenshot\\" + url_go + ".png"

    # 양식 기입
    driver.get(reporting_url)
    driver.find_element_by_css_selector("#login1").send_keys("윤호")
    driver.find_element_by_css_selector("#login2").send_keys("19940220")
    driver.find_element_by_class_name("login-type-btn").click()
    driver.find_element_by_class_name("in_box.in_length150").send_keys("ghgh220@@")
    driver.find_element_by_class_name("btn_t2").click()
    driver.find_element_by_css_selector("#password").send_keys("ghgh220@@")
    driver.find_element_by_css_selector("#password_re").send_keys("ghgh220@@")
    driver.find_element_by_css_selector("#password_ca").send_keys("pink")
    driver.find_element_by_css_selector("#mobile2").send_keys("6394")
    driver.find_element_by_css_selector("#mobile3").send_keys("6391")
    driver.find_element_by_css_selector("#email1").send_keys("kyleyoon12")
    driver.find_element_by_css_selector("#email2").send_keys("gmail.com")
    driver.find_element_by_class_name("btn_t3").click()
    driver.find_element_by_css_selector("#url").send_keys(url)
   # driver.find_element_by_css_selector("#female").click()
    # driver.find_element_by_css_selector("#subject").send_keys("[%s]유해사이트 신고합니다_" %category, url_go)

    driver.find_element_by_css_selector("#cont").send_keys("유해 " + category +"사이트 신고하오니 조치 부탁 드리겠습니다.")
    # driver.find_element_by_css_selector("#ComFileUploader").send_keys(
    #     "./screenshot/", url_go, ".png")
    driver.find_element(By.XPATH, '//input[@id="ComFileUploader"]').send_keys(file_path)
    driver.find_element_by_css_selector("#agree").click()
    driver.find_element_by_css_selector("#board > div.js_tab_box.selected > p > a:nth-child(2)").click()

    # 알람창 처리
    alert = driver.switch_to.alert
    # alert.dismiss()
    alert.accept()
    alert.accept()


    driver.close()


def filtering(title, body):

    light_illegal_keywords = ['애니','웹툰', '미리보기', '유료', '무료', '망가', '인기', '만화', '썰', '순위',
                              '다시보기', '드라마', '티비', '스트리밍', '링크', 'streaming', 'STREAMING', 'Streaming', 'STREAMS', 'Streams', 'stream', 'Streams', 'STREAMS',
                              '실시간', '최신', '주소', '토렌트', 'torrent', 'TORRENT', 'Torrent','줄거리', '공유', '영화', '성인', '야동', '노모', '일본', '유출', '국산', '몰카',
                              '오피', '안마', '유흥', '업소', '키스', '벗방', 'SEX', 'Sex', 'sex', 'Porn', 'porn', 'PORN', '마사지',
                              '토토', '도박', '머니', '스포츠', '베팅', '고액', '배당', '가입', '매충', '지급', '보증', '포커', '경기', '카지노',
                              '환전', '유럽', '중계', '바카라', '먹튀',
                              '토끼', '툰코', '호두코믹스', '포토툰', '늑대닷컴', '펀비']

    cnt = 0
    match_result = []

    if title == '불법·유해정보사이트에 대한 차단 안내':
        return cnt
    elif '판매용입니다' in title:
        return cnt

    for keyword in light_illegal_keywords:
        if keyword in title:
            cnt += 1
            match_result.append(keyword)

        elif keyword not in title:
            if keyword in body:
                cnt += 1
                match_result.append(keyword)

    print(">>> [Verification] Title:", title)
    print(">>> [Result] Match Count: [%d]" % cnt, "Match With", match_result)

    return cnt

def run(playwright: Playwright, urls):

    sql_available_urls = []

    unaccessible = 0 #status != 200
    accessible_not_illegal = 0 #status = 200 & 유해사이트 아님
    accessible_illegal = 0 #status = 200 & 유해사이트인경우

    conn = sqlite3.connect("illegals.db")
    for i, url in enumerate(urls):
        try:
            print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
            print("[%d]Checking Response on:" % (i+1), url)
            print(">>> First Trial on:", url)
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context(viewport={"width": 1440, "height": 2560})

            page = context.new_page()
            response = page.goto(url, timeout=30000)
            print(">>> [Status]", response.status)
            if response.status == 200:
                print(">>> [Result] Success")
                title = page.inner_text("title")
                body = page.inner_text("body")
                result = filtering(title, body) #1 or 0
                if result < 2:
                    print(">>> [WhiteList URL] ", url)
                    accessible_not_illegal += 1

                    #title, siteavailable False 입력하는 sql코드
                    cur = conn.cursor()

                    sql = "UPDATE " + "illegal_sites" + " SET title = ?, site_available = ? WHERE main_url = ?"
                    # print(sql)

                    cur.execute(sql, (title, False, url))
                    conn.commit()

                else:
                    # page.wait_for_timeout(15000)
                    sql_available_urls.append([url, title])
                    print(">>> [Available URL]:", "Title:", title)

                    if 'http://' in url:
                        url_go = re.sub(pattern='http://', repl='', string=url)
                        page.screenshot(path=f'./screenshot/{url_go}.png', full_page=False)
                        print('>>> [Screenshot Success]:', url_go)

                    elif 'https://' in url:
                        url_go = re.sub(pattern='https://', repl='', string=url)
                        page.screenshot(path=f'./screenshot/{url_go}.png', full_page=False)
                        print('>>> [Screenshot Success]:', url_go)

                    #report = (reporting 함수)
                    reporting(url, url_go)

                    try:
                        print(">>> [Reporting Result] Reporting Succeeded: ", url)
                        cur = conn.cursor()
                        sql = "UPDATE " + "illegal_sites" + " SET is_reported = ? WHERE main_url = ?"
                        cur.execute(sql, (True, url))
                        conn.commit()
                    except:
                        print(">>> " )

                    accessible_illegal += 1
                    #title과 site available이 True 입력하는 sql
                    cur = conn.cursor()
                    sql = " UPDATE " + "illegal_sites" + " SET title = ?, site_available = ? WHERE main_url = ?"
                    cur.execute(sql, (title, True, url))
                    conn.commit()

            context.close()
            browser.close()

        # except Exception as e:
        except Exception as e:

            context.close()
            browser.close()


            import traceback
            traceback.print_exc()
            pass

            unaccessible += 1

            print(">>> [Result] First Trial Failed")
            print(">>> [Unavailable URL]", url, "will be given 'FALSE'")
            # print("error:", e)

            # site available 0 주는 sql 코드
            cur = conn.cursor()
            sql = " UPDATE " + "illegal_sites" + " SET site_available = ? WHERE main_url = ?"
            cur.execute(sql, (False, url))
            conn.commit()




            # try:
            #     print(">>> [Result] First Trial Failed")
            #     print(">>> Second Trial on:", url)
            #
            #     browser = playwright.chromium.launch(headless=False)
            #     context = browser.new_context(viewport={"width": 1440, "height": 2560})
            #
            #     page = context.new_page()
            #     page.wait_for_timeout(5000)
            #     response = page.goto(url, timeout=60000)
            #     print(">>> [Status]", response.status)
            #     if response.status == 200:
            #         title = page.inner_text("title")
            #         body = page.inner_text("body")
            #         result = filtering(title, body)  # 1 or 0
            #         if result == 0:
            #             print(">>> [WhiteList URL] ", url)
            #             # title과 Site Available False 주기
            #             cur = conn.cursor()
            #             sql = " UPDATE " + "illegal_sites" + " SET title = ?, site_available = ? WHERE main_url = ?"
            #             cur.execute(sql, (title, False, url))
            #             conn.commit()
            #
            #         else:
            #             # True인 애들
            #             # page.wait_for_timeout(10000)
            #             sql_available_urls.append([url, title])
            #             print(">>> [Available URL] ", "Title:", title)
            #
            #             if 'http://' in url:
            #                 url_go = re.sub(pattern='http://', repl='', string=url)
            #                 page.screenshot(path=f'./screenshot/{url_go}.png', full_page=False)
            #                 print('>>> [Screenshot Success] ', url_go)
            #
            #             elif 'https://' in url:
            #                 url_go = re.sub(pattern='https://', repl='', string=url)
            #                 page.screenshot(path=f'./screenshot/{url_go}.png', full_page=False)
            #                 print('>>> [Screenshot success] ', url_go)
            #
            #             # reporting(url)
            #             reporting(url, url_go)
            #             try:
            #                 print(">>> [Reporting Result] Reporting Succeeded: ", url)
            #                 cur = conn.cursor()
            #                 sql = "UPDATE " + "illegal_sites" + " SET is_reported = ? WHERE main_url = ?"
            #                 cur.execute(sql, (True, url))
            #                 conn.commit()
            #             except:
            #                 print(">>> " )
            #
            #
            #             accessible_illegal += 1
            #             # Title, Site Available-True 입력하는 sql 코드
            #
            #             cur = conn.cursor()
            #             sql = " UPDATE " + "illegal_sites" + " SET title = ?, site_available = ? WHERE main_url = ?"
            #             cur.execute(sql, (title, True, url))
            #             conn.commit()
            #
            #     context.close()
            #     browser.close()
            #
            # except Exception as e:
            #     context.close()
            #     browser.close()
            #
            #     unaccessible += 1
            #
            #     print(">>> [Result] Second Trial Failed")
            #     print(">>> [Unavailable URL]", url, "will be given 'FALSE'")
            #     # print("error:", e)
            #
            #     #site available 0 주는 sql 코드
            #     cur = conn.cursor()
            #     sql = " UPDATE " + "illegal_sites" + " SET site_available = ? WHERE main_url = ?"
            #     cur.execute(sql, (False, url))
            #     conn.commit()


    print("\n[Completed] Please check the overall statistic in below")
    print(">>>[전체: %d]" %len(urls), "[접속불가: %d]" %unaccessible, "[비유해사이트: %d]" %accessible_not_illegal, "[유해사이트: %d]" %accessible_illegal)

    print("\n[List of Illegal Sites]")
    for i in range(len(sql_available_urls)):
        print(">>> [URL]", sql_available_urls[i][0], "[Title]", sql_available_urls[i][1])

def main():
    urls = fetch_urls()

    with sync_playwright() as playwright:
        run(playwright, urls)

if __name__ == '__main__':
    main()