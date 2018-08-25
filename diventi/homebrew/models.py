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


class DiceTable(models.Model):
    """
        A dice table has two columns: the first is an automatic value of the dice, 
        the second is a free description.
    """
    DICES = [
        ('20', 'd20'),
        ('12', 'd12'),
        ('10', 'd10'),
        ('8', 'd8'),
        ('6', 'd6'),
        ('4', 'd4'),
    ]
    dice = models.CharField(max_length=3, choices=DICES, verbose_name=_('dice'))
    title = models.CharField(max_length=60, verbose_name=_('title'))

    def __str__(self):
        return self.title


class DiceTableRow(models.Model):
    description = models.TextField(verbose_name=_('description'))
    dicetable = models.ForeignKey(DiceTable, on_delete=models.CASCADE, related_name=_('rows'))

    def __str__(self):
        return self.description


class Section(TimeStampedModel):
    """
        Each section type needs a function that renders the content of the paper
        in latex. If blank the Brew will display the title as plain string.
    """
    order_id = models.PositiveIntegerField(unique=True, verbose_name=_('order_id')) # This affects the display order of every piece of content
    title = models.CharField(max_length=60, verbose_name=_('title'))
    content = models.TextField(verbose_name=_('content'))
    SECTION_TYPES = [
        ('section', _('section')),
        ('subsection', _('subsection')),
        ('commentbox', _('commentbox')),
        ('quotebox', _('quotebox')),
        ('paperbox', _('paperbox')),
        ('dicetable', _('dicetable')),
    ]
    section_type = models.CharField(max_length=30, blank=True, choices=SECTION_TYPES, verbose_name=_('section type'))
    THEMES = [
        ('PhbLightGreen', _('light green')),
        ('PhbLightCyan', _('light chan')),
        ('PhbMauve', _('muave')), 
        ('PhbTan', _('tan')),
        ('DmgLavender', _('lavender')),
        ('DmgCoral', _('coral')),
        ('DmgSlateGray', _('slate gray')), 
        ('DmgLilac', _('lilac')),
    ]
    theme = models.CharField(max_length=30, blank=True, choices=THEMES, verbose_name=_('theme')) 
    paper = models.ForeignKey(Paper, null=True, on_delete=models.SET_NULL, related_name=_('sections'))
    table = models.OneToOneField(DiceTable, null=True, blank=True, on_delete=models.SET_NULL, related_name=('section'))
    new_page = models.BooleanField(default=False, verbose_name=_('new page'))
    title_page = models.BooleanField(default=False, verbose_name=_('title page'))

    def __str__(self):
        return self.title

    def __repr__ (self):
        if self.section_type:
            return getattr(Section, self.section_type)(self)
        elif self.title_page:
            return ""
        else:
            return self.__str__()

    def titlepage(self):
        return """
            \\phantom{Invisible text}"""

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
            \\begin{commentbox}{%s}[%s]
                %s
            \\end{commentbox}""" % (self.title, self.theme, self.content)

    def quotebox(self):
        return """
            \\begin{quotebox}[%s]
                %s
            \\end{quotebox}""" % (self.theme, self.content)

    def paperbox(self):
        return """
            \\begin{paperbox}{%s}[%s]
                %s
            \\end{paperbox}""" % (self.title, self.theme, self.content)

    def dicetable(self):
        return """
            \\header{%s}""" % self.__str__() # The header of the table


class Watermark(TimeStampedModel):
    """
        Any page can be customized with cool backgrounds thanks to one or more
        watermarks.
    """
    title = models.CharField(max_length=60, verbose_name=_('title'))
    pages = models.CharField(max_length=10, verbose_name=_('pages'))
    scale = models.FloatField(default=1)
    xpos = models.IntegerField()
    ypos = models.IntegerField()
    figurename = models.CharField(max_length=60, verbose_name=_('figure name'))
    paper = models.ForeignKey(Paper, null=True, on_delete=models.SET_NULL, related_name='watermarks')

    def __str__(self):
        return self.title

