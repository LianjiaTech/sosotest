from apps.config.services.serviceConfService import ServiceConfService
from apps.config.services.http_confService import HttpConfService
from apps.config.services.businessLineService import BusinessService
from apps.config.services.modulesService import ModulesService
from apps.config.services.sourceService import SourceService
from apps.config.services.uriService import UriService
from apps.interface.services.HTTP_interfaceService import HTTP_interfaceService
from apps.test_case.services.HTTP_test_case_stepService import HTTP_test_case_stepService
from apps.test_case.services.HTTP_test_caseService import HTTP_test_caseService
from apps.src_file_analyze.services.src_file_analyzeService import SrcFileAnalyzeService
from apps.common.func.CommonFunc import *
from all_models.models import *
import re
import functools
from django.shortcuts import render,HttpResponse
userlog = logging.getLogger("userlog")

def getServiceConf(request):
    context = {}
    serviceConf = ServiceConfService.queryServiceConfSort(request)
    context["serviceCount"] = len(serviceConf)
    serviceIncludeHTTPConf = []
    # serviceList = []
    # 显示前置和后置变量的title
    for i in range(0, len(serviceConf)):
        # serviceList.append(serviceConf[i]["serviceConfKey"])
        serviceIncludeHTTPConf.append(HttpConfService.getServiceIncludHttpConf(serviceConf[i]["serviceConfKey"]))
        httpConfStrList = ""
        for j in range(0, len(serviceIncludeHTTPConf[i])):
            if j == 0:
                httpConfStrList = "包含的环境:%s" % serviceIncludeHTTPConf[i][j]["alias"]
                continue
            httpConfStrList = "%s,%s" % (httpConfStrList, serviceIncludeHTTPConf[i][j]["alias"])
        serviceConf[i]["serviceIncludeHTTPConf"] = httpConfStrList
    context["service"] = serviceConf
    return context

def getHttpConfForUI():
    context = {}
    serviceConf = HttpConfService.getHttpConfForUI()
    context["httpCount"] = len(serviceConf)
    context["httpConfList"] = serviceConf
    return context

def getConfigs(request):
    context = {}
    context["businessLine"] = BusinessService.getBusiness()
    context["modules"] = ModulesService.getModules()
    context["source"] = SourceService.getAllSource()
    context["uri"] = UriService.getUri(request)

    return context

def syncDelTipList(interface):
    stepList = dbModelListToListDict(HTTP_test_case_stepService.getSyncStepFromInterfaceIdNum(interface["interfaceId"]))
    testCaseList = []
    for index in range(0, len(stepList)):
        testCaseList.append(stepList[index]["caseId_id"])
    testCaseList = list(set(testCaseList))
    return {"list":testCaseList,"num":len(testCaseList)}

def syncVersionDelTipList(interface,versionName):
    stepList = dbModelListToListDict(HTTP_test_case_stepService.getVersionSyncStepFromInterfaceIdNum(interface["interfaceId"],versionName))
    testCaseList = []
    for index in range(0, len(stepList)):
        testCaseList.append(stepList[index]["caseId"])
    testCaseList = list(set(testCaseList))
    return {"list":testCaseList,"num":len(testCaseList)}

def syncDel(request,interface):
    stepList = dbModelListToListDict(HTTP_test_case_stepService.getSyncStepFromInterfaceIdNum(interface["interfaceId"]))
    for index in range(0, len(stepList)):
        if request.session.get("loginName") != stepList[index]["addBy_id"]:
            userChangeLogInterfaceToTestCaseStepChange(request,interface,stepList[index])
        stepList[index]["fromInterfaceId"] = ""
        stepList[index]["isSync"] = 0
        stepList[index]["modTime"] = datetime.datetime.now()
        HTTP_test_case_stepService.updateTestCaseStep(request,stepList[index]["id"], stepList[index])

