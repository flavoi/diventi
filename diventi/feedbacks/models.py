from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe
from django.urls import reverse, reverse_lazy
from django.template.defaultfilters import truncatechars

from cuser.middleware import CuserMiddleware

from diventi.core.models import (
    TimeStampedModel, 
    PublishableModel, 
    DiventiCoverModel, 
    DiventiImageModel, 
    FeaturedModel, 
    FeaturedModelQuerySet
)

SHORT_STRINGS_LENGTH = 60


class QuestionGroup(models.Model):
    """
        A question group is a collection of questions centered around a certain topic.
    """
    title = models.CharField(max_length=200, verbose_name=_('title'))
    description = models.TextField(verbose_name=_('description'))
    order_index = models.PositiveIntegerField(verbose_name=_('order index'))

    def __str__(self):
        return '(%s) %s' % (self.order_index, self.title)

    class Meta:
        verbose_name = _('question group')
        verbose_name_plural = _('question groups')

    def get_questions(self):
        return mark_safe("<br>".join([s.question for s in self.questions.all()]))
    get_questions.short_description = _('Questions')


class Question(models.Model):
    """
        A question must be part of a question group to be applied to a survey. 
    """
    question = models.CharField(max_length=200, verbose_name=_('question'))
    group = models.ForeignKey(QuestionGroup, related_name='questions', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')

    def __str__(self):
        return self.question

    @property
    def short_question(self):
        return truncatechars(self.question, SHORT_STRINGS_LENGTH)
        

class QuestionChoice(models.Model):
    """
        A model that defines the choice of a closed question.
    """
    title = models.CharField(max_length=200, verbose_name=_('title'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    score = models.PositiveIntegerField(default=0, verbose_name=_('score'))
    question = models.ForeignKey(Question, null=True, on_delete=models.SET_NULL, related_name='choices')

    class Meta:
        verbose_name = _('choice')
        verbose_name_plural = _('choices')

    def __str__(self):
        return self.title

        
class SurveyQuerySet(FeaturedModelQuerySet):
    
    # Get the list of published surveys from the most recent to the least 
    def history(self):
        surveys = self.published().order_by('-publication_date')
        return surveys

    # Fetch all answers related to a survey
    def answers(self):
        survey = self.prefetch_related('answers')
        return survey

    # Fetch the surveys authored by the user
    def user_collection(self, user):
        surveys = self.filter(answers__author=user)
        surveys = surveys.distinct()
        return surveys


class Survey(TimeStampedModel, DiventiImageModel, PublishableModel):
    """
        A collection of questions and answers centered around a specifi title.
    """
    title = models.CharField(max_length=60, verbose_name=_('title'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    slug = models.SlugField(unique=True, verbose_name=_('slug'))
    question_groups = models.ManyToManyField(QuestionGroup, related_name='surveys', verbose_name=_('question groups'))
    public = models.BooleanField(verbose_name=_('public'))
    
    objects = SurveyQuerySet.as_manager()

    class Meta:
        verbose_name = _('survey')
        verbose_name_plural = _('surveys')
    
    def __str__(self):
        return self.title

    def class_name(self):
        return _('survey')

    def get_absolute_url(self):
        return reverse('feedbacks:questions', args=[str(self.slug)])

    def get_lazy_absolute_url(self):
        return reverse_lazy('feedbacks:new_answers_gate', args=[str(self.slug)])

    def get_question_groups(self):
        return mark_safe("<br>".join([s.__str__() for s in self.question_groups.all()]))
    get_question_groups.short_description = _('Question Groups')

    # Returns true if the user has answered this survey
    def user_has_answered(self, user):
        return self.answers.filter(author=user).exists()


class AnswerQuerySet(models.QuerySet):

    def prefetch(self):
        answers = self.select_related('question__group')
        return answers

    # Fetch all answers related to a survey
    def user_survey(self, user, survey):
        answers = self.filter(author=user)
        answers = answers.filter(survey=survey)
        answers = answers.prefetch()
        return answers


class Answer(TimeStampedModel):
    """
        One answer can be given for each question. If the question provides a score, the answer get it too.
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,         
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        related_name='answers',
        verbose_name=_('author'),
    )
    author_name = models.CharField(
        max_length=60, 
        verbose_name=_('author name'),
    )
    question = models.ForeignKey(
        Question, 
        related_name='answers', 
        verbose_name=_('question'), 
        on_delete=models.SET_NULL, 
        null=True,
    )
    survey = models.ForeignKey(
        Survey, 
        related_name='answers', 
        on_delete=models.SET_NULL, 
        null=True,
    )
    choice = models.ForeignKey(
        QuestionChoice, 
        related_name='answers', 
        on_delete=models.SET_NULL, 
        null=True,
    )
    content = models.TextField(
        verbose_name=_('content'),
    )

    objects = AnswerQuerySet.as_manager()
    
    class Meta:
        verbose_name = _('answer')
        verbose_name_plural = _('answers')
        unique_together = ('author_name', 'author', 'question', 'survey')

    def get_score(self):
        if self.choice:
            score = self.choice.score
        else:
            score = ''
        return mark_safe("%s" % score)
    get_score.short_description = _('Score')

    def __str__(self):
        return self.author_name

    @property
    def short_content(self):
        return truncatechars(self.content, SHORT_STRINGS_LENGTH)

    @property
    def short_question(self):
        return truncatechars(self.question, SHORT_STRINGS_LENGTH)
        

        

