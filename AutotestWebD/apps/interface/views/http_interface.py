from django.shortcuts import render,HttpResponse,redirect
from urllib import parse
from apps.common.config import commonWebConfig
from apps.common.func.LanguageFunc import *
from apps.config.views.http_conf import getDebugBtn
from apps.version_manage.services.common_service import VersionService
from apps.common.model.RedisDBConfig import *
from apps.common.decorator.permission_normal_funcitons import *
from apps.common.func.ValidataFunc import *
from apps.common.func.WebFunc import *

retmsg = ""

logger = logging.getLogger("django")


def http_interfaceCheck(request):
    request.session['groupLevel1'] = groupLevel1
    request.session['groupLevel2'] = groupLevel2
    request.session['isReleaseEnv'] = isRelease

    langDict = getLangTextDict(request)
    context = {}
    if not isRelease:
        context["env"] = "test"
    context["interfaceCheck"] = "current-page"
    context["userName"] = request.session.get("userName")
    context["checkBusinessLine"] = dbModelListToListDict(BusinessService.getAllBusinessLine())
    context["checkModules"] = dbModelListToListDict(ModulesService.getAllModules())
    # 文本
    text = {}
    text["pageTitle"] = langDict["web"]["httpInterfacePageHeadings_check"]
    context["text"] = text
    context["page"] = 1
    context["uri"] = UriService.getUri(request,"HTTP")
    # context["lang"] = getLangTextDict(request)
    context["title"] = "HTTP接口"
    addUserLog(request, "单接口管理->查看用例->页面展示->成功", "PASS")
    return render(request, "InterfaceTest/HTTPInterface/HTTP_interface_check.html", context)


def http_interfaceListCheck(request):
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "单接口管理->查看用例->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))

    orderBy = request.POST.get("orderBy")
    if isSqlInjectable(orderBy):
        addUserLog(request, "单接口管理->查看用例->获取数据->SQL注入检测时发现查询条件非法", "FAIL")
        return HttpResponse("<script>alert('查询条件非法');</script>")

    # 根据版本判断应该从哪个表里取数据 王吉亮添加于20180224
    if VersionService.isCurrentVersion(request):
        tbName = "tb_http_interface"
        versionCondition = ""
    else:
        tbName = "tb_version_http_interface"
        versionCondition = "and versionName='%s'" % request.session.get("version")

    execSql = "SELECT i.*,u.userName,mu.userName modByName from %s i LEFT JOIN tb_user mu ON i.modBy = mu.loginName LEFT JOIN tb_user u ON i.addBy = u.loginName LEFT JOIN  tb_modules m ON i.moduleId = m.id LEFT JOIN tb_business_line b ON i.businessLineId = b.id WHERE 1=1 and i.state=1 %s" % (
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
        elif key == "uri":
            checkList.append("%s" % checkArr[key])
            execSql += """ and i.uri= %s """
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and i.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.interFacePageNum,request=request)

    response = render(request, "InterfaceTest/HTTPInterface/SubPages/HTTP_interface_list_check_page.html", context)
    addUserLog(request, "单接口管理->查看用例->获取数据->成功", "PASS")
    return response

@single_add_page_permission
def interfaceAddPage(request,context):
    langDict = getLangTextDict(request)

    context['option'] = request.GET.get("option", "add")
    context['mockid'] = request.GET.get("mockid", 0)
    context["addHTTPInterface"] = "current-page"
    if not isRelease:
        context["env"] = "test"
    # 文本
    text = {}
    text["pageTitle"] = langDict["web"]["httpInterfacePageHeadings_%s" % context["option"]]
    text["subPageTitle"] = langDict["web"]["httpInterfaceSubPageTitle_%s" % context["option"]]
    context["text"] = text


    # 页面所需参数
    context.update(getConfigs(request))
    context.update(getServiceConf(request))
    context["debugBtnCount"] = commonWebConfig.debugBtnCount
    # 调试按钮
    getDebugBtnList = getDebugBtn(request)
    context.update(getDebugBtnList)
    addUserLog(request, "单接口管理->添加用例->页面展示->成功", "PASS")
    context["title"] = "添加HTTP接口"
    return render(request, "InterfaceTest/HTTPInterface/HTTP_interface.html", context)


