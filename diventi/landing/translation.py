from modeltranslation.translator import register, TranslationOptions

from .models import (
	Feature, 
	Section, 
	SearchSuggestion,
    AboutArticle,
    SectionImage,
)


@register(Feature)
class FeatureTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


@register(Section)
class SectionTranslationOptions(TranslationOptions):
    fields = ('prefix', 'title', 'subtitle', 'description', 'button_label','attachment_label',)


@register(SearchSuggestion)
class SearchSuggestionOptions(TranslationOptions):
    fields = ('title', 'description',)


@register(AboutArticle)
class AboutArticleOptions(TranslationOptions):
    fields = ('title', 'description', 'content', 'slug')


@register(SectionImage)
class SectionImageTranslationOptions(TranslationOptions):
    fields = ('label', )
