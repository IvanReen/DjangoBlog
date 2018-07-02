from django.urls import path, re_path

from blogapp.views import base

app_name = 'blogapp'
urlpatterns = [
    re_path('^$', base, name= 'category'),
]