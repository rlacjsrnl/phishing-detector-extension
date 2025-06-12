import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def feature_14_url_of_anchor(url: str) -> int:
    """
    <a href="..."> 태그의 외부 도메인 링크 비율을 측정

    Returns:
        -1 : 외부 링크 비율 < 31% (정상)
         0 : 31% ≤ 비율 ≤ 67% (의심)
         1 : > 67% (피싱)
    """
    try:
        base_domain = urlparse(url).netloc.lower()
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')

        anchors = soup.find_all('a', href=True)
        if not anchors:
            return -1

        total, external = 0, 0
        for tag in anchors:
            href = tag['href'].strip()
            # 내부 anchor, javascript, mailto 무시
            if href.startswith('#') or href.startswith('javascript') or href.startswith('mailto:'):
                continue

            full_url = urljoin(url, href)
            href_domain = urlparse(full_url).netloc.lower()
            total += 1
            if base_domain not in href_domain:
                external += 1

        if total == 0:
            return -1  # 실질적인 링크가 없으면 정상

        ratio = external / total
        if ratio < 0.31:
            return -1
        elif ratio <= 0.67:
            return 0
        else:
            return 1

    except:
        return 1  # 오류 발생 시 피싱 의심

# 테스트
if __name__ == "__main__":
    test_urls = [
        "https://www.wikipedia.org",       # → -1
        "https://getbootstrap.com",        # → 0 또는 1
        "https://suspicious-site.com"      # → 1 가능성
    ]
    for url in test_urls:
        print(f"{url} → {feature_14_url_of_anchor(url)}")
