from django.shortcuts import render,HttpResponse
from all_models.models import *
from apps.common.func.WebFunc import *
import openpyxl,xlrd,json,platform
from apps.common.func.LanguageFunc import *
from urllib import parse
from apps.version_manage.services.common_service import VersionService
from apps.common.config import commonWebConfig
from apps.ui_test.services.ui_test import ui_test
logger = logging.getLogger("django")

@catch_exception_request
def ui_test_result_page(request):
    request.session['groupLevel1'] = groupLevel1
    request.session['groupLevel2'] = groupLevel2
    request.session['isReleaseEnv'] = isRelease

    langDict = getLangTextDict(request)
    context = {}
    if not isRelease:
        context["env"] = "test"
    context["uiTestResultPage"] = "current-page"
    context["userName"] = request.session.get("userName")
    context["checkBusinessLine"] = dbModelListToListDict(BusinessService.getAllBusinessLine())
    context["checkModules"] = dbModelListToListDict(ModulesService.getAllModules())
    #文本
    text = {}
    text["pageTitle"] = "UI执行信息查看"
    context["text"] = text
    context["page"] = 1
    # context["lang"] = getLangTextDict(request)
    addUserLog(request,"UI测试->查看文件->页面展示->成功","PASS")
    return render(request,"ui_test/ui_file/ui_check.html",context)

def ui_test_resultListCheck(request):
    # ui_test.updateUiTestList()
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "UI测试->查看文件->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))

    orderBy = request.POST.get("orderBy")
    if isSqlInjectable(orderBy):
        addUserLog(request, "UI测试->查看文件->获取数据->SQL注入检测时发现查询条件非法", "FAIL")
        return HttpResponse("<script>alert('查询条件非法');</script>")

    #根据版本判断应该从哪个表里取数据 王吉亮添加于20180224
    if VersionService.isCurrentVersion(request):
        tbName = "tb_http_interface"
        versionCondition = ""
    else:
        tbName = "tb_version_http_interface"
        versionCondition = "and versionName='%s'" % request.session.get("version")

    # execSql = "SELECT i.*,u.userName,mu.userName modByName from %s i LEFT JOIN tb_user mu ON i.modBy = mu.loginName LEFT JOIN tb_user u ON i.addBy = u.loginName LEFT JOIN  tb_modules m ON i.moduleId = m.id LEFT JOIN tb_business_line b ON i.businessLineId = b.id WHERE 1=1 and i.state=1 %s" % (tbName,versionCondition)
    execSql = "SELECT i.*,u.userName from tb_ui_test_execute i LEFT JOIN tb_user u ON i.addBy = u.loginName WHERE  (i.execStatus in (1,2)) OR (i.state = 1 "
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
    execSql += """) ORDER BY %s""" % orderBy

    context = pagination(sqlStr=execSql,attrList=checkList,page=page,pageNum=commonWebConfig.interFacePageNum)
    for contextIndex in context["pageDatas"]:
        contextIndex["businessLineName"] = TbBusinessLine.objects.get(id=contextIndex["businessLineId"]).bussinessLineName
        contextIndex["moduleName"] = TbModules.objects.get(id=contextIndex["moduleId"]).moduleName

        if contextIndex["execStatus"] == 2:
            execProgressString = contextIndex["execProgressString"].replace("\n","")
            if isJson(execProgressString):
                progressDict = json.loads(execProgressString)
                contextIndex["progressDict"] = progressDict
                contextIndex["percentage"] = "%.2f" % (
                    (progressDict["totalTestcaseStepCount"] - progressDict["realNotrunTestcaseStepCount"]) / progressDict["totalTestcaseStepCount"] * 100)
                if progressDict["failTestcaseStepCount"] >= 1:
                    contextIndex["execPercent"] = "FAIL"
                elif progressDict["warningTestcaseStepCount"] >= 1:
                    contextIndex["execPercent"] = "WARNING"
                else:
                    contextIndex["execPercent"] = "PASS"

                # contextIndex["execUser"]
            else:
                progressDict = {}
                contextIndex["progressDict"] = progressDict
                contextIndex["percentage"] = "%.2f" % 0
                contextIndex["execPercent"] = "PASS"

        if contextIndex["testResult"] == "" or contextIndex["testResult"] == "NOTRUN":
            contextIndex["testResult"] = "-"
        contextIndex["httpConfKeyName"] = TbConfigHttp.objects.get(httpConfKey=contextIndex["httpConfKey"]).alias
        contextIndex["execTakeTime"] = "%.2f" % float(contextIndex["execTakeTime"])
        try:
            contextIndex["fileAddByName"] = TbUser.objects.get(loginName=contextIndex["fileAddBy"]).userName
        except Exception as e:
            logger.error("UI任务执行列表 查不到用户名 参数为%s" % contextIndex["fileAddBy"])
            contextIndex["fileAddByName"] = contextIndex["fileAddBy"]
    response = render(request, "ui_test/ui_file/subPages/ui_test_result_list_page.html",context)
    addUserLog(request, "UI测试->查看文件->获取数据->成功", "PASS")
    return response



