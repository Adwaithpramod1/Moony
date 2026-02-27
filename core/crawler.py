import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def crawl_site(domain):
    print("\n[+] Crawling target...\n")

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux; Android 12)"
    }

    result = {
        "Status": None,
        "Internal Links": [],
        "External Links": [],
        "Admin/Login Links": []
    }

    # Try HTTPS first
    urls_to_try = [
        f"https://{domain}",
        f"http://{domain}"
    ]

    response = None

    for url in urls_to_try:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            break
        except requests.RequestException:
            continue

    if response is None:
        return {"Error": "Failed to connect using HTTP or HTTPS"}

    result["Status"] = response.status_code

    soup = BeautifulSoup(response.text, "html.parser")
    found_links = set()

    # Collect all <a> links
    for tag in soup.find_all("a", href=True):
        full_url = urljoin(response.url, tag["href"])
        found_links.add(full_url)

    # Process links
    for link in found_links:
        parsed = urlparse(link)

        if domain in parsed.netloc:
            result["Internal Links"].append(link)

            # Detect admin/login related links
            if any(keyword in link.lower() for keyword in
                   ["admin", "login", "dashboard", "panel", "account"]):
                result["Admin/Login Links"].append(link)
        else:
            result["External Links"].append(link)

    # Sort results
    result["Internal Links"].sort()
    result["External Links"].sort()
    result["Admin/Login Links"].sort()

    return result
