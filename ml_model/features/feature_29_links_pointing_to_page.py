import requests
import time
import random
from urllib.parse import quote

def feature_29_links_pointing_to_page(url: str) -> int:
    """
    Bing 검색에서 'inbody:{url}'로 링크 수를 추정

    Returns:
        -1 : 링크 수 >= 2 (정상)
         1 : 링크 수 < 2 or 검색 실패 (피싱)
    """
    try:
        time.sleep(random.uniform(1.0, 2.0))  # 차단 방지용 딜레이

        query = f'inbody:"{url}"'
        search_url = f"https://www.bing.com/search?q={quote(query)}"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        res = requests.get(search_url, headers=headers, timeout=5)
        html = res.text.lower()

        # 간단한 방식: 검색결과가 2개 이상인지 파악
        if "1 result" in html or "0 result" in html:
            return 1
        elif "2 results" in html or "3 results" in html or "about" in html:
            return -1
        else:
            return 1  # 결과 불확실 시 피싱 간주
    except:
        return 1

# 테스트
if __name__ == "__main__":
    test_urls = [
        "https://www.google.com",
        "http://new-fake-login.xyz"
    ]
    for url in test_urls:
        print(f"{url} → {feature_29_links_pointing_to_page(url)}")
