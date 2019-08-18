import apps.common.func.InitDjango
from all_models_for_dubbo.models import Tb2DubboTask
from django.db import connection
from django.forms.models import model_to_dict
from apps.common.func.CommonFunc import *
from all_models.models.A0011_version_manage import TbVersionTask

class DubboTaskService(object):

    @staticmethod
    def getTask():
        return Tb2DubboTask.objects.all()

    @staticmethod
    def getTaskForId(id):
        return Tb2DubboTask.objects.filter(id=id)[0]

    @staticmethod
    def getVersionTaskById(id):
        return TbVersionTask.objects.filter(id=id)[0]

    @staticmethod
    def getTaskForTaskId(taskId):
        return Tb2DubboTask.objects.filter(taskId=taskId).filter(state=1)[0]

    @staticmethod
    def getVersionTaskForTaskId(taskId,versionName):
        return TbVersionTask.objects.filter(taskId=taskId,versionName_id=versionName).filter(state=1)[0]

    @staticmethod
    def getVersionTaskForId(id, versionName):
        return TbVersionTask.objects.filter(id=id, versionName_id=versionName).filter(state=1)[0]

    @staticmethod
    def interfaceSaveEdit(taskData):
        taskSaveEditResule = Tb2DubboTask.objects.filter(id=taskData["id"]).update(**taskData)
        return taskSaveEditResule

    @staticmethod
    def queryPeopleTask(now_pageNum, pageNum, loginName):
        limit = ('%d,%d' % (now_pageNum * pageNum, pageNum))
        execSql = 'SELECT u.loginName , u.userName, c.count from tb_user u LEFT JOIN (SELECT addBy as loginName,COUNT(*) as count FROM tb_task where state=1 GROUP BY addBy ) c on u.loginName = c.loginName WHERE u.state = 1 and c.count>0 and u.loginName != "%s" order by c.count desc LIMIT %s ;' % (
        loginName, limit)
        resultDict = executeSqlGetDict(execSql, [])
        return resultDict

    @staticmethod
    def queryVersionPeopleTask(now_pageNum, pageNum, loginName,versionName):
        limit = ('%d,%d' % (now_pageNum * pageNum, pageNum))
        execSql = 'SELECT u.loginName , u.userName, c.count from tb_user u LEFT JOIN (SELECT addBy as loginName,COUNT(*) as count FROM tb_version_task where state=1 and versionName="%s" GROUP BY addBy ) c on u.loginName = c.loginName WHERE u.state = 1 and c.count>0 and u.loginName != "%s" order by c.count desc LIMIT %s ;' % (
        versionName,loginName, limit)
        resultDict = executeSqlGetDict(execSql, [])
        return resultDict

    @staticmethod
    def getTestCaseForIdToDict(id):
        return dbModelToDict(Tb2DubboTask.objects.filter(id=id)[0])

    @staticmethod
    def getTaskId(protocol):
        try:
            taskMaxId = Tb2DubboTask.objects.filter(protocol=protocol).latest("id").taskId
        except:
            taskId = "DUBBO_TASK_1"
            return taskId
        splitData = taskMaxId.split("_")
        taskId = "%s_%s_%s" % (splitData[0],splitData[1],(int(splitData[2])+1))
        return taskId

    @staticmethod
    def getVersionTaskId(protocol,versionName):
        try:
            taskMaxId = TbVersionTask.objects.filter(protocol=protocol,versionName_id=versionName).latest("id").taskId
        except:
            taskId = "DUBBO_TASK_1"
            return taskId
        splitData = taskMaxId.split("_")
        taskId = "%s_%s_%s" % (splitData[0],splitData[1],(int(splitData[2])+1))
        return taskId

    @staticmethod
    def addTask(taskData):
        taskData["taskId"] = DubboTaskService.getTaskId(taskData["protocol"])
        createTaskData = Tb2DubboTask.objects.create(**taskData)
        return createTaskData

    @staticmethod
    def addVersionTask(taskData,versionName):
        taskData["versionName_id"] = versionName
        taskData["addTime"] = datetime.datetime.now()
        taskData["modTime"] = datetime.datetime.now()
        taskData["taskId"] = DubboTaskService.getVersionTaskId(taskData["protocol"],versionName)
        createTaskData = TbVersionTask.objects.create(**taskData)
        return createTaskData

    @staticmethod
    def editTask(taskData):
        editTaskData = Tb2DubboTask.objects.filter(id=taskData["id"]).update(**taskData)
        return editTaskData

    @staticmethod
    def editVersionTask(taskData,versionName):
        taskData['versionName_id'] = versionName
        editTaskData = TbVersionTask.objects.filter(id=taskData["id"]).update(**taskData)
        return editTaskData

    @staticmethod
    def findTaskForTaskId(taskId):
        taskData = Tb2DubboTask.objects.filter(taskId=taskId)
        return taskData

    @staticmethod
    def findVersionTaskForTaskId(taskId,versionName):
        taskData = TbVersionTask.objects.filter(taskId=taskId,versionName_id=versionName)
        return taskData

    @staticmethod
    def findTaskForId(id):
        taskData = Tb2DubboTask.objects.filter(id=id)
        return taskData

    @staticmethod
    def delTaskForId(id):
        delData = Tb2DubboTask.objects.filter(id=id).update(state=0)
        return delData

    @staticmethod
    def delVersionTaskForId(id):
        delData = TbVersionTask.objects.filter(id=id).update(state=0)
        return delData

    @staticmethod
    def getUserLastTask(loginName):
        return Tb2DubboTask.objects.filter(addBy_id=loginName).filter(state=1)

    @staticmethod
    def getTaskListForTaskIdList(list):
        return Tb2DubboTask.objects.filter(taskId__in=list).filter(state=1)

    @staticmethod
    def getVersionTaskListForTaskIdList(list,versionName):
        return TbVersionTask.objects.filter(taskId__in=list,versionName_id=versionName).filter(state=1)

if __name__ == "__main__":
    print(DubboTaskService.findTaskForId(59))

