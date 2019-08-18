from urllib import parse
from apps.common.config import commonWebConfig
from apps.common.func.LanguageFunc import *
from apps.config.views.http_conf import getDebugBtn
from apps.version_manage.services.common_service import VersionService
from apps.common.func.ValidataFunc import *
from apps.common.decorator.permission_normal_funcitons import *
from apps.common.func.WebFunc import *

def http_testCaseCheck(request):
    langDict = getLangTextDict(request)
    context = {}

    context["testCaseCheck"] = "current-page"
    context["userName"] = request.session.get("userName")
    context["checkBusinessLine"] = dbModelListToListDict(BusinessService.getAllBusinessLine())
    context["checkModules"] = dbModelListToListDict(ModulesService.getAllModules())
    if not isRelease:
        context["env"] = "test"
    #文本
    text = {}
    text["pageTitle"] = langDict["web"]["httpTestCasePageHeadings_check"]
    context["text"] = text
    context["page"] = 1
    context["title"] = "HTTP业务流"
    return render(request,"InterfaceTest/HTTPTestCase/HTTP_testCase_check.html",context)

def http_testCaseListCheck(request):
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        return HttpResponse("<script>alert('请验证页数参数');</script>")

    checkArr = json.loads(parse.unquote(request.POST.get("checkVal")))

    orderBy = request.POST.get("orderBy")
    if isSqlInjectable(orderBy):
        return HttpResponse("<script>alert('查询条件非法');</script>")

    #根据版本判断应该从哪个表里取数据 王吉亮添加于20180224
    if VersionService.isCurrentVersion(request):
        tbName = "tb_http_testcase"
        versionCondition = ""
    else:
        tbName = "tb_version_http_testcase"
        versionCondition = "and versionName='%s'" % request.session.get("version")


    execSql = "SELECT t.*,u.userName,m.moduleName,b.bussinessLineName,mu.userName modByName from %s t LEFT JOIN tb_user mu ON t.modBy = mu.loginName LEFT JOIN tb_modules m on t.moduleId = m.id LEFT JOIN tb_business_line b on t.businessLineId = b.id LEFT JOIN tb_user u ON t.addBy = u.loginName WHERE 1=1 and t.state=1 %s" % (tbName,versionCondition)
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        elif key == "caseFounder" :
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

    context = pagination(sqlStr=execSql,attrList=checkList,page=page,pageNum=commonWebConfig.testCasePageNum,request=request)

    response = render(request, "InterfaceTest/HTTPTestCase/SubPages/HTTP_testCase_list_check_page.html",context)
    return response

@single_add_page_permission
def testCaseAddPage(request,context):
    langDict = getLangTextDict(request)

    context["page"] = 1
    context["option"] = "add"
    context["addHTTPTestCase"] = "current-page"
    context["checkBusinessLine"] = dbModelListToListDict(BusinessService.getAllBusinessLine())
    context["checkModules"] = dbModelListToListDict(ModulesService.getAllModules())
    if not isRelease:
        context["env"] = "test"
    #文本
    text = {}
    text["pageTitle"] = langDict["web"]["httpTestCasePageHeadings_%s" % context["option"]]
    text["subPageTitle"] = langDict["web"]["httpTestCaseSubPageTitle_%s" % context["option"]]
    context["text"] = text

    #页面所需参数
    context["loginName"] = request.session.get("loginName")
    context.update(getConfigs(request))

    context["debugBtnCount"] = commonWebConfig.debugBtnCount

    #调试按钮
    getDebugBtnList = getDebugBtn(request)
    context.update(getDebugBtnList)
    context["title"] = "添加HTTP业务流"
    return render(request, "InterfaceTest/HTTPTestCase/HTTP_testCase.html", context)

def testCaseStepPage(request):
    context = {}
    return render(request, "InterfaceTest/HTTPTestCase/SubPages/HTTP_testcase_step_page.html", context)

def testCaseStepDetailPage(request):

    context = {}
    context.update(getConfigs(request))
    context.update(getServiceConf(request))
    context["debugBtnCount"] = commonWebConfig.debugBtnCount
    return render(request, "InterfaceTest/HTTPTestCase/SubPages/HTTP_testcase_step_detail_page.html", context)

