from django.shortcuts import (
    render, 
    redirect,
    get_object_or_404,
)
from django.http import Http404
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.utils.translation import gettext as _
from django.db.models import Sum
from django.contrib import messages
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from diventi.core.views import DiventiActionMixin
from diventi.core.utils import send_diventi_email

from .models import Survey, Answer, Question, QuestionGroup
from .forms import AnswerForm, FeaturedSurveyInitForm

from cuser.middleware import CuserMiddleware


class AnswerListView(ListView, LoginRequiredMixin):

    model = Answer
    context_object_name = 'answers'
    template_name = 'feedbacks/answer_list_quick.html'
        
    def get_queryset(self):
        qs = super(AnswerListView, self).get_queryset()
        user = CuserMiddleware.get_user()
        slug = self.kwargs.get('slug', None)
        survey = get_object_or_404(Survey.objects.published(), slug=slug)
        qs = qs.user_survey(user=user, survey=survey)
        return qs

    def get_context_data(self, **kwargs):
        context = super(AnswerListView, self).get_context_data(**kwargs)
        author_name = self.request.user.get_full_name()
        slug = self.kwargs.get('slug', None)
        survey = get_object_or_404(Survey.objects.published(), slug=slug) 
        context['survey'] = survey
        context['author_name'] = author_name
        return context


@login_required
def survey_questions_private(request, slug, author_name=None):
    survey = get_object_or_404(Survey.objects.published(), slug=slug)
    author_name = request.user.get_full_name()
    user_has_answered = Answer.objects.filter(author=request.user, survey=survey).exists()
    author_name = request.user.get_full_name()
    user_has_answered = Answer.objects.filter(author=request.user, survey=survey).exists()  

    question_groups = survey.question_groups.all()
    questions = Question.objects.filter(group__in=(question_groups)).order_by('group__order_index')

    DiventiAnswerFormSet = formset_factory(AnswerForm, max_num=1)
    
    question_data = [{
            'group_title': question.group.title,
            'group_description': question.group.description,
            'question': question, 
            'survey': survey,
            'author_name': author_name,
        } for question in questions]
      
    formset = DiventiAnswerFormSet(request.POST or None, initial=question_data)

    if request.method == 'POST':
        if formset.is_valid():
            for form in formset:
                form.save()
            send_diventi_email(
                subject = _('Diventi: %(user)s has completed %(survey)s') % {'user': author_name, 'survey': survey.title,},
                message = None,
                from_email = 'autori@playdiventi.it',
                recipient_list = ['autori@playdiventi.it',],
                from_name = 'Diventi',
                html_message = _('Dear Diventi authors, new answers are now available for survey %(survey)s.') % {'survey': survey.title,},
            )
            request.session['user_has_answered'] = 1
            return redirect(reverse('feedbacks:survey_done', args=[slug,]))
        else:
            messages.warning(request, _('Please, double check your answers below.'))

    template_name = 'feedbacks/survey_form_quick.html'
    context = {
        'survey': survey,
        'formset': formset,
        'author_name': author_name,
    }
    return render(request, template_name, context)


