import os
from dotenv import load_dotenv
from massive import RESTClient
from massive.rest.models import (
    TickerNews,
)

load_dotenv()


def fetch_massive_news():
    client = RESTClient(os.getenv("MASSIVE_API_KEY"))
    articles = []
    iterator = client.list_ticker_news(order="desc", limit=50, sort="published_utc")
    for index, item in enumerate(iterator):
        if index >= 50:
            break

        if isinstance(item, TickerNews):
            # --- GET FIRST KEYWORD AS CATEGORY ---
            # item.keywords is a list. We use .get() and check if it has items.
            raw_keywords = getattr(item, "keywords", [])
            if raw_keywords and len(raw_keywords) > 0:
                category = raw_keywords[0].title()
            else:
                category = "Finance"

            articles.append(
                {
                    "title": item.title,
                    "url": item.article_url,
                    "source": item.publisher.name,
                    "published_at": item.published_utc,
                    "category": category,
                }
            )
    return articles
