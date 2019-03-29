from django.conf.urls import url
from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import SurveyListView, AnswerListView, AnswerListViewByName, survey_questions

app_name = 'feedbacks'

urlpatterns = [
    path('', SurveyListView.as_view(), name='list'),
    path(_('<slug:slug>/questions/'), survey_questions, name='questions'),
    path(_('<slug:slug>/answers/'), AnswerListView.as_view(), name='answers'),
    path(_('<slug:slug>/answers/<str:author_name>'), AnswerListViewByName.as_view(), name='answers-author'),
]