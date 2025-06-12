def feature_02_url_length(url: str) -> int:
    """
    URL의 길이를 기준으로 피싱 가능성 판단

    Returns:
        -1 : 길이 ≤ 24 (정상)
         0 : 25 ~ 75 (의심)
         1 : 76 이상 (피싱)
    """
    try:
        length = len(url)

        if length <= 24:
            return -1
        elif length <= 75:
            return 0
        else:
            return 1
    except:
        return 1  # 예외 발생 시 피싱 의심

# 테스트
if __name__ == "__main__":
    test_urls = [
        "http://short.url",                                           # → -1
        "http://medium-length-url-example.com/secure-login.html",    # → 0
        "http://very-long-domain-name-example.com/path/to/resource/with/extra/parameters/that/goes/on/and/on"  # → 1
    ]
    for url in test_urls:
        print(f"{url} → {feature_02_url_length(url)}")
