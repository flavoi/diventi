from django import forms

from .models import Answer


class AnswerForm(forms.ModelForm):
    group_title = forms.CharField()
    group_description = forms.CharField()

    class Meta:
        model = Answer
        fields = ('survey', 'question', 'content',)        
        widgets = {
            'survey': forms.HiddenInput(),
            'question': forms.HiddenInput(),            
            'content': forms.Textarea(attrs={'class':'form-control'},),
        }

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.question = kwargs.pop('initial', None)['question']
        if self.question:
            self.fields['content'].label = self.question
        self.fields['survey'].widget = forms.HiddenInput()
        self.fields['group_title'].widget = forms.HiddenInput()
        self.fields['group_description'].widget = forms.HiddenInput()
        

