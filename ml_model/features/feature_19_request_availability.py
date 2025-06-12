import requests

def feature_19_request_availability(url):
    """
    단순 요청 성공 여부

    Returns:
       -1: 요청 성공 (접속 가능) (정상)
        1: 요청 실패 (접속 불가) (피싱)
    """
    try:
        requests.get(
            url,
            timeout=5,
            allow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        return -1  # 접속 성공
    except Exception:
        return 1   # 접속 실패 → 피싱 가능성
