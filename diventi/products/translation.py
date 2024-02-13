from modeltranslation.translator import register, TranslationOptions

from .models import (
    Product, 
    Chapter, 
    ImagePreview, 
    ProductCategory, 
    ChapterCategory, 
    ProductDetail,
    ProductFormat,
    ProductCover,
)


@register(ProductFormat)
class ProductFormatOptions(TranslationOptions):
    fields = ('title', 'description',)


@register(ProductDetail)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


@register(ProductCategory)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'title_plural', 'slug')


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'short_description', 'abstract', 'description', 'file', 'slug', 'courtesy_short_message', 'courtesy_message', 'related_forum_topic')


@register(ChapterCategory)
class ChapterCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Chapter)
class ChapterTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


@register(ImagePreview)
class ImagePreviewTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'image')


@register(ProductCover)
class ProductCoverTranslationOptions(TranslationOptions):
    fields = ('label', 'title', 'description')