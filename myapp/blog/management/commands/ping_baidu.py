# -*- coding: utf-8 -*-



from django.core.management.base import BaseCommand, CommandError
from blog.models import Article, Tag, Category
from DjangoBlog.spider_notify import SpiderNotify
from django.contrib.sites.models import Site

site = Site.objects.get_current().domain


class Command(BaseCommand):
    help = 'notify baidu url'

    def add_arguments(self, parser):
        parser.add_argument('data_type', type=str, choices=['all', 'article', 'tag', 'category'],
                            help='article : all article,tag : all tag,category: all category,all: All of these')

    def get_full_url(self, path):
        return "https://{site}{path}".format(site=site, path=path)

    def handle(self, *args, **options):
        type = options['data_type']
        self.stdout.write(f'start get {type}')

        urls = []
        if type in ['article', 'all']:
            urls.extend(
                article.get_full_url()
                for article in Article.objects.filter(status='p')
            )

        if type in ['tag', 'all']:
            for tag in Tag.objects.all():
                url = tag.get_absolute_url()
                urls.append(self.get_full_url(url))
        if type in ['category', 'all']:
            for category in Category.objects.all():
                url = category.get_absolute_url()
                urls.append(self.get_full_url(url))

        self.stdout.write(self.style.SUCCESS('start notify %d urls' % len(urls)))
        SpiderNotify.baidu_notify(urls)
        self.stdout.write(self.style.SUCCESS('finish notify'))
