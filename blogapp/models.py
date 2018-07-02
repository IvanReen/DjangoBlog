from django.db import models

# 创建种类表
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=24)

# 创建评论表
class Comment(models.Model):
    count = models.IntegerField()

# 创建文章表
class Article(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    content = models.TextField()
    describe = models.CharField(max_length=50, default=None)
    author = models.CharField(max_length=24)
    date_publish = models.DateTimeField(auto_now=True)        # 时间
    click_count = models.IntegerField()         # 浏览
    comment_content = models.ManyToManyField(Comment, through='Article_Comment')  # 评论
    tag = models.ForeignKey(Category, on_delete=models.CASCADE)  # 一个种类可对应多篇文章

# 文章评论中间表
class Article_Comment(models.Model):
    comment_content = models.ForeignKey(Comment, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
