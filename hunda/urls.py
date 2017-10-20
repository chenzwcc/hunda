#coding=utf8
"""hunda URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
import xadmin
from django.views.static import serve
from hunda.settings import MEDIA_ROOT
from hunda.settings import STATIC_ROOT

from users.views import LoginView,RegisterView,ActiveUserView,ForgetPwdView,ResetView,ModifyPwdView
from users.views import LogoutView,IndexView
urlpatterns = [
    # 后台管理页面
    url(r'^xadmin/', xadmin.site.urls),
    # 首页
    #url('^$',TemplateView.as_view(template_name='index.html'),name='index'),
    url('^$',IndexView.as_view(),name='index'),
    #  退出
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    # 登录页
    url('^login/$',LoginView.as_view(),name='login'),
    # 注册页面
    url('^register/$',RegisterView.as_view(),name='register'),
    # 验证码
    url('^captcha/',include('captcha.urls')),
    # 邮箱激活
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    # 找回密码
    url(r'^forget/$', ForgetPwdView.as_view(), name="forget_pwd"),
    # 密码重置
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),

    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$',serve,{'document_root':MEDIA_ROOT}),

    # 作者
    url(r"^author/",include('author.urls',namespace='author')),

    # 用户
    url(r"^user/",include('users.urls',namespace='user')),

    # 文章
    url(r"^article/",include('article.urls',namespace='article')),
    # 配置static,解决debug为false时static路径设置无效
    url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),

]

# 全局404页面配置
handler404 = 'users.views.page_not_found'
# 全局500页面配置
handler500 = 'users.views.page_error'