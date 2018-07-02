from django.urls import path, re_path

from blogapp.views import index, To_Article_By_Category, To_Article_By_id

app_name = 'blogapp'

urlpatterns = [
    re_path('^$', index, name= 'category'),
    path('content/', To_Article_By_Category, name= 'article'),
    path('articleinfo/', To_Article_By_id, name='articleinfo')

]