import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

def feature_10_favicon(url: str) -> int:
    """
    favicon URL이 현재 도메인과 다르면 피싱 가능성 있음

    Returns:
        -1: 파비콘이 같은 도메인 (정상)
         1: 파비콘이 외부 도메인 (피싱)
    """
    try:
        parsed_url = urlparse(url)
        base_domain = parsed_url.netloc.lower()

        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        icon_tags = soup.find_all("link", rel=lambda x: x and "icon" in x.lower())
        icon_urls = []

        for tag in icon_tags:
            href = tag.get("href")
            if href:
                full_url = urljoin(url, href)
                icon_urls.append(full_url)

        # 기본 favicon 경로도 포함
        icon_urls.append(urljoin(url, "/favicon.ico"))

        for icon_url in icon_urls:
            icon_domain = urlparse(icon_url).netloc.lower()
            if base_domain not in icon_domain:
                return 1  # 외부 도메인에서 favicon 불러옴 → 피싱 가능성

        return -1  # 모두 같은 도메인 → 정상
    except:
        return 1  # 오류 발생 시 피싱 의심 처리

# 테스트
if __name__ == "__main__":
    test_urls = [
        "https://www.google.com",          # 정상
        "https://suspicious-site.com",     # 피싱 가능성
    ]
    for url in test_urls:
        print(f"{url} → {feature_10_favicon(url)}")
