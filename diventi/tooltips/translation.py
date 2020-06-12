from modeltranslation.translator import register, TranslationOptions

from .models import (
    Tooltip,
    TooltipGroup,
)

@register(Tooltip)
class TooltipTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(TooltipGroup)
class TooltipGroupTranslationOptions(TranslationOptions):
    fields = ('title',)