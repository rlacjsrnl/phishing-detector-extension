import whois
from urllib.parse import urlparse
from datetime import datetime

def normalize_domain(url: str) -> str:
    domain = urlparse(url).netloc.split(":")[0].lower()
    return domain[4:] if domain.startswith("www.") else domain

def feature_24_age_of_domain(url: str) -> int:
    """
    도메인 나이 (F24)
    - 180일 이상이면 정상 (-1)
    - 미만이거나 WHOIS 실패 시 의심 (0)
    """
    try:
        domain = normalize_domain(url)
        w = whois.whois(domain)
        creation_date = w.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if not isinstance(creation_date, datetime):
            return 0

        age_days = (datetime.now() - creation_date).days
        return -1 if age_days >= 180 else 0

    except Exception:
        return 0
