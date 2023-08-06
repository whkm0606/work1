from django.conf import settings
import hashlib
def mb5(data_string):#进行加密
    obj = hashlib.md5(settings.SECRET_KEY.encode("UTF-8"))
    obj.update(data_string.encode("UTF-8"))
    return obj.hexdigest()