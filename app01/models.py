from django.db import models
class Department(models.Model):
    title = models.CharField(verbose_name="部门名",max_length=32)
    def __str__(self):
        return self.title
class UserInfo(models.Model):
    name = models.CharField(verbose_name="姓名",max_length=16)
    password = models.CharField(verbose_name="密码",max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    depart = models.ForeignKey(verbose_name="部门",to="Department",to_field="id",on_delete=models.CASCADE)
    account =models.DecimalField(verbose_name="账户余额", max_digits=10,decimal_places=2,default=0)
    #create_time = models.DateTimeField(verbose_name="入职时间")
    create_time = models.DateField(verbose_name="入职时间")#只有日期没有时分秒
    gender_choices = ((1,"男"),(2,"女"))
    gender = models.SmallIntegerField(verbose_name="性别",choices=gender_choices)
class PreetyNum(models.Model):
    phone = models.CharField(verbose_name="手机号",max_length=11)
    price = models.IntegerField(verbose_name="价格",default=0)
    level_choices = ((1,"1级"),(2,"2级"),(3,"3级"),(4,"4级"),(5,"5级"),)
    level = models.SmallIntegerField(verbose_name="等级",choices=level_choices,default=1)
    status_choices = ((1,"已占用"),(2,"未占用"))
    status = models.SmallIntegerField(verbose_name="状态",choices=status_choices)
class Admin(models.Model):
    name = models.CharField(verbose_name="用户名",max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
    def __str__(self):
        return self.name
class Order(models.Model):
    oid = models.CharField(verbose_name="订单号",max_length=64)
    title = models.CharField(verbose_name="名称",max_length=32)
    price = models.IntegerField(verbose_name="价格")
    status_choices = (
            (1,"待支付"),
            (2,"已支付"),
    )
    status = models.SmallIntegerField(verbose_name="状态",choices=status_choices,default=1)
    admin = models.ForeignKey(verbose_name="管理员",to="Admin",on_delete=models.CASCADE)
class City(models.Model):
    name = models.CharField(verbose_name="名称",max_length=32)
    count = models.IntegerField(verbose_name="人口数",max_length=64)
    img = models.FileField(verbose_name="Logo",max_length=128,upload_to="city/")#自动添加到Media目录下去