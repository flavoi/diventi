from django.conf.urls import url
from django.utils.translation import gettext_lazy as _

from .views import SurveyListView, AnswerListView, AnswerListViewByName, survey_questions

app_name = 'feedbacks'

urlpatterns = [
    url(r'^$', SurveyListView.as_view(), name='list'),
    url(_(r'^(?P<slug>[-\w]+)/questions/$'), survey_questions, name='questions'),
    url(_(r'^(?P<slug>[-\w]+)/answers/$'), AnswerListView.as_view(), name='answers'),
    url(_(r'^(?P<slug>[-\w]+)/answers/(?P<author_name>\w+)/$'), AnswerListView.as_view(), name='answers-author'),
]