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
from apps.webportal.services.webPortalService import WebPortalService
from all_models.models import *
from apps.task.services.HTTP_taskService import HTTP_taskService

if __name__ == "__main__":

    #获取标准接口数量
    # 查询标准接口
    dataDict = getAllApiCountsNumConfig()
    standardCountSum = dataDict["allCount"]
    print("dataDict:",dataDict)


    standardSql = "SELECT i.interfaceUrl url,m.moduleName moduleName,b.bussinessLineName businessLineName,u.userName userName FROM tb_standard_interface i LEFT JOIN tb_modules m ON i.moduleId = m.id LEFT JOIN tb_business_line b ON i.businessLineId = b.id  LEFT JOIN tb_user u ON i.addBy = u.loginName WHERE i.state=1"
    standardData = executeSqlGetDict(standardSql, [])
    print("standardData:", standardData)
    standardCount = len(standardData)

    #获取维护中的接口总数
    maintenanceCount = len(TbStandardInterface.objects.filter(apiStatus=1,state=1))
    print("maintenanceCount:", maintenanceCount)

    #获取废弃接口总数
    abandonedCount = len(TbStandardInterface.objects.filter(apiStatus=0,state=1))
    print("abandonedCount:", abandonedCount)

    #获取无注释接口总数
    noAnnotationCount = standardCountSum - maintenanceCount - abandonedCount
    print("noAnnotationCount:", noAnnotationCount)

    #获取已覆盖接口数
    t1 = time.time()
    allInterfaceSql = "SELECT i.url url,b.bussinessLineName businessLineName,m.moduleName moduleName,u.userName userName,count(DISTINCT b.bussinessLineName,m.moduleName,i.url ) FROM tb_http_interface i LEFT JOIN tb_business_line b ON i.businessLineId = b.id LEFT JOIN tb_modules m ON i.moduleId = m.id LEFT JOIN tb_user u ON i.addBy = u.loginName WHERE i.state = 1 AND i.caseType IN (1,2) group by i.url,i.businessLineId,i.moduleId"
    allData = executeSqlGetDict(allInterfaceSql, [])
    t2 = time.time()
    # print("(查询接口)t2-t1:%d" % (t2 - t1))

    allStepSql = "SELECT i.url url,b.bussinessLineName businessLineName,m.moduleName moduleName,u.userName userName FROM tb_http_testcase_step i LEFT JOIN tb_business_line b ON i.businessLineId = b.id LEFT JOIN tb_modules m ON i.moduleId = m.id LEFT JOIN tb_user u ON i.addBy = u.loginName WHERE i.state = 1 AND i.caseType IN (2,3) group by i.url,i.businessLineId,i.moduleId"
    allStepData = executeSqlGetDict(allStepSql, [])
    # allData.extend(createSqlDict(checkArr,orderBy,allStepSql,"group by i.url"))
    t3 = time.time()
    # print("(查询step接口)t3-t2:%d" % (t3 - t2))

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
    t4 = time.time()
    # print("(接口步骤去重)t4-t3:%d" % (t4 - t3))

    t5 = time.time()
    # print("(查询标准)t5-t4:%d" % (t5 - t4))

    allDataCount = len(allData)
    coverCount = 0

    # 计算有多少覆盖的接口
    for interfaceIndex in allData:
        for standardIndex in standardData:
            if standardIndex["businessLineName"] == interfaceIndex["businessLineName"]:
                if standardIndex["moduleName"] == interfaceIndex["moduleName"]:
                    if standardIndex["url"] == interfaceIndex["url"]:
                        coverCount += 1

    #接口覆盖率
    platformCoverageRate = '%.2f' % (coverCount / maintenanceCount * 100)
    print("platformCoverageRate:", platformCoverageRate)

    #执行用例接口总数
    standardTaskNum = len(TbWebPortalTask.objects.filter(state=1))
    print("standardTaskNum:", standardTaskNum)


    #执行用例平均数


    #平台覆盖标准接口数量

    #
    # #平台接口覆盖率
    #
    # #平台接口总数量
    # platformInterfaceNum = len(TbHttpInterface.objects.filter(caseType__in=[1,2]).filter(state=1))+len(TbHttpTestcaseStep.objects.filter(caseType__in=[2,3]).filter(state=1))
    #
    # #接口平均用例数
    # interfaceAverageTestCaseNum = round(platformInterfaceNum / standardCount)
    #
    #标准任务数量
    #
    #标准任务已覆盖接口数量
    standardTaskList = dbModelListToListDict(TbWebPortalTask.objects.filter(state=1))
    standardTaskIdList = []
    for index in standardTaskList:
        standardTaskIdList.append(index["taskId"])
    print("standardTaskIdList:", standardTaskIdList)
    taskList = dbModelListToListDict(HTTP_taskService.getTaskListForTaskIdList(standardTaskIdList))
    print("taskList:", taskList)
    allInerfaceIdList = []
    allTestCaseIdList = []
    for taskIndex in range(0, len(taskList)):
        thisTaskInterfaceList = taskList[taskIndex]["taskInterfaces"].split(",")
        allInerfaceIdList.extend(thisTaskInterfaceList)
        thisTaskTestCaseList = taskList[taskIndex]["taskTestcases"].split(",")
        allTestCaseIdList.extend(thisTaskTestCaseList)

    allInerfaceIdList = list(set(allInerfaceIdList))
    allTestCaseIdList = list(set(allTestCaseIdList))
    print("allInerfaceIdList:", allInerfaceIdList)

    t4 = time.time()
    # print("[通过caseIdList获取所有步骤]t4-t3:%f" % (t4 - t3))
    taskAllInterfaceSql = "SELECT i.url url,b.bussinessLineName businessLineName,m.moduleName moduleName,u.userName userName,count(DISTINCT b.bussinessLineName,m.moduleName,i.url ) FROM tb_http_interface i LEFT JOIN tb_business_line b ON i.businessLineId = b.id LEFT JOIN tb_modules m ON i.moduleId = m.id LEFT JOIN tb_user u ON i.addBy = u.loginName where i.state = 1 and i.caseType in (1,2) and i.interfaceId in ('%s') group by i.url,i.businessLineId,i.moduleId" % (
    "','".join(allInerfaceIdList))
    print("eeeeeeeeeeee:", "','".join(allInerfaceIdList))
    taskAllInterfaceData = executeSqlGetDict(taskAllInterfaceSql, [])
    print("taskAllInterfaceData:", taskAllInterfaceData)
    taskAllStepSql = "SELECT i.url url,b.bussinessLineName businessLineName,m.moduleName moduleName,u.userName userName,count(DISTINCT b.bussinessLineName,m.moduleName,i.url ) FROM tb_http_testcase_step i LEFT JOIN tb_business_line b ON i.businessLineId = b.id LEFT JOIN tb_modules m ON i.moduleId = m.id LEFT JOIN tb_user u ON i.addBy = u.loginName where i.state = 1 and i.caseType in (2,3) and i.caseId in ('%s') group by i.url,i.businessLineId,i.moduleId" % (
    "','".join((str(i) for i in allTestCaseIdList)))
    taskAllStepData = executeSqlGetDict(taskAllStepSql, [])
    print("taskAllStepData:", taskAllStepData)
    # 接口和步骤去重
    stepAllDataLen = len(taskAllStepData)
    for dataIndex in range(0, len(taskAllInterfaceData)):
        stepIndex = 0
        while stepIndex < stepAllDataLen:
            if taskAllInterfaceData[dataIndex]["businessLineName"] == taskAllStepData[stepIndex]["businessLineName"]:
                if taskAllInterfaceData[dataIndex]["moduleName"] == taskAllStepData[stepIndex]["moduleName"]:
                    if taskAllInterfaceData[dataIndex]["url"] == taskAllStepData[stepIndex]["url"]:
                        del taskAllStepData[stepIndex]
                        stepAllDataLen = len(taskAllStepData)
            stepIndex += 1
    taskAllInterfaceData.extend(taskAllStepData)
    executeInterfaceNum = 0
    #计算已执行的接口数量
    for interfaceIndex in taskAllInterfaceData:
        for standardIndex in standardData:
            if standardIndex["businessLineName"] == interfaceIndex["businessLineName"]:
                if standardIndex["moduleName"] == interfaceIndex["moduleName"]:
                    if checkUrl(standardIndex["url"]) == checkUrl(interfaceIndex["url"]):
                        executeInterfaceNum += 1

    if len(taskAllInterfaceData) == 1:
        if taskAllInterfaceData[0]["url"] == None:
            taskAllInterfaceData = []
    # taskCoverCount = 0
    # # 计算有多少覆盖的接口
    # for interfaceIndex in taskAllInterfaceData:
    #     for standardIndex in standardData:
    #         if standardIndex["businessLineName"] == interfaceIndex["businessLineName"]:
    #             if standardIndex["moduleName"] == interfaceIndex["moduleName"]:
    #                 if standardIndex["url"] == interfaceIndex["url"]:
    #                     taskCoverCount += 1

    #标准任务未覆盖接口数量
    # standardTaskNotCoveredStandardNum = standardCount - taskCoverCount

    #平台任务接口覆盖率
    # platformTaskCoverage = '%.2f' % (executeInterfaceNum / standardCount * 100)
    #
    # #标准任务接口总数量
    standardTaskInterfaceList = []
    standardTaskInterfaceList.extend(dbModelListToListDict(TbHttpInterface.objects.filter(interfaceId__in=allInerfaceIdList).filter(state=1)))
    standardTaskInterfaceList.extend(dbModelListToListDict(TbHttpTestcaseStep.objects.filter(caseId__in=allTestCaseIdList).filter(state=1)))
    standardTaskInterfaceNum = len(standardTaskInterfaceList)
    # print("没去重的接口数%s" % standardTaskInterfaceNum)
    #
    #
    # print("接口总数  %s" % standardCount) #标准接口总数量
    # print("平台已覆盖数量  %s" % coverCount)  #平台总覆盖
    # print("平台接口覆盖率  %s" % platformCoverage)  #已覆盖接口数除以标准接口总数
    # print("已执行接口数量  %s" % executeInterfaceNum) #标准任务中的接口和用例步骤
    # print("用例执行接口覆盖率  %s" % platformTaskCoverage)  #标准任务中的接口和用例步骤去重 除以 标准接口数
    # print("用例总数  %s" % platformInterfaceNum)  #平台上的所有接口和步骤不去重的总数
    # print("用例平均数  %.2f" % (platformInterfaceNum/coverCount))  #平台上所有接口步骤除以标准接口数量
    # print("执行用例总数  %s" % standardTaskInterfaceNum)  #任务中的接口步骤不去重
    # print("执行用例平均数  %.2f " % (standardTaskInterfaceNum/executeInterfaceNum))  #执行用例总数 除以 已执行接口数
    # print("场景总数  %s" % len(dbModelListToListDict(TbHttpTestcase.objects.filter(state=1).filter(caseType__in=[1,2]))))
    # print("已执行的场景总数  %s" % len(allTestCaseIdList))
    # now_time = datetime.datetime.now()
    # yes_time = now_time + datetime.timedelta(days=-1)
    #
    # tbModule = TbWebPortalActionInterfaceGeneralSituation()
    # tbModule.standardInterfaceNum = standardCount
    # tbModule.platformCoveredStandardNum = coverCount
    # tbModule.platformCoverage = platformCoverage
    # tbModule.executeInterfaceNum = executeInterfaceNum
    # tbModule.executeInterfaceCoverage = platformTaskCoverage
    # tbModule.platformInterfaceNum = platformInterfaceNum
    # tbModule.platformInterfaceAverageStandardInterface = "%.2f" % (platformInterfaceNum/coverCount)
    # tbModule.executeInterfaceSum = standardTaskInterfaceNum
    # tbModule.executeInterfaceAverage = "%.2f" % (standardTaskInterfaceNum/executeInterfaceNum)
    # tbModule.testCaseNum = len(dbModelListToListDict(TbHttpTestcase.objects.filter(state=1).filter(caseType__in=[1,2])))
    # tbModule.executeTestCaseNum = len(allTestCaseIdList)
    # tbModule.statisticalTime = yes_time
    # tbModule.version = dbModelToDict(TbVersion.objects.filter(type=2)[0])["versionName"]
    # tbModule.save()

    statisticalDetail = {"standardCount":standardCountSum,"maintenanceCount":maintenanceCount,"abandonedCount":abandonedCount,"noAnnotationCount":noAnnotationCount,
                         "coverCount":coverCount,"platformCoverageRate":platformCoverageRate,"standardTaskInterfaceNum":executeInterfaceNum,"executeInterfaceAverage":standardTaskInterfaceNum//executeInterfaceNum}
    # print(coverCount)
    tbModel = TbWebPortalActionInterfaceGeneralSituation()
    tbModel.statisticalDetail = json.dumps(statisticalDetail)
    print("tbModel.statisticalDetail :", tbModel.statisticalDetail )
    tbModel.version = dbModelToDict(TbVersion.objects.get(type=2))["versionName"]
    tbModel.save()
    print("done!")
    #概况表完成================================================================================




