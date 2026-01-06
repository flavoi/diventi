from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, RedirectView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from hitcount.views import HitCountDetailView

from .models import (
    Article, 
    BlogCover, 
    ArticleCategory,
)


class ArticlesListView(ListView):

    model = Article
    template_name = 'blog/article_list_quick.html'
    context_object_name = 'articles'
    paginate_by = 6

    def get_queryset(self):
        return Article.objects.history_but_not_hot().prefetch()

    def get_context_data(self, *args, **kwargs):
        context = super(ArticlesListView, self).get_context_data(*args, **kwargs)
        context['categories'] = ArticleCategory.objects.filter(article__in=Article.objects.history()).distinct()
        context['hot_articles'] = Article.objects.pinned_list()
        context['blogcover'] = BlogCover.objects.active()
        return context


class ArticlesListViewByCategory(ArticlesListView):

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.category(category_title=self.kwargs['category'])

    def get_context_data(self, *args, **kwargs):
        context = super(ArticlesListViewByCategory, self).get_context_data(*args, **kwargs)
        context['hot_articles'] = Article.objects.hot().category(category_title=self.kwargs['category'])
        return context


class ArticleDetailView(HitCountDetailView):

    model = Article
    context_object_name = 'article'
    template_name = 'blog/article_detail_quick.html'
    count_hit = True

    # Returns only published articles
    def get_queryset(self):
        qs = super(ArticleDetailView, self).get_queryset()
        return qs.published().prefetch()

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        context['related_articles'] = self.object.related_articles.prefetch()
        return context


class ArticlePromoteToggleView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        article = get_object_or_404(Article, slug=slug)
        user = self.request.user
        if user.is_authenticated:
            if user in article.promotions.all():
                article.promotions.remove(user)
            else:
                article.promotions.add(user)
        return reverse_lazy('blog:detail', kwargs={'slug': slug})


class ArticlePromoteToggleAPIView(APIView):

    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None, slug=None):
        article = get_object_or_404(Article, slug=slug)
        user = self.request.user
        updated = False
        promoted = False
        if user.is_authenticated:
            if user in article.promotions.all():
                article.promotions.remove(user)
                promoted = False
            else:
                article.promotions.add(user)
                promoted = True
            updated = True
        promotions = {
            'updated': updated,
            'promoted': promoted,
        }
        return Response(promotions)

