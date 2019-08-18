import apps.common.func.InitDjango
from all_models.models import TbHttpInterface,TbHttpInterfaceDebug
from django.db import connection
from django.forms.models import model_to_dict
from apps.common.func.CommonFunc import *
from apps.common.config import commonWebConfig

class HTTP_interfaceDebugService(object):

    @staticmethod
    def interfaceDebugAdd(data,addBy):
        newDataDict = {}
        for k, v in data.items():
            newDataDict[k] = data[k]
        newDataDict["addBy_id"] = addBy

        if (len(TbHttpInterfaceDebug.objects.filter(addBy_id=addBy)) == 0):
            print(newDataDict)
            return TbHttpInterfaceDebug.objects.create(**newDataDict)
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
                TbHttpInterfaceDebug.objects.filter(addBy_id=addBy).update(**newDataDict)
            except Exception as e:
                import traceback
                print(traceback.format_exc())
                return False
            return TbHttpInterfaceDebug.objects.filter(addBy_id=addBy)[0]

    @staticmethod
    def getDebugResult(addBy):

        debugResult = TbHttpInterfaceDebug.objects.filter(addBy_id=addBy)[0]
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
        debugFail = TbHttpInterfaceDebug.objects.filter(addBy_id=addBy).update(**dataDict)
        return debugFail


if __name__ == "__main__":
    print(int(67/1000*100))
