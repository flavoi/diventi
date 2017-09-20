from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .models import Article, Category


class ArticlesListView(ListView):
    model = Article
    context_object_name = 'articles'
    paginate_by = 6

    def get_queryset(self):
        return Article.objects.history()


class ArticleDetailView(DetailView):
    model = Article
    context_object_name = 'article'

    # Enables published articles only
    def get_queryset(self):
        qs = super(ArticleDetailView, self).get_queryset()
        return qs.published()