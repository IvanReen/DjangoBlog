from django.shortcuts import render

from blogapp.models import Article, Category

def base(request):
    category_list = Category.objects.all()
    article_list = Article.objects.all()
    return render(request, 'index.html', locals())