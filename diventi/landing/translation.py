from modeltranslation.translator import register, TranslationOptions

from .models import (
	Feature, 
	Section, 
	SearchSuggestion,
    AboutArticle,
    PolicyArticle,
)


@register(Feature)
class FeatureTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


@register(Section)
class SectionTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


@register(SearchSuggestion)
class SearchSuggestionOptions(TranslationOptions):
    fields = ('title', 'description',)


@register(AboutArticle)
class AboutArticleOptions(TranslationOptions):
    fields = ('title', 'content', 'slug')


@register(PolicyArticle)
class AboutArticleOptions(TranslationOptions):
    fields = ('title', 'content', 'slug')