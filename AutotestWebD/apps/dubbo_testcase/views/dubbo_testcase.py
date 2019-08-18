from django.shortcuts import render, HttpResponse
from urllib import parse
from apps.test_case.services.HTTP_test_caseService import HTTP_test_caseService
from apps.test_case.services.HTTP_test_case_stepService import HTTP_test_case_stepService
from apps.interface.services.HTTP_interfaceService import HTTP_interfaceService
from apps.test_case.services.HTTP_test_case_debugService import HTTP_test_case_debugService
from apps.test_case.services.HTTP_test_case_step_debugService import HTTP_test_case_step_debugService
from apps.common.config import commonWebConfig
from apps.common.func.CommonFunc import *
from apps.common.func.LanguageFunc import *
from apps.config.services.businessLineService import BusinessService
from apps.config.services.modulesService import ModulesService
from apps.config.services.uriService import UriService
from apps.config.services.serviceConfService import ServiceConfService
from apps.config.services.http_confService import HttpConfService
from apps.config.views.http_conf import getDebugBtn
from apps.common.func.WebFunc import *
from AutotestWebD.settings import isRelease
import json, time
from apps.version_manage.services.common_service import VersionService
from all_models.models import *
from apps.dubbo_testcase.services.dubbo_testcase_service import DubboTestcaseService
from apps.dubbo_interface.services.dubbo_interface_service import DubboInterfaceService
from apps.dubbo_common.services.ConfigServiceForDubbo import ConfigServiceForDubbo
from apps.common.func.ValidataFunc import *
from apps.common.decorator.permission_normal_funcitons import *
from all_models_for_dubbo.models import *

def dubbo_testCaseCheck(request):
    langDict = getLangTextDict(request)
    context = {}

    context["dubbo_testCaseCheck"] = "current-page"
    context["userName"] = request.session.get("userName")
    context["checkBusinessLine"] = dbModelListToListDict(BusinessService.getAllBusinessLine())
    context["checkModules"] = dbModelListToListDict(ModulesService.getAllModules())
    if not isRelease:
        context["env"] = "test"
    # 文本
    text = {}
    text["pageTitle"] = langDict["dubbo"]["dubboTestCasePageHeadings_check"]
    context["text"] = text

    context["page"] = 1

    # context["lang"] = getLangTextDict(request)
    context["title"] = "DUBBO业务流"
    return render(request, "dubbo/testcase/testCase_check.html", context)

