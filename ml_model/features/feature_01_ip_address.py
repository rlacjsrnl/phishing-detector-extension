import re
from urllib.parse import urlparse


def feature_01_ip_address(url: str) -> int:
    """
    URL에 도메인 대신 IP 주소가 포함되어 있으면 피싱 가능성 높음

    Returns: 
       -1 : 일반 도메인일 경우 (정상)
        1 : 호스트명이 IP 주소일 경우 (피싱)
    """
    try:
        hostname = urlparse(url).netloc.split(':')[0]

        # IPv4 정규식
        ipv4_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')

        # IPv6 정규식 (대괄호 제거 후 검사)
        ipv6_pattern = re.compile(r'^([0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}$')

        if ipv4_pattern.match(hostname) or ipv6_pattern.match(hostname.replace('[', '').replace(']', '')):
            return 1  # IP 주소가 hostname이면 피싱 의심
        return -1
    except Exception as e:
        print(f"[F01 예외] {e}")
        return 1  # 예외 발생 시 피싱 간주


# 테스트
if __name__ == "__main__":
    test_urls = [
        "http://192.168.0.1/login",      # → 1
        "http://[2001:db8::1]/",         # → 1
        "http://example.com/192.168.0.1", # → -1
        "https://google.com"              # → -1
    ]
    for url in test_urls:
        print(f"{url} → {feature_01_ip_address(url)}")
