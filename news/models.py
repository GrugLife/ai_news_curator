from django.db import models


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=500)
    url = models.URLField(unique=True)
    category = models.CharField(max_length=20, default="top news")
    source = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
