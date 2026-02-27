import requests
import time

def http_headers(domain):
    print("\n[+] HTTP Header Analysis...\n")
    info = {}
    try:
        start = time.time()
        response = requests.get(f"https://{domain}", timeout=10)
        end = time.time()
        headers = response.headers

        info = {
            "Status": response.status_code,
            "Server": headers.get("Server"),
            "Response Time": round(end - start, 2),
            "Security Headers": {
                "Content-Security-Policy": headers.get("Content-Security-Policy"),
                "Strict-Transport-Security": headers.get("Strict-Transport-Security"),
                "X-Frame-Options": headers.get("X-Frame-Options"),
                "X-Content-Type-Options": headers.get("X-Content-Type-Options"),
            }
        }

        print("Status Code:", response.status_code)
        print("Server:", headers.get("Server"))
        print("Response Time:", round(end - start, 2), "seconds")
        for k, v in info["Security Headers"].items():
            print(f"{k}: {v}")
    except Exception as e:
        print("HTTP check failed:", e)
    return info
