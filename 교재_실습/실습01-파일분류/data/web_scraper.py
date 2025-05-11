# 간단한 웹 스크래퍼
import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    """웹사이트 내용을 스크래핑하는 함수"""
    try:
        response = requests.get(url)
        response.raise_for_status()  # 오류 발생시 예외 발생
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 제목 가져오기
        title = soup.title.text if soup.title else "제목 없음"
        
        # 모든 링크 가져오기
        links = [a.get('href') for a in soup.find_all('a') if a.get('href')]
        
        # 모든 단락 텍스트 가져오기
        paragraphs = [p.text for p in soup.find_all('p')]
        
        return {
            "title": title,
            "links": links,
            "paragraphs": paragraphs
        }
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    result = scrape_website("https://www.example.com")
    print(f"웹사이트 제목: {result.get('title')}")
    print(f"찾은 링크 수: {len(result.get('links', []))}")
    print(f"찾은 단락 수: {len(result.get('paragraphs', []))}")
