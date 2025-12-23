from django.core.management.base import BaseCommand
from news.models import Article
from news.scraper import (
    fetch_finnhub,
    fetch_yfinance_news,
    fetch_alpha_vantage_news,
    fetch_massive_news,
)  # Assuming scraper.py is in the news folder


class Command(BaseCommand):
    help = "Aggregates news from all source"

    def handle(self, *args, **options):
        # 1 define th scrapers
        scrapers = [
            ("finnhub", fetch_finnhub),
            ("yahoo finance", fetch_yfinance_news),
            ("alphavantage", fetch_alpha_vantage_news),
            ("massive", fetch_massive_news),
        ]

        count = 0
        for website, scraper_func in scrapers:
            self.stdout.write(f"Running scraper for {website}...")

            try:
                items = scraper_func()
                for item in items:
                    # we only look up by URL (the unique field)
                    # get_or_create prevents errors if the article already exists
                    obj, created = Article.objects.get_or_create(
                        url=item["url"],
                        defaults={
                            "title": item["title"],
                            "category": item["category"],
                            "source": item["source"],
                            "published_at": item["published_at"],
                        },
                    )
                    if created:
                        count += 1
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error in scraper: {e}"))

        self.stdout.write(
            self.style.SUCCESS(f"Successfully added {count} new articles!")
        )
