from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from blogapp.models import *

# Register your models here.
admin.site.register([Category, Comment, Article, Label, Articles_Label])
admin.site.register(User_info, UserAdmin)