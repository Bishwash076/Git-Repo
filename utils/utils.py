# utils/scraper_helpers.py

import requests
from bs4 import BeautifulSoup
import time

def fetch_page(url):
    """Fetch page with simple rate limiting."""
    response = requests.get(url)
    time.sleep(1)  # Respect rate limit
    if response.status_code == 200:
        return response.text
    else:
        return None

def parse_html(html):
    """Parse HTML content and extract text."""
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()
