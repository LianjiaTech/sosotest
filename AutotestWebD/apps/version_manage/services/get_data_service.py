import django
import os
import sys
import traceback
import logging

rootpath = os.path.dirname(os.path.realpath(__file__)).replace("\\","/")
rootpath = rootpath.split("/apps")[0]
# print(rootpath)
syspath=sys.path
sys.path=[]
sys.path.append(rootpath) #指定搜索路径绝对目录
sys.path.extend([rootpath+i for i in os.listdir(rootpath) if i[0]!="."])#将工程目录下的一级目录添加到python搜索路径中
sys.path.extend(syspath)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutotestWebD.settings")# project_name 项目名称
django.setup()
from all_models.models import *
from AutotestWebD.settings import *
from apps.common.func.CommonFunc import *
import django.utils.timezone
class GetData(object):

    @staticmethod
    def getCurrentVersion():
        versionSets = TbVersion.objects.filter(type=2).order_by("-id")
        if versionSets:
            return versionSets[0]
        else:
            return False

    @staticmethod
    def changeVersionToHistoyVersion(versionObj):
        versionObj.type = 1
        versionObj.closeTime = django.utils.timezone.now()
        versionObj.save(force_update=True)

    @staticmethod
    def changeVersionToUsingVersion(versionObj):
        versionObj.type = 2
        versionObj.save(force_update=True)

    @staticmethod
    def getUnuseVersion():
        versionSets = TbVersion.objects.filter(type=3).order_by("id")
        if versionSets:
            return versionSets[0]
        else:
            return False

    @staticmethod
    def getAllGlobalText():
        return TbGlobalText.objects.filter(state = 1)

    @staticmethod
    def saveGlobalTextToVersionTable(globalTextObj,versionObj):
        tmpVersionGlobalText = TbVersionGlobalText()
        tmpVersionGlobalText.versionName = versionObj
        tmpVersionGlobalText.textDesc = globalTextObj.textDesc
        tmpVersionGlobalText.textKey = globalTextObj.textKey
        tmpVersionGlobalText.textValue = globalTextObj.textValue
        tmpVersionGlobalText.addBy = globalTextObj.addBy
        tmpVersionGlobalText.modBy = globalTextObj.modBy
        tmpVersionGlobalText.addTime = globalTextObj.addTime
        tmpVersionGlobalText.modTime = globalTextObj.modTime
        tmpVersionGlobalText.save(force_insert=True)

    @staticmethod
    def saveAllGlobalTextToVersionTable(globalTextObjSet,versionObj):
        TbVersionGlobalText.objects.filter(versionName=versionObj).delete()
        for tmpGlobalTextObj in globalTextObjSet:
            GetData.saveGlobalTextToVersionTable(tmpGlobalTextObj,versionObj)

    @staticmethod
    def getAllGlobalVars():
        return TbGlobalVars.objects.filter(state = 1)

    @staticmethod
    def saveGlobalVarsToVersionTable(globalVarsObj,versionObj):
        tbVersionGvar = TbVersionGlobalVars()

        tbVersionGvar.versionName = versionObj

        tbVersionGvar.varKey = globalVarsObj.varKey
        tbVersionGvar.varValue = globalVarsObj.varValue
        tbVersionGvar.varDesc = globalVarsObj.varDesc

        tbVersionGvar.addBy = globalVarsObj.addBy
        tbVersionGvar.modBy = globalVarsObj.modBy
        tbVersionGvar.addTime = globalVarsObj.addTime
        tbVersionGvar.modTime = globalVarsObj.modTime
        tbVersionGvar.save(force_insert=True)

    @staticmethod
    def saveAllGlobalVarsToVersionTable(globalVarsSets,versionObj):
        TbVersionGlobalVars.objects.filter(versionName=versionObj).delete()
        for tmpGlobalTextObj in globalVarsSets:
            GetData.saveGlobalVarsToVersionTable(tmpGlobalTextObj,versionObj)

    @staticmethod
    def getAllHttpIntrface():
        return TbHttpInterface.objects.filter(state = 1)

    @staticmethod
    def saveHttpInterfaceToVersionTable(standardObj,versionObj):
        tbVersionObj = TbVersionHttpInterface()

        tbVersionObj.versionName = versionObj

        tbVersionObj.interfaceId = standardObj.interfaceId
        tbVersionObj.title = standardObj.title
        tbVersionObj.casedesc = standardObj.casedesc
        tbVersionObj.businessLineId = standardObj.businessLineId
        tbVersionObj.moduleId = standardObj.moduleId
        tbVersionObj.sourceId = standardObj.sourceId
        tbVersionObj.caselevel = standardObj.caselevel
        tbVersionObj.status = standardObj.status
        tbVersionObj.caseType = standardObj.caseType

        tbVersionObj.varsPre = standardObj.varsPre
        tbVersionObj.uri = standardObj.uri
        tbVersionObj.method = standardObj.method
        tbVersionObj.header = standardObj.header
        tbVersionObj.url = standardObj.url
        tbVersionObj.params = standardObj.params
        tbVersionObj.bodyType = standardObj.bodyType
        tbVersionObj.bodyContent = standardObj.bodyContent
        tbVersionObj.timeout = standardObj.timeout
        tbVersionObj.varsPost = standardObj.varsPost

        tbVersionObj.addBy = standardObj.addBy
        tbVersionObj.modBy = standardObj.modBy
        tbVersionObj.addTime = standardObj.addTime
        tbVersionObj.modTime = standardObj.modTime
        tbVersionObj.save(force_insert=True)

    @staticmethod
    def saveAllHttpInterfaceToVersionTable(standardObjSets,versionObj):
        TbVersionHttpInterface.objects.filter(versionName=versionObj).delete()
        for tmpStandardObj in standardObjSets:
            GetData.saveHttpInterfaceToVersionTable(tmpStandardObj,versionObj)

    @staticmethod
    def getAllHttpTestcase():
        return TbHttpTestcase.objects.filter(state = 1)

    @staticmethod
    def saveHttpTestcaseToVersionTable(standardObj,versionObj):
        tbVersionObj = TbVersionHttpTestcase()

        tbVersionObj.versionName = versionObj

        tbVersionObj.caseId = standardObj.caseId
        tbVersionObj.title = standardObj.title
        tbVersionObj.casedesc = standardObj.casedesc
        tbVersionObj.businessLineId = standardObj.businessLineId
        tbVersionObj.moduleId = standardObj.moduleId
        tbVersionObj.sourceId = standardObj.sourceId
        tbVersionObj.caselevel = standardObj.caselevel
        tbVersionObj.stepCount = standardObj.stepCount
        tbVersionObj.status = standardObj.status
        tbVersionObj.caseType = standardObj.caseType

        tbVersionObj.addBy = standardObj.addBy
        tbVersionObj.modBy = standardObj.modBy
        tbVersionObj.addTime = standardObj.addTime
        tbVersionObj.modTime = standardObj.modTime
        tbVersionObj.save(force_insert=True)

    @staticmethod
    def saveAllHttpTestcaseToVersionTable(standardObjSets,versionObj):
        TbVersionHttpTestcase.objects.filter(versionName=versionObj).delete()
        for tmpStandardObj in standardObjSets:
            GetData.saveHttpTestcaseToVersionTable(tmpStandardObj,versionObj)

    @staticmethod
    def getAllHttpTestcaseStep():
        return TbHttpTestcaseStep.objects.filter(state = 1)

    @staticmethod
    def saveHttpTestcaseStepToVersionTable(standardObj,versionObj):
        tbVersionObj = TbVersionHttpTestcaseStep()

        tbVersionObj.versionName = versionObj

        tbVersionObj.caseId = standardObj.caseId.caseId
        tbVersionObj.stepNum = standardObj.stepNum

        tbVersionObj.title = standardObj.title
        tbVersionObj.stepDesc = standardObj.stepDesc
        tbVersionObj.businessLineId = standardObj.businessLineId
        tbVersionObj.moduleId = standardObj.moduleId
        tbVersionObj.sourceId = standardObj.sourceId
        tbVersionObj.caseType = standardObj.caseType

        tbVersionObj.fromInterfaceId = standardObj.fromInterfaceId
        tbVersionObj.isSync = standardObj.isSync

        tbVersionObj.varsPre = standardObj.varsPre
        tbVersionObj.uri = standardObj.uri
        tbVersionObj.method = standardObj.method
        tbVersionObj.header = standardObj.header
        tbVersionObj.url = standardObj.url
        tbVersionObj.params = standardObj.params
        tbVersionObj.bodyType = standardObj.bodyType
        tbVersionObj.bodyContent = standardObj.bodyContent
        tbVersionObj.timeout = standardObj.timeout
        tbVersionObj.varsPost = standardObj.varsPost

        tbVersionObj.addBy = standardObj.addBy
        tbVersionObj.modBy = standardObj.modBy
        tbVersionObj.addTime = standardObj.addTime
        tbVersionObj.modTime = standardObj.modTime
        tbVersionObj.save(force_insert=True)

    @staticmethod
    def saveAllHttpTestcaseStepToVersionTable(standardObjSets,versionObj):
        TbVersionHttpTestcaseStep.objects.filter(versionName=versionObj).delete()
        for tmpStandardObj in standardObjSets:
            GetData.saveHttpTestcaseStepToVersionTable(tmpStandardObj,versionObj)

    @staticmethod
    def getAllTask():
        return TbTask.objects.filter(state=1)

    @staticmethod
    def getAllTaskSuite():
        return TbTaskSuite.objects.filter(state=1)

    @staticmethod
    def saveTaskToVersionTable(standardObj, versionObj):
        tbVersionObj = TbVersionTask()

        tbVersionObj.versionName = versionObj

        tbVersionObj.taskId = standardObj.taskId
        tbVersionObj.title = standardObj.title
        tbVersionObj.taskdesc = standardObj.taskdesc
        tbVersionObj.protocol = standardObj.protocol
        tbVersionObj.businessLineGroup = standardObj.businessLineGroup
        tbVersionObj.modulesGroup = standardObj.modulesGroup
        tbVersionObj.sourceGroup = standardObj.sourceGroup
        tbVersionObj.taskLevel = standardObj.taskLevel
        tbVersionObj.highPriorityVARS = standardObj.highPriorityVARS
        tbVersionObj.status = standardObj.status
        tbVersionObj.interfaceCount = standardObj.interfaceCount
        tbVersionObj.taskInterfaces = standardObj.taskInterfaces
        tbVersionObj.caseCount = standardObj.caseCount
        tbVersionObj.taskTestcases = standardObj.taskTestcases
        tbVersionObj.interfaceNum = standardObj.interfaceNum
        tbVersionObj.emailList = standardObj.emailList

        tbVersionObj.addBy = standardObj.addBy
        tbVersionObj.modBy = standardObj.modBy
        tbVersionObj.addTime = standardObj.addTime
        tbVersionObj.modTime = standardObj.modTime
        tbVersionObj.save(force_insert=True)

    @staticmethod
    def saveAllTaskToVersionTable(standardObjSets, versionObj):
        TbVersionTask.objects.filter(versionName=versionObj).delete()
        for tmpStandardObj in standardObjSets:
            GetData.saveTaskToVersionTable(tmpStandardObj, versionObj)

    @staticmethod
    def getAllStandardInterface():
        return TbStandardInterface.objects.filter(state=1,apiStatus = 1)

    @staticmethod
    def saveStandardInterfaceToVersionTable(standardObj, versionObj):
        tbVersionObj = TbVersionStandardInterface()

        tbVersionObj.versionName = versionObj

        tbVersionObj.businessLineId = standardObj.businessLineId
        tbVersionObj.moduleId = standardObj.moduleId
        tbVersionObj.fileName = standardObj.fileName
        tbVersionObj.interfaceUrl = standardObj.interfaceUrl
        tbVersionObj.interfaceCreateBy = standardObj.interfaceCreateBy
        tbVersionObj.interfaceCreateTime = standardObj.interfaceCreateTime
        tbVersionObj.interfaceUpdateBy = standardObj.interfaceUpdateBy
        tbVersionObj.interfaceUpdateTime = standardObj.interfaceUpdateTime
        tbVersionObj.authorEmail = standardObj.authorEmail

        tbVersionObj.addBy = standardObj.addBy
        tbVersionObj.modBy = standardObj.modBy
        tbVersionObj.addTime = standardObj.addTime
        tbVersionObj.modTime = standardObj.modTime
        tbVersionObj.save(force_insert=True)

    @staticmethod
    def saveAllStandardInterfaceToVersionTable(standardObjSets, versionObj):
        TbVersionStandardInterface.objects.filter(versionName=versionObj).delete()
        for tmpStandardObj in standardObjSets:
            GetData.saveStandardInterfaceToVersionTable(tmpStandardObj, versionObj)


    @staticmethod
    def changeTaskExecuteCurrentVersionToVersionName(versionObj):
        TbTaskExecute.objects.filter(version="CurrentVersion").update(version=versionObj.versionName)

    @staticmethod
    def changeTaskSuiteExecuteCurrentVersionToVersionName(versionObj):
        TbTaskSuiteExecute.objects.filter(version="CurrentVersion").update(version=versionObj.versionName)

    @staticmethod
    def saveTaskSuiteToVersionTable(standardObj, versionObj):
        tbVersionObj = TbVersionTaskSuite()

        tbVersionObj.versionName = versionObj

        tbVersionObj.taskSuiteId = standardObj.taskSuiteId
        tbVersionObj.title = standardObj.title
        tbVersionObj.taskSuiteDesc = standardObj.taskSuiteDesc
        tbVersionObj.protocol = standardObj.protocol
        tbVersionObj.emailList = standardObj.emailList
        tbVersionObj.status = standardObj.status
        tbVersionObj.taskCount = standardObj.taskCount
        tbVersionObj.taskList = standardObj.taskList
        tbVersionObj.isCI = standardObj.isCI

        tbVersionObj.state = standardObj.state
        tbVersionObj.addBy = standardObj.addBy
        tbVersionObj.modBy = standardObj.modBy
        tbVersionObj.addTime = standardObj.addTime
        tbVersionObj.modTime = standardObj.modTime
        tbVersionObj.save(force_insert=True)

    @staticmethod
    def saveAllTaskSuiteToVersionTable(standardObjSets, versionObj):
        TbVersionTaskSuite.objects.filter(versionName=versionObj).delete()
        for tmpStandardObj in standardObjSets:
            GetData.saveTaskSuiteToVersionTable(tmpStandardObj, versionObj)

if __name__ == "__main__":
    currentVersionObj = GetData.getCurrentVersion()
    # GetData.saveAllTaskSuiteToVersionTable(GetData.getAllTaskSuite(), currentVersionObj)
    GetData.changeTaskSuiteExecuteCurrentVersionToVersionName(currentVersionObj)