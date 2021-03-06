from modeltranslation.translator import register, TranslationOptions

from .models import DiventiAvatar, DiventiProfilePic, DiventiCover, Achievement, DiventiUser, Role


@register(DiventiUser)
class DiventiAvatarTranslationOptions(TranslationOptions):
    fields = ('bio',)    


@register(DiventiAvatar)
class DiventiAvatarTranslationOptions(TranslationOptions):
    fields = ('label',)


@register(DiventiProfilePic)
class DiventiProfilePicTranslationOptions(TranslationOptions):
    fields = ('label',)


@register(DiventiCover)
class DiventiCoverTranslationOptions(TranslationOptions):
    fields = ('label',)


@register(Achievement)
class AchievementTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


@register(Role)
class RoleTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)