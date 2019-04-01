from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe
from django.urls import reverse, reverse_lazy
from django.template.defaultfilters import truncatechars

from cuser.middleware import CuserMiddleware

from diventi.core.models import TimeStampedModel, PublishableModel, DiventiCoverModel, DiventiImageModel, FeaturedModel, FeaturedModelQuerySet
from diventi.accounts.models import DiventiUser


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
        A qeustion must be part of a question group to be applied to a survey. 
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


class Outcome(models.Model):
    """
        An outcome take in account the sum of the answers scores and produces 
        an authomatic result based on certain indexes.
    """
    title = models.CharField(max_length=60, verbose_name=_('title'))
    upper_score = models.PositiveIntegerField(default=0, verbose_name=_('upper score'))
    upper_outcome = models.TextField(verbose_name=_('upper outcome'))
    medium_score = models.PositiveIntegerField(default=0, verbose_name=_('medium score'))
    medium_outcome = models.TextField(verbose_name=_('medium outcome'))
    lower_score = models.PositiveIntegerField(default=0, verbose_name=_('lower score'))
    lower_outcome = models.TextField(verbose_name=_('lower outcome'))

    class Meta:
        verbose_name = _('outcome')
        verbose_name_plural = _('outcomes')

    def __str__(self):
        return self.title


class Survey(TimeStampedModel, PublishableModel, DiventiImageModel, FeaturedModel):
    """
        A collection of questions and answers centered around a specifi title.
    """
    title = models.CharField(max_length=60, verbose_name=_('title'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    slug = models.SlugField(unique=True, verbose_name=_('slug'))
    question_groups = models.ManyToManyField(QuestionGroup, related_name='surveys', verbose_name=_('question groups'))
    outcome = models.OneToOneField(Outcome, related_name='survey', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('outcome'))
    
    objects = SurveyQuerySet.as_manager()

    class Meta:
        verbose_name = _('survey')
        verbose_name_plural = _('surveys')
    
    def __str__(self):
        return self.title

    def class_name(self):
        return _('survey')

    def get_absolute_url(self):
        return reverse('feedbacks:answers', args=[str(self.slug)])

    def get_lazy_absolute_url(self):
        return reverse_lazy('feedbacks:new_answers_gate', args=[str(self.slug)])

    def get_question_groups(self):
        return mark_safe("<br>".join([s.__str__() for s in self.question_groups.all()]))
    get_question_groups.short_description = _('Question Groups')


class Answer(models.Model):
    """
        One answer can be given for each question. If the question provides a score, the answer get it too.
    """
    author = models.ForeignKey(DiventiUser, verbose_name=_('author'), on_delete=models.SET_NULL, blank=True, null=True)
    author_name = models.CharField(max_length=60, verbose_name=_('author name'))
    question = models.ForeignKey(Question, related_name='answers', verbose_name=_('question'), on_delete=models.SET_NULL, null=True)
    survey = models.ForeignKey(Survey, related_name='answers', on_delete=models.SET_NULL, null=True)
    choice = models.ForeignKey(QuestionChoice, related_name='answers', on_delete=models.SET_NULL, null=True)
    content = models.TextField(verbose_name=_('content'))

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
        

        

