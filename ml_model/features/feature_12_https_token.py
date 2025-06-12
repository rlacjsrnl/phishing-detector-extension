from urllib.parse import urlparse

def feature_12_https_token(url: str) -> int:
    """
    도메인에 'https' 문자열이 포함되어 있는지 여부

    Returns:
       -1 : 포함되지 않음 (정상)
        1 : 포함됨 (피싱)
    """
    try:
        domain = urlparse(url).netloc.lower()
        # www 제거
        if domain.startswith("www."):
            domain = domain[4:]

        return 1 if "https" in domain else -1
    except:
        return 1  # 오류 발생 시 피싱으로 간주

# 테스트
if __name__ == "__main__":
    test_urls = [
        "http://https-login.example.com",  # → 1 (의심)
        "https://secure.example.com",      # → -1 (정상)
        "http://login.httpssecurity.net",  # → 1 (의심)
        "https://example.com"              # → -1 (정상)
    ]
    for url in test_urls:
        print(f"{url} → {feature_12_https_token(url)}")
