from apps.common.func.LanguageFunc import *
from apps.common.config import commonWebConfig
from apps.task_suite.services.HTTP_taskSuiteService import HTTP_taskSuiteService
from apps.task.services.HTTP_task_executeService import HTTP_task_executeService
from urllib import parse
from apps.version_manage.services.common_service import VersionService
from apps.task.services.HTTP_taskService import *
from apps.common.decorator.permission_normal_funcitons import *
from apps.common.func.WebFunc import *

def httpTaskSuiteCheck(request):
    langDict = getLangTextDict(request)

    context = {}
    if not isRelease:
        context["env"] = "test"
    context["taskSuiteCheck"] = "current-page"
    # 文本
    text = {}
    text["pageTitle"] = langDict["web"]["httpTaskSuitePageHeadings_check"]
    context["text"] = text

    context["page"] = 1

    return render(request, "InterfaceTest/HTTPTaskSuite/HTTP_taskSuiteCheck.html", context)


def http_taskSuiteListCheck(request):
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
        tbName = "tb_task_suite"
        versionCondition = ""
    else:
        tbName = "tb_version_task_suite"
        versionCondition = "and versionName='%s'" % request.session.get("version")

    execSql = "SELECT t.*,u.userName,um.userName modByName from %s t LEFT JOIN tb_user u ON t.addBy = u.loginName LEFT JOIN tb_user um ON t.modBy = um.loginName  WHERE 1=1 and t.state=1 %s " %(tbName,versionCondition)
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        elif key == "taskFounder" :
            checkList.append("%%%s%%" % checkArr[key])
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and (t.addBy LIKE %s or u.userName LIKE %s) """
            continue
        elif key == "module":
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and t.modulesGroup LIKE %s """
            continue
        elif key == "businessLine":
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and t.businessLineGroup LIKE %s """
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and t.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy

    context = pagination(sqlStr=execSql,attrList=checkList,page=page,pageNum=commonWebConfig.taskPageNum,request=request)
    return render(request, "InterfaceTest/HTTPTaskSuite/SubPages/HTTP_task_suite_list_check_page.html",context)

def getTaskSuiteForId(request):
    langDict = getLangTextDict(request)
    id = request.GET.get("id")
    if VersionService.isCurrentVersion(request):
        taskData = HTTP_taskSuiteService.getTaskSuiteForId(id)
    else:
        taskData = HTTP_taskSuiteService.getVersionTaskSuiteForId(id)
        # taskData = HTTP_taskService.getVersionTaskForTaskId(taskId, VersionService.getVersionName(request))

    if not taskData:
        return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON).toJson())
    taskSuiteDataDict = dbModelToDict(taskData)
    taskSuiteDataDict["userName"] = TbUser.objects.get(loginName=taskData.addBy).userName
    context = {}
    context.update(getServiceConf(request))
    context["httpConf"] = HttpConfService.queryHttpConfSort(request)
    context["taskSuiteData"] = taskSuiteDataDict
    context["option"] = request.GET.get("option")
    return render(request, "InterfaceTest/HTTPTaskSuite/SubPages/task_suite_run_details_page.html", context)

@single_add_page_permission
def taskSuiteAdd(request,context):
    langDict = getLangTextDict(request)
    context["interfacePage"] = 1
    context["testCasePage"] = 1
    context["option"] = "add"
    if not isRelease:
        context["env"] = "test"
    context["taskSuiteAdd"] = "current-page"
    context["checkBusinessLine"] = dbModelListToListDict(BusinessService.getAllBusinessLine())
    context["checkModules"] = dbModelListToListDict(ModulesService.getAllModules())
    context.update(getServiceConf(request))
    text = {}
    text["pageTitle"] = langDict["web"]["httpTaskSuitePageHeadings_%s" % context["option"]]
    text["subPageTitle"] = langDict["web"]["httpTaskSuiteSubPageTitle_%s" % context["option"]]
    context["text"] = text

    return render(request, "InterfaceTest/HTTPTaskSuite/HTTP_taskSuiteAdd.html", context)


def httpTaskSuiteSelectTaskList(request):
    page = request.POST.get("taskPageNum")
    if isInt(page):
        page = int(page)
    else:
        return HttpResponse("<script>alert('请验证页数参数');</script>")

    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy")
    if isSqlInjectable(orderBy):
        return HttpResponse("<script>alert('查询条件非法');</script>")

    if VersionService.isCurrentVersion(request):
        tbName = "tb_task"
        versionCondition = ""
    else:
        tbName = "tb_version_task"
        versionCondition = "and versionName='%s'" % request.session.get("version")


    execSql = "SELECT i.*,i.addByName userName from %s i WHERE i.state=1 %s " % (tbName,versionCondition)
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        elif key == "caseFounder":
            checkList.append("%%%s%%" % checkArr[key])
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and (i.addBy LIKE %s or i.addByName LIKE %s) """
            continue

        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and i.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy

    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.taskSuiteCheckTaskPageNum)
    response = render(request,"InterfaceTest/HTTPTaskSuite/SubPages/HTTP_task_suite_details_select_task_list_check_page.html", context)
    return response

