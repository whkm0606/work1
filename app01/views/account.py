from app01.utils.pagintion import Pagination
from app01 import models
from django.shortcuts import render,redirect
from django import forms
from app01.utils.encrypt import mb5
from app01.utils.code import check_code
from io import BytesIO
from django.shortcuts import HttpResponse
class LoginForm(forms.Form):

    name = forms.CharField(
        label = "用户名",
        widget = forms.TextInput(attrs={"class": "form-control","placeholder": "用户名"}),
        required=True
    )
    password = forms.CharField(
        label = "密码",
        widget = forms.PasswordInput(attrs={"class": "form-control","placeholder": "密码"}),
        required=True
    )
    #把验证码加入
    code = forms.CharField(
        label = "验证码",
        widget = forms.TextInput(attrs={"class": "form-control","placeholder": "验证码"}),
        required=True
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name,field in self.fields.items():
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_password(self):
        mb5_pwd = mb5(self.cleaned_data.get("password"))
        return  mb5_pwd
def login(request):
    """登录"""
    if request == "GET":
        form = LoginForm()
        return  render(request,'login.html',{"form":form})
    form = LoginForm(data = request.POST)
    if form.is_valid():
        #验证成功
        #验证码效验
        user_input_code = form.cleaned_data.pop('code')#输入的验证码,并且在cleaned_data的数据中去除code数据
        code =  request.session.get('img_code')#图片上的的验证码
        if code != user_input_code:
            form.add_error("code","验证码错误")
            return render(request, 'login.html', {"form": form})
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        #去确认
        if not admin_object:
            form.add_error("password","用户名或者密码错误")
            return render(request, 'login.html', {"form": form})
        #账户密码正确，网站生成随机字符串；写到用户浏览器的cookie中去，在写入session中去
        request.session["info"] = {'id':admin_object.id,'name':admin_object.name}
        #session 可以保持三天
        request.session.set_expiry(60*60*24*3)
        return redirect("/admin_list/")
    return render(request, 'login.html', {"form": form})
def logout(request):
    """注销"""
    request.session.clear()
    return redirect("/login/")
def img_code(request):
    #调用check_code，生成图片
    img,code_string = check_code()
    #写入session中以，便后续获取验证码进行效验
    request.session['img_code'] = code_string
    #给session设置60秒超时
    request.session.set_expiry(60)
    print(code_string)
    #写入内存中
    stream = BytesIO()
    img.save(stream, 'png')
    #返回图片
    return HttpResponse(stream.getvalue())
def test(request):
    return render(request,"test.html")
def test_ajax(request):
    print(request.GET)
    return HttpResponse("1")