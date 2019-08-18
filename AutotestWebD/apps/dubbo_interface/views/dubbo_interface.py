from django.shortcuts import render, HttpResponse,redirect
from urllib import parse
from apps.common.config import commonWebConfig
from apps.common.func.LanguageFunc import *
from apps.version_manage.services.common_service import VersionService
from apps.dubbo_common.services.ConfigServiceForDubbo import ConfigServiceForDubbo
from apps.dubbo_interface.services.dubbo_interface_service import DubboInterfaceService
from apps.common.decorator.permission_normal_funcitons import *
from apps.common.func.WebFunc import *
from all_models_for_dubbo.models import *

retmsg = ""

logger = logging.getLogger("django")


def dubbo_interfaceCheck(request):
    request.session['groupLevel1'] = groupLevel1
    request.session['groupLevel2'] = groupLevel2
    request.session['isReleaseEnv'] = isRelease

    langDict = getLangTextDict(request)
    context = {}
    if not isRelease:
        context["env"] = "test"
    context["dubbo_interfaceCheck"] = "current-page"
    context["userName"] = request.session.get("userName")
    context["checkBusinessLine"] = dbModelListToListDict(BusinessService.getAllBusinessLine())
    context["checkModules"] = dbModelListToListDict(ModulesService.getAllModules())
    # 文本
    text = {}
    text["pageTitle"] = langDict["dubbo"]["interfacePageHeadings_check"]
    context["text"] = text
    context["page"] = 1
    context["uri"] = UriService.getUri(request,"DUBBO")
    # context["lang"] = getLangTextDict(request)
    context["title"] = "DUBBO接口"
    addUserLog(request, "DUBBO单接口管理->查看用例->页面展示->成功", "PASS")
    return render(request, "dubbo/interface/interface_check.html", context)


def dubbo_interfaceListCheck(request):
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "DUBBO单接口管理->查看用例->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))

    orderBy = request.POST.get("orderBy")
    if isSqlInjectable(orderBy):
        addUserLog(request, "DUBBO单接口管理->查看用例->获取数据->SQL注入检测时发现查询条件非法", "FAIL")
        return HttpResponse("<script>alert('查询条件非法');</script>")

    # 根据版本判断应该从哪个表里取数据 王吉亮添加于20180224
    if VersionService.isCurrentVersion(request):
        tbName = "tb2_dubbo_interface"
        versionCondition = ""
    else:
        tbName = "tb2_version_dubbo_interface" #暂时未做多版本处理
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
        elif key == "dubboSystem":
            checkList.append("%s" % checkArr[key])
            execSql += """ and i.dubboSystem= %s """
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and i.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.interFacePageNum,request=request)
    response = render(request, "dubbo/interface/SubPages/interface_list_check_page.html", context)
    addUserLog(request, "DUBBO单接口管理->查看用例->获取数据->成功", "PASS")
    return response

@single_add_page_permission
def interfaceAddPage(request,context):
    langDict = getLangTextDict(request)
    context["option"] = "add"
    context["dubbo_addHTTPInterface"] = "current-page"
    if not isRelease:
        context["env"] = "test"
    # 文本
    text = {}
    text["pageTitle"] = langDict["dubbo"]["interfacePageHeadings_%s" % context["option"]]
    text["subPageTitle"] = langDict["dubbo"]["interfaceSubPageTitle_%s" % context["option"]]
    context["text"] = text

    # 页面所需参数
    ##httoConfList
    #dubugInfos
    envConfList = DubboInterfaceService.queryDubboConfSort(request)
    context["envConfList"] = envConfList
    ###################################################
    context.update(ConfigServiceForDubbo.getConfigs(request))
    context.update(getServiceConf(request))
    context["debugBtnCount"] = commonWebConfig.debugBtnCount
    # 调试按钮
    getDebugBtnList = ConfigServiceForDubbo.getDebugBtn(request)
    context.update(getDebugBtnList)
    addUserLog(request, "DUBBO单接口管理->添加用例->页面展示->成功", "PASS")
    context["title"] = "添加DUBBO接口"
    return render(request, "dubbo/interface/interfaceAddPage.html", context)