def queryPeopleTestCase(request):
    langDict = getLangTextDict(request)
    pageNum = int(request.GET.get("num"))
    if VersionService.isCurrentVersion(request):
        attrData = HTTP_test_caseService.queryPeopleTestCase(pageNum, commonWebConfig.queryPeopleInterface,
                                                              request.session.get("loginName"))
    else:
        attrData = HTTP_test_caseService.queryVersionPeopleTestCase(pageNum, commonWebConfig.queryPeopleInterface,
                                                              request.session.get("loginName"),VersionService.getVersionName(request))
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK, langDict["web"]["httpTestCaseSuccess"], attrData).toJson())

def getTestCaseDataForId(request):
    langDict = getLangTextDict(request)
    if VersionService.isCurrentVersion(request):
        getDBData = HTTP_test_caseService.getTestCaseForIdToDict(request.GET.get("id"))
        getDBData["step"] = HTTP_test_case_stepService.getTestCaseStep(getDBData["caseId"])
    else:
        getDBData = HTTP_test_caseService.getVersionTestCaseForIdToDict(request.GET.get("id"))
        getDBData["step"] = HTTP_test_case_stepService.getVersionTestCaseStep(getDBData["caseId"],request.session.get("version"))

    return HttpResponse(ApiReturn(ApiReturn.CODE_OK,langDict["web"]["httpTestCaseSuccess"],json.dumps(getDBData)).toJson())

@single_page_permission
def operationTestCase(request,context):
    langDict = getLangTextDict(request)

    context["id"] = request.GET.get("id")
    context["option"] = request.GET.get("option")
    context["addBy"] = request.GET.get("addBy")
    context["title"] = "HTTP业务流-"+request.GET.get("id")
    context["page"] = 1
    context["addHTTPTestCase"] = "current-page"
    if not isRelease:
        context["env"] = "test"
    try:
        if VersionService.isCurrentVersion(request):
            context["dataAddBy"] = HTTP_test_caseService.getTestCaseForId(request.GET.get("id")).addBy.loginName
        else:
            context["dataAddBy"] = HTTP_test_caseService.getVersionTestCaseForId(request.GET.get("id")).addBy.loginName

    except Exception as e:
        return HttpResponse("参数id错误 %s" % e)

    #文本
    text = {}
    try:
        text["pageTitle"] = langDict["web"]["httpTestCasePageHeadings_%s" % context["option"]]
        text["subPageTitle"] = langDict["web"]["httpTestCasePageHeadings_%s" % context["option"]]
    except Exception as e:
        return HttpResponse("参数错误 %s" % e)
    context["text"] = text

    context.update(getConfigs(request))
    context.update(getServiceConf(request))
    context["debugBtnCount"] = commonWebConfig.debugBtnCount
    getDebugBtnList = getDebugBtn(request)
    context.update(getDebugBtnList)
    context["serviceJson"] = json.dumps(ServiceConfService.queryServiceConfSort(request))
    return render(request,"InterfaceTest/HTTPTestCase/HTTP_testCase.html",context)

def selectInterfaceAddStep(request):
    langDict = getLangTextDict(request)

    interfaceArr = request.POST.get("list").split(",")

    interfaceList = []
    if VersionService.isCurrentVersion(request):
        for i in range(0,len(interfaceArr)):
            interfaceList.append(dbModelToDict(HTTP_interfaceService.getInterfaceForInterfaceId(interfaceArr[i])))
    else:
        #历史版本
        for i in range(0,len(interfaceArr)):
            interfaceList.append(dbModelToDict(HTTP_interfaceService.getVersionInterfaceForInterfaceId(interfaceArr[i],request.session.get("version"))))
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK,langDict['web']['httpTestCaseSuccess'],interfaceList).toJson())

