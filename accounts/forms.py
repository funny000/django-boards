# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2022/12/30 13:40
# python versions: Python3.7
# file: djangoProject


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254,
                            required=True,
                            widget=forms.EmailInput)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

