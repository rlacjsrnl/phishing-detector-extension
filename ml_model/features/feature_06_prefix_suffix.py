from urllib.parse import urlparse

def feature_06_prefix_suffix(url: str) -> int:
    """
    도메인 내 하이픈(-) 개수 기준 피싱 여부 판단

    Returns:
        -1 : 하이픈 없음 (정상)
         0 : 하이픈 1~2개 (의심)
         1 : 하이픈 3개 이상 (피싱)
    """
    try:
        domain = urlparse(url).netloc.lower().split(":")[0]  # 포트 제거
        if domain.startswith("www."):
            domain = domain[4:]

        hyphen_count = domain.count("-")

        if hyphen_count == 0:
            return -1
        elif hyphen_count <= 2:
            return 0
        else:
            return 1
    except Exception as e:
        print(f"[F06 예외] {e}")
        return 1


# 테스트
if __name__ == "__main__":
    urls = [
        "https://example.com",               # -1
        "https://www.my-bank-login.com",    # 1
        "https://safe-test.net",            # 0
        "http://abc-def-ghi-jkl.com",       # 1
        "http://localhost:8080/test"         # -1
    ]
    for url in urls:
        print(f"{url} → {feature_06_prefix_suffix(url)}")
