from django.shortcuts import HttpResponse,render
from django.db.models import Q
from apps.common.func.LanguageFunc import *
from apps.common.func.CommonFunc import *
from apps.common.config import commonWebConfig
from apps.config.services.http_confService import HttpConfService
from apps.task.services.HTTP_taskService import HTTP_taskService
from apps.config.services.businessLineService import BusinessService
from apps.config.services.modulesService import ModulesService
from apps.config.services.http_confService import HttpConfService
from apps.config.services.sourceService import SourceService
from apps.config.services.serviceConfService import ServiceConfService
from apps.interface.services.HTTP_interfaceService import HTTP_interfaceService
from apps.test_case.services.HTTP_test_caseService import HTTP_test_caseService
from apps.task.services.HTTP_task_executeService import HTTP_task_executeService
from urllib import parse
from apps.common.func.WebFunc import getServiceConf
from django.db.utils import *
import json,os
from apps.common.func.WebFunc import *
# from Redis.config.RedisDBConfig import *
from apps.version_manage.services.common_service import VersionService
from all_models.models.A0007_task import *
from apps.common.model.RedisDBConfig import *
from apps.common.decorator.permission_normal_funcitons import *


def http_teskCheck(request):
    langDict = getLangTextDict(request)

    context = {}
    if not isRelease:
        context["env"] = "test"
    context["taskCheck"] = "current-page"
    context["checkBusinessLine"] = dbModelListToListDict(BusinessService.getAllBusinessLine())
    context["checkModules"] = dbModelListToListDict(ModulesService.getAllModules())
    # 文本
    text = {}
    text["pageTitle"] = langDict["web"]["httpTaskPageHeadings_check"]
    context["text"] = text

    context["page"] = 1

    return render(request, "InterfaceTest/HTTPTask/HTTP_taskCheck.html", context)

