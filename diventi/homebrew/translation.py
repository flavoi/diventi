from modeltranslation.translator import register, TranslationOptions

from diventi.core.admin import DiventiTranslationAdmin

from .models import Paper, Section, Watermark, DiceTable, DiceTableRow, Itemize, ItemizeItem


@register(Paper)
class PaperTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'slug')


@register(Section)
class SectionTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


@register(Watermark)
class WatermarkTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(DiceTable)
class WatermarkTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(DiceTableRow)
class WatermarkTranslationOptions(TranslationOptions):
    fields = ('description',)


@register(Itemize)
class WatermarkTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(ItemizeItem)
class WatermarkTranslationOptions(TranslationOptions):
    fields = ('description',)