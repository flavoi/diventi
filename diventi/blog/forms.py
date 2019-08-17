from django import forms

from diventi.accounts.models import DiventiUser
from diventi.core.forms import StaffOnlyModelForm

from .models import Article


class ArticleForm(StaffOnlyModelForm):
    pass