@single_data_permission(TbHttpTestcase,TbVersionHttpTestcase)
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
    testCaseData["sourceId_id"] = postLoad["sourceId_id"]
    try:
        if VersionService.isCurrentVersion(request):
            testCaseDataAdd = HTTP_test_caseService.testCaseAdd(testCaseData)
        else:
            testCaseDataAdd = HTTP_test_caseService.testVersionCaseAdd(testCaseData,VersionService.getVersionName(request))

    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_TESTCASE_ERROR, "添加用例错误", "Failed: %s" % e).toJson())
    fileDict = request.FILES
    keyCountDict = {}
    for i in range(0,len(postLoad['step'])):
        testCaseStep = {}
        thisStep = postLoad["step"][i]
        testCaseStep["stepNum"] = i+1
        testCaseStep["title"] = "步骤%s" % testCaseStep["stepNum"]
        testCaseStep["stepDesc"] = thisStep["stepDesc"]
        testCaseStep["fromInterfaceId"] = thisStep["fromInterfaceId"]
        testCaseStep["isSync"] = thisStep["isSync"]
        testCaseStep["varsPre"] = thisStep["varsPre"]
        testCaseStep["uri"] = thisStep["uri"]
        testCaseStep["useCustomUri"] = thisStep["useCustomUri"]
        testCaseStep["customUri"] = thisStep["customUri"]
        testCaseStep["stepSwitch"] = thisStep["stepSwitch"]
        testCaseStep["urlRedirect"] = thisStep["urlRedirect"]
        testCaseStep["method"] = thisStep["method"]
        testCaseStep["header"] = thisStep["header"]
        testCaseStep["url"] = thisStep["url"]
        testCaseStep["params"] = thisStep["params"]
        testCaseStep["timeout"] = (thisStep["timeout"] == "" and 20 or thisStep["timeout"])
        testCaseStep["performanceTime"] = (thisStep["performanceTime"] == "" and 1 or thisStep["performanceTime"])
        testCaseStep["varsPost"] = thisStep["varsPost"]
        testCaseStep["businessLineId_id"] = thisStep["businessLineId_id"]
        testCaseStep["moduleId_id"] = thisStep["moduleId_id"]
        testCaseStep["sourceId_id"] = thisStep["sourceId_id"]
        testCaseStep["addBy_id"] = request.session.get("loginName")

        if VersionService.isCurrentVersion(request):
            testCaseStep["caseId_id"] = testCaseDataAdd.caseId
        else:
            testCaseStep["caseId"] = testCaseDataAdd.caseId

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
                        if "realPath" in bodyContent[bodyContentIndex]["value"]:
                            continue
                        fileKey = tmpAttr['key']
                        if fileKey in keyCountDict.keys():
                            keyCountDict[fileKey] += 1
                        else:
                            keyCountDict[fileKey] = 0
                        tmpFileTempObj = fileDict.getlist(fileKey)[keyCountDict[fileKey]]
                        contentRealPath = updateFileSave(request.session.get("loginName"), tmpFileTempObj,
                                                         keyCountDict[fileKey])
                        bodyContent[bodyContentIndex]['value']['fileType'] = tmpFileTempObj.content_type
                        bodyContent[bodyContentIndex]['value']['realPath'] = contentRealPath
                testCaseStep["bodyContent"] = json.dumps(bodyContent, ensure_ascii=False)
            else:
                testCaseStep["bodyContent"] = thisStep["bodyContent"]
        try:
            if VersionService.isCurrentVersion(request):
                HTTP_test_case_stepService.testCaseStepAdd(testCaseStep)
            else:
                HTTP_test_case_stepService.testVersionCaseStepAdd(testCaseStep,VersionService.getVersionName(request))

        except Exception as e:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TESTCASE_ERROR, "添加用例错误", "Failed: %s" % e).toJson())
    if VersionService.isCurrentVersion(request):
        syncTestCaseStepFromInterfaceId(request,testCaseDataAdd.caseId)
    else:
        syncVersionTestCaseStepFromInterfaceId(testCaseDataAdd.caseId,VersionService.getVersionName(request))

    return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())

