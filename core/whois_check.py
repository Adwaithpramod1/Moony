import whois
from datetime import datetime, timezone

def whois_info(domain):
    print("\n[+] WHOIS / HTTPS Info...\n")
    info = {}
    try:
        w = whois.whois(domain)
        info["Domain Name"] = w.domain_name
        info["Registrar"] = w.registrar
        info["Creation Date"] = str(w.creation_date)
        info["Expiration Date"] = str(w.expiration_date)
        info["Name Servers"] = w.name_servers
        info["Status"] = w.status

        print("Domain Name:", w.domain_name)
        print("Registrar:", w.registrar)
        print("Creation Date:", w.creation_date)
        print("Expiration Date:", w.expiration_date)
        if isinstance(w.expiration_date, list):
            exp_date = w.expiration_date[0]
        else:
            exp_date = w.expiration_date
        if exp_date:
            if exp_date.tzinfo is None:
                exp_date = exp_date.replace(tzinfo=timezone.utc)
            days_left = (exp_date - datetime.now(timezone.utc)).days
            print("Days Until Expiration:", days_left)
            if days_left < 30:
                print("⚠ WARNING: Domain expiring soon!")
    except Exception as e:
        print("WHOIS check failed:", e)
    return info
