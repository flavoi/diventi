from django import forms

from .models import Answer, QuestionChoice

from cuser.middleware import CuserMiddleware


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
            choices = self.question.choices.all()
            if choices:
                self.set_closed(closed=True)
                self.fields['content'] = forms.ModelChoiceField(
                        queryset=choices, widget=forms.RadioSelect(attrs={'class':'form-check-input'},), 
                        empty_label=None, required=True, label=self.question)
            else:
                self.set_closed(closed=False)
                self.fields['content'].label = self.question

        self.fields['survey'].widget = forms.HiddenInput()
        self.fields['group_title'].widget = forms.HiddenInput()
        self.fields['group_description'].widget = forms.HiddenInput()

    def save(self, commit=True):
        m = super(AnswerForm, self).save(commit=False)
        user = CuserMiddleware.get_user()
        m.author_name = user.get_full_name()
        m.author = user
        choice = self.cleaned_data['content']
        question = self.cleaned_data['question']
        choices = self.question.choices.all()
        if choices:
            m.choice = choice
        if commit:
            m.save()
        return m
        
    def set_closed(self, closed):
        self.closed = closed

    @property
    def is_closed(self):
        return self.closed




