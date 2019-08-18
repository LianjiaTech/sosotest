from urllib import parse

from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from apps.myadmin.service.AdminManageUserPermissionRelationService import AdminManageUserPermissionRelationService
from apps.common.model.RedisDBConfig import *

logger = logging.getLogger("django")

def adminServiceConf(request):
    context = {}
    context["adminServerConf_check"] = "active"
    return render(request,"myadmin/adminServerConf/admin_server_conf_check.html",context)

def getAdminServiceConf(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy","")
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "单接口管理->查看用例->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT rsc.* from tb_run_server_conf rsc WHERE 1=1 "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and rsc.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql,attrList=checkList,page=page,pageNum=commonWebConfig.userPageNum)
    tcpin = '{"do":300}'
    send_tcp_request(tcpin)

    redisCache = RedisCache()
    runServiceListStr = redisCache.get_data("RUN_SERVICE_LIST")
    runServiceList = json.loads(runServiceListStr)
    for pageData in context['pageDatas']:
        pageData["currentTaskList"] = "-"
        pageData["currentCaseList"] = "-"
        pageData["currentTaskProgressNum"] = 0
        pageData["currentCaseProgressNum"] = 0
    for pageData in context['pageDatas']:
        pageData["protocol"] = ""
        for serviceIndex in runServiceList:
            if pageData["serviceIp"] == serviceIndex["serviceIp"] and pageData["servicePort"] == serviceIndex["servicePort"]:
                if len(serviceIndex["serviceCurrentTaskList"]) > 0:
                    currentTask = ",".join(serviceIndex["serviceCurrentTaskList"])
                else:
                    currentTask = "-"
                if len(serviceIndex["serviceCurrentCaseList"]) > 0:
                    currentCase = ",".join(serviceIndex["serviceCurrentCaseList"])
                else:
                    currentCase = "-"
                pageData["currentTaskList"] = currentTask
                pageData["currentCaseList"] = currentCase
                pageData["currentTaskProgressNum"] = serviceIndex["serviceCurrentTaskProgressNum"]
                pageData["currentCaseProgressNum"] = serviceIndex["serviceCurrentCaseProgressNum"]
                pageData["protocol"] = ",".join(serviceIndex["serviceProtocol"])
    context["serviceList"] = runServiceList
    response = render(request, "myadmin/adminServerConf/subPages/admin_server_conf_sub_page.html",context)
    return response


def getAdminServiceTaskConf(request):

    tcpin = '{"do":301}'
    send_tcp_request(tcpin)
    context = {}
    redisCache = RedisCache()
    taskStatusList = json.loads(redisCache.get_data("TASK_STATUS_LIST"))

    envData = TbConfigHttp.objects.all()
    for index in taskStatusList:
        index["httpConfAlias"] = ""
        if "TaskExecuteEnv" in index.keys():
            for envIndex in envData:
                if index["TaskExecuteEnv"] == envIndex.httpConfKey:
                    index["httpConfAlias"] = envIndex.alias
                    break

        if index["isCluster"] == 0:
            index["status"] = "未消费"
        elif index["isCluster"] == 1:
            index["status"] = "消费中,不可取消"
        elif index["isCluster"] == 2:
            index["status"] = "消费中,可取消"
        elif index["isCluster"] == 3:
            index["status"] = "消费完毕"
        elif index["isCluster"] == 4:
            index["status"] = "标记为不可消费,等待取消"
        elif index["isCluster"] == 5:
            index["status"] = "向消费者告知取消操作"
        elif index["isCluster"] == 6:
            index["status"] = "取消的TCP返回,代表已取消的含义"
        elif index["isCluster"] == 7:
            index["status"] = "执行完成"

    context["taskStatusList"] = taskStatusList
    context["pageCount"] = len(context["taskStatusList"])
    response = render(request, "myadmin/adminServerConf/subPages/admin_task_conf_sub_page.html",context)
    return response

def getAdminServiceConfForId(request):
    serviceId = request.POST.get("serviceId")
    try:
        serviceData = TbRunServerConf.objects.get(id=serviceId)
        requestDict = dbModelToDict(serviceData)
        print(requestDict)
    except Exception as e:
        message = "查询用户出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())
    return HttpResponse(ApiReturn(body=requestDict).toJson())