@single_data_permission(Tb2DubboInterface,Tb2DubboInterface)
def interfaceAdd(request):
    if VersionService.isCurrentVersion(request):
        # 当前版本使用历史代码，不更新。
        if request.method != 'POST':
            return HttpResponse(ApiReturn(ApiReturn.CODE_METHOD_ERROR, "请求方式错误", "").toJson())
        data = json.loads(request.POST.get("interfaceData"))
        try:
            retData = DubboInterfaceService.addInterface(data,request.session.get("loginName"))
            if isinstance(retData,str):
                return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, retData, "").toJson())

        except Exception as e:
            logger.error(traceback.format_exc())
            return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_ERROR, "添加接口错误", "Failed: %s" % e).toJson())

        return HttpResponse(ApiReturn(ApiReturn.CODE_OK, "添加成功", "").toJson())
    else:
        pass

def operationInterfaceByInterfaceId(request):
    try:
        interfaceId = request.GET.get("interfaceId")
        interObj = DubboInterfaceService.getInterfaceByInterfaceId(interfaceId)
        return redirect("/dubbo/operationInterface?id=%s&option=%s" % (interObj.id,request.GET.get("option")))
    except:
        return render(request, "permission/page_404.html")

@single_page_permission
def operationInterface(request,context):
    langDict = getLangTextDict(request)
    context["id"] = request.GET.get("id",-1)
    context["option"] = request.GET.get("option")
    try:
        if int(context["id"]) <= 0:
            interfaceId = request.GET.get("interfaceId")
            interObj = DubboInterfaceService.getInterfaceByInterfaceId(interfaceId)
            return redirect("/dubbo/operationInterface?id=%s&option=%s" % (interObj.id,context["option"]))
    except:
        return render(request, "permission/page_404.html")

    context["addHTTPInterface"] = "current-page"

    if not isRelease:
        context["env"] = "test"
    try:
        if VersionService.isCurrentVersion(request):
            context["addBy"] = DubboInterfaceService.getInterfaceById(request.GET.get("id")).addBy.loginName
        else:
            context["addBy"] = DubboInterfaceService.getInterfaceById(request.GET.get("id")).addBy.loginName

    except Exception as e:
        return HttpResponse("参数id错误 %s" % e)
    ####httoConfList
    ##dubugInfos

    envConfList = DubboInterfaceService.queryDubboConfSort(request)
    context["envConfList"] = envConfList
    ###################################################
    # if context["option"] == 'edit' and request.session.get("loginName") != context["dataAddBy"]:
    #     return HttpResponse("只能修改自己创建的接口")
    # 文本
    text = {}
    try:
        text["pageTitle"] = langDict["dubbo"]["interfacePageHeadings_%s" % context["option"]]
        text["subPageTitle"] = langDict["dubbo"]["interfaceSubPageTitle_%s" % context["option"]]
    except Exception as e:
        return HttpResponse("参数错误 %s" % e)
    context["text"] = text

    # 页面所需参数
    context.update(ConfigServiceForDubbo.getConfigs(request))
    context.update(getServiceConf(request))
    context["debugBtnCount"] = commonWebConfig.debugBtnCount
    # 调试按钮
    getDebugBtnList = ConfigServiceForDubbo.getDebugBtn(request)
    context.update(getDebugBtnList)
    addUserLog(request, "DUBBO单接口管理->%s用例->页面展示->成功" % context["option"], "PASS")
    context["serviceJson"] = json.dumps(ServiceConfService.queryServiceConfSort(request))
    context["title"] = "DUBBO接口-" + request.GET.get("id")
    return render(request, "dubbo/interface/interfaceAddPage.html", context)

def getInterfaceDataById(request):
    langDict = getLangTextDict(request)
    serviceConf = ServiceConfService.queryServiceConfSort(request)

    # 根据版本判断应该从哪个表里取数据 王吉亮添加于20180224
    if VersionService.isCurrentVersion(request):
        getDBData = DubboInterfaceService.getInterfaceByIdToDict(request.GET.get("id"))
    else:
        getDBData = DubboInterfaceService.getInterfaceByIdToDict(request.GET.get("id"))

    varspre = getDBData["varsPre"]
    return HttpResponse(
        ApiReturn(ApiReturn.CODE_OK, langDict["web"]["httpInterfaceSuccess"], json.dumps(getDBData)).toJson())

@single_data_permission(Tb2DubboInterface,Tb2DubboInterface)
def interfaceSaveEdit(request):
    if VersionService.isCurrentVersion(request):
        postLoad = json.loads(request.POST.get("interfaceData"))
        postLoad["modTime"] = datetime.datetime.now()
        postLoad["modBy"] = request.session.get("loginName")
        try:
            retS = DubboInterfaceService.interfaceSaveEdit(postLoad)
            if isinstance(retS,str):
                return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, retS, "").toJson())

            DubboInterfaceService.syncInterfaceToTestcaseStep(postLoad)
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        except Exception as e:
            logger.error(traceback.format_exc())
            return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_ERROR, '保存编辑失败！%s' % e).toJson())
    else:
        pass

