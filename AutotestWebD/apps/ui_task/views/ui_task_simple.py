from django.shortcuts import render,HttpResponse
from all_models.models import *
from apps.common.func.WebFunc import *
import openpyxl,xlrd,json,platform
from django.http import StreamingHttpResponse

from urllib import parse

from apps.ui_task.services.PageObjectService import PageObjectService
from apps.version_manage.services.common_service import VersionService
from apps.common.config import commonWebConfig
logger = logging.getLogger("django")

def uiAddSimpleTaskPage(request):
    context = {}
    text = {}
    text["pageTitle"] = "UI测试任务"
    text["subPageTitle"] = "用例文件查看"
    context["text"] = text
    context["option"] = "add"
    context["uiAddSimpleTaskPage"] = "current-page"
    context["businessLine"] = dbModelListToListDict(BusinessService.getAllBusinessLine())
    return render(request,"ui_test/ui_task/ui_simple_task.html",context)

def saveSimpleTask(request):
    #<QueryDict: {'sheetNameList': ['["OnlyWebCase"]'], 'fileName': ['CaseAndroid.xls'], 'userName': ['wangjl01'], 'businessLineId': ['1'], 'moduleId': ['117'], 'sourceList[]': ['安卓App', '苹果App'], 'taskTitle': ['asdfasdfas'], 'taskDesc': ['zzzzz']}>
    taskId = request.POST.get("taskId","")
    sheetNameList = request.POST.get("sheetNameList")
    fileName = request.POST.get("fileName")
    fileAddBy = request.POST.get("userName")
    businessLineId = request.POST.get("businessLineId")
    moduleId = request.POST.get("moduleId")
    sourceList = request.POST.get("sourceList")
    taskTitle = request.POST.get("taskTitle")
    taskDesc = request.POST.get("taskDesc")
    emailList = request.POST.get("emailList")
    print("emailList:", emailList)
    sheetnameStr = ""
    for tmpSheetName in eval(sheetNameList):
        sheetnameStr += "%s," % tmpSheetName
    sheetnameStr = sheetnameStr[:-1]
    if taskId:
        uiSimpleTask = TbUiTaskSimple.objects.get(taskId=taskId)
    else:
        uiSimpleTask = TbUiTaskSimple()
    uiSimpleTask.title = taskTitle
    uiSimpleTask.taskdesc = taskDesc
    uiSimpleTask.businessLineId = int(businessLineId)
    uiSimpleTask.moduleId = int(moduleId)
    uiSimpleTask.sourceGroup = sourceList
    uiSimpleTask.fileAddBy = fileAddBy
    uiSimpleTask.sheetName = sheetnameStr
    uiSimpleTask.fileName = fileName
    uiSimpleTask.emailList = emailList
    uiSimpleTask.addBy_id = request.session.get("loginName")
    uiSimpleTask.save()
    uiSimpleTask.taskId = "UI_TASK_%d" % uiSimpleTask.id
    uiSimpleTask.save()
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())

def show_ui_simple_task_page(request):
    request.session['groupLevel1'] = groupLevel1
    request.session['groupLevel2'] = groupLevel2
    request.session['isReleaseEnv'] = isRelease

    context = {}
    if not isRelease:
        context["env"] = "test"
    context["uiShowSimpleTaskPage"] = "current-page"
    context["userName"] = request.session.get("userName")
    context["checkBusinessLine"] = dbModelListToListDict(BusinessService.getAllBusinessLine())
    context["checkModules"] = dbModelListToListDict(ModulesService.getAllModules())

    #文本
    text = {}
    text["pageTitle"] = "UI任务查看"
    context["text"] = text
    context["page"] = 1
    addUserLog(request,"UI测试->查看任务->页面展示->成功","PASS")
    return render(request,"ui_test/ui_task/show_ui_simple_task_page.html",context)

def show_ui_test_resultListCheck(request):
    # ui_test.updateUiTestList()
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "UI测试->查看任务->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))

    orderBy = request.POST.get("orderBy")
    if isSqlInjectable(orderBy):
        addUserLog(request, "UI测试->查看文件->获取数据->SQL注入检测时发现查询条件非法", "FAIL")
        return HttpResponse("<script>alert('查询条件非法');</script>")

    execSql = "SELECT i.*,u.userName from tb_ui_task_simple i LEFT JOIN tb_user u ON i.addBy = u.loginName WHERE i.state = 1 "
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

    context = pagination(sqlStr=execSql,attrList=checkList,page=page,pageNum=commonWebConfig.interFacePageNum)

    context["myAppPackages"] = dbModelListToListDict(TbUiPackage.objects.filter(addBy=request.session.get("loginName"),state=1))
    context["envModules"] = HttpConfService.queryUIRunHttpConfSort(request)
    for contextIndex in context["pageDatas"]:
        contextIndex["businessLineName"] = TbBusinessLine.objects.get(id=contextIndex["businessLineId"]).bussinessLineName
        contextIndex["moduleName"] = TbModules.objects.get(id=contextIndex["moduleId"]).moduleName
        contextIndex["addByName"] = TbUser.objects.get(loginName=contextIndex["addBy"]).userName
        contextIndex["fileAddByName"] = TbUser.objects.get(loginName=contextIndex["fileAddBy"]).userName

    response = render(request, "ui_test/ui_task/subPages/ui_simple_task_pagelist.html",context)
    addUserLog(request, "UI测试->查看任务->获取数据->成功", "PASS")
    return response

