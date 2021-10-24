from functools import reduce
import operator, readtime

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation

from ckeditor.fields import RichTextField
from cuser.middleware import CuserMiddleware
from hitcount.models import HitCount

from diventi.core.models import (
    TimeStampedModel, 
    PromotableModel, 
    PublishableModel,
    PublishableModelQuerySet,
    Category, 
    DiventiImageModel, 
    DiventiCoverModel, 
    Element,
    DiventiColModel,
)


class BlogCover(DiventiCoverModel, Element):
    """
        Stores cover images for the blog page.
    """

    class Meta:
        verbose_name = _('Blog Cover')
        verbose_name_plural = _('Blog Covers')


class ArticleCategory(Element):
    """
        Defines the main argument of any article.
    """

    class Meta:
        verbose_name = _('Article Category')
        verbose_name_plural = _('Article Categories')


class ArticleQuerySet(PublishableModelQuerySet):
    
    # Selet articles' related objects
    def prefetch(self):
        articles = self.select_related('category')
        articles = articles.select_related('author')
        articles = articles.prefetch_related('related_articles')
        articles = articles.prefetch_related('promotions')
        return articles

    # Get the list of published articles from the most recent to the least 
    def history(self):
        articles = self.published()
        articles = articles.order_by('-publication_date')
        return articles

    # Get the list of published articles but excludes the hot ones
    def history_but_not_hot(self):
        articles = self.history().exclude(hot=True)
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


class Article(TimeStampedModel, PromotableModel, PublishableModel, DiventiImageModel, DiventiColModel, Element):
    """
        Blog posts are built upon a specific category and are always 
        introduced by a nice heading picture.
    """
    category = models.ForeignKey(
        ArticleCategory, 
        null=True, 
        verbose_name=_('category'), 
        on_delete=models.SET_NULL
    )    
    content = RichTextField(
        verbose_name=_('content')
    )
    hot = models.BooleanField(
        default=False, 
        verbose_name=_('hot')
    )
    slug = models.SlugField(
        unique=True,
        verbose_name=_('slug')
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        related_name='articles',
        verbose_name=_('author'),
        on_delete=models.SET_NULL
    )
    related_articles = models.ManyToManyField(
        'self',
        related_name='related_articles', 
        blank=True, 
        verbose_name=_('related articles'),
    ) # Connect this article to others
    hit_count_generic = GenericRelation(
        HitCount, 
        object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    ) # Counts the views on this model

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

    def get_readtime(self):
        result = readtime.of_text(self.content)
        return result.text

    def get_words_number(self):
        words = self.content.split()
        result = len(words)
        return result

    def class_name(self):
        return _('article')
