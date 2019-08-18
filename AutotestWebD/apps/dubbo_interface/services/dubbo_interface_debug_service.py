import apps.common.func.InitDjango
from all_models_for_dubbo.models import Tb2DubboInterface,Tb2DubboInterfaceDebug
from django.db import connection
from django.forms.models import model_to_dict
from apps.common.func.CommonFunc import *
from apps.common.config import commonWebConfig
import traceback
from apps.common.func.ValidataFunc import *
class DubboInterfaceDebugService(object):

    @staticmethod
    def interfaceDebugAdd(data,addBy):
        retB, retS = verifyPythonMode(data['varsPre'])
        if retB == False:
            return "准备中出现不允许的输入：%s" % retS
        retB, retS = verifyPythonMode(data['varsPost'])

        if retB == False:
            return "断言恢复中出现不允许的输入：%s" % retS

        newDataDict = {}
        for k, v in data.items():
            newDataDict[k] = data[k]
        newDataDict["addBy_id"] = addBy

        if (len(Tb2DubboInterfaceDebug.objects.filter(addBy_id=addBy)) == 0):
            return Tb2DubboInterfaceDebug.objects.create(**newDataDict)
        else:
            newDataDict['actualResult'] = ''
            newDataDict['assertResult'] = ''
            newDataDict['testResult'] = "NOTRUN"
            newDataDict['execStatus'] = 1
            newDataDict['beforeExecuteTakeTime'] = 0
            newDataDict['executeTakeTime'] = 0
            newDataDict['afterExecuteTakeTime'] = 0
            newDataDict['totalTakeTime'] = 0
            newDataDict["modTime"] = datetime.datetime.now()
            try:
                Tb2DubboInterfaceDebug.objects.filter(addBy_id=addBy).update(**newDataDict)
            except Exception as e:
                return str(e)

            return Tb2DubboInterfaceDebug.objects.filter(addBy_id=addBy)[0]

    @staticmethod
    def getDebugResult(addBy):

        debugResult = Tb2DubboInterfaceDebug.objects.filter(addBy_id=addBy)[0]
        if debugResult.execStatus == 3 or debugResult.execStatus == 4:
            debugResultDict = dbModelToDict(debugResult)
            businessLineDict = dbModelToDict(debugResult.businessLineId)
            moduleDict = dbModelToDict(debugResult.moduleId)
            httpConfKey = dbModelToDict(debugResult.httpConfKey)
            debugResultDict.update(httpConfKey)
            debugResultDict.update(businessLineDict)
            debugResultDict.update(moduleDict)
            return debugResultDict
        else:
            return 0

    @staticmethod
    def setDebugFail(addBy,dataDict):
        debugFail = Tb2DubboInterfaceDebug.objects.filter(addBy_id=addBy).update(**dataDict)
        return debugFail


if __name__ == "__main__":
    print(int(67/1000*100))

