import requests

# 클래스 정의: 의미 명확하게 정리
NORMAL = -1       # 응답 정상 (200~399)
SUSPICIOUS = 0    # 요청 실패 (timeout, DNS 실패 등)
PHISHING = 1      # 응답 비정상 (403, 404, 503 등 → 실제 피싱 가능성 높음)

def feature_26_web_traffic(url: str) -> int:
    """
    응답 상태 및 실패 여부

    Returns:
        -1: 응답 상태 200~399 (정상)
         0: 요청 실패 → 타임아웃, DNS 실패 등 (의심)
         1: 응답은 왔지만 상태 코드가 비정상 (피싱)
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=3)
        if 200 <= response.status_code < 400:
            return NORMAL
        else:
            return PHISHING  # 정밀도 97.56% → 실제 피싱 가능성 높음
    except requests.exceptions.RequestException:
        return SUSPICIOUS  # 정밀도 낮음 (66%) → 의심

# 테스트 예시
if __name__ == "__main__":
    urls = [
        "https://www.google.com",               # 정상
        "http://thisdomaindoesnotexist.tld",    # 실패 (DNS 오류)
        "https://httpstat.us/403",              # 응답 있음, 비정상 코드
        "https://www.naver.com",
    ]
    for url in urls:
        result = feature_26_web_traffic(url)
        label = {NORMAL: "정상", SUSPICIOUS: "의심", PHISHING: "피싱"}.get(result, "Unknown")
        print(f"{url} → {result} ({label})")
