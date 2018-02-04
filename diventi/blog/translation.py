from modeltranslation.translator import register, TranslationOptions

from .models import ArticleCategory, Article, BlogCover


@register(ArticleCategory)
class ArticleCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'caption', 'content', 'slug')


@register(BlogCover)
class BlogCoverTranslationOptions(TranslationOptions):
    fields = ('label',)