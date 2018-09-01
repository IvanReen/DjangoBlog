import re

from django import forms
from django.core.exceptions import ValidationError

from user.models import UserProfile


class UserForm(forms.ModelForm):
    # 新声明的字段，必须是字段属性中声明验证信息
    password2 = forms.CharField(max_length=20,
                                error_messages={
                                    'required': '重复口令不能为空'
                                 })

    username = forms.CharField(min_length=6,
                               max_length=20,
                               error_messages={
                                   'required': '用户名不能为空',
                                   'min_length': '用户名不能小于6位',
                                   'max_length': '用户名不能超过20位',
                                   'unique': '账号已存在'
                               })

    class Meta:
        model = UserProfile
        fields = '__all__'
        error_messages = {
            'password': {
                'required': '口令不能为空'
            },
            'nickname': {
                'required': '用户名不能为空'
            },
        }

    # 验证两次口令是否相同
    def clean_password2(self):
        pwd2 = self.cleaned_data.get('password2')
        pwd1 = self.cleaned_data.get('password')
        if pwd2 is not None and pwd2 != pwd1:
            raise ValidationError('两次口令不一致')
        return pwd2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        print('---email-->', email)
        if email is not None and not re.match(r'\w+?@\w+?\.(com|cn|org|net)', email):
            raise ValidationError('必须是合法的邮箱')
        return email