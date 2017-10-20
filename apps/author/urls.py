# coding=utf8
from django.conf.urls import url

from .views import AuthorView, HotArticleView, DynamicView, AddFavView, FavArticleView, FavAuthorView
from .views import ArticleListView, AddCommentView

urlpatterns = [
    # 作者文章列表页
    url(r"^article/(?P<author_id>\d+)/$", AuthorView.as_view(), name='article'),
    # 文章详情页
    url(r"^articlelist/(?P<author_id>\d+)/(?P<article_id>\d+)/$", ArticleListView.as_view(), name='articlelist'),
    # 增加文章评论
    url(r"^add_comment/$", AddCommentView.as_view(), name='add_comment'),
    # 作者动态页
    url(r"^dynamic/(?P<author_id>\d+)/$", DynamicView.as_view(), name='dynamic'),
    # 作者热门文章
    url(r"^hot/(?P<author_id>\d+)/$", HotArticleView.as_view(), name='hot'),
    # 作者收藏的的文章
    url(r"fav_article/(?P<author_id>\d+)/$", FavArticleView.as_view(), name='fav_article'),
    # 作者收藏的作者
    url(r"fav_author/(?P<author_id>\d+)/$", FavAuthorView.as_view(), name='fav_author'),
    # 用户收藏
    url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),

]
