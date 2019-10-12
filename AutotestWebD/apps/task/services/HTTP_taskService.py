from apps.common.func.CommonFunc import *
from all_models.models.A0011_version_manage import TbVersionTask
from apps.version_manage.services.common_service import VersionService
from apps.config.services.businessLineService import BusinessService
from apps.config.services.modulesService import ModulesService
from apps.config.services.sourceService import SourceService


class HTTP_taskService(object):

    @staticmethod
    def getTask():
        return TbTask.objects.all()

    @staticmethod
    def getTaskForId(id):
        return TbTask.objects.filter(id=id)[0]

    @staticmethod
    def getVersionTaskById(id):
        return TbVersionTask.objects.filter(id=id)[0]

    @staticmethod
    def getTaskForTaskId(taskId):
        try:
            return TbTask.objects.filter(taskId=taskId).filter(state=1)[0]
        except Exception as e:
            return False

    @staticmethod
    def getExecuteIdByTaskId(taskId,datefrom,dateto):
        try:
            return TbTaskExecute.objects.filter(taskId=taskId,execFinishTime__range=(datefrom,dateto)).\
                filter(state=1, execStatus=3).order_by('execFinishTime').last()
        except Exception as e:
            return False

    @staticmethod
    def getVersionTaskForId(id,versionName):
        return TbVersionTask.objects.filter(id=id,versionName_id=versionName).filter(state=1)[0]

    @staticmethod
    def getVersionTaskForTaskId(taskId,versionName):
        return TbVersionTask.objects.filter(taskId=taskId,versionName_id=versionName).filter(state=1)[0]

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
    def getTaskId(protocol):
        try:
            taskMaxId = TbTask.objects.filter(protocol=protocol).latest("id").taskId
        except:
            taskId = "HTTP_TASK_1"
            return taskId
        splitData = taskMaxId.split("_")
        taskId = "%s_%s_%s" % (splitData[0],splitData[1],(int(splitData[2])+1))
        return taskId

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
    def addTask(taskData):
        taskData["taskId"] = HTTP_taskService.getTaskId(taskData["protocol"])
        createTaskData = TbTask.objects.create(**taskData)
        return createTaskData

    @staticmethod
    def addVersionTask(taskData,versionName):
        taskData["versionName_id"] = versionName
        taskData["addTime"] = datetime.datetime.now()
        taskData["modTime"] = datetime.datetime.now()
        taskData["taskId"] = HTTP_taskService.getVersionTaskId(taskData["protocol"],versionName)
        createTaskData = TbVersionTask.objects.create(**taskData)
        return createTaskData

    @staticmethod
    def editTask(taskData):
        editTaskData = TbTask.objects.filter(id=taskData["id"]).update(**taskData)
        return editTaskData

    @staticmethod
    def editVersionTask(taskData,versionName):
        taskData['versionName_id'] = versionName
        editTaskData = TbVersionTask.objects.filter(id=taskData["id"]).update(**taskData)
        return editTaskData

    @staticmethod
    def findTaskForTaskId(taskId):
        taskData = TbTask.objects.filter(taskId=taskId)
        return taskData

    @staticmethod
    def findVersionTaskForTaskId(taskId,versionName):
        taskData = TbVersionTask.objects.filter(taskId=taskId,versionName_id=versionName)
        return taskData

    @staticmethod
    def findVersionTaskForId(id, versionName):
        taskData = TbVersionTask.objects.filter(id=id, versionName_id=versionName)
        return taskData

    @staticmethod
    def findTaskForId(id):
        taskData = TbTask.objects.filter(id=id)
        return taskData

    @staticmethod
    def delTaskForId(request,id):
        delData = TbTask.objects.filter(id=id).update(state=0,modBy=request.session.get("loginName"))
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


    @staticmethod
    def taskDataToDict(request,taskData):
        taskInterfaceBusinessLineArr = []
        taskInterfaceModulesArr = []
        taskInterfaceSourceArr = []
        if taskData["taskInterfaces"] != "":
            # 去重，切成数组遍历获取业务线名称
            taskInterfaceList = list(set(taskData["taskInterfaces"].split(",")))
            taskInterfaceListPartSql = ''
            for i in range(0, len(taskInterfaceList)):
                if i == 0:
                    taskInterfaceListPartSql = "interfaceId = '%s'" % taskInterfaceList[i]
                    continue
                taskInterfaceListPartSql += " or interfaceId = '%s'" % taskInterfaceList[i]
            if VersionService.isCurrentVersion(request):
                taskInterfaceBusinessLineArr = BusinessService.getInterfaceListBusinessId(taskInterfaceListPartSql)
                taskInterfaceModulesArr = ModulesService.getInterfaceListModulesId(taskInterfaceListPartSql)
                taskInterfaceSourceArr = SourceService.getInterfaceListSourcesId(taskInterfaceListPartSql)
            else:
                taskInterfaceBusinessLineArr = BusinessService.getVersionInterfaceListBusinessId(
                    taskInterfaceListPartSql, VersionService.getVersionName(request))
                taskInterfaceModulesArr = ModulesService.getVersionInterfaceListModulesId(taskInterfaceListPartSql,
                                                                                          VersionService.getVersionName(
                                                                                              request))
                taskInterfaceSourceArr = SourceService.getVersionInterfaceListSourcesId(taskInterfaceListPartSql,
                                                                                        VersionService.getVersionName(
                                                                                            request))

        taskTestCaseBusinessLineArr = []
        taskTestCaseModulesArr = []
        taskTestCaseSourceArr = []
        if taskData["taskTestcases"] != "":
            # 去重，切成数组遍历获取业务线名称
            taskTestCaseList = list(set(taskData["taskTestcases"].split(",")))
            taskTestCasePartSql = ""
            for i in range(0, len(taskTestCaseList)):
                if i == 0:
                    taskTestCasePartSql = "caseId = '%s'" % taskTestCaseList[i]
                    continue
                taskTestCasePartSql += " or caseId = '%s'" % taskTestCaseList[i]

            if VersionService.isCurrentVersion(request):
                taskTestCaseBusinessLineArr = BusinessService.getTestCaseListBusinessId(taskTestCasePartSql)
                taskTestCaseModulesArr = ModulesService.getTestCaseListModulesId(taskTestCasePartSql)
                taskTestCaseSourceArr = SourceService.getTestCaseListSourcesId(taskTestCasePartSql)
            else:
                taskTestCaseBusinessLineArr = BusinessService.getVersionTestCaseListBusinessId(taskTestCasePartSql,
                                                                                               VersionService.getVersionName(
                                                                                                   request))
                taskTestCaseModulesArr = ModulesService.getVersionTestCaseListModulesId(taskTestCasePartSql,
                                                                                        VersionService.getVersionName(
                                                                                            request))
                taskTestCaseSourceArr = SourceService.getVersionTestCaseListSourcesId(taskTestCasePartSql,
                                                                                      VersionService.getVersionName(
                                                                                          request))

        businessLineGroupArr = taskInterfaceBusinessLineArr + taskTestCaseBusinessLineArr
        businessLineGroup = []
        for i in range(0, len(businessLineGroupArr)):
            businessLineGroup.append(businessLineGroupArr[i]["bussinessLineName"])
        taskData["businessLineGroup"] = list(set(businessLineGroup))

        modulesGroupArr = taskInterfaceModulesArr + taskTestCaseModulesArr
        modulesGroup = []
        for i in range(0, len(modulesGroupArr)):
            modulesGroup.append(modulesGroupArr[i]["moduleName"])
        taskData["modulesGroup"] = list(set(modulesGroup))
        taskData["protocol"] = "HTTP"
        taskData["modBy"] = request.session.get("loginName")
        taskData["modByName"] = request.session.get("userName")

        sourcesGroupArr = taskInterfaceSourceArr + taskTestCaseSourceArr
        sourceGroup = []
        for i in range(0, len(sourcesGroupArr)):
            sourceGroup.append(sourcesGroupArr[i]["sourceName"])
        taskData["sourceGroup"] = list(set(sourceGroup))
        return taskData

if __name__ == "__main__":
    print(HTTP_taskService.findTaskForId(59))

