from django import forms

from .models import Product


class UserCollectionUpdateForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['slug']
        widgets = {
            'slug': forms.HiddenInput(),
        }
