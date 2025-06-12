import ssl
import socket
from urllib.parse import urlparse
from datetime import datetime


def feature_08_sslfinal_state(url: str) -> int:
    """
    HTTPS 사용 여부 + 인증서 유효기간을 기반으로 피싱 여부 판단

    Returns:
        -1: HTTPS + 인증서 유효기간 ≥ 365일 (정상)
         0: HTTPS + 유효기간 < 365일 (의심)
         1: HTTPS 아님 or 인증서 확인 실패 (피싱)
    """
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname
        port = 443

        # HTTPS가 아닌 경우
        if parsed.scheme != "https":
            return 1

        # 인증서 확인
        ctx = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        # 유효기간 계산
        not_before = datetime.strptime(cert['notBefore'], "%b %d %H:%M:%S %Y %Z")
        not_after = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
        duration = (not_after - not_before).days

        if duration >= 365:
            return -1  # 신뢰할 수 있는 HTTPS
        else:
            return 0   # 짧은 인증서 기간 → 의심
    except Exception:
        return 1  # 인증서 확인 실패 → 피싱 의심