def editAdminServiceConf(request):
    try:
        requestDict = json.loads(request.POST.get("serviceData"))
        for requestIndex in requestDict.keys():
            if requestDict[requestIndex] == "":
                return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR,message="%s 不能为空" % requestIndex).toJson())
        print(requestDict)
        data = TbRunServerConf.objects.get(id=requestDict["id"])
        data.serviceName = requestDict["serviceName"]
        data.maxTaskProgressNum = requestDict["maxTaskProgressNum"]
        data.maxCaseProgressNum = requestDict["maxCaseProgressNum"]
        data.save()

        tcpStr = '{"do":205,"serviceIp":"%s","servicePort":%s,"serviceMaxTaskProgressNum":%s,"serviceMaxCaseProgressNum":%s}' % (data.serviceIp,data.servicePort,data.maxTaskProgressNum,data.maxCaseProgressNum)
        return HttpResponse(send_tcp_request(tcpStr).toJson())


    except Exception as e:
        message = "编辑服务数据发生异常 %s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())


def delAdminUser(request):
    userId = request.POST.get("userId","")
    if not userId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="userId参数错误").toJson())
    try:
        userData = TbAdminUser.objects.get(state=1, id=userId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="userId查询错误 %s" % e).toJson())
    userData.state = 0
    userData.save()
    '''删除user时，删除关联关系'''
    TbAdminPlatformPermissionUserRelation.objects.filter(loginName=userData.loginName, state=1).update(state=0)
    TbAdminManageUserPermissionRelation.objects.filter(loginName=userData.loginName, state=1).update(state=0)
    TbAdminUserRoleRelation.objects.filter(loginName=userData.loginName, state=1).update(state=0)

    return HttpResponse(ApiReturn().toJson())

def resetAdminUser(request):
    userId = request.POST.get("userId","")
    if not userId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="userId参数错误").toJson())
    try:
        userData = TbAdminUser.objects.get(state=0, id=userId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="userId查询错误 %s" % e).toJson())
    userData.state = 1
    userData.save()
    # AdminUserService.addDefaultPermission(userData.loginName)

    return HttpResponse(ApiReturn().toJson())


'''给单个用户授权'''
def addPermissionsToUser(request):
    userRequest = json.loads(request.POST.get("userPermissionsData"))
    logger.info("addPermission %s" % request.POST.get("userPermissionsData"))
    userId = userRequest["userId"]
    loginName = dbModelListToListDict(TbAdminUser.objects.filter(id=userId))[0]["loginName"]
    permissionKeys = userRequest["permissionKeys"]
    userPermissionsData = {}
    relationData = TbAdminManageUserPermissionRelation.objects.filter(loginName=loginName)
    relationDataList = dbModelListToListDict(relationData)
    for relation in relationDataList:
        '''判断loginName已经插入到数据库中的权限，是否在这次需要插入的permission列表中'''
        relationPermissionKey = relation["permissionKey"]
        '''如果在列表中，说明该permission是这次需要增加的；并且state=0，那么需要更新'''
        if relationPermissionKey in permissionKeys:
            if relation["state"] == 0:
                relation["state"] =1
                AdminManageUserPermissionRelationService.updateUserPermission(relation)
        else:
            '''如果不在列表中，说明该permission是这次需要删除的；并且state=1，将state置为0'''
            if relation["state"] == 1:
                relation["state"] = 0
                AdminManageUserPermissionRelationService.updateUserPermission(relation)

    '''判断loginName是否已经有授权permissionKey,如果没有授权，新增；如果有授权，判断该授权是否已经删除，如果已经删除了，进行更新'''
    for permissionKey in permissionKeys:
        userPermissionsData["loginName"] = loginName
        userPermissionsData["permissionKey"] = permissionKey
        data = TbAdminManageUserPermissionRelation.objects.filter(loginName=loginName, permissionKey=permissionKey)
        '''没有授权，新增'''
        if len(data) == 0:
            result = TbAdminManageUserPermissionRelation()
            result.loginName = userPermissionsData["loginName"]
            result.permissionKey = userPermissionsData["permissionKey"]
            result.save()
        else:
            '''有授权，判断授权是否被删除了'''
            permissionList = dbModelListToListDict(data)
            for permissionIndex in permissionList:
                if permissionIndex["state"] == 0:
                    AdminManageUserPermissionRelationService.updateUserPermission(userPermissionsData)
    return HttpResponse(ApiReturn().toJson())

def queueDeleteTask(request):
    print(11111111111111111111111111111)
    tcpStr = '{"do":302,"TaskExecuteId":%s}' % request.GET.get("taskExecuteId")
    c = send_tcp_request(tcpStr)
    print(c.toJson())
    return HttpResponse(ApiReturn().toJson())
