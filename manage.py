#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    print(f'argv = {sys.argv}')
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    """
    运行服务：python manage.py runserver
    更新配置(添加新字段时更新数据库)：python manage.py makemigrations
    应用迁移(更新数据库之后)：python manage.py migrate
    测试服务：python manage.py test --verbosity=2
    用测试套件测试指定app： python manage.py test boards
    用测试套件测试app下的文件：python manage.py test boards.tests.test_view_topic_posts
    指定单个测试用例：python manage.py test boards.tests.test_view_topic_posts.TopicPostsTests.test_status_code
    创建管理员账户：python manage.py createsuperuser
    密码：pop321987
    python manage.py migrate
    创建用户：django-admin startapp accounts
    """
    main()
