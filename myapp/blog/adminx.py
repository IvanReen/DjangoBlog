# _*_ coding: utf-8 _*_
# 系统(内置)模块
import os

import xadmin  # 第三方模块
from xadmin import views


from blog.models import Tag, Category, Article, SideBar, Links  # 自定义模块

# Register your models here.


class BaseSettings:  # 设置admin的站点样式
    enable_themes = True
    use_bootswatch = True


class GlobalSettings:
    site_title = '博客后台管理系统'
    site_footer = '西安小城Py爱好者 | 联系方式：18127655676'
    menu_style = 'accordion'
    # global_search_models = (Tag,)
    apps_label_title = {
        'blog': '博客管理',   # 应用名：'应用标题'
        'oauth': '授权管理',
        'accounts': '账户信息',
        'comments': '评论管理',
        'servermanager': '命令管理',

    }
    apps_icons = {
        'blog': 'glyphicon glyphicon-book',
        'oauth':'glyphicon glyphicon-briefcase',
        # 'accounts': '账户信息',
        'comments': '	glyphicon glyphicon-stats',
        'servermanager': 'glyphicon glyphicon-tasks',
    }
    global_models_icon = {
        Tag: 'glyphicon glyphicon-tags',
        Article: 'glyphicon glyphicon-tags',
        Category: 'glyphicon glyphicon-tags',
        Links: 'glyphicon glyphicon-tags',
        SideBar: 'glyphicon glyphicon-tags',
    }

xadmin.site.register(views.BaseAdminView, BaseSettings)
xadmin.site.register(views.CommAdminView, GlobalSettings)


class ArticleAdmin:
    list_display = ('title', 'pub_time', 'status', 'comment_status', 'type', 'views', 'author', 'category', 'tags')
    list_per_page = 10
    list_filter = ('pub_time',)
    search_fields = ('title', 'author', 'category', 'tags')
    style_fields = {'body': 'ueditor'}

class TagAdmin:
    list_display = ('name',)
    list_per_page = 10  # 每页显示的记录数
    list_filter = ('name', )  # 过滤字段-查询数据的条件
    search_fields = ('name',)  # 搜索字段


class CategoryAdmin:
    list_display = ('name', 'parent_category')
    list_per_page = 10  # 每页显示的记录数


class LinksAdmin:
    list_display = ('name', 'link', 'sequence', 'created_time', 'last_mod_time')
    list_per_page = 10  # 每页显示的记录数


class SideBarAdmin:
    list_display = ('name', 'content', 'sequence', 'is_enable', 'created_time', 'last_mod_time')
    list_per_page = 10  # 每页显示的记录数


xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(SideBar, SideBarAdmin)

xadmin.site.register(Links, LinksAdmin)
xadmin.site.register(Article, ArticleAdmin)

