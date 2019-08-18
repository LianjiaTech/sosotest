import apps.common.func.InitDjango
from all_models.models import TbTaskExecute
from apps.common.func.CommonFunc import *
from apps.task.services.HTTP_taskService import HTTP_taskService

class HTTP_task_executeService(object):

    @staticmethod
    def findTaskRestltForId(id):
        taskExecuteData = TbTaskExecute.objects.filter(id=id)
        return taskExecuteData[0]

    @staticmethod
    def againRunTask(id,addBy,addByName):
        taskExecuteData = dbModelToDict(TbTaskExecute.objects.filter(id=id)[0])
        taskId = taskExecuteData['taskId']
        if taskExecuteData['version'] == "CurrentVersion":
            tmpTask = HTTP_taskService.getTaskForTaskId(taskId)
            if not tmpTask :
                return False
            taskData = dbModelToDict(tmpTask)
            taskData['version'] = "CurrentVersion"
        else:
            tmpTask = HTTP_taskService.getVersionTaskForTaskId(taskId,taskExecuteData['version'])
            if not tmpTask:
                return False
            taskData = dbModelToDict(tmpTask)
            del taskData['versionName_id']
            taskData['version'] = taskExecuteData['version']


        if taskData["state"] == 0:
            return False

        del taskData["id"]
        del taskData["addTime"]
        del taskData["modTime"]
        taskData["taskId"] = taskExecuteData["taskId"]
        taskData["addBy_id"] = addBy
        taskData["addByName"] = addByName
        taskData["execBy_id"] = addBy
        taskData["execByName"] = addByName
        taskData["httpConfKey_id"] = taskExecuteData["httpConfKey_id"]
        taskData["httpConfKeyAlias"] = taskExecuteData["httpConfKeyAlias"]
        taskData["isSaveHistory"] = taskExecuteData["isSaveHistory"]
        taskData["isSendEmail"] = taskExecuteData["isSendEmail"]
        taskData["execComments"] = taskExecuteData["execComments"]
        taskData["retryCount"] = taskExecuteData["retryCount"]
        taskData["testResultMsg"] = ""
        taskData["performanceResult"] = "N/A"
        taskData["modBy"] = addBy
        taskData["modByName"] = addByName
        addResult = TbTaskExecute.objects.create(**taskData)
        return addResult

    @staticmethod
    def updateFailExecute(id,data):
        tb = TbTaskExecute.objects.get(id=id)
        tb.execStatus = 4
        tb.testResult = "EXCEPTION"
        tb.testResultMsg = data
        tb.save()

    @staticmethod
    def stopTaskRun(id):
        tb = TbTaskExecute.objects.get(id=id)
        tb.execStatus = 10
        tb.testResult = "CANCEL"
        tb.testResultMsg = "任务取消"
        tb.execFinishTime = datetime.datetime.now()
        tb.save()
        

    @staticmethod
    def taskRunAdd(taskData):
        result = TbTaskExecute.objects.create(**taskData)
        return result

    @staticmethod
    def queryPeopleTaskExecute(now_pageNum, pageNum, loginName):
        limit = ('%d,%d' % (now_pageNum * pageNum, pageNum))
        execSql = 'SELECT u.loginName , u.userName, c.count from tb_user u LEFT JOIN (SELECT addBy as loginName,COUNT(*) as count FROM tb_task_execute where state=1 GROUP BY addBy ) c on u.loginName = c.loginName WHERE u.state = 1 and c.count>0 and u.loginName != "%s" order by c.count desc LIMIT %s ;' % (
            loginName, limit)
        resultDict = executeSqlGetDict(execSql, [])
        return resultDict



    @staticmethod
    def contrastTask(taskIdList):
        try:
            leftTaskData = HTTP_task_executeService.findTaskRestltForId(taskIdList[0]).testResultMsg
            leftTask = json.loads(leftTaskData)["taskContrastDict"]
            rightTaskData = HTTP_task_executeService.findTaskRestltForId(taskIdList[1]).testResultMsg
            rightTask = json.loads(rightTaskData)["taskContrastDict"]
        except Exception as e:
            return {"code":10001,"message":"历史任务不可做比对"}
        leftExecuteSummary = json.loads(leftTaskData)["totalExecuteSummary"]
        if leftExecuteSummary["total"] != 0:
            leftExecuteSummary["passRate"] = "%.2f" % (leftExecuteSummary["pass"]/leftExecuteSummary["total"]*100)
        else:
            leftExecuteSummary["passRate"] = "%.2f" % 0

        rightExecuteSummary = json.loads(rightTaskData)["totalExecuteSummary"]
        if rightExecuteSummary["total"] != 0:
            rightExecuteSummary["passRate"] = "%.2f" % (rightExecuteSummary["pass"]/rightExecuteSummary["total"]*100)
        else:
            rightExecuteSummary["passRate"] = "%.2f" % 0


        resultDict = {"contrast": {}, "noContrast": {},"leftTaskExecuteId":taskIdList[0],"rightTaskExecuteId":taskIdList[1],"leftExecuteSummary":leftExecuteSummary,"rightExecuteSummary":rightExecuteSummary}
        for tmpLeftKey, tmpLeftValue in leftTask.items():
            for tmpRightKey, tmpRightValue in rightTask.items():
                if tmpLeftKey == tmpRightKey:
                    resultDict["contrast"][tmpLeftKey] = {}
                    resultDict["contrast"][tmpLeftKey]["title"] = tmpLeftValue["title"]
                    resultDict["contrast"][tmpLeftKey]["result"] = []

                    for index in range(0, len(tmpLeftValue["result"])):
                        if len(tmpRightValue["result"]) > index:
                            tmpDict = {"left": tmpLeftValue["result"][index], "right": tmpRightValue["result"][index]}
                            if tmpLeftValue["result"][index] == tmpRightValue["result"][index]:
                                tmpDict["result"] = "PASS"
                            else:
                                tmpDict["result"] = "FAIL"

                            tmpLeftValue["result"][index]["isContrast"] = True
                            tmpRightValue["result"][index]["isContrast"] = True
                            resultDict["contrast"][tmpLeftKey]["result"].append(tmpDict)

        for tmpLeftKey, tmpLeftValue in leftTask.items():
            for index in range(0, len(tmpLeftValue["result"])):
                if "isContrast" not in tmpLeftValue["result"][index].keys():
                    if tmpLeftKey not in resultDict["noContrast"].keys():
                        resultDict["noContrast"][tmpLeftKey] = {"title": tmpLeftValue["title"], "result": []}
                    resultDict["noContrast"][tmpLeftKey]["result"].append(
                        {"left": tmpLeftValue["result"][index], "right": {"null":True}})

        for tmpRightKey, tmpRightValue in rightTask.items():
            for index in range(0, len(tmpRightValue["result"])):
                if "isContrast" not in tmpRightValue["result"][index].keys():
                    if tmpRightKey not in resultDict["noContrast"].keys():
                        resultDict["noContrast"][tmpRightKey] = {"title": tmpRightValue["title"], "result": []}
                    resultDict["noContrast"][tmpRightKey]["result"].append(
                        {"left": {"null":True}, "right": tmpRightValue["result"][index]})
        print(resultDict)
        return resultDict
if __name__ == "__main__":
   print(HTTP_task_executeService.findTaskRestltForId(59))

