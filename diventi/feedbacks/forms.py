from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AnonymousUser

from .models import Survey, Answer, QuestionChoice

from cuser.middleware import CuserMiddleware


class AnswerForm(forms.ModelForm):
    group_title = forms.CharField()
    group_description = forms.CharField()

    class Meta:
        model = Answer
        fields = ('survey', 'question', 'content', 'author', 'author_name')        
        widgets = {
            'survey': forms.HiddenInput(),
            'question': forms.HiddenInput(),
            'author': forms.HiddenInput(), 
            'author_name': forms.HiddenInput(),    
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

    def save(self, request, commit=True):
        m = super(AnswerForm, self).save(commit=False)
        user = CuserMiddleware.get_user()
        
        if user.is_anonymous:
            m.author = None
        elif user.is_superuser:            
            if m.author_name is None:
                m.author = user
                m.author_name = user.get_full_name()
            else:
                m.author = None
        else:
            m.author = user
            m.author_name = user.get_full_name()
        request.session['author'] = m.author # Returns the author to the view
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


class FeaturedSurveyInitForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ('survey', 'author_name',)
        widgets = {
            'survey': forms.HiddenInput(),
            'author_name': forms.TextInput(attrs={'class':'form-control', 'placeholder': _('Name')},),
        }
        