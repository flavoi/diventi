from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationStackedInline

from diventi.core.admin import DiventiTranslationAdmin, make_published, make_unpublished, deactivate
from .models import Survey, Question, Answer, SurveyCover, QuestionGroup, QuestionChoice, Outcome


class AnswerAdmin(DiventiTranslationAdmin):
    model = Answer
    list_display = ['question', 'author', 'get_score', 'content',]

    def get_form(self, request, obj=None, **kwargs):
        form = super(AnswerAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['author'].initial = request.user
        form.base_fields['author_name'].initial = request.user.get_full_name()
        return form


class QuestionChoiceInline(TranslationStackedInline):
    model = QuestionChoice
    fields = ('title', 'description', 'score')


class QuestionAdmin(DiventiTranslationAdmin):
    list_display = ['question', 'group']
    inlines = [QuestionChoiceInline]


class QuestionInline(TranslationStackedInline):
    model = Question
    fields = ('question',)
    extra = 1


class QuestionGroupAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'get_questions']
    inlines = [QuestionInline]


class OutcomeAdmin(DiventiTranslationAdmin):
    model = Outcome
    list_display = ['title', 'lower_score', 'medium_score', 'upper_score',]


class SurveyAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'get_question_groups', 'published', 'publication_date']
    readonly_fields = ['created', 'modified', 'publication_date']
    prepopulated_fields = {"slug": ("title",)} 
    fieldsets = (
        (_('Management'), {
            'fields': ('published',)
        }),
        (_('Editing'), {
            'fields': ('title', 'description', 'question_groups', 'outcome', 'slug', 'publication_date'),
        }),
    )
    actions = [make_published, make_unpublished]
    inlines = []


class SurveyCoverAdmin(DiventiTranslationAdmin):
    list_display= ('label', 'image_tag', 'active')
    actions = [deactivate]


admin.site.register(Outcome, OutcomeAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionGroup, QuestionGroupAdmin)
admin.site.register(SurveyCover, SurveyCoverAdmin)
