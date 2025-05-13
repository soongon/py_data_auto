# url : https://books.toscrape.com/
# 특정 책의 제목을 스크래핑
# 제목에 대한 css selector : #default > div > div > div > div > section > div:nth-child(2) > ol > li:nth-child(1) > article > h3 > a
# a태그의 텍스트 값
# 스크래핑 해서 콘솔에 출력하는 코드

# (필요 시) pip install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup

def scrape_first_book_title():
    url = "https://books.toscrape.com/"
    # 2. 페이지 요청
    response = requests.get(url)
    response.raise_for_status()  # 요청 실패 시 예외 발생

    # 3. HTML 파싱
    soup = BeautifulSoup(response.text, "html.parser")

    # 4. CSS Selector로 제목 추출
    selector = "#default > div > div > div > div > section > div:nth-child(2) > ol > li:nth-child(1) > article > h3 > a"
    title_tag = soup.select_one(selector)
    if not title_tag:
        print("책 제목을 찾을 수 없습니다.")
        return

    # a 태그의 텍스트 값 출력
    title = title_tag.get_text(strip=True)
    print(f"첫 번째 책 제목: {title}")

if __name__ == "__main__":
    scrape_first_book_title()
