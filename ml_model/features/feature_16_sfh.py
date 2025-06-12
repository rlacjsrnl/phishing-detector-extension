from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import requests

def feature_16_sfh(url):
    """
    Returns:
       -1: <form>이 존재하고, action이 현재 도메인과 동일 (정상)
        0: form이 없거나, action이 외부 도메인 (but 화이트리스트 아님) (의심)
        1: action이 blank, about:blank, #, javascript:void(0) 등 (피싱)
    """
    try:
        response = requests.get(url, timeout=5)
        content = response.text
    except Exception:
        return 1  # 연결 자체가 안 되면 피싱 의심

    soup = BeautifulSoup(content, "html.parser")
    forms = soup.find_all("form")

    # form이 없는 경우도 의심 처리 (기존: -1 → 변경: 0)
    if not forms:
        return 0

    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()

    # 외부 인증 또는 CDN 등의 정상 예외 도메인
    known_safe_hosts = [
        "accounts.google.com",
        "cdn.cloudflare.com",
        "auth0.com",
        "login.microsoftonline.com",
        "paypal.com"
    ]

    for form in forms:
        action = form.get("action", "").strip().lower()

        # 의심스러운 action 패턴
        if action in ["", " ", "about:blank", "#", "javascript:void(0)", "data:", "mailto:", "tel:"]:
            return 1

        # 상대경로 → 절대 URL로 변환
        full_action_url = urljoin(url, action)
        action_domain = urlparse(full_action_url).netloc.lower()

        if not action_domain:
            return 1

        if action_domain != domain:
            # 안전한 외부 도메인일 경우 예외적으로 정상 처리
            if any(k in action_domain for k in known_safe_hosts):
                return -1
            return 0  # 외부 도메인은 기본적으로 의심

    return -1  # 모든 form이 자기 도메인으로 향함 → 정상
