from django.shortcuts import render,HttpResponse
from apps.test_case.services.HTTP_test_case_debugService import HTTP_test_case_debugService
from apps.test_case.services.HTTP_test_case_step_debugService import HTTP_test_case_step_debugService
from apps.common.func.CommonFunc import *
from apps.common.func.LanguageFunc import *
import json,time
from apps.version_manage.services.common_service import VersionService
from apps.common.func.WebFunc import *
from apps.common.model.RedisDBConfig import *
from all_models.models import *
from apps.common.func.ValidataFunc import *

def testCaseDebugAdd(request):
    testCaseDebugId = "testCaseDebug_%s_%s" % (request.session.get("loginName"),int(time.time() * 1000))
    testCaseStepDebugId = "testCaseStepDebug_%s_%s" % (request.session.get("loginName"),int(time.time() * 1000))
    postLoad = json.loads(request.POST.get("stepArr"))

    for i in range(0, len(postLoad['step'])):
        thisStep = postLoad["step"][i]
        retB, retS = verifyPythonMode(thisStep["varsPre"])
        if retB == False:
            return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_DEBUG_ADD_EXCEPITON, "准备中出现不允许的输入：%s" % retS,
                                          "准备中出现不允许的输入：%s" % retS).toJson())
        retB, retS = verifyPythonMode(thisStep["varsPost"])
        if retB == False:
            return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_DEBUG_ADD_EXCEPITON, "断言恢复中出现不允许的输入：%s" % retS,
                                          "断言恢复中出现不允许的输入：%s" % retS).toJson())

    testCaseData = {}
    testCaseData["caseId"] = postLoad["caseId"]
    testCaseData["title"] = postLoad["title"]
    testCaseData["casedesc"] = postLoad["casedesc"]
    testCaseData["caselevel"] = postLoad["caselevel"]
    testCaseData["stepCount"] = len(postLoad['step'])
    testCaseData["addBy"] = request.session.get("loginName")
    testCaseData["businessLineId"] = postLoad["businessLineId_id"]
    testCaseData["moduleId"] = postLoad["moduleId_id"]
    testCaseData["sourceId"] = postLoad["sourceId_id"]
    testCaseData["httpConfKey"] = postLoad["httpConfKey"]
    testCaseData['version'] = request.session.get("version","CurrentVersion")
    testCaseData['execStatus'] = 1
    testCaseStepList = []
    fileDict = request.FILES
    keyCountDict = {}
    for i in range(0, testCaseData["stepCount"]):
        testCaseStep = {}
        thisStep = postLoad["step"][i]
        testCaseStep["stepNum"] = i + 1
        testCaseStep["title"] = "步骤%s" % testCaseStep["stepNum"]
        testCaseStep["stepDesc"] = thisStep["stepDesc"]
        testCaseStep["fromInterfaceId"] = thisStep["fromInterfaceId"]
        testCaseStep["isSync"] = thisStep["isSync"]
        testCaseStep["varsPre"] = thisStep["varsPre"]
        testCaseStep["uri"] = thisStep["uri"]
        testCaseStep["method"] = thisStep["method"]
        testCaseStep["header"] = thisStep["header"]
        testCaseStep["url"] = thisStep["url"]
        testCaseStep["params"] = thisStep["params"]
        testCaseStep["timeout"] = (thisStep["timeout"] == "" and 20 or thisStep["timeout"])
        testCaseStep["performanceTime"] = (thisStep["performanceTime"] == "" and 1 or float(thisStep["performanceTime"]))
        testCaseStep["varsPost"] = thisStep["varsPost"]
        testCaseStep["businessLineId"] = thisStep["businessLineId_id"]
        testCaseStep["moduleId"] = thisStep["moduleId_id"]
        testCaseStep["sourceId"] = thisStep["sourceId_id"]
        testCaseStep["httpConfKey"] = postLoad["httpConfKey"]
        testCaseStep["state"] = 1
        testCaseStep['version'] = request.session.get("version", "CurrentVersion")
        testCaseStep["useCustomUri"] = thisStep["useCustomUri"]
        testCaseStep["customUri"] = thisStep["customUri"]
        testCaseStep["stepSwitch"] = thisStep["stepSwitch"]
        testCaseStep["urlRedirect"] = thisStep["urlRedirect"]
        if thisStep["method"] != "GET" and thisStep["method"] != "HEAD":
            testCaseStep["bodyType"] = thisStep["bodyType"]
            bodyContent = thisStep["bodyContent"]
            if testCaseStep["bodyType"] == "binary":
                if "realPath" in bodyContent:
                    testCaseStep["bodyContent"] = json.dumps(bodyContent, ensure_ascii=False)
                else:
                    if not fileDict.get("file"):
                        pass
                    thisFile = fileDict.get("file")
                    contentRealPath = updateFileSave(request.session.get("loginName"), thisFile, "0")
                    bodyContent["realPath"] = contentRealPath
                    bodyContent["fileType"] = thisFile.content_type
                    testCaseStep["bodyContent"] = json.dumps(bodyContent, ensure_ascii=False)
            elif testCaseStep["bodyType"] == "form-data":
                if (type(bodyContent) == str):
                    bodyContent = json.loads(bodyContent)
                for bodyContentIndex in range(0, len(bodyContent)):
                    tmpAttr = bodyContent[bodyContentIndex]
                    if tmpAttr['type'] == "file":
                        if "value" not in bodyContent[bodyContentIndex].keys() or "realPath" in bodyContent[bodyContentIndex]["value"]:
                            continue
                        fileKey = tmpAttr['key']
                        if fileKey in keyCountDict.keys():
                            keyCountDict[fileKey] += 1
                        else:
                            keyCountDict[fileKey] = 0
                        tmpFileTempObj = fileDict.getlist(fileKey)[keyCountDict[fileKey]]
                        contentRealPath = updateFileSave(request.session.get("loginName"), tmpFileTempObj,keyCountDict[fileKey])
                        bodyContent[bodyContentIndex]['value']['fileType'] = tmpFileTempObj.content_type
                        bodyContent[bodyContentIndex]['value']['realPath'] = contentRealPath
                testCaseStep["bodyContent"] = json.dumps(bodyContent, ensure_ascii=False)
            else:
                testCaseStep["bodyContent"] = thisStep["bodyContent"]
        else:
            testCaseStep["bodyType"] = ""
            testCaseStep["bodyContent"] = ""
        testCaseStep["execStatus"] = 1
        testCaseStep["actualResult"] = ""
        testCaseStep["assertResult"] = ""
        testCaseStep["testResult"] = "NOTRUN"
        testCaseStep["beforeExecuteTakeTime"] = 0
        testCaseStep["afterExecuteTakeTime"] = 0
        testCaseStep["executeTakeTime"] = 0
        testCaseStep["totalTakeTime"] = 0

        testCaseStepList.append(testCaseStep)
    try:
        RedisCache().set_data(testCaseDebugId,json.dumps(testCaseData),60*60)
        RedisCache().set_data(testCaseStepDebugId,json.dumps(testCaseStepList),60*60)
    except Exception as e:
        addUserLog(request,"业务流管理->添加用例调试->失败", "FAIL")
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR).toJson())

    addUserLog(request, "业务流管理->添加用例调试->成功", "PASS")
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK,body={"testCaseDebugId":testCaseDebugId,"testCaseStepDebugId":testCaseStepDebugId}).toJson())

