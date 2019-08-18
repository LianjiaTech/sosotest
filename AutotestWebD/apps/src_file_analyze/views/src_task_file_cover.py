from apps.common.func.CommonFunc import *
from apps.common.func.LanguageFunc import *
from django.shortcuts import render, HttpResponse
from urllib import parse
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from apps.task.services.HTTP_taskService import HTTP_taskService
from apps.test_case.services.HTTP_test_case_stepService import HTTP_test_case_stepService
from apps.src_file_analyze.services.src_file_analyzeService import SrcFileAnalyzeService
import json
from copy import deepcopy
from apps.version_manage.services.common_service import VersionService

def srcTaskFileCoverCheck(request):
    langDict = getLangTextDict(request)
    context = {}

    context["srcFileCover"] = "open"
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
    return render(request, "InterfaceTest/src_file_analyze/src_task_file_cover.html", context)


def srcTaskFileCoverList(request):
    t0 = time.time()
    if request.POST.get("taskList"):
        taskIdList = request.POST.get("taskList").split(",")
    else:
        selflastTask = dbModelListToListDict(HTTP_taskService.getUserLastTask(request.session.get("loginName")))
        if len(selflastTask) < 1:
            response = render(request, "InterfaceTest/src_file_analyze/SubPages/src_task_file_cover_sub_page.html",{})
            return response
        taskIdList = [selflastTask[-1]["taskId"]]

    t1 = time.time()
    print("[查询任务list]t1-t0:%f" % (t1-t0))
    if VersionService.isCurrentVersion(request):
        taskList = dbModelListToListDict(HTTP_taskService.getTaskListForTaskIdList(taskIdList))
    else:
        taskList = dbModelListToListDict(HTTP_taskService.getVersionTaskListForTaskIdList(taskIdList,VersionService.getVersionName(request)))

    t2 = time.time()
    print("[查询所有任务]t2-t1:%f" % (t2-t1))
    allInerfaceIdList = []
    allTestCaseIdList = []
    for taskIndex in range(0,len(taskList)):
        thisTaskInterfaceList = taskList[taskIndex]["taskInterfaces"].split(",")
        allInerfaceIdList.extend(thisTaskInterfaceList)
        thisTaskTestCaseList = taskList[taskIndex]["taskTestcases"].split(",")
        allTestCaseIdList.extend(thisTaskTestCaseList)

    allInerfaceIdList = list(set(allInerfaceIdList))
    allTestCaseIdList = list(set(allTestCaseIdList))
    allstepIdList = []
    t3 = time.time()
    print("[去重任务中的接口和用例]t3-t2:%f" % (t3-t2))

    if VersionService.isCurrentVersion(request):
        allstepList = HTTP_test_case_stepService.getTestCaseStepList(allTestCaseIdList)
    else:
        allstepList = HTTP_test_case_stepService.getVersionTestCaseStepList(allTestCaseIdList,VersionService.getVersionName(request))
    for stepIndex in range(0, len(allstepList)):
        allstepIdList.append(allstepList[stepIndex]["id"])
    t4 = time.time()
    print("[通过caseIdList获取所有步骤]t4-t3:%f" % (t4-t3))

    if VersionService.isCurrentVersion(request):
        tbName = "tb_http_interface"
        versionCondition = ""
    else:
        tbName = "tb_version_http_interface"
        versionCondition = "and i.versionName='%s'" % request.session.get("version")
    allInterfaceSql = "SELECT i.url url,b.bussinessLineName businessLineName,m.moduleName moduleName,u.userName userName,count(DISTINCT b.bussinessLineName,m.moduleName,i.url ) FROM %s i LEFT JOIN tb_business_line b ON i.businessLineId = b.id LEFT JOIN tb_modules m ON i.moduleId = m.id LEFT JOIN tb_user u ON i.addBy = u.loginName where i.state = 1 and i.caseType in (1,2) and i.interfaceId in ('%s') %s group by i.url,i.businessLineId,i.moduleId" % (tbName,"','".join(allInerfaceIdList),versionCondition)
    allInterfaceData = executeSqlGetDict(allInterfaceSql,[])

    if VersionService.isCurrentVersion(request):
        tbName = "tb_http_testcase_step"
        versionCondition = ""
    else:
        tbName = "tb_version_http_testcase_step"
        versionCondition = "and i.versionName='%s'" % request.session.get("version")
    allStepSql = "SELECT i.url url,b.bussinessLineName businessLineName,m.moduleName moduleName,u.userName userName,count(DISTINCT b.bussinessLineName,m.moduleName,i.url ) FROM %s i LEFT JOIN tb_business_line b ON i.businessLineId = b.id LEFT JOIN tb_modules m ON i.moduleId = m.id LEFT JOIN tb_user u ON i.addBy = u.loginName where i.state = 1 and i.caseType in (2,3) and i.id in ('%s') %s GROUP BY i.url,i.businessLineId,i.moduleId" % (tbName,"','".join((str(i) for i in allstepIdList)),versionCondition)
    allStepData = executeSqlGetDict(allStepSql,[])
    t5 = time.time()
    print("[查询接口和步骤]t5-t4:%f" % (t5-t4))
    print(len(allInterfaceData))
    print(len(allStepData))

    #接口和步骤去重
    stepDataLen = len(allStepData)
    for dataIndex in range(0, len(allInterfaceData)):
        stepIndex = 0
        while stepIndex < stepDataLen:
            if allInterfaceData[dataIndex]["businessLineName"] == allStepData[stepIndex]["businessLineName"]:
                if allInterfaceData[dataIndex]["moduleName"] == allStepData[stepIndex]["moduleName"]:
                    if allInterfaceData[dataIndex]["url"] == allStepData[stepIndex]["url"]:
                        del allStepData[stepIndex]
                        stepDataLen = len(allStepData)
            stepIndex += 1
    allInterfaceData.extend(allStepData)
    print(len(allInterfaceData))
    t6= time.time()
    print("[去重接口和步骤]t6-t5:%f" % (t6-t5))

    if VersionService.isCurrentVersion(request):
        tbName = "tb_standard_interface"
        versionCondition = ""
    else:
        tbName = "tb_version_standard_interface"
        versionCondition = "and i.versionName='%s'" % request.session.get("version")
    standardSql = "SELECT i.interfaceUrl url,m.moduleName moduleName,b.bussinessLineName businessLineName,u.userName userName FROM %s i LEFT JOIN tb_modules m ON i.moduleId = m.id LEFT JOIN tb_business_line b ON i.businessLineId = b.id  LEFT JOIN tb_user u ON i.addBy = u.loginName WHERE 1=1 AND i.apiStatus = 1 AND i.state=1 %s GROUP BY i.interfaceUrl,i.businessLineId,i.moduleId" % (tbName,versionCondition)
    standardData = executeSqlGetDict(standardSql,[])
    t7= time.time()
    print("[查询标准]t7-t6:%f" % (t7-t6))

    for dataIndex in standardData:
        dataIndex["standardIsCovered"] = False
    t71= time.time()
    print("[生成标准dict]t71-t7:%f" % (t71-t7))
    #生成用户数据dict
    allDataDict = {}
    for tmpInterfaceDict in allInterfaceData:
        tmpInterfaceDict["standardIsCovered"] = False
        tmpBusinessLine = tmpInterfaceDict['businessLineName']
        tmpModule = tmpInterfaceDict['moduleName']
        if tmpBusinessLine not in allDataDict.keys():
            allDataDict[tmpBusinessLine] = {"dataList": [], "businessLineCount": 0, "businessLineIsCoveredCount": 0,"businessLineStandardCount":0,"moduleDict": {},"queryBL":True}
        allDataDict[tmpBusinessLine]['dataList'].append(tmpInterfaceDict)
        allDataDict[tmpBusinessLine]['businessLineCount'] += 1
        if tmpModule not in allDataDict[tmpBusinessLine]['moduleDict'].keys():
            allDataDict[tmpBusinessLine]['moduleDict'][tmpModule] = {"dataList": [], "moduleCount": 0,"moduleStandardCount":0, "moduleIsCoveredCount": 0,"queryMD":True}
        allDataDict[tmpBusinessLine]['moduleDict'][tmpModule]['dataList'].append(tmpInterfaceDict)
        allDataDict[tmpBusinessLine]['moduleDict'][tmpModule]['moduleCount'] += 1
    t72= time.time()
    print("[生成用户数据dict]t72-t71:%f" % (t72-t71))

    standardDataDict = {}
    # 生成标准dict
    for tmpInterfaceDict in standardData:
        tmpBusinessLine = tmpInterfaceDict['businessLineName']
        tmpModule = tmpInterfaceDict['moduleName']
        if tmpBusinessLine not in allDataDict.keys():
            continue
        if tmpBusinessLine not in standardDataDict.keys():
            standardDataDict[tmpBusinessLine] = {"dataList": [], "businessLineCount": 0,"businessLineIsCoveredCount": 0, "moduleDict": {}}
        standardDataDict[tmpBusinessLine]['dataList'].append(tmpInterfaceDict)
        standardDataDict[tmpBusinessLine]['businessLineCount'] += 1
        allDataDict[tmpBusinessLine]['businessLineStandardCount'] += 1
        if tmpModule not in allDataDict[tmpBusinessLine]['moduleDict'].keys():
            continue
        if tmpModule not in standardDataDict[tmpBusinessLine]['moduleDict'].keys():
            standardDataDict[tmpBusinessLine]['moduleDict'][tmpModule] = {"dataList": [], "moduleCount": 0,"moduleIsCoveredCount": 0}
        standardDataDict[tmpBusinessLine]['moduleDict'][tmpModule]['dataList'].append(tmpInterfaceDict)
        standardDataDict[tmpBusinessLine]['moduleDict'][tmpModule]['moduleCount'] += 1
        allDataDict[tmpBusinessLine]['moduleDict'][tmpModule]['moduleStandardCount'] += 1
    # 开始遍历标准字典了！为了给是否覆盖的tag改为True
    coverCount = 0 #不用用同一个名字！！如果用同一个名字，要分清楚哪里要还原为0！
    allDataStatistics = {}
    allDataStatistics["allDataCount"] = len(allInterfaceData)
    allDataStatistics["standardCount"] = len(standardData)
    allDataStatistics["coverCount"] = 0 #执行后生成
    allDataStatistics["notCoverCount"] = 0  #执行后还要重算
    allDataStatistics["notStandardCount"] = len(allInterfaceData) - coverCount  #执行后还要重算
    for standardBLineKey, standardBLineValue in standardDataDict.items():
        # 遍历自己的业务线datalist生成业务线的覆盖率统计
        if standardBLineKey not in allDataDict:
            allDataDict[standardBLineKey] = {"dataList": [], "businessLineCount": 0, "businessLineIsCoveredCount": 0,"moduleDict": {}}
        #先循环判断当期业务线的数据统计
        allBLineValue = allDataDict[standardBLineKey]
        for tmpStandardUrlDict in standardBLineValue['dataList']:
            for tmpAllUrlDict in allBLineValue['dataList']:
                if checkUrl(tmpStandardUrlDict['url']) == checkUrl(tmpAllUrlDict['url']) and tmpStandardUrlDict['moduleName'] == tmpAllUrlDict['moduleName']:
                    tmpStandardUrlDict["standardIsCovered"] = True
                    tmpAllUrlDict["dataIsCovered"] = True
                    tmpStandardUrlDict["dataUrl"] = tmpAllUrlDict['url']
                    allBLineValue["businessLineIsCoveredCount"] += 1
                    allDataStatistics["coverCount"] += 1
        #在判断当前业务线线下的modelDict的统计
        tmpStandardModuleDict = standardDataDict[standardBLineKey]["moduleDict"]
        for standardModuleKey, standardModuleValue in tmpStandardModuleDict.items():
            if standardModuleKey not in allDataDict[standardBLineKey]["moduleDict"]:
                allDataDict[standardBLineKey]["moduleDict"][standardModuleKey] = {"dataList": [], "moduleCount": 0,"moduleIsCoveredCount": 0}
                allDataDict[standardBLineKey]["moduleDict"][standardModuleKey]["queryMD"] = False
                continue
            allMdValue = allDataDict[standardBLineKey]["moduleDict"][standardModuleKey]["dataList"]
            for tmpStandardMdDict in tmpStandardModuleDict[standardModuleKey]["dataList"]:
                for tmpAllMdDict in allMdValue:
                    if checkUrl(tmpStandardMdDict["url"]) == checkUrl(tmpAllMdDict["url"]):
                        tmpStandardMdDict["standardIsCovered"] = True
                        tmpAllMdDict["dataIsCovered"] = True
                        tmpStandardMdDict["dataUrl"] = tmpAllMdDict["url"]
                        allDataDict[standardBLineKey]["moduleDict"][standardModuleKey]["moduleIsCoveredCount"] += 1

    allDataStatistics["notCoverCount"] = allDataStatistics["standardCount"] - allDataStatistics["coverCount"]  # 执行后还要重算
    allDataStatistics["notStandardCount"] = len(allInterfaceData) - allDataStatistics["coverCount"]   # 执行后还要重算
    coverage = '%.2f' % 0
    if allDataStatistics["standardCount"] != 0:
        coverage = '%.2f' % (allDataStatistics["coverCount"] / allDataStatistics["standardCount"] * 100)
    allDataStatistics["coverage"] = coverage

    #生成覆盖tag后开始计算覆盖率所有数据的覆盖率
    for standardKey,standardValue in standardDataDict.items():
        for dataKey,dataValue in allDataDict.items():
            if dataKey == standardKey:
                dataValue["businessCovered"] = '%.2f' % 0
                dataValue["businessNotCovered"] = dataValue["businessLineStandardCount"] - dataValue["businessLineIsCoveredCount"]
                if dataValue["businessLineCount"] != 0:
                    dataValue["businessCovered"] = '%.2f' % (dataValue["businessLineIsCoveredCount"] / dataValue["businessLineStandardCount"] * 100)
                else:
                    dataValue["businessCovered"] = '%.2f' % 0
                for dataModuleKey,dataModuleValue in dataValue["moduleDict"].items():
                        dataModuleValue["moduleNotCoveredCount"] = dataModuleValue["moduleStandardCount"] - dataModuleValue["moduleIsCoveredCount"]
                        if dataModuleValue["moduleStandardCount"] != 0:
                            dataModuleValue["moduleCovered"] = '%.2f' % (dataModuleValue["moduleIsCoveredCount"] / dataModuleValue["moduleStandardCount"] * 100)
                        else:
                            dataModuleValue["moduleCovered"] = '%.2f' % 0
    context = {}
    context["allDataStatistics"] = allDataStatistics
    context["standardDataDict"] = standardDataDict
    context["dataDict"] = allDataDict

    #生成任务的字典
    taskDict = {}
    for taskIndex in range(0,len(taskList)):
        thisTaskData = getTaskInterfaceData(taskList[taskIndex]["taskId"],request)
        print(len(thisTaskData))
        for dataIndex in thisTaskData:
            dataIndex["isCovered"] = False
        taskDict[taskList[taskIndex]["taskId"]] = {"taskInterfaceCount":len(thisTaskData),
                                                   "taskDataList":thisTaskData,
                                                   "taskIsCoveredCount":0,
                                                   "taskContainsBl":{},
                                                   "standardDataList":deepcopy(standardData)}
        taskDict[taskList[taskIndex]["taskId"]]["coverage"] = '%.2f' % 0.00
        tmpBlDict = taskDict[taskList[taskIndex]["taskId"]]["taskContainsBl"]
        for tmpBlIndex in thisTaskData:
            if tmpBlIndex["businessLineName"] not in tmpBlDict:
                tmpBlDict[tmpBlIndex["businessLineName"]] = {"blCount":0,"blDataList":[],"blIsCoveredCount":0,"blContainsMd":{},"standardDataList":[],"standardBlCount":0,"blNotCoveredCount":0}
                tmpBlDict[tmpBlIndex["businessLineName"]]["blCoverage"] = '%.2f' % 0.00
            tmpBlDict[tmpBlIndex["businessLineName"]]["blCount"] += 1
            tmpBlDict[tmpBlIndex["businessLineName"]]["blDataList"].append(deepcopy(tmpBlIndex))
            for standardIndex in standardData:
                if standardIndex["businessLineName"] == tmpBlIndex["businessLineName"]:
                    tmpBlDict[tmpBlIndex["businessLineName"]]["standardDataList"].append(deepcopy(standardIndex))

            tmpMd = tmpBlDict[tmpBlIndex["businessLineName"]]["blContainsMd"]
            if tmpBlIndex["moduleName"] not in tmpMd:
                tmpMd[tmpBlIndex["moduleName"]] = {"mdCount":0,"mdDataList":[],"mdIsCoveredCount":0,"standardDataList":[],"standardMdCount":0,"mdNotCoveredCount":0}
                tmpMd[tmpBlIndex["moduleName"]]["mdCoverage"] = '%.2f' % 0.00
            tmpMd[tmpBlIndex["moduleName"]]["mdCount"] += 1
            tmpMd[tmpBlIndex["moduleName"]]["mdDataList"].append(deepcopy(tmpBlIndex))
            for standardIndex in standardData:
                if standardIndex["moduleName"] == tmpBlIndex["moduleName"] and standardIndex["businessLineName"] == tmpBlIndex["businessLineName"]:
                    tmpMd[tmpBlIndex["moduleName"]]["standardDataList"].append(deepcopy(standardIndex))

    t75 = time.time()
    #开始生成任务的覆盖率了！
    for tmpTaskKey,tmpTaskValue in taskDict.items():
        for taskDataIndex in tmpTaskValue["taskDataList"]:
            for standardIndex in standardData:
                if checkUrl(taskDataIndex["url"]) == checkUrl(standardIndex["url"]) and taskDataIndex["businessLineName"] == standardIndex["businessLineName"] and taskDataIndex["moduleName"] == standardIndex["moduleName"]:
                    taskDataIndex["isCovered"] = True
                    tmpTaskValue["taskIsCoveredCount"] += 1
                    for taskStandardDataIndex in tmpTaskValue["standardDataList"]:
                        if checkUrl(taskStandardDataIndex["url"]) == checkUrl(standardIndex["url"]) and taskStandardDataIndex["businessLineName"] == standardIndex["businessLineName"] and taskStandardDataIndex["moduleName"] == standardIndex["moduleName"]:
                            taskStandardDataIndex["standardIsCovered"] = True
                            taskStandardDataIndex["dataUrl"] = standardIndex["url"]

        for tmpTaskBlKey,tmpTaskBlValue in tmpTaskValue["taskContainsBl"].items():
            for tmpTaskBlDataIndex in tmpTaskBlValue["blDataList"]:
                for standardIndex in standardData:
                    if checkUrl(tmpTaskBlDataIndex["url"]) == checkUrl(standardIndex["url"]) and tmpTaskBlDataIndex["businessLineName"] == standardIndex[
                        "businessLineName"] and tmpTaskBlDataIndex["moduleName"] == standardIndex["moduleName"]:
                        tmpTaskBlDataIndex["isCovered"] = True
                        tmpTaskBlValue["blIsCoveredCount"] += 1
                        for taskStandardDataIndex in tmpTaskBlValue["standardDataList"]:
                            if checkUrl(taskStandardDataIndex["url"]) == checkUrl(standardIndex["url"]) and taskStandardDataIndex[
                                "businessLineName"] == standardIndex[
                                "businessLineName"] and taskStandardDataIndex["moduleName"] == standardIndex["moduleName"]:
                                taskStandardDataIndex["standardIsCovered"] = True
                                taskStandardDataIndex["dataUrl"] = standardIndex["url"]
            for tmpTaskMdKey,tmpTaskMdValue in tmpTaskBlValue["blContainsMd"].items():
                for tmpTaskMdDataIndex in tmpTaskMdValue["mdDataList"]:
                    for standardIndex in standardData:
                        if checkUrl(tmpTaskMdDataIndex["url"]) == checkUrl(standardIndex["url"]) and tmpTaskMdDataIndex[
                            "businessLineName"] == standardIndex[
                            "businessLineName"] and tmpTaskMdDataIndex["moduleName"] == standardIndex["moduleName"]:
                            tmpTaskMdDataIndex["isCovered"] = True
                            tmpTaskMdValue["mdIsCoveredCount"] += 1
                            for taskStandardDataIndex in tmpTaskMdValue["standardDataList"]:
                                if checkUrl(taskStandardDataIndex["url"]) == checkUrl(standardIndex["url"]) and taskStandardDataIndex[
                                    "businessLineName"] == standardIndex[
                                    "businessLineName"] and taskStandardDataIndex["moduleName"] == standardIndex[
                                    "moduleName"]:
                                    taskStandardDataIndex["standardIsCovered"] = True
                                    taskStandardDataIndex["dataUrl"] = standardIndex["url"]

    t76 = time.time()
    print("[生成任务覆盖率]t76-t75:%f" % (t76 - t75))

    #计算覆盖率
    standardDataCount = len(standardData)
    for tmpTaskKey,tmpTaskValue in taskDict.items():
        tmpTaskValue["standardDataCount"] = standardDataCount
        tmpTaskValue["notCoveredCount"] = standardDataCount - tmpTaskValue["taskIsCoveredCount"]
        tmpTaskValue["notStandardCount"] = tmpTaskValue["taskInterfaceCount"] - tmpTaskValue["taskIsCoveredCount"]
        if standardDataCount != 0:
            tmpTaskValue["coverage"] = '%.2f' % (tmpTaskValue["taskIsCoveredCount"] / standardDataCount * 100)
        for tmpTaskBlKey, tmpTaskBlValue in tmpTaskValue["taskContainsBl"].items():
            tmpTaskBlValue["notStandardCount"] = tmpTaskBlValue["blCount"] - tmpTaskBlValue["blIsCoveredCount"]
            if tmpTaskBlKey in standardDataDict.keys():
                tmpTaskBlValue["standardBlCount"] = standardDataDict[tmpTaskBlKey]["businessLineCount"]
                tmpTaskBlValue["blNotCoveredCount"] = tmpTaskBlValue["standardBlCount"] - tmpTaskBlValue["blIsCoveredCount"]
                if standardDataDict[tmpTaskBlKey]["businessLineCount"] != 0:
                    tmpTaskBlValue["blCoverage"] = '%.2f' % (tmpTaskBlValue["blIsCoveredCount"] / standardDataDict[tmpTaskBlKey]["businessLineCount"] * 100)
                for tmpTaskMdKey,tmpTaskMdValue in tmpTaskBlValue["blContainsMd"].items():

                    tmpTaskMdValue["notStandardCount"] = tmpTaskMdValue["mdCount"] - tmpTaskMdValue["mdIsCoveredCount"]
                    if tmpTaskMdKey in standardDataDict[tmpTaskBlKey]["moduleDict"].keys():
                        tmpTaskMdValue["standardMdCount"] = standardDataDict[tmpTaskBlKey]["moduleDict"][tmpTaskMdKey]["moduleCount"]
                        tmpTaskMdValue["mdNotCoveredCount"] = tmpTaskMdValue["standardMdCount"] - tmpTaskMdValue["mdIsCoveredCount"]
                        if standardDataDict[tmpTaskBlKey]["moduleDict"][tmpTaskMdKey]["moduleCount"] != 0:
                            tmpTaskMdValue["mdCoverage"] = '%.2f' % (tmpTaskMdValue["mdIsCoveredCount"] / standardDataDict[tmpTaskBlKey]["moduleDict"][tmpTaskMdKey]["moduleCount"] * 100)

    t77 = time.time()
    print("[计算任务覆盖率]t77-t76:%f" % (t77 - t76))

    context["taskDict"] = taskDict
    response = render(request, "InterfaceTest/src_file_analyze/SubPages/src_task_file_cover_sub_page.html", context)
    t8= time.time()
    print("[render]t8-t77:%f" % (t8-t77))

    print("[所有计算时间]t8-t7:%f" % (t8-t7))

    return response

