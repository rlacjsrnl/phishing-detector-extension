import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

def feature_15_links_in_tags(url: str) -> int:
    """
    <meta>, <script>, <link> 태그에서 외부 도메인 링크 비율 계산

    Returns:
        -1: 외부 링크 비율 < 17% (정상)
         0: 17% ≤ 비율 ≤ 81% (의심)
         1: 비율 > 81% (피싱)
    """
    try:
        domain = urlparse(url).netloc.lower()
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        tags = []

        # <meta>에 포함된 URL (예: http-equiv="refresh" 등)
        for tag in soup.find_all("meta"):
            if tag.get("content") and "url=" in tag.get("content").lower():
                tags.append(tag.get("content").lower().split("url=")[-1])

        # <script src="">
        for tag in soup.find_all("script"):
            if tag.get("src"):
                tags.append(tag.get("src"))

        # <link href="">
        for tag in soup.find_all("link"):
            if tag.get("href"):
                tags.append(tag.get("href"))

        if not tags:
            return -1  # 외부 링크 없으면 정상

        external_count = 0
        for tag_url in tags:
            full_url = urljoin(url, tag_url)
            parsed_tag_domain = urlparse(full_url).netloc.lower()
            if parsed_tag_domain and domain not in parsed_tag_domain:
                external_count += 1

        external_ratio = external_count / len(tags)

        if external_ratio < 0.17:
            return -1
        elif external_ratio <= 0.81:
            return 0
        else:
            return 1

    except Exception:
        return 1  # 오류 → 피싱 의심

# 테스트 예시
if __name__ == "__main__":
    test_urls = [
        "https://www.google.com",
        "https://getbootstrap.com",
        "http://suspicious-iframe-login.xyz"
    ]
    for url in test_urls:
        print(f"{url} → {feature_15_links_in_tags(url)}")
