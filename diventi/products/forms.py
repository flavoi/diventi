from django import forms

from diventi.accounts.models import DiventiUser
from .models import Product


class UserCollectionUpdateForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['slug']
        widgets = {
            'slug': forms.HiddenInput(),
        }


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        users = DiventiUser.objects.filter(is_staff=True);
        # Staff users only cam be authors
        w = self.fields['authors'].widget
        choices = []
        for choice in users:
            choices.append((choice.id, choice))
        w.choices = choices
        # Products should not be related to themselves but ot other Products only
        instance = kwargs.pop('instance', None)
        if instance:
            self.fields['related_products'].queryset = Product.objects.exclude(pk=instance.pk)