def getTaskInterfaceData(taskId,request):
    if VersionService.isCurrentVersion(request):
        taskData = dbModelToDict(HTTP_taskService.getTaskForTaskId(taskId))
    else:
        taskData = dbModelToDict(HTTP_taskService.getVersionTaskForTaskId(taskId,VersionService.getVersionName(request)))

    allInerfaceIdList = []
    allTestCaseIdList = []
    thisTaskInterfaceList = taskData["taskInterfaces"].split(",")
    allInerfaceIdList.extend(thisTaskInterfaceList)
    thisTaskTestCaseList = taskData["taskTestcases"].split(",")
    allTestCaseIdList.extend(thisTaskTestCaseList)

    allInerfaceIdList = list(set(allInerfaceIdList))
    allTestCaseIdList = list(set(allTestCaseIdList))
    allstepIdList = []
    for testCaseIndex in range(0, len(allTestCaseIdList)):
        if VersionService.isCurrentVersion(request):
            thisStepList = HTTP_test_case_stepService.getTestCaseStep(allTestCaseIdList[testCaseIndex])
        else:
            thisStepList = HTTP_test_case_stepService.getVersionTestCaseStep(allTestCaseIdList[testCaseIndex],VersionService.getVersionName(request))

        for stepIndex in range(0, len(thisStepList)):
            allstepIdList.append(thisStepList[stepIndex]["id"])

    if VersionService.isCurrentVersion(request):
        tbName = "tb_http_interface"
        versionCondition = ""
    else:
        tbName = "tb_version_http_interface"
        versionCondition = "and i.versionName='%s'" % request.session.get("version")
    allInterfaceSql = "SELECT i.url url,b.bussinessLineName businessLineName,m.moduleName moduleName,u.userName userName,count(DISTINCT b.bussinessLineName,m.moduleName,i.url ) FROM %s i LEFT JOIN tb_business_line b ON i.businessLineId = b.id LEFT JOIN tb_modules m ON i.moduleId = m.id LEFT JOIN tb_user u ON i.addBy = u.loginName where i.state = 1 and i.interfaceId in ('%s') %s group by i.url,i.businessLineId,i.moduleId" % (
    tbName,"','".join(allInerfaceIdList),versionCondition)
    allInterfaceData = executeSqlGetDict(allInterfaceSql, [])

    if VersionService.isCurrentVersion(request):
        tbName = "tb_http_testcase_step"
        versionCondition = ""
    else:
        tbName = "tb_version_http_testcase_step"
        versionCondition = "and i.versionName='%s'" % request.session.get("version")
    allStepSql = "SELECT i.url url,b.bussinessLineName businessLineName,m.moduleName moduleName,u.userName userName,count(DISTINCT b.bussinessLineName,m.moduleName,i.url ) FROM %s i LEFT JOIN tb_business_line b ON i.businessLineId = b.id LEFT JOIN tb_modules m ON i.moduleId = m.id LEFT JOIN tb_user u ON i.addBy = u.loginName where i.state = 1 and i.id in ('%s') %s GROUP BY i.url,i.businessLineId,i.moduleId" % (
    tbName,"','".join((str(i) for i in allstepIdList)),versionCondition)
    allStepData = executeSqlGetDict(allStepSql, [])

    print(len(allInterfaceData))
    print(len(allStepData))
    stepDataLen = len(allStepData)
    for dataIndex in range(0, len(allInterfaceData)):
        stepIndex = 0
        while stepIndex < stepDataLen:
            if allInterfaceData[dataIndex]["businessLineName"] == allStepData[stepIndex]["businessLineName"]:
                if allInterfaceData[dataIndex]["moduleName"] == allStepData[stepIndex]["moduleName"]:
                    if allInterfaceData[dataIndex]["url"] == allStepData[stepIndex]["url"]:
                        del allStepData[stepIndex]
                        stepDataLen = len(allStepData)
            stepIndex += 1
    allInterfaceData.extend(allStepData)
    return allInterfaceData

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
        tbName = "tb_task"
        versionCondition = "and t.versionName='%s'" % request.session.get("version")
    execSql = "SELECT t.*,u.userName from %s t LEFT JOIN tb_user u ON t.addBy = u.loginName  WHERE 1=1 and t.state=1 %s" %(tbName,versionCondition)
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

    context = pagination(sqlStr=execSql,attrList=checkList,page=page,pageNum=commonWebConfig.taskPageNum)
    response = render(request, "InterfaceTest/src_file_analyze/SubPages/HTTP_Select_Task_list_check_page.html",context)
    return response
