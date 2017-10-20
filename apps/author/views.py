# coding=utf8
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from markdown import markdown

from .models import Author
from article.models import Article
from operation.models import UserFavorite,ArticleComments,UserMessage
from users.models import UserProfile
from utils.mixin_util import LoginRequiredMixin


class AuthorView(View):
    # 该用户的文章
    def get(self, request, author_id):
        current_page = 'article'
        author = Author.objects.get(id=int(author_id))
        all_article = author.article_set.all()
        huan_article = all_article.order_by('-fav_nums')[:1]
        hot_article = author.article_set.order_by('-click_nums')[:2]

        message = ''
        message_list = UserMessage.objects.filter(user=request.user.id, has_read=False)
        if message_list.__len__():
            message = 'message'

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_article, 5, request=request)
        article = p.page(page)

        has_fav = False
        if request.user.is_authenticated():
            # 判断该用户是否已经收藏该作者
            if UserFavorite.objects.filter(user=request.user, fav_id=author.id, fav_type=2):
                has_fav = True
        return render(request, 'TAdetail.html', {
            'author': author,
            'all_article': article,
            'current_page': current_page,
            'hot_article': hot_article,
            'huan_article': huan_article,
            'has_fav': has_fav,
            'message': message,

        })


class DynamicView(View):
    # 该用户的文章动态
    def get(self, request, author_id):
        current_page = 'dynamic'
        author = Author.objects.get(id=int(author_id))
        all_article = author.article_set.all().order_by('-add_time')
        huan_article = all_article.order_by('-fav_nums')[:1]
        hot_article = author.article_set.order_by('-click_nums')[:2]
        all_dynamic = []
        for article in all_article:
            all_dynamic += article.get_comments().order_by('-add_time')

        message = ''
        message_list = UserMessage.objects.filter(user=request.user.id, has_read=False)
        if message_list.__len__():
            message = 'message'

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_dynamic, 10, request=request)
        article = p.page(page)
        has_fav = False
        if request.user.is_authenticated():
            # 判断该用户是否已经收藏该作者
            if UserFavorite.objects.filter(user=request.user, fav_id=author.id, fav_type=2):
                has_fav = True
        return render(request, 'TAdetail-dongtai.html', {
            'current_page': current_page,
            'author': author,
            'huan_article': huan_article,
            'hot_article': hot_article,
            'all_dynamic': article,
            'has_fav': has_fav,
            'message': message,
        })


class HotArticleView(View):
    # 该用户的热门文章
    def get(self, request, author_id):
        current_page = 'hot'
        author = Author.objects.get(id=int(author_id))
        all_article = author.article_set.all()
        huan_article = all_article.order_by('-fav_nums')[:1]
        hot_article = author.article_set.order_by('-click_nums')[:2]
        hot_list_article = author.article_set.order_by('-click_nums')[:15]

        message = ''
        message_list = UserMessage.objects.filter(user=request.user.id, has_read=False)
        if message_list.__len__():
            message = 'message'

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(hot_list_article, 5, request=request)
        article = p.page(page)
        has_fav = False
        if request.user.is_authenticated():
            # 判断该用户是否已经收藏该作者
            if UserFavorite.objects.filter(user=request.user, fav_id=author.id, fav_type=2):
                has_fav = True
        return render(request, 'TAdetail-hot.html', {
            'current_page': current_page,
            'author': author,
            'huan_article': huan_article,
            'hot_article': hot_article,
            'hot_list_article': article,
            'has_fav': has_fav,
            'message': message,
        })


class FavArticleView(View):
    # 该用户收藏的文章
    def get(self, request, author_id):
        current_page = 'article'
        author = Author.objects.get(id=int(author_id))
        all_article = author.article_set.all()
        huan_article = all_article.order_by('-fav_nums')[:1]
        hot_article = author.article_set.order_by('-click_nums')[:2]
        fav_article = []
        user = UserProfile.objects.get(id=int(author_id))

        author_fav_article = UserFavorite.objects.filter(user=user, fav_type=1)
        for article in author_fav_article:
            article_id = article.fav_id
            articl = Article.objects.get(id=article_id)
            fav_article.append(articl)

        message = ''
        message_list = UserMessage.objects.filter(user=request.user.id, has_read=False)
        if message_list.__len__():
            message = 'message'

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(fav_article, 5, request=request)
        fav_article = p.page(page)
        has_fav = False
        if request.user.is_authenticated():
            # 判断该用户是否已经收藏该作者
            if UserFavorite.objects.filter(user=request.user, fav_id=author.id, fav_type=2):
                has_fav = True
        return render(request, 'TAdetail-guanzhu-wen.html', {
            'fav_article': fav_article,
            'author': author,
            'huan_article': huan_article,
            'hot_article': hot_article,
            'has_fav': has_fav,
            'current_page': current_page,
            'message': message,
        })


