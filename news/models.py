from django.db import models
from django.utils import timezone


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=500)
    url = models.URLField(unique=True)
    category = models.CharField(max_length=100, default="General")
    source = models.CharField(max_length=100, default="Unknown")
    summary = models.TextField(blank=True, null=True)
    published_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
