from django.shortcuts import render
from django.views.generic.detail import DetailView


from .models import Survey


class ArticleDetailView(DetailView):

    model = Article
    context_object_name = 'article'

    def get_queryset(self):
        qs = super(ArticleDetailView, self).get_queryset()
        return qs.published().promotions()
