# url : https://books.toscrape.com/
# 특정 책의 제목들을 스크래핑
# ol > li 형태도 목록이 되어 있음
# ol 의 selector : #default > div > div > div > div > section > div:nth-child(2) > ol
# - 제목에 대한 css selector : #default > div > div > div > div > section > div:nth-child(2) > ol > li:nth-child(1) > article > h3 > a
# - 책커버 이미지 url : #default > div > div > div > div > section > div:nth-child(2) > ol > li:nth-child(1) > article > div.image_container > a > img (src 속성)
# - 평점 : 보류
# - 가격 : #default > div > div > div > div > section > div:nth-child(2) > ol > li:nth-child(1) > article > div.product_price > p.price_color
# - 재고여부 : #default > div > div > div > div > section > div:nth-child(2) > ol > li:nth-child(1) > article > div.product_price > p.instock.availability
# 5갸지 데이터를 처음에 순번(1부터 시작)을 포함하여 6개 컬럼으로 표형 데이터를 만들어서
# 페이징 처리는 하지 않음
# 콘솔에 내용을 출력하는 파이썬 코드
# (필요 시) pip install requests beautifulsoup4 pandas openpyxl

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
books_scraper.py

퇴임 5년 앞둔 빨대부장님도 보실 유지보수용 스크래퍼.
GitHub에 바로 올려도 되는 가독성·모듈화·로그 관리된 코드입니다.
"""

import logging
import re
from pathlib import Path
from typing import List, Dict

import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.compat import urljoin

# ─── 설정 상수 ────────────────────────────────────────────────────────────
BASE_URL    = "https://books.toscrape.com/"
MAX_PAGES   = 50
OUTPUT_FILE = Path(__file__).parent / "all_books.xlsx"
USER_AGENT  = "MaintenanceBot/1.0 (+https://github.com/your_org/your_repo)"
# ─────────────────────────────────────────────────────────────────────────

# ─── 로깅 설정 ────────────────────────────────────────────────────────────
logging.basicConfig(
    level    = logging.INFO,
    format   = "[%(levelname)s] %(asctime)s - %(message)s",
    datefmt  = "%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)
# ─────────────────────────────────────────────────────────────────────────

def fetch_page(session: requests.Session, page_num: int) -> BeautifulSoup:
    """
    주어진 페이지 번호의 HTML을 가져와 BeautifulSoup 객체로 반환한다.
    404를 만나면 ValueError를 발생시킨다.
    """
    if page_num == 1:
        url = BASE_URL
    else:
        url = urljoin(BASE_URL, f"catalogue/page-{page_num}.html")

    logger.info(f"Scraping page {page_num}: {url}")
    resp = session.get(url)
    if resp.status_code == 404:
        raise ValueError(f"Page {page_num} not found (404)")
    resp.raise_for_status()
    resp.encoding = "utf-8"
    return BeautifulSoup(resp.text, "html.parser")


def parse_books(soup: BeautifulSoup, seq_start: int) -> List[Dict]:
    """
    BeautifulSoup 객체에서 책 리스트를 파싱해
    순번(seq), 제목, 이미지URL, 평점, 가격(숫자), 재고여부를 딕셔너리 리스트로 반환.
    """
    items = soup.select(
        "#default > div > div > div > div > section > div:nth-child(2) > ol > li"
    )
    results = []

    for item in items:
        title = item.select_one("article > h3 > a").get_text(strip=True)
        img_rel = item.select_one("article > div.image_container > a > img")["src"]
        img_url = urljoin(BASE_URL, img_rel)

        # 평점 보류
        rating = "–"

        price_text = item.select_one(
            "article > div.product_price > p.price_color"
        ).get_text(strip=True)
        clean_price = float(re.sub(r"[^\d.]", "", price_text))

        availability_text = item.select_one(
            "article > div.product_price > p.instock.availability"
        ).get_text(strip=True)
        in_stock = "In stock" in availability_text

        results.append({
            "No": seq_start,
            "제목": title,
            "이미지URL": img_url,
            "평점": rating,
            "가격(숫자)": clean_price,
            "재고여부(Boolean)": in_stock
        })
        seq_start += 1

    return results


def save_to_excel(data: List[Dict], output_path: Path) -> None:
    """
    데이터 리스트를 pandas DataFrame으로 변환해 Excel 파일로 저장.
    """
    logger.info(f"Saving {len(data)} records to '{output_path}'")
    df = pd.DataFrame(data)
    df.to_excel(output_path, index=False)
    logger.info("Excel 저장 완료")


def main():
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    all_books = []
    seq = 1

    for page in range(1, MAX_PAGES + 1):
        try:
            soup = fetch_page(session, page)
        except ValueError as ve:
            logger.warning(str(ve) + " — 크롤링 종료")
            break
        except requests.HTTPError as he:
            logger.error(f"HTTP error on page {page}: {he}")
            break

        books = parse_books(soup, seq)
        all_books.extend(books)
        seq += len(books)

    if all_books:
        save_to_excel(all_books, OUTPUT_FILE)
    else:
        logger.warning("수집된 데이터가 없습니다.")

if __name__ == "__main__":
    main()