class FavAuthorView(View):
    # 该用户收藏的作者
    def get(self, request, author_id):
        current_page = 'author'
        author_he = Author.objects.get(id=int(author_id))
        all_article = author_he.article_set.all()
        huan_article = all_article.order_by('-fav_nums')[:1]
        hot_article = author_he.article_set.order_by('-click_nums')[:2]
        author_list = []
        user = UserProfile.objects.get(id=int(author_id))
        fav_author = UserFavorite.objects.filter(user=user, fav_type=2)
        for author_1 in fav_author:
            author_id = author_1.fav_id
            author = Author.objects.get(id=author_id)
            author_list.append(author)

        message = ''
        message_list = UserMessage.objects.filter(user=request.user.id, has_read=False)
        if message_list.__len__():
            message = 'message'

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(author_list, 5, request=request)
        fav_Author = p.page(page)

        has_fav = False
        if request.user.is_authenticated():
            # 判断该用户是否已经收藏该作者
            if UserFavorite.objects.filter(user=request.user, fav_id=author_he.id, fav_type=2):
                has_fav = True
        return render(request, 'TAdetail-guanzhu-ren.html', {
            'current_page': current_page,
            'fav_Author': fav_Author,
            'author': author_he,
            'huan_article': huan_article,
            'hot_article': hot_article,
            'has_fav': has_fav,
            'message': message,

        })


class ArticleListView(View):
    # 作者的文章详情页
    def get(self, request, author_id, article_id):
        author = Author.objects.get(id=int(author_id))
        #article = Article.objects.filter(article=author)[(int(article_id))-1]
        article = Article.objects.get(id=int(article_id))
        article.click_nums+=1
        article.save()

        #获取文章的所有评论
        all_comments=ArticleComments.objects.filter(article=article).order_by('-add_time')
        all_article = author.article_set.all()
        huan_article = all_article.order_by('-fav_nums')[:1]
        hot_article = author.article_set.order_by('-click_nums')[:2]
        has_author_fav = False
        has_article_fav=False

        message = ''
        message_list = UserMessage.objects.filter(user=request.user.id, has_read=False)
        if message_list.__len__():
            message = 'message'

        if request.user.is_authenticated():
            # 判断该用户是否已经收藏该作者
            if UserFavorite.objects.filter(user=request.user, fav_id=author.id, fav_type=2):
                has_author_fav = True
            if UserFavorite.objects.filter(user=request.user,fav_id=article_id,fav_type=1):
                has_article_fav=True

        return render(request, 'text-detail.html', {
            'author': author,
            'articl': article,
            'all_comments':all_comments,
            'huan_article':huan_article,
            'hot_article':hot_article,
            'has_author_fav':has_author_fav,
            'has_article_fav':has_article_fav,
            'message': message,

        })


class AddCommentView(View):
    """
    axaj添加课程评论
    """

    def post(self, request):
        article_id = request.POST.get('article_id', 0)
        comments = request.POST.get('comments', 0)

        # 判断用户是否登录
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')

        if article_id > 0 and comments:
            article_comments = ArticleComments()
            article = Article.objects.get(id=article_id)
            article_comments.article = article
            article_comments.comments = comments
            article_comments.user = request.user
            article_comments.save()

            author=Author.objects.get(name=article.article)
            user=UserProfile.objects.get(nick_name=author)

            # 回复话题需要发生消息
            message = UserMessage()
            message.from_id = request.user.id
            message.user = user.id
            # 消息内容
            contents = '''{0}  评论了你的文章  {1}:{2}'''.format(
                request.user.nick_name, article.name,comments)

            message.message = contents
            message.save()

            return HttpResponse('{"status":"success","msg":"添加评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加评论失败"}', content_type='application/json')


class AddFavView(View):
    # 用户收藏操作
    def post(self, request):
        # 收藏的id
        fav_id = request.POST.get('fav_id', 0)
        # 收藏的类型
        fav_type = request.POST.get('fav_type', 0)

        # 判断用户是否登录
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')

        # 判断是否已经收藏了,如果已经收藏了,就取消收藏
        exist_recodes = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_recodes:
            # 取消收藏
            exist_recodes.delete()
            if int(fav_type) == 1:
                article = Article.objects.get(id=int(fav_id))
                article.fav_nums -= 1
                if article.fav_nums < 0:
                    article.fav_nums = 0
                article.save()
            elif int(fav_type) == 2:
                author = Author.objects.get(id=int(fav_id))
                author.fav_nums -= 1
                if author.fav_nums < 0:
                    author.fav_nums = 0
                author.save()
            return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')
        else:
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav = UserFavorite()
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.user = request.user

                user_fav.save()

                if int(fav_type) == 1:
                    article = Article.objects.get(id=int(fav_id))
                    article.fav_nums += 1
                    article.save()
                elif int(fav_type) == 2:
                    author = Author.objects.get(id=int(fav_id))
                    author.fav_nums += 1
                    author.save()

                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"收藏失败"}', content_type='application/json')