def executeSimpleTask(request):
    #<QueryDict: {'sheetNameList': ['["OnlyWebCase"]'], 'fileName': ['CaseAndroid.xls'], 'userName': ['wangjl01'], 'businessLineId': ['1'], 'moduleId': ['117'], 'sourceList[]': ['安卓App', '苹果App'], 'taskTitle': ['asdfasdfas'], 'taskDesc': ['zzzzz']}>
    taskId = request.POST.get("taskId")
    uiTask = TbUiTaskSimple.objects.filter(taskId = taskId).all()
    if uiTask:
        uiTask = uiTask[0]
        envList = eval(request.POST.get("envList"))
        if len(envList) == 0:
            return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="至少选择一个环境！").toJson())
        packageList = json.loads(request.POST.get("packageList"))
        if len(packageList) == 0:
            return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="至少选择一个app包！").toJson())
        isSendEmail = request.POST.get("isSendEmail")
        emailList = json.loads(request.POST.get("emailList"))
        for tmpEnv in envList:
            for tmpPackage in packageList:
                tmpUITaskExecute = TbUITestExecute()
                tmpUITaskExecute.taskId = uiTask.taskId
                tmpUITaskExecute.title = uiTask.title
                tmpUITaskExecute.taskdesc = uiTask.taskdesc
                tmpUITaskExecute.businessLineId = uiTask.businessLineId
                tmpUITaskExecute.moduleId = uiTask.moduleId
                tmpUITaskExecute.sourceGroup = uiTask.sourceGroup
                tmpUITaskExecute.tasklevel = uiTask.tasklevel

                tmpUITaskExecute.fileAddBy = uiTask.fileAddBy
                tmpUITaskExecute.fileName = uiTask.fileName
                tmpUITaskExecute.sheetName = uiTask.sheetName
                tmpUITaskExecute.emailList = emailList
                tmpUITaskExecute.isSendEmail = isSendEmail
                tmpUITaskExecute.packageId = tmpPackage
                tmpUITaskExecute.httpConfKey = tmpEnv
                tmpUITaskExecute.reportDir = ""
                tmpUITaskExecute.execStatus = 1
                tmpUITaskExecute.addBy = request.session.get("loginName")
                tmpUITaskExecute.save(force_insert=True)
                tcpStr = '{"do":31,"UITaskExecuteId":"%s"}' % tmpUITaskExecute.id

                retApi = send_tcp_request_to_uiport(tcpStr)
                if retApi.code != 10000:
                    return HttpResponse(retApi.toJson())
        return HttpResponse(ApiReturn(ApiReturn.CODE_OK,message=uiTask.title).toJson())
    else:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR,message="没有找到任务，错误的任务id[%s]" % taskId).toJson())

def ui_operationTask(request):
    taskId = request.GET.get("taskId","")
    option = request.GET.get("option","")
    if taskId == "":
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message="缺少taskId参数").toJson())
    try:
        taskData = TbUiTaskSimple.objects.filter(state=1).get(taskId=taskId)
    except Exception as e:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message="taskId查不到数据").toJson())
    text = {}
    context = {}
    context["uiAddSimpleTaskPage"] = "current-page"
    if option == "copy":
        text["pageTitle"] = "拷贝任务"
        text["subPageTitle"] = "UI任务拷贝"
    elif option == "edit":
        text["pageTitle"] = "编辑任务"
        text["subPageTitle"] = "UI任务编辑"
    elif option == "check":
        text["pageTitle"] = "查看任务"
        text["subPageTitle"] = "UI任务查看"
    else:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message="option参数:值错误").toJson())
    context["text"] = text
    context["option"] = option
    context["taskId"] = taskId
    context["businessLine"] = dbModelListToListDict(BusinessService.getAllBusinessLine())
    return render(request,"ui_test/ui_task/ui_simple_task.html",context)

def getTaskForTaskId(request):

    taskId = request.POST.get("taskId","")
    if taskId == "":
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="缺少taskId参数").toJson())
    try:
        taskData = TbUiTaskSimple.objects.filter(state=1).get(taskId=taskId)
    except Exception as e:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message="taskId查不到数据").toJson())

    context = dbModelToDict(taskData)
    return HttpResponse(ApiReturn(body=context).toJson())

