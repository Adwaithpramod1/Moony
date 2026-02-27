import requests
import re
from urllib.parse import urlparse, urljoin
import random
import time

# Bot detection bypass headers
BOT_BYPASS_UA = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
]

STEALTH_HEADERS = {
    'Accept': 'text/javascript, application/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.google.com/',
    'Sec-Fetch-Dest': 'script',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'cross-site',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache'
}

def get_stealth_headers():
    """Generate stealth headers for JS file requests"""
    headers = STEALTH_HEADERS.copy()
    headers['User-Agent'] = random.choice(BOT_BYPASS_UA)
    headers['Sec-Ch-Ua'] = f'"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"'
    return headers

def stealth_request(url: str, timeout: int = 10):
    """Make stealthy request to bypass bot detection"""
    session = requests.Session()
    session.headers.update(get_stealth_headers())
    
    # Human-like delay
    time.sleep(random.uniform(0.3, 0.8))
    
    try:
        response = session.get(
            url,
            timeout=timeout,
            allow_redirects=True,
            verify=True
        )
        response.raise_for_status()
        return response
    except requests.RequestException:
        # Fallback for strict SSL
        time.sleep(random.uniform(0.2, 0.5))
        response = session.get(
            url,
            timeout=timeout,
            allow_redirects=True,
            verify=False
        )
        response.raise_for_status()
        return response


def js_endpoint_extractor(js_url: str) -> dict:
    try:
        response = stealth_request(js_url, timeout=10)
        js_content = response.text
    except requests.RequestException as e:
        return {"error": f"Failed to fetch JS file: {e}"}

    parsed = urlparse(js_url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"

    # Match quoted strings starting with /
    pattern = r'(?:"|\')(/[^"\']+)(?:"|\')'
    matches = re.findall(pattern, js_content)

    seen = set()
    endpoints = []

    for rel in matches:
        if rel not in seen:
            seen.add(rel)
            full_url = urljoin(base_url, rel)
            endpoints.append(full_url)

    return {
        "js_url": js_url,
        "total_found": len(endpoints),
        "endpoints": endpoints
    }
