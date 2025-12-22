from django.core.management.base import BaseCommand
from news.models import Article
from news.scraper import fetch_finnhub  # Assuming scraper.py is in the news folder


class Command(BaseCommand):
    help = "Fetches top stories from finnhub and save them to the database"

    def handle(self, *args, **options):
        self.stdout.write("Fetching news...")
        news_items = fetch_finnhub()

        count = 0
        for item in news_items:
            # get_or_create prevents errors if the article already exists
            obj, created = Article.objects.get_or_create(
                title=item["title"],
                url=item["url"],
                category=item["category"],
            )
            if created:
                count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Successfully added {count} new articles!")
        )
