# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2023/4/17 13:09
# python versions: Python3.7
# file: djangoProject
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Board, Post, Topic
from ..views import topic_posts, PostListView


class TopicPostsTests(TestCase):
    def setUp(self) -> None:
        board = Board.objects.create(name='Django', description='Django board')
        user = User.objects.create_user(username='john', email='john@doe.com', password='123')
        topic = Topic.objects.create(subject='hello world!', board=board, starter=user)
        Post.objects.create(message='Lorem ipsum dolor sit amet', topic=topic, created_by=user)

        url = reverse('topic_posts', kwargs={'pk':board.pk, 'topic_pk': topic.pk})
        # print(f'url = {url}')
        self.response = self.client.get(url)
        # print(f'res = {self.response}')

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/boards/1/topics/1/')
        # self.assertEquals(view.func, topic_posts)
        self.assertEquals(view.func.view_class, PostListView)
