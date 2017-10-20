#coding=utf8

import xadmin

from .models import Article

class ArticleAdmin(object):
    list_display = ['article', 'name', 'desc', 'image','fav_nums', 'click_nums','add_time']
    search_fields = ['article', 'name', 'desc', 'content', 'image','fav_nums', 'click_nums']
    list_filter = ['article__name', 'name', 'desc', 'content', 'image','fav_nums', 'click_nums','add_time']


xadmin.site.register(Article, ArticleAdmin)