@single_data_permission(Tb2DubboInterface,Tb2DubboInterface)
def interfaceDel(request):
    id = request.GET.get("id")
    try:
        if VersionService.isCurrentVersion(request):
            interfaceData = DubboInterfaceService.getInterfaceById(request.GET.get("id"))
            # syncDel(dbModelToDict(interfaceData)) #TODO 实现dubbo用例的时候要做此部分
        else:
            #TODO 多版本未实现
            interfaceData = HTTP_interfaceService.getVersionInterfaceForId(request.GET.get("id"))
            syncVersionDel(dbModelToDict(interfaceData), VersionService.getVersionName(request))
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_ERROR, "参数id错误 %s" % e).toJson())
    # if request.session.get("loginName") != interfaceData.addBy.loginName:
    #     return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_ERROR, "只能删除自己创建的接口").toJson())

    #

    if VersionService.isCurrentVersion(request):
        if DubboInterfaceService.delInterfaceById(id) == 1:
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        else:
            return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_ERROR).toJson())
    else:
        if HTTP_interfaceService.delVersionInterfaceForId(id) == 1:
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        else:
            return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_ERROR).toJson())

def queryPeopleInterface(request):
    langDict = getLangTextDict(request)
    pageNum = int(request.GET.get("num"))
    attrData = ConfigServiceForDubbo.queryPeopleInterface(pageNum, commonWebConfig.queryPeopleInterface,
                                                          request.session.get("loginName"))

    return HttpResponse(ApiReturn(ApiReturn.CODE_OK, langDict["web"]["httpInterfaceSuccess"], attrData).toJson())

def getDubboServices(request):
    systemKey = request.GET.get("system")
    envKey = request.GET.get("env")
    allServiceList,allServiceDict = DubboInterfaceService.getAllServices(envKey,systemKey)
    serviceInfo = {}
    serviceInfo['serviceList'] = allServiceList
    serviceInfo['serviceDict'] = allServiceDict
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK, "成功！", serviceInfo).toJson())

def getDubboMethodsInService(request):
    systemKey = request.GET.get("system")
    envKey = request.GET.get("env")
    serviceKey = request.GET.get("service")
    allMethods = DubboInterfaceService.getAllMethods(envKey,systemKey,serviceKey)
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK, "成功！", allMethods).toJson())

def interfaceQuickDebugPage(request):
    langDict = getLangTextDict(request)
    context = {}
    context["option"] = "add"
    context["dubbo_quickDebug"] = "current-page"
    if not isRelease:
        context["env"] = "test"
    # 文本
    text = {}
    text["pageTitle"] = "DUBBO快速调试"
    text["subPageTitle"] = "DUBBO调试小工具"
    context["text"] = text
    envConfList = DubboInterfaceService.queryDubboConfSort(request)
    context["envConfList"] = envConfList
    ###################################################
    context.update(ConfigServiceForDubbo.getConfigs(request))
    context.update(getServiceConf(request))
    # 调试按钮
    getDebugBtnList = ConfigServiceForDubbo.getDebugBtn(request)
    context.update(getDebugBtnList)
    addUserLog(request, "DUBBO单接口管理->添加用例->页面展示->成功", "PASS")
    return render(request, "dubbo/interface/interfaceQuickDebugPage.html", context)

def dubboGetRequestAddr(request):
    systemKey = request.GET.get("system")
    envKey = request.GET.get("env")
    host,port = DubboInterfaceService.getDubboHostAndPort(envKey, systemKey)
    if host == "" or port == 0:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, "没有配置ip port", "").toJson())
    else:
        return HttpResponse(ApiReturn(ApiReturn.CODE_OK, "成功！", host+":"+port).toJson())

def getDubboServicesByAddr(request):
    host = request.GET.get("host")
    port = request.GET.get("port")
    allServiceList,allServiceDict = DubboInterfaceService.getServiceListAndDict(host,int(port))
    serviceInfo = {}
    if "TELNET_ERROR: Telnet请求时发生网络问题或者接口错误，请确认。" in allServiceList:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, "TELNET_ERROR: Telnet请求时发生网络问题或者接口错误，请确认请求地址！", "").toJson())
    serviceInfo['serviceList'] = allServiceList
    serviceInfo['serviceDict'] = allServiceDict
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK, "成功！", serviceInfo).toJson())

