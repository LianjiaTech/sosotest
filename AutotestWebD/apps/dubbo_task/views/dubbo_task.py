from django.shortcuts import HttpResponse,render
from apps.common.func.LanguageFunc import *
from apps.common.func.CommonFunc import *
from apps.common.config import commonWebConfig
from apps.config.services.http_confService import HttpConfService
# from apps.task.services.HTTP_taskService import HTTP_taskService
from apps.dubbo_task.services.dubbo_taskService import DubboTaskService
from apps.config.services.businessLineService import BusinessService
from apps.config.services.modulesService import ModulesService
from apps.config.services.http_confService import HttpConfService
from apps.config.services.sourceService import SourceService
from apps.config.services.serviceConfService import ServiceConfService
from apps.dubbo_interface.services.dubbo_interface_service import DubboInterfaceService
from apps.dubbo_testcase.services.dubbo_testcase_service import DubboTestcaseService
from apps.dubbo_task.services.dubbo_task_executeService import DubboTaskExecuteService
from urllib import parse
from all_models_for_dubbo.models import Tb2DubboTaskExecute,Tb2DubboTask
from apps.common.func.WebFunc import getServiceConf
from django.db.utils import *
import json
from apps.common.func.WebFunc import *
from apps.common.decorator.permission_normal_funcitons import *

from apps.version_manage.services.common_service import VersionService

def dubbo_testCheck(request):
    langDict = getLangTextDict(request)

    context = {}
    if not isRelease:
        context["env"] = "test"
    context["taskCheck"] = "current-page"
    context["checkBusinessLine"] = dbModelListToListDict(BusinessService.getAllBusinessLine())
    context["checkModules"] = dbModelListToListDict(ModulesService.getAllModules())
    # 文本
    text = {}
    text["pageTitle"] = langDict["dubbo"]["dubboTaskPageHeadings_check"]
    context["text"] = text
    context["page"] = 1

    # context["lang"] = getLangTextDict(request)
    return render(request, "dubbo/task/taskCheck.html", context)

def dubbo_taskListCheck(request):
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
        tbName = "tb2_dubbo_task"
        versionCondition = ""
    else:
        tbName = "tb2_dubbo_version_task"
        versionCondition = "and versionName='%s'" % request.session.get("version")

    execSql = "SELECT t.*,u.userName,um.userName modByName from %s t LEFT JOIN tb_user u ON t.addBy = u.loginName LEFT JOIN tb_user um ON t.modBy = um.loginName  WHERE t.state=1 %s " %(tbName,versionCondition)
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


    response = render(request, "dubbo/task/SubPages/taskList_check_page.html",context)
    return response

def getTaskForTaskId(request):
    langDict = getLangTextDict(request)
    id = request.GET.get("id")
    if VersionService.isCurrentVersion(request):
        taskData = DubboTaskService.getTaskForId(id)
    else:
        taskData = DubboTaskService.getVersionTaskForId(id,VersionService.getVersionName(request))

    if not taskData:
        return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON).toJson())
    taskDataDict = dbModelToDict(taskData)
    taskDataUser = dbModelToDict(taskData.addBy)
    del taskDataUser["id"]
    taskDataDict.update(taskDataUser)
    context = {}
    context.update(getServiceConf(request))
    # context["httpConf"] = HttpConfService.queryHttpConfSort(request)
    envConfList = DubboInterfaceService.queryDubboConfSort(request)
    context["httpConf"] = envConfList
    context["taskData"] = taskDataDict
    context["option"] = request.GET.get("option")
    return render(request,"dubbo/task/SubPages/task_Run_DetailsPage.html",context)

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
    text["pageTitle"] = langDict["dubbo"]["dubboTaskPageHeadings_%s" % context["option"]]
    text["subPageTitle"] = langDict["dubbo"]["dubboTaskSubPageTitle_%s" % context["option"]]
    context["text"] = text
    return render(request, "dubbo/task/taskAdd.html", context)

def queryPeopleTask(request):
    langDict = getLangTextDict(request)
    pageNum = int(request.GET.get("num"))
    if VersionService.isCurrentVersion(request):
        attrData = DubboTaskService.queryPeopleTask(pageNum, commonWebConfig.queryPeopleInterface,request.session.get("loginName"))
    else:
        attrData = DubboTaskService.queryVersionPeopleTask(pageNum, commonWebConfig.queryPeopleInterface,request.session.get("loginName"),VersionService.getVersionName(request))
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK, langDict["dubbo"]["httpTestCaseSuccess"], attrData).toJson())

