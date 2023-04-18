# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2023/4/18 16:37
# python versions: Python3.7
# file: djangoProject

import hashlib
from urllib.parse import urlencode
from django import template
from django.conf import settings

register = template.Library()

@register.filter
def gravatar(user):
    email = user.email.lower().encode('utf-8')
    default = 'mm'
    size = 256
    url = 'https://sdn.geekzu.org/avatar//{md5}?{params}'.format(
        md5=hashlib.md5(email).hexdigest(),
        params=urlencode({'d': default, 's': str(size)})
    )
    return url