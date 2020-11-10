from django import forms
from django.utils.translation import gettext_lazy as _

from diventi.accounts.models import DiventiUser
from diventi.core.forms import StaffOnlyModelForm

from .models import Article


class ArticleForm(StaffOnlyModelForm):
    pass