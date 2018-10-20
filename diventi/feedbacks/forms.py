from django import forms

from .models import Answer


class AnswerForm(forms.ModelForm):
    group = forms.CharField(max_length=100)

    class Meta:
        model = Answer
        fields = ('survey', 'question', 'content', 'group')        
        widgets = {
            'survey': forms.HiddenInput,
            'question': forms.HiddenInput,
            'group': forms.HiddenInput,
            'content': forms.Textarea(attrs={'class':'form-control'},),
        }

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.question = kwargs.pop('initial', None)['question']
        if self.question:
            self.fields['content'].label = self.question
        

