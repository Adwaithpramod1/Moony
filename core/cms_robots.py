import requests
from urllib.parse import urljoin

CMS_SIGNATURES = {
    "WordPress": [
        "wp-content", "wp-includes", "wp-login.php",
        "xmlrpc.php", "wp-json"
    ],
    "Joomla": [
        "administrator/index.php", "joomla!", "/components/"
    ],
    "Drupal": [
        "sites/default", "drupal.settings"
    ]
}

def analyze_site(base_url):
    result = {
        "cms": "Unknown",
        "cms_confidence": "Low",
        "cloudflare": False,
        "server": "Unknown",
        "powered_by": "Unknown",
        "robots_found": False,
        "robots_disallowed": []
    }

    session = requests.Session()
    session.headers.update({
        "User-Agent": "MoonyScanner/2.0"
    })

    try:
        response = session.get(base_url, timeout=8, allow_redirects=True)
        content = response.text.lower()

        # -------------------------
        # Detect Server & Headers
        # -------------------------
        result["server"] = response.headers.get("Server", "Unknown")
        result["powered_by"] = response.headers.get("X-Powered-By", "Unknown")

        if "cloudflare" in result["server"].lower() or \
           "cf-ray" in response.headers:
            result["cloudflare"] = True

        # -------------------------
        # CMS Detection (HTML scan)
        # -------------------------
        for cms, signatures in CMS_SIGNATURES.items():
            matches = 0
            for sig in signatures:
                if sig.lower() in content:
                    matches += 1

            if matches >= 2:
                result["cms"] = cms
                result["cms_confidence"] = "High"
                break
            elif matches == 1:
                result["cms"] = cms
                result["cms_confidence"] = "Medium"

        # -------------------------
        # Extra CMS path probing
        # -------------------------
        if result["cms"] == "Unknown":
            wp_check = session.get(urljoin(base_url, "/wp-login.php"), timeout=5)
            if wp_check.status_code in [200, 302]:
                result["cms"] = "WordPress"
                result["cms_confidence"] = "Medium"

    except requests.RequestException:
        pass

    # -------------------------
    # Robots.txt Analysis
    # -------------------------
    try:
        robots_url = urljoin(base_url, "/robots.txt")
        robots_response = session.get(robots_url, timeout=5)

        if robots_response.status_code == 200:
            result["robots_found"] = True

            lines = robots_response.text.splitlines()
            for line in lines:
                if line.lower().startswith("disallow"):
                    parts = line.split(":")
                    if len(parts) > 1:
                        path = parts[1].strip()
                        if path:
                            result["robots_disallowed"].append(path)

    except requests.RequestException:
        pass

    return result


# -------------------------
# Pretty Display Function
# -------------------------
def print_analysis(result):
    print("\n========== CMS + Robots Analysis ==========\n")

    print(f"[+] CMS Detected      : {result['cms']}")
    print(f"[+] Confidence Level  : {result['cms_confidence']}")
    print(f"[+] Server            : {result['server']}")
    print(f"[+] Powered By        : {result['powered_by']}")
    print(f"[+] Cloudflare        : {result['cloudflare']}")
    print(f"[+] Robots.txt Found  : {result['robots_found']}")

    if result["robots_disallowed"]:
        print("\n[+] Disallowed Paths:")
        for path in result["robots_disallowed"]:
            print(f"    - {path}")
    else:
        print("\n[-] No Disallowed Paths Found")

    print("\n===========================================\n")


# -------------------------
# Standalone Test
# -------------------------
if __name__ == "__main__":
    site = "https://example.com"
    analysis = analyze_site(site)
    print_analysis(analysis)