def interfaceGetSyncTestCaseStep(request):
    id = request.GET.get("id")
    if VersionService.isCurrentVersion(request):
        interfaceData = dbModelToDict(HTTP_interfaceService.getInterfaceForId(id))
        syncList = syncDelTipList(interfaceData)
    else:
        interfaceData = dbModelToDict(HTTP_interfaceService.getVersionInterfaceForId(id))
        syncList = syncVersionDelTipList(interfaceData, VersionService.getVersionName(request))
    return HttpResponse(ApiReturn(body=syncList).toJson())


@single_data_permission(TbHttpInterface,TbVersionHttpInterface)
def interfaceDel(request):
    id = request.GET.get("id")
    try:
        if VersionService.isCurrentVersion(request):
            interfaceData = HTTP_interfaceService.getInterfaceForId(request.GET.get("id"))

        else:
            interfaceData = HTTP_interfaceService.getVersionInterfaceForId(request.GET.get("id"))

    except Exception as e:
        print(traceback.format_exc())
        return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_ERROR, "参数id错误 %s" % e).toJson())

    if VersionService.isCurrentVersion(request):
        syncDel(request,dbModelToDict(interfaceData))
        if HTTP_interfaceService.delInterfaceForId(request,id) == 1:
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        else:
            return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_ERROR).toJson())
    else:
        syncVersionDel(request,dbModelToDict(interfaceData), VersionService.getVersionName(request))
        if HTTP_interfaceService.delVersionInterfaceForId(request,id) == 1:
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        else:
            return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_ERROR).toJson())


def operationInterfaceByInterfaceId(request):
    try:
        interfaceId = request.GET.get("interfaceId")
        interObj = HTTP_interfaceService.getInterfaceByInterfaceId(interfaceId)
        return redirect("/interfaceTest/HTTP_operationInterface?id=%s&option=%s" % (interObj.id,request.GET.get("option")))
    except:
        return render(request, "permission/page_404.html")

@single_page_permission
def operationInterface(request,context):
    langDict = getLangTextDict(request)
    context["id"] = request.GET.get("id",-1)
    context["option"] = request.GET.get("option")
    context["addBy"] = request.GET.get("addBy")
    try:
        if int(context["id"]) <= 0:
            interfaceId = request.GET.get("interfaceId")
            interObj = HTTP_interfaceService.getInterfaceByInterfaceId(interfaceId)
            return redirect("/interfaceTest/HTTP_operationInterface?id=%s&option=%s" % (interObj.id,context["option"]))
    except:
        return render(request, "permission/page_404.html")


    context["addHTTPInterface"] = "current-page"

    if not isRelease:
        context["env"] = "test"
    try:
        if VersionService.isCurrentVersion(request):
            context["dataAddBy"] = HTTP_interfaceService.getInterfaceForId(request.GET.get("id")).addBy.loginName
        else:
            context["dataAddBy"] = HTTP_interfaceService.getVersionInterfaceForId(request.GET.get("id")).addBy.loginName

    except Exception as e:
        return render(request, "permission/page_404.html")

    # 文本
    text = {}
    try:
        text["pageTitle"] = langDict["web"]["httpInterfacePageHeadings_%s" % context["option"]]
        text["subPageTitle"] = langDict["web"]["httpInterfaceSubPageTitle_%s" % context["option"]]
    except Exception as e:
        return HttpResponse("参数错误 %s" % e)
    context["text"] = text

    context.update(getConfigs(request))
    context.update(getServiceConf(request))
    context["debugBtnCount"] = commonWebConfig.debugBtnCount
    getDebugBtnList = getDebugBtn(request)
    context.update(getDebugBtnList)
    context["serviceJson"] = json.dumps(ServiceConfService.queryServiceConfSort(request))
    context["title"] = "HTTP接口-" + request.GET.get("id")

    return render(request, "InterfaceTest/HTTPInterface/HTTP_interface.html", context)


