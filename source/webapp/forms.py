from django import forms
from .models import STATUS_CHOICES

default_status = STATUS_CHOICES[0][0]


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=200, required=True, label='Заголовок')
    text = forms.CharField(max_length=3000, required=True, label="Текст",
                           widget=forms.Textarea)
    author = forms.CharField(max_length=40, required=True, label='Автор', initial='Unknown')
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=True, label='Статус',
                               initial=default_status)
