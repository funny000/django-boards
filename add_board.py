# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2023/4/18 13:11
# python versions: Python3.7
# file: djangoProject
from django.contrib.auth.models import User
from boards.models import Board, Topic, Post
user = User.objects.first()
board = Board.objects.get(name='Django')
for i in range(30):
    subject = 'Topic test #{}'.format(i)
    topic = Topic.objects.create(subject=subject, board=board, starter=user)
    Post.objects.create(message='Lorem ipsum...', topic=topic, created_by=user)