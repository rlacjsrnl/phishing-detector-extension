def feature_05_double_slash_redirecting(url: str) -> int:
    """
    URL 내에서 추가적인 '//'가 존재하는지 확인

    Returns:
       -1 : '//'는 스킴(http://)에만 있음 (정상)
        1 : '//'가 1번 이상 더 등장 (피싱)
    """
    try:
        first_double_slash = url.find('//')
        if first_double_slash == -1:
            return -1  # '//' 자체가 없으면 정상
        
        # '//' 이후에 또 '//'가 있는지 확인
        if url.find('//', first_double_slash + 2) != -1:
            return 1
        else:
            return -1
    except:
        return 1  # 예외 발생 시 피싱 의심

# 테스트
if __name__ == "__main__":
    test_urls = [
        "https://example.com/account",           # -1 (정상)
        "http://secure-login.com//login",        # 1 (의심)
        "https://phishing-site.com/path//fake",  # 1 (의심)
        "ftp://host/file"                        # -1 (정상)
    ]
    for url in test_urls:
        print(f"{url} → {feature_05_double_slash_redirecting(url)}")
