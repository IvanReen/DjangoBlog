from django.contrib.auth.hashers import make_password, SHA1PasswordHasher
from django.db import models

# Create your models here.
class UserProfile(models.Model):
    username = models.CharField(max_length=20,
                                verbose_name='账号',
                                unique=True)
    password = models.CharField(max_length=100,
                                verbose_name='口令')

    nickname = models.CharField(max_length=50,
                                verbose_name='用户名')

    photo = models.CharField(max_length=100,
                             verbose_name='头像',
                             blank=True,
                             null=True
                             )

    phone = models.CharField(max_length=20,
                             verbose_name='手机号',
                             blank=True,
                             null=True)

    source = models.CharField(max_length=50,
                              verbose_name='来源',
                              null=True,
                              blank=True)

    email = models.CharField(max_length=50,
                             verbose_name='邮箱',
                             blank=True,
                             null=True)

    regist_time = models.DateTimeField(auto_now_add=True,
                                       verbose_name='注册时间')

    def __str__(self):
        return self.username

    def __repr__(self):
        return '<UserProfile: %d>' % self.id

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if len(self.password) <= 20:
            # ？django加密算法有哪些
            # django.contrib.auth.hashers 包下类
            self.password = make_password(self.password)

        super().save()

    class Meta:
        db_table = 't_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

