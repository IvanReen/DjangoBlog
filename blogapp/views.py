from django.contrib.auth import authenticate, login as auto_login, logout
from django.shortcuts import render, HttpResponseRedirect

from blogapp.models import *

# 首页引导
def index(request):
    category_list = Category.objects.all()
    article_list = Article.objects.all()
    label_list = Label.objects.all()
    return render(request, 'index.html', locals())

# 通过种类查博客，并且获取种类，切换时显示
def To_Article_By_Category(request):
    category_list = Category.objects.all()
    aid = request.GET.get('cid')
    article_list = Article.objects.filter(tag_id=aid)
    cname = Category.objects.get(id=aid).name
    return render(request, 'index.html', locals())

# 点击文章名显示文章信息
def To_Article_By_id(request):
    category_list = Category.objects.all()
    info_id = request.GET.get('id')
    article = Article.objects.filter(id=info_id)
    return render(request, 'article.html', locals())

# 看评论
def See_comment(request):
    category_list = Category.objects.all()
    info_id = request.GET.get('id')
    article = Article.objects.get(id=info_id)
    try:
        comment_list = Comment.objects.filter(art=article)
        print(comment_list)
    except Exception:
        msg = "此文章没有评论"
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
    content = request.POST.get('content')   # 评论内容
    aname = request.POST.get('aname')   # 文章id
    rname = request.POST.get('rname')       # 用户名
    user_id = User_info.objects.get(username=rname)    # 通过用户名找用户，给前台显示
    Comment.objects.create(content=content, user_info=user_id, art_id=aname)  # 将评论记录在评论表中
    return HttpResponseRedirect('/seecomment/?id='+aname)

# 标签
def Labels(request):
    label_id = request.GET.get('lid')
    labobj = Label.objects.get(id=label_id)
    article_list = labobj.articles.all()
    category_list = Category.objects.all()
    label_list = Label.objects.all()
    return render(request, 'index.html', locals())