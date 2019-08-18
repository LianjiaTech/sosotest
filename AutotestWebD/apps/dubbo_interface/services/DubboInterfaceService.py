
from apps.common.func.CommonFunc import dbModelListToListDict
from apps.config.services.businessLineService import BusinessService
from apps.config.services.modulesService import ModulesService
from apps.config.services.sourceService import SourceService
from all_models.models import TbConfigUri
from apps.dubbo_common.services.UriServiceForDubbo import UriServiceForDubbo
from apps.config.services.http_confService import HttpConfService
from apps.common.config import commonWebConfig
from apps.common.func.CommonFunc import  *
from all_models_for_dubbo.models.B0001_dubbo_interface import *

class DubboInterfaceService(object):
    @staticmethod
    def getInterfaceId():
        try:
            interfaceMaxId = Tb2DubboInterface.objects.latest('id').interfaceId
        except Exception as e:
            interfaceId = 'DUBBO_INTERFACE_1'
            return interfaceId
        splitData = interfaceMaxId.split('_')
        interfaceId = "%s_%s_%s" % (splitData[0],splitData[1],(int(splitData[2])+1))
        return interfaceId

    @staticmethod
    def addInterface(data,addBy):
        newDataDict = {}
        for k, v in data.items():
            newDataDict[k] = data[k]
        newDataDict["addBy_id"] = addBy
        newDataDict["interfaceId"] = DubboInterfaceService.getInterfaceId()
        saveInterface = Tb2DubboInterface.objects.create(**newDataDict)
        return saveInterface

    @staticmethod
    def getInterfaceById(id):
        return Tb2DubboInterface.objects.filter(id=id)[0]

    @staticmethod
    def getInterfaceByIdToDict(id):
        return dbModelToDict(Tb2DubboInterface.objects.filter(id=id)[0])

    @staticmethod
    def interfaceSaveEdit(interfaceData):
        interfaceSaveEditResule = Tb2DubboInterface.objects.filter(id=interfaceData["id"]).update(**interfaceData)
        return interfaceSaveEditResule

    @staticmethod
    def delInterfaceById(id):
        return Tb2DubboInterface.objects.filter(id=id).update(state=0)
