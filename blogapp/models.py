from django.db import models

# 创建种类表
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=24)

# 创建文章表
class Article(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    content = models.CharField(max_length=1024)
    author = models.CharField(max_length=24)
    write_time = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # 一个种类可对应多篇文章