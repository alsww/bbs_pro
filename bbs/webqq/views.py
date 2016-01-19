#coding:utf-8
from django.shortcuts import render,HttpResponse
import json,datetime
# Create your views here.
import models
import utils




global_msg_dic = {}  #空的queue
def dashboard(request):
    return render(request,'webqq/dashboard.html')

def send_msg(request):
    print request.POST
    data = request.POST.get('data')
    data = json.loads(data)  #反序列化
    data['date'] =datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") #打上时间戳
    to_id = data.get('to_id')
    user_obj = models.bbs_models.UserProfile.objects.get(id=to_id)
    contact_type = data.get('contact_type')             #对话类型
    if contact_type == 'single':                        #如果对话类型是single
        if not global_msg_dic.has_key(to_id):           #判断有没有to_id这个queue
            global_msg_dic[to_id] = utils.Chat()         #创建一个queue；在utils里面进行初始化
        global_msg_dic[to_id].msg_queue.put(data)        #如果存在to_id这个queue，就把刚才的消息扔进去
        print '\033[31;1m Push msg [%s] into user [%s] queue' % (data['msg'], user_obj.name)
    elif contact_type == 'group':  #如果对话类型是group
        group_obj = models.QQGroup.objects.get(id=to_id)     #获取到组
        for member in group_obj.members.select_related():    #循环所有的名字
            if member.id != request.user.userprofile.id:     #排除自己
                if not global_msg_dic.has_key(member.id):    #如果没queue
                    global_msg_dic[member.id] = utils.Chat()  #创建queue
                global_msg_dic[member.id].msg_queue.put(data) #把数据放进去queue
                print '\033[31;1m Push msg [%s] into user [%s] queue' % (data['msg'], member.name)

    return HttpResponse("as大苏打")


def get_msg(request):
    uid = request.GET.get('uid') #获取UID
    if uid:  #如果UID获取到
        res = []
        if not global_msg_dic.has_key(uid): ##判断uid在不在消息队列中
            global_msg_dic[uid] = utils.Chat() ##创建一个queue
        res = global_msg_dic[uid].get_msg(request)
        return HttpResponse(json.dumps(res))
    else: #如果uid不为真
        return HttpResponse(json.dumps("uid not provided!")) #返回一个错误信息
