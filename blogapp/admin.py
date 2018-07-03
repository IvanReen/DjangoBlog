from django.contrib import admin
from blogapp.models import *
# Register your models here.
admin.site.register([Category,Comment,Article])

from django.contrib.auth.admin import UserAdmin
admin.site.register(User_info, UserAdmin)