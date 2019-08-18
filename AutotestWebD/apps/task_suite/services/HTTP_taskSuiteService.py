import apps.common.func.InitDjango
from all_models.models import TbTask
from django.db import connection
from django.forms.models import model_to_dict
from apps.common.func.CommonFunc import *
from all_models.models.A0011_version_manage import TbVersionTask

class HTTP_taskSuiteService(object):

    @staticmethod
    def getTaskSuite():
        return TbTaskSuite.objects.all()

    @staticmethod
    def getTaskSuiteForId(id):
        return TbTaskSuite.objects.filter(id=id)[0]

    @staticmethod
    def getVersionTaskSuiteForId(id):
        return TbVersionTaskSuite.objects.filter(id=id)[0]

    @staticmethod
    def getTaskSuiteForTaskSuiteId(taskSuiteId):
        try:
            return TbTaskSuite.objects.filter(taskSuiteId=taskSuiteId).filter(state=1)[0]
        except Exception as e:
            return False

    @staticmethod
    def getVersionTaskSuiteForTaskId(taskSuiteId,versionName):
        return TbVersionTaskSuite.objects.filter(taskSuiteId=taskSuiteId,versionName_id=versionName).filter(state=1)[0]

    @staticmethod
    def interfaceSaveEdit(taskData):
        taskSaveEditResule = TbTask.objects.filter(id=taskData["id"]).update(**taskData)
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
        return dbModelToDict(TbTask.objects.filter(id=id)[0])

    @staticmethod
    def getTaskSuiteId(protocol):
        try:
            taskSuiteMaxId = TbTaskSuite.objects.filter(protocol=protocol).latest("id").taskSuiteId
        except:
            taskSuiteId = "HTTP_TASK_SUITE_1"
            return taskSuiteId
        splitData = taskSuiteMaxId.split("_")
        taskSuiteId = "%s_%s_%s_%s" % (splitData[0],splitData[1],splitData[2],(int(splitData[3])+1))
        return taskSuiteId

    @staticmethod
    def getVersionTaskId(protocol,versionName):
        try:
            taskMaxId = TbVersionTask.objects.filter(protocol=protocol,versionName_id=versionName).latest("id").taskId
        except:
            taskId = "HTTP_TASK_1"
            return taskId
        splitData = taskMaxId.split("_")
        taskId = "%s_%s_%s" % (splitData[0],splitData[1],(int(splitData[2])+1))
        return taskId

    @staticmethod
    def addTaskSuite(taskSuiteData):
        taskSuiteId = HTTP_taskSuiteService.getTaskSuiteId(taskSuiteData["protocol"])
        print(taskSuiteId)
        print(taskSuiteData)
        tmpObj = TbTaskSuite()
        tmpObj.taskSuiteId = taskSuiteId
        tmpObj.title = taskSuiteData["title"]
        tmpObj.taskSuiteDesc = taskSuiteData["taskSuiteDesc"]
        tmpObj.protocol = taskSuiteData["protocol"]
        tmpObj.emailList = taskSuiteData["emailList"]
        tmpObj.taskCount = taskSuiteData["taskCount"]
        tmpObj.taskList = taskSuiteData["taskList"]
        tmpObj.addBy = taskSuiteData["addBy"]
        tmpObj.save()
        return tmpObj

    @staticmethod
    def addVersionTask(taskData,versionName):
        taskData["versionName_id"] = versionName
        taskData["addTime"] = datetime.datetime.now()
        taskData["modTime"] = datetime.datetime.now()
        taskData["taskId"] = HTTP_taskSuiteService.getVersionTaskId(taskData["protocol"],versionName)
        createTaskData = TbVersionTask.objects.create(**taskData)
        return createTaskData

    @staticmethod
    def editTaskSuite(taskData):
        editTaskData = TbTaskSuite.objects.filter(id=taskData["id"]).update(**taskData)
        return editTaskData

    @staticmethod
    def editVersionTask(taskData,versionName):
        taskData['versionName_id'] = versionName
        editTaskData = TbVersionTask.objects.filter(id=taskData["id"]).update(**taskData)
        return editTaskData

    @staticmethod
    def findTaskSuiteForTaskSuiteId(taskSuiteId):
        taskSuiteData = TbTaskSuite.objects.filter(taskSuiteId=taskSuiteId)
        return taskSuiteData

    @staticmethod
    def findVersionTaskForTaskId(taskId,versionName):
        taskData = TbVersionTask.objects.filter(taskId=taskId,versionName_id=versionName)
        return taskData

    @staticmethod
    def findTaskForId(id):
        taskData = TbTask.objects.filter(id=id)
        return taskData

    @staticmethod
    def delTaskSuiteForId(request,id):
        delData = TbTaskSuite.objects.filter(id=id).update(state=0,modBy=request.session.get("loginName"))
        return delData

    @staticmethod
    def delVersionTaskForId(request,id):
        delData = TbVersionTask.objects.filter(id=id).update(state=0,modBy=request.session.get("loginName"))
        return delData

    @staticmethod
    def getUserLastTask(loginName):
        return TbTask.objects.filter(addBy_id=loginName).filter(state=1)

    @staticmethod
    def getTaskListForTaskIdList(list):
        return TbTask.objects.filter(taskId__in=list).filter(state=1)

    @staticmethod
    def getVersionTaskListForTaskIdList(list,versionName):
        return TbVersionTask.objects.filter(taskId__in=list,versionName_id=versionName).filter(state=1)

if __name__ == "__main__":
    print(HTTP_taskService.findTaskForId(59))

