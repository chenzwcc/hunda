# coding=utf8
import os
import json
import uuid

from django.shortcuts import render
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from markdown import markdown
from django.shortcuts import render_to_response

from hunda.settings import MEDIA_ROOT


from .models import UserProfile,EmailVerifyRecord,Banner
from .forms import LoginForm,RegisterForm,ForgetForm,ModifyPwdForm,UserInfoForm
from author.models import Author
from article.models import Article
from operation.models import UserFavorite,UserMessage
from utils.email_send import send_register_email
from utils.mixin_util import LoginRequiredMixin
from utils.qiniusdk import qiniu_upload_file



class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUserView(View):
    def get(self, request, active_code):
    # 用code在数据库中过滤处信息
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                # 通过邮箱查找到对应的用户
                user = UserProfile.objects.get(email=email)
                # 激活用户
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")



class RegisterView(View):
    # 注册
    def get(self,request):
        register_form=RegisterForm()
        return render(request,'register.html',{'register_form':register_form})

    def post(self,request):
        register_form=RegisterForm(request.POST)
        pre_check=register_form.is_valid()
        if pre_check:
            user_name=request.POST.get('email','')
            if UserProfile.objects.filter(email=user_name):
                return render(request,'register.html',{'register_form':register_form,'msg':u'该邮箱已被注册'})
            pass_word=request.POST.get('password','')
            user_profile=UserProfile()
            user_profile.username=user_name
            user_profile.email=user_name
            user_profile.is_active=False
            user_profile.password=make_password(pass_word)
            user_profile.save()

            # 写入注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎注册混搭在线网"
            user_message.save()

            send_register_email(user_name,'register')
            return render(request,'login.html')
        else:
            return render(request,'register.html',{'register_form':register_form})


