from django import forms
from django.utils.translation import gettext_lazy as _

from dal import autocomplete

from .models import Section, Chapter, Book


class SectionForm(forms.ModelForm):
    book = forms.ModelChoiceField(queryset=Book.objects.all())
    chapter = forms.ModelChoiceField(
        queryset=Chapter.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='ebooks:chapter-autocomplete',
            attrs={
                # Set some placeholder
                'data-placeholder': _('Autocomplete ...'),
                # Only trigger autocompletion after 3 characters have been typed
                'data-minimum-input-length': 3,
            },
            forward=['book'],
        )
    )

    class Meta:
        model = Section
        fields = ('__all__')