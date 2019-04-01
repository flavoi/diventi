from django import forms
from django.utils.translation import ugettext_lazy as _

from diventi.products.models import Product
from diventi.feedbacks.models import Survey


class PresentationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PresentationForm, self).__init__(*args, **kwargs)
        LINK_CHOICES = {
            ('', '----'),
        }
        featured_product = Product.objects.featured()
        if featured_product:
            LINK_CHOICES.update([(featured_product.get_lazy_absolute_url(), '%s/%s' % (featured_product.class_name(), featured_product))])
        featured_survey = Survey.objects.featured()
        if featured_survey:
            featured_survey = featured_survey.get()
            LINK_CHOICES.update([(featured_survey.get_lazy_absolute_url(), '%s/%s' % (featured_survey.class_name(), featured_survey))])
        self.fields['featured_link'].widget = forms.Select(
            choices = LINK_CHOICES
            )