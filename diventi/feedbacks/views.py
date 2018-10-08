from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .models import Survey


class SurveyListView(ListView):

    model = Survey
    context_object_name = 'surveys'
    paginate_by = 6

    def get_queryset(self):
        return Survey.objects.history()


class SurveyDetailView(DetailView):

    model = Survey
    context_object_name = 'survey'

    def get_queryset(self):
        qs = super(SurveyDetailView, self).get_queryset()
        return qs.published()