@single_data_permission(TbTaskSuite,TbVersionTaskSuite)
def taskSuiteAddData(request):
    taskSuiteData = json.loads(request.body)

    taskSuiteData["protocol"] = "HTTP"

    if VersionService.isCurrentVersion(request):

        taskSuiteData["addBy"] = request.session.get("loginName")
        createTask = HTTP_taskSuiteService.addTaskSuite(taskSuiteData)
        if createTask.id >= 1:
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        else:

            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON,"任务保存失败").toJson())

    else:
        createTask = HTTP_taskSuiteService.addVersionTask(taskSuiteData,VersionService.getVersionName(request))
        if createTask.id >= 1:
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        else:

            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, "任务保存失败").toJson())

@single_data_permission(TbTaskSuite,TbVersionTaskSuite)
def taskSuiteSaveEdit(request):
    taskSuiteData = json.loads(request.body)
    taskSuiteData["protocol"] = "HTTP"
    if VersionService.isCurrentVersion(request):

        taskSuiteData["modTime"] = datetime.datetime.now()
        taskSuiteData["modBy"] = request.session.get("loginName")
        editTaskData = HTTP_taskSuiteService.editTaskSuite(taskSuiteData)
        if editTaskData == 1:
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        else:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, "任务编辑保存失败").toJson())
    else:
        taskSuiteData["modTime"] = datetime.datetime.now()
        editTaskData = HTTP_taskSuiteService.editVersionTask(taskSuiteData, VersionService.getVersionName(request))
        if editTaskData == 1:
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        else:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, "任务编辑保存失败").toJson())

@single_page_permission
def operationTaskSuite(request,context):
    langDict = getLangTextDict(request)

    context["option"] = request.GET.get("option")
    context["page"] = 1
    if not isRelease:
        context["env"] = "test"
    try:
        if VersionService.isCurrentVersion(request):
            context["addBy"] = HTTP_taskSuiteService.getTaskSuiteForId(request.GET.get("id")).addBy
        else:
            context["addBy"] = HTTP_taskSuiteService.getVersionTaskSuiteForId(request.GET.get("id")).addBy

    except Exception as e:
        print(traceback.format_exc())
        return render(request, "permission/page_404.html")

    context["checkBusinessLine"] = dbModelListToListDict(BusinessService.getAllBusinessLine())
    context["checkModules"] = dbModelListToListDict(ModulesService.getAllModules())
    context["id"] = request.GET.get("id")
    context["interfacePage"] = 1
    context["testCasePage"] = 1
    context["taskAdd"] = "current-page"
    text = {}
    text["pageTitle"] = langDict["web"]["httpTaskPageHeadings_%s" % context["option"]]
    context["text"] = text
    context.update(getServiceConf(request))
    return render(request, "InterfaceTest/HTTPTaskSuite/HTTP_taskSuiteAdd.html", context)



