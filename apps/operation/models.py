#coding=utf8
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

from users.models import UserProfile
from article.models import Article

# Create your models here.


class ArticleComments(models.Model):
    """
    文章评论
    """
    user=models.ForeignKey(UserProfile,verbose_name=u'用户')
    article=models.ForeignKey(Article,verbose_name=u'文章')
    comments=models.CharField(max_length=300,verbose_name=u'评论')
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name=u'文章评论'
        verbose_name_plural=verbose_name

    #获取文章评论者的名字
    def get_people(self):
        return self.user

    # 获取文章评论者的头像
    def get_people_image(self):
        return self.user.image

    def __unicode__(self):
        return self.comments


class UserFavorite(models.Model):
    user=models.ForeignKey(UserProfile,verbose_name=u'用户')
    fav_id=models.IntegerField(default=0,verbose_name=u'数据ID')
    fav_type=models.IntegerField(choices=((1,u'文章'),(2,u'作者')),default=1,verbose_name=u'收藏类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name=u'用户收藏'
        verbose_name_plural=verbose_name

    def __unicode__(self):
        return unicode(self.user)


class UserMessage(models.Model):
    user=models.IntegerField(default=0,verbose_name=u'接受用户')
    message=models.CharField(max_length=500,verbose_name=u'用户消息')
    has_read=models.BooleanField(default=False,verbose_name=u'是否已读')
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name=u'用户消息'
        verbose_name_plural=verbose_name

    def get_message(self):
        return self.message[:15]

    def __unicode__(self):
        return unicode(self.user)


class UserArticle(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u'用户')
    article = models.ForeignKey(Article, verbose_name=u'文章')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')


    class Meta:
        verbose_name=u'用户发表的文章'
        verbose_name_plural=verbose_name

    def __unicode__(self):
        return unicode(self.user)