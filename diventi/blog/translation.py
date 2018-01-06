from modeltranslation.translator import register, TranslationOptions

from .models import Category, Article


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'caption', 'content', 'hot', 'slug')