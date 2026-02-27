#!/usr/bin/env python3

from colorama import Fore, Style, init
import os
import json
from core.dns_lookup import dns_lookup
from core.whois_check import whois_info
from core.http_check import http_headers
from core.geoip_lookup import geoip_lookup
from core.mx_lookup import mx_lookup
from core.crawler import crawl_site
from core.js_endpoint import js_endpoint_extractor
from core.scrapper import scrapper
from core.bloggers_view import bloggers_view
from core.sqli_detector import detect_sqli
from core.admin_panel import detect_admin_panel
from core.cms_robots import analyze_site, print_analysis

init(autoreset=True)

report = {}

# ===============================
# YOUR ORIGINAL ASCII BANNER
# ===============================
def show_banner():
    os.system("clear")

    banner = r"""
._____.___ ._______  ._______  ._______  .______   ____   ____
:         |: .___  \ : .___  \ : .___  \ :      \   \   \_/   /
|   \  /   || :   |  || :   |  || :   |  ||       |   \___ ___/ 
|   |\/    ||     :  ||     :  ||     :  ||   |   |     |   |   
|___| |    | \_. ___/  \_. ___/  \_. ___/  |___|   |     |___|   
      |___|   :/        :/        :/           |___|            
              :         :         :                            
"""
    print(banner)
    print("\n           🌙 MOONY AUTHOR ADWAITH PRAMOD")


# ===============================
# SAVE REPORT
# ===============================
def save_report(domain):
    filename = f"{domain}_report.json"
    with open(filename, "w") as f:
        json.dump(report, f, indent=4)
    print(f"\n[+] Report saved as {filename}")


# ===============================
# RUN & DISPLAY
# ===============================
def run_and_display(key, func, *args):
    print(f"\n[+] Running {key}...\n")

    try:
        result = func(*args)
        report[key] = result

        if isinstance(result, dict):
            for k, v in result.items():
                if isinstance(v, list):
                    print(f"\n========== {k} ==========")
                    print(f"Total: {len(v)}\n")
                    for i, item in enumerate(v, 1):
                        print(f"[{i}] {item}")
                else:
                    print(f"{k}: {v}")
        else:
            print(result)

    except Exception as e:
        print(f"[!] Error in {key}: {e}")


# ===============================
# MAIN MENU
# ===============================
def main():
    show_banner()

    domain = input("Enter domain (example.com): ").strip()

    while True:
        print("\n" + "="*50)
        print("\nMoony v3 Menu:\n")

        print(f"{Fore.MAGENTA}[01]:{Style.RESET_ALL} DNS Lookup")
        print(f"{Fore.MAGENTA}[02]:{Style.RESET_ALL} WHOIS / HTTPS Info")
        print(f"{Fore.MAGENTA}[03]:{Style.RESET_ALL} HTTP Header Analysis")
        print(f"{Fore.MAGENTA}[04]:{Style.RESET_ALL} GeoIP Lookup")
        print(f"{Fore.MAGENTA}[05]:{Style.RESET_ALL} Crawler")
        print(f"{Fore.MAGENTA}[06]:{Style.RESET_ALL} MX Lookup")
        print(f"{Fore.MAGENTA}[07]:{Style.RESET_ALL} JS Endpoint Extractor")
        print(f"{Fore.MAGENTA}[08]:{Style.RESET_ALL} Scrapper")
        print(f"{Fore.MAGENTA}[09]:{Style.RESET_ALL} Bloggers View")
        print(f"{Fore.MAGENTA}[10]:{Style.RESET_ALL} SQL Injection Test")
        print(f"{Fore.MAGENTA}[11]:{Style.RESET_ALL} Admin Panel Detection")
        print(f"{Fore.MAGENTA}[12]:{Style.RESET_ALL} CMS + Robots.txt Analysis")
        print(f"{Fore.MAGENTA}[13]:{Style.RESET_ALL} Run Full Scan")
        print(f"{Fore.MAGENTA}[14]:{Style.RESET_ALL} Save Report")
        print(f"{Fore.MAGENTA}[15]:{Style.RESET_ALL} Exit")

        choice = input("\nSelect option: ").strip()

        if choice == "1":
            run_and_display("DNS", dns_lookup, domain)

        elif choice == "2":
            run_and_display("WHOIS", whois_info, domain)

        elif choice == "3":
            run_and_display("HTTP", http_headers, domain)

        elif choice == "4":
            run_and_display("GeoIP", geoip_lookup, domain)

        elif choice == "5":
            run_and_display("Crawler", crawl_site, domain)

        elif choice == "6":
            run_and_display("MX", mx_lookup, domain)

        elif choice == "7":
            js_url = input("Enter JavaScript file URL: ").strip()
            run_and_display("JS Endpoints", js_endpoint_extractor, js_url)

        elif choice == "8":
            scrape_email = input("Scrape Emails? (y/n): ").strip().lower() == "y"
            scrape_phone = input("Scrape Phone Numbers? (y/n): ").strip().lower() == "y"
            run_and_display("Scrapper", scrapper, domain, scrape_email, scrape_phone)

        elif choice == "9":
            run_and_display("Bloggers View", bloggers_view, domain)

        elif choice == "10":
            run_and_display("SQLi Detector", detect_sqli, domain)

        elif choice == "11":
            run_and_display("Admin Panel", detect_admin_panel, f"https://{domain}")

        elif choice == "12":
            analysis = analyze_site(f"https://{domain}")
            print_analysis(analysis)
            report["CMS + Robots"] = analysis

        elif choice == "13":
            run_and_display("DNS", dns_lookup, domain)
            run_and_display("WHOIS", whois_info, domain)
            run_and_display("HTTP", http_headers, domain)
            run_and_display("GeoIP", geoip_lookup, domain)
            run_and_display("MX", mx_lookup, domain)
            run_and_display("Crawler", crawl_site, domain)
            run_and_display("Bloggers View", bloggers_view, domain)
            run_and_display("SQLi Detector", detect_sqli, domain)
            run_and_display("Admin Panel", detect_admin_panel, f"https://{domain}")
            analysis = analyze_site(f"https://{domain}")
            print_analysis(analysis)
            report["CMS + Robots"] = analysis

        elif choice == "14":
            save_report(domain)

        elif choice == "15":
            print("Exiting Moony...")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
