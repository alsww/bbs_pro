#coding:utf-8

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
import models
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
import  utils
import json
from django.contrib.auth import authenticate,login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

def account_login(request):
    if request.method == 'GET':  #如果是提交数据
        return  render(request,'login.html')
    else:
        print request.POST
        username = request.POST.get('username')  #获取用户名
        passwd = request.POST.get('password')  #获取密码
        user = authenticate(username=username,password=passwd)   #验证输入的用户名和密码
        if user is not None:  #代表用户的帐号和密码OK
            login(request,user)
            user.userprofile.online = True
            user.userprofile.save()
            return  HttpResponseRedirect("/") #返回到首页
        else:
            return  render(request,'login.html',{  ##如果用户名和密码不正确
                'login_err': "Wrong username or password!"  #打印错误信息
            })


#分页
def index(request):
    article_list = models.Article.objects.all().order_by('-publish_date') #models.Article.objects.all()取出所有，order_by排序，“-”publish_date按降序排列，时间从新到旧，新的在上面
    paginator = Paginator(article_list, 3) # 每1页显示3篇文章
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)

    return render(request,'index.html',{
        'articles': articles
    })

def article(request,article_id):
    err_msg = ''
    try:
        article_obj = models.Article.objects.get(id=article_id)
        comments = utils.build_comments_tree(request)
    except ObjectDoesNotExist,e:
        err_msg = str(e)

    return  render(request,'article.html',{
                   'article':article_obj,
                    'err_msg': err_msg,
                    'comments':comments
                    }
                   )


#创建帖子
def create_article(request):
    if request.method == "GET":
        return render(request,'create_article.html')
    elif request.method == 'POST':
        print request.FILES
        bbs_generater = utils.ArticleGen(request)
        res = bbs_generater.create()
        html_ele = '''Your article <<a href="/article/%s/">%s</a>>has been created successfully! ''' %(res.id,res.title)
        return HttpResponse(html_ele)

def life(request):

    return  render(request,'life.html')

def tech(request):

    return  render(request,'tech.html')
def category1024(request):

    return  render(request,'1024.html')