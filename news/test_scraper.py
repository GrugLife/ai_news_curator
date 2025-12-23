import requests


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


yfinance_news = fetch_alpha_vantage_news()
for item in yfinance_news:
    print(
        f"Title: {item['title']}\nLink: {item['url']}\nCategory: {item['category']}\nSource: {item['source']}\n Date: {item['published_at']}\n"
    )
