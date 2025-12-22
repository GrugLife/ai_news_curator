from django.shortcuts import render
from .models import Article


def article_list(request):
    # fetch all articles, ordered by the most recent first
    articles = Article.objects.all().order_by("-created_at")
    # pass the articles to the template using a context dictionary
    return render(request, "news/article_list.html", {"articles": articles})


# Create your views here.
