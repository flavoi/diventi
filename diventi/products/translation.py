from modeltranslation.translator import register, TranslationOptions

from .models import Product, Chapter, Characteristic, ImagePreview


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'slug')


@register(Chapter)
class ChapterTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


@register(Characteristic)
class CharacteristicTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


@register(ImagePreview)
class ImagePreviewTranslationOptions(TranslationOptions):
    fields = ('label',)