def TestCaseSelectInterfaceCheckList(request):
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
        tbName = "tb2_dubbo_interface"
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
    response = render(request,"dubbo/testcase/SubPages/TestCase_Select_interface_list_check_page.html", context)
    return response

def dubboTaskSelectTestCaseCheckList(request):
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
        tbName = "tb2_dubbo_testcase"
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

@single_data_permission(Tb2DubboTask,Tb2DubboTask)
def taskAddData(request):
    taskData = json.loads(request.body)

    taskInterfaceBusinessLineArr = []
    taskInterfaceModulesArr = []
    taskInterfaceSourceArr = []
    if taskData["taskInterfaces"] != "":
        #去重，切成数组遍历获取业务线名称
        taskInterfaceList =  list(set(taskData["taskInterfaces"].split(",")))
        taskInterfaceListPartSql = ''
        for i in range(0,len(taskInterfaceList)):
            if i == 0:
                taskInterfaceListPartSql = "interfaceId = '%s'" % taskInterfaceList[i]
                continue
            taskInterfaceListPartSql += " or interfaceId = '%s'" % taskInterfaceList[i]
        if VersionService.isCurrentVersion(request):
            taskInterfaceBusinessLineArr = BusinessService.getInterfaceListBusinessId(taskInterfaceListPartSql,"DUBBO")
            taskInterfaceModulesArr = ModulesService.getInterfaceListModulesId(taskInterfaceListPartSql,"DUBBO")
            # taskInterfaceSourceArr = SourceService.getInterfaceListSourcesId(taskInterfaceListPartSql)
        else:
            taskInterfaceBusinessLineArr = BusinessService.getVersionInterfaceListBusinessId(taskInterfaceListPartSql,VersionService.getVersionName(request))
            taskInterfaceModulesArr = ModulesService.getVersionInterfaceListModulesId(taskInterfaceListPartSql,VersionService.getVersionName(request))
            # taskInterfaceSourceArr = SourceService.getVersionInterfaceListSourcesId(taskInterfaceListPartSql,VersionService.getVersionName(request))

    taskTestCaseBusinessLineArr = []
    taskTestCaseModulesArr = []
    # taskTestCaseSourceArr = []
    if taskData["taskTestcases"] != "":
        #去重，切成数组遍历获取业务线名称
        taskTestCaseList =  list(set(taskData["taskTestcases"].split(",")))
        taskTestCasePartSql = ""
        for i in range(0, len(taskTestCaseList)):
            if i == 0:
                taskTestCasePartSql = "caseId = '%s'" % taskTestCaseList[i]
                continue
            taskTestCasePartSql += " or caseId = '%s'" % taskTestCaseList[i]

        if VersionService.isCurrentVersion(request):
            taskTestCaseBusinessLineArr = BusinessService.getTestCaseListBusinessId(taskTestCasePartSql,protocol="DUBBO")
            taskTestCaseModulesArr = ModulesService.getTestCaseListModulesId(taskTestCasePartSql,protocol="DUBBO")
            # taskTestCaseSourceArr = SourceService.getTestCaseListSourcesId(taskTestCasePartSql)
        else:
            taskTestCaseBusinessLineArr = BusinessService.getVersionTestCaseListBusinessId(taskTestCasePartSql,VersionService.getVersionName(request))
            taskTestCaseModulesArr = ModulesService.getVersionTestCaseListModulesId(taskTestCasePartSql,VersionService.getVersionName(request))
            # taskTestCaseSourceArr = SourceService.getVersionTestCaseListSourcesId(taskTestCasePartSql,VersionService.getVersionName(request))

    businessLineGroupArr = taskInterfaceBusinessLineArr + taskTestCaseBusinessLineArr
    businessLineGroup = []
    for i in range(0,len(businessLineGroupArr)):
        businessLineGroup.append(businessLineGroupArr[i]["bussinessLineName"])
    taskData["businessLineGroup"] = list(set(businessLineGroup))

    modulesGroupArr = taskInterfaceModulesArr + taskTestCaseModulesArr
    modulesGroup = []
    for i in range(0,len(modulesGroupArr)):
        modulesGroup.append(modulesGroupArr[i]["moduleName"])
    taskData["modulesGroup"] = list(set(modulesGroup))
    taskData["protocol"] = "DUBBO"
    taskData["addBy_id"] = request.session.get("loginName")

    # sourcesGroupArr = taskInterfaceSourceArr + taskTestCaseSourceArr
    # sourceGroup = []
    # for i in range(0,len(sourcesGroupArr)):
    #     sourceGroup.append(sourcesGroupArr[i]["sourceName"])
    # taskData["sourceGroup"] = list(set(sourceGroup))

    if VersionService.isCurrentVersion(request):
        if "id" not in taskData.keys():
            createTask = DubboTaskService.addTask(taskData)
            if createTask.id >= 1:
                return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
            else:

                return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON,"任务保存失败").toJson())
        else:
            taskData["modTime"] = datetime.datetime.now()
            editTaskData = DubboTaskService.editTask(taskData)
            if editTaskData == 1:
                return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
            else:
                return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, "任务编辑保存失败").toJson())
    else:
        if "id" not in taskData.keys():
            createTask = DubboTaskService.addVersionTask(taskData,VersionService.getVersionName(request))
            if createTask.id >= 1:
                return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
            else:

                return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, "任务保存失败").toJson())
        else:
            taskData["modTime"] = datetime.datetime.now()
            editTaskData = DubboTaskService.editVersionTask(taskData,VersionService.getVersionName(request))
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
            context["dataAddBy"] = DubboTaskService.getTaskForId(request.GET.get("id")).addBy.loginName
        else:
            context["dataAddBy"] = DubboTaskService.getVersionTaskForId(request.GET.get("id"),request.session.get("version")).addBy.loginName

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
    text["pageTitle"] = langDict["dubbo"]["dubboTaskPageHeadings_%s" % context["option"]]
    context["text"] = text
    context.update(getServiceConf(request))
    return render(request, "dubbo/task/taskAdd.html", context)


