# coding=utf8

import xadmin

from .models import Author


class AuthorAdmin(object):
    list_display = ['name', 'write_time', 'fav_nums', 'click_nums', 'add_time', 'introduce']
    search_fields = ['name', 'fav_nums', 'click_nums', 'introduce']
    list_filter = ['name', 'write_time', 'fav_nums', 'click_nums', 'add_time', 'introduce']


xadmin.site.register(Author, AuthorAdmin)
