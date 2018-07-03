from django.urls import path, re_path

from blogapp.views import index, To_Article_By_Category, To_Article_By_id, Register, Login, Logout, See_comment, Receive

app_name = 'blogapp'

urlpatterns = [
    re_path('^$', index, name= 'index'),
    path('article/', To_Article_By_Category, name= 'article'),
    path('articleinfo/', To_Article_By_id, name='articleinfo'),
    path('register/', Register, name='register'),
    path('login/', Login, name='login'),
    path('logout/', Logout, name='logout'),
    path('seecomment/', See_comment, name='articleinfo'),
    path('Receive/', Receive, name='receive'),
]