def dubbo_testCaseListCheck(request):
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        return HttpResponse("<script>alert('请验证页数参数');</script>")

    checkArr = json.loads(parse.unquote(request.POST.get("checkVal")))

    orderBy = request.POST.get("orderBy")
    if isSqlInjectable(orderBy):
        return HttpResponse("<script>alert('查询条件非法');</script>")

    # 根据版本判断应该从哪个表里取数据 王吉亮添加于20180224
    if VersionService.isCurrentVersion(request):
        tbName = "tb2_dubbo_testcase"
        versionCondition = ""
    else:
        tbName = "tb_version_http_testcase"
        versionCondition = "and versionName='%s'" % request.session.get("version")

    execSql = "SELECT t.*,u.userName,m.moduleName,b.bussinessLineName,mu.userName modByName from %s t LEFT JOIN tb_user mu ON t.modBy = mu.loginName LEFT JOIN tb_modules m on t.moduleId = m.id LEFT JOIN tb_business_line b on t.businessLineId = b.id LEFT JOIN tb_user u ON t.addBy = u.loginName WHERE 1=1 and t.state=1 %s" % (
    tbName, versionCondition)
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        elif key == "caseFounder":
            checkList.append("%%%s%%" % checkArr[key])
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and (t.addBy LIKE %s or u.userName LIKE %s) """
            continue
        elif key == "module":
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and m.moduleName LIKE %s """
            continue
        elif key == "businessLine":
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and b.bussinessLineName LIKE %s """
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and t.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy

    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.testCasePageNum,request=request)

    response = render(request, "dubbo/testcase/SubPages/testCase_list_check_page.html", context)
    return response

def queryPeopleTestCase(request):
    langDict = getLangTextDict(request)
    pageNum = int(request.GET.get("num"))
    if VersionService.isCurrentVersion(request):
        attrData = DubboTestcaseService.queryPeopleTestCase(pageNum, commonWebConfig.queryPeopleInterface,
                                                             request.session.get("loginName"))
    else:
        attrData = HTTP_test_caseService.queryVersionPeopleTestCase(pageNum, commonWebConfig.queryPeopleInterface,
                                                                    request.session.get("loginName"),
                                                                    VersionService.getVersionName(request))
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK, langDict["web"]["httpTestCaseSuccess"], attrData).toJson())

@single_add_page_permission
def testCaseAddPage(request,context):
    langDict = getLangTextDict(request)

    context["page"] = 1
    context["option"] = "add"
    context["dubbo_addHTTPTestCase"] = "current-page"
    context["checkBusinessLine"] = dbModelListToListDict(BusinessService.getAllBusinessLine())
    context["checkModules"] = dbModelListToListDict(ModulesService.getAllModules())
    if not isRelease:
        context["env"] = "test"
    # 文本
    text = {}
    text["pageTitle"] = langDict["dubbo"]["dubboTestCasePageHeadings_%s" % context["option"]]
    text["subPageTitle"] = langDict["dubbo"]["dubboTestCaseSubPageTitle_%s" % context["option"]]
    context["text"] = text

    # 页面所需参数
    context["loginName"] = request.session.get("loginName")
    context.update(getConfigs(request))

    context["debugBtnCount"] = commonWebConfig.debugBtnCount

    # 调试按钮
    getDebugBtnList = ConfigServiceForDubbo.getDebugBtn(request)
    context.update(getDebugBtnList)

    context["title"] = "添加DUBBO业务流"
    return render(request, "dubbo/testcase/testCase.html", context)

# def testCaseStepPage(request):
#     context = {}
#     context.update(getConfigs(request))
#     context.update(getServiceConf(request))
#     context["debugBtnCount"] = commonWebConfig.debugBtnCount
#
#     context.update(ConfigServiceForDubbo.getConfigs(request))
#
#     envConfList = DubboInterfaceService.queryDubboConfSort(request)
#     context["envConfList"] = envConfList
#     return render(request, "dubbo/testcase/SubPages/testcase_step_page.html", context)

def testCaseStepPage(request):
    context = {}
    return render(request, "dubbo/testcase/SubPages/testcase_step_page.html", context)

def testCaseStepDetailPage(request):

    context = {}
    context.update(getConfigs(request))
    context.update(getServiceConf(request))
    context["debugBtnCount"] = commonWebConfig.debugBtnCount

    context.update(ConfigServiceForDubbo.getConfigs(request))

    envConfList = DubboInterfaceService.queryDubboConfSort(request)
    context["envConfList"] = envConfList
    return render(request, "dubbo/testcase/SubPages/testcase_step_detail_page.html", context)


@single_data_permission(Tb2DubboTestcase,Tb2DubboTestcase)
def testCaseAdd(request):
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
    testCaseData["title"] = postLoad["title"]
    testCaseData["casedesc"] = postLoad["casedesc"]
    testCaseData["caselevel"] = postLoad["caselevel"]
    testCaseData["stepCount"] = len(postLoad['step'])
    testCaseData["addBy_id"] = request.session.get("loginName")
    testCaseData["businessLineId_id"] = postLoad["businessLineId_id"]
    testCaseData["moduleId_id"] = postLoad["moduleId_id"]
    # testCaseData["sourceId_id"] = postLoad["sourceId"]
    try:
        if VersionService.isCurrentVersion(request):
            testCaseDataAdd = DubboTestcaseService.testCaseAdd(testCaseData)
        else:
            testCaseDataAdd = DubboTestcaseService.testVersionCaseAdd(testCaseData,
                                                                       VersionService.getVersionName(request))

    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_TESTCASE_ERROR, "添加用例错误", "Failed: %s" % e).toJson())
    fileDict = request.FILES
    keyCountDict = {}
    for i in range(0, len(postLoad['step'])):
        testCaseStep = {}
        thisStep = postLoad["step"][i]
        testCaseStep["stepNum"] = i + 1
        testCaseStep["title"] = "步骤%s" % testCaseStep["stepNum"]
        testCaseStep["stepDesc"] = thisStep["stepDesc"]
        testCaseStep["fromInterfaceId"] = thisStep["fromInterfaceId"]
        testCaseStep["isSync"] = thisStep["isSync"]
        testCaseStep["varsPre"] = thisStep["varsPre"]
        testCaseStep["dubboSystem"] = thisStep["dubboSystem"]
        testCaseStep["dubboService"] = thisStep["dubboService"]
        testCaseStep["dubboMethod"] = thisStep["dubboMethod"]
        testCaseStep["stepSwitch"] = thisStep["stepSwitch"]
        testCaseStep["customUri"] = thisStep["customUri"]
        testCaseStep["useCustomUri"] = thisStep["useCustomUri"]
        testCaseStep["dubboParams"] = thisStep["dubboParams"]
        testCaseStep["encoding"] = thisStep["encoding"]
        # testCaseStep["timeout"] = thisStep["timeout"]
        testCaseStep["varsPost"] = thisStep["varsPost"]
        testCaseStep["businessLineId_id"] = thisStep["businessLineId_id"]
        testCaseStep["moduleId_id"] = thisStep["moduleId_id"]
        # testCaseStep["sourceId_id"] = thisStep["sourceId"]
        testCaseStep["addBy_id"] = request.session.get("loginName")

        if VersionService.isCurrentVersion(request):
            testCaseStep["caseId_id"] = testCaseDataAdd.caseId
        else:
            testCaseStep["caseId"] = testCaseDataAdd.caseId

        try:
            if VersionService.isCurrentVersion(request):
                DubboTestcaseService.testCaseStepAdd(testCaseStep)
            else:
                HTTP_test_case_stepService.testVersionCaseStepAdd(testCaseStep, VersionService.getVersionName(request))

        except Exception as e:
            print(e)
            return HttpResponse(ApiReturn(ApiReturn.CODE_TESTCASE_ERROR, "添加用例错误", "Failed: %s" % e).toJson())
    if VersionService.isCurrentVersion(request):
        syncTestCaseStepFromInterfaceId(request,testCaseDataAdd.caseId)
    else:
        syncVersionTestCaseStepFromInterfaceId(testCaseDataAdd.caseId, VersionService.getVersionName(request))

    return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())

def selectInterfaceAddStep(request):
    langDict = getLangTextDict(request)

    interfaceArr = request.POST.get("list").split(",")

    interfaceList = []
    if VersionService.isCurrentVersion(request):
        for i in range(0, len(interfaceArr)):
            interfaceList.append(dbModelToDict(DubboInterfaceService.getInterfaceForInterfaceId(interfaceArr[i])))
    else:
        # 历史版本
        for i in range(0, len(interfaceArr)):
            interfaceList.append(dbModelToDict(HTTP_interfaceService.getVersionInterfaceForInterfaceId(interfaceArr[i],request.session.get("version"))))

    return HttpResponse(ApiReturn(ApiReturn.CODE_OK, langDict['web']['httpTestCaseSuccess'], interfaceList).toJson())

def testCaseSelectInterfaceCheckList(request):
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))

    orderBy = request.POST.get("orderBy")
    if isSqlInjectable(orderBy):
        return HttpResponse("<script>alert('查询条件非法');</script>")

    if VersionService.isCurrentVersion(request):
        tbName = "tb2_dubbo_interface"
        versionCondition = ""
    else:
        tbName = "tb_version_http_interface"
        versionCondition = "and versionName='%s'" % request.session.get("version")

    execSql = "SELECT i.*,u.userName from %s i LEFT JOIN tb_user u ON i.addBy = u.loginName LEFT JOIN  tb_modules m ON i.moduleId = m.id LEFT JOIN tb_business_line b ON i.businessLineId = b.id  WHERE 1=1 and i.state=1 %s " % (
    tbName, versionCondition)
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        elif key == "caseFounder":
            checkList.append("%%%s%%" % checkArr[key])
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and (i.addBy LIKE %s or u.userName LIKE %s) """
            continue
        elif key == "module":
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and m.moduleName LIKE %s """
            continue
        elif key == "businessLine":
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and b.bussinessLineName LIKE %s """
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and i.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.interfaceSelectPageNum)
    response = render(request, "dubbo/testcase/SubPages/TestCase_Select_interface_list_check_page.html", context)
    return response

