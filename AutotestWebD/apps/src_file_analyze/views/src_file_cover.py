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
from copy import deepcopy
from apps.version_manage.services.common_service import VersionService


def srcFileCoverCheck(request):
    langDict = getLangTextDict(request)
    context = {}

    context["srcFileCoverCheck"] = "current-page"
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
    return render(request, "InterfaceTest/src_file_analyze/src_file_cover.html", context)


def srcFileCoverList(request):
    checkArr = json.loads(parse.unquote(request.POST.get("queryArr")))
    orderBy = request.POST.get("orderBy")
    if isSqlInjectable(orderBy):
        return HttpResponse("<script>alert('查询条件非法');</script>")

    t1 = time.time()
    if VersionService.isCurrentVersion(request):
        tbName = "tb_http_interface"
        versionCondition = ""
    else:
        tbName = "tb_version_http_interface"
        versionCondition = "and i.versionName='%s'" % request.session.get("version")
    #获取所有的接口
    allInterfaceSql = "SELECT i.url url,b.bussinessLineName businessLineName,m.moduleName moduleName,u.userName userName,count(DISTINCT b.bussinessLineName,m.moduleName,i.url ) FROM %s i LEFT JOIN tb_business_line b ON i.businessLineId = b.id LEFT JOIN tb_modules m ON i.moduleId = m.id LEFT JOIN tb_user u ON i.addBy = u.loginName where i.state = 1 and i.caseType in (1,2) %s " %(tbName,versionCondition)
    allData = createSqlDict(checkArr,orderBy,allInterfaceSql,"group by i.url,i.businessLineId,i.moduleId")
    t2 = time.time()
    print("(查询接口)t2-t1:%d" % (t2-t1) )
    if VersionService.isCurrentVersion(request):
        tbName = "tb_http_testcase_step"
        versionCondition = ""
    else:
        tbName = "tb_version_http_testcase_step"
        versionCondition = "and i.versionName='%s'" % request.session.get("version")
    #获取所有的步骤接口
    allStepSql = "SELECT i.url url,b.bussinessLineName businessLineName,m.moduleName moduleName,u.userName userName,count(DISTINCT b.bussinessLineName,m.moduleName,i.url ) FROM %s i LEFT JOIN tb_business_line b ON i.businessLineId = b.id LEFT JOIN tb_modules m ON i.moduleId = m.id LEFT JOIN tb_user u ON i.addBy = u.loginName where i.state = 1 and i.caseType in (2,3) %s " % (tbName,versionCondition)
    allStepData = createSqlDict(checkArr,orderBy,allStepSql,"group by i.url,i.businessLineId,i.moduleId")
    t3 = time.time()
    print("(查询step接口)t3-t2:%d" % (t3-t2) )

    #步骤和接口去重
    stepDataLen = len(allStepData)
    for dataIndex in range(0,len(allData)):
        stepIndex = 0
        while stepIndex < stepDataLen:
            if allData[dataIndex]["businessLineName"] == allStepData[stepIndex]["businessLineName"]:
                if allData[dataIndex]["moduleName"] == allStepData[stepIndex]["moduleName"]:
                    if allData[dataIndex]["url"] == allStepData[stepIndex]["url"]:
                        del allStepData[stepIndex]
                        stepDataLen = len(allStepData)
            stepIndex += 1
    allData.extend(allStepData)
    t4 = time.time()
    print("(接口步骤去重)t4-t3:%d" % (t4-t3) )

    #查询标准接口
    if VersionService.isCurrentVersion(request):
        tbName = "tb_standard_interface"
        versionCondition = ""
    else:
        tbName = "tb_version_standard_interface"
        versionCondition = "and i.versionName='%s'" % request.session.get("version")
    standardSql = "SELECT i.interfaceUrl url,m.moduleName moduleName,b.bussinessLineName businessLineName,u.userName userName FROM %s i LEFT JOIN tb_modules m ON i.moduleId = m.id LEFT JOIN tb_business_line b ON i.businessLineId = b.id  LEFT JOIN tb_user u ON i.addBy = u.loginName WHERE 1=1 AND i.state=1 AND i.apiStatus = 1 %s " % (tbName,versionCondition)
    del checkArr["addBy"]
    standardData = createSqlDict(checkArr, "", standardSql, "group by i.interfaceUrl,i.businessLineId,i.moduleId")
    # print(standardData)
    t5 = time.time()
    print("(查询标准)t5-t4:%d" % (t5-t4) )
    allDataCount = len(allData)
    standardCount = len(standardData)
    coverCount = 0
    standardDataDict = {}

    for tmpInterfaceDict in standardData:
        tmpInterfaceDict["standardIsCovered"] = False
        tmpBusinessLine = tmpInterfaceDict['businessLineName']
        tmpModule = tmpInterfaceDict['moduleName']
        if tmpBusinessLine not in standardDataDict.keys():
            standardDataDict[tmpBusinessLine] = {"dataList":[],"businessLineCount":0,"businessLineIsCoveredCount":0,"moduleDict":{}}
        standardDataDict[tmpBusinessLine]['dataList'].append(tmpInterfaceDict)
        standardDataDict[tmpBusinessLine]['businessLineCount'] += 1
        if tmpModule not in standardDataDict[tmpBusinessLine]['moduleDict'].keys():
            standardDataDict[tmpBusinessLine]['moduleDict'][tmpModule] = {"dataList":[],"moduleCount":0,"moduleIsCoveredCount":0}
        standardDataDict[tmpBusinessLine]['moduleDict'][tmpModule]['dataList'].append(tmpInterfaceDict)
        standardDataDict[tmpBusinessLine]['moduleDict'][tmpModule]['moduleCount'] += 1

    allDataDict = {}
    for tmpInterfaceDict in allData:
        tmpInterfaceDict["standardIsCovered"] = False
        tmpBusinessLine = tmpInterfaceDict['businessLineName']
        tmpModule = tmpInterfaceDict['moduleName']
        if tmpBusinessLine not in allDataDict.keys():
            allDataDict[tmpBusinessLine] = {"dataList":[],"businessLineCount":0,"businessLineIsCoveredCount":0,"moduleDict":{}}
        if tmpBusinessLine not in standardDataDict.keys():
            standardDataDict[tmpBusinessLine] = {"dataList":[],"businessLineCount":0,"businessLineIsCoveredCount":0,"moduleDict":{}}
        allDataDict[tmpBusinessLine]['dataList'].append(tmpInterfaceDict)
        allDataDict[tmpBusinessLine]['businessLineCount'] += 1
        if tmpModule not in allDataDict[tmpBusinessLine]['moduleDict'].keys():
            allDataDict[tmpBusinessLine]['moduleDict'][tmpModule] = {"dataList":[],"moduleCount":0,"moduleIsCoveredCount":0}
        if tmpModule not in standardDataDict[tmpBusinessLine]['moduleDict'].keys():
            standardDataDict[tmpBusinessLine]['moduleDict'][tmpModule] = {"dataList": [], "moduleCount": 0,"moduleIsCoveredCount": 0}
        allDataDict[tmpBusinessLine]['moduleDict'][tmpModule]['dataList'].append(tmpInterfaceDict)
        allDataDict[tmpBusinessLine]['moduleDict'][tmpModule]['moduleCount'] += 1
    #开始遍历标准字典了！
    for standardBLineKey, standardBLineValue in standardDataDict.items():
        #遍历自己的业务线datalist生成业务线的覆盖率统计
        #if panduan shifou you key
        if standardBLineKey not in allDataDict:
            allDataDict[standardBLineKey] = {"dataList":[],"businessLineCount":0,"businessLineIsCoveredCount":0,"moduleDict":{}}
            continue
            # pass
        allBLineValue = allDataDict[standardBLineKey]
        for tmpStandardUrlDict in standardBLineValue['dataList']:
            for tmpAllUrlDict in allBLineValue['dataList']:
                # if tmpStandardUrlDict['url'] == tmpAllUrlDict['url']:
                #     print(tmpAllUrlDict)
                if checkUrl(tmpStandardUrlDict['url']) == checkUrl(tmpAllUrlDict['url']) and tmpStandardUrlDict["moduleName"] == tmpAllUrlDict["moduleName"]:
                    tmpStandardUrlDict["standardIsCovered"] = True
                    tmpStandardUrlDict["dataUrl"] = tmpAllUrlDict['url']
                    tmpAllUrlDict["dataIsCovered"] = True
                    # if tmpStandardUrlDict["moduleName"] == "元数据":
                    #     print(tmpAllUrlDict)
                    standardBLineValue["businessLineIsCoveredCount"] += 1
                    coverCount += 1
        tmpStandardModuleDict = standardDataDict[standardBLineKey]["moduleDict"]
        for standardModuleKey , standardModuleValue in tmpStandardModuleDict.items():
            if standardModuleKey not in allDataDict[standardBLineKey]["moduleDict"]:
                allDataDict[standardBLineKey]["moduleDict"][standardModuleKey] = {"dataList":[],"moduleCount":0,"moduleIsCoveredCount":0}
                continue
                # pass
            allMdValue = allDataDict[standardBLineKey]["moduleDict"][standardModuleKey]["dataList"]
            for tmpStandardMdDict in tmpStandardModuleDict[standardModuleKey]["dataList"]:
                for tmpAllMdDict in allMdValue:
                    if checkUrl(tmpStandardMdDict["url"]) == checkUrl(tmpAllMdDict["url"]):
                        tmpStandardMdDict["standardIsCovered"] = True
                        tmpAllMdDict["dataIsCovered"] = True
                        tmpStandardMdDict["dataUrl"] = tmpAllMdDict["url"]
                        tmpStandardModuleDict[standardModuleKey]["moduleIsCoveredCount"] += 1

    for standardKey,standardValue in standardDataDict.items():
        for dataKey,dataValue in allDataDict.items():
            if dataKey == standardKey:
                standardValue["businessCovered"] = '%.2f' % 0
                standardValue["businessNotCovered"] = standardValue["businessLineCount"] - standardValue["businessLineIsCoveredCount"]
                standardValue["notStandardCount"] = dataValue["businessLineCount"] - standardValue["businessLineIsCoveredCount"]
                if standardValue["businessLineCount"] != 0:
                    standardValue["businessCovered"] = '%.2f' % (standardValue["businessLineIsCoveredCount"] / standardValue["businessLineCount"] * 100)

                for standardModuleKey,standardModuleValue in standardValue["moduleDict"].items():
                    standardModuleValue["moduleCovered"] = '%.2f' % 0
                    standardModuleValue["moduleNotCoveredCount"] = standardModuleValue["moduleCount"]
                    standardModuleValue["notStandardCount"] = 0
                    for dataModuleKey,dataModuleValue in dataValue["moduleDict"].items():
                        if dataModuleKey == standardModuleKey:
                            standardModuleValue["moduleNotCoveredCount"] = standardModuleValue["moduleCount"] - standardModuleValue["moduleIsCoveredCount"]
                            standardModuleValue["notStandardCount"] = dataModuleValue["moduleCount"] - standardModuleValue["moduleIsCoveredCount"]
                            if standardModuleValue["moduleCount"] != 0:
                                standardModuleValue["moduleCovered"] = '%.2f' % (standardModuleValue["moduleIsCoveredCount"] / standardModuleValue["moduleCount"] * 100)

    context = {}
    if checkArr["businessLine"] == "" and checkArr["module"] == "":
        context["allDataStatistics"] = {}
        context["allDataStatistics"]["allDataCount"] = allDataCount
        context["allDataStatistics"]["standardCount"] = standardCount
        context["allDataStatistics"]["coverCount"] = coverCount
        context["allDataStatistics"]["notCoverCount"] = standardCount - coverCount
        context["allDataStatistics"]["notStandardCount"] = allDataCount - coverCount
        coverage = '%.2f' % 0
        if standardCount != 0:
            coverage = '%.2f' % (coverCount / standardCount * 100)
        context["allDataStatistics"]["coverage"] = coverage
    context["standardDataDict"] = standardDataDict
    context["dataDict"] = allDataDict
    print(context)
    response = render(request, "InterfaceTest/src_file_analyze/SubPages/src_file_cover_sub_page.html", context)
    t6 = time.time()
    print("(所有统计时间)t6-t5:%d" % (t6-t5) )

    return response