class LoginView(View):
    # 登陆
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    return render(request, 'login.html', {'msg': u'用户尚未激活,去邮箱激活'})
            else:
                return render(request, 'login.html', {'msg': u'用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class LogoutView(View):
    """
       退出登录
    """

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class ForgetPwdView(View):
    def get(self,request):
        forget_form = ForgetForm()
        return render(request,'password-forget.html',{'forget_form':forget_form})

    def post(self,request):
        forget_form= ForgetForm(request.POST)
        if forget_form.is_valid():
            email=request.POST.get('email','')
            send_register_email(email,'forget')
            return render(request,'send_success.html')
        else:
            return render(request, 'password-forget.html', {'forget_form': forget_form})


class ResetView(View):
    """
    重置密码页面
    """
    def get(self,request,active_code):
        all_records=EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email=record.email
                return render(request,'password_reset.html',{'email':email})
        else:
            return render(request,'active_fail.html')
        return render(request,'login.html')


class ModifyPwdView(View):
    """
       用户未登录修改用户密码
    """
    def post(self,request):
        modify_form=ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1=request.POST.get('password1','')
            pwd2=request.POST.get('password2','')
            email=request.POST.get('email','')
            if pwd1 != pwd2:
                return render(request,'password_reset.html',{'email':email,'msg':u'密码不一致'})
            user=UserProfile.objects.get(email=email)
            user.password=make_password(pwd2)
            user.save()

            return render(request,'login.html')

        else:
            email = request.POST.get('email', '')
            return render(request,'password_reset.html',{'email':email,'msg':u'密码不一致'})


class UserInfoView(LoginRequiredMixin,View):
    """
       用户信息页面
    """

    def get(self, request):

        current_page='userinfo'
        message = ''
        message_list = UserMessage.objects.filter(user=request.user.id, has_read=False)
        userprofile=UserProfile.objects.get(username=request.user)
        if message_list.__len__():
            message = 'message'

        return render(request, 'usercentr-info.html', {
            'userprofile':userprofile,
            'current_page':current_page,
            'message': message,

        })

    def post(self,request):
        """
        用户修改个人信息
        :param request:
        :return:
        """
        """
        nick_name = request.POST.get('nick_name', '')
        author=Author.objects.filter(name=nick_name)
        if author.__len__()==0:
            introduce = request.POST.get('introduce', '')
            mobile = request.POST.get('mobile', '')
            birday = request.POST.get('birday', '')


            user = UserProfile.objects.get(username=request.user)
            request.user.nick_name = nick_name
            request.user.mobile = mobile
            request.user.birday = birday

            request.user.save()

            author = Author()
            author.user = user
            author.name = user.nick_name
            author.introduce = introduce

            author.save()
            return HttpResponse('{"status":"0","msg":"修改个人信息成功"}', content_type='application/json')
        else:
            introduce = request.POST.get('introduce', '')
            mobile = request.POST.get('mobile', '')
            birday = request.POST.get('birday', '')


            user = UserProfile.objects.get(username=request.user)
            request.user.nick_name = nick_name
            request.mobile = mobile
            request.birday = birday
            request.user.save()

            author = Author.objects.get(user=user)
            author.user = user
            author.name = user.nick_name
            author.introduce = introduce
            author.save()
            return HttpResponse('{"status":"0","msg":"修改个人信息成功"}', content_type='application/json')
            """

        if request.user.nick_name:
            user = UserProfile.objects.get(username=request.user)
            author = Author.objects.get(name=user.nick_name)

            nick_name = request.POST.get('nick_name', '')
            introduce = request.POST.get('introduce', '')


            request.user.nick_name = nick_name
            request.user.introduce = introduce
            request.user.save()


            author.user = user
            author.name = nick_name
            author.introduce = introduce

            author.save()
            return HttpResponse('{"status":"0","msg":"修改个人信息成功"}', content_type='application/json')

        user = UserProfile.objects.get(username=request.user)

        nick_name = request.POST.get('nick_name', '')
        if Author.objects.filter(name=nick_name).__len__()!=0:
            return HttpResponse('{"status":"1","msg":"修改个人信息失败"}', content_type='application/json')
        introduce = request.POST.get('introduce', '')


        user.nick_name = nick_name
        user.save()

        author = Author()
        author.user = user
        author.name = user.nick_name
        author.introduce = introduce
        author.save()
        return HttpResponse('{"status":"0","msg":"修改个人信息成功"}', content_type='application/json')

class UploadImage(LoginRequiredMixin, View):
    def post(self, request):
        # 获取文件后先存在本地，再转存至七牛云
        file_obj = request.FILES.get('file', None)
        file_ext = ""
        if file_obj.name.rfind('.') > 0:
            file_ext = file_obj.name.rsplit('.', 1)[1].strip().lower()
            file_name = str(uuid.uuid1()).replace('-', '') + '.' + file_ext
        path = default_storage.save('' + file_name, ContentFile(file_obj.read()))
        # 保存在本地的临时路径
        temp_file = os.path.join(MEDIA_ROOT, path)

        # 上传到七牛云 返回的是 七牛云上存储的地址
        image_url = qiniu_upload_file(file_name, temp_file)

        # 删除保存在本地的临时文件
        os.remove(temp_file)
        request.user.image = image_url
        request.user.save()
        user=UserProfile.objects.get(username=request.user)
        author=Author.objects.get(name=request.user.nick_name)
        author.image=image_url
        author.save()
        user.image=image_url
        user.save()
        return HttpResponseRedirect('/user/info/')


class UserArticleView(View):
    def get(self,request):
        current_page='userarticle'
        author=Author.objects.filter(name=request.user.nick_name)
        my_article = Article.objects.filter(article=author).order_by('-add_time')
        huan_article = my_article.order_by('-fav_nums')[:1]
        hot_article = my_article.order_by('-click_nums')[:2]
        message = ''
        message_list = UserMessage.objects.filter(user=request.user.id, has_read=False)
        if message_list.__len__():
            message = 'message'

        return render(request,'usercenter-mytext.html',{
            'current_page':current_page,
            'author':author,
            'my_article':my_article,
            'huan_article': huan_article,
            'hot_article': hot_article,
            'message': message,
        })


class MyFavArticleView(View):
    def get(self,request):

        current_page = 'my_fav'
        article_list=[]
        my_fav_article=UserFavorite.objects.filter(user=request.user,fav_type=1)

        message = ''
        message_list = UserMessage.objects.filter(user=request.user.id, has_read=False)
        if message_list.__len__():
            message = 'message'


        for fav_article in my_fav_article:
            article_id=fav_article.fav_id
            article=Article.objects.get(id=article_id)
            article_list.append(article)

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(article_list, 5, request=request)
        article_list = p.page(page)

        return render(request,'usercenter-fav-text.html',{
            "article_list":article_list,
            'current_page': current_page,
            'message': message,

        })


class MyFavAuthorView(View):
    def get(self,request):

        current_page = 'my_fav'
        author_list=[]
        my_fav_author=UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_author in my_fav_author:
            author_id=fav_author.fav_id
            author=Author.objects.get(id=author_id)
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
        author_list = p.page(page)

        return render(request,'usercenter-fav-people.html',{
            "author_list":author_list,
            'current_page': current_page,
            'message': message,

        })


class MyMessageView(LoginRequiredMixin,View):
    def get(self,request):
        current_page='message'
        #该用户的所有消息
        mymessages=UserMessage.objects.filter(user=int(request.user.id)).order_by('-add_time')
        # 该用户所有未读的消息
        message = ''
        message_list = UserMessage.objects.filter(user=request.user.id, has_read=False)
        if message_list.__len__():
            message = 'message'
            # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(mymessages, 5, request=request)
        messages = p.page(page)
        return render(request,'usercenter-message.html',{
            'current_page':current_page,
            'mymessages': messages,
            'message_list':message_list,
            'message': message,
        })

class MyMessageDetailView(View):
    def get(self,request,message_id):
        current_page = 'message'
        msg=UserMessage.objects.get(user=request.user.id,id=int(message_id))
        msg.has_read=True
        msg.save()

        message = ''
        message_list = UserMessage.objects.filter(user=request.user.id, has_read=False)
        if message_list.__len__():
            message = 'message'

        return render(request,'usercenter-message-detail.html',{
            'msg':msg,
            'current_page':current_page,
            'message': message,
        })


class ManagementView(View):
    # 账户管理
    def get(self,request):
        current_page='management'
        message = ''
        message_list = UserMessage.objects.filter(user=request.user.id, has_read=False)
        if message_list.__len__():
            message = 'message'
        return render(request,"usercenter-zhguanli.html",{
            'current_page':current_page,
            'message': message,
        })


class IndexView(View):
    # 首页
    def get(self, request):

        keywords = request.GET.get('keywords', '')

        # 取出轮播图
        banners = Banner.objects.all().order_by('index')
        # 取出文章
        article = Article.objects.all().order_by('-add_time')

        if keywords:
            article=article.filter(Q(article__name__icontains=keywords) | Q(name__icontains=keywords))
        # 推荐文章
        article_list=Article.objects.all().order_by("-fav_nums")[:4]
        message=''
        message_list=UserMessage.objects.filter(user=request.user.id,has_read=False)
        if message_list.__len__():
            message='message'
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(article, 7, request=request)
        article = p.page(page)
        return render(request, 'index.html', {
            'banners':banners,
            'article':article,
            'article_list':article_list,
            'message':message,
        })


class WriteArticleView(View):
    def get(self,request):
        current_page='write'

        return render(request, 'write.html', {
            'current_page': current_page,
        })

    def post(self, request):
        title = request.POST.get('title','')
        content = request.POST.get('content','')
        content=markdown(content)
        #image = request.POST.get('image')
        article = Article()
        article.name = title
        article.content = content
        article.desc = content[:100]

        user = UserProfile.objects.get(id=request.user.id)
        author = Author.objects.get(name=user.nick_name)
        article.article = author
        article.article.save()
        article.save()

        data = {"status": "0", "msg": "发表成功"}
        return HttpResponse(json.dumps(data), content_type='application/json')


class UploadArticleImageView(LoginRequiredMixin,View):
    """
    上传封面图
    """

    def post(self, request):
        # 获取文件后先存在本地，再转存至七牛云
        file_obj = request.FILES.get('file', None)
        file_ext = ""
        if file_obj.name.rfind('.') > 0:
            file_ext = file_obj.name.rsplit('.', 1)[1].strip().lower()
            file_name = str(uuid.uuid1()).replace('-', '') + '.' + file_ext
        path = default_storage.save('' + file_name, ContentFile(file_obj.read()))
        # 保存在本地的临时路径
        temp_file = os.path.join(MEDIA_ROOT, path)

        # 上传到七牛云 返回的是 七牛云上存储的地址
        image_url = qiniu_upload_file(file_name, temp_file)

        # 删除保存在本地的临时文件
        os.remove(temp_file)

        user = UserProfile.objects.get(username=request.user)
        author = Author.objects.get(name=request.user.nick_name)
        article_list=Article.objects.filter(article=author).order_by('-add_time')[:1]

        for article in article_list:
            article.image=image_url
            article.save()
        data = {"status": "0", "msg": image_url}
        return HttpResponseRedirect('/user/article/')


# 404
def page_not_found(request):
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


# 500
def page_error(request):
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
