from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse,redirect
class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        #排除登录页面做验证：
        if request.path_info in ["/login/","/img_code/"]:
            return
        info_dict = request.session.get("info")
        if info_dict:
            return
        return redirect("/login/")
    def process_response(self, request, response):
        return response