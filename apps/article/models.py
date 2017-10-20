#coding=utf8
from __future__ import unicode_literals
from datetime import  datetime

from django.db import models

from author.models import Author
# Create your models here.


class Article(models.Model):
    """
    文章信息
    """
    article=models.ForeignKey(Author,verbose_name=u'所属作者')
    name=models.CharField(max_length=100,verbose_name=u'标题名称')
    desc=models.CharField(max_length=200,verbose_name=u'文章描述')
    content=models.TextField(verbose_name=u'文章内容')
    image = models.CharField(max_length=200, verbose_name='文章封面图的七牛云地址',
                             default='http://oxr5eyw7q.bkt.clouddn.com/85efe984b00511e7bb4b000c299be46c.jpg')
    fav_nums=models.IntegerField(default=0,verbose_name=u'收藏人数')
    click_nums=models.IntegerField(default=0,verbose_name=u'浏览量')
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')


    class Meta:
        verbose_name=u'文章'
        verbose_name_plural=verbose_name

    # 获取文章的评论
    def get_comments(self):
        return self.articlecomments_set.all()

    # 获取文章的评论量
    def get_comments_nums(self):
        return self.articlecomments_set.all().count()

    # 获取文章的时间
    def get_time(self):
        return self.add_time

    def __unicode__(self):
        return self.name
