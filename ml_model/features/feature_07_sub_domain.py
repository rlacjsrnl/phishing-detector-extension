from urllib.parse import urlparse

def feature_07_sub_domain(url: str) -> int:
    """
    도메인 내 서브도메인 개수에 따라 피싱 여부 판단

    Returns:
        -1 : 서브도메인 ≤ 1 (정상)
         0 : 서브도메인 = 2 (의심)
         1 : 서브도메인 ≥ 3 (피싱)
    """
    try:
        domain = urlparse(url).netloc
        # 포트 번호 제거 (예: example.com:443)
        domain = domain.split(':')[0]

        # 서브도메인 수 계산
        dot_count = domain.count('.')
        if dot_count <= 1:
            return -1
        elif dot_count == 2:
            return 0
        else:
            return 1
    except:
        return 1  # 예외 발생 시 보수적으로 피싱 간주

# 테스트
if __name__ == "__main__":
    test_urls = [
        "https://example.com",                    # -1 (정상)
        "https://www.example.com",                # -1 (정상, www만 있음)
        "https://login.example.com",              # 0 (의심)
        "https://secure.login.example.com",       # 1 (피싱 가능성)
        "https://a.b.c.d.e.com"                   # 1 (서브도메인 많음)
    ]
    for url in test_urls:
        print(f"{url} → {feature_07_sub_domain(url)}")
