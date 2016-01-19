#coding:utf-8
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Article(models.Model): #创建文章表
    title = models.CharField(max_length=254) #帖子名称，可以重名
    category = models.ForeignKey('Category') #板块表
    content = models.TextField(max_length=100000) #帖子内容，使用textfield，因为文字很多
    author = models.ForeignKey('UserProfile') #作者，外键关联到UserProfile
    summary = models.TextField(max_length=500) #简介
    head_img = models.ImageField(upload_to="statics/imgs/upload") #头部配图
    publish_date = models.DateTimeField(auto_now_add=True) #日期，auto_now_add=True自动生成
    #thumb_ups = models.ForeignKey("ThumbUp",blank=True) #点赞，blank=True不是必须的，由于是一个文章需要多个点赞，因此需要单独列出一个点赞表，反向外键关联到文章表上
    #comments = models.ManyToManyField("Comment",blank=True) #评论表
    def __unicode__(self):
        return self.title

class Category(models.Model): #板块表
    name = models.CharField(unique=True,max_length=64) #板块名，unique=True不能重复
    admins = models.ManyToManyField('UserProfile')  #版主
    def __unicode__(self):
        return self.name
class ThumbUp(models.Model): #点赞表
    article = models.ForeignKey('Article') #文章表，外键反关联到Aritcle表中
    user = models.ForeignKey('UserProfile') #谁点的赞
    date = models.DateTimeField(auto_now_add=True) #日期
    def __unicode__(self):
        return self.article.title

class Comment(models.Model): #评论表
    article = models.ForeignKey('Article') #标题
    user = models.ForeignKey('UserProfile') #用户
    #特别注意，如果做自关联时候，必须要用related_name
    parent_comment = models.ForeignKey('self',blank=True,null=True,related_name='pid') #父级评论（自己关联自己），blank=True可以为空（admin页面可以为空），null=True数据库中可以为空
    comment = models.TextField(max_length=1024) #评论内容
    date = models.DateTimeField(auto_now_add=True) #评论时间
    def __unicode__(self):
        return  self.comment

class UserProfile(models.Model):  #用户信息表
    user = models.OneToOneField(User) #用户
    name = models.CharField(max_length=32) #中文名
    user_groups = models.ManyToManyField('UserGroup') #用户组
    friends = models.ManyToManyField('self',blank=True,related_name='my_friends') #好友
    def __unicode__(self):
        return self.name

class UserGroup(models.Model): #用户组表
    name = models.CharField(max_length=32,unique=True) #组名，unique=True不能重复
    def __unicode__(self):
        return self.name
