#!/usr/bin/env python3

import os
import re
import sys
import time
import requests
import random
from urllib.parse import urlparse

def normalize_url(url):
    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    return parsed.scheme + "://" + parsed.netloc
# ==============================
# Bot Bypass Configuration
# ==============================

BOT_BYPASS_UA = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0'
]

BOT_BYPASS_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

def get_random_headers():
    headers = BOT_BYPASS_HEADERS.copy()
    headers['User-Agent'] = random.choice(BOT_BYPASS_UA)
    return headers


# ==============================
# Internet Check
# ==============================

def check_internet():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except:
        print("[!] No internet connection.")
        return False


# ==============================
# Stealth Request
# ==============================

def make_stealth_request(url, timeout=10):
    session = requests.Session()
    session.headers.update(get_random_headers())

    time.sleep(random.uniform(0.5, 1.5))

    response = session.get(url, timeout=timeout, allow_redirects=True)
    response.raise_for_status()
    return response


# ==============================
# Scanner
# ==============================

def scanner():
    url_input = input("\n[*] Enter target domain (example.com): ").strip()

    if not url_input:
        print("[!] Invalid input.")
        return

    # Try HTTPS first
    https_url = f"https://{url_input}"
    http_url = f"http://{url_input}"

    try:
        make_stealth_request(https_url, timeout=5)
        url = https_url
    except:
        url = http_url

    email = input(" Scrape emails? (y/n): ").strip().lower()
    phone = input(" Scrape phone numbers? (y/n): ").strip().lower()

    if email in ['y', 'yes'] or phone in ['y', 'yes']:
        scrapper(url, email in ['y', 'yes'], phone in ['y', 'yes'])
    else:
        print("[!] Nothing selected.")


# ==============================
# Scraper Core
# ==============================

def scrapper(url, scrape_email, scrape_phone):

    try:
        url = normalize_url(url)

        print(f"\n[*] Fetching: {url}")
        response = make_stealth_request(url, timeout=10)

        with open("temp.txt", "w", encoding="utf-8") as f:
            f.write(response.text)

        print("[+] Content retrieved successfully")

    except Exception as e:
        print(f"[!] Failed to fetch URL: {e}")
        return

    if scrape_email:
        email_scraping()

    if scrape_phone:
        phone_scraping()

    if os.path.exists("email.txt") or os.path.exists("phone.txt"):
        save_output = input("\n Save results? (y/n): ").strip().lower()
        if save_output in ['y', 'yes']:
            output()

    cleanup()
    print("\n[+] Scan finished. Returning to menu...\n")


# ==============================
# Email Scraping
# ==============================

def email_scraping():
    print("\n[+] Email Scraping...\n")

    pattern = re.compile(r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,6}', re.IGNORECASE)

    with open("temp.txt", "r", encoding="utf-8") as f:
        content = f.read()

    emails = sorted(set(pattern.findall(content)))

    if emails:
        with open("email.txt", "w") as f:
            for e in emails:
                f.write(e + "\n")

        print("Emails found:")
        for e in emails:
            print(f"  - {e}")
    else:
        print("No emails found.")


# ==============================
# Phone Scraping
# ==============================

def phone_scraping():
    print("\n[+] Phone Scraping...\n")

    patterns = [
        r'\(\d{3}\)\s?\d{3}-\d{4}',
        r'\d{3}-\d{3}-\d{4}',
        r'\d{10}',
        r'\d{3}\s\d{3}\s\d{4}'
    ]

    with open("temp.txt", "r", encoding="utf-8") as f:
        content = f.read()

    phones = set()
    for p in patterns:
        phones.update(re.findall(p, content))

    phones = sorted(phones)

    if phones:
        with open("phone.txt", "w") as f:
            for p in phones:
                f.write(p + "\n")

        print("Phone numbers found:")
        for p in phones:
            print(f"  - {p}")
    else:
        print("No phone numbers found.")


# ==============================
# Save Output
# ==============================

def output():
    folder_name = input(" Enter folder name: ").strip()

    if os.path.exists(folder_name):
        print("[!] Folder already exists.")
        return

    os.mkdir(folder_name)

    if os.path.exists("email.txt"):
        os.rename("email.txt", os.path.join(folder_name, "email.txt"))
    if os.path.exists("phone.txt"):
        os.rename("phone.txt", os.path.join(folder_name, "phone.txt"))

    print("[+] Output saved successfully.")


# ==============================
# Cleanup
# ==============================

def cleanup():
    if os.path.exists("temp.txt"):
        os.remove("temp.txt")

    for file in ["email.txt", "phone.txt"]:
        if os.path.exists(file):
            os.remove(file)


# ==============================
# Main Menu Loop
# ==============================

def main_menu():
    while True:
        print("\n========== MOONY SCRAPER ==========")
        print("1. Start Scan")
        print("2. Exit")
        print("====================================")

        choice = input("Select option: ").strip()

        if choice == "1":
            scanner()
        elif choice == "2":
            print("[!] Exiting program.")
            break
        else:
            print("[!] Invalid option.")


# ==============================
# Entry Point
# ==============================

if __name__ == "__main__":
    if not check_internet():
        sys.exit(1)

    main_menu()
