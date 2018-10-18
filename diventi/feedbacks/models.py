from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe
from django.urls import reverse

from cuser.middleware import CuserMiddleware

from diventi.core.models import TimeStampedModel, PublishableModel, DiventiCoverModel, DiventiImageModel
from diventi.accounts.models import DiventiUser


class QuestionGroup(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('title'))
    description = models.TextField(verbose_name=_('description'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('question group')
        verbose_name_plural = _('question groups')

    def get_questions(self):
        return mark_safe("<br>".join([s.question for s in self.questions.all()]))
    get_questions.short_description = _('Questions')


class Question(models.Model):
    question = models.CharField(max_length=200, verbose_name=_('question'))
    group = models.ForeignKey(QuestionGroup, related_name='questions', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')

    def __str__(self):
        return self.question


class SurveyQuerySet(models.QuerySet):
    
    # Get the list of published surveys
    def published(self):
        user = CuserMiddleware.get_user()
        if user.is_superuser:
            surveys = self
        else:
            surveys = self.filter(published=True)
        return surveys

    # Get the list of published surveys from the most recent to the least 
    def history(self):
        surveys = self.published().order_by('-publication_date')
        return surveys

    # Fetch all questions related to a survey
    def questions(self):
        survey = self.prefetch_related('questions')
        return survey

    # Fetch all answers related to a survey
    def answers(self):
        survey = self.prefetch_related('answers')
        return survey        


class Survey(TimeStampedModel, PublishableModel):
    """
        A collection of questions and answers centered around a specifi title.
    """
    title = models.CharField(max_length=60, verbose_name=_('title'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    slug = models.SlugField(unique=True, verbose_name=_('slug'))
    question_groups = models.ManyToManyField(QuestionGroup, related_name='surveys')

    objects = SurveyQuerySet.as_manager()

    class Meta:
        verbose_name = _('survey')
        verbose_name_plural = _('survey')
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('feedbacks:answers', args=[str(self.slug)])

    def get_question_groups(self):
        return mark_safe("<br>".join([s.__str__() for s in self.question_groups.all()]))
    get_question_groups.short_description = _('Question Groups')


class SurveyCover(DiventiCoverModel):
    """
        Stores cover images for the survey page.
    """
    class Meta:
        verbose_name = _('Survey Cover')
        verbose_name_plural = _('Survey Covers')


class Answer(models.Model):
    author = models.ForeignKey(DiventiUser, on_delete=models.SET_NULL, blank=True, null=True)
    author_name = models.CharField(max_length=60, verbose_name=_('author name'))
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.SET_NULL, null=True)
    survey = models.ForeignKey(Survey, related_name='answers', on_delete=models.SET_NULL, null=True)
    content = models.TextField()

    class Meta:
        verbose_name = _('answer')
        verbose_name_plural = _('answers')
        unique_together = ('author_name', 'author', 'question', 'survey')

    def __str__(self):
        return self.author_name