from django import forms

from diventi.accounts.models import DiventiUser


class StaffOnlyModelForm(forms.ModelForm):
    """
        This forms assumes that the name of the author field is passed from outside. 
    """
    def __init__(self, *args, **kwargs):
        super(StaffOnlyModelForm, self).__init__(*args, **kwargs)
        users = DiventiUser.objects.filter(is_staff=True);
        # Staff users only should be authors
        author_field = self.author_field
        w = self.fields[author_field].widget
        choices = []
        for choice in users:
            choices.append((choice.id, choice))
        w.choices = choices