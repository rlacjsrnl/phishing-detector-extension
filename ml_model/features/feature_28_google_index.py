import requests
import time
import random
from urllib.parse import quote, urlparse

# 클래스 정의
NORMAL = -1      # 색인되어 있음 → 정상
PHISHING = 1     # 색인 안됨 or 요청 실패 → 피싱 가능성

def feature_28_google_index(url: str) -> int:
    """
    Google Index 여부 (Bing 사용)

    설명:
    - site:{도메인}으로 Bing 검색 수행
    - 결과가 있으면 색인된 것으로 간주 → 정상(-1)
    - 결과 없음 or 요청 실패 → 피싱(1)

    기준:
    - "there are no results", "찾을 수 없습니다" → 피싱
    - "results", "<ol id=\"b_results\">" → 색인됨 (정상)
    - 그 외는 보수적으로 피싱 처리
    """

    try:
        time.sleep(random.uniform(1.0, 2.0))  # 크롤링 차단 방지용 딜레이

        domain = urlparse(url).netloc
        query = f'site:{domain}'
        search_url = f"https://www.bing.com/search?q={quote(query)}"

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

        response = requests.get(search_url, headers=headers, timeout=5)
        html = response.text.lower()

        # 색인 여부 판별
        if "there are no results" in html or "찾을 수 없습니다" in html:
            return PHISHING
        elif "results" in html or "<ol id=\"b_results\">" in html:
            return NORMAL
        else:
            return PHISHING

    except requests.exceptions.RequestException:
        return PHISHING
    except Exception:
        return PHISHING


# 테스트 예시
if __name__ == "__main__":
    test_urls = [
        "https://google.com",                      # 정상
        "https://wikipedia.org",                   # 정상
        "https://thisdoesnotexist-abc1234.xyz",    # 피싱 가능성
    ]

    for url in test_urls:
        result = feature_28_google_index(url)
        label = {NORMAL: "정상", PHISHING: "피싱"}.get(result, "Unknown")
        print(f"{url} → {result} ({label})")
