# 1. 랜딩 페이지 : https://webscraper.io/test-sites/e-commerce/allinone
# 2. 링크를 클릭 : #side-menu > li.nav-item.active > a
# 3. 링크를 클릭 : #side-menu > li.nav-item.active > ul > li:nth-child(2) > a

# 플레이라이트를 사용해서 위 순서대로 액션을 진행한다.
# 첫번째상품의 이름 : body > div.wrapper > div.container.test-site > div > div.col-lg-9 > div.row > div:nth-child(1) > div > div > div.caption > h4:nth-child(2) > a
# 콘솔에 출력하는 파이썬 코드

# 최대한 심플하게 작성, 향후 고도화 예정
# 각 액션 단계별로 확인할수 있게 헤드레스모드 해제하고 3초씩 쉰다.
from playwright.sync_api import sync_playwright
import time

URL = "https://webscraper.io/test-sites/e-commerce/allinone"
MAIN_MENU = "#side-menu > li:nth-child(2) > a"
SUB_MENU  = "#side-menu > li.nav-item.active > ul > li:nth-child(2) > a"
PRODUCT   = (
    "body > div.wrapper > div.container.test-site > div > "
    "div.col-lg-9 > div.row > div:nth-child(1) > div > "
    "div > div.caption > h4:nth-child(2) > a"
)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # 1) 랜딩 페이지 이동
    page.goto(URL, wait_until="networkidle")
    time.sleep(3)

    # 2) 첫 번째 메뉴 클릭
    page.wait_for_selector(MAIN_MENU, timeout=10_000)
    page.click(MAIN_MENU)
    time.sleep(3)

    # 3) 두 번째 하위 메뉴 클릭
    page.wait_for_selector(SUB_MENU, timeout=10_000)
    page.click(SUB_MENU)
    time.sleep(3)

    # 4) 첫 번째 상품 이름 추출 및 출력
    page.wait_for_selector(PRODUCT, timeout=10_000)
    print(page.locator(PRODUCT).inner_text())

    time.sleep(3)
    browser.close()


