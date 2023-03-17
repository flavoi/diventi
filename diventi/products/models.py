from functools import reduce
import operator

from django.db import models
from django.db.models import Prefetch, Q, Count
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.utils.translation import gettext_lazy as _, gettext
from django.contrib.humanize.templatetags.humanize import naturalday
from django.contrib.auth import get_user_model

from cuser.middleware import CuserMiddleware

from .fields import ProtectedFileField

from diventi.feedbacks.models import Survey
from diventi.blog.models import Article

from diventi.core.models import (
    Element,
    DiventiImageModel,
    TimeStampedModel,
    PublishableModel,
    PublishableModelQuerySet,
    Category,
    Element,
    SectionModel,
    HighlightedModel,
    DiventiColModel,
    DiventiCoverModel,
    FeaturedModel,
    FeaturedModelQuerySet
)


class ProductCover(DiventiCoverModel, Element):
    """
        Stores cover images for the blog page.
    """

    class Meta:
        verbose_name = _('Product Cover')
        verbose_name_plural = _('Product Covers')


class ProductQuerySet(FeaturedModelQuerySet):

    # Prefetch all relevant data
    def prefetch(self):
        products = self.prefetch_related('chapters')
        products = products.prefetch_related('authors')
        products = products.prefetch_related('related_products')
        products = products.prefetch_related('customers')
        products = products.prefetch_related('details')
        products = products.select_related('category')
        products = products.prefetch_related('formats')
        products = products.prefetch_related('related_articles')
        products = products.select_related('product_survey')
        return products

    # Fetch the products purchased by the user
    def user_collection(self, user):
        current_user = CuserMiddleware.get_user() # The user that is operating in the session
        products = self.filter(customers=user)
        if current_user != user: # Hide non-published products if the user is not visiting his own profile
            products = products.published()
        products = products.prefetch()
        return products

    # Fetch the products authored by the user
    def user_authored(self, user):
        products = self.filter(authors=user)
        products = products.prefetch()
        return products

    # Return true if the user has authored at least one product
    def has_user_authored(self, user):
        return self.user_authored(user).exists()

    # Get the list of published products of a certain category
    def category(self, category_slug):
        products = self.published().filter(category__slug=category_slug)
        products = products.exclude(category__meta_category=True)
        return products

    # Exclude hot products
    def not_hot(self):
        products = self.exclude(featured=True)
        return products

    # Get the list of published products but excludes the hot ones
    def published_but_not_hot(self):
        products = self.published().not_hot()
        return products

    # Get the latest product that has public access
    def latest_public(self):
        product = self.published().filter(public=True).latest('publication_date')
        return product

    # Filter public products only
    def public(self):
        products = self.filter(public=True)
        return products

    # Exclude public products        
    def not_public(self):
        products = self.exclude(public=True)
        return products


class ProductCategoryQuerySet(models.QuerySet):

    # Meta categories won\'t be listed in search results, nor on reporting pages.
    # In addition, we show categories that are related to published projects only.
    def visible(self):
        categories = self.exclude(meta_category=True)
        published_projects = Product.objects.published()
        categories = categories.filter(projects__pk__in=published_projects) # Exclude empty categories
        categories = categories.prefetch_related(Prefetch('projects', queryset=published_projects)).distinct()
        return categories


class ProductCategory(Element):
    """
        Defines the type of a product.
    """
    meta_category = models.BooleanField(
        default=False, 
        verbose_name=_('meta category'), 
        help_text=_('Meta categories won\'t be listed in search results, nor on reporting pages.')
    )
    slug = models.SlugField(
        verbose_name=_('slug')
    )

    objects = ProductCategoryQuerySet.as_manager()

    class Meta:
        verbose_name = _('Product category')
        verbose_name_plural = _('Product categories')


class ProductFormat(Element):
    """ A specific format of a product."""

    class Meta:
        verbose_name = _('Format')
        verbose_name_plural = _('Formats')