def getParamByServiceMethod(request):
    service = request.GET.get("service")
    method = request.GET.get("method")
    paramIndex = request.GET.get("paramIndex")
    paramStr = DubboInterfaceService.getRecentParam(service,method,int(paramIndex))
    bodyDict = {"param": paramStr,"encoding":""}
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK, "成功！", bodyDict).toJson())

def quickDebug(request):
    addr = request.POST.get("addr")
    addrList = addr.split(":")
    service = request.POST.get("service")
    method = request.POST.get("method")
    params = request.POST.get("params")
    encoding = request.POST.get("encoding","gb18030")
    print("1111 %s" % encoding)
    cmd = "invoke %s.%s(%s)" % (service,method,params)
    retMsg = DubboInterfaceService.do_telnet(addrList[0],addrList[1],cmd,encoding=encoding)
    retMsg = retMsg.replace("\r\ndubbo>","")
    bodyDict = {}
    if "elapsed:" in retMsg:
        msgList = retMsg.split("elapsed:")
        bodyDict['actualMsg'] = msgList[0]
        bodyDict['taketime'] = int(msgList[1].split("ms")[0].strip())
    else:
        bodyDict['actualMsg'] = retMsg
        bodyDict['taketime'] = 0
    if "TELNET_ERROR: Telnet请求时发生网络问题或者接口错误，请确认。" not in retMsg:
        id = DubboInterfaceService.addQuickDebugData(addr,service,method,params,bodyDict['actualMsg'],bodyDict['taketime'],request.session.get("loginName"),encoding=encoding)
        bodyDict['id'] = id
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK, "成功！", bodyDict).toJson())

def doTelnetCommand(request):
    addr = request.POST.get("addr")
    addrList = addr.split(":")
    encoding = request.POST.get("encoding","gb18030")
    print("1111 %s" % encoding)
    cmd = request.POST.get("params")
    retMsg = DubboInterfaceService.do_telnet(addrList[0],addrList[1],cmd,encoding=encoding)
    retMsg = retMsg.replace("\r\ndubbo>","")
    bodyDict = {}
    if "elapsed:" in retMsg:
        msgList = retMsg.split("elapsed:")
        bodyDict['actualMsg'] = msgList[0]
        bodyDict['taketime'] = int(msgList[1].split("ms")[0].strip())
    else:
        bodyDict['actualMsg'] = retMsg
        bodyDict['taketime'] = 0
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK, "成功！", bodyDict).toJson())

def getRbecentQueryDebug(request):
    recentDebug = DubboInterfaceService.getRecentQueryDebug(request.session.get("loginName"))
    bodyDict = {}
    if recentDebug:
        bodyDict = recentDebug[0]
        return HttpResponse(ApiReturn(ApiReturn.CODE_OK, "成功！", bodyDict).toJson())
    else:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, "没有找到当前用户的调试记录！", bodyDict).toJson())


########################################################################################################################
def interfaceGetSyncTestCaseStep(request):
    id = request.GET.get("id")
    if VersionService.isCurrentVersion(request):
        interfaceData = dbModelToDict(DubboInterfaceService.getInterfaceForId(id))
        syncList = DubboInterfaceService.syncDelTipList(interfaceData)
    else:
        interfaceData = dbModelToDict(HTTP_interfaceService.getVersionInterfaceForId(id))
        syncList = syncVersionDelTipList(interfaceData, VersionService.getVersionName(request))
    return HttpResponse(ApiReturn(body=syncList).toJson())


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

def importLogPage(request):
    context = {}
    context.update(getConfigs(request))
    context["host"] = request.get_host()
    return render(request,"dubbo/interface/importLogDubboData.html",context)

def saveLogDataToDubboInterfaces(request):
    interfaceCaseList = json.loads(request.body.decode("utf8"))
    importResBl = True
    failMsg = ""
    for tmpCase in interfaceCaseList:
        retBl,retInfo = DubboInterfaceService.addBaseDataToDubboInterface(tmpCase,request.session.get("loginName"),"日志导入数据")
        if retBl == False:
            importResBl = False
            failMsg += "%s.%s(%s)导入失败，原因：%s\n" % (tmpCase['dubboService'],tmpCase['dubboMethod'],tmpCase['dubboParams'],retInfo)

    if importResBl:
        return HttpResponse(ApiReturn(ApiReturn.CODE_OK,message="ok").toJson())
    else:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR,message=failMsg).toJson())

