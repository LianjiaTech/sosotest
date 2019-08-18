from apps.config.services.serviceConfService import ServiceConfService
from apps.config.services.businessLineService import BusinessService
from apps.common.func.WebFunc import *
from all_models.models import *
from django.shortcuts import HttpResponse
import json

def getBusinessLineAndModuleRelation(request):
    businessLineListData = dbModelListToListDict(BusinessService.getAllBusinessLine())
    resultDict = {}
    for blIndex in businessLineListData:
        resultDict[blIndex["id"]] = []
        dataList = dbModelListToListDict(TbBusinessLineModuleRelation.objects.filter(businessLineId__bussinessLineName=blIndex["bussinessLineName"],businessLineId__state=1).order_by("level"))
        for index in dataList:
            resultDict[blIndex["id"]].append(dbModelToDict(TbModules.objects.get(id=index["moduleId_id"])))
    return HttpResponse(ApiReturn(body=resultDict).toJson())
