from django.urls import path, re_path
from blogapp.views import index, register, login, Logout, receive, publish

app_name = 'blogapp'

urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', Logout, name='logout'),
    path('receive/', receive, name='receive'),
    path('publish/', publish, name='publish'),
]