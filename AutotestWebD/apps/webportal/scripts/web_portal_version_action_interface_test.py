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
import json
if __name__ == "__main__":
    now_time = datetime.datetime.now()
    now_timeStr = datetime.datetime.now().strftime('%Y-%m-%d 00:00:00')
    yes_time = now_time + datetime.timedelta(days=-1)
    #获取所有环境
    versionList = dbModelListToListDict(TbWebPortalStandardEnv.objects.filter(state=1))
    # print(versionList)

    #获取每个环境中的标准接口
    # versionDict = {}
    # for versionIndex in versionList:
    #     if versionIndex["version"] not in versionDict.keys():
    #         versionDict[versionIndex["version"]] = WebPortalService.getVersionStandardData(versionIndex["version"])

    #获取环境对应的task的测试结果
    allEnv = dbModelListToListDict(TbWebPortalStandardEnv.objects.filter(state=1,actionIsShow=1).order_by("lineSort"))
    print("allEnv:", allEnv)
    #获取所有环境包含的版本
    envVersionList = []
    for envIndex in allEnv:
        if envIndex["version"] not in envVersionList:
            envVersionList.append(envIndex["version"])
    #那当前需要的多版本的所有任务
    allTaskList = dbModelListToListDict(TbWebPortalStandardTask.objects.filter(state=1,version__in=envVersionList))

    taskDataDict = {}
    for taskIndex in allTaskList:
        if taskIndex["businessLine"] not in taskDataDict.keys():
            taskDataDict[taskIndex["businessLine"]] = {"envTest":{},"taskTestDetail":{}}
        if taskIndex["taskId"] not in taskDataDict[taskIndex["businessLine"]]["taskTestDetail"].keys():
            taskDataDict[taskIndex["businessLine"]]["taskTestDetail"][taskIndex["taskId"]] = {"taskTest":{}}
        for envIndex in allEnv:
            #获取当前环境要执行的任务list
            thisEnvRunTaskList = []
            thisEnvRunTaskData = dbModelListToListDict(TbWebPortalStandardTask.objects.filter(state=1,version=envIndex["version"]))
            for thisEnvRunTaskIndex in thisEnvRunTaskData:
                thisEnvRunTaskList.append(thisEnvRunTaskIndex["taskId"])
            try:
                taskName = dbModelToDict(TbTask.objects.filter(taskId=taskIndex["taskId"])[0])["title"]
            except Exception as e:
                print("没获取到任务 任务Id %s" % taskIndex["taskId"])
                taskName = taskIndex["taskId"]
            #如果任务不存在于环境要执行的list里，则返回
            taskDataDict[taskIndex["businessLine"]]["taskTestDetail"][taskIndex["taskId"]]["taskName"] = taskName
            taskDataDict[taskIndex["businessLine"]]["taskTestDetail"][taskIndex["taskId"]]["head"] = taskIndex["head"]
            if taskIndex["taskId"] not in thisEnvRunTaskList:
                taskDataDict[taskIndex["businessLine"]]["taskTestDetail"][taskIndex["taskId"]]["taskTest"][envIndex["httpConfKey"]] = {"alias":envIndex["alias"],"testResult":"NOTENV","testResultMsg":"{}","testReportUrl":"","passExecuteInterfaceNum":0,"allExecuteInterfaceNum":0,"actionIsShow":envIndex["actionIsShow"]}
                continue
            taskDataDict[taskIndex["businessLine"]]["taskTestDetail"][taskIndex["taskId"]]["taskTest"][envIndex["httpConfKey"]] = {"alias":envIndex["alias"],"testResult":"","passingRate":"","actionIsShow":envIndex["actionIsShow"]}
            if dbModelToDict(TbVersion.objects.filter(state=1,versionName=envIndex["version"])[0])["type"] == 2:
                thisVersion = "CurrentVersion"
            else:
                thisVersion = envIndex["version"]

            # lastExecuteTask = TbTaskExecute.objects.filter(state=1).filter(taskId=taskIndex["taskId"]).filter(httpConfKey=envIndex["httpConfKey"],version=thisVersion).filter(addTime__gt=now_timeStr).last()
            lastExecuteTask = TbTaskExecute.objects.filter(state=1).filter(taskId=taskIndex["taskId"]).filter(httpConfKey=envIndex["httpConfKey"],version=thisVersion).last()

            if not lastExecuteTask:
                taskExecuteData = {"testResult":"NOTRUN","testResultMsg":"{}","testReportUrl":"","toDayExecute":False}
            else:
                taskExecuteData = dbModelToDict(lastExecuteTask)
                if taskExecuteData["addTime"] > now_timeStr:
                    # print(taskExecuteData)
                    taskExecuteData["toDayExecute"] = True
                else:
                    taskExecuteData["toDayExecute"] = False
            # if taskIndex["taskId"] == "HTTP_TASK_27" and envIndex["httpConfKey"] == "httpIntegration":
            #     print("===========================")
            #     print(taskIndex["taskId"])
            #     print(envIndex["httpConfKey"])
            #     print(thisVersion)
            #     print(now_timeStr)
            #     print(taskExecuteData)
            # if taskIndex["taskId"] == "HTTP_TASK_27" and envIndex["httpConfKey"] == "httpIntegration":
                # print(taskExecuteData)
            taskId = taskDataDict[taskIndex["businessLine"]]["taskTestDetail"][taskIndex["taskId"]]["taskTest"][envIndex["httpConfKey"]]
            taskId["testResult"] = taskExecuteData["testResult"]
            taskId["toDayExecute"] = taskExecuteData["toDayExecute"]
            # if taskIndex["taskId"] == "HTTP_TASK_27" and envIndex["httpConfKey"] == "httpIntegration":
            #     print(taskExecuteData["testResult"])
            try:
                taskExecuteResult = json.loads(taskExecuteData["testResultMsg"])
            except Exception as e:
                taskExecuteResult = {}
            if "interfaceExecuteSummary" not in taskExecuteResult.keys():
                taskExecuteResult["interfaceExecuteSummary"] = {"total": 0, "pass": 0, "fail": 0, "error": 0,"notrun": 0}
            if "testcaseStepExecuteSummary" not in taskExecuteResult.keys():
                taskExecuteResult["testcaseStepExecuteSummary"] = {"total": 0, "pass": 0, "fail": 0, "error": 0,"notrun": 0}
            taskId["env"] = envIndex["httpConfKey"]
            taskId["allExecuteInterfaceNum"] = taskExecuteResult["interfaceExecuteSummary"]["total"] + taskExecuteResult["testcaseStepExecuteSummary"]["total"]
            taskId["passExecuteInterfaceNum"] = taskExecuteResult["interfaceExecuteSummary"]["pass"] + taskExecuteResult["testcaseStepExecuteSummary"]["pass"]
            taskId["failExecuteInterfaceNum"] = taskExecuteResult["interfaceExecuteSummary"]["fail"] + taskExecuteResult["testcaseStepExecuteSummary"]["fail"]
            taskId["errorExecuteInterfaceNum"] = taskExecuteResult["interfaceExecuteSummary"]["error"] + taskExecuteResult["testcaseStepExecuteSummary"]["error"]
            taskId["notrunExecuteInterfaceNum"] = taskExecuteResult["interfaceExecuteSummary"]["notrun"] + taskExecuteResult["testcaseStepExecuteSummary"]["notrun"]

            taskId["testReportUrl"] = taskExecuteData["testReportUrl"]
            if taskId["allExecuteInterfaceNum"] == 0:
                taskId["passingRate"] = 0
            else:
                taskId["passingRate"] = '%.2f' % (
                taskId["passExecuteInterfaceNum"] / taskId["allExecuteInterfaceNum"] * 100)

    allBlDict = dbModelListToListDict(TbBusinessLine.objects.filter(state=1))
    # 用标准的业务线赋值字典 看有没有遗漏的业务线
    for blIndex in allBlDict:
        if blIndex["bussinessLineName"] not in taskDataDict.keys():
            taskDataDict[blIndex["bussinessLineName"]] = {"envTest": {}, "taskTestDetail": {}}
            for envIndex in allEnv:
                if envIndex["httpConfKey"] not in taskDataDict[blIndex["bussinessLineName"]]["envTest"].keys():
                    taskDataDict[blIndex["bussinessLineName"]]["envTest"][envIndex["httpConfKey"]] = {
                        "alias": envIndex["alias"], "testResult": "NOTRUN", "passingRate": 0, "taskResultList": [],"allNum": 0, "passNum": 0,"actionIsShow":envIndex["actionIsShow"]}

    # 生成大字典的数据
    for blIndexKey, blIndexValue in taskDataDict.items():
        for envIndex in allEnv:
            if envIndex["httpConfKey"] not in blIndexValue["envTest"].keys():
                blIndexValue["envTest"][envIndex["httpConfKey"]] = {"passNum": 0, "allNum": 0, "taskResultList": [],"version":envIndex["version"],"testResult":"","actionIsShow":envIndex["actionIsShow"]}
            for taskKey, taskValue in blIndexValue["taskTestDetail"].items():
                blIndexValue["envTest"][envIndex["httpConfKey"]]["passNum"] += taskValue["taskTest"][envIndex["httpConfKey"]]["passExecuteInterfaceNum"]
                blIndexValue["envTest"][envIndex["httpConfKey"]]["allNum"] += taskValue["taskTest"][envIndex["httpConfKey"]]["allExecuteInterfaceNum"]
                blIndexValue["envTest"][envIndex["httpConfKey"]]["taskResultList"].append(taskValue["taskTest"][envIndex["httpConfKey"]]["testResult"])

        for envIndex in allEnv:
            blResult = blIndexValue["envTest"][envIndex["httpConfKey"]]
            blResultList = blIndexValue["envTest"][envIndex["httpConfKey"]]["taskResultList"]
            if "EXCEPTION" in blResultList:
                blResult["testResult"] = "EXCEPITON"
            elif "ERROR" in blResultList:
                blResult["testResult"] = "ERROR"
            elif "FAIL" in blResultList:
                blResult["testResult"] = "FAIL"
            elif "PASS" in blResultList:
                blResult["testResult"] = "PASS"
            elif "NOTRUN" in blResultList:
                blResult["testResult"] = "NOTRUN"

            if blResult["testResult"] == "PASS":
                blResult["passingRate"] = "%.2f" % 100
            else:
                if blResult["allNum"] == 0:
                    blResult["passingRate"] = 0
                else:
                    blResult["passingRate"] = "%.2f" % (blResult["passNum"] / blResult["allNum"] * 100)
        webPortalActionInterface = TbWebPortalActionInterfaceTest()
        webPortalActionInterface.businessLine = blIndexKey
        webPortalActionInterface.envTestDetail = json.dumps(blIndexValue)
        webPortalActionInterface.statisticalTime = yes_time
        webPortalActionInterface.save()
    print("taskDataDict:",taskDataDict)
    print("done!")
