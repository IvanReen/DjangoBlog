from django.conf.urls import url

from user import views

urlpatterns = [
    url(r'^regist/', views.regist),
    url(r'^upload/', views.upload),
    url(r'^logout/', views.logout),
    url(r'^login/', views.login),
]
