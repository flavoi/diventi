from django import forms
from django.utils.translation import gettext_lazy as _

from dal import autocomplete

from diventi.ebooks.models import Section

from .models import (
    Adventure,
    Situation,
    Resolution,
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
        required=False,
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


class SituationStoryResolutionForm(forms.Form):
    enable_third_ring = forms.BooleanField(required=False)
    resolution =  forms.ModelChoiceField(
        queryset=Resolution.objects.all(),
        widget=forms.RadioSelect,
        empty_label=None,
    )

    def __init__(self, *args, **kwargs):
        ring = kwargs.pop('ring', False)
        super().__init__(*args, **kwargs)
        # Game master shouldn't be able to enable the third ring
        # if they have just started or finished their adventure.
        if ring == 'third' or ring == 'first':
            self.fields.pop('enable_third_ring')