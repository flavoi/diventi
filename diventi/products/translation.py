from modeltranslation.translator import register, TranslationOptions

from .models import Product, Chapter, ImagePreview, ProductCategory, ChapterCategory


@register(ProductCategory)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'abstract', 'description', 'file', 'slug', 'courtesy_message')


@register(ChapterCategory)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Chapter)
class ChapterTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


@register(ImagePreview)
class ImagePreviewTranslationOptions(TranslationOptions):
    fields = ('label', 'image') # A preview can cointain text that has to be translated