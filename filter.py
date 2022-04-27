from playwright.sync_api import Playwright, sync_playwright, expect
import sqlite3
import re


def fetch_urls():
    conn = sqlite3.connect("illegals.db")
    cur = conn.cursor()
    cur.execute("SELECT main_url from illegal_sites")
    row = cur.fetchall()
    url_raw = re.findall(
        'http[s]?://(?:[a-zA-Z-ㄱ-ㅣ가-힣]|[0-9]|[$\-@\.&+:/?=_&;]|[!*\(\),]|(?:%[0-9a-fA-F-ㄱ-ㅣ가-힣][0-9a-fA-F-ㄱ-ㅣ가-힣]))+',
        str(row))

    return url_raw

def filtering(title):

    white_list = ["불법·유해정보사이트에 대한 차단 안내", "판매", "용품", "Domain", "Apache2, IIS", "WordPress", "warning", "쿠팡", "404"]

    illegal_keywords = ['무료웹툰', '유료웹툰', '성인웹툰', 'BL웹툰', '미리보기', '인기웹툰 미리보기', '웹툰툰플릭스', '툰플릭스웹툰', '웹툰순위', '웹툰미리보기', '네이버웹툰',
                        '다음웹툰', '웹툰사이트', '레진코믹스', '19웹툰', '유료회차', '무료만화', '유료만화', '만화', '망가', '인기웹툰', '웹툰무료보기',
                        '웹툰미리보기사이트', '네이버웹툰미리보기', '밤토끼', '툰코', '호두코믹스', '웹툰', '포토툰', '만화미리보기', '짬툰', '탑툰', '썰만화',
                        '썰툰', '야한웹툰', '섹툰보기', '레진코믹스미리보기', '웹툰장르', '꽁짜웹툰', '늑대닷컴', '펀비', '만화순위', '만화사이트', '유료', 'AV',
                        '19만화', '만화무료보기', '보기사이트', '토끼', '밤토키', '토키', '호두', '짬', 'torrent', 'TORRENT', 'Torrent',
                        '무료', '줄거리', '감독토렌트', '토렌트김', '토렌트맵', '유토파일', '보고', '다운', '마그넷', '자료', '공유', '외국영화', '무료성인', '성인사이트',
                        '한국야동', '일본', '일본노모', '노모', '망가', '유출영', '국산야동', '산야', '몰카', '무료성인사이트', '오피', 'OP', '강남오피', '선릉오피', '대전오피',
                        '대구오피', '부산오피', '인천오피', '광주오피', '울산오피', '제주오피', '부천오피', '일산오피', '분당오피', '수원오피', '천안오피', '유흥', '유흥업소', '업소',
                        '립카페', '핸플', '패티쉬', '휴게', '휴게텔', '키스', '키스방', '안마', '공유사이트', '가이드오피무료', '일본야동', '서양야동', '벗방', '야동토렌트', '동토',
                        '야설', '야사', '성인', '비아그라', '바나나몰', '리얼돌', '야동', '오르가즘', '업소', "먹튀", "토토", "도박", "꽁머니", "스포츠", "배팅", "보증금", "파워볼",
                        "놀이터", '코드', '고액', '고액', '배당', '가입코드', '배당', '가입코드', '게임', '매충', '국내배당', '지급', '배팅', '보증', '포커', '경기', '천만원고액전용',
                        '제재', '인플레이', '진행', '환전', '미니게임', '스포츠상한', '매출', '무제', '유럽식', '검증', '충전', '머니', '유럽식스포츠', '쿠폰', '그램', '보증업체', '라이브포커', '호텔카지노',
                        '총판', '제한', '토토', '핸디캡', '스포츠주소', '총판문의', '추천인', '오버가능', '보너스', '베팅', '상품', '업계', '단폴', '입금', '스포츠배팅', '파워볼', '라이센스', '상한가',
                        '가입머니', '보증금', '전세계', '먹튀검증', '고액전용노리터', '중계', '배팅가능', '바카라', '도박', '수익', "다시보기", "드라마", "티비", "스트리밍", "토렌트", "링크", "최신주소",
                        "현재주소", "무료웹툰사이트", "먹튀검증사이트", "영화무료사이트", '링크모음', '주소']

    light_illegal_keywords = ['웹툰', '미리보기', '19', '유료', '무료', '망가', '인기', '만화', '썰', '순위',
                              '다시보기', '드라마', '티비', '스트리밍', '링크', 'streaming',
                              '최신', '주소', '토렌트', 'torrent', '줄거리', '공유', '영화', '성인', 'av', '야동', '노모', '일본', '유출', '국산', '몰카',
                              '오피', 'op', '안마', '유흥', '업소', '키스', '벗방',
                              '토토', '도박', '머니', '스포츠', '베팅', '코드', '고액', '배당', '가입', '매충', '지급', '보증', '포커', '경기', '카지노', '유럽',
                              '환전', '유럽', '중계', '머니', '바카라', '먹튀'
                              '토끼', '툰코', '호두코믹스', '포토툰', '늑대닷컴', '펀비']

    cnt = 0
    match_result = []

    for keyword in light_illegal_keywords:
        if keyword in title:
            cnt += 1
            match_result.append(keyword)

    print(">>> [Verification] Title:", title)
    print(">>> [Result] Match Count: [%d]" % cnt, "Match With", match_result)
    #print("Title:", title, "match count:", cnt, "match with", match_result)

    return cnt