@single_data_permission(TbHttpTestcase,TbVersionHttpTestcase)
def testCaseDel(request):

    id = request.GET.get("id")
    if VersionService.isCurrentVersion(request):
        try:
            testCaseData = HTTP_test_caseService.getTestCaseForId(id)
        except Exception as e:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TESTCASE_ERROR,"参数id错误 %s" % e).toJson())

        if HTTP_test_caseService.delTestCaseForId(request,id) == 1:
            HTTP_test_case_stepService.stepDel(request,dbModelToDict(testCaseData)["caseId"])
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        else:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TESTCASE_ERROR).toJson())
    else:
        testCaseData =  HTTP_test_caseService.getVersionTestCaseForId(id)
        if HTTP_test_caseService.delVersionTestCaseForId(request,id) == 1:
            HTTP_test_case_stepService.stepVersionDel(request,dbModelToDict(testCaseData)["caseId"],VersionService.getVersionName(request))
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        else:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TESTCASE_ERROR).toJson())

@single_data_permission(TbHttpTestcase,TbVersionHttpTestcase)
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
    #     thisUser = dbModelToDict(HTTP_test_caseService.getTestCaseForId(postLoad["id"]))
    # else:
    #     thisUser = dbModelToDict(HTTP_test_caseService.getVersionTestCaseForId(postLoad["id"]))

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
    testCaseData["sourceId_id"] = postLoad["sourceId_id"]
    testCaseData["modTime"] = datetime.datetime.now()
    if VersionService.isCurrentVersion(request):
        testCaseDataSaveEdit = HTTP_test_caseService.saveEdit(request,testCaseData)
    else:
        testCaseData["versionName_id"] = VersionService.getVersionName(request)
        testCaseDataSaveEdit = HTTP_test_caseService.saveVersionEdit(request,testCaseData)

    if testCaseDataSaveEdit != 1:
        return HttpResponse(ApiReturn(ApiReturn.CODE_TESTCASE_ERROR, '保存编辑用例失败').toJson())

    fileDict = request.FILES
    keyCountDict = {}
    if VersionService.isCurrentVersion(request):
        DBstepNum = HTTP_test_case_stepService.getTestCaseAllStep(postLoad["caseId"])
    else:
        DBstepNum = HTTP_test_case_stepService.getVersionTestCaseAllStep(postLoad["caseId"],VersionService.getVersionName(request))

    if testCaseData["stepCount"] <= len(DBstepNum):
        for i in range(0,len(DBstepNum)):
            if i < testCaseData["stepCount"]:
                testCaseStep = {}
                thisStep = postLoad["step"][i]
                testCaseStep["stepNum"] = i+1
                testCaseStep["title"] = "步骤%s" % testCaseStep["stepNum"]
                testCaseStep["stepDesc"] = thisStep["stepDesc"]
                testCaseStep["fromInterfaceId"] = thisStep["fromInterfaceId"]
                testCaseStep["isSync"] = thisStep["isSync"]
                testCaseStep["varsPre"] = thisStep["varsPre"]
                testCaseStep["uri"] = thisStep["uri"]
                testCaseStep["useCustomUri"] = thisStep["useCustomUri"]
                testCaseStep["customUri"] = thisStep["customUri"]
                testCaseStep["stepSwitch"] = thisStep["stepSwitch"]
                testCaseStep["urlRedirect"] = thisStep["urlRedirect"]
                testCaseStep["method"] = thisStep["method"]
                testCaseStep["header"] = thisStep["header"]
                testCaseStep["url"] = thisStep["url"]
                testCaseStep["params"] = thisStep["params"]
                testCaseStep["timeout"] = (thisStep["timeout"] == "" and 20 or thisStep["timeout"])
                testCaseStep["performanceTime"] = (thisStep["performanceTime"] == "" and 1 or thisStep["performanceTime"])
                testCaseStep["varsPost"] = thisStep["varsPost"]
                testCaseStep["businessLineId_id"] = thisStep["businessLineId_id"]
                testCaseStep["moduleId_id"] = thisStep["moduleId_id"]
                testCaseStep["sourceId_id"] = thisStep["sourceId_id"]
                testCaseStep["state"] = 1
                testCaseStep["modTime"] = datetime.datetime.now()
                testCaseStep["modBy"] = request.session.get("loginName")
                if VersionService.isCurrentVersion(request) :
                    testCaseStep["caseId_id"] = postLoad["caseId"]
                else:
                    testCaseStep["caseId"] = postLoad["caseId"]
                    testCaseStep["versionName_id"] = VersionService.getVersionName(request)

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
                        if(type(bodyContent) == str):
                            bodyContent = json.loads(bodyContent)
                        for bodyContentIndex in range(0, len(bodyContent)):
                            tmpAttr = bodyContent[bodyContentIndex]
                            if tmpAttr['type'] == "file":
                                if "realPath" in bodyContent[bodyContentIndex]["value"]:
                                    continue
                                fileKey = tmpAttr['key']
                                if fileKey in keyCountDict.keys():
                                    keyCountDict[fileKey] += 1
                                else:
                                    keyCountDict[fileKey] = 0
                                tmpFileTempObj = fileDict.getlist(fileKey)[keyCountDict[fileKey]]
                                contentRealPath = updateFileSave(request.session.get("loginName"), tmpFileTempObj,
                                                                 keyCountDict[fileKey])
                                bodyContent[bodyContentIndex]['value']['fileType'] = tmpFileTempObj.content_type
                                bodyContent[bodyContentIndex]['value']['realPath'] = contentRealPath
                        testCaseStep["bodyContent"] = json.dumps(bodyContent, ensure_ascii=False)
                    else:
                        testCaseStep["bodyContent"] = thisStep["bodyContent"]
                else:
                    testCaseStep["bodyType"] = ""
                    testCaseStep["bodyContent"] = ""
                if VersionService.isCurrentVersion(request):
                    HTTP_test_case_stepService.updateTestCaseStep(request,DBstepNum[i]["id"],testCaseStep)
                else:
                    HTTP_test_case_stepService.updateVersionTestCaseStep(request,DBstepNum[i]["id"],testCaseStep)
            else:
                if VersionService.isCurrentVersion(request):
                    HTTP_test_case_stepService.updateCancel(DBstepNum[i]["id"])
                else:
                    HTTP_test_case_stepService.updateVersionCancel(DBstepNum[i]["id"])
    else:
        for i in range(0,testCaseData["stepCount"]):
            testCaseStep = {}
            thisStep = postLoad["step"][i]
            testCaseStep["stepNum"] = i + 1
            testCaseStep["title"] = "步骤%s" % testCaseStep["stepNum"]
            testCaseStep["stepDesc"] = thisStep["stepDesc"]
            testCaseStep["fromInterfaceId"] = thisStep["fromInterfaceId"]
            testCaseStep["isSync"] = thisStep["isSync"]
            testCaseStep["varsPre"] = thisStep["varsPre"]
            testCaseStep["uri"] = thisStep["uri"]
            testCaseStep["useCustomUri"] = thisStep["useCustomUri"]
            testCaseStep["customUri"] = thisStep["customUri"]
            testCaseStep["stepSwitch"] = thisStep["stepSwitch"]
            testCaseStep["urlRedirect"] = thisStep["urlRedirect"]
            testCaseStep["method"] = thisStep["method"]
            testCaseStep["header"] = thisStep["header"]
            testCaseStep["url"] = thisStep["url"]
            testCaseStep["params"] = thisStep["params"]
            testCaseStep["timeout"] = (thisStep["timeout"] == "" and 20 or thisStep["timeout"])
            testCaseStep["performanceTime"] = (thisStep["performanceTime"] == "" and 1 or thisStep["performanceTime"])
            testCaseStep["varsPost"] = thisStep["varsPost"]
            testCaseStep["businessLineId_id"] = thisStep["businessLineId_id"]
            testCaseStep["moduleId_id"] = thisStep["moduleId_id"]
            testCaseStep["sourceId_id"] = thisStep["sourceId_id"]
            testCaseStep["caseId_id"] = postLoad["caseId"]
            testCaseStep["modTime"] = datetime.datetime.now()
            testCaseStep["modBy"] = request.session.get("loginName")
            if VersionService.isCurrentVersion(request) == False:
                testCaseStep["versionName_id"] = VersionService.getVersionName(request)

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
                            if "realPath" in bodyContent[bodyContentIndex]["value"]:
                                continue
                            fileKey = tmpAttr['key']
                            if fileKey in keyCountDict.keys():
                                keyCountDict[fileKey] += 1
                            else:
                                keyCountDict[fileKey] = 0
                            tmpFileTempObj = fileDict.getlist(fileKey)[keyCountDict[fileKey]]
                            contentRealPath = updateFileSave(request.session.get("loginName"), tmpFileTempObj,
                                                             keyCountDict[fileKey])
                            bodyContent[bodyContentIndex]['value']['fileType'] = tmpFileTempObj.content_type
                            bodyContent[bodyContentIndex]['value']['realPath'] = contentRealPath
                    testCaseStep["bodyContent"] = json.dumps(bodyContent, ensure_ascii=False)
                else:
                    testCaseStep["bodyContent"] = thisStep["bodyContent"]
            else:
                testCaseStep["bodyType"] = ""
                testCaseStep["bodyContent"] = ""

            if i < len(DBstepNum):
                testCaseStep["state"] = 1
                if VersionService.isCurrentVersion(request):
                    HTTP_test_case_stepService.updateTestCaseStep(request,DBstepNum[i]["id"], testCaseStep)
                else:
                    HTTP_test_case_stepService.updateVersionTestCaseStep(request,DBstepNum[i]["id"], testCaseStep)
            else:
                testCaseStep["addBy_id"] = request.session.get("loginName")
                if VersionService.isCurrentVersion(request):
                    HTTP_test_case_stepService.testCaseStepAdd(testCaseStep)
                else:

                    HTTP_test_case_stepService.testVersionCaseStepAdd(testCaseStep,request.session.get("version"))
    if VersionService.isCurrentVersion(request):
        syncTestCaseStepFromInterfaceId(request,postLoad["caseId"])
    else:
        syncVersionTestCaseStepFromInterfaceId(postLoad["caseId"],VersionService.getVersionName(request))
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())

