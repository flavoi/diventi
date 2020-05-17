from functools import reduce
import operator

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField
from cuser.middleware import CuserMiddleware

from diventi.core.models import (
    TimeStampedModel, 
    PromotableModel, 
    PublishableModel, 
    Category, 
    DiventiImageModel, 
    DiventiCoverModel, 
    Element,
    DiventiColModel,
)


class ArticleQuerySet(models.QuerySet):
    
    # Selet articles' related objects
    def prefetch(self):
        articles = self.select_related('category')
        articles = articles.select_related('author')
        return articles

    # Get the list of published articles f
    def published(self):
        user = CuserMiddleware.get_user()
        if user.is_superuser:
            articles = self
        else:
            articles = self.filter(published=True)
        return articles

    # Get the list of published articles from the most recent to the least 
    def history(self):
        articles = self.published().order_by('-hot', '-publication_date')
        articles = articles.prefetch()
        return articles

    # Get the list of published articles of a certain category
    def category(self, category_title):
        articles = self.history().filter(category__title=category_title)
        return articles

    # Get the featured articles
    def hot(self):
        articles = self.history().filter(hot=True)
        return articles

    # Get the hottest article
    def hottest(self):
        article = self.hot().latest('publication_date')
        return article

    # Fetch all the promotions related to the article
    def promotions(self):
        article = self.prefetch_related('promotions')
        return article

    # Get the most recent article
    def current(self):
        try:
            article = self.hottest()
        except Article.DoesNotExist:
            article = self.published().latest('publication_date')
        return article


class BlogCover(DiventiCoverModel, Element):
    """
        Stores cover images for the blog page.
    """

    class Meta:
        verbose_name = _('Blog Cover')
        verbose_name_plural = _('Blog Covers')


class ArticleCategory(Category):
    """
        Defines the main argument of any article.
    """
    pass


class Article(TimeStampedModel, PromotableModel, PublishableModel, DiventiImageModel, DiventiColModel):
    """
        Blog posts are built upon a specific category and are always 
        introduced by a nice heading picture.
    """
    title = models.CharField(max_length=60, verbose_name=_('title'))
    description = models.TextField(max_length=250, verbose_name=_('description'))
    category = models.ForeignKey(ArticleCategory, null=True, verbose_name=_('category'), on_delete=models.SET_NULL)    
    content = RichTextField(verbose_name=_('content'))
    hot = models.BooleanField(default=False, verbose_name=_('hot'))
    slug = models.SlugField(unique=True, verbose_name=_('slug'))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='articles', verbose_name=_('author'), on_delete=models.SET_NULL)

    objects = ArticleQuerySet.as_manager()
    

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', args=[str(self.slug)])

    def search(self, query, *args, **kwargs):
        results = Article.objects.history()
        query_list = query.split()
        results = results.filter(
            reduce(operator.and_,
                   (Q(title__icontains=q) for q in query_list)) |
            reduce(operator.and_,
                   (Q(description__icontains=q) for q in query_list))
        )
        return results

    def reporting(self, *args, **kwargs):
        results = Article.objects.none()
        return results

    def class_name(self):
        return _('article')
