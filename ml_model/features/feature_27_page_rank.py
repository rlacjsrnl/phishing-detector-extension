import csv
from urllib.parse import urlparse

# Tranco 로딩
TRANKO_RANKS = {}
with open("data/tranco_1m.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        rank = int(row[0].strip())
        domain = row[1].strip().lower()
        TRANKO_RANKS[domain] = rank
        TRANKO_RANKS[f"www.{domain}"] = rank  # www. 버전도 추가

# 상수 정의
NORMAL = -1
SUSPICIOUS = 0  

# URL 정규화 함수
def normalize_url(url: str) -> str:
    """
    URL에서 스킴(https, http)과 www.를 제거하고 순수 도메인만 반환
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    if domain.startswith("www."):
        domain = domain[4:]
    return domain

def feature_27_page_rank(url: str) -> int:
    """
    Tranco 순위 기반 PageRank 피처 (2-class: 정상 vs 의심)

    Returns:
        -1: Tranco 순위 있음 (정상)
         0: 순위 없음 (의심)
    """
    try:
        domain = normalize_url(url)
        
        # 두 버전으로 탐색
        rank = TRANKO_RANKS.get(domain) or TRANKO_RANKS.get(f"www.{domain}")
        return NORMAL if rank else SUSPICIOUS
    except Exception:
        return SUSPICIOUS

# 테스트
if __name__ == "__main__":
    test_urls = [
        "https://google.com",                     # 정상
        "https://www.google.com",                 # 정상
        "https://naver.com",                      # 정상
        "https://chatgpt.com/g/g-p-67dd8eac25948191a17e794264b4b5ac-kaebseuton-dijain-pising-url-tamji-peulreogeuin/c/683dbf7a-16cc-8005-911a-20386314884e",                  # 정상
        "https://unknown-site-example.xyz",       # 의심
        "https://www.unknown-site-example.xyz"    # 의심
    ]
    for url in test_urls:
        result = feature_27_page_rank(url)
        label = {NORMAL: "정상", SUSPICIOUS: "의심"}.get(result, "Unknown")
        print(f"{url} → {result} ({label})")
