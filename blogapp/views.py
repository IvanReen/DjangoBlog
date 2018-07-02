from django.shortcuts import render

from blogapp.models import Article, Category

# 首页引导
def index(request):
    category_list = Category.objects.all()
    article_list = Article.objects.all()
    return render(request, 'index.html', locals())

# 通过种类查博客
def To_Article_By_Category(request):
    aid = request.GET.get('cid')
    category_list = Category.objects.all()
    article_list = Article.objects.filter(tag_id=aid)
    cname = Category.objects.get(id=aid).name
    return render(request, 'index.html', locals())

# 点击文章名显示文章信息
def To_Article_By_id(request):
    info_id = request.GET.get('id')
    category_list = Category.objects.all()
    article_list = Article.objects.filter(id=info_id)
    return render(request, 'article.html', locals())
