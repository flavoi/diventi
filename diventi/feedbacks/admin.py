from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationStackedInline

from diventi.core.admin import DiventiTranslationAdmin, make_published, make_unpublished, deactivate
from .models import Survey, Question, Answer, QuestionGroup, QuestionChoice, Outcome


class AnswerAdmin(DiventiTranslationAdmin):
    model = Answer
    list_display = ['question', 'author', 'author_name', 'get_score', 'content', 'created', 'modified']
    readonly_fields = ['created', 'modified']

    def get_form(self, request, obj=None, **kwargs):
        form = super(AnswerAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['author'].initial = request.user
        form.base_fields['author_name'].initial = request.user.get_full_name()
        return form


class QuestionChoiceInline(TranslationStackedInline):
    model = QuestionChoice
    fields = ('title', 'score')


class QuestionAdmin(DiventiTranslationAdmin):
    list_display = ['short_question', 'group']
    inlines = [QuestionChoiceInline]


class QuestionInline(TranslationStackedInline):
    model = Question
    fields = ('question',)
    extra = 1


class QuestionGroupAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'order_index', 'get_questions']
    inlines = [QuestionInline]
    ordering = ('order_index',)


class OutcomeAdmin(DiventiTranslationAdmin):
    model = Outcome
    list_display = ['title', 'lower_score', 'medium_score', 'upper_score',]


class SurveyAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'image_tag', 'get_question_groups', 'published', 'publication_date', 'public']
    readonly_fields = ['created', 'modified', 'publication_date']
    prepopulated_fields = {"slug": ("title",)} 
    fieldsets = (
        (_('Management'), {
            'fields': ('published', 'featured', 'public')
        }),
        (_('Editing'), {
            'fields': ('title', 'image', 'description', 'question_groups', 'outcome', 'slug', 'publication_date'),
        }),
    )
    actions = [make_published, make_unpublished]
    inlines = []



admin.site.register(Outcome, OutcomeAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionGroup, QuestionGroupAdmin)
