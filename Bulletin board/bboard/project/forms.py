from django.forms import ModelForm
from django import forms
from .models import Post,Comment
from django_summernote.widgets import SummernoteWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'title', 'image', 'cat', 'body']
        prepopulated_fields = {'slug': ('title',)}

    body = forms.CharField(widget=SummernoteWidget)

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('email', 'body')