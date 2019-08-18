from django.shortcuts import render
from django.shortcuts import HttpResponse
from apps.common.helper.ApiReturn import ApiReturn
from all_models.models import *
from apps.common.func.CommonFunc import *
from apps.common.func.LanguageFunc import *
from django.forms.models import model_to_dict
from apps.webportal.services.webPortalService import WebPortalService
import time,logging
from apps.common.func.WebFunc import *

def getEnvVersion(request):

    httpConfKey = request.GET.get("httpConfKey","")
    if httpConfKey:
        result = dbModelListToListDict(TbWebPortalStandardEnv.objects.filter(state=1,httpConfKey=httpConfKey))
    else:
        result = dbModelListToListDict(TbWebPortalStandardEnv.objects.filter(state=1))
    for resultIndex in result:
        versionData = TbVersion.objects.get(versionName=resultIndex["version"])
        if versionData:
            versionDict = dbModelToDict(versionData)
            if versionDict["type"] == 2:
                resultIndex["invokeVersion"] = "CurrentVersion"
            else:
                resultIndex["invokeVersion"] = resultIndex["version"]
    return HttpResponse(ApiReturn(body=result).toJson())

def invokeGetEnvVersion(request):
    httpConfKey = request.GET.get("httpConfKey", "")
    if httpConfKey:
        result = dbModelListToListDict(TbWebPortalStandardEnv.objects.filter(state=1, httpConfKey=httpConfKey))
    else:
        return HttpResponse("缺少参数httpConfKey")
    if not result:
        return HttpResponse("httpConfKey未查询到数据")
    invokeVersion = ""
    for resultIndex in result:
        versionData = TbVersion.objects.get(versionName=resultIndex["version"])
        if versionData:
            versionDict = dbModelToDict(versionData)
            if versionDict["type"] == 2:
                invokeVersion = "CurrentVersion"
            else:
                invokeVersion = resultIndex["version"]
    return HttpResponse(invokeVersion)