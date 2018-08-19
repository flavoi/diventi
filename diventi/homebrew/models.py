from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from diventi.core.models import TimeStampedModel, PublishableModel, DiventiImageModel


class Paper(TimeStampedModel):
    """
        A Paper is a document written in latex that contains fantastic adventures.
    """
    title = models.CharField(max_length=60, verbose_name=_('title'))
    description = models.TextField(max_length=250, verbose_name=_('description'))
    slug = models.SlugField(unique=True, verbose_name=_('slug'))

    class Meta:
        verbose_name = _('paper')
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('homebrew:detail', args=[str(self.slug)])


class Section(TimeStampedModel):
    """
        Each section type needs a function that renders the content of the paper
        in latex. If blank the Brew will display the title as plain string.
    """
    order_id = models.PositiveIntegerField(unique=True, verbose_name=_('order_id')) # This affects the display order of every piece of content
    title = models.CharField(max_length=60, verbose_name=_('title'))
    content = models.TextField(verbose_name=_('content'))
    SECTION_TYPES = [
        (_('section'), 'section'),
        (_('subsection'), 'subsection'),
        (_('commentbox'), 'commentbox'),
        (_('quotebox'), 'quotebox'),
    ]
    section_type = models.CharField(max_length=30, blank=True, choices=SECTION_TYPES, verbose_name=_('section_type'))    
    paper = models.ForeignKey(Paper, null=True, on_delete=models.SET_NULL, related_name='sections')

    def __str__(self):
        return self.content

    def __repr__ (self):
        if self.section_type:
            return getattr(Section, self.section_type)(self)
        else:
            return self.__str__()

    def section(self):
        return """
            \\subsection{%s}
                %s""" % (self.title, self.content)
    
    def subsection(self):
        return """
            \\subsubsection{%s}
                %s""" % (self.title, self.content)

    def commentbox(self):
        return """
            \\begin{commentbox}{%s}
                %s
            \\end{commentbox}""" % (self.title, self.content)

    def quotebox(self):
        return """
            \\begin{quotebox}
                %s
            \\end{quotebox}""" % (self.content)


class Watermark(TimeStampedModel):
    """
        Any page can be customized with cool backgrounds thanks to one or more
        watermarks.
    """
    title = models.CharField(max_length=60, verbose_name=_('title'))
    pages = models.CharField(max_length=10, verbose_name=_('pages'))
    scale = models.PositiveIntegerField(default=1)
    xpos = models.IntegerField()
    ypos = models.IntegerField()
    figurename = models.CharField(max_length=60, verbose_name=_('figure name'))
    paper = models.ForeignKey(Paper, null=True, on_delete=models.SET_NULL, related_name='watermarks')

    def __str__(self):
        return self.title

