import apps.common.func.InitDjango
from all_models.models import TbHttpTestcaseStep
from apps.common.func.CommonFunc import *
from all_models.models.A0011_version_manage import TbVersionHttpTestcaseStep
class HTTP_test_case_stepService(object):

    @staticmethod
    def getTestCase():
        return TbHttpTestcaseStep.objects.all()

    @staticmethod
    def getTestCaseStep(caseId):
        stepList = TbHttpTestcaseStep.objects.filter(caseId=caseId).filter(state=1)
        return dbModelListToListDict(stepList)

    @staticmethod
    def getVersionTestCaseStep(caseId,versionName):
        stepList = TbVersionHttpTestcaseStep.objects.filter(caseId=caseId,state=1,versionName_id = versionName)
        return dbModelListToListDict(stepList)


    @staticmethod
    def getTestCaseStepList(caseIdList):
        stepList = TbHttpTestcaseStep.objects.filter(caseId__in=caseIdList).filter(state=1)
        return dbModelListToListDict(stepList)

    @staticmethod
    def getVersionTestCaseStepList(caseIdList,versionName):
        stepList = TbVersionHttpTestcaseStep.objects.filter(caseId__in=caseIdList,versionName_id=versionName).filter(state=1)
        return dbModelListToListDict(stepList)

    @staticmethod
    def getTestCaseAllStep(caseId):
        stepList = TbHttpTestcaseStep.objects.filter(caseId=caseId).order_by("stepNum")
        return dbModelListToListDict(stepList)

    @staticmethod
    def getVersionTestCaseAllStep(caseId,versionName):
        stepList = TbVersionHttpTestcaseStep.objects.filter(caseId=caseId,versionName_id=versionName).order_by("stepNum")
        return dbModelListToListDict(stepList)

    @staticmethod
    def testCaseStepAdd(stepData):
        try:
            stepDataAdd = TbHttpTestcaseStep.objects.create(**stepData)
        except Exception as e:
            print(traceback.format_exc())
            raise "添加步骤失败"
        return stepDataAdd

    @staticmethod
    def testVersionCaseStepAdd(stepData,versionName):
        try:
            if "caseId_id" in stepData.keys():
                stepData["caseId"] = stepData["caseId_id"]
                del stepData["caseId_id"]
            stepData['versionName_id'] = versionName
            # print(versionName)
            stepData['addTime'] = datetime.datetime.now()
            stepData['modTime'] = datetime.datetime.now()
            # print(stepData)
            stepDataAdd = TbVersionHttpTestcaseStep.objects.create(**stepData)
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            raise "添加步骤失败"
        return stepDataAdd

    @staticmethod
    def updateTestCaseStep(request,id,stepData):
        # print(id)
        testCaseStepObj = TbHttpTestcaseStep.objects.filter(id=id)
        if testCaseStepObj[0].addBy.loginName != request.session.get("loginName"):
            userChangeLogTestCaseStepToTestCaseChangeStep(request,dbModelToDict(testCaseStepObj[0]),stepData)
        updateStep = testCaseStepObj.update(**stepData)
        return updateStep

    @staticmethod
    def updateVersionTestCaseStep(request,id,stepData):

        if "caseId_id" in stepData.keys():
            stepData["caseId"] = stepData["caseId_id"]
            del stepData["caseId_id"]

        testCaseStepObj = TbVersionHttpTestcaseStep.objects.filter(id=id)
        if testCaseStepObj[0].addBy.loginName != request.session.get("loginName"):
            userChangeLogTestCaseStepToTestCaseChangeStep(request, dbModelToDict(testCaseStepObj[0]), stepData)
        updateStep = testCaseStepObj.update(**stepData)
        return updateStep



    @staticmethod
    def updateCancel(id):
        updateCancel = TbHttpTestcaseStep.objects.filter(id=id).update(state=0)
        return updateCancel

    @staticmethod
    def updateVersionCancel(id):

        updateCancel = TbVersionHttpTestcaseStep.objects.filter(id=id).update(state=0)
        return updateCancel


    @staticmethod
    def stepDel(request,caseId):
        testCaseStepObject = TbHttpTestcaseStep.objects.filter(caseId=caseId)
        testCaseStepObjectList = dbModelListToListDict(testCaseStepObject)
        for index in range(0,len(testCaseStepObjectList)):
            if testCaseStepObjectList[index]["addBy_id"] != request.session.get("loginName"):
                userChangeLogTestCaseStepDel(request,testCaseStepObjectList[index])
        testCaseStepObject.update(state=0)

    @staticmethod
    def stepVersionDel(request,caseId,versionName):
        testCaseStepObject = TbVersionHttpTestcaseStep.objects.filter(caseId=caseId,versionName_id=versionName)
        testCaseStepObjectList = dbModelListToListDict(testCaseStepObject)
        for index in range(0, len(testCaseStepObjectList)):
            if testCaseStepObjectList[index]["addBy_id"] != request.session.get("loginName"):
                userChangeLogTestCaseStepDel(request, testCaseStepObjectList[index])
        testCaseStepObject.update(state=0)

    @staticmethod
    def getSyncStepFromInterfaceIdNum(interfaceId):
        return TbHttpTestcaseStep.objects.filter(fromInterfaceId=interfaceId,isSync=1,state=1)

    @staticmethod
    def getVersionSyncStepFromInterfaceIdNum(interfaceId,versionName):
        return TbVersionHttpTestcaseStep.objects.filter(fromInterfaceId=interfaceId,versionName_id=versionName,state=1)


    @staticmethod
    def getSyncStepFromInterfaceId(interfaceId):
        return TbHttpTestcaseStep.objects.filter(fromInterfaceId=interfaceId).filter(isSync=1,state=1)

    @staticmethod
    def getVersionSyncStepFromInterfaceId(interfaceId,versionName):
        return TbVersionHttpTestcaseStep.objects.filter(fromInterfaceId=interfaceId,versionName_id=versionName).filter(isSync=1,state=1)

    @staticmethod
    def getSyncStep(caseId):
        return TbHttpTestcaseStep.objects.filter(state=1).filter(caseId=caseId).filter(isSync=1)

    @staticmethod
    def getVersionSyncStep(caseId,versionName):
        return TbVersionHttpTestcaseStep.objects.filter(state=1, versionName_id=versionName,caseId=caseId, isSync=1)


if __name__ == "__main__":
    HTTP_test_case_stepService.getTestCaseStep("HTTP_TESTCASE_23")

    # print(UserService.getUserByLoginname(UserService.getUsers()[0].loginname))