import random
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import json
from app01.utils.pagintion import Pagination
from app01 import models
from django.shortcuts import render,redirect
from django import forms
from app01.utils.encrypt import mb5
from app01.utils.code import check_code
from io import BytesIO
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from app01.modelform.form import BModelForm

class OrderModelForm(BModelForm):
    class Meta:
        model = models.Order
        exclude = ["oid","admin"]

def order_list(request):
    form = OrderModelForm()
    queryset = models.Order.objects.all().order_by('-id')
    page_object = Pagination(request, queryset, page_size=10)
    context = {
            "order_list": page_object.page_queryset,  # 分完页的数据
            "page_string": page_object.html, # 生成页码
            "form":form
        }
    #context = {"form":form}
    return render(request, 'order.html', context)
@csrf_exempt
def order_add(request):
    """添加订单"""
    form  = OrderModelForm(request.POST)
    if form.is_valid():
        #设置订单号
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000,10000))
        #获取当前登录管理员的信息 在session中获取，
        form.instance.admin_id = request.session["info"]["id"]
        form.save()
        # return HttpResponse(json.dumps({"status": True}))二者等价
        return JsonResponse({"status": True})#二者等价
    return   JsonResponse({"status": False,'error':form.errors})

def order_del(request,nid):
    """删除订单"""
    if models.Order.objects.filter(id=nid).exists():
        models.Order.objects.filter(id=nid).delete()
        return JsonResponse({"status": True})
    return   JsonResponse({"status": False,'error':"删除失败,订单不存在"})
def order_detail(request):
    nid = request.GET.get("nid")
    if models.Order.objects.filter(id=nid).exists():
        # data_object = models.Order.objects.filter(id=nid).first()
        # data_dict = {
        #     "title":data_object.title,
        #     "price":data_object.price,
        #     "status":data_object.status
        # }
        #直接转化为字典
        data_dict =  models.Order.objects.filter(id = nid).values("title","price","status").first()
        return JsonResponse({"status": True,"data_list":data_dict})
    return JsonResponse({"status": False, 'error': "订单不存在"})
@csrf_exempt
def order_edit(request,nid):
    print(nid)
    object = models.Order.objects.filter(id = 222)
    if object.exists():
        form = OrderModelForm(instance = object.first(),data = request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"status": True})
        return JsonResponse({"status": False, 'error': form.errors})
    return JsonResponse({"status": False, 'tip': "订单不存在"})

