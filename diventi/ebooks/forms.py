from django import forms
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import capfirst

from dal import autocomplete

from .models import Section, Chapter, Book, UniversalSection


class SectionForm(forms.ModelForm):
    book = forms.ModelChoiceField(
        queryset=Book.objects.all(), 
        label=_('Book'),
        help_text = _('You can filter chapters by selecting the related book in this field.'),
        required = False,
    )
    chapter = forms.ModelChoiceField(
        queryset=Chapter.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='ebooks:chapter-autocomplete',
            attrs={
                'data-placeholder': _('Autocomplete ...'),
                'data-minimum-input-length': 3,
            },
            forward=['book'],
        ),
        label=_('Chapter'),
    )

    class Meta:
        model = Section
        fields = ('__all__')

    class Media:
        js = [
            'https://code.jquery.com/jquery-3.4.1.min.js',
            'autocomplete_light/jquery.init.js',
            'vendor/select2/dist/js/select2.full.js',
            #'vendor/select2/dist/js/i18n/en.js',
            #'vendor/select2/dist/js/i18n/it.js',
            'autocomplete_light/autocomplete.init.js',
            'autocomplete_light/forward.js',
            'autocomplete_light/select2.js',
            'autocomplete_light/jquery.post-setup.js'
        ]