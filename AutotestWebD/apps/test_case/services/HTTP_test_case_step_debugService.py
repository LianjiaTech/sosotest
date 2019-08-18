import apps.common.func.InitDjango
from all_models.models import TbHttpTestcaseStepDebug
from apps.common.func.CommonFunc import *

class HTTP_test_case_step_debugService(object):

    @staticmethod
    def getTestCaseStepDebug(caseId):
        stepList = TbHttpTestcaseStepDebug.objects.filter(caseId=caseId).filter(state=1)
        return dbModelListToListDict(stepList)

    @staticmethod
    def getTestCaseAllStepDebug(addBy):
        stepList = TbHttpTestcaseStepDebug.objects.filter(addBy_id=addBy)
        return dbModelListToListDict(stepList)

    @staticmethod
    def testCaseStepAddDebug(stepData):
        try:
            stepDataAdd = TbHttpTestcaseStepDebug.objects.create(**stepData)
        except Exception as e:
            print(e)
            return e
        return stepDataAdd

    @staticmethod
    def updateTestCaseStepDebug(id,stepData):
        updateStep = TbHttpTestcaseStepDebug.objects.filter(id=id).update(**stepData)
        TbHttpTestcaseStepDebug.objects.get(id=id).save()
        return updateStep

    @staticmethod
    def updateCancelDebug(id):
        updateCancel = TbHttpTestcaseStepDebug.objects.filter(id=id).update(state=0)
        return updateCancel

    @staticmethod
    def getStepIdList(addBy):
        stepIdList = dbModelListToListDict(TbHttpTestcaseStepDebug.objects.filter(addBy_id=addBy).filter(state=1))
        return stepIdList

    @staticmethod
    def getStep(addBy):
        stepList = TbHttpTestcaseStepDebug.objects.filter(addBy_id=addBy).filter(state=1)
        return stepList
if __name__ == "__main__":
    # HTTP_test_case_stepService.getTestCaseStep("HTTP_TESTCASE_23")
    print(HTTP_test_case_step_debugService.getStep("liyc"))
    # print(UserService.getUserByLoginname(UserService.getUsers()[0].loginname))