import django
import sys,os
rootpath = os.path.dirname(os.path.realpath(__file__)).replace("\\","/")
rootpath = rootpath.split("/apps")[0]
# print(rootpath)
syspath=sys.path
sys.path=[]
sys.path.append(rootpath) #指定搜索路径绝对目录
sys.path.extend([rootpath+i for i in os.listdir(rootpath) if i[0]!="."])#将工程目录下的一级目录添加到python搜索路径中
sys.path.extend(syspath)

from apps.common.func.WebFunc import *
from all_models.models import *
from apps.task.services.HTTP_taskService import HTTP_taskService

def getCoverage(resultDict,taskIdList,businessLine,module):
    if businessLine not in resultDict.keys():
        resultDict[businessLine] = {}
    # 标准接口
    standardSql = "SELECT i.interfaceUrl url,m.moduleName moduleName,b.bussinessLineName businessLineName,u.userName userName FROM tb_standard_interface i LEFT JOIN tb_modules m ON i.moduleId = m.id LEFT JOIN tb_business_line b ON i.businessLineId = b.id  LEFT JOIN tb_user u ON i.addBy = u.loginName WHERE 1=1 AND i.state=1"
    if businessLine != "":
        standardSql = '%s and b.bussinessLineName = "%s"' % (standardSql,businessLine)
    if module != "":
        standardSql = "%s and m.moduleName = '%s'" % (standardSql,module)
    standardData = executeSqlGetDict(standardSql, [])
    for dataIndex in standardData:
        dataIndex["standardIsCovered"] = False

    standardDataDict = {}

    # 生成标准dict
    for tmpInterfaceDict in standardData:
        tmpBusinessLine = tmpInterfaceDict['businessLineName']

        if tmpBusinessLine not in standardDataDict.keys():
            standardDataDict[tmpBusinessLine] = {"dataList": [], "businessLineCount": 0,
                                                 "businessLineIsCoveredCount": 0, "moduleDict": {}}
        standardDataDict[tmpBusinessLine]['dataList'].append(tmpInterfaceDict)
        standardDataDict[tmpBusinessLine]['businessLineCount'] += 1

    taskList = dbModelListToListDict(HTTP_taskService.getTaskListForTaskIdList(taskIdList))
    allInerfaceIdList = []
    allTestCaseIdList = []
    for taskIndex in range(0, len(taskList)):
        thisTaskInterfaceList = taskList[taskIndex]["taskInterfaces"].split(",")
        allInerfaceIdList.extend(thisTaskInterfaceList)
        thisTaskTestCaseList = taskList[taskIndex]["taskTestcases"].split(",")
        allTestCaseIdList.extend(thisTaskTestCaseList)

    #场景总数
    resultDict[businessLine]["testCaseSum"] = len(allTestCaseIdList)

    allInerfaceIdList = list(set(allInerfaceIdList))
    allTestCaseIdList = list(set(allTestCaseIdList))
    allstepIdList = []
    allstepList = HTTP_test_case_stepService.getTestCaseStepList(allTestCaseIdList)
    for stepIndex in range(0, len(allstepList)):
        allstepIdList.append(allstepList[stepIndex]["id"])

    #获取没去重的接口和步骤数量
    allInterfaceNotDistinctSql = "SELECT i.url url,b.bussinessLineName businessLineName,m.moduleName moduleName,u.userName userName FROM tb_http_interface i LEFT JOIN tb_business_line b ON i.businessLineId = b.id LEFT JOIN tb_modules m ON i.moduleId = m.id LEFT JOIN tb_user u ON i.addBy = u.loginName where i.state = 1 and i.caseType in (1,2) and i.interfaceId in ('%s') group by i.url,i.businessLineId,i.moduleId" % (
        "','".join(allInerfaceIdList))
    allInterfaceNotDistinctData = executeSqlGetDict(allInterfaceNotDistinctSql, [])
    allStepNotDisTinctSql = "SELECT i.url url,b.bussinessLineName businessLineName,m.moduleName moduleName,u.userName userName FROM tb_http_testcase_step i LEFT JOIN tb_business_line b ON i.businessLineId = b.id LEFT JOIN tb_modules m ON i.moduleId = m.id LEFT JOIN tb_user u ON i.addBy = u.loginName where i.state = 1 and i.caseType in (2,3) and i.id in ('%s') group by i.url,i.businessLineId,i.moduleId" % (
        "','".join((str(i) for i in allstepIdList)))
    allStepNotDisTinctData = executeSqlGetDict(allStepNotDisTinctSql, [])
    #设置没去重的用例总数
    resultDict[businessLine]["executeInterfaceSum"] = len(allInterfaceNotDistinctData) + len(allStepNotDisTinctData)

    allInterfaceSql = "SELECT i.url url,b.bussinessLineName businessLineName,m.moduleName moduleName,u.userName userName,count(DISTINCT b.bussinessLineName,m.moduleName,i.url ) FROM tb_http_interface i LEFT JOIN tb_business_line b ON i.businessLineId = b.id LEFT JOIN tb_modules m ON i.moduleId = m.id LEFT JOIN tb_user u ON i.addBy = u.loginName where i.state = 1 and i.caseType in (1,2) and i.interfaceId in ('%s') group by i.url,i.businessLineId,i.moduleId" % (
        "','".join(allInerfaceIdList))
    allInterfaceData = executeSqlGetDict(allInterfaceSql, [])
    allStepSql = "SELECT i.url url,b.bussinessLineName businessLineName,m.moduleName moduleName,u.userName userName,count(DISTINCT b.bussinessLineName,m.moduleName,i.url ) FROM tb_http_testcase_step i LEFT JOIN tb_business_line b ON i.businessLineId = b.id LEFT JOIN tb_modules m ON i.moduleId = m.id LEFT JOIN tb_user u ON i.addBy = u.loginName where i.state = 1 and i.caseType in (2,3) and i.id in ('%s') group by i.url,i.businessLineId,i.moduleId" % (
        "','".join((str(i) for i in allstepIdList)))
    allStepData = executeSqlGetDict(allStepSql, [])
    # 接口和步骤去重
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
    # 生成用户数据dict
    allDataDict = {}
    for tmpInterfaceDict in allInterfaceData:
        tmpInterfaceDict["standardIsCovered"] = False
        tmpBusinessLine = tmpInterfaceDict['businessLineName']
        if tmpBusinessLine not in allDataDict.keys():
            allDataDict[tmpBusinessLine] = {"dataList": [], "businessLineCount": 0, "businessLineIsCoveredCount": 0}
        allDataDict[tmpBusinessLine]['dataList'].append(tmpInterfaceDict)
        allDataDict[tmpBusinessLine]['businessLineCount'] += 1

    resultDict[businessLine]["allDataCount"] = len(allInterfaceData)
    resultDict[businessLine]["coverCount"] = 0  # 执行后生成
    resultDict[businessLine]["notCoverCount"] = 0  # 执行后还要重算
    resultDict[businessLine]["notStandardCount"] = 0  # 执行后还要重算
    for standardBLineKey, standardBLineValue in standardDataDict.items():
        # 遍历自己的业务线datalist生成业务线的覆盖率统计
        if standardBLineKey not in allDataDict:
            allDataDict[standardBLineKey] = {"dataList": [], "businessLineCount": 0, "businessLineIsCoveredCount": 0,"moduleDict": {}}
            continue
        # 先循环判断当期业务线的数据统计
        allBLineValue = allDataDict[standardBLineKey]
        for tmpAllUrlDict in allBLineValue['dataList']:
            for tmpStandardUrlDict in standardBLineValue['dataList']:
                if checkUrl(tmpStandardUrlDict['url']) == checkUrl(tmpAllUrlDict['url']) and tmpStandardUrlDict['businessLineName'] == tmpAllUrlDict['businessLineName'] and tmpStandardUrlDict['moduleName'] == tmpAllUrlDict['moduleName']:
                    tmpStandardUrlDict["standardIsCovered"] = True
                    tmpAllUrlDict["dataIsCovered"] = True
                    standardBLineValue["businessLineIsCoveredCount"] += 1
                    resultDict[businessLine]["coverCount"] += 1
                    continue
    
    resultDict[businessLine]["notCoverCount"] = len(standardData) - resultDict[businessLine]["coverCount"]
    resultDict[businessLine]["notStandardCount"] = len(allInterfaceData) - resultDict[businessLine]["coverCount"]


