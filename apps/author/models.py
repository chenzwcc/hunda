#coding=utf8
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

# Create your models here.
from users.models import UserProfile


class Author(models.Model):
    user=models.OneToOneField(UserProfile,verbose_name=u'用户'),
    name=models.CharField(max_length=100,verbose_name=u'作者名')
    write_time=models.DateTimeField(default=datetime.now,verbose_name=u'写作年龄')
    introduce = models.CharField(max_length=300, null=True, blank=True,verbose_name=u'自我介绍')
    image = models.CharField(max_length=200, verbose_name='作者头像的七牛云地址',
                             default='http://oxr5eyw7q.bkt.clouddn.com/f6eae958b00111e7bb4b000c299be46c.jpg')
    fav_nums=models.IntegerField(default=0,verbose_name=u'收藏数')
    click_nums = models.IntegerField(default=0, verbose_name=u'浏览量')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name=u'作者'
        verbose_name_plural=verbose_name

    def __unicode__(self):
        return self.name