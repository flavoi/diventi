from modeltranslation.translator import register, TranslationOptions

from .models import DiventiAvatar, DiventiCover, Achievement


@register(DiventiAvatar)
class DiventiAvatarTranslationOptions(TranslationOptions):
    fields = ('label',)


@register(DiventiCover)
class DiventiCoverTranslationOptions(TranslationOptions):
    fields = ('label',)


@register(Achievement)
class AchievementTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)