# feature_18_abnormal_url.py

from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

def feature_18_abnormal_url(url):
    """
    외부 도메인 비율을 측정

    Returns:
       -1: 외부 도메인 비율 < 30% (정상)
        0: 요청 실패, form 없음, 외부 도메인 ≥ 30% (의심)
    """

    try:
        response = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        content = response.text
    except Exception:
        return 0  # 요청 실패 → 의심

    soup = BeautifulSoup(content, "lxml")
    forms = soup.find_all("form")

    if not forms:
        return 0  # form 없음 → 의심

    parsed_main = urlparse(url)
    page_domain = parsed_main.hostname or ""

    external_count = 0
    total_count = 0

    for form in forms:
        action = form.get("action", "").strip()
        if not action:
            continue

        parsed_action = urlparse(action)
        action_domain = parsed_action.hostname

        total_count += 1
        if action_domain and action_domain != page_domain:
            external_count += 1

    if total_count == 0:
        return 0  # action 없는 form만 있음 → 의심

    external_ratio = external_count / total_count

    if external_ratio >= 0.3:
        return 0  # 외부 도메인 비율 높음 → 의심
    else:
        return -1  # 정상
