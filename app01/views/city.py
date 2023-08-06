from django.http import HttpResponse

from app01 import models
from app01.utils.pagintion import Pagination
from django.shortcuts import render,redirect
from app01.modelform.form import BAdminModelFrom,BModelForm
class CityModelForm(BModelForm):
    bootstrap_exclude_fields = ['img']
    class Meta:
        model = models.City
        fields = '__all__'

def city_list(request):
    form = CityModelForm
    data_list = models.City.objects.all()
    return render(request,"city_list.html",{"form":form,"city_list":data_list})
def city_add(request):
    if request.method == "get":
        form = CityModelForm
        return render(request,"city_add.html",{"form":form})
    form = CityModelForm(data=request.POST,files=request.FILES)
    from django.utils.datastructures import MultiValueDict
    print(request.FILES.values())
    print(request.FILES)
    if form.is_valid():
        form.save()
        return  redirect("/city_list/")
    return render(request, "city_add.html", {"form": form})