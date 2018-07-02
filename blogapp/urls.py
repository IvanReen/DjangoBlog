from django.urls import path, re_path

from blogapp.views import index, content

app_name = 'blogapp'

urlpatterns = [
    re_path('^$', index, name= 'category'),
    re_path('^$', content, name= 'article'),
]