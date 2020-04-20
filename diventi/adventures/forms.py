from django import forms
from django.utils.translation import gettext_lazy as _

from dal import autocomplete

from diventi.ebooks.models import Section

from .models import (
    Adventure,
    Situation,
)


class AdventureForm(forms.ModelForm):
    section = forms.ModelChoiceField(
        queryset=Section.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='ebooks:section-autocomplete-book',
            attrs={
                'data-placeholder': _('Autocomplete ...'),
                'data-minimum-input-length': 3,
            },
            forward=['product'],
        ),
        label=_('Section'),
    )

    class Meta:
        model = Adventure
        fields = ('title', 'ring', 'product', 'section')

    class Media:
        js = [
            'https://code.jquery.com/jquery-3.4.1.min.js',
        ]


class SituationCreateForm(forms.ModelForm):
    adventure = forms.ModelChoiceField(
        queryset=Adventure.objects.first_rings(),
    )
    class Meta:       
        model = Situation
        fields = ['adventure',]