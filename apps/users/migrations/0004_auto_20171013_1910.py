# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-10-13 19:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_userprofile_introduce'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.CharField(default='http://oxr5eyw7q.bkt.clouddn.com/f6eae958b00111e7bb4b000c299be46c.jpg', max_length=200, verbose_name='\u7528\u6237\u5934\u50cf\u7684\u4e03\u725b\u4e91\u5730\u5740'),
        ),
    ]