def getInterfaceDataForId(request):
    langDict = getLangTextDict(request)
    serviceConf = ServiceConfService.queryServiceConfSort(request)

    # 根据版本判断应该从哪个表里取数据 王吉亮添加于20180224
    if VersionService.isCurrentVersion(request):
        getDBData = HTTP_interfaceService.getInterfaceForIdToDict(request.GET.get("id"))
    else:
        getDBData = HTTP_interfaceService.getVersionInterfaceForIdToDict(request.GET.get("id"),
                                                                         request.session.get("version"))
    return HttpResponse(
        ApiReturn(ApiReturn.CODE_OK, langDict["web"]["httpInterfaceSuccess"], json.dumps(getDBData)).toJson())

@single_data_permission(TbHttpInterface,TbVersionHttpInterface)
def interfaceAdd(request):
    if VersionService.isCurrentVersion(request):
        # 当前版本使用历史代码，不更新。
        if request.method != 'POST':
            return HttpResponse(ApiReturn(ApiReturn.CODE_METHOD_ERROR, "请求方式错误", "").toJson())
        data = json.loads(request.POST.get("interfaceData"))
        if data["method"] != "GET" and data["method"] != "HEAD":
            file = request.FILES
            bodyContent = data["bodyContent"]
            bodyType = data["bodyType"]
            if bodyType == "binary":
                if "realPath" in bodyContent:
                    data["bodyContent"] = json.dumps(bodyContent, ensure_ascii=False)
                else:
                    if not file.get("file"):
                        return HttpResponse(ApiReturn(ApiReturn.CODE_NOT_FILE_EXCEPITON, "请选择文件").toJson())
                    thisFile = file.get("file")
                    contentRealPath = updateFileSave(request.session.get("loginName"), thisFile, "0")
                    bodyContent["realPath"] = contentRealPath
                    bodyContent["fileType"] = thisFile.content_type
                    data["bodyContent"] = json.dumps(bodyContent, ensure_ascii=False)
            elif bodyType == "form-data":
                fileDict = request.FILES
                keyCountDict = {}
                for i in range(0, len(bodyContent)):
                    tmpAttr = bodyContent[i]
                    if tmpAttr['type'] == "file":
                        if "realPath" in bodyContent[i]["value"]:
                            continue
                        fileKey = tmpAttr['key']
                        if fileKey in keyCountDict.keys():
                            keyCountDict[fileKey] += 1
                        else:
                            keyCountDict[fileKey] = 0
                        keyRealFileList = fileDict.getlist(fileKey)
                        lenRealFileList = len(keyRealFileList)
                        currentFileIndex = keyCountDict[fileKey]
                        if currentFileIndex >= lenRealFileList:
                            return HttpResponse(ApiReturn(ApiReturn.CODE_NOT_FILE_EXCEPITON, "请选择文件").toJson())
                        tmpFileTempObj = keyRealFileList[currentFileIndex]
                        contentRealPath = updateFileSave(request.session.get("loginName"), tmpFileTempObj,
                                                         keyCountDict[fileKey])
                        bodyContent[i]['value']['fileType'] = tmpFileTempObj.content_type
                        bodyContent[i]['value']['realPath'] = contentRealPath
                data["bodyContent"] = json.dumps(bodyContent, ensure_ascii=False)
        try:
            retB, retS = verifyPythonMode(data["varsPre"])
            if retB == False:
                return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_DEBUG_ADD_EXCEPITON,"",
                                              "准备中出现不允许的输入：%s" % retS).toJson())
            retB, retS = verifyPythonMode(data["varsPost"])
            if retB == False:
                return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_DEBUG_ADD_EXCEPITON,"",
                                              "断言恢复中出现不允许的输入：%s" % retS).toJson())

            HTTP_interfaceService.addInterface(data, request.session.get("loginName"))
        except Exception as e:
            logger.error(traceback.format_exc())
            return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_ERROR, "添加接口错误", "Failed: %s" % e).toJson())
        return HttpResponse(ApiReturn(ApiReturn.CODE_OK, "添加成功", "").toJson())
    else:
        # 添加接口到历史版本
        if request.method != 'POST':
            return HttpResponse(ApiReturn(ApiReturn.CODE_METHOD_ERROR, "请求方式错误", "").toJson())
        data = json.loads(request.POST.get("interfaceData"))
        if data["method"] != "GET" and data["method"] != "HEAD":
            file = request.FILES
            bodyContent = data["bodyContent"]
            bodyType = data["bodyType"]
            if bodyType == "binary":
                if "realPath" in bodyContent:
                    data["bodyContent"] = json.dumps(bodyContent, ensure_ascii=False)
                else:
                    if not file.get("file"):
                        return HttpResponse(ApiReturn(ApiReturn.CODE_NOT_FILE_EXCEPITON, "请选择文件").toJson())
                    thisFile = file.get("file")
                    contentRealPath = updateFileSave(request.session.get("loginName"), thisFile, "0")
                    bodyContent["realPath"] = contentRealPath
                    bodyContent["fileType"] = thisFile.content_type
                    data["bodyContent"] = json.dumps(bodyContent, ensure_ascii=False)
            elif bodyType == "form-data":
                fileDict = request.FILES
                keyCountDict = {}
                for i in range(0, len(bodyContent)):
                    tmpAttr = bodyContent[i]
                    if tmpAttr['type'] == "file":
                        if "realPath" in bodyContent[i]["value"]:
                            continue
                        fileKey = tmpAttr['key']
                        if fileKey in keyCountDict.keys():
                            keyCountDict[fileKey] += 1
                        else:
                            keyCountDict[fileKey] = 0
                        keyRealFileList = fileDict.getlist(fileKey)
                        lenRealFileList = len(keyRealFileList)
                        currentFileIndex = keyCountDict[fileKey]
                        if currentFileIndex >= lenRealFileList:
                            return HttpResponse(ApiReturn(ApiReturn.CODE_NOT_FILE_EXCEPITON, "请选择文件").toJson())
                        tmpFileTempObj = keyRealFileList[currentFileIndex]
                        contentRealPath = updateFileSave(request.session.get("loginName"), tmpFileTempObj,
                                                         keyCountDict[fileKey])
                        bodyContent[i]['value']['fileType'] = tmpFileTempObj.content_type
                        bodyContent[i]['value']['realPath'] = contentRealPath
                data["bodyContent"] = json.dumps(bodyContent, ensure_ascii=False)

        try:
            retB, retS = verifyPythonMode(data["varsPre"])
            if retB == False:
                return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_DEBUG_ADD_EXCEPITON,"",
                                              "准备中出现不允许的输入：%s" % retS).toJson())
            retB, retS = verifyPythonMode(data["varsPost"])
            if retB == False:
                return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_DEBUG_ADD_EXCEPITON,"",
                                              "断言恢复中出现不允许的输入：%s" % retS).toJson())
            HTTP_interfaceService.addVersionInterface(data, request.session.get("loginName"),
                                                      VersionService.getVersionName(request))
        except Exception as e:
            logger.error(traceback.format_exc())
            return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_ERROR, "添加接口错误", "Failed: %s" % e).toJson())
        return HttpResponse(ApiReturn(ApiReturn.CODE_OK, "添加成功", "").toJson())