def getTaskData(request):
    id = request.GET.get("id")
    if VersionService.isCurrentVersion(request):
        taskDataModel = DubboTaskService.findTaskForId(id)[0]
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
                    thisInterface = DubboInterfaceService.getInterfaceForInterfaceId(taskInterfaceList[i])
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
                    thisTestCase = DubboTestcaseService.getTestCaseForTestCaseId(taskTestCaseList[i])
                    taskData["testCaseList"].append(dbModelToDict(thisTestCase))
                    addBy = dbModelToDict(thisTestCase.addBy)
                    del addBy["id"]
                    del addBy["state"]
                    taskData["testCaseList"][i].update(addBy)
                except Exception as e:
                    continue
        return HttpResponse(ApiReturn(ApiReturn.CODE_OK,body=taskData).toJson())
    else:
        taskDataModel = DubboTaskService.findVersionTaskForId(id,VersionService.getVersionName(request))[0]
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

@single_data_permission(Tb2DubboTask,Tb2DubboTask)
def taskDataEdit(request):
    if VersionService.isCurrentVersion(request):
        postLoad = json.loads(request.body)
        # if postLoad["addBy"] != request.session.get("loginName"):
        #     return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, '只可以编辑自己的任务').toJson())
        taskInterfaceBusinessLineArr = []
        taskInterfaceModulesArr = []
        taskInterfaceSourceArr = []
        if postLoad["taskInterfaces"] != "":
            # 去重，切成数组遍历获取业务线名称
            taskInterfaceList = list(set(postLoad["taskInterfaces"].split(",")))
            taskInterfaceListPartSql = ''
            for i in range(0, len(taskInterfaceList)):
                if i == 0:
                    taskInterfaceListPartSql = "interfaceId = '%s'" % taskInterfaceList[i]
                    continue
                taskInterfaceListPartSql += " or interfaceId = '%s'" % taskInterfaceList[i]
            taskInterfaceBusinessLineArr = BusinessService.getInterfaceListBusinessId(taskInterfaceListPartSql,"DUBBO")
            taskInterfaceModulesArr = ModulesService.getInterfaceListModulesId(taskInterfaceListPartSql,"DUBBO")
            # taskInterfaceSourceArr = SourceService.getInterfaceListSourcesId(taskInterfaceListPartSql)

        taskTestCaseBusinessLineArr = []
        taskTestCaseModulesArr = []
        # taskTestCaseSourceArr = []
        if postLoad["taskTestcases"] != "":
            # 去重，切成数组遍历获取业务线名称
            taskTestCaseList = list(set(postLoad["taskTestcases"].split(",")))
            taskTestCasePartSql = ""
            for i in range(0, len(taskTestCaseList)):
                if i == 0:
                    taskTestCasePartSql = "caseId = '%s'" % taskTestCaseList[i]
                    continue
                taskTestCasePartSql += " or caseId = '%s'" % taskTestCaseList[i]
            taskTestCaseBusinessLineArr = BusinessService.getTestCaseListBusinessId(taskTestCasePartSql,protocol="DUBBO")
            taskTestCaseModulesArr = ModulesService.getTestCaseListModulesId(taskTestCasePartSql,protocol="DUBBO")
            # taskTestCaseSourceArr = SourceService.getTestCaseListSourcesId(taskTestCasePartSql)

        businessLineGroupArr = taskInterfaceBusinessLineArr + taskTestCaseBusinessLineArr
        businessLineGroup = []
        for i in range(0, len(businessLineGroupArr)):
            businessLineGroup.append(businessLineGroupArr[i]["bussinessLineName"])
        postLoad["businessLineGroup"] = list(set(businessLineGroup))

        modulesGroupArr = taskInterfaceModulesArr + taskTestCaseModulesArr
        modulesGroup = []
        for i in range(0, len(modulesGroupArr)):
            modulesGroup.append(modulesGroupArr[i]["moduleName"])
        postLoad["modulesGroup"] = list(set(modulesGroup))

        # sourcesGroupArr = taskInterfaceSourceArr + taskTestCaseSourceArr
        # sourceGroup = []
        # for i in range(0, len(sourcesGroupArr)):
        #     sourceGroup.append(sourcesGroupArr[i]["sourceName"])
        # postLoad["sourceGroup"] = list(set(sourceGroup))

        postLoad["modTime"] = datetime.datetime.now()
        postLoad["modBy"] = request.session.get("loginName")

        saveEditResult = DubboTaskService.editTask(postLoad)
        if saveEditResult == 1:
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        else:
            return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_ERROR,'保存编辑失败！').toJson())
    else:
        #TODO 历史版本
        postLoad = json.loads(request.body)
        if postLoad["addBy"] != request.session.get("loginName"):
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, '只可以编辑自己的任务').toJson())
        taskInterfaceBusinessLineArr = []
        taskInterfaceModulesArr = []
        taskInterfaceSourceArr = []
        if postLoad["taskInterfaces"] != "":
            # 去重，切成数组遍历获取业务线名称
            taskInterfaceList = list(set(postLoad["taskInterfaces"].split(",")))
            taskInterfaceListPartSql = ''
            for i in range(0, len(taskInterfaceList)):
                if i == 0:
                    taskInterfaceListPartSql = "interfaceId = '%s'" % taskInterfaceList[i]
                    continue
                taskInterfaceListPartSql += " or interfaceId = '%s'" % taskInterfaceList[i]
            taskInterfaceBusinessLineArr = BusinessService.getVersionInterfaceListBusinessId(taskInterfaceListPartSql,VersionService.getVersionName(request))
            taskInterfaceModulesArr = ModulesService.getVersionInterfaceListModulesId(taskInterfaceListPartSql,VersionService.getVersionName(request))
            taskInterfaceSourceArr = SourceService.getVersionInterfaceListSourcesId(taskInterfaceListPartSql,VersionService.getVersionName(request))

        taskTestCaseBusinessLineArr = []
        taskTestCaseModulesArr = []
        taskTestCaseSourceArr = []
        if postLoad["taskTestcases"] != "":
            # 去重，切成数组遍历获取业务线名称
            taskTestCaseList = list(set(postLoad["taskTestcases"].split(",")))
            taskTestCasePartSql = ""
            for i in range(0, len(taskTestCaseList)):
                if i == 0:
                    taskTestCasePartSql = "caseId = '%s'" % taskTestCaseList[i]
                    continue
                taskTestCasePartSql += " or caseId = '%s'" % taskTestCaseList[i]
            taskTestCaseBusinessLineArr = BusinessService.getVersionTestCaseListBusinessId(taskTestCasePartSql,VersionService.getVersionName(request))
            taskTestCaseModulesArr = ModulesService.getVersionTestCaseListModulesId(taskTestCasePartSql,VersionService.getVersionName(request))
            taskTestCaseSourceArr = SourceService.getVersionTestCaseListSourcesId(taskTestCasePartSql,VersionService.getVersionName(request))

        businessLineGroupArr = taskInterfaceBusinessLineArr + taskTestCaseBusinessLineArr
        businessLineGroup = []
        for i in range(0, len(businessLineGroupArr)):
            businessLineGroup.append(businessLineGroupArr[i]["bussinessLineName"])
        postLoad["businessLineGroup"] = list(set(businessLineGroup))

        modulesGroupArr = taskInterfaceModulesArr + taskTestCaseModulesArr
        modulesGroup = []
        for i in range(0, len(modulesGroupArr)):
            modulesGroup.append(modulesGroupArr[i]["moduleName"])
        postLoad["modulesGroup"] = list(set(modulesGroup))

        sourcesGroupArr = taskInterfaceSourceArr + taskTestCaseSourceArr
        sourceGroup = []
        for i in range(0, len(sourcesGroupArr)):
            sourceGroup.append(sourcesGroupArr[i]["sourceName"])
        postLoad["sourceGroup"] = list(set(sourceGroup))

        postLoad["modTime"] = datetime.datetime.now()

        saveEditResult = DubboTaskService.editVersionTask(postLoad,VersionService.getVersionName(request))
        if saveEditResult == 1:
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        else:
            return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_ERROR, '保存编辑失败！').toJson())

