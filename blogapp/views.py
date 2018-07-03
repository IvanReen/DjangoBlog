from django.contrib.auth import authenticate, login as auto_login, logout
from django.shortcuts import render, HttpResponseRedirect

from blogapp.models import *

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
    article = Article.objects.filter(id=info_id)
    return render(request, 'article.html', locals())

# 看评论
def See_comment(request):
    info_id = request.GET.get('id')
    category_list = Category.objects.all()
    article = Article.objects.get(id=info_id)
    try:
        comment_list = Comment.objects.filter(isarticle=article.name)
    except Exception:
        print("此文章没有评论")
    finally:
        return render(request, 'article.html', locals())

# 注册
def Register(request):
    if request.method == 'POST':
        regname = request.POST.get('regname')
        regemail = request.POST.get('regemail')
        regurl = request.POST.get('regurl')
        regpwd = request.POST.get('regpwd')
        User_info.objects.create_user(username=regname, password=regpwd, useremail=regemail, userurl=regurl)
        return HttpResponseRedirect('/login/')
    else:
        return render(request,'reg.html')

# 登录
def Login(request):
    uname = request.POST.get('username')
    pwd = request.POST.get('password')
    user = authenticate(username=uname, password=pwd)
    if user is not None:
        auto_login(request, user)
        return HttpResponseRedirect('/')
    else:
        return render(request, 'login.html', locals())

# 注销
def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# 接收评论
def Receive(request):
    content = request.POST.get('content')
    article_name = request.POST.get('aname')
    user_name = request.POST.get('rname')
    user_id = User_info.objects.get(username=user_name)
    article = Article.objects.get(name=article_name)
    print(content)
    print(article_name)
    Comment.objects.create(content=content, isarticle=article_name, user_info=user_id)
    category_list = Category.objects.all()
    try:
        comment_list = Comment.objects.filter(isarticle=article_name)
    except Exception:
        print("此文章没有评论")
    finally:
        return render(request, 'article.html', locals())