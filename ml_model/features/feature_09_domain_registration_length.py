import whois
from urllib.parse import urlparse
from datetime import datetime

NORMAL = -1
PHISHING = 1
UNKNOWN = 0

def normalize_domain(url: str) -> str:
    domain = urlparse(url).netloc.split(":")[0].lower()
    return domain[4:] if domain.startswith("www.") else domain

def feature_09_domain_registration_length(url: str) -> int:
    """
    도메인 등록 기간 (F09)
    - 기간 1년 이하 → 피싱
    - WHOIS 실패 또는 정보 없음 → 0
    """
    try:
        domain = normalize_domain(url)
        w = whois.whois(domain)

        creation_date = w.creation_date
        expiration_date = w.expiration_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]

        if not creation_date or not expiration_date:
            return UNKNOWN

        if isinstance(creation_date, datetime) and isinstance(expiration_date, datetime):
            duration_days = (expiration_date - creation_date).days
            return PHISHING if duration_days <= 365 else NORMAL
        else:
            return UNKNOWN

    except Exception:
        return UNKNOWN
