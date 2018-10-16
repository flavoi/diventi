from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required

from diventi.core.views import DiventiActionMixin

from .models import Survey, Answer, Question, SurveyCover
from .forms import AnswerForm

from cuser.middleware import CuserMiddleware

class SurveyListView(ListView):

    model = Survey
    context_object_name = 'surveys'
    paginate_by = 6

    def get_queryset(self):
        return Survey.objects.history()


class AnswerListView(ListView):

    model = Answer
    context_object_name = 'answers'
        
    def get_queryset(self):
        qs = super(AnswerListView, self).get_queryset()
        user = CuserMiddleware.get_user()
        slug = self.kwargs.get('slug', None)
        survey = Survey.objects.published().get(slug=slug)
        qs = qs.filter(survey=survey)
        qs = qs.filter(author=user)
        return qs

    def get_context_data(self, **kwargs):
        context = super(AnswerListView, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        survey = Survey.objects.published().get(slug=slug)
        context['survey'] = survey        
        return context


@login_required
def survey_questions(request, slug):
    survey = Survey.objects.published().get(slug=slug)
    surveycover = SurveyCover.objects.active()
    questions = survey.questions.all()
    question_data = [{'question': question, 'survey': survey} for question in questions]
    
    DiventiAnswerFormSet = formset_factory(AnswerForm, max_num=1)
    formset = DiventiAnswerFormSet(request.POST or None, initial=question_data)
    if formset.is_valid():
        for answer_form in formset:
            if answer_form.is_valid():
                instance = answer_form.save(commit=False)
                instance.author_name = request.user.get_full_name()
                instance.author = request.user
                instance.save()
        messages.success(request, _('Your survey has been saved!'))                
    
    user_has_answered = Answer.objects.filter(author=request.user, survey=survey).exists()
    if user_has_answered:
        return redirect(reverse('feedbacks:answers', args=[slug,]))

    combined = zip(questions, formset.forms)

    template_name = 'feedbacks/answer_form.html'
    context = {
        'survey': survey,
        'surveycover': surveycover,
        'formset': formset,
        'combined': combined,
    }
    return render(request, template_name, context)    