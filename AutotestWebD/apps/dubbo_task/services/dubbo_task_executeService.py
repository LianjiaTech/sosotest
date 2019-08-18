import apps.common.func.InitDjango
# from all_models.models import TbTaskExecute
from all_models_for_dubbo.models import Tb2DubboTaskExecute
from apps.common.func.CommonFunc import *
# from apps.task.services.HTTP_taskService import HTTP_taskService
from apps.dubbo_task.services.dubbo_taskService import DubboTaskService
class DubboTaskExecuteService(object):

    @staticmethod
    def findTaskRestltForId(id):
        taskExecuteData = Tb2DubboTaskExecute.objects.filter(id=id)
        return taskExecuteData[0]

    @staticmethod
    def againRunTask(id,addBy):
        taskExecuteData = dbModelToDict(Tb2DubboTaskExecute.objects.filter(id=id)[0])
        taskId = taskExecuteData['taskId']

        if taskExecuteData['version'] == "CurrentVersion":
            taskData = dbModelToDict(DubboTaskService.getTaskForTaskId(taskId))
            taskData['version'] = "CurrentVersion"
        else:
            taskData = dbModelToDict(DubboTaskService.getVersionTaskForTaskId(taskId,taskExecuteData['version']))
            del taskData['versionName_id']
            taskData['version'] = taskExecuteData['version']


        if taskData["state"] == 0:
            return False

        del taskData["id"]
        del taskData["addTime"]
        del taskData["modTime"]
        taskData["taskId"] = taskExecuteData["taskId"]
        taskData["addBy_id"] = addBy
        taskData["execBy_id"] = addBy
        taskData["httpConfKey_id"] = taskExecuteData["httpConfKey_id"]
        taskData["isSaveHistory"] = taskExecuteData["isSaveHistory"]
        taskData["isSendEmail"] = taskExecuteData["isSendEmail"]
        taskData["execComments"] = taskExecuteData["execComments"]
        taskData["retryCount"] = taskExecuteData["retryCount"]
        taskData["testResultMsg"] = ""
        taskData["modBy"] = addBy

        addResult = Tb2DubboTaskExecute.objects.create(**taskData)
        return addResult

    @staticmethod
    def updateFailExecute(id,data):
        tb = Tb2DubboTaskExecute.objects.get(id=id)
        tb.execStatus = 4
        tb.testResult = "EXCEPTION"
        tb.testResultMsg = data
        tb.save()

    @staticmethod
    def stopTaskRun(id):
        tb = Tb2DubboTaskExecute.objects.get(id=id)
        tb.execStatus = 10
        tb.testResult = "CANCEL"
        tb.testResultMsg = "任务取消"
        tb.execFinishTime = datetime.datetime.now()
        tb.save()

    @staticmethod
    def taskRunAdd(taskData):
        result =Tb2DubboTaskExecute .objects.create(**taskData)
        return result

    @staticmethod
    def queryPeopleTaskExecute(now_pageNum, pageNum, loginName):
        limit = ('%d,%d' % (now_pageNum * pageNum, pageNum))
        execSql = 'SELECT u.loginName , u.userName, c.count from tb_user u LEFT JOIN (SELECT addBy as loginName,COUNT(*) as count FROM tb_task_execute where state=1 GROUP BY addBy ) c on u.loginName = c.loginName WHERE u.state = 1 and c.count>0 and u.loginName != "%s" order by c.count desc LIMIT %s ;' % (
            loginName, limit)
        resultDict = executeSqlGetDict(execSql, [])
        return resultDict
if __name__ == "__main__":
   print(Tb2DubboTaskExecute.findTaskRestltForId(59))

