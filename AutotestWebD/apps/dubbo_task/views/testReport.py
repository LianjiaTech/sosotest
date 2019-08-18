from django.shortcuts import HttpResponse
from apps.common.func.CommonFunc import *


def testreport(request,file):
    realFile = "%s/reports/%s" % (BASE_DIR,file)
    fileContent = open(realFile,"r",encoding="utf-8")
    return HttpResponse(fileContent)

