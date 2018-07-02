from django.shortcuts import render

from blogapp.models import Article, Category

def index(request):
    category_list = Category.objects.all()
    article_list = Article.objects.all()
    return render(request, 'index.html', locals())

def content(request):
    article_list = Article.objects.all()
    return render(request, 'content.html', locals())