from apps.common.func.CommonFunc import *
from apps.common.func.LanguageFunc import *
from django.shortcuts import render, HttpResponse
from apps.config.services.http_confService import HttpConfService
from urllib import parse
from apps.common.config import commonWebConfig
from apps.config.services.businessLineService import BusinessService
from apps.config.services.modulesService import ModulesService
from apps.common.func.WebFunc import *
from apps.src_file_analyze.services.src_file_analyzeService import SrcFileAnalyzeService
import json
from apps.version_manage.services.common_service import VersionService
from all_models.models import TbStandardInterface

def srcFileCheck(request):
    langDict = getLangTextDict(request)
    context = {}

    context["srcFileAnalyze"] = "open"
    context["userName"] = request.session.get("userName")
    if not isRelease:
        context["env"] = "test"

    # 文本
    text = {}
    text["pageTitle"] = langDict["web"]["srcFileAnalyzePageTitle"]
    text["subPageTitle"] = langDict["web"]["httpUserCenterGlobalVarsSubPageTitle"]
    context["text"] = text
    context["checkBusinessLine"] = dbModelListToListDict(BusinessService.getAllBusinessLine())
    context["checkModules"] = dbModelListToListDict(ModulesService.getAllModules())

    context["page"] = 1
    return render(request, "InterfaceTest/src_file_analyze/src_file.html", context)


def srcFileList(request):

    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    checkArr = json.loads(parse.unquote(request.POST.get("queryArr")))
    orderBy = request.POST.get("orderBy")
    if isSqlInjectable(orderBy):
        return HttpResponse("<script>alert('查询条件非法');</script>")

    if VersionService.isCurrentVersion(request):
        tbName = "tb_standard_interface"
        versionCondition = ""
    else:
        tbName = "tb_version_standard_interface"
        versionCondition = "and g.versionName='%s'" % request.session.get("version")

    execSql = "SELECT g.*,m.moduleName,b.bussinessLineName FROM %s g LEFT JOIN tb_modules m on g.moduleId = m.id LEFT JOIN tb_business_line b on g.businessLineId = b.id WHERE g.state=1 %s" % (tbName,versionCondition)
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        elif key == "businessLine":
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and b.bussinessLineName LIKE %s """
            continue
        elif key == "module":
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and m.moduleName LIKE %s """
            continue
        elif key == "fileRealPath":
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and g.fileName LIKE %s """
            continue
        elif key == "interfaceUrl":
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and g.interfaceUrl LIKE %s """
            continue
        elif key == "apiStatus":
            statusDict = {"有效":"1","废弃":"0","未发现注释":"3","注释不合法":"4"}
            statusValue = statusDict[checkArr[key]]
            checkList.append("%s" % statusValue)
            execSql += """ and g.apiStatus = %s """
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and g.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    print(execSql)
    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.standardInterfacePageNum)
    context["checkBusinessLine"] = dbModelListToListDict(BusinessService.getAllBusinessLine())
    context["checkModules"] = dbModelListToListDict(ModulesService.getAllModules())
    response = render(request, "InterfaceTest/src_file_analyze/SubPages/src_file_sub_page.html", context)
    return response

def refreshSrcFile(request):
    standardInterfaceId = request.GET.get("id")
    sObjSets = TbStandardInterface.objects.filter(id=standardInterfaceId)
    if sObjSets:
        standardObj = sObjSets[0]
    else:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_PARAM_ERROR,message="信息不存在").toJson())
    if SrcFileAnalyzeService.gitPullRecentCode() == False:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_METHOD_ERROR,message="无法更新到最新代码，请联系管理员。").toJson())

    isValidFileWithCorrectFileName = False
    for tmpLastRoleName in srcFoldersLastFileNameRole:
        if standardObj.fileName.endswith(tmpLastRoleName):
            isValidFileWithCorrectFileName = True
            break
    if isValidFileWithCorrectFileName:
        retUrlList = SrcFileAnalyzeService.analyzeFileWithAnno(standardObj.fileName)
        messageDict = {}
        # if len(retUrlList) > 0:
        messageDict[standardObj.fileName] = {}
        messageDict[standardObj.fileName]['urlDictList'] = retUrlList
        retMessage = SrcFileAnalyzeService.createStandardInterfaceUseAnnoDictUrls(messageDict)
        if retMessage == "":
            return HttpResponse(ApiReturn().toJson())
        else:
            #如果不为空，输出报警信息。
            return HttpResponse(ApiReturn(code=ApiReturn.CODE_PARAM_ERROR, message=retMessage).toJson())
    else:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_PARAM_ERROR, message="不合法的解析文件").toJson())

def getAllInterfaceCounts(request):
    messageDict = {}
    messageDict["allCount"] = 0

    for root, dirs, files in os.walk(srcRootDir):
        for tmpFile in files:
            for tmpLastRoleName in srcFoldersLastFileNameRole:
                if tmpFile.endswith(tmpLastRoleName):
                    realPath = (root + os.sep + tmpFile).replace("\\","/")
                    fileRealPath = realPath.split(srcRootDir)[1].replace("\\","/")
                    retUrlList, retFileName, retFileText = SrcFileAnalyzeService.analyzeFile(fileRealPath)
                    messageDict["allCount"] += len(retUrlList)
                    messageDict[fileRealPath] = len(retUrlList)
                    break

    return HttpResponse(ApiReturn(body=messageDict).toJson())

def getAllApiCountsNum(request):
    messageDict = getAllApiCountsNumConfig()

    return HttpResponse(ApiReturn(body=messageDict).toJson())

def generateAllInterfacesByAnno(request):
    try:
        cmdStr = 'python3 %s/AutotestWebD/apps/src_file_analyze/scripts/generate_all_standard_interfaces_by_anno.py' % rootDir
        print("CMDSTR:%s" % cmdStr)
        output = os.popen(cmdStr)
        outStr = output.read()
        print("outStr:%s" % outStr)
        finalOutStr = outStr.split(djangoSettingSplitString)[-1].replace("\n","<br>")
        if "ERROR:" in outStr:
            return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR,message=finalOutStr).toJson())
        elif "EXCEPTION:" in outStr:
            return HttpResponse(ApiReturn(code=ApiReturn.CODE_EXCEPTION,message=finalOutStr).toJson())
        elif "WARNING:" in outStr:
            return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=finalOutStr).toJson())
        else:
            return HttpResponse(ApiReturn(code=ApiReturn.CODE_OK,message=finalOutStr).toJson())
    except Exception as e:
        print(traceback.format_exc())
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_EXCEPTION, message=traceback.format_exc()).toJson())