def getTaskSuiteData(request):
    id = request.GET.get("id")

    if VersionService.isCurrentVersion(request):
        taskSuiteDataModel = HTTP_taskSuiteService.getTaskSuiteForId(id)
        taskSuiteData = dbModelToDict(taskSuiteDataModel)
        taskDataList = []
        taskSuiteTaskList = taskSuiteData["taskList"].split(",")
        for i in range(0,len(taskSuiteTaskList)):
            try:
                thisTask = HTTP_taskService.getTaskForTaskId(taskSuiteTaskList[i])
                if not thisTask:
                    continue
                thisTaskDict = dbModelToDict(thisTask)
                thisTaskDict["userName"] = thisTask.addBy.userName
                taskDataList.append(thisTaskDict)
            except Exception as e:
                continue
        taskSuiteData["taskDataList"] = taskDataList
        # print(taskDataList)
        return HttpResponse(ApiReturn(ApiReturn.CODE_OK,body=taskSuiteData).toJson())
    else:
        taskSuiteDataModel = HTTP_taskSuiteService.getVersionTaskSuiteForId(id)
        taskSuiteData = dbModelToDict(taskSuiteDataModel)
        taskDataList = []
        taskSuiteTaskList = taskSuiteData["taskList"].split(",")
        for i in range(0, len(taskSuiteTaskList)):
            try:
                # thisTask = HTTP_taskService.getTaskForTaskId(taskSuiteTaskList[i])
                thisTask = HTTP_taskService.getVersionTaskForTaskId(taskSuiteTaskList[i])
                if not thisTask:
                    continue
                thisTaskDict = dbModelToDict(thisTask)
                thisTaskDict["userName"] = thisTask.addBy.userName

                taskDataList.append(thisTaskDict)
            except Exception as e:
                # print(addBy)
                # taskData["interfaceList"][i].update(addBy)
                continue
        taskSuiteData["taskDataList"] = taskDataList
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR).toJson())

@single_data_permission(TbTaskSuite,TbVersionTaskSuite)
def taskSuiteDel(request):
    id = request.GET.get("id")
    if VersionService.isCurrentVersion(request):
        try:
            taskData = HTTP_taskService.getTaskForId(id)
        except Exception as e:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, "参数id错误 %s" % e).toJson())

        if HTTP_taskSuiteService.delTaskSuiteForId(request,id) == 1:
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        else:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON,"删除失败，请联系管理员").toJson())
    else:
        try:
            taskData = HTTP_taskService.getVersionTaskById(id)
        except Exception as e:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, "参数id错误 %s" % e).toJson())
        # if request.session.get("loginName") != taskData.addBy.loginName:
        #     return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, "只能删除自己创建的任务").toJson())
        if HTTP_taskService.delVersionTaskForId(request,id) == 1:
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        else:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, "删除失败，请联系管理员").toJson())

def getTaskListDataForTaskSuite(request):
    id = request.GET.get("id")
    if VersionService.isCurrentVersion(request):
        taskDataModel = TbTaskSuite.objects.get(id=id)
        taskData = dbModelToDict(taskDataModel)
        getTaskDataSql = taskData["taskList"].replace(",","' union all select thi.id,thi.taskId,thi.title,thi.taskdesc,thi.interfaceNum,thi.addBy,tu.userName from tb_task thi  LEFT JOIN tb_user tu on thi.addBy = tu .loginName  where taskId = '")
        sql = "select thi.id,thi.taskId,thi.title,thi.taskdesc,thi.interfaceNum,thi.addBy,tu.userName from tb_task thi  LEFT JOIN tb_user tu on thi.addBy = tu .loginName  where taskId = '%s'" % getTaskDataSql
        print(sql)
    else:
        taskDataModel = HTTP_taskService.getVersionTaskById(id)
        taskData = dbModelToDict(taskDataModel)
        getInterFaceDataSql = taskData["taskInterfaces"].replace(",","' union all select thi.id,thi.interfaceId,thi.title,thi.casedesc,thi.url,thi.addBy,tu.userName from tb_version_http_interface thi  LEFT JOIN tb_user tu on thi.addBy = tu .loginName  where interfaceId = '")
        sql = "select thi.id,thi.interfaceId,thi.title,thi.casedesc,thi.url,thi.addBy,tu.userName from tb_version_http_interface thi  LEFT JOIN tb_user tu on thi.addBy = tu .loginName  where interfaceId = '%s' and versionName='%s'" % (getInterFaceDataSql,VersionService.getVersionName(request))

    taskInterfaceListData = executeSqlGetDict(sql)
    response = render(request,"InterfaceTest/HTTPTaskSuite/SubPages/task_list_check_page.html", {"pageDatas":taskInterfaceListData})
    return response


