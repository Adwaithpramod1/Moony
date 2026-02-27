import requests
from bs4 import BeautifulSoup

def bloggers_view(url: str) -> dict:
    """
    Analyze a website like a blogger would: 
    - Shows title, meta description, h1 headings, and social links
    """
    if not url.startswith("http"):
        url = "http://" + url

    try:
        response = requests.get(url, timeout=5)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        # Page title
        title = soup.title.string if soup.title else "No title found"

        # Meta description
        meta_desc_tag = soup.find("meta", attrs={"name": "description"})
        meta_desc = meta_desc_tag["content"] if meta_desc_tag else "No description"

        # H1 headings
        h1_tags = [h.get_text(strip=True) for h in soup.find_all("h1")]

        # Social media links (basic)
        social_domains = ["facebook.com", "twitter.com", "instagram.com", "linkedin.com", "tiktok.com"]
        social_links = []
        for a in soup.find_all("a", href=True):
            if any(domain in a["href"] for domain in social_domains):
                social_links.append(a["href"])

        return {
            "title": title,
            "meta_description": meta_desc,
            "h1_headings": h1_tags,
            "social_links": social_links
        }

    except requests.RequestException as e:
        return {"error": str(e)}