def delSimpleTask(request):
    taskId = request.GET.get("taskId","")
    if taskId == "":
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="缺少taskId参数").toJson())
    try:
        taskData = TbUiTaskSimple.objects.filter(state=1).get(taskId=taskId)
    except Exception as e:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message="taskId查不到数据").toJson())
    taskData.state = 0
    taskData.save()
    return HttpResponse(ApiReturn().toJson())

def getTaskRunDetailsForTaskId(request):
    taskId = request.GET.get("taskId")
    taskDataDict = {}
    taskDataDict["taskId"] = taskId
    uiTask = TbUiTaskSimple.objects.filter(taskId=taskId, state=1)
    uiTaskLists = dbModelListToListDict(uiTask)
    if len(uiTaskLists) !=0 :
        uiTaskList = uiTaskLists[0]
        taskDataDict["title"] = uiTaskList["title"]
        taskDataDict["taskdesc"] = uiTaskList["taskdesc"]
        taskDataDict["addBy"] = uiTaskList["addBy_id"]
        taskDataDict["addTime"] = uiTaskList["addTime"]
        taskDataDict["modTime"] = uiTaskList["modTime"]
        taskDataDict["emailList"] = uiTaskList["emailList"]
    context = {}
    context["taskData"] = taskDataDict
    context["envModules"] = HttpConfService.queryUIRunHttpConfSort(request)
    context["myAppPackages"] = dbModelListToListDict(TbUiPackage.objects.filter(addBy=request.session.get("loginName"), state=1))
    return render(request,"ui_test/ui_task/subPages/ui_task_Run_DetailsPage.html",context)


def addPageObject(request):
    pageObjectDataRequest = json.loads(request.POST.get("pageObjectData"))
    print("pageObjectDataRequest:", pageObjectDataRequest)
    logger.info("addPageObject %s" % request.POST.get("pageObjectData"))
    poKey = pageObjectDataRequest["POKey"]
    poTitle = pageObjectDataRequest["POTitle"]
    poDesc = pageObjectDataRequest["PODesc"]
    addBy =  request.session.get("loginName")
    print("addBy:", addBy)
    pageObjectResult = TbUiPageObject.objects.filter(poKey=poKey)
    if len(pageObjectResult) == 0:
        pageObject = TbUiPageObject()
        pageObject.poKey = poKey
        pageObject.poTitle = poTitle
        pageObject.poDesc = poDesc
        pageObject.addBy = addBy
        pageObject.state = 1
        pageObject.save()
        return HttpResponse(ApiReturn().toJson())
    else:
        if pageObjectResult[0].state == 0:
            pageObjectResult[0].state = 1
            pageObjectResult[0].poTitle = poTitle
            pageObjectResult[0].poDesc = poDesc
            pageObjectResult[0].addBy = addBy
            pageObjectResult[0].save()
            return HttpResponse(ApiReturn().toJson())
        else:
            logger.info("addPageObject pageObject添加失败")
            return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="pageObject添加失败,请检查账号是否重复").toJson())


def getPageObject(request):
    context = {}
    pageObjectList = []
    pageObjectList.extend(dbModelListToListDict(TbUiPageObject.objects.filter()))
    pageObjectSorted = sorted(pageObjectList, key=lambda pageObject: pageObject["id"], reverse=True)
    context["pageDatas"] = sorted(pageObjectSorted, key=lambda pageObject: pageObject["state"], reverse=True)
    response = render(request, "ui_main/page_object/SubPages/page_object_add_subpage.html",context)
    return response


def getPageObjectForId(request):
    pageObjectId = request.POST.get("pageObjectId")
    try:
        pageObjectData = TbUiPageObject.objects.get(id=pageObjectId)
    except Exception as e:
        message = "pageObject查询出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())
    return HttpResponse(ApiReturn(body=dbModelToDict(pageObjectData)).toJson())


def editPageObject(request):
    try:
        requestDict =json.loads(request.POST.get("pageObjectData"))
        requestDict["modTime"] = datetime.datetime.now()
        PageObjectService.updatePageObject(requestDict)
    except Exception as e:
        print(traceback.format_exc())
        message = "编辑pageObject发生异常 %s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())

    return HttpResponse(ApiReturn().toJson())


def delPageObject(request):
    pageObjectId = request.POST.get("pageObjectId", "")
    if not pageObjectId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="pageObjectId参数错误").toJson())
    try:
        pageObjectData = TbUiPageObject.objects.get(state=1, id=pageObjectId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="pageObjectId查询错误 %s" % e).toJson())
    pageObjectData.state = 0
    pageObjectData.save()
    return HttpResponse(ApiReturn().toJson())

def resetPageObject(request):
    pageObjectId = request.POST.get("pageObjectId", "")
    if not pageObjectId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="pageObjectId参数错误").toJson())
    try:
        pageObjectData = TbUiPageObject.objects.get(state=0, id=pageObjectId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="pageObjectId查询错误 %s" % e).toJson())
    pageObjectData.state = 1
    pageObjectData.save()

    return HttpResponse(ApiReturn().toJson())