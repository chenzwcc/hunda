# coding=utf8
from django.conf.urls import url

from .views import UserInfoView,UserArticleView,MyFavArticleView,MyFavAuthorView,MyMessageView
from .views import ManagementView,MyMessageDetailView,WriteArticleView,UploadArticleImageView,UploadImage
urlpatterns=[
    # 用户中心修改详情页
    url(r"^info/$",UserInfoView.as_view(),name='info'),

    # 用户  我的文章页
    url(r"^article/$",UserArticleView.as_view(),name='user_article'),
    # 用户  我的收藏——文章页
    url(r"^favArticle/$",MyFavArticleView.as_view(),name='fav_article'),
    # 用户  我的收藏——作者页
    url(r"^favAuthor/$",MyFavAuthorView.as_view(),name='fav_author'),
    # 用户  我的消息
    url(r"^message/$",MyMessageView.as_view(),name='message'),
    # 用户  我的消息详情页
    url(r"^messageDetail/(?P<message_id>\d+)/$",MyMessageDetailView.as_view(),name='message_detail'),
    # 用户  账户管理
    url(r"^management/$",ManagementView.as_view(),name='management'),
    # 用户写文章
    url(r"^write/$",WriteArticleView.as_view(),name='write'),
    # 用户上传头像
    url(r"^upload/$",UploadImage.as_view(),name='upload'),
    # 用户上传文章封面图
    url(r"^uploadArt/$",UploadArticleImageView.as_view(),name='uploadArt'),

]