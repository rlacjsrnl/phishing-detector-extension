import requests
from bs4 import BeautifulSoup

def feature_20_on_mouseover(url: str) -> int:
    """
    HTML에 onmouseover 속성이 포함되어 있는지 검사

    Returns:
       -1 : 없음 (정상)
        1 : 사용됨 (피싱)
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        html = response.text.lower()

        if "onmouseover" in html:
            return 1
        else:
            return -1
    except:
        return 1  # 예외 발생 시 피싱 의심으로 간주

# 테스트
if __name__ == "__main__":
    test_urls = [
        "https://example.com",                      # → -1 (정상)
        "http://phishy.site.com/mouseover.html"     # → 1 (onmouseover 사용 시)
    ]
    for url in test_urls:
        print(f"{url} → {feature_20_on_mouseover(url)}")
