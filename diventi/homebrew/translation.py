from modeltranslation.translator import register, TranslationOptions

from diventi.core.admin import DiventiTranslationAdmin

from .models import Paper, Section, Watermark, DiceTable, DiceTableRow, Itemize, ItemizeItem, CharacterBlock, CharacterItem


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
class DiceTableTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(DiceTableRow)
class DiceTableRowTranslationOptions(TranslationOptions):
    fields = ('description',)


@register(Itemize)
class ItemizeTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(ItemizeItem)
class ItemizeItemTranslationOptions(TranslationOptions):
    fields = ('description',)


@register(CharacterBlock)
class CharacterBlockTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(CharacterItem)
class CharacterItemTranslationOptions(TranslationOptions):
    fields = ('title', 'description')