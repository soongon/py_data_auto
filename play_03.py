from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import time
import re  # ① 숫자 처리용

URL = "https://www.melon.com/chart/index.htm"

# 1) Playwright로 HTML 가져오기
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(URL, wait_until="networkidle")
    html = page.content()
    browser.close()

# 2) BeautifulSoup 파싱
soup = BeautifulSoup(html, "html.parser")
rows = soup.select('tr[id^="lst"]')

# 3) 결과 저장용 리스트 준비
data = []
for row in rows:
    # 원본 텍스트
    rank_str = row.select_one('td:nth-child(2) span.rank').get_text(strip=True)
    like_str = row.select_one('td:nth-child(8) button span.cnt').get_text(strip=True)

    # 숫자 변환
    rank_num = int(rank_str)
    like_num = int(re.sub(r'\D', '', like_str))

    data.append({
        "순위":       rank_num,
        "곡 제목":     row.select_one('td:nth-child(6) .ellipsis.rank01 a').get_text(strip=True),
        "아티스트":    row.select_one('td:nth-child(6) .ellipsis.rank02 a').get_text(strip=True),
        "앨범명":      row.select_one('td:nth-child(7) div a').get_text(strip=True),
        "좋아요":      like_num,
        "이미지 URL":  row.select_one('td:nth-child(4) a img')['src']
    })

# 4) DataFrame 생성 후 엑셀 저장
df = pd.DataFrame(data)
df.to_excel("melon_chart.xlsx", index=False)

print("✅ melon_chart.xlsx 파일로 저장 완료!")


# 현재 페이지의 멜론 차트 100곡을 스크래핑할거야
# 전체 구조가 <table> : #frm > div > table
# 하위의 <tr> : 에 곡 정보가 있어
# 스크래핑 할 정보는
# 1. 순위 : #lst50 > td:nth-child(2) > div > span.rank
# 2. 앨범 이미지 URL : #lst50 > td:nth-child(4) > div > a > img 의 src 속성
# 3. 곡 타이틀 : #lst50 > td:nth-child(6) > div > div > div.ellipsis.rank01 > span > a
# 4. 아티스트 : #lst50 > td:nth-child(6) > div > div > div.ellipsis.rank02 > a
# 5. 앨범명 : #lst50 > td:nth-child(7) > div > div > div > a
# 6. 좋아요 : #lst50 > td:nth-child(8) > div > button > span.cnt
# 위 6개 컬럼으로 표형 구조를 만들어 먼저 콘솔에 출력하는 파이썬 코드를 심플하게 작성해줘
# 위 코드를 기반으로 작성해줘 (향후 고도화 할거야)