def taskSuiteRunAdd(request):
    if VersionService.isCurrentVersion(request):
        taskSuiteData = HTTP_taskSuiteService.getTaskSuiteForId(request.POST.get("id"))
    else:
        taskSuiteData = HTTP_taskSuiteService.getVersionTaskSuiteForId(request.POST.get("id"))

    #先写taskSuite
    taskSuiteExecuteModel = TbTaskSuiteExecute()
    taskSuiteExecuteModel.taskSuiteId = taskSuiteData.taskSuiteId
    taskSuiteExecuteModel.title = taskSuiteData.title
    taskSuiteExecuteModel.taskSuiteDesc = taskSuiteData.taskSuiteDesc
    taskSuiteExecuteModel.protocol = taskSuiteData.protocol
    taskSuiteExecuteModel.status = taskSuiteData.status
    taskSuiteExecuteModel.taskCount = taskSuiteData.taskCount
    taskSuiteExecuteModel.taskList = taskSuiteData.taskList
    taskSuiteExecuteModel.isSendEmail = request.POST.get("isSendEmail")
    taskSuiteExecuteModel.emailList = request.POST.get("emailList") != "" and request.POST.get("emailList") or taskSuiteData.emailList
    taskSuiteExecuteModel.isSaveHistory = request.POST.get("isSaveHistory")
    taskSuiteExecuteModel.execComments = request.POST.get("execComments")
    taskSuiteExecuteModel.retryCount = request.POST.get("retryCount",0)
    taskSuiteExecuteModel.execBy = request.session.get("loginName")
    taskSuiteExecuteModel.httpConfKeyList = request.POST.get("httpConfKey_id")
    taskSuiteExecuteModel.execTime = datetime.datetime.now()
    taskSuiteExecuteModel.execStatus = 2
    httpConfList = request.POST.get("httpConfKey_id").split(",")
    httpConfKeyAliasList = ""
    for httpConfIndex in httpConfList:
        if httpConfKeyAliasList == "":
            httpConfKeyAliasList = TbConfigHttp.objects.get(httpConfKey=httpConfIndex).alias
        else:
            httpConfKeyAliasList = "%s,%s" % (httpConfKeyAliasList,TbConfigHttp.objects.get(httpConfKey=httpConfIndex).alias)
    taskSuiteExecuteModel.httpConfKeyAliasList = httpConfKeyAliasList

    taskSuiteExecuteModel.addBy = request.session.get("loginName")
    taskSuiteExecuteModel.save()

    taskList = taskSuiteData.taskList.split(",")



    #获取taskExecuteId list
    taskExecuteIdList = []
    taskExecuteTcpList = []
    for taskIndex in taskList:
        taskData = TbTask.objects.get(taskId=taskIndex)
        for httpConfIndex in range(0,len(httpConfList)):
            taskExecuteData = TbTaskExecute()
            taskExecuteData.taskId = taskData.taskId
            if taskSuiteData.emailList != "":
                taskExecuteData.emailList = taskSuiteData.emailList
            else:
                taskExecuteData.emailList = taskData.emailList
            taskExecuteData.title = taskData.title
            taskExecuteData.taskdesc = taskData.taskdesc
            taskExecuteData.protocol = taskData.protocol
            taskExecuteData.businessLineGroup = taskData.businessLineGroup
            taskExecuteData.modulesGroup = taskData.modulesGroup
            taskExecuteData.interfaceCount = taskData.interfaceCount
            taskExecuteData.taskInterfaces = taskData.taskInterfaces
            taskExecuteData.caseCount = taskData.caseCount
            taskExecuteData.taskTestcases = taskData.taskTestcases
            taskExecuteData.interfaceNum = taskData.interfaceNum
            taskExecuteData.protocol = request.POST.get("protocol")
            taskExecuteData.emailList = request.POST.get("emailList")
            taskExecuteData.addBy_id = request.session.get("loginName")
            taskExecuteData.addByName = request.session.get("userName")
            taskExecuteData.modBy = request.session.get("loginName")
            taskExecuteData.modByName = request.session.get("userName")

            taskExecuteData.isSaveHistory = request.POST.get("isSaveHistory")
            # taskExecuteData.isSendEmail = 0

            taskExecuteData.isSendEmail = 0
            taskExecuteData.execBy_id = request.session.get("loginName")
            taskExecuteData.execByName = request.session.get("userName")

            taskExecuteData.version = VersionService.getVersionName(request)
            taskExecuteData.execComments = request.POST.get("execComments")
            taskExecuteData.retryCount = request.POST.get("retryCount",0)
            taskExecuteData.httpConfKey_id = httpConfList[httpConfIndex]
            taskExecuteData.httpConfKeyAlias = TbConfigHttp.objects.get(httpConfKey=httpConfList[httpConfIndex]).alias
            taskExecuteData.taskSuiteExecuteId = taskSuiteExecuteModel.id

            taskExecuteData.save(force_insert=True)
            taskExecuteIdList.append(taskExecuteData.id)
            RedisCache().set_data("%s_taskExecute_%s" % ("HTTP",taskExecuteData.id), "0:0:0:0:0", 60 * 60 * 12)
            RedisCache().set_data("%s_taskExecuteStatus_%s" % ("HTTP",taskExecuteData.id), "1", 60 * 60 * 12)
            RedisCache().set_data("%s_taskSuite_%s_task_%s" % ("HTTP",taskSuiteExecuteModel.id,taskExecuteData.id), json.dumps({"progress":0,"testResult":"","execStatus":0}), 60 * 60 * 12)
            tcpin = '{"do":3,"TaskExecuteId":%s,"TaskExecuteEnv":"%s","TaskId":"%s","protocol":"HTTP","TaskSuiteExecuteId":"%s"}' % (
                taskExecuteData.id, taskExecuteData.httpConfKey_id, taskExecuteData.taskId, taskSuiteExecuteModel.id)
            taskExecuteTcpList.append(tcpin)


    taskSuiteExecuteModel.taskExecuteIdList = ",".join('%s' %id for id in taskExecuteIdList)
    taskSuiteExecuteModel.save(force_update=True)
    taskSuiteRedisDict = {"taskExecuteIdList": taskExecuteIdList, "execStatus": 1, "progress": 0,"protocol":taskSuiteData.protocol}
    RedisCache().set_data("%s_taskSuiteExecuteId_%s" % ("HTTP",taskSuiteExecuteModel.id), json.dumps(taskSuiteRedisDict),60 * 60 * 12)
    for index in taskExecuteTcpList:
        retApiResult = send_tcp_request(index)
        if retApiResult.code != ApiReturn.CODE_OK:
            RedisCache().del_data("%s_taskSuiteExecuteId_%s" % ("HTTP",taskSuiteExecuteModel.id))
            for taskIndex in taskExecuteTcpList:
                RedisCache().del_data("%s_taskExecute_%s" % ("HTTP",json.loads(taskIndex)['TaskExecuteId']))
                taskExecuteDataDel = TbTaskExecute.objects.get(id=json.loads(taskIndex)['TaskExecuteId'])
                taskExecuteDataDel.testResult = "ERROR"
                taskExecuteDataDel.save()
            taskSuiteExecuteModel.testResult = "ERROR"
            taskSuiteExecuteModel.save()
            return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, "任务执行添加成功，但是执行服务出现异常，请联系管理员").toJson())

    addUserLog(request, "任务管理->任务执行->成功", "PASS")

    return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())

