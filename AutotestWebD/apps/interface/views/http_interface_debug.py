from django.shortcuts import render,HttpResponse
from apps.interface.services.HTTP_interface_debugService import HTTP_interfaceDebugService
from apps.common.func.CommonFunc import *
from apps.common.func.LanguageFunc import *
from apps.common.helper.ApiReturn import ApiReturn
from AutotestWebD import settings
import json,time,logging
from apps.common.func.WebFunc import *
from apps.common.model.RedisDBConfig import *
from all_models.models import *
logger = logging.getLogger("web")
from apps.common.func.ValidataFunc import *

def interfaceDebugAdd(request):
    testDebugId = "interfaceDebug_%s_%s" % (request.session.get("loginName"),int(time.time() * 1000))
    if request.method != 'POST':
        addUserLog(request, "单接口管理->添加接口调试->请求方式错误", "FAIL")
        return HttpResponse(ApiReturn(ApiReturn.CODE_METHOD_ERROR,"请求方式错误","").toJson())
    data = json.loads(request.POST.get("interfaceData"))
    data['version'] = request.session.get("version")
    if data["method"] != "GET" and data["method"] != "HEAD":
        file = request.FILES
        bodyContent = data["bodyContent"]
        bodyType = data["bodyType"]
        if bodyType == "binary":
            if "realPath" in bodyContent:
                data["bodyContent"] = json.dumps(bodyContent,ensure_ascii=False)
            else:
                if not file.get("file"):
                    pass
                thisFile = file.get("file")
                contentRealPath = updateFileSave(request.session.get("loginName"), thisFile, "0")
                bodyContent["realPath"] = contentRealPath
                bodyContent["fileType"] = thisFile.content_type
                data["bodyContent"] = json.dumps(bodyContent,ensure_ascii=False)
        elif bodyType == "form-data":
            fileDict = request.FILES
            keyCountDict = {}
            for i in range(0,len(bodyContent)):
                tmpAttr = bodyContent[i]
                if tmpAttr['type'] == "file":
                    if "realPath" in bodyContent[i]["value"]:
                        continue
                    fileKey = tmpAttr['key']
                    if fileKey in keyCountDict.keys():
                        keyCountDict[fileKey] += 1
                    else:
                        keyCountDict[fileKey] = 0
                    tmpFileTempObj = fileDict.getlist(fileKey)[keyCountDict[fileKey]]
                    contentRealPath = updateFileSave(request.session.get("loginName"), tmpFileTempObj, keyCountDict[fileKey])
                    bodyContent[i]['value']['fileType'] = tmpFileTempObj.content_type
                    bodyContent[i]['value']['realPath'] = contentRealPath
            data["bodyContent"] = json.dumps(bodyContent,ensure_ascii=False)
    data['actualResult'] = ''
    data['assertResult'] = ''
    data['testResult'] = "NOTRUN"
    data['execStatus'] = 1
    data['beforeExecuteTakeTime'] = 0
    data['executeTakeTime'] = 0
    data['afterExecuteTakeTime'] = 0
    data['totalTakeTime'] = 0
    data['businessLineId'] = data["businessLineId_id"]
    data['moduleId'] = data["moduleId_id"]
    data['httpConfKey'] = data["httpConfKey_id"]
    langDict = getLangTextDict(request)
    try:
        retB,retS = verifyPythonMode(data["varsPre"])
        if retB == False:
            return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_DEBUG_ADD_EXCEPITON,langDict['web']['httpInterfaceDebugAddException'],"准备中出现不允许的输入：%s" % retS).toJson())
        retB, retS = verifyPythonMode(data["varsPost"])
        if retB == False:
            return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_DEBUG_ADD_EXCEPITON,langDict['web']['httpInterfaceDebugAddException'],"断言恢复中出现不允许的输入：%s" % retS).toJson())

        RedisCache().set_data(testDebugId,json.dumps(data),60*60)
        #初始设置接口debug的时间是1小时
        # debugId = HTTP_interfaceDebugService.interfaceDebugAdd(data,request.session.get("loginName")).id
    except Exception as e:
        logging.error(traceback.format_exc())
        addUserLog(request, "单接口管理->添加接口调试->插入失败，原因\n%s" % ApiReturn(ApiReturn.CODE_INTERFACE_DEBUG_ADD_EXCEPITON,langDict['web']['httpInterfaceDebugAddException'],"%s" % e).toJson(), "FAIL")
        return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_DEBUG_ADD_EXCEPITON,langDict['web']['httpInterfaceDebugAddException'],"%s" % e).toJson())
    addUserLog(request, "单接口管理->添加接口调试->成功" , "PASS")
    # return HttpResponse(ApiReturn(ApiReturn.CODE_OK,langDict['web']['httpInterfaceDebugAdd'],str(debugId)).toJson())
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK,langDict['web']['httpInterfaceDebugAdd'],testDebugId).toJson())

def debugInterface(request):
    langDict = getLangTextDict(request)
    testDebugId = request.POST.get("body")
    #aaabbb
    tcpStr = '{"do":1,"InterfaceDebugId":"%s","protocol":"HTTP"}' % testDebugId
    retApiResult = send_tcp_request(tcpStr)
    if retApiResult.code != ApiReturn.CODE_OK:
        debugMsg = {}
        debugMsg["execStatus"] = 4
        debugMsg["actualResult"] = str(retApiResult.code)+":"+retApiResult.message
        debugMsg["assertResult"] = str(retApiResult.code)+":"+retApiResult.message
        debugMsg["modTime"] = datetime.datetime.now()
        RedisCache().del_data(testDebugId)
        # HTTP_interfaceDebugService.setDebugFail(request.session.get("loginName"),debugMsg)
        addUserLog(request, "单接口管理->接口调试->发送TCP请求->失败，原因\n%s" % retApiResult.toJson(), "FAIL")
        return HttpResponse(retApiResult.toJson())
    else:
        addUserLog(request, "单接口管理->接口调试->发送TCP请求->成功", "PASS")
        return HttpResponse(ApiReturn(ApiReturn.CODE_OK, langDict['web']['httpInterfaceDebugSuccess']).toJson())

def getDebugResult(request):
    langDict = getLangTextDict(request)
    startTime = time.time()
    testDebugId = request.POST.get("body")
    while True:
        if (time.time() - startTime) >= 1:
            return HttpResponse(ApiReturn(ApiReturn.CODE_DEBUG_TIMEOUT, langDict['web']['httpDebugTimeout']).toJson())

        try:
            debugResult = json.loads(RedisCache().get_data(testDebugId))
        except Exception as e:
            print(traceback.format_exc())
            return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, "调试结果解析异常，请联系管理员").toJson())
        if debugResult["execStatus"] == 3 or debugResult["execStatus"] == 4:
            debugResult["alias"] = TbConfigHttp.objects.get(httpConfKey=debugResult["httpConfKey"]).alias
            RedisCache().del_data(testDebugId)
            try:
                content = json.loads(debugResult['actualResult'])['content']
                if isJson(content):
                    debugResult["respBodyText"] = content
                else:
                    debugResult["respBodyText"] = ""
            except:
                debugResult["respBodyText"] = ""

            addUserLog(request, "单接口管理->接口调试->获取结果->成功", "PASS")
            return render(request,"InterfaceTest/HTTPInterface/SubPages/HTTP_interface_debug_page.html",debugResult)
if __name__=="__main__":
    print(settings.BASE_DIR)