def syncVersionDel(request,interface,versionName):
    stepList = dbModelListToListDict(HTTP_test_case_stepService.getVersionSyncStepFromInterfaceIdNum(interface["interfaceId"],versionName))
    for index in range(0, len(stepList)):
        if request.session.get("loginName") != stepList[index]["addBy_id"]:
            userChangeLogInterfaceToTestCaseStepChange(request, interface, stepList[index])
        stepList[index]["fromInterfaceId"] = ""
        stepList[index]["isSync"] = 0
        stepList[index]["modTime"] = datetime.datetime.now()
        HTTP_test_case_stepService.updateVersionTestCaseStep(stepList[index]["id"], stepList[index])

def syncInterfaceToTestcaseStep(request,interface):
    stepList = dbModelListToListDict(HTTP_test_case_stepService.getSyncStepFromInterfaceId(interface["interfaceId"]))
    for index in range(0,len(stepList)):
        if request.session.get("loginName") != stepList[index]["addBy_id"]:
            userChangeLogInterfaceToTestCaseStepChange(request, interface, stepList[index])
        stepList[index]["stepDesc"] = interface["casedesc"]
        stepList[index]["varsPre"] = interface["varsPre"]
        stepList[index]["uri"] = interface["uri"]
        stepList[index]["customUri"] = interface["customUri"]
        stepList[index]["useCustomUri"] = interface["useCustomUri"]
        stepList[index]["urlRedirect"] = interface["urlRedirect"]
        stepList[index]["method"] = interface["method"]
        stepList[index]["header"] = interface["header"]
        stepList[index]["url"] = interface["url"]
        stepList[index]["params"] = interface["params"]
        stepList[index]["varsPost"] = interface["varsPost"]
        stepList[index]["timeout"] = interface["timeout"]
        stepList[index]["performanceTime"] = interface["performanceTime"]
        stepList[index]["modBy"] = interface["modBy"]
        stepList[index]["modTime"] = datetime.datetime.now()
        stepList[index]["businessLineId_id"] = interface["businessLineId_id"]
        stepList[index]["moduleId_id"] = interface["moduleId_id"]
        stepList[index]["bodyContent"] = interface["bodyContent"]
        stepList[index]["bodyType"] = interface["bodyType"]
        stepList[index]["sourceId_id"] = interface["sourceId_id"]
        HTTP_test_case_stepService.updateTestCaseStep(request,stepList[index]["id"],stepList[index])

def syncVersionInterfaceToTestcaseStep(request,interface,versionName):
    stepList = dbModelListToListDict(HTTP_test_case_stepService.getVersionSyncStepFromInterfaceId(interface["interfaceId"],versionName))
    for index in range(0,len(stepList)):
        if request.session.get("loginName") != stepList[index]["addBy_id"]:
            userChangeLogInterfaceToTestCaseStepChange(request, interface, stepList[index])
        stepList[index]["stepDesc"] = interface["casedesc"]
        stepList[index]["varsPre"] = interface["varsPre"]
        stepList[index]["uri"] = interface["uri"]
        stepList[index]["customUri"] = interface["customUri"]
        stepList[index]["useCustomUri"] = interface["useCustomUri"]
        stepList[index]["urlRedirect"] = interface["urlRedirect"]
        stepList[index]["method"] = interface["method"]
        stepList[index]["header"] = interface["header"]
        stepList[index]["url"] = interface["url"]
        stepList[index]["params"] = interface["params"]
        stepList[index]["varsPost"] = interface["varsPost"]
        stepList[index]["timeout"] = interface["timeout"]
        stepList[index]["performanceTime"] = interface["performanceTime"]
        stepList[index]["modBy"] = interface["modBy"]
        stepList[index]["modTime"] = datetime.datetime.now()
        stepList[index]["businessLineId_id"] = interface["businessLineId_id"]
        stepList[index]["moduleId_id"] = interface["moduleId_id"]
        stepList[index]["bodyContent"] = interface["bodyContent"]
        stepList[index]["bodyType"] = interface["bodyType"]
        stepList[index]["sourceId_id"] = interface["sourceId_id"]
        stepList[index]["versionName_id"] = interface["versionName_id"]
        HTTP_test_case_stepService.updateVersionTestCaseStep(stepList[index]["id"],stepList[index])


