# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-10-10 08:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20171002_0308'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='introduce',
        ),
    ]