@single_data_permission(TbHttpInterface,TbVersionHttpInterface)
def interfaceSaveEdit(request):
    if VersionService.isCurrentVersion(request):
        postLoad = json.loads(request.POST.get("interfaceData"))
        postLoad["modTime"] = datetime.datetime.now()
        postLoad["modBy"] = request.session.get("loginName")
        if postLoad["method"] != "GET" and postLoad["method"] != "HEAD":
            file = request.FILES
            bodyContent = postLoad["bodyContent"]
            bodyType = postLoad["bodyType"]
            if bodyType == "binary":
                if "realPath" in bodyContent:
                    postLoad["bodyContent"] = json.dumps(bodyContent, ensure_ascii=False)
                else:
                    if not file.get("file"):
                        pass
                    thisFile = file.get("file")
                    contentRealPath = updateFileSave(request.session.get("loginName"), thisFile, "0")
                    bodyContent["realPath"] = contentRealPath
                    bodyContent["fileType"] = thisFile.content_type
                    postLoad["bodyContent"] = json.dumps(bodyContent, ensure_ascii=False)
            elif bodyType == "form-data":
                fileDict = request.FILES
                keyCountDict = {}
                for i in range(0, len(bodyContent)):
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
                        contentRealPath = updateFileSave(request.session.get("loginName"), tmpFileTempObj,
                                                         keyCountDict[fileKey])
                        bodyContent[i]['value']['fileType'] = tmpFileTempObj.content_type
                        bodyContent[i]['value']['realPath'] = contentRealPath
                postLoad["bodyContent"] = json.dumps(bodyContent, ensure_ascii=False)
        try:
            retB, retS = verifyPythonMode(postLoad["varsPre"])
            if retB == False:
                return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_DEBUG_ADD_EXCEPITON,"准备中出现不允许的输入：%s" % retS,
                                              "准备中出现不允许的输入：%s" % retS).toJson())
            retB, retS = verifyPythonMode(postLoad["varsPost"])
            if retB == False:
                return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_DEBUG_ADD_EXCEPITON,"断言恢复中出现不允许的输入：%s" % retS,
                                              "断言恢复中出现不允许的输入：%s" % retS).toJson())
            HTTP_interfaceService.interfaceSaveEdit(request,postLoad)
            syncInterfaceToTestcaseStep(request,postLoad)
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        except Exception as e:
            logger.error(traceback.format_exc())
            return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_ERROR, '保存编辑失败！%s' % e).toJson())
    else:
        # 历史版本编辑接口啊
        postLoad = json.loads(request.POST.get("interfaceData"))
        postLoad["modTime"] = datetime.datetime.now()
        postLoad["modBy"] = request.session.get("loginName")
        if postLoad["method"] != "GET" and postLoad["method"] != "HEAD":
            file = request.FILES
            bodyContent = postLoad["bodyContent"]
            bodyType = postLoad["bodyType"]
            if bodyType == "binary":
                if "realPath" in bodyContent:
                    postLoad["bodyContent"] = json.dumps(bodyContent, ensure_ascii=False)
                else:
                    if not file.get("file"):
                        pass
                    thisFile = file.get("file")
                    contentRealPath = updateFileSave(request.session.get("loginName"), thisFile, "0")
                    bodyContent["realPath"] = contentRealPath
                    bodyContent["fileType"] = thisFile.content_type
                    postLoad["bodyContent"] = json.dumps(bodyContent, ensure_ascii=False)
            elif bodyType == "form-data":
                fileDict = request.FILES
                keyCountDict = {}
                for i in range(0, len(bodyContent)):
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
                        contentRealPath = updateFileSave(request.session.get("loginName"), tmpFileTempObj,
                                                         keyCountDict[fileKey])
                        bodyContent[i]['value']['fileType'] = tmpFileTempObj.content_type
                        bodyContent[i]['value']['realPath'] = contentRealPath
                postLoad["bodyContent"] = json.dumps(bodyContent, ensure_ascii=False)
        try:
            postLoad['versionName_id'] = VersionService.getVersionName(request)

            retB, retS = verifyPythonMode(postLoad["varsPre"])
            if retB == False:
                return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_DEBUG_ADD_EXCEPITON, "准备中出现不允许的输入：%s" % retS,
                                              "准备中出现不允许的输入：%s" % retS).toJson())
            retB, retS = verifyPythonMode(postLoad["varsPost"])
            if retB == False:
                return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_DEBUG_ADD_EXCEPITON, "断言恢复中出现不允许的输入：%s" % retS,
                                              "断言恢复中出现不允许的输入：%s" % retS).toJson())

            HTTP_interfaceService.interfaceVersionSaveEdit(postLoad)
            syncVersionInterfaceToTestcaseStep(request,postLoad, VersionService.getVersionName(request))
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        except Exception as e:
            logger.error(traceback.format_exc())
            return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_ERROR, '保存编辑失败！%s' % e).toJson())


