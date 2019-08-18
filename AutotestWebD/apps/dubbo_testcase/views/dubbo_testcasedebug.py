from django.shortcuts import render,HttpResponse
from apps.test_case.services.HTTP_test_case_debugService import HTTP_test_case_debugService
from apps.test_case.services.HTTP_test_case_step_debugService import HTTP_test_case_step_debugService
from apps.common.func.CommonFunc import *
from apps.common.func.LanguageFunc import *
import json,time
from apps.version_manage.services.common_service import VersionService
from apps.common.func.WebFunc import *
from apps.dubbo_testcase.services.dubbo_testcase_service import DubboTestcaseService
from apps.common.func.ValidataFunc import *
from apps.common.model.RedisDBConfig import *

def testCaseDebugAdd(request):
    testCaseDebugId = "testCaseDebug_%s_%s" % (request.session.get("loginName"), int(time.time() * 1000))
    testCaseStepDebugId = "testCaseStepDebug_%s_%s" % (request.session.get("loginName"), int(time.time() * 1000))
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

    dataAddBy = request.session.get("loginName")
    testCaseData = {}
    testCaseData["caseId"] = postLoad["caseId"]
    testCaseData["title"] = postLoad["title"]
    testCaseData["casedesc"] = postLoad["casedesc"]
    testCaseData["caselevel"] = postLoad["caselevel"]
    testCaseData["stepCount"] = len(postLoad['step'])
    testCaseData["addBy_id"] = request.session.get("loginName")
    testCaseData["businessLineId"] = postLoad["businessLineId_id"]
    testCaseData["moduleId"] = postLoad["moduleId_id"]
    # testCaseData["sourceId_id"] = postLoad["sourceId"]
    # testCaseData["httpConfKey_id"] = postLoad["httpConfKey"]
    testCaseData["httpConfKey"] = postLoad["httpConfKey"]
    testCaseData['version'] = request.session.get("version","CurrentVersion")
    testCaseData['execStatus'] = 1
    # try:
        # DubboTestcaseService.testCaseDebugAdd(dataAddBy, testCaseData)
    # except Exception as e:
    #     logging.error(traceback.format_exc())
    #     addUserLog(request, "DUBBO业务流管理->添加用例调试->插入失败，原因\n%s" % traceback.format_exc(), "FAIL")
    #     return HttpResponse(ApiReturn(ApiReturn.CODE_TESTCASE_DEBUG_EXCEPITON, '保存用例调试信息失败').toJson())

    testCaseStepList = []
    # if testCaseData["stepCount"] <= len(DBstepNum):
    for i in range(0, testCaseData["stepCount"]):
        # if i < testCaseData["stepCount"]:
        testCaseStep = {}
        thisStep = postLoad["step"][i]
        testCaseStep["stepNum"] = i + 1
        testCaseStep["title"] = "步骤%s" % testCaseStep["stepNum"]
        testCaseStep["stepDesc"] = thisStep["stepDesc"]
        testCaseStep["fromInterfaceId"] = thisStep["fromInterfaceId"]
        testCaseStep["isSync"] = thisStep["isSync"]
        testCaseStep["varsPre"] = thisStep["varsPre"]

        testCaseStep["stepSwitch"] = thisStep["stepSwitch"]
        testCaseStep["customUri"] = thisStep["customUri"]
        testCaseStep["useCustomUri"] = thisStep["useCustomUri"]
        testCaseStep["dubboSystem"] = thisStep["dubboSystem"]
        testCaseStep["dubboService"] = thisStep["dubboService"]
        testCaseStep["dubboMethod"] = thisStep["dubboMethod"]
        testCaseStep["dubboParams"] = thisStep["dubboParams"]
        testCaseStep["encoding"] = thisStep["encoding"]

        # testCaseStep["timeout"] = thisStep["timeout"]

        testCaseStep["varsPost"] = thisStep["varsPost"]
        testCaseStep["businessLineId"] = thisStep["businessLineId_id"]
        testCaseStep["moduleId"] = thisStep["moduleId_id"]
        # testCaseStep["sourceId_id"] = thisStep["sourceId"]
        testCaseStep["httpConfKey"] = postLoad["httpConfKey"]
        testCaseStep["state"] = 1
        testCaseStep['version'] = request.session.get("version", "CurrentVersion")

        testCaseStep["execStatus"] = 1
        testCaseStep["actualResult"] = ""
        testCaseStep["assertResult"] = ""
        testCaseStep["testResult"] = "NOTRUN"
        testCaseStep["beforeExecuteTakeTime"] = 0
        testCaseStep["afterExecuteTakeTime"] = 0
        testCaseStep["executeTakeTime"] = 0
        testCaseStep["totalTakeTime"] = 0
        testCaseStepList.append(testCaseStep)

        #     DubboTestcaseService.updateTestCaseStepDebug(DBstepNum[i]["id"], testCaseStep)
        # else:
        #     DubboTestcaseService.updateCancelDebug(DBstepNum[i]["id"])
    try:
        RedisCache().set_data(testCaseDebugId,json.dumps(testCaseData),60*60)
        RedisCache().set_data(testCaseStepDebugId,json.dumps(testCaseStepList),60*60)
    except Exception as e:
        addUserLog(request,"业务流管理->添加用例调试->失败", "FAIL")
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR).toJson())
    addUserLog(request, "DUBBO业务流管理->添加用例调试+步骤->成功", "PASS")
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK,body={"testCaseDebugId":testCaseDebugId,"testCaseStepDebugId":testCaseStepDebugId}).toJson())

