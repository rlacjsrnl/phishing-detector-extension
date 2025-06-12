import requests
from bs4 import BeautifulSoup

def feature_21_rightclick(url):
    """
    우클릭 차단 여부

    Returns:
       -1: 우클릭 차단 코드 없음 (정상)
        0: 우클릭 차단 흔적 있음 (의심)
    """

    try:
        response = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        html = response.text.lower()
    except Exception:
        return 0  # 요청 실패 → 보류 (의심 처리)

    # 우클릭 차단을 유추할 수 있는 문자열 패턴
    block_patterns = [
        "event.button==2",
        "oncontextmenu=\"return false\"",
        "document.oncontextmenu",
        "contextmenu"
    ]

    # 패턴이 하나라도 포함되어 있으면 의심(0)
    for pattern in block_patterns:
        if pattern in html:
            return 0

    return -1  # 차단 흔적 없음 → 정상
