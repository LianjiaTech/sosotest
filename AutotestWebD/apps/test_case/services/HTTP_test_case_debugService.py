import apps.common.func.InitDjango
from all_models.models import TbHttpTestcaseDebug,TbUser
from django.db import connection
from django.forms.models import model_to_dict
from apps.common.func.CommonFunc import *
class HTTP_test_case_debugService(object):
    @staticmethod
    def testCaseDebugAdd(addBy,dataDict):
        if len(TbHttpTestcaseDebug.objects.filter(addBy_id=addBy)) == 0:
            dataDict["addBy_id"] = addBy
            return TbHttpTestcaseDebug.objects.create(**dataDict)
        else:
            dataDict["execStatus"] = 1
            dataDict["assertResult"] = ""
            dataDict["testResult"] = ""
            dataDict["beforeExecuteTakeTime"] = 0
            dataDict["afterExecuteTakeTime"] = 0
            dataDict["executeTakeTime"] = 0
            dataDict["totalTakeTime"] = 0
            dataDict["modBy"] = addBy
            return TbHttpTestcaseDebug.objects.filter(addBy_id=addBy).update(**dataDict)


    @staticmethod
    def setDebugFail(addBy, dataDict):
        debugFail = TbHttpTestcaseDebug.objects.filter(addBy_id=addBy).update(**dataDict)
        return debugFail

    @staticmethod
    def getCaseDebugId(addBy):
        caseDebugId = TbHttpTestcaseDebug.objects.filter(addBy_id=addBy)[0].id
        return caseDebugId

    @staticmethod
    def getCaseDebug(addBy):
        caseDebugResult = TbHttpTestcaseDebug.objects.filter(addBy_id=addBy)[0]
        return caseDebugResult
if __name__ == "__main__":
   HTTP_test_case_debugService.testCaseDebugAdd("liycs")
    # print(UserService.getUserByLoginname(UserService.getUsers()[0].loginname))
    # HTTP_test_caseService.testCaseAdd("")

