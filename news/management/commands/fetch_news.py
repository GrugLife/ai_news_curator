from django.core.management.base import BaseCommand
from news.models import Article
from news.scraper import fetch_hacker_news  # Assuming scraper.py is in the news folder


class Command(BaseCommand):
    help = "Fetches top stories from Hacker News and saves them to the database"

    def handle(self, *args, **options):
        self.stdout.write("Fetching news...")
        news_items = fetch_hacker_news()

        count = 0
        for item in news_items:
            # get_or_create prevents errors if the article already exists
            obj, created = Article.objects.get_or_create(
                title=item["title"], url=item["url"]
            )
            if created:
                count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Successfully added {count} new articles!")
        )
