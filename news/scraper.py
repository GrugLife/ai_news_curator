import os
import finnhub
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def fetch_finnhub():
    finnhub_client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))
    if not finnhub_client:
        print("Error: FINNHUB_API_KEY not found in .env")
        return []

    articles = []
    for item in finnhub_client.general_news("general", min_id=0)[:10]:
        articles.append(
            {
                "title": item["headline"],
                "url": item["url"],
                "category": item["category"],
                "source": item["source"],
                "date": datetime.fromtimestamp(item["datetime"]),
            }
        )
    return articles


# To test it, run: python news/scraper.py
if __name__ == "__main__":
    fin_news = fetch_finnhub()
    for item in fin_news:
        print(
            f"Title: {item['title']}\nLink: {item['url']}\nCategory: {item['category']}\n, Date: {item['date']}\n"
        )
