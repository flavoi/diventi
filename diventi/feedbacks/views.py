from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.utils.translation import ugettext_lazy as _
from django.db.models import Sum
from django.contrib import messages
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required

from diventi.core.views import DiventiActionMixin

from .models import Survey, Answer, Question, QuestionGroup
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
        qs = qs.select_related('question__group')
        return qs

    def get_context_data(self, **kwargs):
        context = super(AnswerListView, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', None)
        survey = Survey.objects.published().get(slug=slug)    
        outcome = survey.outcome
        if outcome is not None:
            answers_outcome = self.get_queryset().aggregate(Sum('choice__score'))
            # Generic calculation of the survey outcome
            # @myself: consider to improve the algorithm
            answers_score_value = answers_outcome['choice__score__sum']
            if answers_score_value:
                if answers_score_value >= outcome.upper_score - outcome.upper_score / 10:
                    answers_outcome['result'] = outcome.upper_outcome
                elif answers_score_value >= outcome.lower_score:
                    answers_outcome['result'] = outcome.medium_outcome
                elif answers_score_value < outcome.lower_score:
                    answers_outcome['result'] = outcome.lower_outcome
                answers_outcome['lower_score'] = outcome.lower_score
                answers_outcome['upper_score'] = outcome.upper_score
                answers_outcome['progress'] = answers_score_value / outcome.upper_score * 100
        else:
            answers_outcome = None
        context['survey'] = survey
        context['answers_outcome'] = answers_outcome 
        return context


@login_required
def survey_questions(request, slug):   

    survey = Survey.objects.published().get(slug=slug)
    question_groups = survey.question_groups.all()
    questions = Question.objects.filter(group__in=(question_groups)).order_by('group__order_index')

    user_has_answered = Answer.objects.filter(author=request.user, survey=survey).exists()
    if user_has_answered:
        return redirect(reverse('feedbacks:answers', args=[slug,]))

    DiventiAnswerFormSet = formset_factory(AnswerForm, max_num=1)
    
    question_data = [{
            'group_title': question.group.title,
            'group_description': question.group.description,
            'question': question, 
            'survey': survey
        } for question in questions]

    formset = DiventiAnswerFormSet(request.POST or None, initial=question_data)

    if request.method == 'POST':
        if formset.is_valid():
            for form in formset:
                form.save()
            messages.success(request, _('Your survey has been saved!'))
            return redirect(reverse('feedbacks:answers', args=[slug,]))              
        else:
            messages.warning(request, _('Please, double check your answers below.'))

    template_name = 'feedbacks/answer_form.html'
    context = {
        'survey': survey,
        'formset': formset
    }
    return render(request, template_name, context)    
