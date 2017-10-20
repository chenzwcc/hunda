# coding=utf8
from django.conf.urls import url

from .views import NewArticleView,HotArticleView,CommentsArticleView
urlpatterns=[
    # 最新发表
    url(r"^newArticle/$",NewArticleView.as_view(),name='newArticlle'),
    # 最新发表
    url(r"^hotArticle/$",HotArticleView.as_view(),name='hotArticlle'),
    # 最新发表
    url(r"^commentsArticle/$",CommentsArticleView.as_view(),name='commentsArticlle'),
]