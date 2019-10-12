from apps.config.services.http_confService import *
from apps.common.config import commonWebConfig
from apps.common.func.CommonFunc import *
import math
from django.shortcuts import HttpResponse

def getDebugBtn(request):
    context = {}
    httpConf = HttpConfService.queryHttpConfSort(request)
    context['httpConf'] = httpConf
    httpConfList = []
    httpConfList.append([])
    if len(httpConf) <= commonWebConfig.debugBtnCount:
        for k in range(0,len(httpConf)):
            httpConfList[0].append(httpConf[k])
    else:
        for k in range(0,commonWebConfig.debugBtnCount-1):
            httpConfList[0].append(httpConf[k])
        httpConfListSize = math.ceil((len(httpConf)-(commonWebConfig.debugBtnCount-1)) / commonWebConfig.debugBtnCount)
        for i in range(1,httpConfListSize+1):
            httpConfList.append([])
            for j in range(i*commonWebConfig.debugBtnCount-1,i*commonWebConfig.debugBtnCount+(commonWebConfig.debugBtnCount-1)):
                if j >= len(httpConf):
                    break
                httpConfList[i].append(httpConf[j])

    context["httpConfList"] = httpConfList
    if len(httpConfList) > 1:
        context["httpConfListPage"] = "open"
    else:
        context["httpConfListPage"] = "close"

    return context

def getHttpConf(request):
    httpConf = HttpConfService.queryHttpConfSort(request)
    httpConfArr = {}
    httpConfArr["key"] = httpConf
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK,body=httpConfArr).toJson())

def getUiConf(request):
    httpConf = HttpConfService.getHttpConfForUI()
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK,body=httpConf).toJson())