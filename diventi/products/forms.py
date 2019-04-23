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
        w = self.fields['authors'].widget
        choices = []
        for choice in users:
            choices.append((choice.id, choice))
        w.choices = choices