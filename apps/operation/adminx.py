# coding=utf8

import xadmin

from .models import ArticleComments, UserMessage, UserArticle, UserFavorite


class ArticleCommentsAdmin(object):
    list_display = ['user', 'article', 'comments', 'add_time']
    search_fields = ['user', 'article', 'comments']
    list_filter = ['user', 'article', 'comments', 'add_time']


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'add_time']


class UserArticleAdmin(object):
    list_display = ['user', 'article', 'add_time']
    search_fields = ['user', 'article']
    list_filter = ['user', 'article', 'add_time']


class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']


xadmin.site.register(ArticleComments, ArticleCommentsAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserArticle, UserArticleAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