def syncTestCaseStepFromInterfaceId(request,caseId):
    stepList = dbModelListToListDict(HTTP_test_case_stepService.getSyncStep(caseId))
    failTestCaseList = []
    for index in range(0,len(stepList)):
        interface = dbModelToDict(HTTP_interfaceService.getInterfaceForInterfaceId(stepList[index]["fromInterfaceId"]))
        if interface["state"] == 0:
            failTestCaseList.append(stepList[index]["title"])
            continue
        stepList[index]["stepDesc"] = interface["casedesc"]
        stepList[index]["varsPre"] = interface["varsPre"]
        stepList[index]["uri"] = interface["uri"]
        stepList[index]["method"] = interface["method"]
        stepList[index]["header"] = interface["header"]
        stepList[index]["customUri"] = interface["customUri"]
        stepList[index]["useCustomUri"] = interface["useCustomUri"]
        stepList[index]["url"] = interface["url"]
        stepList[index]["params"] = interface["params"]
        stepList[index]["varsPost"] = interface["varsPost"]
        stepList[index]["timeout"] = interface["timeout"]
        stepList[index]["performanceTime"] = interface["performanceTime"]
        stepList[index]["modBy"] = interface["modBy"]
        stepList[index]["modTime"] = datetime.datetime.now()
        stepList[index]["businessLineId_id"] = interface["businessLineId_id"]
        stepList[index]["moduleId_id"] = interface["moduleId_id"]
        stepList[index]["bodyContent"] = interface["bodyContent"]
        stepList[index]["bodyType"] = interface["bodyType"]
        stepList[index]["sourceId_id"] = interface["sourceId_id"]
        HTTP_test_case_stepService.updateTestCaseStep(request,stepList[index]["id"], stepList[index])
    if failTestCaseList == []:
        return True
    else:
        return failTestCaseList

def syncVersionTestCaseStepFromInterfaceId(caseId,versionName):
    stepList = dbModelListToListDict(HTTP_test_case_stepService.getVersionSyncStep(caseId,versionName))
    failTestCaseList = []
    for index in range(0,len(stepList)):
        interface = dbModelToDict(HTTP_interfaceService.getVersionInterfaceForInterfaceId(stepList[index]["fromInterfaceId"],versionName))
        if interface["state"] == 0:
            failTestCaseList.append(stepList[index]["title"])
            continue
        stepList[index]["stepDesc"] = interface["casedesc"]
        stepList[index]["varsPre"] = interface["varsPre"]
        stepList[index]["uri"] = interface["uri"]
        stepList[index]["method"] = interface["method"]
        stepList[index]["header"] = interface["header"]
        stepList[index]["url"] = interface["url"]
        stepList[index]["params"] = interface["params"]
        stepList[index]["varsPost"] = interface["varsPost"]
        stepList[index]["timeout"] = interface["timeout"]
        stepList[index]["performanceTime"] = interface["performanceTime"]
        stepList[index]["modBy"] = interface["modBy"]
        stepList[index]["modTime"] = datetime.datetime.now()
        stepList[index]["customUri"] = interface["customUri"]
        stepList[index]["useCustomUri"] = interface["useCustomUri"]
        stepList[index]["businessLineId_id"] = interface["businessLineId_id"]
        stepList[index]["moduleId_id"] = interface["moduleId_id"]
        stepList[index]["bodyContent"] = interface["bodyContent"]
        stepList[index]["bodyType"] = interface["bodyType"]
        stepList[index]["sourceId_id"] = interface["sourceId_id"]
        stepList[index]["versionName_id"] = interface["versionName_id"]
        HTTP_test_case_stepService.updateVersionTestCaseStep(stepList[index]["id"], stepList[index])
    if failTestCaseList == []:
        return True
    else:
        return failTestCaseList

def srcFileIsFile(fileRealPath):
    if len(fileRealPath) < 6:
        return 0
    if fileRealPath.endswith(".java"):
        return 1
    else:
        return 2

