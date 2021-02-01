from django.db import models
from django.utils import timezone
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from django.utils.safestring import mark_safe

#記事モデル
class Article(models.Model):
    title = models.CharField(max_length=128)
    text = MarkdownxField('Contents', help_text='To Write with Markdown format')
    posted_at = models.DateTimeField(auto_now_add=True)
    last_modify = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

    def get_text_markdownx(self):
        return mark_safe(markdownify(self.text))

#いいねモデル  
class Ine(models.Model):  
    ip_address = models.CharField('IPアドレス', max_length=20)
    parent = models.ForeignKey(Article, on_delete=models.CASCADE)

#コメントモデル
class Comment(models.Model):
    text = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(to=Article, related_name='comments', on_delete=models.CASCADE)
    def __str__(self):
        return self.text