def debugTestCase(request):
    langDict = getLangTextDict(request)
    testCaseDebugId = request.POST.get("testCaseDebugId")
    testCaseStepDebugId = request.POST.get("testCaseStepDebugId")
    # dataAddBy = request.session.get("loginName")
    # caseDebugId = HTTP_test_case_debugService.getCaseDebugId(dataAddBy)
    #
    # caseDebugStepList = HTTP_test_case_step_debugService.getStepIdList(dataAddBy)
    # caseDebugIdList = ''
    # for i in range(0,len(caseDebugStepList)):
    #     if i == 0:
    #         caseDebugIdList += str(caseDebugStepList[i]["id"])
    #         continue
    #     caseDebugIdList += ",%s" % str(caseDebugStepList[i]["id"])
    tcpStr = '{"do":2,"CaseDebugId":"%s","CaseStepDebugIdList":"%s","protocol":"HTTP"}' % (testCaseDebugId,testCaseStepDebugId)
    retApiResult = send_tcp_request(tcpStr)
    if retApiResult.code != ApiReturn.CODE_OK:
        debugMsg = {}
        debugMsg["execStatus"] = 4
        debugMsg["testResult"] = "ERROR"
        debugMsg["assertResult"] = retApiResult.message
        debugMsg["modTime"] = datetime.datetime.now()
        RedisCache().del_data(testCaseDebugId)
        RedisCache().del_data(testCaseStepDebugId)
        # HTTP_test_case_debugService.setDebugFail(dataAddBy,debugMsg)
        addUserLog(request, "业务流管理->添加用例调试->发送TCP消息->失败,原因\n%s" % retApiResult.toJson(), "FAIL")
        return HttpResponse(retApiResult.toJson())
    else:
        addUserLog(request, "业务流管理->添加用例调试->发送TCP消息->成功", "PASS")
        return HttpResponse(ApiReturn(ApiReturn.CODE_OK, langDict['web']['httpInterfaceDebugSuccess']).toJson())

def getDebugResult(request):
    langDict = getLangTextDict(request)
    testCaseDebugId = request.POST.get("testCaseDebugId")
    testCaseStepDebugId = request.POST.get("testCaseStepDebugId")

    startTime = time.time()
    while True:
        if (time.time() - startTime) >= 1:
            return HttpResponse(ApiReturn(ApiReturn.CODE_DEBUG_TIMEOUT, langDict['web']['httpDebugTimeout']).toJson())

        debugResult = json.loads(RedisCache().get_data(testCaseDebugId))
        debugStepResult = json.loads(RedisCache().get_data(testCaseStepDebugId))
        if debugResult["execStatus"] == 3 or debugResult["execStatus"] == 4:
            # RedisCache().del_data(testCaseDebugId)
            # RedisCache().del_data(testCaseStepDebugId)
            debugResultDict = debugResult
            debugResultDict["alias"] = TbConfigHttp.objects.get(httpConfKey=debugResult["httpConfKey"]).alias
            # httpConfKeyDict = dbModelToDict(debugResult.httpConfKey)
            # debugResultDict.update(httpConfKeyDict)
            debugResultDict['step'] = []
            for i in range(0,len(debugStepResult)):
                # debugStepResultDict =
                # debugStepHttpConfKeyDict = dbModelToDict(debugStepResult[i].httpConfKey)
                # debugStepBussubessLineDict = dbModelToDict(debugStepResult[i].businessLineId)
                # debugStepResultDict.update(debugStepHttpConfKeyDict)
                # debugStepResultDict.update(debugStepBussubessLineDict)
                debugResultDict['step'].append(debugStepResult[i])
            addUserLog(request, "业务流管理->添加用例调试->获取调试结果->成功", "PASS")
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK,body=debugResultDict).toJson())