def taskSuiteResultCheck(request):
    langDict = getLangTextDict(request)

    context = {}
    if not isRelease:
        context["env"] = "test"
    context["taskSuiteExecuteResult"] = "current-page"
    context["checkBusinessLine"] = dbModelListToListDict(BusinessService.getAllBusinessLine())
    context["checkModules"] = dbModelListToListDict(ModulesService.getAllModules())
    context["httpConf"] = HttpConfService.queryHttpConfSort(request)
    # 文本
    text = {}
    text["pageTitle"] = langDict["web"]["httpTaskCheckPageHeadings_check"]
    context["text"] = text

    context["page"] = 1
    return render(request, "InterfaceTest/HTTPTaskSuite/HTTP_task_suite_ExecResult.html", context)


def getTaskSuiteResultList(request):
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy")
    if isSqlInjectable(orderBy):
        return HttpResponse("<script>alert('查询条件非法');</script>")
    execSql = "SELECT t.*,u.userName from tb_task_suite_execute t LEFT JOIN tb_user u ON t.addBy = u.loginName  WHERE  (t.execStatus between 1 and 2) or (t.state=1"
    checkList = []

    for key in checkArr:
        if checkArr[key] == "":
            continue
        elif key == "taskFounder":
            checkList.append("%s%%" % checkArr[key])
            execSql += """ and u.userName LIKE %s """
            continue
        elif key == "module":
            checkList.append("%s%%" % checkArr[key])
            execSql += """ and t.modulesGroup LIKE %s """
            continue
        elif key == "businessLine":
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and t.businessLineGroup LIKE %s """
            continue
        elif key == "httpConfKey":
            checkList.append("%s" % checkArr[key])
            execSql += """ and tch.alias = %s """
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and t.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """) ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.taskPageNum)
    redisCache = RedisCache()

    for pageData in context["pageDatas"]:
        try:
            if pageData["execStatus"] == 2 or pageData["execStatus"] == 1:
                taskExecuteIdList = pageData["taskExecuteIdList"].split(",")
                progressList = []
                for taskIndex in taskExecuteIdList:
                    taskExecStatus = json.loads(redisCache.get_data("%s_taskSuite_%s_task_%s" % ("HTTP",pageData["id"], taskIndex)))
                    # print("""taskExecStatus["execStatus"] """, taskExecStatus["execStatus"])

                    if taskExecStatus["execStatus"] == None:
                        progressList.append(0)
                    elif int(taskExecStatus["execStatus"]) == 3:
                        continue
                    elif int(taskExecStatus["execStatus"]) == 10 or int(taskExecStatus["execStatus"]) == 11:
                        return HttpResponse(ApiReturn(ApiReturn.CODE_RELOAD).toJson())
                    else:
                        progressList.append(taskExecStatus["progress"])
                progressList.sort(reverse=False)
                pageData["passPercent"] = progressList[0]
                print("%s%s" % (pageData["id"], pageData["passPercent"]))

        except Exception:
            print(traceback.format_exc())
            if pageData["execStatus"] == 2 or pageData["execStatus"] == 1:
                pageData["passPercent"] = 0
            else:
                pageData["passPercent"] = 100
            # print(traceback.format_exc())
            pageData["passCount"] = 0
            pageData["failCount"] = 0
            pageData["errorCount"] = 0
        #版本号
        if pageData["version"] == "CurrentVersion":
            pageData["versionText"] = request.session.get("CurrentVersion")
        else:
            pageData["versionText"] = pageData["version"]
        #执行备注
        if pageData["execComments"] == "":
            pageData["execComments"] = "-"

        #保存到历史记录
        if pageData["isSaveHistory"] == 1:
            pageData["isSaveHistoryText"] = "是"
        else:
            pageData["isSaveHistoryText"] = "否"

        #发送报告邮件
        if str(pageData["isSendEmail"])[0] == "1":
            pageData["isSendEmailText"] = "是"
        else:
            pageData["isSendEmailText"] = "否"

    response = render(request, "InterfaceTest/HTTPTaskSuite/SubPages/task_suite_result_list_page.html", context)

    return response


