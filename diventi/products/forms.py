from django import forms

from diventi.accounts.models import DiventiUser
from diventi.core.forms import StaffOnlyModelForm

from .models import Product


class UserCollectionUpdateForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['slug']
        widgets = {
            'slug': forms.HiddenInput(),
        }


class ProductForm(StaffOnlyModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        # Products should not be related to themselves but ot other Products only
        instance = kwargs.pop('instance', None)
        if instance:
            self.fields['related_products'].queryset = Product.objects.exclude(pk=instance.pk)
