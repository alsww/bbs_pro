
from django.conf.urls import include, url

import views
urlpatterns = [
    url(r'^$', views.dashboard,name='chat'),
    url(r'^send_msg/$', views.send_msg, name='chat_send_msg'),
    url(r'^get_msg/$', views.get_msg, name='get_new_msg'),
]
