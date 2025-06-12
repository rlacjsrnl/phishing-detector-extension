# feature_23_iframe.py

import requests
from bs4 import BeautifulSoup

def feature_23_iframe(url: str) -> int:
    """
    IFrame 존재 여부 및 숨김 여부 판단

    Returns:
       -1: 정상 iframe이거나 없음 (정상)
        0: 숨겨진 iframe 존재 또는 요청 실패 (의심)
    """
    try:
        response = requests.get(
            url, timeout=5,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        content = response.text
    except Exception:
        return 0  # 요청 실패 → 의심 처리

    soup = BeautifulSoup(content, "lxml")
    iframes = soup.find_all("iframe")

    for iframe in iframes:
        style = iframe.get("style", "").lower()
        width = iframe.get("width", "")
        height = iframe.get("height", "")

        # 숨김 iframe 판단 조건
        if (
            "display:none" in style
            or "visibility:hidden" in style
            or width in ("0", "0px")
            or height in ("0", "0px")
        ):
            return 0  # 숨겨진 iframe → 의심

    return -1  # 모두 정상 iframe이거나 없음
