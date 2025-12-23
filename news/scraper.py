import os
import requests
import finnhub
import yfinance as yf
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def fetch_finnhub():
    finnhub_client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))
    if not finnhub_client:
        print("Error: FINNHUB_API_KEY not found in .env")
        return []

    articles = []
    for item in finnhub_client.general_news("general", min_id=0)[:50]:
        raw_dt = datetime.fromtimestamp(item["datetime"])
        articles.append(
            {
                "title": item["headline"],
                "url": item["url"],
                "category": item["category"],
                "source": item["source"],
                "published_at": raw_dt,
            }
        )
    return articles


def fetch_yfinance_news():
    indexes = ["^GSPC", "^IXIC", "GC=F", "SI=F"]

    all_articles = []
    for ticker_symbol in indexes:
        ticker = yf.Ticker(ticker_symbol)
        for item in ticker.news[:50]:
            all_articles.append(
                {
                    "title": item["content"]["title"],
                    "url": item["content"]["canonicalUrl"]["url"],
                    "source": item["content"]["provider"]["displayName"],
                    "category": "Finance",
                    "published_at": item["content"]["pubDate"],
                }
            )
    return all_articles


def fetch_alpha_vantage_news():
    # ... your API request logic ...
    url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=AAPL&apikey={"ALPHAVANTAGE_API_KEY"}'
    r = requests.get(url)
    data = r.json()

    # 1. Access the 'feed' list
    articles_data = data.get("feed", [])

    articles = []
    for item in articles_data:
        # 2. Parse the special Alpha Vantage date format: YYYYMMDDTHHMMSS
        # Example: 20251222T222153
        topics = item.get("topics", [])
        if topics:
            category = topics[0].get("topic").replace("_", " ").title()
        else:
            category = "Finance"

        articles.append(
            {
                "title": item.get("title"),
                "url": item.get("url"),
                "summary": item.get("summary"),
                "source": item.get("source"),
                "published_at": item.get("time_published"),
                "category": category,  # You could also pull from the 'topics' list
            }
        )
    return articles


# To test it, run: python news/scraper.py
if __name__ == "__main__":
    fin_news = fetch_finnhub()
    for item in fin_news:
        print(
            f"Title: {item['title']}\nLink: {item['url']}\nCategory: {item['category']}\nSource: {item['source']}\n Date: {item['published_at']}\n"
        )

    yfinance_news = fetch_yfinance_news()
    for item in yfinance_news:
        print(
            f"Title: {item['title']}\nLink: {item['url']}\nCategory: {item['category']}\nSource: {item['source']}\n Date: {item['published_at']}\n"
        )

    av_news = fetch_alpha_vantage_news()
    for item in av_news:
        print(
            f"Title: {item['title']}\nLink: {item['url']}\nCategory: {item['category']}\nSource: {item['source']}\n Date: {item['published_at']}\n"
        )