def createSqlDict(checkArr,orderBy,sql,afterSql):
    execSql = sql
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        elif key == "addBy":
            checkList.append("%%%s%%" % checkArr[key])
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and (i.addBy LIKE %s or u.userName LIKE %s) """
            continue
        elif key == "businessLine":
            checkList.append("%s" % checkArr[key])
            execSql += """ and b.bussinessLineName = %s """
            continue
        elif key == "module":
            checkList.append("%s" % checkArr[key])
            execSql += """ and m.moduleName = %s """
            continue

    execSql += """ %s """ % afterSql
    if orderBy != "":
        execSql += """ ORDER BY %s """ % orderBy
    return executeSqlGetDict(sqlStr=execSql, attrList=checkList)

def addUserLog(request,optionDesc,optionResult,isToDb = False):
    ip = ""
    if 'HTTP_X_FORWARDED_FOR' in request.META.keys():
        ip = request.META['HTTP_X_FORWARDED_FOR']
    elif 'REMOTE_ADDR' in request.META.keys():
        ip = request.META['REMOTE_ADDR']
    else:
        ip = "unknown"
    userlog.info("%s[%s]->%s->%s->%s->%s" %
         (request.session.get('userName', "未知用户"),
          request.session.get('loginName', "unknown"),
          request.get_full_path().split("?")[0],
          optionDesc,
          optionResult,
          ip))
    if isToDb:
        ulog = TbUserLog()
        ulog.loginName = request.session.get('loginName',"unknown")
        ulog.userName = request.session.get('userName',"未知用户")
        ulog.operationUrl = request.get_full_path().split("?")[0]
        ulog.operationDesc = optionDesc
        ulog.operationResult = optionResult
        ulog.fromHostIp = ip
        ulog.save(force_insert=True)


def checkUrl(url):
    newUrl = url
    if " " in newUrl:
        newUrl = newUrl.replace(" ","")
    if "{" in url:
        newUrl = re.sub('\{.*?\}',"",newUrl)
    if "$VAR[" in url:
        newUrl = re.sub('\$VAR\[.*?\]',"",newUrl)
    if "$GVAR[" in url:
        newUrl = re.sub('\$GVAR\[.*?\]',"",newUrl)
    return newUrl

def getAllApiCountsNumConfig():
    messageDict = {}
    messageDict["allCount"] = 0

    for root, dirs, files in os.walk(srcRootDir):
        for tmpFile in files:
            for tmpLastRoleName in srcFoldersLastFileNameRole:
                if tmpFile.endswith(tmpLastRoleName):
                    realPath = (root + os.sep + tmpFile).replace("\\","/")
                    fileRealPath = realPath.split(srcRootDir)[1].replace("\\","/")
                    tmpCount  = SrcFileAnalyzeService.getFileApisCountNum(fileRealPath)
                    messageDict["allCount"] += tmpCount
                    messageDict[fileRealPath] = tmpCount
                    break
    return messageDict

def catch_exception_request(func):
    @functools.wraps(func)
    def catch_exception_wrapper(*args, **kwargs):
        try:
            funcRet = func(*args, **kwargs)
            return funcRet
        except Exception as e:
            retMsg = "[EXCEPTION]: 函数[%s]异常：%s" % (func.__name__,traceback.format_exc())
            logging.error(retMsg)
            logging.error(traceback.format_exc())
            #返回一个提示对象，明确提示错误
            return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message=ApiReturn.RQUEST_EXCEPTION_MSG).toJson())
    return catch_exception_wrapper

def BL_MD_isList(tmpStr):
    try:
        if eval("""type(%s)""" % tmpStr) == list:
            return eval(tmpStr)
        else:
            return tmpStr.split(",")
    except:
        return tmpStr.split(",")

def queryPeopleCountByTablename(now_pageNum,pageNum , loginName,tbName):
    limit = ('%d,%d' % (now_pageNum * pageNum,pageNum))
    execSql = 'SELECT u.loginName , u.userName, c.count from tb_user u LEFT JOIN (SELECT addBy as loginName,COUNT(*) as count FROM %s where state=1 GROUP BY addBy ) c on u.loginName = c.loginName WHERE u.state = 1 and c.count>0 and u.loginName != "%s" order by c.count desc LIMIT %s ;' % (tbName,loginName,limit)
    resultDict = executeSqlGetDict(execSql,[])
    return resultDict