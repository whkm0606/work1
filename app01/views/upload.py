from django.http import JsonResponse, HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def upload_list(request):
    if request.method == "get":
        return render(request,"upload.html")
    fidel_object = request.FILES.get("image")#获取文件
    f = open(fidel_object.name,mode='wb') #进行上传文件
    for chunk in fidel_object.chunks():
        f.write(chunk)
    f.close()
    return render(request,"upload.html")