@single_page_permission
def operationTestCase(request,context):
    langDict = getLangTextDict(request)

    context["id"] = request.GET.get("id")
    context["option"] = request.GET.get("option")
    context["page"] = 1
    context["dubbo_addHTTPTestCase"] = "current-page"
    if not isRelease:
        context["env"] = "test"
    try:
        if VersionService.isCurrentVersion(request):
            context["dataAddBy"] = DubboTestcaseService.getTestCaseForId(request.GET.get("id")).addBy.loginName
        else:
            context["dataAddBy"] = HTTP_test_caseService.getVersionTestCaseForId(request.GET.get("id")).addBy.loginName

    except Exception as e:
        return HttpResponse("参数id错误 %s" % e)

    # 文本
    text = {}
    try:
        text["pageTitle"] = langDict["dubbo"]["dubboTestCasePageHeadings_%s" % context["option"]]
        text["subPageTitle"] = langDict["dubbo"]["dubboTestCasePageHeadings_%s" % context["option"]]
    except Exception as e:
        return HttpResponse("参数错误 %s" % e)
    context["text"] = text

    context.update(ConfigServiceForDubbo.getConfigs(request))
    context.update(getServiceConf(request))
    context["debugBtnCount"] = commonWebConfig.debugBtnCount
    getDebugBtnList = ConfigServiceForDubbo.getDebugBtn(request)
    context.update(getDebugBtnList)
    context["serviceJson"] = json.dumps(ServiceConfService.queryServiceConfSort(request))
    context["title"] = "DUBBO业务流-" + request.GET.get("id")
    return render(request, "dubbo/testcase/testCase.html", context)

