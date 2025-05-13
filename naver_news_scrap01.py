
# 1. url : https://news.naver.com/section/105

# 2. 첫번째 단계 - 뉴스 헤드라인 5개.. 스크랩
# 뉴스 헤드라인의 css셀렉터 - #_SECTION_HEADLINE_LIST_7mn9y > li:nth-child(1) > div > div > div.sa_text > a > strong
# 헤드라인 5개를 나열하기 위한 <ul>태그의 css 셀렉터 - #_SECTION_HEADLINE_LIST_7mn9y
# 3. 출력은 헤드라인 제목 5개를 콘솔에 출력

import requests
from bs4 import BeautifulSoup

def main():
    url = 'https://news.naver.com/section/105'  # IT/과학 섹션
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    res = requests.get(url, headers=headers)
    print(res.text)
    if res.status_code != 200:
        print(f"❌ 요청 실패: {res.status_code}")
        return

    soup = BeautifulSoup(res.text, 'html.parser')

    # 헤드라인 리스트 추출
    ul = soup.select_one('#_SECTION_HEADLINE_LIST_7mn9y')
    if not ul:
        print("❌ 헤드라인 리스트를 찾을 수 없습니다.")
        return

    # li 항목 5개 추출
    items = ul.select('li')[:5]

    print("📌 최신 IT 헤드라인:")
    for idx, item in enumerate(items, start=1):
        title_tag = item.select_one('div.sa_text > a > strong')
        if title_tag:
            print(f"{idx}. {title_tag.get_text(strip=True)}")
        else:
            print(f"{idx}. 제목을 찾을 수 없음")

if __name__ == '__main__':
    main()
