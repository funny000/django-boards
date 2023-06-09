# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2023/2/17 15:21
# python versions: Python3.7
# file: djangoProject

from django.core import mail
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase



class PasswordResetMailTests(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(username='john', email='john@doe.com', password='123')
        self.response = self.client.post(reverse('password_reset'),
                                         {'email': 'john@doe.com'})
        self.email = mail.outbox[0]


    def test_email_subject(self):
        self.assertEquals('[Django Boards] Please reset your password',
                          self.email.subject)


    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('password_reset_config',
                                           kwargs={
                                               'uidb64': uid,
                                               'token': token
                                           })
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn('john', self.email.body)
        self.assertIn('john@doe.com', self.email.body)

    def test_email_to(self):
        self.assertEqual(['john@doe.com',], self.email.to)