class Product(TimeStampedModel, FeaturedModel, DiventiImageModel, Element, SectionModel, DiventiColModel):
    """ An adventure or a module published by Diventi. """
    title = models.CharField(
        max_length=50, 
        verbose_name=_('title')
    )
    short_description = models.TextField(
        blank=True, 
        max_length=50, 
        verbose_name=_('short description')
    )
    abstract = models.TextField(
        blank=True, 
        max_length=200, 
        verbose_name=_('abstract')
    )
    description = models.TextField(
        blank=True, 
        verbose_name=_('description')
    )
    slug = models.SlugField(
        unique=True, 
        verbose_name=_('slug')
    )
    authors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='products', 
        verbose_name=_('authors')
    )
    buyers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='collection',
        blank=True, 
        verbose_name=_('buyers')
    )
    customers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        through='Purchase', 
        blank=True, 
        verbose_name=_('customers')
    )
    file = ProtectedFileField(
        upload_to='products/files/', 
        blank=True, 
        verbose_name=_('file')
    )
    category = models.ForeignKey(
        ProductCategory, 
        null=True, 
        blank=True,     
        default='default',
        related_name='projects',
        on_delete=models.SET_NULL,
        verbose_name=_('category'), 
    )
    unfolded = models.BooleanField(
        default = False,
        verbose_name = _('unfolded'),
        help_text = _('Unfolded products can be bought by users')
    )
    public = models.BooleanField(
        default = False,
        verbose_name = _('public'),
        help_text = _('Public products diplay their content to anonimous users')
    ) 
    courtesy_short_message = models.CharField(
        blank=True, 
        max_length=50, 
        verbose_name=_('short courtesy messages')
    )
    courtesy_message = models.TextField(
        blank=True, 
        verbose_name = _('courtesy message'),
        help_text = _('Folded products return this message to all users')
    )
    relatable = models.BooleanField(
        default=True, 
        verbose_name=_('relatable'),
        help_text = _('Activate to show related objects')
    ) 
    related_products = models.ManyToManyField(
        'self',
        related_name = 'products', 
        blank = True, 
        verbose_name = _('related products'),
    )
    related_articles = models.ManyToManyField(
        Article,
        related_name = 'products', 
        blank = True, 
        verbose_name = _('related articles'),
    )
    formats = models.ManyToManyField(
        ProductFormat, 
        blank = True, 
        related_name = 'products', 
        verbose_name = _('formats'),
    )
    stripe_price = models.CharField(
        blank = True,
        max_length = 50,
        verbose_name = _('stripe price')
    )
    stripe_product = models.CharField(
        unique = True,
        null = True,
        blank = True,
        max_length = 50,
        verbose_name = _('stripe product')
    )
    product_survey = models.ForeignKey(
        Survey, 
        related_name = 'product', 
        on_delete = models.SET_NULL, 
        null = True, 
        blank = True, 
        verbose_name = _('survey')
    )
    image = models.URLField(
        blank=True, 
        verbose_name = _('cover')
    )
    postcard = models.URLField(
        blank=True, 
        verbose_name = _('postcard')
    )

    def image_tag(self):
        return super(Product, self).image_tag()
    image_tag.short_description = _('Cover')

    def postcard_tag(self):
        return super(Product, self).image_tag(image_url=self.postcard)
    postcard_tag.short_description = _('Postcard')

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return '{} ({})'.format(self.title, self.category) 

    def class_name(self):
        return _('application')

    def get_absolute_url(self):
        return reverse('products:detail', args=[str(self.slug)])

    def get_lazy_absolute_url(self):
        return reverse_lazy('products:detail', args=[str(self.slug)])

    def search(self, query, *args, **kwargs):
        results = Product.objects.published()
        query_list = query.split()
        results = results.filter(
            reduce(operator.and_,
                   (Q(title__icontains=q) for q in query_list)) |
            reduce(operator.and_,
                   (Q(description__icontains=q) for q in query_list))
        )
        return results

    def reporting_public(self, *args, **kwargs):
        queryset_public = Product.objects.public()
        queryset_public = queryset_public.prefetch()
        results = []
        for product in queryset_public:
            results.append({
                'columns': 4,
                'name': '%(product)s' % {
                    'product': product.title,
                },
                'title': product.book.hit_count.hits,
                'description1': _('views in the last week: %(d)s') % {
                    'd': product.book.hit_count.hits_in_last(days=7),
                },
                'description2': '',
                'action': '',
            })
        return results

    def reporting_private(self, *args, **kwargs):
        queryset_not_public = Product.objects.not_public().exclude(category__meta_category=True)
        queryset_not_public = queryset_not_public.prefetch()
        results = []
        for product in queryset_not_public:
            last_purchase = Purchase.objects.last_purchase(product)
            prefix = _('Last purchase')
            customers_en = Purchase.objects.customers(product, 'en')
            customers_en_emails = Purchase.objects.customers_emails(product, 'en')
            customers_it = Purchase.objects.customers(product, 'it')
            customers_it_emails = Purchase.objects.customers_emails(product, 'it')
            results.append({
                'columns': 6,
                'name': _('%(product)s: total customers') % {
                    'product': product.title,
                },
                'title': product.customers.count(),
                'description1': _('%(en)s english customers, %(it)s italian customers') % {
                    'en': customers_en.count(),
                    'it': customers_it.count(),
                },
                'description2': last_purchase.get_description(prefix) if last_purchase is not None else prefix + ': -',
                'action': '',
            })

            results.append({
                'columns': 3,
                'name': _('%(product)s: english subscribers') % {
                    'product': product.title,
                },
                'title': customers_en_emails.count(),
                'action': {
                    'label': _('copy emails'), 
                    'function': 'copy-emails', 
                    'parameters': customers_en_emails,
                },
            })
            results.append({
                'columns': 3,
                'name': _('%(product)s: italian subscribers') % {
                    'product': product.title,
                },
                'title': customers_it_emails.count(),
                'action': {
                    'label': _('copy emails'),
                    'function': 'copy-emails',
                    'parameters': customers_it_emails,
                },
            })
        return results

    # Return True if the user has added the product to his collections
    def user_has_already_bought(self, user):
        return user in self.customers.all()

    # Return True if the user has authored this collection
    def user_has_authored(self, user):
        return user in self.authors.all()

    # Returns the default currency of any product
    def get_currency(self):
        return 'EUR'

    # Returns the publishable status of the product
    def get_status(self): 
        if self.published:
            return _('published')
        else:
            return _('draft')

    # Returns true if the product is free
    def _at_a_premium(self):
        if self.stripe_product and self.stripe_price:
            return True
        else:
            return False
    _at_a_premium.boolean = True
    _at_a_premium.short_description = _('at a premium')
    at_a_premium = property(_at_a_premium)


