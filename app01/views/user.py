from dataclasses import fields

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.shortcuts import render,redirect
import requests
from django import forms
from django.utils.safestring import mark_safe
from app01.utils.pagintion import Pagination
from app01 import models
from app01.modelform.form import UserModelForm
def user_list(request):
    """员工列表"""

    data_dict = {}
    seacher_data = request.GET.get('q', "")
    if seacher_data:
        data_dict["name__contains"] = seacher_data
    queryset = models.UserInfo.objects.filter(**data_dict)
    if not queryset:
        queryset = models.UserInfo.objects.all()
        page_object = Pagination(request, queryset, page_size=2)
        context = {
            "user_list": page_object.page_queryset,  # 分完页的数据
            "page_string": page_object.html  # 生成页码
        }
        return render(request,'user_list.html',context)
    page_object = Pagination(request, queryset,page_size=2)
    context = {
            "user_list": page_object.page_queryset,  # 分完页的数据
            "page_string": page_object.html   #生成页码
        }
    return  render(request,'user_list.html',context)
def user_add(request):
    """添加员工<简单方式>"""
    if request.method=="GET":
        content = {'depart_list': models.Department.objects.all(),
                   'gender_choices': models.UserInfo.gender_choices}
        return  render(request,'user_add.html',content)
    print(request.POST)
    name = request.POST.get("name")
    pwd = request.POST.get("pwd")
    age = request.POST.get("age")
    depart_id = request.POST.get("depart")
    create_time = request.POST.get("ct")
    gender = request.POST.get("gender")
    account = request.POST.get("account")
    models.UserInfo.objects.create(name=name,password=pwd,age=age,depart_id=depart_id,gender=gender,create_time=create_time)
    return redirect("/user_list")

def user_del(request):
    """删除员工"""
    id = request.GET.get("nid")
    models.UserInfo.objects.filter(id = id).delete()
    return redirect('/user_list/')
def user_model_form_add(request):
    """添加员工<ModelForm方式>"""
    if request.method=="GET":
        form = UserModelForm
        return render(request,'user_model_form_add.html',{"form":form})
    form = UserModelForm(data = request.POST)
    if form.is_valid():
        print(form.data)
        form.save()
        return redirect("/user_list/")
    else:
        print(form.errors)
        return render(request,'user_model_form_add.html',{"form":form})
def user_edit(request,nid):
    """编辑员工"""
    data_list = models.UserInfo.objects.filter(id=nid).first()
    title = "编辑员工"
    if request.method == "GET":
        print(data_list.password)
        form = UserModelForm(instance=data_list)#instance默认值
        return  render(request,"user_edit.html",{"form":form,"title":title})
    form = UserModelForm(data=request.POST,instance=data_list)#确定对象，之后.save()，就是新增对象而是修改对象
    #form默认保存用户输入的所有数据，如果想加入一些字段（在目标表中，不在用户输入中）
    #想要新增form里面的数据，form.instance.字段名 = 值
    if form.is_valid():
        form.save()
        return redirect("/user_list/")
    else:
        print(form.errors)
        return render(request,'user_edit.html',{"form":form,"title":title})