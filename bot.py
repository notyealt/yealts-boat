
import os
import feedparser
import requests
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Configuration from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WP_URL = os.getenv("WP_SITE_URL")
WP_USER = os.getenv("WP_USERNAME")
WP_PASS = os.getenv("WP_PASSWORD")

client = OpenAI(api_key=OPENAI_API_KEY)

# Source list (Expandable)
SOURCES = [
    "https://www.ign.com/news",
    "https://www.gamespot.com/news/",
]

def get_latest_news():
    articles = []
    for url in SOURCES:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]: # Get top 5 from each source
            articles.append({
                'title': entry.title,
                'link': entry.link,
                'summary': entry.description if 'description' in entry else ""
            })
    return articles

def rewrite_with_ai(title, summary):
    prompt = f"Rewrite this gaming news item and make it engaging for a high-traffic website. Keep the core facts but improve the hook.
Title: {title}
Summary: {summary}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a professional gaming journalist."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def post_to_wordpress(title, content):
    # This handles the actual posting to your site
    # In a production environment, we use the provided WP credentials here
    print(f"Successfully prepared content for: {title}")
    # Logic for requests.post() would go here using WP data

def main():
    print("Bot started...")
    articles = get_latest_news()
    for item in articles:
        content = rewrite_with_ai(item['title'], item['summary'])
        post_to_wordpress(item['title'], content)
    print("Loop complete.")

if __name__ == "__main__":
    main()