def http_taskListCheck(request):
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
        tbName = "tb_task"
        versionCondition = ""
    else:
        tbName = "tb_version_task"
        versionCondition = "and versionName='%s'" % request.session.get("version")

    execSql = "SELECT t.*,addByName userName from %s t  WHERE t.state=1 %s " %(tbName,versionCondition)
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        elif key == "taskFounder" :
            checkList.append("%%%s%%" % checkArr[key])
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and (t.addBy LIKE %s or t.addByName LIKE %s) """
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
    return render(request,"InterfaceTest/HTTPTask/SubPages/HTTP_taskList_check_page.html",context)


def getTaskForId(request):
    langDict = getLangTextDict(request)
    id = request.GET.get("id")
    if VersionService.isCurrentVersion(request):
        taskData = HTTP_taskService.getTaskForId(id)
    else:
        taskData = HTTP_taskService.getVersionTaskForId(id,VersionService.getVersionName(request))

    if not taskData:
        return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON).toJson())
    taskDataDict = dbModelToDict(taskData)
    taskDataUser = dbModelToDict(taskData.addBy)
    del taskDataUser["id"]
    taskDataDict.update(taskDataUser)
    context = {}
    context.update(getServiceConf(request))
    context["httpConf"] = HttpConfService.queryHttpConfSort(request)
    context["taskData"] = taskDataDict
    context["option"] = request.GET.get("option")
    return render(request,"InterfaceTest/HTTPTask/SubPages/task_Run_DetailsPage.html",context)

# @permission_self
@single_add_page_permission
def taskAdd(request,context):
    langDict = getLangTextDict(request)
    context["interfacePage"] = 1
    context["testCasePage"] = 1
    context["option"] = "add"
    if not isRelease:
        context["env"] = "test"
    context["taskAdd"] = "current-page"
    context["checkBusinessLine"] = dbModelListToListDict(BusinessService.getAllBusinessLine())
    context["checkModules"] = dbModelListToListDict(ModulesService.getAllModules())
    context.update(getServiceConf(request))
    text = {}
    text["pageTitle"] = langDict["web"]["httpTaskPageHeadings_%s" % context["option"]]
    text["subPageTitle"] = langDict["web"]["httpTaskSubPageTitle_%s" % context["option"]]
    context["text"] = text
    # return request.session.get("loginName"),request, "InterfaceTest/HTTPTask/HTTP_taskAdd.html", context
    return render(request, "InterfaceTest/HTTPTask/HTTP_taskAdd.html", context)

def queryPeopleTask(request):
    langDict = getLangTextDict(request)
    pageNum = int(request.GET.get("num"))
    if VersionService.isCurrentVersion(request):
        attrData = HTTP_taskService.queryPeopleTask(pageNum, commonWebConfig.queryPeopleInterface,request.session.get("loginName"))
    else:
        attrData = HTTP_taskService.queryVersionPeopleTask(pageNum, commonWebConfig.queryPeopleInterface,request.session.get("loginName"),VersionService.getVersionName(request))
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK, langDict["web"]["httpTestCaseSuccess"], attrData).toJson())

def httpTestCaseSelectInterfaceCheckList(request):
    page = request.POST.get("interfacePage")
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


    execSql = "SELECT i.*,u.userName from %s i LEFT JOIN tb_user u ON i.addBy = u.loginName LEFT JOIN  tb_modules m ON i.moduleId = m.id LEFT JOIN tb_business_line b ON i.businessLineId = b.id WHERE 1=1 and i.state=1 %s " % (tbName,versionCondition)
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

    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.taskCheckInterfaceSelectPage)
    response = render(request,"InterfaceTest/HTTPTestCase/SubPages/HTTP_TestCase_Select_interface_list_check_page.html", context)
    return response

def httpTaskSelectTestCaseCheckList(request):
    page = request.POST.get("testCasePage")
    if isInt(page):
        page = int(page)
    else:
        return HttpResponse("<script>alert('请验证页数参数');</script>")

    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))

    orderBy = request.POST.get("orderBy")
    if isSqlInjectable(orderBy):
        return HttpResponse("<script>alert('查询条件非法');</script>")

    if VersionService.isCurrentVersion(request):
        tbName = "tb_http_testcase"
        versionCondition = ""
    else:
        tbName = "tb_version_http_testcase"
        versionCondition = "and versionName='%s'" % request.session.get("version")

    execSql = "SELECT t.*,u.userName from %s t LEFT JOIN tb_user u ON t.addBy = u.loginName LEFT JOIN  tb_modules m ON t.moduleId = m.id LEFT JOIN tb_business_line b ON t.businessLineId = b.id WHERE 1=1 and t.state=1 %s " %(tbName,versionCondition)

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

    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.interfaceSelectPageNum)
    response = render(request,"InterfaceTest/HTTPTask/SubPages/HTTP_Task_Select_TestCase_list_check_page.html", context)
    return response

@single_data_permission(TbTask,TbVersionTask)
def taskAddData(request):
    taskData = json.loads(request.body)

    taskData = HTTP_taskService.taskDataToDict(request,taskData)
    taskData["addBy_id"] = request.session.get("loginName")
    taskData["addByName"] = request.session.get("userName")
    if VersionService.isCurrentVersion(request):
        # if "id" not in taskData.keys():
            createTask = HTTP_taskService.addTask(taskData)
            if createTask.id >= 1:
                return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
            else:

                return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON,"任务保存失败").toJson())
        # else:
        #     taskData["modTime"] = datetime.datetime.now()
        #     editTaskData = HTTP_taskService.editTask(taskData)
        #     if editTaskData == 1:
        #         return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        #     else:
        #         return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, "任务编辑保存失败").toJson())
    else:
        # if "id" not in taskData.keys():
            createTask = HTTP_taskService.addVersionTask(taskData,VersionService.getVersionName(request))
            if createTask.id >= 1:
                return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
            else:

                return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, "任务保存失败").toJson())
        # else:
        #     taskData["modTime"] = datetime.datetime.now()
        #     editTaskData = HTTP_taskService.editVersionTask(taskData,VersionService.getVersionName(request))
        #     if editTaskData == 1:
        #         return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        #     else:
        #         return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, "任务编辑保存失败").toJson())

@single_data_permission(TbTask,TbVersionTask)
def taskDataSaveEdit(request):
    taskData = json.loads(request.body)

    taskData = HTTP_taskService.taskDataToDict(request,taskData)

    if VersionService.isCurrentVersion(request):
        taskData["modTime"] = datetime.datetime.now()
        editTaskData = HTTP_taskService.editTask(taskData)
        if editTaskData == 1:
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        else:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, "任务编辑保存失败").toJson())
    else:
        taskData["modTime"] = datetime.datetime.now()
        editTaskData = HTTP_taskService.editVersionTask(taskData,VersionService.getVersionName(request))
        if editTaskData == 1:
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        else:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, "任务编辑保存失败").toJson())


@single_page_permission
def operationTask(request,context):
    langDict = getLangTextDict(request)

    context["option"] = request.GET.get("option")
    context["page"] = 1
    if not isRelease:
        context["env"] = "test"
    try:
        if VersionService.isCurrentVersion(request):
            context["dataAddBy"] = HTTP_taskService.getTaskForId(request.GET.get("id")).addBy.loginName
        else:
            context["dataAddBy"] = HTTP_taskService.getVersionTaskForId(request.GET.get("id"),request.session.get("version")).addBy.loginName

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
    return render(request, "InterfaceTest/HTTPTask/HTTP_taskAdd.html", context)

def getTaskData(request):
    id = request.GET.get("id")

    if VersionService.isCurrentVersion(request):
        taskDataModel = HTTP_taskService.findTaskForId(id)[0]
        taskData = dbModelToDict(taskDataModel)
        serviceConf = ServiceConfService.queryServiceConfSort(request)
        highPriorityVARS = taskData["highPriorityVARS"]
        taskData["priorityCommon"] = substr(highPriorityVARS, "[CONF=common]", "[ENDCONF]")
        taskData["confPriority"] = {}
        for i in range(0, len(serviceConf)):
            if serviceConf[i]["serviceConfKey"] not in highPriorityVARS:
                taskData["confPriority"]["priority%s" % serviceConf[i]["serviceConfKey"]] = ""
                continue
            taskData["confPriority"]["priority%s" % serviceConf[i]["serviceConfKey"]] = substr(highPriorityVARS,"[CONF=%s]" % serviceConf[i]["serviceConfKey"],"[ENDCONF]")
        taskData["interfaceList"] = []
        if taskData["taskInterfaces"]:
            taskInterfaceList = taskData["taskInterfaces"].split(",")
            for i in range(0,len(taskInterfaceList)):
                try:
                    thisInterface = HTTP_interfaceService.getInterfaceForInterfaceId(taskInterfaceList[i])
                    if not thisInterface:
                        continue
                    taskData["interfaceList"].append(dbModelToDict(thisInterface))
                    addBy = dbModelToDict(thisInterface.addBy)
                    del addBy["id"]
                    del addBy["state"]
                    taskData["interfaceList"][i].update(addBy)
                except Exception as e:
                    continue
        taskData["testCaseList"] = []
        if taskData["taskTestcases"]:
            taskTestCaseList = taskData["taskTestcases"].split(",")
            for i in range(0,len(taskTestCaseList)):
                try:
                    thisTestCase = HTTP_test_caseService.getTestCaseForTestCaseId(taskTestCaseList[i])
                    taskData["testCaseList"].append(dbModelToDict(thisTestCase))
                    addBy = dbModelToDict(thisTestCase.addBy)
                    del addBy["id"]
                    del addBy["state"]
                    taskData["testCaseList"][i].update(addBy)
                except Exception as e:
                    continue
        return HttpResponse(ApiReturn(ApiReturn.CODE_OK,body=taskData).toJson())
    else:
        taskDataModel = HTTP_taskService.findVersionTaskForId(id,VersionService.getVersionName(request))[0]
        taskData = dbModelToDict(taskDataModel)
        serviceConf = ServiceConfService.queryServiceConfSort(request)
        highPriorityVARS = taskData["highPriorityVARS"]
        taskData["priorityCommon"] = substr(highPriorityVARS, "[CONF=common]", "[ENDCONF]")
        taskData["confPriority"] = {}
        for i in range(0, len(serviceConf)):
            if serviceConf[i]["serviceConfKey"] not in highPriorityVARS:
                taskData["confPriority"]["priority%s" % serviceConf[i]["serviceConfKey"]] = ""
                continue
            taskData["confPriority"]["priority%s" % serviceConf[i]["serviceConfKey"]] = substr(highPriorityVARS,"[CONF=%s]" % serviceConf[i]["serviceConfKey"],"[ENDCONF]")
        taskData["interfaceList"] = []
        if taskData["taskInterfaces"]:
            taskInterfaceList = taskData["taskInterfaces"].split(",")
            for i in range(0,len(taskInterfaceList)):
                try:
                    thisInterface = HTTP_interfaceService.getVersionInterfaceForInterfaceId(taskInterfaceList[i],VersionService.getVersionName(request))
                    if not thisInterface:
                        continue
                    taskData["interfaceList"].append(dbModelToDict(thisInterface))
                    addBy = dbModelToDict(thisInterface.addBy)
                    del addBy["id"]
                    del addBy["state"]
                    taskData["interfaceList"][i].update(addBy)
                    # print( taskData["interfaceList"][i])
                except Exception as e:
                    # print(addBy)
                    # taskData["interfaceList"][i].update(addBy)
                    taskData["interfaceList"].append('')
                    continue
        taskData["testCaseList"] = []
        if taskData["taskTestcases"]:
            taskTestCaseList = taskData["taskTestcases"].split(",")
            for i in range(0,len(taskTestCaseList)):
                try:
                    thisTestCase = HTTP_test_caseService.getVersionTestCaseForTestCaseId(taskTestCaseList[i],VersionService.getVersionName(request))
                    taskData["testCaseList"].append(dbModelToDict(thisTestCase))
                    addBy = dbModelToDict(thisTestCase.addBy)
                    del addBy["id"]
                    del addBy["state"]
                    taskData["testCaseList"][i].update(addBy)
                except Exception as e:
                    taskData["interfaceList"].append('')
                    continue
        return HttpResponse(ApiReturn(ApiReturn.CODE_OK,body=taskData).toJson())


@single_data_permission(TbTask,TbVersionTask)
def taskDel(request):
    id = request.GET.get("id")
    if VersionService.isCurrentVersion(request):
        try:
            taskData = HTTP_taskService.getTaskForId(id)
        except Exception as e:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, "参数id错误 %s" % e).toJson())


        if HTTP_taskService.delTaskForId(request,id) == 1:
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

def taskDelTheSameCase(request):
    id = request.GET.get("id")
    if VersionService.isCurrentVersion(request):
        try:
            taskData = HTTP_taskService.getTaskForId(id)
        except Exception as e:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, "参数id错误 %s" % e).toJson())
        if request.session.get("loginName") != taskData.addBy.loginName:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, "只能去重自己创建的任务").toJson())

        #开始对task进行去重并保存。


    else:
        try:
            taskData = HTTP_taskService.getVersionTaskById(id)
        except Exception as e:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, "参数id错误 %s" % e).toJson())
        if request.session.get("loginName") != taskData.addBy.loginName:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, "只能去重自己创建的任务").toJson())

        #开始对VersionTask进行去重并保存

    oldTaskInterfaces = taskData.taskInterfaces
    oldInterfaceList = oldTaskInterfaces.split(",")
    newInterfaceList = list(set(oldInterfaceList))
    newInterfaceListStr = ""
    for tmpInterface in newInterfaceList:
        newInterfaceListStr += tmpInterface + ","
    newInterfaceListStr = newInterfaceListStr[:-1]
    taskData.taskInterfaces = newInterfaceListStr

    oldTaskCases = taskData.taskTestcases

    oldCaseList = oldTaskCases.split(",")
    newCaseList = list(set(oldCaseList))
    newCaseStr = ""
    for tmpCase in newCaseList:
        newCaseStr += tmpCase + ","
    newCaseStr = newCaseStr[:-1]
    taskData.taskTestcases = newCaseStr

    try:
        taskData.save(force_update=True)
        return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_ERROR, '去重失败！').toJson())


def taskResultCheck(request):
    langDict = getLangTextDict(request)

    context = {}
    if not isRelease:
        context["env"] = "test"
    context["taskExecuteResult"] = "current-page"
    context["checkBusinessLine"] = dbModelListToListDict(BusinessService.getAllBusinessLine())
    context["checkModules"] = dbModelListToListDict(ModulesService.getAllModules())
    context["httpConf"] = HttpConfService.queryHttpConfSort(request)
    # 文本
    text = {}
    text["pageTitle"] = langDict["web"]["httpTaskCheckPageHeadings_check"]
    context["text"] = text

    context["page"] = 1
    return render(request, "InterfaceTest/HTTPTask/HTTP_task_ExecResult.html", context)

def getTaskResultList(request):
    t1 = datetime.datetime.now()
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy")
    if isSqlInjectable(orderBy):
        return HttpResponse("<script>alert('查询条件非法');</script>")
    execSql = "SELECT t.*,addByName userName,httpConfKeyAlias alias from tb_task_execute t WHERE  (t.execStatus between 1 and 2) or (t.state=1"
    checkList = []
    print(checkArr)
    for key in checkArr:
        if checkArr[key] == "":
            continue
        elif key == "taskFounder":
            checkList.append("%s%%" % checkArr[key])
            execSql += """ and t.addByName LIKE %s """
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
            execSql += """ and t.httpConfKeyalias = %s """
            continue
        elif key == "taskId":
            checkList.append("%s" % checkArr[key])
            execSql += """ and t.taskId = %s """
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and t.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """) ORDER BY %s,%s""" % ("t.execStatus asc",orderBy)
    print(execSql)
    print(checkList)
    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.taskPageNum)
    for pageData in context["pageDatas"]:
        execProgressDataLen = pageData["execProgressData"].split(":")
        try:
            pageData["execPercent"] = "pass"
            pageData["execColor"] = "success"
            pageData["executeCount"] = (
            int(execProgressDataLen[1]) + int(execProgressDataLen[2]) + int(execProgressDataLen[3]))
            pageData["passCount"] = int(execProgressDataLen[1])
            pageData["failCount"] = int(execProgressDataLen[2])
            pageData["errorCount"] = int(execProgressDataLen[3])
            pageData["passPercent"] = int(
                (pageData["executeCount"] / int(execProgressDataLen[0])) * 100)

            if int(execProgressDataLen[2]) > 0 or int(execProgressDataLen[3]) > 0:
                pageData["execPercent"] = "fail"
                pageData["execColor"] = "danger"
        except ZeroDivisionError:
            pageData["passPercent"] = 0

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

    response = render(request, "InterfaceTest/HTTPTask/SubPages/task_result_list_page.html", context)

    return response

def updateTaskExecuteProgressData(request):
    taskExecuteIdList = request.POST.get("taskExecuteIds").split(",")
    redisCache = RedisCache()
    resultDict = {}

    for idIndex in taskExecuteIdList:
        try:
            selfData = redisCache.get_data("%s_taskExecute_%s" % ("HTTP",idIndex))
            # print(selfData)
            selfStatus = redisCache.get_data("%s_taskExecuteStatus_%s" % ("HTTP",idIndex))
        except ValueError:
            taskExecute = TbTaskExecute.objects.get(id=idIndex)
            selfData = taskExecute.execProgressData
            selfStatus = taskExecute.execStatus
            # print(taskExecute.execStatus)
        if selfData == None or int(selfStatus) == 10 or int(selfStatus) == 11 or int(selfStatus) == 3:
            #已经有任务执行完毕了，要刷新页面
            return HttpResponse(ApiReturn(ApiReturn.CODE_RELOAD).toJson())
        else:
            resultDict[idIndex] = {}
            execProgressDataLen = selfData.split(":")
            resultDict[idIndex]["status"] = selfStatus
            resultDict[idIndex]["execPercent"] = "pass"
            resultDict[idIndex]["execColor"] = "success"
            resultDict[idIndex]["executeCount"] = (int(execProgressDataLen[1]) + int(execProgressDataLen[2]) + int(execProgressDataLen[3]))
            resultDict[idIndex]["passCount"] = int(execProgressDataLen[1])
            resultDict[idIndex]["failCount"] = int(execProgressDataLen[2])
            resultDict[idIndex]["errorCount"] = int(execProgressDataLen[3])
            if int(execProgressDataLen[0]) == 0:
                resultDict[idIndex]["passPercent"] = 0.00
            else:
                resultDict[idIndex]["passPercent"] = int((resultDict[idIndex]["executeCount"] / int(execProgressDataLen[0])) * 100)

            if int(execProgressDataLen[2]) > 0 or int(execProgressDataLen[3]) > 0:
                resultDict[idIndex]["execPercent"] = "fail"
                resultDict[idIndex]["execColor"] = "danger"

    return HttpResponse(ApiReturn(ApiReturn.CODE_OK,body=resultDict).toJson())

def queryPeopleTaskExecute(request):
    langDict = getLangTextDict(request)
    pageNum = int(request.GET.get("num"))
    attrData = HTTP_task_executeService.queryPeopleTaskExecute(pageNum, commonWebConfig.queryPeopleInterface,request.session.get("loginName"))
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK, langDict["web"]["httpTestCaseSuccess"], attrData).toJson())


def getTaskRestltDetail(request):
    id = request.GET.get("id")
    taskExecDataModel = HTTP_task_executeService.findTaskRestltForId(id)
    taskExecData = dbModelToDict(taskExecDataModel)
    taskExecData.update(dbModelToDict(taskExecDataModel.httpConfKey))
    taskExecData.update(dbModelToDict(taskExecDataModel.addBy))
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK,body=json.dumps(taskExecData)).toJson())

@sql_inject_validate
def getInterfeceListDataForTask(request):
    id = request.GET.get("id")
    if VersionService.isCurrentVersion(request):
        taskDataModel = HTTP_taskService.getTaskForId(id)
        taskData = dbModelToDict(taskDataModel)
        getInterFaceDataSql = taskData["taskInterfaces"].replace(",","' union all select thi.id,thi.interfaceId,thi.title,thi.casedesc,thi.url,thi.addBy,tu.userName from tb_http_interface thi  LEFT JOIN tb_user tu on thi.addBy = tu .loginName  where interfaceId = '")
        sql = "select thi.id,thi.interfaceId,thi.title,thi.casedesc,thi.url,thi.addBy,tu.userName from tb_http_interface thi  LEFT JOIN tb_user tu on thi.addBy = tu .loginName  where interfaceId = '%s'" % getInterFaceDataSql
    else:
        taskDataModel = HTTP_taskService.getVersionTaskById(id)
        taskData = dbModelToDict(taskDataModel)
        getInterFaceDataSql = taskData["taskInterfaces"].replace(",","' union all select thi.id,thi.interfaceId,thi.title,thi.casedesc,thi.url,thi.addBy,tu.userName from tb_version_http_interface thi  LEFT JOIN tb_user tu on thi.addBy = tu .loginName  where interfaceId = '")
        sql = "select thi.id,thi.interfaceId,thi.title,thi.casedesc,thi.url,thi.addBy,tu.userName from tb_version_http_interface thi  LEFT JOIN tb_user tu on thi.addBy = tu .loginName  where interfaceId = '%s' and versionName='%s'" % (getInterFaceDataSql,VersionService.getVersionName(request))

    taskInterfaceListData = executeSqlGetDict(sql)
    response = render(request,"InterfaceTest/HTTPTask/SubPages/HTTP_Task_Details_Select_interface_list_check_page.html", {"pageDatas":taskInterfaceListData})
    return response

def getTestCaseListDataForTask(request):
    id = request.GET.get("id")
    if VersionService.isCurrentVersion(request):
        taskDataModel = HTTP_taskService.getTaskForId(id)
        taskData = dbModelToDict(taskDataModel)
        getTestCaseDataSql = taskData["taskTestcases"].replace(",","' union all select tht.id,tht.caseId,tht.title,tht.casedesc,tht.stepCount,tht.addBy,tu.userName from tb_http_testcase tht  LEFT JOIN tb_user tu on tht.addBy = tu .loginName where tht.caseId = '")
        sql = "select tht.id,tht.caseId,tht.title,tht.casedesc,tht.stepCount,tht.addBy,tu.userName from tb_http_testcase tht  LEFT JOIN tb_user tu on tht.addBy = tu .loginName where tht.caseId ='%s'" % getTestCaseDataSql
    else:
        taskDataModel = HTTP_taskService.getVersionTaskById(id)
        taskData = dbModelToDict(taskDataModel)
        getTestCaseDataSql = taskData["taskTestcases"].replace(",","' union all select tht.id,tht.caseId,tht.title,tht.casedesc,tht.stepCount,tht.addBy,tu.userName from tb_version_http_testcase tht  LEFT JOIN tb_user tu on tht.addBy = tu .loginName where tht.caseId = '")
        sql = "select tht.id,tht.caseId,tht.title,tht.casedesc,tht.stepCount,tht.addBy,tu.userName from tb_version_http_testcase tht  LEFT JOIN tb_user tu on tht.addBy = tu .loginName where tht.caseId ='%s' and versionName='%s'" % (getTestCaseDataSql,VersionService.getVersionName(request))

    taskTestCaseListData = executeSqlGetDict(sql)
    response = render(request,"InterfaceTest/HTTPTask/SubPages/HTTP_Task_Details_Select_TestCase_list_check_page.html", {"pageDatas":taskTestCaseListData})
    return response


def getInterfeceListData(request):
    #根据任务执行结果
    id = request.GET.get("id")
    taskDataModel = HTTP_task_executeService.findTaskRestltForId(id)
    taskData = dbModelToDict(taskDataModel)
    if taskDataModel.version == "CurrentVersion":
        getInterFaceDataSql = taskData["taskInterfaces"].replace(",","' union all select thi.id,thi.interfaceId,thi.title,thi.casedesc,thi.url,thi.addBy,tu.userName from tb_http_interface thi  LEFT JOIN tb_user tu on thi.addBy = tu .loginName  where interfaceId = '")
        sql = "select thi.id,thi.interfaceId,thi.title,thi.casedesc,thi.url,thi.addBy,tu.userName from tb_http_interface thi  LEFT JOIN tb_user tu on thi.addBy = tu .loginName  where interfaceId = '%s'" % getInterFaceDataSql
    else:
        getInterFaceDataSql = taskData["taskInterfaces"].replace(",","' union all select thi.id,thi.interfaceId,thi.title,thi.casedesc,thi.url,thi.addBy,tu.userName from tb_version_http_interface thi  LEFT JOIN tb_user tu on thi.addBy = tu .loginName  where interfaceId = '")
        sql = "select thi.id,thi.interfaceId,thi.title,thi.casedesc,thi.url,thi.addBy,tu.userName from tb_version_http_interface thi  LEFT JOIN tb_user tu on thi.addBy = tu .loginName  where interfaceId = '%s' and versionName='%s'" % (getInterFaceDataSql,taskDataModel.version)

    taskInterfaceListData = executeSqlGetDict(sql)
    response = render(request,"InterfaceTest/HTTPTask/SubPages/HTTP_Task_Details_Select_interface_list_check_page.html", {"pageDatas":taskInterfaceListData})
    return response

def getTestCaseListData(request):
    id = request.GET.get("id")
    taskDataModel = HTTP_task_executeService.findTaskRestltForId(id)
    taskData = dbModelToDict(taskDataModel)
    if taskDataModel.version == "CurrentVersion":
        getTestCaseDataSql = taskData["taskTestcases"].replace(",","' union all select tht.id,tht.caseId,tht.title,tht.casedesc,tht.stepCount,tht.addBy,tu.userName from tb_http_testcase tht  LEFT JOIN tb_user tu on tht.addBy = tu .loginName where tht.caseId = '")
        sql = "select tht.id,tht.caseId,tht.title,tht.casedesc,tht.stepCount,tht.addBy,tu.userName from tb_http_testcase tht  LEFT JOIN tb_user tu on tht.addBy = tu .loginName where tht.caseId ='%s'" % getTestCaseDataSql
    else:
        getTestCaseDataSql = taskData["taskTestcases"].replace(",","' union all select tht.id,tht.caseId,tht.title,tht.casedesc,tht.stepCount,tht.addBy,tu.userName from tb_version_http_testcase tht  LEFT JOIN tb_user tu on tht.addBy = tu .loginName where tht.caseId = '")
        sql = "select tht.id,tht.caseId,tht.title,tht.casedesc,tht.stepCount,tht.addBy,tu.userName from tb_version_http_testcase tht  LEFT JOIN tb_user tu on tht.addBy = tu .loginName where tht.caseId ='%s' and versionName='%s'" % (getTestCaseDataSql,taskDataModel.version)

    taskTestCaseListData = executeSqlGetDict(sql)
    response = render(request,"InterfaceTest/HTTPTask/SubPages/HTTP_Task_Details_Select_TestCase_list_check_page.html", {"pageDatas":taskTestCaseListData})
    return response

def againRunTask(request):
    #历史版本再次执行取任务错误。
    id = request.GET.get("id")
    res = HTTP_task_executeService.againRunTask(id,request.session.get("loginName"),request.session.get("userName"))
    if res == False:
        return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, '任务已被删除').toJson())

    result = dbModelToDict(res)
    tcpin = '{"do":3,"TaskExecuteId":%s,"TaskExecuteEnv":"%s","TaskId":"%s","protocol":"HTTP"}' % (result["id"],result["httpConfKey_id"],result["taskId"])
    RedisCache().set_data("%s_taskExecute_%s" % ("HTTP",result["id"]), "0:0:0:0:0")
    RedisCache().set_data("%s_taskExecuteStatus_%s" % ("HTTP",result["id"]), "1")
    retApiResult = send_tcp_request(tcpin)
    if retApiResult.code != ApiReturn.CODE_OK:
        HTTP_task_executeService.updateFailExecute(result["id"],retApiResult.message)
        RedisCache().del_data("%s_taskExecute_%s" % ("HTTP",result["id"]))
        RedisCache().del_data("%s_taskExecuteStatus_%s" % ("HTTP",result["id"]))
        return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, retApiResult.message).toJson())
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())

def stopTaskRun(request):
    id = request.GET.get("id")
    taskSuiteExecuteId = request.GET.get("taskSuiteExecuteId")
    try:
        HTTP_task_executeService.stopTaskRun(id)
        RedisCache().set_data("%s_taskExecuteStatus_%s" % ("HTTP",id),"10")
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON,"请验证id正确性%s" % e).toJson())
    tcpin = '{"do":4,"TaskExecuteId":%s,"protocol":"HTTP","TaskSuiteExecuteId":%s}' % (id,taskSuiteExecuteId)
    retApiResult = send_tcp_request(tcpin)
    if retApiResult.code != ApiReturn.CODE_OK:
        return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, retApiResult.message).toJson())
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())

def taskRunAdd(request):
    if VersionService.isCurrentVersion(request):
        taskData = dbModelToDict(HTTP_taskService.getTaskForId(request.POST.get("id")))

    else:
        taskData = dbModelToDict(HTTP_taskService.getVersionTaskForId(request.POST.get("id"),VersionService.getVersionName(request)))
        del taskData["versionName_id"]

    del taskData["id"]
    taskData["protocol"] = request.POST.get("protocol")
    taskData["emailList"] = request.POST.get("emailList")
    taskData["addBy_id"] = request.session.get("loginName")
    taskData["addByName"] = request.session.get("userName")
    taskData["isSaveHistory"] = request.POST.get("isSaveHistory")
    taskData["isSendEmail"] = request.POST.get("isSendEmail")
    taskData["execComments"] = request.POST.get("execComments")
    taskData["retryCount"] = request.POST.get("retryCount")
    taskData["execBy_id"] = request.session.get("loginName")
    taskData["execByName"] = request.session.get("userName")
    taskData["version"] = VersionService.getVersionName(request)

    httpConfList = request.POST.get("httpConfKey_id").split(",")

    retmsg = 0

    for httpConfIndex in range(0,len(httpConfList)):
        taskData["httpConfKey_id"] = httpConfList[httpConfIndex]
        taskData["httpConfKeyAlias"] = TbConfigHttp.objects.filter(httpConfKey=httpConfList[httpConfIndex])[0].alias
        cres = HTTP_task_executeService.taskRunAdd(taskData)
        addDataResult = dbModelToDict(cres)
        # 将任务执行的信息写入缓存，任务执行的前缀为 taskExecute_executeId
        RedisCache().set_data("%s_taskExecute_%s" % ("HTTP",addDataResult["id"]),"0:0:0:0:0",60*60*12)
        RedisCache().set_data("%s_taskExecuteStatus_%s" % ("HTTP",addDataResult["id"]),"1",60*60*12)
        # tcpin = '{"do":3,"TaskExecuteId":"%s"}' % addDataResult["id"]
        tcpin = '{"do":3,"TaskExecuteId":%s,"TaskExecuteEnv":"%s","TaskId":"%s","protocol":"HTTP"}' % (addDataResult["id"], addDataResult["httpConfKey_id"], addDataResult["taskId"])
        retApiResult = send_tcp_request(tcpin)
        if retApiResult.code != ApiReturn.CODE_OK:
            retmsg = 1
            RedisCache().del_data("%s_taskExecute_%s" % ("HTTP",addDataResult["id"]))
            RedisCache().del_data("%s_taskExecuteStatus_%s" % ("HTTP",addDataResult["id"]))

    if retmsg == 1:
        addUserLog(request,"任务管理->任务执行->任务执行添加成功，但是执行服务出现异常，请联系管理员","FAIL")
        return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, "任务执行添加成功，但是执行服务出现异常，请联系管理员").toJson())
    addUserLog(request, "任务管理->任务执行->成功", "PASS")

    return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())

def getSelectExecuteStatus(request):
    sql = "SELECT testResult,count(*) as count from tb_task_execute GROUP BY testResult"
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK,body=executeSqlGetDict(sql,[])).toJson())

def contrastTaskResult(request):
    context = {}
    taskIds = request.POST.get("taskId")
    taskIdList = taskIds.split(",")
    if len(taskIdList) != 2:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR,message="只能选择两个任务进行比对").toJson())
    ret = HTTP_task_executeService.contrastTask(taskIdList)
    if "code" in ret.keys():
        return HttpResponse(ApiReturn(ret["code"], message=ret["message"]).toJson())
    context["taskContrastDict"] = ret
    return render(request,"InterfaceTest/HTTPTask/SubPages/taskContrast.html",context)

def mergeTask(request):
    taskIds = request.POST.get("taskId","")
    taskIdList = taskIds.split(",")

    for index in range(1,len(taskIdList)):
        if taskIdList[0] == taskIdList[index]:
            return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR,message="副任务中包含主任务，不能合并").toJson())
    tbModule = TbTask.objects.get(taskId=taskIdList[0])
    businessLineList = []
    moduleList = []
    emailList = []
    interfeces = ""
    testCases= ""
    interfaceNum = 0
    sourceList = []
    for index in taskIdList:
        try:
            tmpTaskData = HTTP_taskService.getTaskForTaskId(index)
        except:
            return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR,message="任务不存在").toJson())
        interfaceNum += tmpTaskData.interfaceNum
        if interfaceNum > commonWebConfig.maxTaskInculedInterfaceNum:
            return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR, message="合并任务包含总接口数量超过阈值%s，合并失败" % commonWebConfig.maxTaskInculedInterfaceNum).toJson())
        businessLineList.extend(BL_MD_isList(tmpTaskData.businessLineGroup))
        moduleList.extend(BL_MD_isList(tmpTaskData.modulesGroup))
        sourceList.extend(BL_MD_isList(tmpTaskData.sourceGroup))
        if tmpTaskData.emailList != "":
            emailList.extend(tmpTaskData.emailList.split(","))
        if interfeces == "":
            interfeces = tmpTaskData.taskInterfaces
        else:
            interfeces = "%s,%s"%(interfeces,tmpTaskData.taskInterfaces)
        if testCases == "":
            testCases = tmpTaskData.taskTestcases
        else:
            testCases = "%s,%s"%(testCases,tmpTaskData.taskTestcases)
    try:
        #业务线和模块和email去重
        tbModule.businessLineGroup = list(set(businessLineList))
        tbModule.modulesGroup = list(set(moduleList))
        tbModule.taskInterfaces = interfeces
        tbModule.taskTestcases = testCases
        tbModule.interfaceNum = interfaceNum
        tbModule.emailList = ','.join(list(set(emailList)))
        tbModule.sourceGroup = list(set(sourceList))
        tbModule.save()
    except Exception as e:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR, message="任务合并出错，请联系管理员").toJson())
    return HttpResponse(ApiReturn().toJson())


def executeIdforTask(request):
    taskId = request.GET.get("taskId", "")
    date = request.GET.get("date", "")
    # 如果date为空，默认查询1天内数据
    if date == "":
        dateTo = datetime.date.today()
        dateFrom = dateTo - datetime.timedelta(days=1)
    else:
        try:
            dateFrom = datetime.datetime.strptime(date, '%Y-%m-%d')
            dateTo = dateFrom + datetime.timedelta(days=1)
        except Exception as e:
            return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR, message="date格式不正确").toJson())
    executeId = HTTP_taskService.getExecuteIdByTaskId(taskId,dateFrom,dateTo)
    if executeId:
        executeResult = dbModelToDict(executeId)
    else:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR, message="任务"+taskId+"不存在").toJson())
    return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR, message="",body={'result':executeResult['testResultMsg']}).toJson())