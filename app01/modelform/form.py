from dataclasses import fields

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.shortcuts import render,redirect
import requests
from django import forms
from django.utils.safestring import mark_safe
from app01.utils.encrypt import mb5
from app01 import models
class UserModelForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = '__all__'
        # widgets = {
        #     "name":forms.TextInput(attrs={"class":"form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"})
        # }过于麻烦
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        #循环找到所有的插件，添加class =
        for name,field in self.fields.items():
            if name == "password":
                # field.widget = forms.PasswordInput()#密码修改不可见
                field.widget.attrs = {"class": "form-control"}
                continue
            # print(name,field)
            field.widget.attrs = {"class": "form-control"}


class BModelForm(forms.ModelForm):
    bootstrap_exclude_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name,field in self.fields.items():
            if name in self.bootstrap_exclude_fields:
                continue
            field.widget.attrs = {"class": "form-control"}

class PhoneModelForm(BModelForm):
    #验证方式1
    # phone = forms.CharField(
    #     label="手机号",
    #     validators=[RegexValidator(r'^1[3-9]\d{9}$','手机号格式错误'),],
    # )

    class Meta:
        model = models.PreetyNum
        fields = '__all__'
    def clean_phone(self):
        text_phone = self.cleaned_data["phone"]
        if len(text_phone)!=11:
            raise ValidationError("格式错误")
        pid = self.instance.pk
        print(pid)
        exits = models.PreetyNum.objects.filter(phone = text_phone).exists()
        if exits:
            raise  ValidationError("手机号已存在")
        return  text_phone
class PhoneEditModelForm(BModelForm):
    #验证方式1
    # phone = forms.CharField(
    #     label="手机号",
    #     validators=[RegexValidator(r'^1[3-9]\d{9}$','手机号格式错误'),],
    # )
    #phone = forms.CharField(disabled=True,label="手机号")#显示但不可更改
    class Meta:
        model = models.PreetyNum
        fields = '__all__'
    def clean_phone(self):
        text_phone = self.cleaned_data["phone"]
        if len(text_phone)!=11:
            raise ValidationError("格式错误")
        pid = self.instance.pk
        print(pid)
        exits = models.PreetyNum.objects.exclude(id = pid).filter(phone = text_phone).exists()
        if exits:
            raise  ValidationError("手机号已存在")
        return  text_phone

class BAdminModelFrom(BModelForm):

    def clean_confirm_pwd(self):
        pwd = self.cleaned_data.get('password')
        comfirm_pwd = mb5(self.cleaned_data.get('confirm_pwd'))
        if comfirm_pwd != pwd:
            raise ValidationError("密码不一致")
        return comfirm_pwd#返回什么，该字段就为 什么
    def clean_password(self):#对密码进行加密
        pwd = self.cleaned_data.get('password')
        return mb5(pwd)
class AdminModelFrom(BAdminModelFrom):
    confirm_pwd = forms.CharField(label="确认密码", widget=forms.PasswordInput(render_value=True))  # render_value是否重新输入
    class Meta:
        model = models.Admin
        fields = ['name', 'password', 'confirm_pwd']
        widgets = {'password': forms.PasswordInput(render_value=True)}
class AdminEditModelForm(BAdminModelFrom):
    confirm_pwd = forms.CharField(label="确认密码进行修改", widget=forms.PasswordInput(render_value=True))  # render_value是否重新输入
    class Meta:
        model = models.Admin
        fields = ['name']
    def clean_confirm_pwd(self):
        pws = models.Admin.objects.filter(id = self.instance.pk).first()
        pwd = pws.password
        print(pwd)
        comfirm_pwd = mb5(self.cleaned_data.get('confirm_pwd'))
        print(comfirm_pwd)
        if comfirm_pwd != pwd:
            raise ValidationError("密码不一致")
        return comfirm_pwd#返回什么，该字段就为 什么
class AdminResetModelForm(BAdminModelFrom):
    """重置密码"""
    confirm_pwd = forms.CharField(label="确认密码", widget=forms.PasswordInput(render_value=True))  # render_value是否重新输入
    x = 0
    class Meta:
        model = models.Admin
        fields = ['password','confirm_pwd']
        widgets = {"password": forms.PasswordInput(render_value=True)}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.x = True
    def clean_password(self):  # 对密码进行加密
        pwd = self.cleaned_data.get('password')
        mb5_pwd = mb5(pwd)
        exits = models.Admin.objects.filter(id = self.instance.pk,password=mb5_pwd).exists()
        if exits:
            raise ValidationError("密码不能与之前相同")
            self.x = False
        return mb5_pwd
    def clean_confirm_pwd(self):
        pwd = self.cleaned_data.get('password')
        comfirm_pwd = mb5(self.cleaned_data.get('confirm_pwd'))
        if self.x == False:
            if comfirm_pwd != pwd:
                raise ValidationError("密码不一致")
        return comfirm_pwd#返回什么，该字段就为 什么
