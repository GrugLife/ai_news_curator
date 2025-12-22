import requests
from bs4 import BeautifulSoup


def fetch_hacker_news():
    url = "https://news.ycombinator.com/"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        print("Failed to retrieve news")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = []

    # HackerNews titles are inside spans with the class 'titleline'
    links = soup.find_all("span", class_="titleline")

    for link in links[:10]:  # Just get the top 10 for now
        a_tag = link.find("a")
        articles.append({"title": a_tag.text, "url": a_tag["href"]})

    return articles


# To test it, run: python news/scraper.py
if __name__ == "__main__":
    news = fetch_hacker_news()
    for item in news:
        print(f"Title: {item['title']}\nLink: {item['url']}\n")
