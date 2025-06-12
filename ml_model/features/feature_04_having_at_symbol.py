def feature_04_having_at_symbol(url: str) -> int:
    """
    URL에 '@' 문자가 포함되어 있는지 검사

    Returns:
       -1 : 포함되지 않음 (정상)
        1 : 포함됨 (피싱)
    """
    try:
        return 1 if '@' in url else -1
    except:
        return 1  # 예외 발생 시 보수적으로 피싱 처리

# 테스트
if __name__ == "__main__":
    test_urls = [
        "https://user@phishing.com",    # → 1 (피싱 의심)
        "https://secure.example.com",   # → -1 (정상)
        "http://test.com/path@file",    # → 1 (의심)
        "https://example.com"           # → -1 (정상)
    ]
    for url in test_urls:
        print(f"{url} → {feature_04_having_at_symbol(url)}")