if __name__ == "__main__":

    #标准接口数量
    standardSql = "SELECT i.interfaceUrl url,m.moduleName moduleName,b.bussinessLineName businessLineName,u.userName userName FROM tb_standard_interface i LEFT JOIN tb_modules m ON i.moduleId = m.id LEFT JOIN tb_business_line b ON i.businessLineId = b.id  LEFT JOIN tb_user u ON i.addBy = u.loginName WHERE 1=1 AND i.apiStatus = 1 AND i.state=1 group by i.interfaceUrl,i.businessLineId,i.moduleId"
    standardData = executeSqlGetDict(standardSql, [])


    #所有接口步骤去重
    allInterfaceSql = "SELECT i.url url,b.bussinessLineName businessLineName,m.moduleName moduleName,u.userName userName,count(DISTINCT b.bussinessLineName,m.moduleName,i.url ) FROM tb_http_interface i LEFT JOIN tb_business_line b ON i.businessLineId = b.id LEFT JOIN tb_modules m ON i.moduleId = m.id LEFT JOIN tb_user u ON i.addBy = u.loginName where i.state = 1 and i.caseType in (1,2) group by i.url,i.businessLineId,i.moduleId"
    allData = executeSqlGetDict(allInterfaceSql,[])

    #所有步骤去重
    allStepSql = "SELECT i.url url,b.bussinessLineName businessLineName,m.moduleName moduleName,u.userName userName,count(DISTINCT b.bussinessLineName,m.moduleName,i.url ) FROM tb_http_testcase_step i LEFT JOIN tb_business_line b ON i.businessLineId = b.id LEFT JOIN tb_modules m ON i.moduleId = m.id LEFT JOIN tb_user u ON i.addBy = u.loginName where i.state = 1 and i.caseType in (2,3) group by i.url,i.businessLineId,i.moduleId"
    allStepData = executeSqlGetDict(allStepSql,[])


    # 步骤和接口去重
    stepDataLen = len(allStepData)
    for dataIndex in range(0, len(allData)):
        stepIndex = 0
        while stepIndex < stepDataLen:
            if allData[dataIndex]["businessLineName"] == allStepData[stepIndex]["businessLineName"]:
                if allData[dataIndex]["moduleName"] == allStepData[stepIndex]["moduleName"]:
                    if allData[dataIndex]["url"] == allStepData[stepIndex]["url"]:
                        del allStepData[stepIndex]
                        stepDataLen = len(allStepData)
            stepIndex += 1
    allData.extend(allStepData)

    allDataCount = len(allData)
    standardCount = len(standardData)
    coverCount = 0
    standardDataDict = {}

    for tmpInterfaceDict in standardData:
        tmpInterfaceDict["standardIsCovered"] = False
        tmpBusinessLine = tmpInterfaceDict['businessLineName']
        tmpModule = tmpInterfaceDict['moduleName']
        if tmpBusinessLine not in standardDataDict.keys():
            standardDataDict[tmpBusinessLine] = {"dataList":[],"businessLineCount":0,"businessLineIsCoveredCount":0}
        standardDataDict[tmpBusinessLine]['dataList'].append(tmpInterfaceDict)
        standardDataDict[tmpBusinessLine]['businessLineCount'] += 1

    allDataDict = {}
    for tmpInterfaceDict in allData:
        tmpInterfaceDict["standardIsCovered"] = False
        tmpBusinessLine = tmpInterfaceDict['businessLineName']
        tmpModule = tmpInterfaceDict['moduleName']
        if tmpBusinessLine not in allDataDict.keys():
            allDataDict[tmpBusinessLine] = {"dataList":[],"businessLineCount":0,"businessLineIsCoveredCount":0}
        allDataDict[tmpBusinessLine]['dataList'].append(tmpInterfaceDict)
        allDataDict[tmpBusinessLine]['businessLineCount'] += 1

    #开始遍历标准字典了！
    for standardBLineKey, standardBLineValue in standardDataDict.items():
        #遍历自己的业务线datalist生成业务线的覆盖率统计
        #if panduan shifou you key
        if standardBLineKey not in allDataDict:
            allDataDict[standardBLineKey] = {"dataList":[],"businessLineCount":0,"businessLineIsCoveredCount":0}
            continue
            # pass
        allBLineValue = allDataDict[standardBLineKey]
        for tmpStandardUrlDict in standardBLineValue['dataList']:
            for tmpAllUrlDict in allBLineValue['dataList']:
                if checkUrl(tmpStandardUrlDict['url']) == checkUrl(tmpAllUrlDict['url']) and tmpStandardUrlDict["moduleName"] == tmpAllUrlDict["moduleName"]:
                    tmpStandardUrlDict["standardIsCovered"] = True
                    tmpAllUrlDict["dataIsCovered"] = True
                    standardBLineValue["businessLineIsCoveredCount"] += 1
                    coverCount += 1
    allBusinessLine = dbModelListToListDict(TbBusinessLine.objects.filter(state=1))
    now_time = datetime.datetime.now()
    yes_time = now_time + datetime.timedelta(days=-1)
    resultDict = {}
    for blIndex in allBusinessLine:
        if blIndex["bussinessLineName"] not in standardDataDict.keys():
            standardDataDict[blIndex["bussinessLineName"]] = {"businessCovered": 0,"notStandardBl":True,"businessLineCount":0,"businessLineIsCoveredCount":0}
    for standardKey,standardValue in standardDataDict.items():
        for dataKey,dataValue in allDataDict.items():
            if "notStandardBl" in standardValue.keys():
                continue
            if dataKey == standardKey:
                standardValue["businessCovered"] =  0
                standardValue["businessNotCovered"] = standardValue["businessLineCount"] - standardValue["businessLineIsCoveredCount"]
                standardValue["notStandardCount"] = dataValue["businessLineCount"] - standardValue["businessLineIsCoveredCount"]
                if standardValue["businessLineCount"] != 0:
                    standardValue["businessCovered"] =  "%.2f" % (standardValue["businessLineIsCoveredCount"] / standardValue["businessLineCount"] * 100)
                    # 获取用例总数
        # 所有接口步骤去重
        allInterfaceNumSql = "SELECT i.url url,b.bussinessLineName businessLineName,m.moduleName moduleName,u.userName userName FROM tb_http_interface i LEFT JOIN tb_business_line b ON i.businessLineId = b.id LEFT JOIN tb_modules m ON i.moduleId = m.id LEFT JOIN tb_user u ON i.addBy = u.loginName where i.state = 1 and b.bussinessLineName = '%s' and i.caseType in (1,2) " % standardKey
        allNumData = executeSqlGetDict(allInterfaceNumSql, [])

        # 所有步骤去重
        allStepNumSql = "SELECT i.url url,b.bussinessLineName businessLineName,m.moduleName moduleName,u.userName userName FROM tb_http_testcase_step i LEFT JOIN tb_business_line b ON i.businessLineId = b.id LEFT JOIN tb_modules m ON i.moduleId = m.id LEFT JOIN tb_user u ON i.addBy = u.loginName where i.state = 1 and b.bussinessLineName = '%s' and i.caseType in (2,3)" % standardKey
        allStepNumData = executeSqlGetDict(allStepNumSql, [])
        interfaceNum = len(allNumData) + len(allStepNumData)

        resultDict[standardKey] = {}
        resultDict[standardKey]["businessLine"] = standardKey
        resultDict[standardKey]["standardInterfaceNum"] = standardValue["businessLineCount"]
        resultDict[standardKey]["coveredInterfaceNum"] = standardValue["businessLineIsCoveredCount"]
        resultDict[standardKey]["coverage"] = standardValue["businessCovered"]
        resultDict[standardKey]["allDataCount"] = 0
        resultDict[standardKey]["coverCount"] = 0
        resultDict[standardKey]["notStandardCount"] = 0
        resultDict[standardKey]["notCoverCount"] = 0
        resultDict[standardKey]["executeInterfaceSum"] = 0
        resultDict[standardKey]["interfaceNum"] = interfaceNum
        resultDict[standardKey]["testCaseSum"] = 0

    allStandardTaskData = dbModelListToListDict(TbWebPortalTask.objects.filter(state=1))
    taskDict = {}
    for index in allStandardTaskData:
        if index["businessLine"] not in taskDict.keys():
            taskDict[index["businessLine"]] = {"taskList": [], "team": {}}
        if index["taskId"] not in taskDict[index["businessLine"]]["taskList"]:
            taskDict[index["businessLine"]]["taskList"].append(index["taskId"])
        if index["team"] not in taskDict[index["businessLine"]].keys():
            taskDict[index["businessLine"]]["team"][index["team"]] = {"taskList": []}
            taskDict[index["businessLine"]]["team"][index["team"]]["taskList"].append(index["taskId"])

    for taskKey, taskValue in taskDict.items():
        getCoverage(resultDict,taskValue["taskList"], taskKey, "")

    now_time = datetime.datetime.now()
    yes_time = now_time + datetime.timedelta(days=-1)
    #写入数据库
    for blKey,blValue in resultDict.items():
        webPortalPlatformInterfaceCovered = TbWebPortalPlatformInterfaceCovered()
        webPortalPlatformInterfaceCovered.businessLine = blValue["businessLine"]
        webPortalPlatformInterfaceCovered.standardInterfaceNum = blValue["standardInterfaceNum"]
        webPortalPlatformInterfaceCovered.coveredInterfaceNum = blValue["coveredInterfaceNum"]
        webPortalPlatformInterfaceCovered.coverage = blValue["coverage"]
        webPortalPlatformInterfaceCovered.executeInterfaceNum = blValue["coverCount"]
        if blValue["standardInterfaceNum"] == 0:
            webPortalPlatformInterfaceCovered.executeInterfaceCoverage = "%.2f" % 0
        else:
            webPortalPlatformInterfaceCovered.executeInterfaceCoverage = "%.2f" % (blValue["coverCount"]/ blValue["standardInterfaceNum"]*100)
        webPortalPlatformInterfaceCovered.interfaceNum = blValue["interfaceNum"]
        webPortalPlatformInterfaceCovered.executeInterfaceSum = blValue["executeInterfaceSum"]
        webPortalPlatformInterfaceCovered.testCaseSum = blValue["testCaseSum"]
        webPortalPlatformInterfaceCovered.statisticalTime = yes_time
        webPortalPlatformInterfaceCovered.version = dbModelToDict(TbVersion.objects.filter(type=2)[0])["versionName"]
        webPortalPlatformInterfaceCovered.save()
    print("done!")