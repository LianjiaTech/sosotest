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

def updateWebPortalData(request):
    tmpSrcRoot = "%s/AutotestWebD/apps/webportal/scripts" % (releaseDir)

   
    resultList = []
    for index in WebPortalService.scriptList:
        # if "openApi" in index:
        #     continue
        thisResule = {"code":10000,"msg":"%s 执行成功!" % index}
        output = os.popen('cd %s && python3 %s' % (tmpSrcRoot,index))
        outStr = output.read()
        if "done!" not in outStr:
            thisResule = {"code": 10001, "msg": "%s  执行失败!"% index,"body":'cd %s && python3 %s' % (tmpSrcRoot,index)}
        resultList.append(thisResule)
    return HttpResponse(ApiReturn(resultList).toJson())

def updateTaskToCurrentVersion(request):
    try:
        oldVersion = request.GET.get("version","")
        if oldVersion == "":
            oldVersion = TbVersion.objects.filter(state=1).order_by("-addTime")[1].versionName
        currentVersion = TbVersion.objects.get(type=2).versionName
        taskList = dbModelListToListDict(TbWebPortalStandardTask.objects.filter(version=oldVersion))
        for index in taskList:
            tbModel = TbWebPortalStandardTask()
            tbModel.version = currentVersion
            tbModel.businessLine = index["businessLine"]
            tbModel.team = index["team"]
            tbModel.taskId = index["taskId"]
            tbModel.head = index["head"]
            tbModel.save()
    except Exception as e:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR, message="添加失败%s " % e).toJson())
    return HttpResponse(ApiReturn(code=ApiReturn.CODE_OK,message="添加成功").toJson())