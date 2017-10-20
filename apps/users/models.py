# coding=utf8

from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.

class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name=u'昵称', default='')
    introduce = models.CharField(max_length=300, null=True, blank=True, verbose_name=u'自我介绍')
    gender = models.CharField(choices=(('male', u'男'), ('female', u'女')), default='female',max_length=6,verbose_name=u'性别')
    image = models.CharField(max_length=200, verbose_name='用户头像的七牛云地址',
                             default='http://oxr5eyw7q.bkt.clouddn.com/75fc0f9cb00211e7bb4b000c299be46c.jpg')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name



    def __unicode__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code=models.CharField(max_length=20,verbose_name=u'验证码')
    email= models.EmailField(max_length=50,verbose_name=u'邮箱')
    send_type=models.CharField(choices=(('register',u'注册'),('forgetpwd',u'找回密码')),max_length=10,verbose_name=u'发送类型')
    send_time=models.DateTimeField(default=datetime.now,verbose_name=u'发送时间')

    class Meta:
        verbose_name=u'邮箱验证码'
        verbose_name_plural=verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)


class Banner(models.Model):
    title=models.CharField(max_length=100,verbose_name=u'标题')
    image=models.ImageField(upload_to='banner/%Y/%m',verbose_name=u'轮播图',max_length=100)
    url=models.URLField(max_length=200,verbose_name=u'访问地址')
    index=models.IntegerField(default=100,verbose_name=u'顺序')
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name=u'轮播图'
        verbose_name_plural=verbose_name