#dgb-toon3.site - 이 웹 사이트는 판매용입니다! - dgb toon3 자료와 정보
#불법·유해정보사이트에 대한 차단 안내

def temp(playwright: Playwright, urls):

    sql_available_urls = []

    unaccessible = 0 #status != 200
    accessible_not_illegal = 0 #status = 200 & 유해사이트 아님
    accessible_illegal = 0 #status = 200 & 유해사이트인경우

    for i, url in enumerate(urls):
        try:
            print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
            print("[%d]Checking Response on:" % (i+1), url)
            print(">>> First Trial on:", url)
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context(viewport={"width": 1440, "height": 2560})

            page = context.new_page()
            response = page.goto(url, timeout=60000)
            print(">>> [Status]", response.status)
            if response.status == 200:
                print(">>> [Result] Success")
                title = page.inner_text("title")
                result = filtering(title) #1 or 0
                if result == 0:
                    print(">>> [WhiteList URL] ", url)
                    accessible_not_illegal += 1
                    #title, siteavailable False 입력하는 sql코드

                else:
                    page.wait_for_timeout(15000)
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


                    accessible_illegal += 1
                    #title과 site available이 True 입력하는 sql

            context.close()
            browser.close()

        except Exception as e:
            context.close()
            browser.close()

            try:
                print(">>> [Result] First Trial Failed")
                print(">>> Second Trial on:", url)

                browser = playwright.chromium.launch(headless=False)
                context = browser.new_context(viewport={"width": 1440, "height": 2560})

                page = context.new_page()
                page.wait_for_timeout(5000)
                response = page.goto(url, timeout=60000)
                print(">>> [Status]", response.status)
                if response.status == 200:
                    title = page.inner_text("title")
                    result = filtering(title)
                    if result == 0:
                        print(">>> [WhiteList URL] ", url)
                        # title과 Site Available False 주기
                    else:
                        # True인 애들
                        page.wait_for_timeout(15000)
                        sql_available_urls.append([url, title])
                        print(">>> [Available URL]:", "Title:", title)

                        if 'http://' in url:
                            url_go = re.sub(pattern='http://', repl='', string=url)
                            page.screenshot(path=f'./screenshot/{url_go}.png', full_page=False)
                            print('>>> [Screenshot Success]:', url_go)

                        elif 'https://' in url:
                            url_go = re.sub(pattern='https://', repl='', string=url)
                            page.screenshot(path=f'./screenshot/{url_go}.png', full_page=False)
                            print('>>>screenshot success]:', url_go)

                        accessible_illegal += 1
                        # Title, Site Available-True 입력하는 sql 코드

                context.close()
                browser.close()

            except Exception as e:
                context.close()
                browser.close()

                unaccessible += 1

                print(">>> [Result] Second Trial Failed")
                print(">>> [Unavailable URL]", url, "will be given 'FALSE'")
                print("error:", e)
                
                #site available 0 주는 sql 코드

    for i in range(len(sql_available_urls)):
        print("URL:", sql_available_urls[i][0], "Title:", sql_available_urls[i][1])

    print("done")

def main():
    urls = fetch_urls()

    with sync_playwright() as playwright:
        temp(playwright, urls)

if __name__ == '__main__':
    main()