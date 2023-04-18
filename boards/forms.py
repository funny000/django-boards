# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2022/12/29 16:34
# python versions: Python3.7
# file: djangoProject

from django import forms
from .models import Topic
from .models import Post


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 5, 'placeholder': 'What is on your mind?'}
    ),
                              max_length=4000,
                              help_text='The max length of the text is 4000.')
    class Meta:
        model = Topic
        fields = ['subject', 'message']


# 给回帖创建表单
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]


