from django import forms
from .models import Article

from markdownx.widgets import MarkdownxWidget


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'text')
        widgets = {
                'text': MarkdownxWidget(),
        }