def queryPeopleInterface(request):
    langDict = getLangTextDict(request)
    pageNum = int(request.GET.get("num"))
    attrData = HTTP_interfaceService.queryPeopleInterface(pageNum, commonWebConfig.queryPeopleInterface,
                                                          request.session.get("loginName"))
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK, langDict["web"]["httpInterfaceSuccess"], attrData).toJson())

def queryPeopleInterfaceByTableName(request):
    langDict = getLangTextDict(request)
    pageNum = int(request.GET.get("num"))
    tbName = request.GET.get("tbName","")
    attrData = queryPeopleCountByTablename(pageNum, commonWebConfig.queryPeopleInterface,request.session.get("loginName"),tbName)
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK, langDict["web"]["httpInterfaceSuccess"], attrData).toJson())


def updateInterfaceLevel(request):
    userToken = request.GET.get("token", "")

    if userToken == "":
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="toekn为空").toJson())
    try:
        userData = TbUser.objects.get(token=userToken)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="token错误，未查询到用户").toJson())

    interfaceId = request.GET.get("interfaceId", "")
    if interfaceId == "":
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="interfaceId为必填参数").toJson())
    try:
        interfaceData = TbHttpInterface.objects.get(interfaceId=interfaceId, state=1)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="InterfaceId 参数错误").toJson())

    if userData.loginName != interfaceData.addBy.loginName:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="只能更新自己的接口").toJson())

    levelDict = {"高": 0, "中": 5, "低": 9}
    levelText = request.GET.get("level", "中")

    if levelText in levelDict.keys():
        level = levelDict[levelText]
    else:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="level参数的值为【高】、【中】、【低】").toJson())

    interfaceData.caselevel = level
    interfaceData.save(force_update=True)
    return HttpResponse(ApiReturn().toJson())