@single_data_permission(Tb2DubboTask,Tb2DubboTask)
def taskDel(request):
    id = request.GET.get("id")
    if VersionService.isCurrentVersion(request):
        try:
            taskData = DubboTaskService.getTaskForId(id)
        except Exception as e:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, "参数id错误 %s" % e).toJson())
        # if request.session.get("loginName") != taskData.addBy.loginName:
        #     return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, "只能删除自己创建的任务").toJson())

        if DubboTaskService.delTaskForId(id) == 1:
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        else:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON,"删除失败，请联系管理员").toJson())
    else:
        try:
            taskData = DubboTaskService.getVersionTaskById(id)
        except Exception as e:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, "参数id错误 %s" % e).toJson())
        # if request.session.get("loginName") != taskData.addBy.loginName:
        #     return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, "只能删除自己创建的任务").toJson())

        if DubboTaskService.delVersionTaskForId(id) == 1:
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        else:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, "删除失败，请联系管理员").toJson())

def taskDelTheSameCase(request):
    id = request.GET.get("id")
    if VersionService.isCurrentVersion(request):
        try:
            taskData = DubboTaskService.getTaskForId(id)
        except Exception as e:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, "参数id错误 %s" % e).toJson())
        if request.session.get("loginName") != taskData.addBy.loginName:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, "只能去重自己创建的任务").toJson())

        #开始对task进行去重并保存。


    else:
        try:
            taskData = DubboTaskService.getVersionTaskById(id)
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
    text["pageTitle"] = langDict["dubbo"]["dubboTaskCheckPageHeadings_check"]
    context["text"] = text

    context["page"] = 1
    return render(request, "dubbo/task/task_ExecResult.html", context)

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
    execSql = "SELECT t.*,u.userName,tch.alias from tb2_dubbo_task_execute t LEFT JOIN tb_user u ON t.addBy = u.loginName LEFT JOIN tb_config_http tch on t.httpConfKey = tch.httpConfKey WHERE  (t.execStatus in (1,2)) or (t.state=1"
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        elif key == "taskFounder":
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
        elif key == "httpConfKey":
            checkList.append("%s" % checkArr[key])
            execSql += """ and tch.alias = %s """
            continue
        elif key == "taskId":
            checkList.append("%s" % checkArr[key])
            execSql += """ and t.taskId = %s """
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and t.%s """ % key
        execSql += """ LIKE %s"""

    execSql += """) ORDER BY %s,%s""" % ("t.execStatus asc", orderBy)
    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.taskPageNum)

    for pageData in context["pageDatas"]:
        #进度条和颜色
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
        if pageData["isSendEmail"] == 1:
            pageData["isSendEmailText"] = "是"
        else:
            pageData["isSendEmailText"] = "否"

    response = render(request, "dubbo/task/SubPages/task_result_list_page.html", context)

    print(datetime.datetime.now()-t1)
    return response



def updateTaskExecuteProgressData(request):
    taskExecuteIdList = request.POST.get("taskExecuteIds").split(",")
    redisCache = RedisCache()
    resultDict = {}
    for idIndex in taskExecuteIdList:
        try:
            selfData = redisCache.get_data("%s_taskExecute_%s" % ("DUBBO",idIndex))
            # print(selfData)
            selfStatus = redisCache.get_data("%s_taskExecuteStatus_%s" % ("DUBBO",idIndex))
        except ValueError:
            taskExecute = Tb2DubboTaskExecute.objects.get(id=idIndex)
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
    attrData = DubboTaskExecuteService.queryPeopleTaskExecute(pageNum, commonWebConfig.queryPeopleInterface,request.session.get("loginName"))
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK, langDict["dubbo"]["httpTestCaseSuccess"], attrData).toJson())


def getTaskRestltDetail(request):
    id = request.GET.get("id")
    taskExecDataModel = DubboTaskExecuteService.findTaskRestltForId(id)
    taskExecData = dbModelToDict(taskExecDataModel)
    taskExecData.update(dbModelToDict(taskExecDataModel.httpConfKey))
    taskExecData.update(dbModelToDict(taskExecDataModel.addBy))
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK,body=json.dumps(taskExecData)).toJson())

@sql_inject_validate
def getInterfeceListDataForTask(request):
    id = request.GET.get("id")
    if VersionService.isCurrentVersion(request):
        taskDataModel = DubboTaskService.getTaskForId(id)
        taskData = dbModelToDict(taskDataModel)
        getInterFaceDataSql = taskData["taskInterfaces"].replace(",","' union all select thi.id,thi.interfaceId,thi.title,thi.casedesc,thi.dubboSystem,thi.dubboService,thi.dubboMethod,thi.addBy,tu.userName from tb2_dubbo_interface thi  LEFT JOIN tb_user tu on thi.addBy = tu .loginName  where interfaceId = '")
        sql = "select thi.id,thi.interfaceId,thi.title,thi.casedesc,thi.dubboSystem,thi.dubboService,thi.dubboMethod,thi.addBy,tu.userName from tb2_dubbo_interface thi  LEFT JOIN tb_user tu on thi.addBy = tu .loginName  where interfaceId = '%s'" % getInterFaceDataSql
    else:
        taskDataModel = DubboTaskService.getVersionTaskById(id)
        taskData = dbModelToDict(taskDataModel)
        getInterFaceDataSql = taskData["taskInterfaces"].replace(",","' union all select thi.id,thi.interfaceId,thi.title,thi.casedesc,thi.url,thi.addBy,tu.userName from tb_version_http_interface thi  LEFT JOIN tb_user tu on thi.addBy = tu .loginName  where interfaceId = '")
        sql = "select thi.id,thi.interfaceId,thi.title,thi.casedesc,thi.url,thi.addBy,tu.userName from tb_version_http_interface thi  LEFT JOIN tb_user tu on thi.addBy = tu .loginName  where interfaceId = '%s' and versionName='%s'" % (getInterFaceDataSql,VersionService.getVersionName(request))

    print(sql)
    taskInterfaceListData = executeSqlGetDict(sql)
    response = render(request,"dubbo/task/SubPages/Task_Details_Select_interface_list_check_page.html", {"pageDatas":taskInterfaceListData})
    return response

def getTestCaseListDataForTask(request):
    id = request.GET.get("id")
    if VersionService.isCurrentVersion(request):
        taskDataModel = DubboTaskService.getTaskForId(id)
        taskData = dbModelToDict(taskDataModel)
        getTestCaseDataSql = taskData["taskTestcases"].replace(",","' union all select tht.id,tht.caseId,tht.title,tht.casedesc,tht.stepCount,tht.addBy,tu.userName from tb2_dubbo_testcase tht  LEFT JOIN tb_user tu on tht.addBy = tu .loginName where tht.caseId = '")
        sql = "select tht.id,tht.caseId,tht.title,tht.casedesc,tht.stepCount,tht.addBy,tu.userName from tb2_dubbo_testcase tht  LEFT JOIN tb_user tu on tht.addBy = tu .loginName where tht.caseId ='%s'" % getTestCaseDataSql
        print(sql)

    else:
        taskDataModel = DubboTaskService.getVersionTaskById(id)
        taskData = dbModelToDict(taskDataModel)
        getTestCaseDataSql = taskData["taskTestcases"].replace(",","' union all select tht.id,tht.caseId,tht.title,tht.casedesc,tht.stepCount,tht.addBy,tu.userName from tb_version_http_testcase tht  LEFT JOIN tb_user tu on tht.addBy = tu .loginName where tht.caseId = '")
        sql = "select tht.id,tht.caseId,tht.title,tht.casedesc,tht.stepCount,tht.addBy,tu.userName from tb_version_http_testcase tht  LEFT JOIN tb_user tu on tht.addBy = tu .loginName where tht.caseId ='%s' and versionName='%s'" % (getTestCaseDataSql,VersionService.getVersionName(request))

    taskTestCaseListData = executeSqlGetDict(sql)
    response = render(request,"dubbo/task/SubPages/Task_Details_Select_TestCase_list_check_page.html", {"pageDatas":taskTestCaseListData})
    return response


def getInterfeceListData(request):
    #根据任务执行结果
    id = request.GET.get("id")
    taskDataModel = DubboTaskExecuteService.findTaskRestltForId(id)
    taskData = dbModelToDict(taskDataModel)
    print(len(taskData))
    if taskDataModel.version == "CurrentVersion":
        getInterFaceDataSql = taskData["taskInterfaces"].replace(",","' union all select thi.id,thi.interfaceId,thi.title,thi.casedesc,thi.dubboSystem,thi.dubboService,thi.dubboMethod,thi.addBy,tu.userName from tb2_dubbo_interface thi  LEFT JOIN tb_user tu on thi.addBy = tu .loginName  where interfaceId = '")
        sql = "select thi.id,thi.interfaceId,thi.title,thi.casedesc,thi.dubboSystem,thi.dubboService,thi.dubboMethod,thi.addBy,tu.userName from tb2_dubbo_interface thi  LEFT JOIN tb_user tu on thi.addBy = tu .loginName  where interfaceId = '%s'" % getInterFaceDataSql
    else:
        getInterFaceDataSql = taskData["taskInterfaces"].replace(",","' union all select thi.id,thi.interfaceId,thi.title,thi.casedesc,thi.url,thi.addBy,tu.userName from tb_version_http_interface thi  LEFT JOIN tb_user tu on thi.addBy = tu .loginName  where interfaceId = '")
        sql = "select thi.id,thi.interfaceId,thi.title,thi.casedesc,thi.url,thi.addBy,tu.userName from tb_version_http_interface thi  LEFT JOIN tb_user tu on thi.addBy = tu .loginName  where interfaceId = '%s' and versionName='%s'" % (getInterFaceDataSql,taskDataModel.version)

    taskInterfaceListData = executeSqlGetDict(sql)
    response = render(request,"dubbo/task/SubPages/Task_Details_Select_interface_list_check_page.html", {"pageDatas":taskInterfaceListData})
    return response

def getTestCaseListData(request):
    id = request.GET.get("id")
    taskDataModel = DubboTaskExecuteService.findTaskRestltForId(id)
    taskData = dbModelToDict(taskDataModel)
    if taskDataModel.version == "CurrentVersion":
        getTestCaseDataSql = taskData["taskTestcases"].replace(",","' union all select tht.id,tht.caseId,tht.title,tht.casedesc,tht.stepCount,tht.addBy,tu.userName from tb2_dubbo_testcase tht  LEFT JOIN tb_user tu on tht.addBy = tu .loginName where tht.caseId = '")
        sql = "select tht.id,tht.caseId,tht.title,tht.casedesc,tht.stepCount,tht.addBy,tu.userName from tb2_dubbo_testcase tht  LEFT JOIN tb_user tu on tht.addBy = tu .loginName where tht.caseId ='%s'" % getTestCaseDataSql
    else:
        getTestCaseDataSql = taskData["taskTestcases"].replace(",","' union all select tht.id,tht.caseId,tht.title,tht.casedesc,tht.stepCount,tht.addBy,tu.userName from tb_version_http_testcase tht  LEFT JOIN tb_user tu on tht.addBy = tu .loginName where tht.caseId = '")
        sql = "select tht.id,tht.caseId,tht.title,tht.casedesc,tht.stepCount,tht.addBy,tu.userName from tb_version_http_testcase tht  LEFT JOIN tb_user tu on tht.addBy = tu .loginName where tht.caseId ='%s' and versionName='%s'" % (getTestCaseDataSql,taskDataModel.version)

    taskTestCaseListData = executeSqlGetDict(sql)
    response = render(request,"dubbo/task/SubPages/Task_Details_Select_TestCase_list_check_page.html", {"pageDatas":taskTestCaseListData})
    return response

def againRunTask(request):
    #历史版本再次执行取任务错误。
    id = request.GET.get("id")
    res = DubboTaskExecuteService.againRunTask(id,request.session.get("loginName"))
    if res == False:
        return ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, '任务已被删除').toJson()

    result = dbModelToDict(res)
    tcpin = '{"do":3,"TaskExecuteId":%s,"protocol":"DUBBO","TaskExecuteEnv":"%s","TaskId":"%s"}' % (result["id"], result["httpConfKey_id"], result["taskId"])
    RedisCache().set_data("%s_taskExecute_%s" % ("DUBBO", result["id"]), "0:0:0:0:0")
    RedisCache().set_data("%s_taskExecuteStatus_%s" % ("DUBBO", result["id"]), "1")
    retApiResult = send_tcp_request(tcpin)
    if retApiResult.code != ApiReturn.CODE_OK:
        RedisCache().del_data("%s_taskExecute_%s" % ("DUBBO", result["id"]))
        RedisCache().del_data("%s_taskExecuteStatus_%s" % ("DUBBO", result["id"]))
        DubboTaskExecuteService.updateFailExecute(result["id"],retApiResult.message)
        return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, retApiResult.message).toJson())
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())

def stopTaskRun(request):
    id = request.GET.get("id")
    try:
        DubboTaskExecuteService.stopTaskRun(id)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON,"请验证id正确性%s" % e).toJson())
    tcpin = '{"do":4,"TaskExecuteId":"%s","protocol":"DUBBO"}' % id
    retApiResult = send_tcp_request(tcpin)
    if retApiResult.code != ApiReturn.CODE_OK:
        return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, retApiResult.message).toJson())
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())

def taskRunAdd(request):
    if VersionService.isCurrentVersion(request):
        taskData = dbModelToDict(DubboTaskService.getTaskForTaskId(request.POST.get("taskId")))
        del taskData["taskId"]
        taskData["taskId"] = request.POST.get("taskId")
    else:
        taskData = dbModelToDict(DubboTaskService.getVersionTaskForTaskId(request.POST.get("taskId"),VersionService.getVersionName(request)))
        del taskData["taskId"]
        del taskData["versionName_id"]
        taskData["taskId"] = request.POST.get("taskId")

    del taskData["id"]
    taskData["protocol"] = request.POST.get("protocol")
    taskData["emailList"] = request.POST.get("emailList")
    taskData["addBy_id"] = request.session.get("loginName")
    taskData["isSaveHistory"] = request.POST.get("isSaveHistory")
    taskData["isSendEmail"] = request.POST.get("isSendEmail")
    taskData["execComments"] = request.POST.get("execComments")
    taskData["retryCount"] = request.POST.get("retryCount",0)
    taskData["execBy_id"] = request.session.get("loginName")
    taskData["version"] = VersionService.getVersionName(request)

    httpConfList = request.POST.get("httpConfKey_id").split(",")

    retmsg = 0

    for httpConfIndex in range(0,len(httpConfList)):
        taskData["httpConfKey_id"] = httpConfList[httpConfIndex]
        cres = DubboTaskExecuteService.taskRunAdd(taskData)
        addDataResult = dbModelToDict(cres)

        RedisCache().set_data("%s_taskExecute_%s" % ("DUBBO",addDataResult["id"]),"0:0:0:0:0",60*60*12)
        RedisCache().set_data("%s_taskExecuteStatus_%s" % ("DUBBO",addDataResult["id"]),"1",60*60*12)
        tcpin = '{"do":3,"TaskExecuteId":%s,"protocol":"DUBBO","TaskExecuteEnv":"%s","TaskId":"%s"}' % (
            addDataResult["id"], addDataResult["httpConfKey_id"], addDataResult["taskId"])
        retApiResult = send_tcp_request(tcpin)
        if retApiResult.code != ApiReturn.CODE_OK:
            retmsg = 1

    if retmsg == 1:
        addUserLog(request,"任务管理->任务执行->任务执行添加成功，但是执行服务出现异常，请联系管理员","FAIL")
        return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXCEPITON, "任务执行添加成功，但是执行服务出现异常，请联系管理员").toJson())
    addUserLog(request, "任务管理->任务执行->成功", "PASS")
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())

def getSelectExecuteStatus(request):
    sql = "SELECT testResult,count(*) as count from tb2_dubbo_task_execute GROUP BY testResult"
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK,body=executeSqlGetDict(sql,[])).toJson())