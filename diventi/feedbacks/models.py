from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe

from diventi.core.models import TimeStampedModel, PublishableModel
from diventi.accounts.models import DiventiUser


class Question(models.Model):
    question = models.CharField(max_length=200, verbose_name=_('question'))

    def __str__(self):
        return self.question


class Survey(TimeStampedModel, PublishableModel):
    """
        A collection of questions and answers centered around a specifi title.
    """
    title = models.CharField(max_length=60, verbose_name=_('title'))
    slug = models.SlugField(unique=True, verbose_name=_('slug'))
    questions = models.ManyToManyField(Question)

    class Meta:
        verbose_name = _('survey')
        verbose_name_plural = _('survey')
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('', args=[str(self.slug)])

    def get_questions(self):
        return mark_safe("<br>".join([s.question for s in self.questions.all()]))


class Answer(models.Model):
    author = models.OneToOneField(DiventiUser, on_delete=models.SET_NULL, blank=True, null=True)
    author_name = models.CharField(max_length=60, verbose_name=_('author name'))
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    survey = models.OneToOneField(Survey, on_delete=models.SET_NULL, null=True)
    content = models.TextField()

    def __str__(self):
        return self.author_name