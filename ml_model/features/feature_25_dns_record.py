import socket
import whois
from urllib.parse import urlparse
import time
from dateutil import parser

# WHOIS 요청 timeout 제한 (5초)
socket.setdefaulttimeout(5)


def safe_whois(domain, retries=0, delay=2):
    for i in range(retries):
        try:
            return whois.whois(domain)
        except Exception as e:
            error_msg = str(e).splitlines()[0]  # 첫 줄만 출력
            print(f"[WHOIS 재시도 {i+1} - {domain}] 실패 → {error_msg}")
            time.sleep(delay)
    return None


def feature_25_dns_record(url: str) -> int:
    """
    DNS 조회와 WHOIS 조회가 모두 실패하면 피싱으로 간주

    Returns:
        -1 : DNS or WHOIS 조회 성공 (정상)
         1 : 둘 다 실패 (피싱)
    """
    try:
        domain = urlparse(url).netloc.split(":")[0]

        # DNS 조회 시도 (IP 확인)
        socket.gethostbyname(domain)
        return -1  # DNS 성공 → 정상
    except:
        try:
            # DNS 실패했지만 WHOIS는 될 수도 있음
            result = safe_whois(domain)
            if result is not None:
                if isinstance(result.creation_date, str):
                    result.creation_date = parser.parse(result.creation_date)
                return -1
            return 1
        except Exception as e:
            print(f"[WHOIS 예외 - {domain}] {e}")
            return 1  # 둘 다 실패 → 피싱 가능성


# 테스트
if __name__ == "__main__":
    test_urls = [
        "https://google.com",             # → -1 (정상)
        "http://nonexistentdomain.abcde"  # → 1 (DNS, WHOIS 모두 실패)
    ]
    for url in test_urls:
        print(f"{url} → {feature_25_dns_record(url)}")