# def interfaceGetAutoFillData(request):
#     interfaceAutoFillKey = request.GET.get("interfaceAutoFillKey", None)
#     if interfaceAutoFillKey:
#         try:
#             sendParams = RedisCache().get_data(interfaceAutoFillKey)
#             RedisCache().del_data(interfaceAutoFillKey)
#         except Exception as e:
#             return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR, message="读取数据错误，请联系管理员").toJson())
#         return HttpResponse(ApiReturn(body=sendParams).toJson())
#     return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR, message="没有找到KEY值，请联系管理员").toJson())


# def getUrikeyByUrihost(request):
#     host = request.GET.get("host", "")
#     if host == "":
#         return HttpResponse("")
#     try:
#         confHttp = TbConfigHttp.objects.filter(httpConf__contains=host)
#         if confHttp:
#             confHttp = confHttp[0]
#             confDict = Config.getConfDictByString(confHttp.httpConf)
#             for protocolKey, protocolValue in confDict.items():
#                 for uriKey, uriValue in protocolValue.items():
#                     if uriValue == host:
#                         return HttpResponse(uriKey)
#             return HttpResponse("")
#         else:
#             return HttpResponse("")
#     except:
#         logging.error(traceback.format_exc())
#         return HttpResponse("")


def interfaceGetAutoFillData(request):
    interfaceAutoFillKey = request.GET.get("interfaceAutoFillKey",None)
    if interfaceAutoFillKey:
        try:
            sendParams = RedisCache().get_data(interfaceAutoFillKey)
            RedisCache().del_data(interfaceAutoFillKey)
        except Exception as e:
            return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR,message="读取数据错误，请联系管理员").toJson())
        return HttpResponse(ApiReturn(body=sendParams).toJson())
    return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR,message="没有找到KEY值，请联系管理员").toJson())

