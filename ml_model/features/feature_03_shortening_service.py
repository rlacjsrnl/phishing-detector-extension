from urllib.parse import urlparse
import re

SHORTENING_SERVICES = {
    "bit.ly", "goo.gl", "tinyurl.com", "ow.ly", "t.co", "bit.do", "adf.ly",
    "is.gd", "buff.ly", "mcaf.ee", "rebrand.ly", "shorte.st", "cutt.ly",
    "t.ly", "tiny.cc", "soo.gd", "v.gd", "yourls.org", "short.io", "s.id",
    "qr.ae", "lnkd.in", "rb.gy", "2.gp"
}

SHORT_PATH_REGEX = re.compile(r"^/[a-zA-Z0-9_-]{4,10}$")

def feature_03_shortening_service(url: str) -> int:
    """
    단축 URL 도메인 사용 여부 또는 경로 패턴으로 단축 여부 판단

    Returns:
       -1 : 일반 URL (정상)
        1 : 단축 URL 사용 (피싱)
    """
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower().strip(".")  # t.co. → t.co
        path = parsed.path

        # www, m, l, amp 등 흔한 서브도메인 제거
        domain_parts = domain.split(".")
        if len(domain_parts) > 2:
            domain = ".".join(domain_parts[-2:])

        # 1. 도메인 기반 단축 서비스
        if domain in SHORTENING_SERVICES:
            return 1

        # 2. 경로가 짧고 도메인이 단순하면 단축 가능성
        if SHORT_PATH_REGEX.match(path) and len(domain.split(".")) <= 2:
            return 1

        return -1
    except Exception as e:
        print(f"[F03 예외] {e}")
        return 1  # 예외 발생 시 피싱 처리


# 테스트
if __name__ == "__main__":
    urls = [
        "https://bit.ly/abc12",
        "https://www.tinyurl.com/xyz9",
        "https://t.co/xyz",
        "https://t.co./abc",
        "https://example.com/a1b2",
        "https://blog.example.com/path"
    ]
    for url in urls:
        print(f"{url} → {feature_03_shortening_service(url)}")
