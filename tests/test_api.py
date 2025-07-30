# tests/test_scraper.py

from utils.scraper_helpers import fetch_page, parse_html

def test_fetch_page():
    url = "http://example.com"
    content = fetch_page(url)
    assert content is not None

def test_parse_html():
    html = "<html><body><p>Hello World!</p></body></html>"
    text = parse_html(html)
    assert "Hello World!" in text
