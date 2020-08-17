from django import forms
from django.utils.translation import ugettext_lazy as _

from django_comments.forms import CommentForm                            

from .models import DiventiComment


class DiventiCommentForm(CommentForm):
    parent = forms.ModelChoiceField(queryset=DiventiComment.objects.all(), required=False, widget=forms.HiddenInput)
    honeypot = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={
            'class': 'form-control honeypot',
        })
    )
    comment = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control border-0 px-1',
            'placeholder': _('Write your comment'),
        })
    )

    def get_comment_model(self):
        # Use our custom comment model instead of the built-in one.
        return DiventiComment

    def get_comment_create_data(self, **kwargs):
        # Use the data of the superclass, and add in the parent field field
        data = super(DiventiCommentForm, self).get_comment_create_data()
        data['parent'] = self.cleaned_data['parent']
        return data