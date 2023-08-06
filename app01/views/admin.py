from app01 import models
from app01.utils.pagintion import Pagination
from django.shortcuts import render,redirect
from app01.modelform.form import AdminModelFrom,AdminEditModelForm,AdminResetModelForm
def admin_list(request):
    """部门列表"""
    #检测用户是否登录，未登录返回登录页面
    #方法 查看用户发来的请求，获取cookie随机字符串，通过随机字符串查看有没有session
    info = request.session.get("info")
    print(info)
    if not info:
        return redirect("/login/")

    if request.method == 'GET':
        queryset = models.Admin.objects.all()
        #create_time.strftime("%Y-%m-%d")
        #obj.get_gender_display()#get_字段名称_display()
        page_object = Pagination(request,queryset,page_size=3)
        context = {
            "manage_list": page_object.page_queryset,  # 分完页的数据
            "page_string": page_object.html  # 生成页码
        }
        return  render(request,'admin_list.html',context)
def admin_add(request):
    """添加管理员"""
    if request.method == "GET":
        form = AdminModelFrom
        return render(request,'admin_add.html',{"form":form})
    form = AdminModelFrom(data=request.POST)
    if form.is_valid():

        form.save()
        print(form.cleaned_data.get("password"))
        return redirect("/admin_list/")
    print(form.errors)
    title = "新建管理员"
    return render(request, 'admin_add.html', {"form": form,"title":title})


def admin_del(request,nid):
    """删除管理员"""
    # id = request.GET.get("nid")
    models.Admin.objects.filter(id = nid).delete()
    return redirect('/admin_list/')
def admin_edit(request,nid):
    """编辑密码"""
    object = models.Admin.objects.filter(id = nid).first()
    title = "编辑管理员"
    if not object:
        return redirect("/admin_list/")
    if request.method == "GET":
        form = AdminEditModelForm(instance=object)#instance默认值
        print(form)
        return  render(request,"phone_edit.html",{"form":form,"title":title})
    form = AdminEditModelForm(instance = object,data = request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin_list/")
    else:
        print(form.errors)
        return render(request, 'phone_edit.html', {"form": form,"title":title})
def admin_reset(request,nid):
    """重置密码"""
    object = models.Admin.objects.filter(id = nid).first()
    title = "重置密码-{}".format(object.name)
    if not object:
        return redirect("/admin_list/")
    if request.method == "GET":
        form = AdminResetModelForm()
        return render(request, "phone_edit.html", {"form": form, "title": title})
    form = AdminResetModelForm(instance=object,data =request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin_list/")
    return render(request, "phone_edit.html", {"form": form, "title": title})