# myapp/forms.py

from django import forms

class PDFUploadForm(forms.Form):
    title = forms.CharField(max_length=255, label="Titolo del documento")
    pdf_file = forms.FileField(label="Carica PDF")

class WebIngestionForm(forms.Form):
    title = forms.CharField(max_length=255, label="Titolo del sito web")
    url = forms.URLField(max_length=2000, label="URL del sito web")