def debugTestCase(request):
    langDict = getLangTextDict(request)
    # dataAddBy = request.session.get("loginName")
    # caseDebugId = DubboTestcaseService.getCaseDebugId(dataAddBy)
    testCaseDebugId = request.POST.get("testCaseDebugId")
    testCaseStepDebugId = request.POST.get("testCaseStepDebugId")
    # caseDebugStepList = DubboTestcaseService.getStepIdList(dataAddBy)
    # caseDebugIdList = ''
    # for i in range(0,len(caseDebugStepList)):
    #     if i == 0:
    #         caseDebugIdList += str(caseDebugStepList[i]["id"])
    #         continue
    #     caseDebugIdList += ",%s" % str(caseDebugStepList[i]["id"])
    tcpStr = '{"do":2,"CaseDebugId":"%s","CaseStepDebugIdList":"%s","protocol":"DUBBO"}' % (testCaseDebugId,testCaseStepDebugId)
    retApiResult = send_tcp_request(tcpStr)
    if retApiResult.code != ApiReturn.CODE_OK:
        debugMsg = {}
        debugMsg["execStatus"] = 4
        debugMsg["testResult"] = "ERROR"
        debugMsg["assertResult"] = retApiResult.message
        debugMsg["modTime"] = datetime.datetime.now()
        RedisCache().del_data(testCaseDebugId)
        RedisCache().del_data(testCaseStepDebugId)
        # DubboTestcaseService.setDebugFail(dataAddBy,debugMsg)
        addUserLog(request, "DUBBO业务流管理->添加用例调试->发送TCP消息->失败,原因\n%s" % retApiResult.toJson(), "FAIL")
        return HttpResponse(retApiResult.toJson())
    else:
        addUserLog(request, "DUBBO业务流管理->添加用例调试->发送TCP消息->成功", "PASS")
        return HttpResponse(ApiReturn(ApiReturn.CODE_OK, langDict['web']['httpInterfaceDebugSuccess']).toJson())

def getDebugResult(request):
    langDict = getLangTextDict(request)
    # dataAddBy = request.session.get("loginName")
    testCaseDebugId = request.POST.get("testCaseDebugId")
    testCaseStepDebugId = request.POST.get("testCaseStepDebugId")
    startTime = time.time()
    while True:
        if (time.time() - startTime) >= 1:
            return HttpResponse(ApiReturn(ApiReturn.CODE_DEBUG_TIMEOUT, langDict['web']['httpDebugTimeout']).toJson())

        # debugResult = DubboTestcaseService.getCaseDebug(dataAddBy)
        debugResult = json.loads(RedisCache().get_data(testCaseDebugId))
        debugStepResult = json.loads(RedisCache().get_data(testCaseStepDebugId))
        if debugResult["execStatus"] == 3 or debugResult["execStatus"] == 4:
            print()
            # debugResultDict = dbModelToDict(debugResult)
            # httpConfKeyDict = dbModelToDict(debugResult.httpConfKey)
            # debugResultDict.update(httpConfKeyDict)
            debugResultDict = debugResult
            debugResultDict['step'] = []
            # debugStepResult = DubboTestcaseService.getStep(dataAddBy)
            for i in range(0,len(debugStepResult)):
                print(debugStepResult[i])
                # debugStepResultDict =
                # if int(debugStepResultDict["stepSwitch"]) == 1:
                    # debugStepHttpConfKeyDict = dbModelToDict(debugStepResult[i].httpConfKey)
                    # debugStepBussubessLineDict = dbModelToDict(debugStepResult[i].businessLineId)
                    # debugStepResultDict.update(debugStepHttpConfKeyDict)
                    # debugStepResultDict.update(debugStepBussubessLineDict)
                debugResultDict['step'].append(debugStepResult[i])
            addUserLog(request, "DUBBO业务流管理->添加用例调试->获取调试结果->成功", "PASS")
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK,body=debugResultDict).toJson())