def survey_questions_public(request, slug, author_name=None):
    survey = get_object_or_404(Survey.objects.published(), slug=slug)
    user_has_answered = Answer.objects.filter(author_name=author_name, survey=survey).exists()
    if user_has_answered and author_name != request.user.get_full_name():
        messages.warning(request, _('An other user already picked that name and answered, please choose another name.'))
        return redirect(reverse('feedbacks:new_answers_gate', args=[survey.slug,]))
    elif author_name is None:
        return redirect(reverse('feedbacks:new_answers_gate', args=[survey.slug,]))

    question_groups = survey.question_groups.all()
    questions = Question.objects.filter(group__in=(question_groups)).order_by('group__order_index')

    DiventiAnswerFormSet = formset_factory(AnswerForm, max_num=1)
    
    question_data = [{
            'group_title': question.group.title,
            'group_description': question.group.description,
            'question': question, 
            'survey': survey,
            'author_name': author_name,
        } for question in questions]
      
    formset = DiventiAnswerFormSet(request.POST or None, initial=question_data)

    if request.method == 'POST':
        if formset.is_valid():
            for form in formset:
                form.save()
            send_diventi_email(
                subject = _('Diventi: %(user)s has completed %(survey)s') % {'user': author_name, 'survey': survey.title,},
                message = None,
                from_email = 'autori@playdiventi.it',
                from_name = 'Diventi',
                recipient_list = ['autori@playdiventi.it',],
                html_message = _('Dear Diventi authors, new answers are now available for survey %(survey)s.') % {'survey': survey.title,},            
            )
            request.session['user_has_answered'] = 1
            return redirect(reverse('feedbacks:survey_done', args=[slug,]))
        else:
            messages.warning(request, _('Please, double check your answers below.'))

    template_name = 'feedbacks/survey_form_quick.html'
    context = {
        'survey': survey,
        'formset': formset,
        'author_name': author_name,
    }
    return render(request, template_name, context)


def survey_questions(request, slug, author_name=None):
    survey = get_object_or_404(Survey.objects.published(), slug=slug)
    if request.user.is_authenticated:
        return redirect(reverse('feedbacks:questions_private', args=[survey.slug,]))
    elif request.user.is_anonymous and survey.public:    
        return redirect(reverse('feedbacks:questions_public', args=[survey.slug,]))
    elif request.user.is_anonymous and survey.public and author_name:
        return redirect(reverse('feedbacks:questions_public', args=[survey.slug, author_name]))
    elif request.user.is_anonymous and not survey.public and author_name:
        return redirect(reverse('feedbacks:questions_author_private', args=[survey.slug, author_name]))
    elif request.user.is_anonymous and not survey.public and not author_name:
        return redirect(reverse('feedbacks:questions_private', args=[survey.slug,]))
    raise Http404(_('No survey found, please go back and redo your survey.'))


def survey_done_quick(request, slug):
    survey = get_object_or_404(Survey.objects.published(), slug=slug)
    if request.user.is_authenticated:
        user_has_answered = Answer.objects.filter(author=request.user, survey=survey).exists()
    else:
        user_has_answered = request.session.get('user_has_answered', None)
        del request.session['user_has_answered']
    if user_has_answered:        
        template_name = 'feedbacks/survey_done_quick.html'
        context = {
            'survey': survey,
        }
        return render(request, template_name, context)
    else:
        raise Http404(_('No survey found, please go back and redo your survey.'))    

def new_answers_gate(request, slug):

    survey = get_object_or_404(Survey.objects.published(), slug=slug)
    
    if request.user.is_authenticated:
        user_has_answered = Answer.objects.filter(author=request.user, survey=survey).exists()
        if user_has_answered:
            return redirect(reverse('feedbacks:answers', args=[slug,]))
        else:
            return redirect(reverse('feedbacks:questions', args=[slug,]))
    elif survey.public:
        if request.method == 'POST':
            form = FeaturedSurveyInitForm(request.POST)
            if form.is_valid():
                author_name = form.cleaned_data['author_name']
                user_has_answered = Answer.objects.filter(author_name=author_name, survey=survey).exists()
                if user_has_answered:
                    messages.warning(request, _('An other user already picked that name and answered, please choose another name.'))
                    return redirect(reverse('feedbacks:new_answers_gate', args=[survey.slug,]))
                else:
                    return redirect(reverse('feedbacks:questions_author', args=[slug, author_name]))
            else:
                messages.warning(request, _('There was an error while processing your survey.'))
                return redirect(reverse('feedbacks:new_answers_gate', args=[survey.slug,]))
        else:
            template_name = 'feedbacks/author_form_quick.html'
            featured_survey_data = {
                'survey': survey,
            }
            form = FeaturedSurveyInitForm(initial = featured_survey_data)
            context = {
                'survey': survey,
                'form': form,
            }
            return render(request, template_name, context)
    else:
        raise Http404(_("This survey is not open to public, sorry."))
