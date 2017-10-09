from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, RedirectView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from .models import Article, Category


class ArticlesListView(ListView):

    model = Article
    context_object_name = 'articles'
    paginate_by = 6

    def get_queryset(self):
        return Article.objects.history().promotions()


class ArticleDetailView(DetailView):

    model = Article
    context_object_name = 'article'

    # Returns only published articles
    def get_queryset(self):
        qs = super(ArticleDetailView, self).get_queryset()
        return qs.published().promotions()

    # Returns True if the user has promoted the article
    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        article = self.object
        user = self.request.user
        user_has_promoted = False
        if user in article.promotions.all():
            user_has_promoted = True
        extra_context = {
            'user_has_promoted': user_has_promoted,
        }
        context.update(extra_context)
        return context


class ArticlePromoteToggleView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        article = get_object_or_404(Article, slug=slug)
        user = self.request.user
        if user.is_authenticated():
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
        if user.is_authenticated():
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

