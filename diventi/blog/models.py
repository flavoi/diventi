from functools import reduce
import operator

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

from ckeditor.fields import RichTextField

from diventi.core.models import TimeStampedModel, PromotableModel, PublishableModel


class ArticleQuerySet(models.QuerySet):
    
    # Get all the published articles 
    def published(self):
        articles = self.filter(published=True)
        return articles

    # Get the list of published articles from the most recent to the least 
    def history(self):
        articles = self.published().order_by('-hot', 'publication_date')
        return articles

    # Get the list of published articles of a certain category
    def category(self, category_title):
        articles = self.history().filter(category__title=category_title)
        return articles

    # Get the hottest article
    def hottest(self):
        article = self.history().filter(hot=True).latest('publication_date')
        return article

    # Fetch all the promotions related to the article
    def promotions(self):
        article = self.prefetch_related('promotions')
        return article

    # Get the most recent article
    def current(self):
        try:
            article = self.get_hottest_article()
        except ObjectDoesNotExist:
            article = self.published().latest('publication_date')
        return article


class Category(models.Model):
    """
        Defines the main argument of any article.
    """
    title = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.title

    class Meta:
    	verbose_name_plural = "categories"


class Article(TimeStampedModel, PromotableModel, PublishableModel):
    """
        Blog posts are built upon a specific category and are always 
        introduced by a nice heading picture.
    """
    title = models.CharField(max_length=60)
    description = RichTextField(max_length=250)
    category = models.ForeignKey(Category)
    image = models.ImageField(blank=True, upload_to='blog/')
    caption = models.CharField(max_length=60, blank=True)
    content = RichTextField()    
    hot = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='articles')

    objects = ArticleQuerySet.as_manager()

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

    def class_name(self):
        return self.__class__.__name__