def updateTaskSuiteExecuteProgressData(request):
    taskExecuteIdList = request.POST.get("taskExecuteIds").split(",")
    redisCache = RedisCache()
    resultDict = {}
    try:
        for idIndex in taskExecuteIdList:

            taskSuiteExecuteData = json.loads(redisCache.get_data("%s_taskSuiteExecuteId_%s" % ("HTTP",idIndex)))
            progressList = []
            for taskIndex in taskSuiteExecuteData["taskExecuteIdList"]:
                taskExecStatus = json.loads(redisCache.get_data("%s_taskSuite_%s_task_%s" % ("HTTP",idIndex, taskIndex)))
                # print("""taskExecStatus["execStatus"] """,taskExecStatus["execStatus"] )

                if taskExecStatus["execStatus"] == None :
                    progressList.append(0)
                elif int(taskExecStatus["execStatus"]) == 3:
                    continue
                elif int(taskExecStatus["execStatus"]) == 10 or int(taskExecStatus["execStatus"]) == 11 :
                    return HttpResponse(ApiReturn(ApiReturn.CODE_RELOAD).toJson())
                else:
                    progressList.append(taskExecStatus["progress"])
            progressList.sort(reverse=False)
            taskSuiteExecuteData["passPercent"] = progressList[0]
            resultDict[idIndex] = {}
            resultDict[idIndex]["passPercent"] = taskSuiteExecuteData["passPercent"]
            resultDict[idIndex]["status"] = "2"
            print("progressList[0]",progressList[0])
    except Exception:
        # print(traceback.format_exc())
        return HttpResponse(ApiReturn(ApiReturn.CODE_RELOAD).toJson())

    return HttpResponse(ApiReturn(ApiReturn.CODE_OK,body=resultDict).toJson())

