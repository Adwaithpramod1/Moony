import socket
import requests

def geoip_lookup(domain):
    print("\n[+] GeoIP Lookup...\n")
    info = {}
    try:
        ip = socket.gethostbyname(domain)
        r = requests.get(f"http://ip-api.com/json/{ip}")
        data = r.json()
        info = {
            "IP": ip,
            "Country": data.get("country"),
            "Region": data.get("regionName"),
            "City": data.get("city"),
            "ISP": data.get("isp")
        }
        for k, v in info.items():
            print(f"{k}: {v}")
    except Exception as e:
        print("GeoIP lookup failed:", e)
    return info
