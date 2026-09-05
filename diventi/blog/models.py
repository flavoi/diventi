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
from hitcount.models import HitCount, HitCountMixin

from diventi.core.models import (
    TimeStampedModel, 
    PromotableModel, 
    PublishableModel,
    FeaturedModel,
    PublishableModelQuerySet,
    FeaturedModelQuerySet,
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
    slug = models.SlugField(
        verbose_name=_('slug')
    )

    class Meta:
        verbose_name = _('Article Category')
        verbose_name_plural = _('Article Categories')


class ArticleQuerySet(FeaturedModelQuerySet):
    
    def prefetch_basic(self):
        """Prefetch basilare per liste ed elenchi generali."""
        return self.select_related('category', 'author')

    def prefetch_detail(self):
        """Prefetch completo per la pagina di dettaglio del singolo articolo."""
        return self.prefetch_basic().prefetch_related(
            'related_articles',
            'promotions'
        )

    # Mantieni retrocompatibilità
    def prefetch(self):
        return self.prefetch_basic()

    def prefetch_hitcount(self):
        return self.prefetch_related('hit_count_generic')

    def history(self):
        return self.published().order_by('-publication_date')

    def history_but_not_hot(self):
        return self.history().exclude(featured=True)

    def category(self, category_title):
        return self.history().filter(category__title_plural=category_title)

    def hot(self):
        return self.history().pinned_list()

    def hottest(self):
        return self.hot().latest('publication_date')

    def current(self):
        try:
            return self.hottest()
        except Article.DoesNotExist:
            return self.published().latest('publication_date')

    def hit_count(self):
        return self.published().prefetch_basic().prefetch_hitcount().order_by('-hit_count_generic__hits')

    def popular(self):
        return self.hit_count()[:3]

    def popular_recent(self):
        return self.hit_count().order_by('-publication_date')[:3]


class Article(TimeStampedModel, PromotableModel, FeaturedModel, DiventiImageModel, DiventiColModel, Element, HitCountMixin):
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
    slug = models.SlugField(
        unique=True,
        verbose_name=_('slug')
    )
    postcard = models.URLField(
        blank=True, 
        verbose_name = _('postcard')
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

    def postcard_tag(self):
        return super(Article, self).image_tag(image_url=self.postcard)
    postcard_tag.short_description = _('Postcard')

    def search(self, query, *args, **kwargs):
        results = Article.objects.history()
        query_list = query.split()
        results = results.filter(
            reduce(operator.and_,
                   (Q(title__icontains=q) for q in query_list)) |
            reduce(operator.and_,
                   (Q(description__icontains=q) for q in query_list)) |
            reduce(operator.and_,
                   (Q(category__title__icontains=q) for q in query_list))
        )
        return results

    def reporting_popular(self, *args, **kwargs):
        queryset = Article.objects.popular()
        results = []
        for article in queryset:
            results.append({
                'columns': 4,
                'name': '%(article)s' % {
                    'article': article.title,
                },
                'title': article.hit_count.hits,
                'description1': _('views in the last week: %(d)s') % {
                    'd': article.hit_count.hits_in_last(days=7),
                },
                'description2': '',
                'action': '',
            })
        return results

    def reporting_latest(self, *args, **kwargs):
        queryset = Article.objects.popular_recent()
        results = []
        for article in queryset:
            results.append({
                'columns': 4,
                'name': '%(article)s' % {
                    'article': article.title,
                },
                'title': article.hit_count.hits,
                'description1': _('views in the last week: %(d)s') % {
                    'd': article.hit_count.hits_in_last(days=7),
                },
                'description2': '',
                'action': '',
            })
        return results

    def get_readtime(self):
        result = readtime.of_text(self.content)
        return result.text
    get_readtime.short_description = _('Readtime')

    def get_words_number(self):
        words = self.content.split()
        result = len(words)
        return result
    get_words_number.short_description = _('Words number')

    def get_hitcounts(self):
        return self.hit_count.hits
    get_hitcounts.short_description = _('Hit counts')
    get_hitcounts.admin_order_field = 'hit_count_generic__hits'

    def class_name(self):
        return _('article')
