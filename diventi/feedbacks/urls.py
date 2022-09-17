from django.conf.urls import url
from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (
	AnswerListView,
	survey_questions,
    survey_questions_private,
    survey_questions_public,
	new_answers_gate,
    survey_done_quick,
)

app_name = 'feedbacks'

urlpatterns = [
    path(_('<slug:slug>/new-submit/'), new_answers_gate, name='new_answers_gate'),
    path(_('<slug:slug>/questions/gate/'), survey_questions, name='questions'),
    path(_('<slug:slug>/questions/gate/<str:author_name>/'), survey_questions, name='questions_author'),
    path(_('<slug:slug>/questions/private/'), survey_questions_private, name='questions_private'),
    path(_('<slug:slug>/questions/private/<str:author_name>/'), survey_questions_private, name='questions_author_private'),
    path(_('<slug:slug>/questions/public/'), survey_questions_public, name='questions_public'),
    path(_('<slug:slug>/questions/public/<str:author_name>/'), survey_questions_public, name='questions_author_public'),
    path(_('<slug:slug>/answers/'), AnswerListView.as_view(), name='answers'),
    path(_('<slug:slug>/survey-done/'), survey_done_quick, name='survey_done')
    

]