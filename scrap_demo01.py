# 1. url : https://estudy.kitri.re.kr/usrs/eduRegMgnt/eduCrsScheduleByMonth.do
# 과정 카테고리 정보 확보
# <ul> selector - #sub > div.lnb > div > ul
# <ul> 하위의 <li> 태그내에 카테고리 데이터 css selector - #sub > div.lnb > div > ul > li:nth-child(2) > a
# 첫번째 li 태그는 타이틀 메타데이터이고 두번째 li 부터 실제 카테고리 정보가 있음
# 카테고리 정보를 콘솔로 출력

import requests
from bs4 import BeautifulSoup
import re

def extract_real_url(js_text):
    """javascript:goMenu('...') 에서 실제 URL 추출"""
    match = re.search(r"goMenu\('([^']+)'", js_text)
    return match.group(1) if match else None

def main():
    url = 'https://estudy.kitri.re.kr/usrs/eduRegMgnt/eduCrsScheduleByMonth.do'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(f"❌ 요청 실패: {res.status_code}")
        return

    soup = BeautifulSoup(res.text, 'html.parser')

    # <ul> 태그 선택
    ul = soup.select_one('#sub > div.lnb > div > ul')
    if not ul:
        print("❌ <ul> 카테고리 리스트를 찾을 수 없습니다.")
        return

    # <li> 목록 추출 (0번은 '전체과정' 메타, 1번부터 카테고리)
    li_tags = ul.find_all('li')[1:]

    print("📚 과정 카테고리 목록:")
    for li in li_tags:
        a_tag = li.find('a')
        if a_tag and 'href' in a_tag.attrs:
            title = a_tag.get_text(strip=True)
            js_href = a_tag['href']
            real_url = extract_real_url(js_href)
            print(f"- {title} → {real_url}")

if __name__ == '__main__':
    main()
