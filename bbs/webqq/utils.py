#coding:utf-8
__author__ = 'coffee'

import Queue

class Chat(object):
    def __init__(self): #构造函数
        self.msg_queue= Queue.Queue()

    def get_msg(self,request):  #取消息
        new_msgs = []
        if self.msg_queue.qsize()>0:  ##如果有消息
            for msg in range(self.msg_queue.qsize()):  ##循环qsize，有个几个就循环几次
                new_msgs.append(self.msg_queue.get_nowait())  #取消息，nowait不阻塞
        else:   #如果没新消息，则等待6秒
            try:
                print '-----如果没新消息，则等待6秒-----'
                new_msgs.append(self.msg_queue.get(timeout=6)) #如果6秒内有消息，则扔到消息列表中
                print "\033[32;1m Found  new msg\033[0m" ,new_msgs
            except Queue.Empty: #如果没消息
                print "\033[31;1m Time out , no new msg for user[%s] \033[0m" %request.user.userprofile.name
        print "\033[33;1m Found [%s] new msgs \033[0m" % len(new_msgs)
        return new_msgs