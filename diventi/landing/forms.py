from django import forms
from django.utils.translation import ugettext_lazy as _

from diventi.products.models import Product
from diventi.feedbacks.models import Survey
from diventi.accounts.models import DiventiUser


class SectionForm(forms.ModelForm): 
    def __init__(self, *args, **kwargs):
        super(SectionForm, self).__init__(*args, **kwargs)
        pass