def ui_report(request):

    realFile = "%s%s" % (BASE_DIR.replace("\\", "/"), "/ui_test_reports/%s" % request.GET.get())
    print(realFile)
    fileContent = open(realFile, "r", encoding="utf-8")
    return HttpResponse(fileContent)

def cancelExecuteUiTask(request):
    execId = request.GET.get("id","0").strip()
    if isInt(execId) and int(execId) > 0:
        execUiTask = TbUITestExecute.objects.filter(id=int(execId))
        if execUiTask:
            execUiTask = execUiTask[0]
            execProgressString = execUiTask.execProgressString.strip()
            if execProgressString.startswith("{") and isJson(execProgressString):
                execProgressDict = json.loads(execProgressString)
                if str(execProgressDict['whetherCanCancelTask']) == "1":
                    execUiTask.execStatus = 10
                    execUiTask.save(force_update=True)
                    send_tcp_request_to_uiport("""{"do":32,"UITaskExecuteId":%s}""" % execId)
                    return HttpResponse("""{"code":10000,"msg":"任务%s取消成功！"}""" % execId)
                else:
                    return HttpResponse("""{"code":10002,"msg":"任务%s取消失败！正在初始化driver，请稍后再试。"}""" % execId)
            else:
                execUiTask.execStatus = 10
                execUiTask.save(force_update=True)
                send_tcp_request_to_uiport("""{"do":32,"UITaskExecuteId":%s}""" % execId)
                return HttpResponse("""{"code":10000,"msg":"任务%s取消成功！"}""" % execId)
        else:
            return HttpResponse("""{"code":10001,"msg":"任务%s取消失败！没有找到此任务。"}""" % execId)
    else:
        return HttpResponse("""{"code":10001,"msg":"任务%s取消失败！没有找到此任务。"}""" % execId)

def checkUiTestLog(request):
    logDir = request.GET.get("logDir")
    completeDir = "%s%s" % (BASE_DIR.replace("\\", "/"),logDir)
    if os.path.isfile(completeDir) and logDir.endswith("/report.log"):
        file_object = open(completeDir, 'r')
        try:
            file_context = file_object.read()
        finally:
            file_object.close()
    else:
        file_context = "未生成log文件"

    return HttpResponse(file_context.replace("\n","<br>"))

def againRunTask(request):
    id = request.POST.get("id")
    taskExecuteData = TbUITestExecute.objects.filter(id=id)
    if len(taskExecuteData) == 0:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message="任务执行数据不存在").toJson())
    taskExecuteDict = dbModelToDict(taskExecuteData[0])
    taskData = TbUiTaskSimple.objects.filter(taskId=taskExecuteDict["taskId"])
    if len(taskData) == 0:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="任务不存在").toJson())
    runtaskDict = dbModelToDict(taskData[0])
    print(runtaskDict)
    tbModel = TbUITestExecute()
    # 基本信息
    tbModel.taskId = runtaskDict["taskId"]
    tbModel.title = runtaskDict["title"]
    tbModel.fileName = runtaskDict["fileName"]
    tbModel.sheetName = runtaskDict["sheetName"]
    tbModel.sourceGroup = runtaskDict["sourceGroup"]
    tbModel.fileAddBy = runtaskDict["fileAddBy"]
    tbModel.businessLineId = runtaskDict["businessLineId"]
    tbModel.moduleId = runtaskDict["moduleId"]
    tbModel.addBy = request.session.get("loginName")
    tbModel.httpConfKey = taskExecuteDict["httpConfKey"]
    tbModel.execComments = taskExecuteDict["execComments"]
    tbModel.isSendEmail = taskExecuteDict["isSendEmail"]
    tbModel.emailList = taskExecuteDict["emailList"]
    tbModel.save()
    saveId = tbModel.id
    tcpStr = '{"do":31,"UITaskExecuteId":"%s"}' % saveId
    print(tcpStr)
    retApiResult = send_tcp_request_to_uiport(tcpStr)
    if retApiResult.code != ApiReturn.CODE_OK:
        tbModel.execStatus = 4
        tbModel.testResult = "EXCEPTION"
        print(str(retApiResult.code) + ":" + retApiResult.message)
        tbModel.testResultMessage = str(retApiResult.code) + ":" + retApiResult.message
        tbModel.save()
        addUserLog(request, "单接口管理->接口调试->发送TCP请求->失败，原因\n%s" % retApiResult.toJson(), "FAIL")
        return HttpResponse(retApiResult.toJson(ApiReturn.CODE_WARNING))
    else:
        addUserLog(request, "单接口管理->接口调试->发送TCP请求->成功", "PASS")
        return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
