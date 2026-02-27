import requests
from urllib.parse import urljoin

# Large admin wordlist
ADMIN_WORDLIST = [
    "admin", "administrator", "administration", "admin/login",
    "admin.php", "admin/login.php", "adminarea", "admin_area",
    "adminpanel", "admin-panel", "cpanel", "controlpanel",
    "dashboard", "backend", "manage", "manager", "management",
    "user", "users", "account", "accounts", "auth",
    "login", "signin", "log-in", "member", "members",
    "wp-login.php", "wp-admin", "wp-admin/login.php",
    "joomla/administrator", "administrator/index.php",
    "drupal/user/login", "cms", "panel", "moderator",
    "staff", "root", "secure", "portal"
]

# Keywords to confirm login/admin page
KEYWORDS = [
    "login", "password", "username", "admin",
    "dashboard", "control panel", "sign in"
]

def detect_admin_panel(base_url):
    found = []
    session = requests.Session()
    session.headers.update({
        "User-Agent": "MoonyScanner/2.0"
    })

    print("[*] Starting advanced admin panel scan...\n")

    for path in ADMIN_WORDLIST:
        url = urljoin(base_url.rstrip("/") + "/", path)

        try:
            # First try HEAD request (faster)
            head = session.head(url, timeout=5, allow_redirects=True)

            if head.status_code in [200, 301, 302, 403]:
                # Now GET request to verify content
                res = session.get(url, timeout=7, allow_redirects=True)

                if res.status_code in [200, 403]:
                    content = res.text.lower()

                    if any(keyword in content for keyword in KEYWORDS):
                        print(f"[+] Possible Admin Panel Found: {url}")
                        found.append(url)

        except requests.RequestException:
            continue

    if not found:
        print("[-] No admin panel detected with current wordlist.")

    return found
