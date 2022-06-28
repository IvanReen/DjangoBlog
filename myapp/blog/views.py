# _*_ coding: utf-8 _*_
from django.shortcuts import render

# Create your views here.
import os
import datetime
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.conf import settings
from django import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from DjangoBlog.utils import cache, logger
from django.shortcuts import get_object_or_404
from blog.models import Article, Category, Tag
from comments.forms import CommentForm


class ArticleListView(ListView):
    # template_name属性用于指定使用哪个模板进行渲染
    template_name = 'blog/article_index.html'

    # context_object_name属性用于给上下文变量取名（在模板中使用该名字）
    context_object_name = 'article_list'

    # 页面类型，分类目录或标签列表等
    page_type = ''
    paginate_by = settings.PAGINATE_BY
    page_kwarg = 'page'

    def get_view_cache_key(self):
        return self.request.get['pages']

    @property
    def page_number(self):
        page_kwarg = self.page_kwarg
        return self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1

    def get_queryset_cache_key(self):
        """
        子类重写.获得queryset的缓存key
        """
        raise NotImplementedError()

    def get_queryset_data(self):
        """
        子类重写.获取queryset的数据
        """
        raise NotImplementedError()

    def get_queryset_from_cache(self, cache_key):
        if value := cache.get(cache_key):
            logger.info('get view cache.key:{key}'.format(key=cache_key))
            return value
        else:
            article_list = self.get_queryset_data()
            cache.set(cache_key, article_list)
            logger.info('set view cache.key:{key}'.format(key=cache_key))
            return article_list

    def get_queryset(self):
        key = self.get_queryset_cache_key()
        return self.get_queryset_from_cache(key)


class IndexView(ArticleListView):
    def get_queryset_data(self):
        return Article.objects.filter(type='a', status='p')

    def get_queryset_cache_key(self):
        return 'index_{page}'.format(page=self.page_number)


class ArticleDetailView(DetailView):
    template_name = 'blog/article_detail.html'
    model = Article
    pk_url_kwarg = 'article_id'
    context_object_name = "article"

    def get_object(self, queryset=None):
        obj = super(ArticleDetailView, self).get_object()
        obj.viewed()
        self.object = obj
        return obj

    def get_context_data(self, **kwargs):
        articleid = int(self.kwargs[self.pk_url_kwarg])
        comment_form = CommentForm()
        user = self.request.user

        if user.is_authenticated and not user.is_anonymous and user.email and user.username:
            comment_form.fields.update({
                'email': forms.CharField(widget=forms.HiddenInput()),
                'name': forms.CharField(widget=forms.HiddenInput()),
            })
            comment_form.fields["email"].initial = user.email
            comment_form.fields["name"].initial = user.username

        article_comments = self.object.comment_list()

        kwargs['form'] = comment_form
        kwargs['article_comments'] = article_comments
        kwargs['comment_count'] = len(article_comments) if article_comments else 0

        kwargs['next_article'] = self.object.next_article
        kwargs['prev_article'] = self.object.prev_article

        return super(ArticleDetailView, self).get_context_data(**kwargs)


class CategoryDetailView(ArticleListView):
    page_type = "分类目录归档"

    def get_queryset_data(self):
        slug = self.kwargs['category_name']
        category = get_object_or_404(Category, slug=slug)

        categoryname = category.name
        self.categoryname = categoryname
        categorynames = list(map(lambda c: c.name, category.get_sub_categorys()))
        return Article.objects.filter(category__name__in=categorynames, status='p')

    def get_queryset_cache_key(self):
        slug = self.kwargs['category_name']
        category = get_object_or_404(Category, slug=slug)
        categoryname = category.name
        self.categoryname = categoryname
        return 'category_list_{categoryname}_{page}'.format(
            categoryname=categoryname, page=self.page_number
        )

    def get_context_data(self, **kwargs):

        categoryname = self.categoryname
        try:
            categoryname = categoryname.split('/')[-1]
        except:
            pass
        kwargs['page_type'] = CategoryDetailView.page_type
        kwargs['tag_name'] = categoryname
        return super(CategoryDetailView, self).get_context_data(**kwargs)


