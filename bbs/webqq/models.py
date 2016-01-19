#coding:utf-8
from django.db import models
from bbs import models as bbs_models
# Create your models here.


class QQGroup(models.Model):
    name = models.CharField(max_length=64)
    founder = models.ForeignKey(bbs_models.UserProfile)  #创始人，引用用户表
    brief = models.TextField(max_length=1024,default="nothing...") ##群介绍
    admin = models.ManyToManyField(bbs_models.UserProfile,related_name='group_admins') #管理员
    members = models.ManyToManyField(bbs_models.UserProfile,related_name='group_members') #成员
    members_limit = models.IntegerField(default=200) ##限制成员数量
    def __unicode__(self):
        return self.name