def getTaskSuiteRestltDetail(request):
    id = request.GET.get("id")
    taskExecDataModel = TbTaskSuiteExecute.objects.get(id=id)
    taskExecData = dbModelToDict(taskExecDataModel)
    taskExecData['userName'] = TbUser.objects.get(loginName=taskExecDataModel.addBy).userName
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK,body=json.dumps(taskExecData)).toJson())

def againRunTaskSuite(request):
    if VersionService.isCurrentVersion(request):
        print(request.GET.get("taskSuiteId"))
        taskSuiteData = TbTaskSuiteExecute.objects.get(id = request.GET.get("taskSuiteId"))
    else:
        taskSuiteData = TbTaskSuiteExecute.objects.get(id = request.GET.get("taskSuiteId"))

    # 先写taskSuite
    taskSuiteExecuteModel = TbTaskSuiteExecute()
    taskSuiteExecuteModel.taskSuiteId = taskSuiteData.taskSuiteId
    taskSuiteExecuteModel.title = taskSuiteData.title
    taskSuiteExecuteModel.taskSuiteDesc = taskSuiteData.taskSuiteDesc
    taskSuiteExecuteModel.protocol = taskSuiteData.protocol
    taskSuiteExecuteModel.status = taskSuiteData.status
    taskSuiteExecuteModel.taskCount = taskSuiteData.taskCount
    taskSuiteExecuteModel.taskList = taskSuiteData.taskList
    taskSuiteExecuteModel.isSendEmail = taskSuiteData.isSendEmail
    taskSuiteExecuteModel.emailList = taskSuiteData.emailList
    taskSuiteExecuteModel.isSaveHistory = taskSuiteData.isSaveHistory
    taskSuiteExecuteModel.execComments = taskSuiteData.execComments
    taskSuiteExecuteModel.retryCount = taskSuiteData.retryCount
    taskSuiteExecuteModel.execBy = request.session.get("loginName")
    taskSuiteExecuteModel.httpConfKeyList = taskSuiteData.httpConfKeyList
    taskSuiteExecuteModel.httpConfKeyAliasList = taskSuiteData.httpConfKeyAliasList
    taskSuiteExecuteModel.execTime = datetime.datetime.now()
    taskSuiteExecuteModel.execStatus = 2
    taskSuiteExecuteModel.addBy = request.session.get("loginName")
    taskSuiteExecuteModel.save()

    taskList = taskSuiteData.taskList.split(",")

    httpConfList = taskSuiteData.httpConfKeyList.split(",")

    # 获取taskExecuteId list
    taskExecuteIdList = []
    taskExecuteTcpList = []
    for taskIndex in taskList:
        taskData = TbTask.objects.get(taskId=taskIndex)
        for httpConfIndex in range(0, len(httpConfList)):
            taskExecuteData = TbTaskExecute()
            taskExecuteData.taskId = taskData.taskId
            if taskSuiteData.emailList != "":
                taskExecuteData.emailList = taskSuiteData.emailList
            else:
                taskExecuteData.emailList = taskData.emailList
            taskExecuteData.title = taskData.title
            taskExecuteData.taskdesc = taskData.taskdesc
            taskExecuteData.protocol = taskData.protocol
            taskExecuteData.businessLineGroup = taskData.businessLineGroup
            taskExecuteData.modulesGroup = taskData.modulesGroup
            taskExecuteData.interfaceCount = taskData.interfaceCount
            taskExecuteData.taskInterfaces = taskData.taskInterfaces
            taskExecuteData.caseCount = taskData.caseCount
            taskExecuteData.taskTestcases = taskData.taskTestcases
            taskExecuteData.interfaceNum = taskData.interfaceNum
            taskExecuteData.protocol = taskSuiteData.protocol
            taskExecuteData.emailList = taskSuiteData.emailList
            taskExecuteData.addBy_id = request.session.get("loginName")
            taskExecuteData.addByName = request.session.get("userName")
            taskExecuteData.modBy = request.session.get("loginName")
            taskExecuteData.modByName = request.session.get("userName")
            taskExecuteData.isSaveHistory = taskSuiteData.isSaveHistory
            taskExecuteData.retryCount = taskSuiteData.retryCount
            # taskExecuteData.isSendEmail = 0

            taskExecuteData.isSendEmail = 0
            taskExecuteData.execBy_id = request.session.get("loginName")
            taskExecuteData.execByName = request.session.get("userName")

            taskExecuteData.version = VersionService.getVersionName(request)
            taskExecuteData.execComments = taskSuiteData.execComments
            taskExecuteData.httpConfKey_id = httpConfList[httpConfIndex]
            taskExecuteData.httpConfKeyAlias = TbConfigHttp.objects.get(httpConfKey=httpConfList[httpConfIndex]).alias
            taskExecuteData.taskSuiteExecuteId = taskSuiteExecuteModel.id

            taskExecuteData.save(force_insert=True)
            taskExecuteIdList.append(taskExecuteData.id)
            RedisCache().set_data("%s_taskExecute_%s" % ("HTTP",taskExecuteData.id), "0:0:0:0:0", 60 * 60 * 12)
            RedisCache().set_data("%s_taskExecuteStatus_%s" % ("HTTP",taskExecuteData.id), "1", 60 * 60 * 12)
            RedisCache().set_data("%s_taskSuite_%s_task_%s" % ("HTTP",taskSuiteExecuteModel.id, taskExecuteData.id),
                                  json.dumps({"progress": 0, "testResult": "", "execStatus": 0}), 60 * 60 * 12)
            tcpin = '{"do":3,"TaskExecuteId":%s,"TaskExecuteEnv":"%s","TaskId":"%s","protocol":"HTTP","TaskSuiteExecuteId":"%s"}' % (
                taskExecuteData.id, taskExecuteData.httpConfKey_id, taskExecuteData.taskId,
                taskSuiteExecuteModel.id)
            taskExecuteTcpList.append(tcpin)

    taskSuiteExecuteModel.taskExecuteIdList = ",".join('%s' % id for id in taskExecuteIdList)
    taskSuiteExecuteModel.save(force_update=True)
    taskSuiteRedisDict = {"taskExecuteIdList": taskExecuteIdList, "execStatus": 1, "progress": 0,"protocol":taskSuiteData.protocol}
    RedisCache().set_data("%s_taskSuiteExecuteId_%s" % ("HTTP",taskSuiteExecuteModel.id), json.dumps(taskSuiteRedisDict),
                          60 * 60 * 12)
    for index in taskExecuteTcpList:
        retApiResult = send_tcp_request(index)
        if retApiResult.code != ApiReturn.CODE_OK:
            RedisCache().del_data("%s_taskSuiteExecuteId_%s" % ("HTTP",taskSuiteExecuteModel.id))
            for taskIndex in taskExecuteTcpList:
                RedisCache().del_data("%s_taskExecute_%s" % ("HTTP",json.loads(taskIndex)['TaskExecuteId']))
                taskExecuteDataDel = TbTaskExecute.objects.get(id=json.loads(taskIndex)['TaskExecuteId'])
                taskExecuteDataDel.testResult = "ERROR"
                taskExecuteDataDel.save()
            taskSuiteExecuteModel.testResult = "ERROR"
            taskSuiteExecuteModel.save()
            return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, "任务执行添加成功，但是执行服务出现异常，请联系管理员").toJson())

    addUserLog(request, "任务管理->任务执行->成功", "PASS")

    return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())

