from playwright.sync_api import sync_playwright

URL = "https://news.naver.com/section/105"
SELECTOR = "#_SECTION_HEADLINE_LIST_hv1tj > li:nth-child(1) > div > div > div.sa_text > a > strong"
UA_STRING = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/136.0.0.0 Safari/537.36"
)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    # 1) user_agent 교체
    context = browser.new_context(user_agent=UA_STRING)
    page = context.new_page()

    # 2) 페이지 완전 로드 대기
    page.goto(URL, wait_until="networkidle")
    # 3) 셀렉터 등장 대기
    page.wait_for_selector(SELECTOR, timeout=10_000)

    # 4) 텍스트 추출 및 출력
    title = page.locator(SELECTOR).inner_text()
    print(title)

    browser.close()

