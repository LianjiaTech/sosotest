from django.shortcuts import render,HttpResponse
from urllib import parse
from apps.common.func.CommonFunc import *
import datetime,time
from urllib.parse import urlparse
from apps.common.model.RedisDBConfig import *

def interface_plug_in(request):
    redisKey = "%s" % (round(time.time() * 1000))
    print(request.POST.get("request"))
    try:
        requestData = json.loads(request.POST.get("requestData"))
    except Exception:
        return HttpResponse(ApiReturn(code=10001,message="无法解析为json对象，请联系管理员").toJson())


    RedisCache().set_data("%s_interface_%s" % (request.session.get("loginName"),redisKey),json.dumps(requestData),60*60)
    return HttpResponse(ApiReturn(body=redisKey).toJson())


def getRedisIntrerface(request):
    try:
        redisKey = request.GET.get("dataKey")
        interfaceData = RedisCache().get_data("%s_interface_%s" % (request.session.get("loginName"),redisKey))
        print(interfaceData)
        # RedisCache().del_data("%s_interface_%s" % (request.session.get("loginName"),redisKey))

    except Exception:
        return HttpResponse(ApiReturn(code=10001,message="%s 不存在" % redisKey).toJson())


    return HttpResponse(ApiReturn(body=interfaceData).toJson())
