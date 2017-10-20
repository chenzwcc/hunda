# coding=utf8
from django.shortcuts import render
from django.views.generic import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

from .models import Article


class NewArticleView(View):
    # 最新发表
    def get(self,request):
        current_page='new'
        article=Article.objects.all().order_by('-add_time')[:20]
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(article, 5, request=request)
        article = p.page(page)
        return render(request,'text-new.html',{
            'current_page':current_page,
            'article':article,
        })


class HotArticleView(View):
    # 最火
    def get(self,request):
        current_page = 'hot'
        article = Article.objects.all().order_by('-click_nums')[:20]
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(article, 5, request=request)
        article = p.page(page)
        return render(request,'text-hot.html',{
            'current_page': current_page,
            'article': article,
        })


class CommentsArticleView(View):
    # 收藏最多的
    def get(self,request):
        current_page = 'comments'
        article = Article.objects.all().order_by('-fav_nums')[:20]
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(article, 5, request=request)
        article = p.page(page)
        return render(request,'text-comment-zuiduo.html',{
            'current_page': current_page,
            'article': article,
        })