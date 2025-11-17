# scraper.py
import requests
from bs4 import BeautifulSoup

def scrape_wikipedia(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch URL: {url}")

    soup = BeautifulSoup(response.text, "html.parser")
    
    title = soup.find("h1").text
    paragraphs = soup.find_all("p")
    summary = " ".join([p.text for p in paragraphs[:3]])

    sections = [h2.text.replace("[edit]", "").strip() for h2 in soup.find_all("h2")]

    key_entities = {"people": [], "organizations": [], "locations": []}

    return {
        "title": title,
        "summary": summary,
        "sections": sections,
        "key_entities": key_entities,
        "raw_html": response.text
    }
