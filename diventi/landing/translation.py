from modeltranslation.translator import register, TranslationOptions

from .models import (
	Feature, 
	Section, 
	SearchSuggestion,
    AboutArticle,
    SectionImage,
    LandingPage,
)


@register(Feature)
class FeatureTranslationOptions(TranslationOptions):
    fields = ('prefix', 'title', 'subtitle', 'description',)


@register(Section)
class SectionTranslationOptions(TranslationOptions):
    fields = ('slug', 'prefix', 'title', 'subtitle', 'short_description', 'description', 'button_label',)


@register(SearchSuggestion)
class SearchSuggestionOptions(TranslationOptions):
    fields = ('title', 'description',)


@register(AboutArticle)
class AboutArticleOptions(TranslationOptions):
    fields = ('title', 'description', 'content', 'slug')


@register(SectionImage)
class SectionImageTranslationOptions(TranslationOptions):
    fields = ('label', )


@register(LandingPage)
class FeatureTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'slug')
