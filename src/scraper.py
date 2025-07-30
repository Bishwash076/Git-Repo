```
import scrapy
from boto3 import client
from dotenv import load_dotenv
import os
import re

load_dotenv()

class GutenbergSpider(scrapy.Spider):
    name = "gutenberg"
    start_urls = [os.getenv("TARGET_SITE", "https://www.gutenberg.org/ebooks/search/?sort_order=downloads")]
    custom_settings = {
        "DOWNLOAD_DELAY": 1,  # 1-second delay to respect rate limits
        "ROBOTSTXT_OBEY": True,  # Respect robots.txt
        "CONCURRENT_REQUESTS": 2  # Limit concurrent requests
    }

    def __init__(self):
        self.minio_client = client(
            "s3",
            endpoint_url="http://minio:9000",
            aws_access_key_id=os.getenv("MINIO_ROOT_USER"),
            aws_secret_access_key=os.getenv("MINIO_ROOT_PASSWORD")
        )
        self.page_count = 0
        self.max_pages = 50  # Limit to 50 pages

    def parse(self, response):
        # Extract book links from the search page
        for link in response.css("li.booklink a::attr(href)").getall():
            if self.page_count >= self.max_pages:
                return
            self.page_count += 1
            yield response.follow(link, callback=self.parse_book)

        # Follow pagination links
        next_page = response.css("a[title='Go to the next page of results']::attr(href)").get()
        if next_page and self.page_count < self.max_pages:
            yield response.follow(next_page, callback=self.parse)

    def parse_book(self, response):
        # Extract metadata and text
        title = response.css("h1::text").get(default="Unknown").strip()
        author = response.css("a[href*='/author/']::text").get(default="Unknown").strip()
        text = " ".join(response.css("body *::text").getall())
        # Clean text (remove excessive whitespace)
        text = re.sub(r'\s+', ' ', text).strip()
        html = response.text
        book_id = response.url.split("/")[-1]

        # Prepare metadata
        metadata = {
            "title": title,
            "author": author,
            "url": response.url,
            "scrape_timestamp": response.meta.get("scrape_time", "")
        }

        # Save raw HTML to MinIO
        self.minio_client.put_object(
            Bucket="lake",
            Key=f"raw/html/{book_id}.html",
            Body=html.encode("utf-8")
        )

        # Save extracted text with metadata to MinIO
        self.minio_client.put_object(
            Bucket="lake",
            Key=f"raw/text/{book_id}.txt",
            Body=f"Title: {title}\nAuthor: {author}\nURL: {response.url}\n\n{text}".encode("utf-8")
        )
```