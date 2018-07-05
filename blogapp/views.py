from django.contrib.auth import authenticate, login as auto_login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from blogapp.models import Category, Article, Articles_Label, Comment, User_info, Label

# 首页引导
def index(request):
    category_list = Category.objects.all()       # 获取所有的种类目录
    # 按照种类查看文章
    cid = request.GET.get('cid')
    cname = Category.objects.filter(id=cid)
    if cid:
        articles = Article.objects.filter(tag_id=cid).order_by('id')
    else:
        articles = Article.objects.all().order_by('id')  # 获取所有的文章目录
    # 分页实现
    paginator = Paginator(articles, 2)
    page_num = request.GET.get('page')
    try:
        article_list = paginator.page(page_num)
    except PageNotAnInteger:
        article_list = paginator.page(1)
    except EmptyPage:
        article_list = paginator.page(paginator.num_pages)
    # 按照文章id查看文章信息,以及评论信息
    aid = request.GET.get('id')
    if aid:
        article = Article.objects.get(id=aid)
        comment_list = Comment.objects.filter(art=article)
        return render(request, 'article.html', {'category_list': category_list, "article": article, 'comment_list':comment_list})

    # 标签云
    label_list = Label.objects.all()
    label_id = request.GET.get('lid')
    if label_id:
        labobj = Label.objects.get(id=label_id)
        article_list = labobj.articles.all()

    # 评论排行


    return render(request, 'index.html', {'category_list':category_list, 'article_list':article_list, 'cname':cname, 'cid':cid, 'paginator':paginator, 'label_list':label_list})

# # 按照文章id查看文章信息
# def detail(request):
#     category_list = Category.objects.all()  # 获取所有的种类目录
#     aid = request.GET.get('id')
#     print(aid)
#     article = Article.objects.get(id=aid)
#     print(article)
#     return render(request, 'article.html', {'category_list':category_list, "article":article})

# 用户登录注册
def register(request):
    if request.method == 'POST':
        uname = request.POST.get('regname')
        uemail = request.POST.get('regemail')
        uurl = request.POST.get('regurl')
        upwd = request.POST.get('regpwd')
        User_info.objects.create_user(username=uname, password=upwd, useremail=uemail, userurl=uurl)
        return HttpResponseRedirect('/login/')
    else:
        return render(request, 'reg.html')

# 用户登录
def login(request):
    uname = request.POST.get('username')
    pwd = request.POST.get('password')
    user = authenticate(username=uname, password=pwd)
    if user is not None:
        auto_login(request, user)
        return HttpResponseRedirect('/')
    else:
        return render(request, 'login.html')

# 注销
def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# 接收评论
def receive(request):
    content = request.POST.get('content')   # 评论内容
    aname = request.POST.get('aname')   # 文章id
    rname = request.POST.get('rname')       # 用户名
    user_id = User_info.objects.get(username=rname)    # 通过用户名找用户，给前台显示
    Comment.objects.create(content=content, user_info=user_id, art_id=aname)  # 将评论记录在评论表中
    return HttpResponseRedirect('/?id='+aname)

# 发表文章
def publish(request):
    return render(request, 'publish.html')
