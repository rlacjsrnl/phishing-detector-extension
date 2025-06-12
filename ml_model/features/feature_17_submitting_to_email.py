import requests
from bs4 import BeautifulSoup

def feature_17_submitting_to_email(url: str) -> int:
    """
    mailto 사용 여부
    
    Returns:
    -1 : mailto 없음 (정상)
     0 : mailto 있음 또는 요청 실패 (의심)
    """
    try:
        response = requests.get(
            url,
            timeout=5,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        content = response.text
    except Exception:
        return 0  # 요청 실패는 의심 처리

    soup = BeautifulSoup(content, "lxml")
    forms = soup.find_all("form")

    for form in forms:
        action = form.get("action", "")
        if "mailto:" in action.lower():
            return 0  # 이메일 전송 시도는 의심 처리

    return -1  # 정상