class ProductDetail(Element, HighlightedModel):
    """ A specific detail of a product."""
    product = models.ForeignKey(
        Product, 
        null = True, 
        related_name = 'details', 
        verbose_name = _('product'), 
        on_delete = models.SET_NULL,
    )

    class Meta:
        verbose_name = _('Detail')
        verbose_name_plural = _('Details')


class ChapterCategory(Category):
    """ Defines the type of a chapter. """
    class Meta:
        verbose_name = _('Chapter category')
        verbose_name_plural = _('Chapter categories')


class Chapter(Element, DiventiImageModel):
    """ A specific chapter of a product."""
    product = models.ForeignKey(Product, null=True, related_name='chapters', verbose_name=_('product'), on_delete=models.SET_NULL)     
    category = models.ForeignKey(ChapterCategory, null=True, verbose_name=_('category'), on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('Chapter')
        verbose_name_plural = _('Chapters')


class ImagePreview(Element, DiventiImageModel):    
    """A list of cool images of the product."""
    product = models.ForeignKey(Product, null=True, related_name='imagepreviews', verbose_name=_('product'), on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')


class PurchaseQuerySet(models.QuerySet):

    # Prefetch all relevant data
    def related(self):
        purchases = self.select_related('customer')
        purchases = purchases.select_related('product')
        return purchases

    # Returns the users that purchased the product
    # with "lan" as main language
    def customers(self, product, lan=None):
        purchases = self.filter(product=product)
        customers_id = purchases.values_list('customer')
        UserModel = get_user_model() 
        customers = UserModel.objects.filter(id__in=customers_id)
        if lan:
            customers = customers.filter(language=lan)
        customers = customers.is_active()
        return customers

    # Returns the emails of users that purchased the product
    # with "lan" as main language
    def customers_emails(self, product, lan):
        customers = self.customers(product, lan)
        customers = customers.has_agreed_gdpr()
        customers = customers.values_list('email', flat=True)
        return customers

    # Returns the last customer that has purchased the product
    # with "lan" as main language
    def last_purchase(self, product, lan=None):
        purchases = self.related()
        purchases = purchases.filter(product=product)
        if lan:
            purchases = purchases.filter(customer__language=lan)
        last_purchase = purchases.order_by('-created').first()
        return last_purchase


class Purchase(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('product'))
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('customer'))

    objects = PurchaseQuerySet.as_manager()

    class Meta:
        verbose_name = _('Purchase')
        verbose_name_plural = _('Purchases')


    def __str__(self):
        return _('Purchase: %(id)s') % {'id': self.id}

    # Returns the description of the purchase
    # Or none if none is found
    def get_description(self, prefix):
        description = _('%(prefix)s: %(last_pur)s on %(created)s') % {
            'prefix': prefix,
            'last_pur': self.customer.get_short_name(),
            'created': naturalday(self.created),
        }
        return description