def http_testCaseSelectInterfaceCheckList(request):
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
        tbName = "tb_http_interface"
        versionCondition = ""
    else:
        tbName = "tb_version_http_interface"
        versionCondition = "and versionName='%s'" % request.session.get("version")

    execSql = "SELECT i.*,u.userName from %s i LEFT JOIN tb_user u ON i.addBy = u.loginName LEFT JOIN  tb_modules m ON i.moduleId = m.id LEFT JOIN tb_business_line b ON i.businessLineId = b.id  WHERE 1=1 and i.state=1 %s " %(tbName,versionCondition)
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        elif key == "caseFounder" :
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

    context = pagination(sqlStr=execSql,attrList=checkList,page=page,pageNum=commonWebConfig.interfaceSelectPageNum)
    response = render(request, "InterfaceTest/HTTPTestCase/SubPages/HTTP_TestCase_Select_interface_list_check_page.html",context)
    return response

def updateTestCaseLevel(request):
    userToken = request.GET.get("token","")

    if userToken == "":
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR,message="toekn为空").toJson())
    try:
        userData = TbUser.objects.get(token=userToken)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR,message="token错误，未查询到用户").toJson())

    testCaseId = request.GET.get("testCaseId","")
    if testCaseId == "":
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR,message="interfaceId为必填参数").toJson())
    try:
        testCaseData = TbHttpTestcase.objects.get(caseId=testCaseId,state=1)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR,message="InterfaceId 参数错误").toJson())

    if userData.loginName != testCaseData.addBy.loginName:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR,message="只能更新自己的接口").toJson())

    levelDict = {"高":0,"中":5,"低":9}
    levelText = request.GET.get("level","中")

    if levelText in levelDict.keys():
        level = levelDict[levelText]
    else:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR,message="level参数的值为【高】、【中】、【低】").toJson())

    testCaseData.caselevel = level
    testCaseData.save(force_update=True)
    return HttpResponse(ApiReturn().toJson())