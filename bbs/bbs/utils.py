#coding:utf-8
__author__ = 'coffee'


import models
from s10day12bbs import settings

class ArticleGen(object):
    def __init__(self,request):  ##构造函数
        self.request = request
    def parse_data(self): ##解析数据
        form_data = {
            'title' : self.request.POST.get('title'),        ##获取标题,
            'content': self.request.POST.get('content'),     ##获取内容,
            'category_id' : 1,
            'summary': self.request.POST.get('summary'), ##获取摘要
            'author_id':self.request.user.userprofile.id,
            'head_img':'/root/',
        }
        return form_data



    def create(self): ##把前台提交过来的数据提取出来再进行处理
        self.data = self.parse_data()
        bbs_obj=models.Article(**self.data)   ##有待查询
        bbs_obj.save()
        filename = handle_upload_file(self.request,self.request.FILES['head_img'])
        bbs_obj.head_img = 'imgs/upload/%s' % filename
        bbs_obj.save()
        return  bbs_obj



    def update(self):
        pass


def handle_upload_file(request,file_obj):
    upload_dir = '%s/%s' %(settings.BASE_DIR,settings.FileUploadDir)

    print '-->',dir(file_obj)
    with open('%s/%s' %(upload_dir,file_obj.name),'wb') as destination :
        for chunk in file_obj.chunks():
            destination.write(chunk)
    return   file_obj.name

def recursive_search(data_dic,comment):
    for parent,v in data_dic.items():
        if parent == comment.parent_comment: #如果在第一层
            print "find parent of [%s]" % comment
            data_dic[comment.parent_comment][comment] = {}
        else:
            print "cannot find [%s]'s parent,going to furhter layer" % comment, data_dic[parent]
            recursive_search(data_dic[parent],comment)


#创建评论树
def build_comments_tree(request):
    bbs_obj = models.Article.objects.first()
    print bbs_obj.comment_set.select_related()
    tree_dic = {}
    for comment in bbs_obj.comment_set.select_related().order_by('id'):  ##循环这篇文章
        if not comment.parent_comment:  ##如果没父亲，就是第一层
            tree_dic[comment] ={}
        else:
            recursive_search(tree_dic,comment)

    return  tree_dic
    for k,v in tree_dic.items():
        print '-->', k,v
