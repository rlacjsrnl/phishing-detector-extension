from urllib.parse import urlparse

BLACKLIST_PATH = "data/blacklist.txt"

# 블랙리스트 로딩
try:
    with open(BLACKLIST_PATH, "r") as f:
        blacklisted = set(line.strip().lower() for line in f if line.strip())
except FileNotFoundError:
    blacklisted = set()

def feature_30_statistical_report(url: str) -> int:
    """
    URL의 도메인 또는 IP가 블랙리스트에 포함되어 있는지 단순 비교

    Returns:
       -1 : 정상
        1 : 블랙리스트 일치 (피싱)
    """
    try:
        netloc = urlparse(url).netloc.split(":")[0].lower()
        return 1 if netloc in blacklisted else -1
    except:
        return 1  # 예외 발생 시 보수적으로 피싱 간주

# 테스트
if __name__ == "__main__":
    test_urls = [
        "http://malicious-phish.xyz",
        "http://47.119.189.207:8888",
        "https://google.com"
    ]
    for url in test_urls:
        print(f"{url} → {feature_30_statistical_report(url)}")
