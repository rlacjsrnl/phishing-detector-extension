import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def feature_13_request_url(url: str) -> int:
    """
    웹페이지에서 불러오는 리소스 (이미지, 오디오, 임베드 등) 중 외부 URL 비율 측정

    Returns:
        -1: 외부 요청 비율 < 22% (정상)
         0: 22% ~ 61% (의심)
         1: > 61% (피싱)
    """
    try:
        domain = urlparse(url).netloc.lower()
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')

        tags = soup.find_all(['img', 'audio', 'embed', 'iframe'])
        if not tags:
            return -1  # 리소스 없으면 정상으로 간주

        total, external = 0, 0
        for tag in tags:
            src = tag.get('src')
            if not src:
                continue
            full_url = urljoin(url, src)
            src_domain = urlparse(full_url).netloc.lower()
            total += 1
            if domain not in src_domain:
                external += 1

        ratio = external / total

        if ratio < 0.22:
            return -1
        elif ratio <= 0.61:
            return 0
        else:
            return 1

    except Exception:
        return 1  # 오류 발생 시 피싱 의심 처리

# 테스트
if __name__ == "__main__":
    test_urls = [
        "https://www.wikipedia.org",   # 리소스 대부분 자사 도메인일 것 → -1 또는 0
        "https://bit.ly/3nP0K4v"       # 리디렉션/외부 요소 많을 가능성 → 1
    ]
    for url in test_urls:
        print(f"{url} → {feature_13_request_url(url)}")
