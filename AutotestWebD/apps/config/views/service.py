from apps.config.services.serviceConfService import ServiceConfService
from django.shortcuts import HttpResponse
import json

def getServiceConf(request):
    serviceConf = ServiceConfService.queryServiceConfSort(request)
    return HttpResponse(json.dumps(serviceConf))

