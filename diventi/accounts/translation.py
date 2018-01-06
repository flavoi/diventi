from modeltranslation.translator import register, TranslationOptions

from .models import DiventiAvatar, DiventiCover


@register(DiventiAvatar)
class DiventiAvatarTranslationOptions(TranslationOptions):
    fields = ('label',)


@register(DiventiCover)
class DiventiCoverTranslationOptions(TranslationOptions):
    fields = ('label',)