def getUrikeyByUrihost(request):
    host = request.GET.get("host", "")
    app = request.GET.get("app", "")
    protocol = request.GET.get("protocol", "DUBBO")
    if host == "" and app == "":
        return HttpResponse("")
    if host != "":
        #通过host从 env uri 中查找
        try:
            envUriConf = TbEnvUriConf.objects.filter(requestAddr=host)
            if envUriConf:
                retUri = envUriConf[0].uriKey
                return HttpResponse(retUri)
            else:
                return HttpResponse("")
        except:
            logging.error(traceback.format_exc())
            return HttpResponse("")
    if app != "":
        #通过域名在服务配置的描述中模糊搜索
        try:
            envUriConf = TbConfigUri.objects.filter(uriDesc__icontains="[%s]" % app,protocol=protocol)
            if envUriConf:
                retUri = envUriConf[0].uriKey
                return HttpResponse(retUri)
            else:
                return HttpResponse("")
        except:
            logging.error(traceback.format_exc())
            return HttpResponse("")



def importPostmanPage(request):
    context = {}
    context.update(getConfigs(request))
    return render(request,"InterfaceTest/HTTPInterface/importPostmanPage.html",context)

def savePostmanDataToHttpInterface(request):
    dataList = json.loads(request.body.decode("utf8"))
    try:
        for tmpData in dataList:
            if "domain" in tmpData.keys():
                tmpData.pop("domain")
            if "lineno" in tmpData.keys():
                tmpData.pop("lineno")

            if "response" in tmpData.keys():
                response = tmpData['response']
                tmpData.pop("response")
                if response != "":
                    tmpData['varsPost'] += "\nASSERT(%s)" % response

            tmpData["businessLineId_id"] = int(tmpData['businessLineId_id'].strip())
            tmpData["moduleId_id"] = int(tmpData['moduleId_id'].strip())

            tmpData['varsPost'] = tmpData['varsPost'].strip()
            tmpData['varsPre'] = tmpData['varsPre'].strip()

            tmpData['title'] = "POSTMAN导入数据自动生成标题" if tmpData['title'].strip() == "" else tmpData['title'].strip()
            tmpData['casedesc'] = "POSTMAN导入数据自动生成描述" if tmpData['casedesc'].strip() == "" else tmpData['casedesc'].strip()
            tmpData['url'] = "/" if tmpData['url'].strip() == "" else tmpData['url'].strip()
            HTTP_interfaceService.addInterface(tmpData,request.session.get("loginName"))

        addUserLog(request,"导入postman数据","PASS",isToDb = True)
        return HttpResponse(ApiReturn(ApiReturn.CODE_OK,"OK").toJson())
    except Exception as e:
        print(traceback.format_exc())
        return HttpResponse(ApiReturn(ApiReturn.CODE_EXCEPTION,str(traceback.format_exc())).toJson())

def importLogPage(request):
    context = {}
    context.update(getConfigs(request))
    context["host"] = request.get_host()
    return render(request,"InterfaceTest/HTTPInterface/importLogHttpData.html",context)

@catch_exception_request
def saveLogDataToHttpInterfaces(request):
    interfaceCaseList = json.loads(request.body.decode("utf8"))
    importResBl = True
    failMsg = ""
    for tmpCase in interfaceCaseList:
        retInfo = HTTP_interfaceService.addInterface(tmpCase,request.session.get("loginName"),"日志导入数据")
        if isinstance(retInfo,str):
            importResBl = False
            failMsg += "(%s)%s/%s导入失败，原因：%s\n" % (tmpCase['method'],tmpCase['uri'],tmpCase['url'],retInfo)

    if importResBl:
        return HttpResponse(ApiReturn(ApiReturn.CODE_OK,message="ok").toJson())
    else:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR,message=failMsg).toJson())
