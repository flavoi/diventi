from django import forms
from django.utils.translation import gettext_lazy as _

from diventi.ebooks.forms import SectionProductForm

from .models import Tooltip


class TooltipForm(SectionProductForm):

    class Meta:
        model = Tooltip
        fields = ('group', 'title', 'product', 'section',)