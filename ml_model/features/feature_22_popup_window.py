# feature_22_popup_window.py

import requests
from bs4 import BeautifulSoup

def feature_22_popup_window(url: str) -> int:
    """
    window.open 사용 여부

    Returns:
       -1: 사용 되지 않음 (정상)
        0: window.open 사용되었거나 요청 실패 (의심)
    """
    try:
        response = requests.get(
            url, timeout=5,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        content = response.text
    except Exception:
        return 0  # 요청 실패 → 의심

    soup = BeautifulSoup(content, "lxml")
    scripts = soup.find_all("script")

    for script in scripts:
        if "window.open" in script.text.lower():
            return 0  # 실제 JS 내부에서 사용된 경우 → 의심

    return -1  # 정상
