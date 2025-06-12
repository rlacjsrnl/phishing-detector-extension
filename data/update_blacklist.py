import requests
import os
import re

# URLhaus / OpenPhish 블랙리스트 경로
HOSTFILE_URL = "https://urlhaus.abuse.ch/downloads/hostfile/"
URLHAUS_FEED_URL = "https://urlhaus.abuse.ch/downloads/text/"
OPENPHISH_FEED_URL = "https://openphish.com/feed.txt"

BLACKLIST_FILE = "data/blacklist.txt"
URLHAUS_FILE_PATH = "data/hostfile.txt"

def is_ipv4(ip: str) -> bool:
    return re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", ip) is not None

def download_hostfile():
    try:
        response = requests.get(HOSTFILE_URL)
        with open(URLHAUS_FILE_PATH, "wb") as f:
            f.write(response.content)
        print("Hostfile downloaded successfully!")
    except Exception as e:
        print(f"Error downloading hostfile: {e}")

def parse_hostfile():
    try:
        with open(URLHAUS_FILE_PATH, "r") as file:
            lines = file.readlines()
    except Exception as e:
        print(f"Error reading hostfile.txt: {e}")
        return set()

    entries = set()
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split()
        if len(parts) >= 2:
            ip = parts[0].split(":")[0]
            host = parts[1].lower().replace("www.", "")
            entries.update([ip, host])
        else:
            value = line.split()[0].split(":")[0]
            if value:
                entries.add(value.lower())

    return entries

def parse_urlhaus():
    try:
        response = requests.get(URLHAUS_FEED_URL)
        entries = set()
        for line in response.text.splitlines():
            if line.startswith("http"):
                host = line.split("/")[2].lower().replace("www.", "")
                entries.add(host)
        return entries
    except:
        return set()

def parse_openphish():
    try:
        response = requests.get(OPENPHISH_FEED_URL)
        entries = set()
        for line in response.text.splitlines():
            if line.startswith("http"):
                host = line.split("/")[2].lower().replace("www.", "")
                entries.add(host)
        return entries
    except:
        return set()

def update_blacklist():
    download_hostfile()
    all_entries = parse_hostfile()
    all_entries.update(parse_urlhaus())
    all_entries.update(parse_openphish())

    print(f"최종 수집된 블랙리스트 수: {len(all_entries)}")

    os.makedirs("data", exist_ok=True)
    with open(BLACKLIST_FILE, "w") as f:
        for entry in sorted(all_entries):
            f.write(f"{entry}\n")

if __name__ == "__main__":
    update_blacklist()
