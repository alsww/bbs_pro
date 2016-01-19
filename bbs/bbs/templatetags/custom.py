#coding:utf-8
__author__ = 'coffee'
from django import template

register = template.Library()


#自定义标签，filter和simple_tap表示的意思不同
@register.filter
def test_tag(data):
    print 'tag:::',data
    return "<h1>%s</h1>" % data


@register.simple_tag
def test_tag2(data):
    return "<h1>%s</h1>" % data


def insert_comment_node(data_dic,margin_val):
    html = ''
    for p,v in data_dic.items():  ##评论的样式及内容
        r = '''<div style="margin-left:%spx;margin-top:15px;border-left:1px dashed green;border-bottom:1px dashed green">
                <span class="comment-user">%s</span>
                <span class="comment-content">%s</span>
                <span class="comment-date">%s</span>
                </div>'''%(margin_val,p.user.name,p.comment,p.date)
        if v is not None:
            r += insert_comment_node(v,margin_val+20)  ##错开位置
        html += r
    return html


@register.simple_tag
#创建评论树
def build_comment_tree(tree_data):

    html_ele = ""
    for p,v in tree_data.items():
        row = '''<div style="margin-top:15px;border-left:1px dashed green;border-bottom:1px  dashed green">
                <span class="comment-user">%s</span>
                <span class="comment-content">%s</span>
                <span class="comment-date">%s</span>
                </div>'''%(p.user.name,p.comment,p.date)
        if v is not None:
            row += insert_comment_node(v,20)
        html_ele += row
    return html_ele