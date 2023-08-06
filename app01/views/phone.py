
from dataclasses import fields

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.shortcuts import render,redirect
import requests
from django import forms
from django.utils.safestring import mark_safe
from app01.utils.pagintion import Pagination
from app01 import models
from app01.modelform.form import PhoneModelForm,PhoneEditModelForm
######################################################靓号管理#######################################################################################


def phone_list(request):
    """靓号列表"""

      # 添加数据
    # for i in range(0,100):
    #      phones = "102750215"+str(i).rjust(2,'0')
    #      print(phones)
    #      models.PreetyNum.objects.create(phone=phones,price=100,level=1,status=2)

    # 搜索框
    #搜索框的搜索内容，和搜索条件
    data_dict = {}
    seacher_data = request.GET.get('q', "")
    if seacher_data:
        data_dict["phone__contains"] = seacher_data
    queryset = models.PreetyNum.objects.filter(**data_dict).order_by("-level")
    page_object = Pagination(request,queryset)
    data_list = page_object.page_queryset
    page_string = page_object.html()
    return  render(request,'phone_list.html',{"seacher_data":seacher_data,"phone_list":data_list,"page_string":page_string})

def phone_add(request):
    """添加靓号<ModelForm方式>"""
    if request.method=="GET":
        form = PhoneModelForm
        return render(request,'phone_add.html',{"form":form})
    form = PhoneModelForm(data = request.POST)
    if form.is_valid():
        print(form.data)
        form.save()
        return redirect("/phone_list/")
    else:
        print(form.errors)
        return render(request,'phone_add.html',{"form":form})

def phone_edit(request,nid):
    """编辑靓号"""
    data_list = models.PreetyNum.objects.filter(id=nid).first()
    title = "编辑靓号"
    if request.method == "GET":
        form = PhoneEditModelForm(instance=data_list)#instance默认值
        print(form)
        return  render(request,"phone_edit.html",{"form":form,"title":title})
    form = PhoneEditModelForm(data=request.POST,instance=data_list)#确定对象，之后.save()，就是新增对象而是修改对象
    #form默认保存用户输入的所有数据，如果想加入一些字段（在目标表中，不在用户输入中）
    #想要新增form里面的数据，form.instance.字段名 = 值
    if form.is_valid():
        form.save()
        return redirect("/phone_list/")
    else:
        print(form.errors)
        return render(request,'phone_edit.html',{"form":form,"title":title})
def phone_del(request):
    """删除靓号"""
    id = request.GET.get("nid")
    models.PreetyNum.objects.filter(id = id).delete()
    return redirect('/phone_list/')