def stopTaskSuiteRun(request):
    taskSuiteExecuteId = request.GET.get("taskSuiteExecuteId")
    try:
        taskSuite = TbTaskSuiteExecute.objects.get(id=taskSuiteExecuteId)
        taskSuite.execStatus = 10
        taskSuite.save()
        taskList = taskSuite.taskExecuteIdList.split(",")
        isCancel = True
        for taskIndex in taskList:
            status = TbTaskExecute.objects.get(id=taskIndex).execStatus
            if status == 1 or status == 2:
                isCancel = False
                tcpin = '{"do":4,"TaskExecuteId":%s,"protocol":"HTTP","TaskSuiteExecuteId":%s}' % (
                    taskIndex, taskSuiteExecuteId)
                retApiResult = send_tcp_request(tcpin)
                if retApiResult.code != ApiReturn.CODE_OK:
                    return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, retApiResult.message).toJson())
        if isCancel:
            taskSuite.execStatus = 11
            taskSuite.save()
    except Exception as e:
        print(traceback.format_exc())
        return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON,"请验证id正确性%s" % e).toJson())

    return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())

def getSelectExecuteStatus(request):
    sql = "SELECT testResult,count(*) as count from tb_task_suite_execute GROUP BY testResult"
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK,body=executeSqlGetDict(sql,[])).toJson())