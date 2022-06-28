# _*_ coding: utf-8 _*_

from django.conf import settings
from django.contrib.auth import get_user_model


class EmailOrUsernameModelBackend(object):
    """
    允许使用用户名或邮箱登录
    """
    def authenticate(self, username=None, password=None):
        kwargs = {'email': username} if '@' in username else {'username': username}
        try:
            user = get_user_model().objects.get(**kwargs)
            if user.check_password(password):
                return user
        except get_user_model().DoesNotExist:
            return None

    def get_user(self, username):
        try:
            return get_user_model().objects.get(pk=username)
        except get_user_model().DoesNotExist:
            return None
