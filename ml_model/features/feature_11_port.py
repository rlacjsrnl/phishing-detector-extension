from urllib.parse import urlparse

# 일반적으로 사용되는 정상 포트 목록
NORMAL_PORTS = {80, 443}

def feature_11_port(url: str) -> int:
    """
    URL에 비정상적인 포트 번호가 명시되어 있으면 피싱 가능성

    Returns:
        -1 : 기본 포트 or 정상 포트 사용 (정상)
         1 : 비정상 포트 명시 (피싱)
    """
    try:
        parsed = urlparse(url)
        port = parsed.port

        # 포트가 명시되지 않은 경우 (스킴 기본값 사용)
        if port is None:
            return -1

        return -1 if port in NORMAL_PORTS else 1
    except:
        return 1  # 파싱 오류 등은 피싱 가능성으로 처리

# 테스트
if __name__ == "__main__":
    test_urls = [
        "http://example.com",              # → -1 (80)
        "https://secure.site.com",        # → -1 (443)
        "http://phishy.site.com:8080",    # → 1 (비정상 포트)
        "https://weird.site.com:10000",   # → 1 (비정상 포트)
        "https://example.com:443"         # → -1 (정상)
    ]
    for url in test_urls:
        print(f"{url} → {feature_11_port(url)}")
