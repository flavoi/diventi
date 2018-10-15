from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationStackedInline

from diventi.core.admin import DiventiTranslationAdmin, make_published, make_unpublished, deactivate
from .models import Survey, Question, Answer, SurveyCover


class AnswerAdmin(DiventiTranslationAdmin):
    model = Answer
    list_display = ['survey', 'question', 'author_name', 'author', 'content']

    def get_form(self, request, obj=None, **kwargs):
        form = super(AnswerAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['author'].initial = request.user
        form.base_fields['author_name'].initial = request.user.get_full_name()
        return form


class QuestionAdmin(DiventiTranslationAdmin):
    model = Question


class SurveyAdmin(DiventiTranslationAdmin):
    list_display = ['title', 'image_tag', 'get_questions', 'published', 'publication_date']
    readonly_fields = ['created', 'modified', 'publication_date']
    prepopulated_fields = {"slug": ("title",)} 
    fieldsets = (
        (_('Management'), {
            'fields': ('published',)
        }),
        (_('Editing'), {
            'fields': ('title', 'image', 'description', 'questions', 'slug', 'publication_date'),
        }),
    )
    actions = [make_published, make_unpublished]
    inlines = []


class SurveyCoverAdmin(DiventiTranslationAdmin):
    list_display= ('label', 'image_tag', 'active')
    actions = [deactivate]


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(SurveyCover, SurveyCoverAdmin)