class AuthorDetailView(ArticleListView):
    page_type = '作者文章归档'

    def get_queryset_cache_key(self):
        author_name = self.kwargs['author_name']
        return 'author_{author_name}_{page}'.format(
            author_name=author_name, page=self.page_number
        )

    def get_queryset_data(self):
        author_name = self.kwargs['author_name']
        return Article.objects.filter(author__username=author_name)

    def get_context_data(self, **kwargs):
        author_name = self.kwargs['author_name']
        kwargs['page_type'] = AuthorDetailView.page_type
        kwargs['tag_name'] = author_name
        return super(AuthorDetailView, self).get_context_data(**kwargs)


class TagListView(ListView):
    template_name = ''
    context_object_name = 'tag_list'

    def get_queryset(self):
        tags_list = []
        tags = Tag.objects.all()
        for t in tags:
            t.article_set.count()


class TagDetailView(ArticleListView):
    page_type = '分类标签归档'

    def get_queryset_data(self):
        slug = self.kwargs['tag_name']
        tag = get_object_or_404(Tag, slug=slug)
        tag_name = tag.name
        self.name = tag_name
        return Article.objects.filter(tags__name=tag_name)

    def get_queryset_cache_key(self):
        slug = self.kwargs['tag_name']
        tag = get_object_or_404(Tag, slug=slug)
        tag_name = tag.name
        self.name = tag_name
        return 'tag_{tag_name}_{page}'.format(tag_name=tag_name, page=self.page_number)

    def get_context_data(self, **kwargs):
        # tag_name = self.kwargs['tag_name']
        tag_name = self.name
        kwargs['page_type'] = TagDetailView.page_type
        kwargs['tag_name'] = tag_name
        return super(TagDetailView, self).get_context_data(**kwargs)


class ArchivesView(ArticleListView):
    page_type = '文章归档'
    paginate_by = None
    page_kwarg = None
    template_name = 'blog/article_archives.html'

    def get_queryset_data(self):
        return Article.objects.filter(status='p').all()

    def get_queryset_cache_key(self):
        return 'archives'


@csrf_exempt
def fileupload(request):
    if request.method != 'POST':
        return HttpResponse("only for post")
    response = []
    imgextensions = ['jpg', 'png', 'jpeg', 'bmp']
    for filename in request.FILES:
        timestr = datetime.datetime.now().strftime('%Y/%m/%d')
        fname = u''.join(str(filename))

        isimage = len([i for i in imgextensions if i in fname]) > 0

        basepath = r'/var/www/resource/{type}/{timestr}'.format(
            type='image' if isimage else 'files', timestr=timestr
        )

        if settings.TESTING:
            basepath = f'{settings.BASE_DIR}/uploads'
        url = (
            'https://resource.lylinux.net/{type}/{timestr}/{filename}'.format(
                type='image' if isimage else 'files',
                timestr=timestr,
                filename=filename,
            )
        )

        if not os.path.exists(basepath):
            os.makedirs(basepath)
        savepath = os.path.join(basepath, filename)
        with open(savepath, 'wb+') as wfile:
            for chunk in request.FILES[filename].chunks():
                wfile.write(chunk)
        if isimage:
            from PIL import Image
            image = Image.open(savepath)
            image.save(savepath, quality=20, optimize=True)
        response.append(url)
    return HttpResponse(response)


@login_required
def refresh_memcache(request):
    try:

        if request.user.is_superuser:
            from DjangoBlog.utils import cache
            if cache and cache is not None:
                cache.clear()
            return HttpResponse("ok")
        else:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden()
    except Exception as e:
        return HttpResponse(e)


def page_not_found_view(request, exception, template_name='blog/error_page.html'):
    if exception:
        logger.warn(exception)
    url = request.get_full_path()
    return render(
        request,
        template_name,
        {
            'message': f'哎呀，您访问的地址 {url} 是一个未知的地方。请点击首页看看别的？',
            'statuscode': '404',
        },
        status=404,
    )


def server_error_view(request, template_name='blog/error_page.html'):
    return render(request, template_name,
                  {'message': '哎呀，出错了，我已经收集到了错误信息，之后会抓紧抢修，请点击首页看看别的？', 'statuscode': '500'}, status=500)


def permission_denied_view(request, exception, template_name='blog/error_page.html'):
    if exception:
        logger.warn(exception)
    return render(request, template_name,
                  {'message': '哎呀，您没有权限访问此页面，请点击首页看看别的？', 'statuscode': '403'}, status=403)