def getTestCaseDataForId(request):
    langDict = getLangTextDict(request)
    if VersionService.isCurrentVersion(request):
        getDBData = DubboTestcaseService.getTestCaseForIdToDict(request.GET.get("id"))
        getDBData["step"] = DubboTestcaseService.getTestCaseStep(getDBData["caseId"])
    else:
        getDBData = HTTP_test_caseService.getVersionTestCaseForIdToDict(request.GET.get("id"))
        getDBData["step"] = HTTP_test_case_stepService.getVersionTestCaseStep(getDBData["caseId"],
                                                                              request.session.get("version"))
    return HttpResponse(
        ApiReturn(ApiReturn.CODE_OK, langDict["web"]["httpTestCaseSuccess"], json.dumps(getDBData)).toJson())

@single_data_permission(Tb2DubboTestcase,Tb2DubboTestcase)
def testCaseSaveEdit(request):
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

    # if VersionService.isCurrentVersion(request):
    #     thisUser = dbModelToDict(DubboTestcaseService.getTestCaseForId(postLoad["id"]))
    # else:
    #     thisUser = dbModelToDict(DubboTestcaseService.getVersionTestCaseForId(postLoad["id"]))

    # if thisUser["addBy_id"] != request.session.get("loginName"):
    #     return HttpResponse(ApiReturn(ApiReturn.CODE_TESTCASE_ERROR, '只可以编辑自己的用例').toJson())

    testCaseData = {}
    testCaseData["id"] = postLoad["id"]
    testCaseData["title"] = postLoad["title"]
    testCaseData["casedesc"] = postLoad["casedesc"]
    testCaseData["caselevel"] = postLoad["caselevel"]
    testCaseData["stepCount"] = len(postLoad['step'])
    testCaseData["modBy"] = request.session.get("loginName")
    testCaseData["businessLineId_id"] = postLoad["businessLineId_id"]
    testCaseData["moduleId_id"] = postLoad["moduleId_id"]
    # testCaseData["sourceId_id"] = postLoad["sourceId"]
    testCaseData["modTime"] = datetime.datetime.now()
    if VersionService.isCurrentVersion(request):
        testCaseDataSaveEdit = DubboTestcaseService.saveEdit(testCaseData)
    else:
        testCaseData["versionName_id"] = VersionService.getVersionName(request)
        testCaseDataSaveEdit = DubboTestcaseService.saveVersionEdit(testCaseData)

    if testCaseDataSaveEdit != 1:
        return HttpResponse(ApiReturn(ApiReturn.CODE_TESTCASE_ERROR, '保存编辑用例失败').toJson())

    fileDict = request.FILES
    keyCountDict = {}
    if VersionService.isCurrentVersion(request):
        DBstepNum = DubboTestcaseService.getTestCaseAllStep(postLoad["caseId"])
    else:
        DBstepNum = HTTP_test_case_stepService.getVersionTestCaseAllStep(postLoad["caseId"],
                                                                         VersionService.getVersionName(request))

    if testCaseData["stepCount"] <= len(DBstepNum):
        for i in range(0, len(DBstepNum)):
            if i < testCaseData["stepCount"]:
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

                testCaseStep["varsPost"] = thisStep["varsPost"]
                testCaseStep["businessLineId_id"] = thisStep["businessLineId_id"]
                testCaseStep["moduleId_id"] = thisStep["moduleId_id"]
                # testCaseStep["sourceId_id"] = thisStep["sourceId"]
                testCaseStep["state"] = 1
                testCaseStep["modTime"] = datetime.datetime.now()
                testCaseStep["modBy"] = request.session.get("loginName")
                if VersionService.isCurrentVersion(request):
                    testCaseStep["caseId_id"] = postLoad["caseId"]
                else:
                    testCaseStep["caseId"] = postLoad["caseId"]
                    testCaseStep["versionName_id"] = VersionService.getVersionName(request)

                if VersionService.isCurrentVersion(request):
                    DubboTestcaseService.updateTestCaseStep(DBstepNum[i]["id"], testCaseStep)
                else:
                    HTTP_test_case_stepService.updateVersionTestCaseStep(DBstepNum[i]["id"], testCaseStep)
            else:
                if VersionService.isCurrentVersion(request):
                    DubboTestcaseService.updateCancel(DBstepNum[i]["id"])
                else:
                    HTTP_test_case_stepService.updateVersionCancel(DBstepNum[i]["id"])
    else:
        for i in range(0, testCaseData["stepCount"]):
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

            testCaseStep["businessLineId_id"] = thisStep["businessLineId_id"]
            testCaseStep["moduleId_id"] = thisStep["moduleId_id"]
            # testCaseStep["sourceId_id"] = thisStep["sourceId"]
            testCaseStep["caseId_id"] = postLoad["caseId"]
            testCaseStep["modTime"] = datetime.datetime.now()
            testCaseStep["modBy"] = request.session.get("loginName")
            if VersionService.isCurrentVersion(request) == False:
                testCaseStep["versionName_id"] = VersionService.getVersionName(request)

            if i < len(DBstepNum):
                testCaseStep["state"] = 1
                if VersionService.isCurrentVersion(request):
                    DubboTestcaseService.updateTestCaseStep(DBstepNum[i]["id"], testCaseStep)
                else:
                    HTTP_test_case_stepService.updateVersionTestCaseStep(DBstepNum[i]["id"], testCaseStep)
            else:
                testCaseStep["addBy_id"] = request.session.get("loginName")
                if VersionService.isCurrentVersion(request):
                    DubboTestcaseService.testCaseStepAdd(testCaseStep)
                else:

                    HTTP_test_case_stepService.testVersionCaseStepAdd(testCaseStep, request.session.get("version"))
    if VersionService.isCurrentVersion(request):
        DubboTestcaseService.syncTestCaseStepFromInterfaceId(postLoad["caseId"])
    else:
        syncVersionTestCaseStepFromInterfaceId(postLoad["caseId"], VersionService.getVersionName(request))
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())

