from modeltranslation.translator import register, TranslationOptions

from .models import Product, Chapter, Characteristic, ImagePreview, ProductCategory, ChapterCategory


@register(ProductCategory)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'file', 'slug',)


@register(ChapterCategory)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Chapter)
class ChapterTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


@register(Characteristic)
class CharacteristicTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


@register(ImagePreview)
class ImagePreviewTranslationOptions(TranslationOptions):
    fields = ('label',)