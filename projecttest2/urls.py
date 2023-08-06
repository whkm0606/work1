"""projecttest2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from app01 import views
from app01.views import depart,phone,user,admin,account,order,chart,upload,city
from app01 import media
from django.views.static import  serve
from django.conf import settings
urlpatterns = [
    # path('admin/', admin.site.urls),
    #使用Media进行配置
    re_path(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT},name = 'media'),

    #部门管理
    path('depart_list/', depart.depart_list),
    path('depart_add/', depart.depart_add),
    path('depart_del/', depart.depart_del),
    path('depart_edit/<int:nid>/', depart.depart_edit),
    path('depart_upload/', depart.depart_upload),
    #员工管理
    path('user_list/', user.user_list),
    path('user_add/', user.user_add),
    path('user/model/form/add/', user.user_model_form_add),
    path('user_del/', user.user_del),
    path('user_edit/<int:nid>/', user.user_edit),
    #靓号管理
    path('phone_list/', phone.phone_list),
    path('phone_add/', phone.phone_add),
    path('phone_del/', phone.phone_del),
    path('phone_edit/<int:nid>/', phone.phone_edit),
    #管理员管理
    path('admin_list/', admin.admin_list),
    path('admin_add/', admin.admin_add),
    path('admin_edit/<int:nid>/', admin.admin_edit),
    path('admin_del/<int:nid>/', admin.admin_del),
    path('admin_reset/<int:nid>/', admin.admin_reset),
    #登录
    path('login/', account.login),
    path('logout/', account.logout),
    path('img_code/', account.img_code),
    #test
    path('test/', account.test),
    path('test/ajax/', account.test_ajax),

    #订单管理
    path('order_list/',order.order_list),
    path('order_add/', order.order_add),
    path('order_del/<int:nid>/', order.order_del),
    path('order_detail/', order.order_detail),
    path('order_edit/<int:nid>/', order.order_edit),

    #数据统计
    path('chart_list/', chart.chart_list),
    path('chart_bar/', chart.chart_bar),
    #文件传输
    path('upload/list/', upload.upload_list),

    #city
    path('city_list/', city.city_list),
    path('city_add/', city.city_add),
]
