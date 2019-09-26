import apps.common.func.InitDjango
from all_models_for_dubbo.models import Tb2DubboTestcase,TbUser,Tb2DubboTestcaseStep,Tb2DubboInterface,Tb2DubboTestcaseDebug,Tb2DubboTestcaseStepDebug

from all_models.models.A0011_version_manage import TbVersionHttpTestcase
from django.db import connection
from django.forms.models import model_to_dict
from apps.common.func.CommonFunc import *

class DubboTestcaseService(object):

    @staticmethod
    def getTestCase():
        return Tb2DubboTestcase.objects.all()

    @staticmethod
    def getTestCaseForId(id):
        return Tb2DubboTestcase.objects.filter(id=id)[0]

    @staticmethod
    def getVersionTestCaseForId(id):
        return TbVersionHttpTestcase.objects.filter(id=id)[0]

    @staticmethod
    def getInterfaceList(execCheckSql,list):
        cursor = connection.cursor()
        cursor.execute(execCheckSql,list)
        return cursor.fetchall()

    @staticmethod
    def delTestCaseForId(id):
        delData = Tb2DubboTestcase.objects.filter(id=id).update(state=0)
        return delData

    @staticmethod
    def delVersionTestCaseForId(id):
        delData = TbVersionHttpTestcase.objects.filter(id=id).update(state=0)
        return delData

    @staticmethod
    def user_contacts():
        audit = 2
        sql = """SElECT * from tb_http_interface i LEFT JOIN tb_user u ON i.addBy = u.loginName WHERE 1=1 and i.state=1 and (i.addBy LIKE %s or u.userName LIKE %s)  LIMIT 0,20 """
        import pymysql
        cursor = connection.cursor()
        cursor.execute(sql, ["l11111111111iyc","liyc"])
        rowData = cursor.fetchall()

        col_names = [desc[0] for desc in cursor.description]
        result = []
        for row in rowData:
            objDict = {}
            # 把每一行的数据遍历出来放到Dict中
            for index, value in enumerate(row):
                # print(index, col_names[index], value)
                objDict[col_names[index]] = value

            result.append(objDict)

        return rowData


    @staticmethod
    def queryPeopleTestCase(now_pageNum,pageNum , loginName):
        limit = ('%d,%d' % (now_pageNum * pageNum ,pageNum))
        execSql = 'SELECT u.loginName , u.userName, c.count from tb_user u LEFT JOIN (SELECT addBy as loginName,COUNT(*) as count FROM tb2_dubbo_testcase where state=1 GROUP BY addBy ) c on u.loginName = c.loginName WHERE u.state = 1 and c.count>0 and u.loginName != "%s" order by c.count desc LIMIT %s ;' % (loginName,limit)
        resultDict = executeSqlGetDict(execSql,[])
        return resultDict

    @staticmethod
    def queryVersionPeopleTestCase(now_pageNum,pageNum , loginName,versionName):
        limit = ('%d,%d' % (now_pageNum * pageNum ,pageNum))
        execSql = 'SELECT u.loginName , u.userName, c.count from tb_user u LEFT JOIN (SELECT addBy as loginName,COUNT(*) as count FROM tb_version_http_testcase where state=1 and versionName="%s" GROUP BY addBy ) c on u.loginName = c.loginName WHERE u.state = 1 and c.count>0 and u.loginName != "%s" order by c.count desc LIMIT %s ;' % (versionName,loginName,limit)
        resultDict = executeSqlGetDict(execSql,[])
        return resultDict

    @staticmethod
    def getTestCaseForIdToDict(id):
        return dbModelToDict(Tb2DubboTestcase.objects.filter(id=id)[0])

    @staticmethod
    def getVersionTestCaseForIdToDict(id):
        return dbModelToDict(TbVersionHttpTestcase.objects.filter(id=id)[0])

    @staticmethod
    def testCaseAdd(testCaseData):
        testCaseData["caseId"] = DubboTestcaseService.getTestCaseId()
        try:
            saveTestCase = Tb2DubboTestcase.objects.create(**testCaseData)
        except Exception as e:
            print(e)
        return saveTestCase

    @staticmethod
    def testVersionCaseAdd(testCaseData,versionName):
        testCaseData["versionName_id"] = versionName
        testCaseData["addTime"] = datetime.datetime.now()
        testCaseData["modTime"] = datetime.datetime.now()
        testCaseData["caseId"] = DubboTestcaseService.getVersionTestCaseId(versionName)
        try:
            saveTestCase = TbVersionHttpTestcase.objects.create(**testCaseData)
            print(1111)
        except Exception as e:
            print(e)
        return saveTestCase

    @staticmethod
    def getTestCaseId():
        try:
            testCaseMaxId = Tb2DubboTestcase.objects.latest('id').caseId
        except Exception as e:
            caseId = 'DUBBO_TESTCASE_1'
            return caseId
        splitData = testCaseMaxId.split('_')
        caseId = "%s_%s_%s" % (splitData[0], splitData[1], (int(splitData[2]) + 1))
        return caseId

    @staticmethod
    def getVersionTestCaseId(versionName):
        try:
            testCaseMaxId = TbVersionHttpTestcase.objects.filter(versionName_id=versionName).latest('id').caseId
        except Exception as e:
            caseId = 'DUBBO_TESTCASE_1'
            return caseId
        splitData = testCaseMaxId.split('_')
        caseId = "%s_%s_%s" % (splitData[0], splitData[1], (int(splitData[2]) + 1))
        return caseId

    @staticmethod
    def saveEdit(testCaseData):
        saveEditResult = Tb2DubboTestcase.objects.filter(id=testCaseData["id"]).update(**testCaseData)
        return saveEditResult

    @staticmethod
    def saveVersionEdit(testCaseData):
        saveEditResult = TbVersionHttpTestcase.objects.filter(id=testCaseData["id"]).update(**testCaseData)
        return saveEditResult

    @staticmethod
    def taskCheckTestCaseList(testCaseIdList):
        testCaseList = Tb2DubboTestcase.objects.filter(caseId__in=testCaseIdList)
        return testCaseList

    @staticmethod
    def getTestCaseForTestCaseId(testCaseId):
        return Tb2DubboTestcase.objects.filter(caseId=testCaseId, state=1)[0]

    @staticmethod
    def getVersionTestCaseForTestCaseId(testCaseId,versionName):
        return TbVersionHttpTestcase.objects.filter(caseId=testCaseId,versionName_id=versionName)[0]

    ##########test step functions
    @staticmethod
    def testCaseStepAdd(stepData):
        try:
            stepDataAdd = Tb2DubboTestcaseStep.objects.create(**stepData)
        except Exception as e:
            print(e)
            raise "添加步骤失败"
        return stepDataAdd

    @staticmethod
    def getTestCaseStep(caseId):
        stepList = Tb2DubboTestcaseStep.objects.filter(caseId=caseId).filter(state=1)
        return dbModelListToListDict(stepList)

    @staticmethod
    def getTestCaseAllStep(caseId):
        stepList = Tb2DubboTestcaseStep.objects.filter(caseId=caseId).order_by("stepNum")
        return dbModelListToListDict(stepList)

    @staticmethod
    def updateTestCaseStep(id,stepData):
        print(stepData)
        updateStep = Tb2DubboTestcaseStep.objects.filter(id=id).update(**stepData)
        return updateStep

    @staticmethod
    def updateCancel(id):
        updateCancel = Tb2DubboTestcaseStep.objects.filter(id=id).update(state=0)
        return updateCancel

    @staticmethod
    def testCaseStepAdd(stepData):
        try:
            stepDataAdd = Tb2DubboTestcaseStep.objects.create(**stepData)
        except Exception as e:
            print(e)
            raise "添加步骤失败"
        return stepDataAdd

    @staticmethod
    def getSyncStep(caseId):
        return Tb2DubboTestcaseStep.objects.filter(state=1).filter(caseId=caseId).filter(isSync=1)

    @staticmethod
    def getInterfaceForInterfaceId(interfaceId):
        return Tb2DubboInterface.objects.filter(interfaceId=interfaceId)[0]

    @staticmethod
    def syncTestCaseStepFromInterfaceId(caseId):
        stepList = dbModelListToListDict(DubboTestcaseService.getSyncStep(caseId))
        failTestCaseList = []
        for index in range(0, len(stepList)):
            interface = dbModelToDict(
                DubboTestcaseService.getInterfaceForInterfaceId(stepList[index]["fromInterfaceId"]))
            if interface["state"] == 0:
                failTestCaseList.append(stepList[index]["title"])
                continue
            stepList[index]["stepDesc"] = interface["casedesc"]
            stepList[index]["varsPre"] = interface["varsPre"]

            stepList[index]["dubboSystem"] = interface["dubboSystem"]
            stepList[index]["dubboService"] = interface["dubboService"]
            stepList[index]["dubboMethod"] = interface["dubboMethod"]
            stepList[index]["dubboParams"] = interface["dubboParams"]
            stepList[index]["encoding"] = interface["encoding"]

            stepList[index]["customUri"] = interface["customUri"]
            stepList[index]["useCustomUri"] = interface["useCustomUri"]
            stepList[index]["varsPost"] = interface["varsPost"]
            stepList[index]["timeout"] = interface["timeout"]
            stepList[index]["modBy"] = interface["modBy"]
            stepList[index]["modTime"] = datetime.datetime.now()
            stepList[index]["businessLineId_id"] = interface["businessLineId_id"]
            stepList[index]["moduleId_id"] = interface["moduleId_id"]
            DubboTestcaseService.updateTestCaseStep(stepList[index]["id"], stepList[index])
        if failTestCaseList == []:
            return True
        else:
            return failTestCaseList

    @staticmethod
    def stepDel(caseId):
        Tb2DubboTestcaseStep.objects.filter(caseId=caseId).update(state=0)

    @staticmethod
    def getSyncStepFromInterfaceIdNum(interfaceId):
        return Tb2DubboTestcaseStep.objects.filter(fromInterfaceId=interfaceId)

    #############debug####################
    @staticmethod
    def testCaseDebugAdd(addBy,dataDict):
        if len(Tb2DubboTestcaseDebug.objects.filter(addBy_id=addBy)) == 0:
            dataDict["addBy_id"] = addBy
            return Tb2DubboTestcaseDebug.objects.create(**dataDict)
        else:
            dataDict["execStatus"] = 1
            dataDict["assertResult"] = ""
            dataDict["testResult"] = ""
            dataDict["beforeExecuteTakeTime"] = 0
            dataDict["afterExecuteTakeTime"] = 0
            dataDict["executeTakeTime"] = 0
            dataDict["totalTakeTime"] = 0
            dataDict["modBy"] = addBy
            return Tb2DubboTestcaseDebug.objects.filter(addBy_id=addBy).update(**dataDict)

    @staticmethod
    def getTestCaseAllStepDebug(addBy):
        stepList = Tb2DubboTestcaseStepDebug.objects.filter(addBy_id=addBy)
        return dbModelListToListDict(stepList)

    @staticmethod
    def updateTestCaseStepDebug(id,stepData):
        updateStep = Tb2DubboTestcaseStepDebug.objects.filter(id=id).update(**stepData)
        Tb2DubboTestcaseStepDebug.objects.get(id=id).save()
        return updateStep

    @staticmethod
    def updateCancelDebug(id):
        updateCancel = Tb2DubboTestcaseStepDebug.objects.filter(id=id).update(state=0)
        return updateCancel

    @staticmethod
    def testCaseStepAddDebug(stepData):
        try:
            stepDataAdd = Tb2DubboTestcaseStepDebug.objects.create(**stepData)
        except Exception as e:
            print(e)
            return e
        return stepDataAdd

    @staticmethod
    def getCaseDebugId(addBy):
        caseDebugId = Tb2DubboTestcaseDebug.objects.filter(addBy_id=addBy)[0].id
        return caseDebugId

    @staticmethod
    def getStepIdList(addBy):
        stepIdList = dbModelListToListDict(Tb2DubboTestcaseStepDebug.objects.filter(addBy_id=addBy).filter(state=1))
        return stepIdList

    @staticmethod
    def setDebugFail(addBy, dataDict):
        debugFail = Tb2DubboTestcaseDebug.objects.filter(addBy_id=addBy).update(**dataDict)
        return debugFail

    @staticmethod
    def getCaseDebug(addBy):
        caseDebugResult = Tb2DubboTestcaseDebug.objects.filter(addBy_id=addBy)[0]
        return caseDebugResult

    @staticmethod
    def getStep(addBy):
        stepList = Tb2DubboTestcaseStepDebug.objects.filter(addBy_id=addBy).filter(state=1)
        return stepList