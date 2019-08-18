from django.shortcuts import render,HttpResponse
from apps.dubbo_interface.services.dubbo_interface_service import DubboInterfaceService
from apps.dubbo_interface.services.dubbo_interface_debug_service import DubboInterfaceDebugService
from apps.common.func.CommonFunc import *
from apps.common.func.LanguageFunc import *
from apps.common.helper.ApiReturn import ApiReturn
from AutotestWebD import settings
import json,time,logging
from apps.common.func.WebFunc import *
from apps.common.model.RedisDBConfig import *
logger = logging.getLogger("web")

def interfaceDebugAdd(request):
    testDebugId = "interfaceDebug_%s_%s" % (request.session.get("loginName"),int(time.time() * 1000))
    if request.method != 'POST':
        addUserLog(request, "DUBBO单接口管理->添加接口调试->请求方式错误", "FAIL")
        return HttpResponse(ApiReturn(ApiReturn.CODE_METHOD_ERROR,"请求方式错误","").toJson())
    data = json.loads(request.POST.get("interfaceData"))
    data['version'] = request.session.get("version")
    langDict = getLangTextDict(request)
    try:
        # addDebugRes = DubboInterfaceDebugService.interfaceDebugAdd(data,request.session.get("loginName"))
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
        RedisCache().set_data(testDebugId, json.dumps(data), 60 * 60)
        # if isinstance(addDebugRes,str):
        #     return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_DEBUG_ADD_EXCEPITON,
        #                                   langDict['dubbo']['interfaceDebugAddError'],
        #                                   "%s" % str(addDebugRes)).toJson())
        # else:
        #     debugId = addDebugRes.id


    except Exception as e:
        logging.error(traceback.format_exc())
        addUserLog(request, "DUBBO单接口管理->添加接口调试->插入失败，原因\n%s" % ApiReturn(ApiReturn.CODE_INTERFACE_DEBUG_ADD_EXCEPITON,langDict['web']['httpInterfaceDebugAddException'],"%s" % e).toJson(), "FAIL")
        return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_DEBUG_ADD_EXCEPITON,langDict['web']['httpInterfaceDebugAddException'],"%s" % e).toJson())

    addUserLog(request, "DUBBO单接口管理->添加接口调试->成功" , "PASS")
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK,langDict['web']['httpInterfaceDebugAdd'],str(testDebugId)).toJson())

def sendDebugInterfaceTcpMsg(request):
    langDict = getLangTextDict(request)
    #aaabbb
    tcpStr = '{"do":1,"InterfaceDebugId":"%s","protocol":"DUBBO"}' % request.POST.get("body")
    retApiResult = send_tcp_request(tcpStr)
    if retApiResult.code != ApiReturn.CODE_OK:
        debugMsg = {}
        debugMsg["execStatus"] = 4
        debugMsg["actualResult"] = str(retApiResult.code)+":"+retApiResult.message
        debugMsg["assertResult"] = str(retApiResult.code)+":"+retApiResult.message
        debugMsg["modTime"] = datetime.datetime.now()
        DubboInterfaceDebugService.setDebugFail(request.session.get("loginName"),debugMsg)
        addUserLog(request, "DUBBO单接口管理->接口调试->发送TCP请求->失败，原因\n%s" % retApiResult.toJson(), "FAIL")
        return HttpResponse(retApiResult.toJson())
    else:
        addUserLog(request, "DUBBO单接口管理->接口调试->发送TCP请求->成功", "PASS")
        return HttpResponse(ApiReturn(ApiReturn.CODE_OK, langDict['web']['httpInterfaceDebugSuccess']).toJson())

def getDebugResult(request):
    langDict = getLangTextDict(request)
    testDebugId = request.POST.get("body")
    startTime = time.time()
    while True:
        if (time.time() - startTime) >= 1:
            return HttpResponse(ApiReturn(ApiReturn.CODE_DEBUG_TIMEOUT, langDict['web']['httpDebugTimeout']).toJson())
        # debugResult = DubboInterfaceDebugService.getDebugResult(request.session.get("loginName"))
        # if debugResult != 0:
        #     addUserLog(request, "DUBBO单接口管理->接口调试->获取结果->成功", "PASS")
        #     print(debugResult)
        #     return render(request,"dubbo/interface/SubPages/interface_debug_page.html",debugResult)
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
            return render(request, "dubbo/interface/SubPages/interface_debug_page.html", debugResult)

if __name__=="__main__":
    print(settings.BASE_DIR)