def testCaseDel(request):
    id = request.GET.get("id")
    if VersionService.isCurrentVersion(request):
        try:
            testCaseData = DubboTestcaseService.getTestCaseForId(id)
        except Exception as e:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TESTCASE_ERROR, "参数id错误 %s" % e).toJson())
        # if request.session.get("loginName") != testCaseData.addBy.loginName:
        #     return HttpResponse(ApiReturn(ApiReturn.CODE_TESTCASE_ERROR, "只能删除自己创建的用例").toJson())

        if DubboTestcaseService.delTestCaseForId(id) == 1:
            DubboTestcaseService.stepDel(dbModelToDict(testCaseData)["caseId"])
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        else:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TESTCASE_ERROR).toJson())
    else:
        try:
            testCaseData = HTTP_test_caseService.getVersionTestCaseForId(id)
        except Exception as e:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TESTCASE_ERROR, "参数id错误 %s" % e).toJson())
        # if request.session.get("loginName") != testCaseData.addBy.loginName:
        #     return HttpResponse(ApiReturn(ApiReturn.CODE_TESTCASE_ERROR, "只能删除自己创建的用例").toJson())

        if HTTP_test_caseService.delVersionTestCaseForId(id) == 1:
            HTTP_test_case_stepService.stepVersionDel(dbModelToDict(testCaseData)["caseId"],
                                                      VersionService.getVersionName(request))
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        else:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TESTCASE_ERROR).toJson())

#============================================================================================================================

def updateTestCaseLevel(request):
    userToken = request.GET.get("token", "")

    if userToken == "":
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="toekn为空").toJson())
    try:
        print(TbUser.objects.filter(token=userToken).first())
        userData = TbUser.objects.get(token=userToken)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="token错误，未查询到用户").toJson())

    testCaseId = request.GET.get("testCaseId", "")
    if testCaseId == "":
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="interfaceId为必填参数").toJson())
    try:
        testCaseData = TbHttpTestcase.objects.get(caseId=testCaseId, state=1)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="InterfaceId 参数错误").toJson())

    if userData.loginName != testCaseData.addBy.loginName:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="只能更新自己的接口").toJson())

    levelDict = {"高": 0, "中": 5, "低": 9}
    levelText = request.GET.get("level", "中")

    if levelText in levelDict.keys():
        level = levelDict[levelText]
    else:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="level参数的值为【高】、【中】、【低】").toJson())

    testCaseData.caselevel = level
    testCaseData.save(force_update=True)
    return HttpResponse(ApiReturn().toJson())