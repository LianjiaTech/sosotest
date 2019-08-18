import django
import os
import sys
import traceback
import logging

rootpath = os.path.dirname(os.path.realpath(__file__)).replace("\\","/")
rootpath = rootpath.split("/apps")[0]
# print(rootpath)
syspath=sys.path
sys.path=[]
sys.path.append(rootpath) #指定搜索路径绝对目录
sys.path.extend([rootpath+i for i in os.listdir(rootpath) if i[0]!="."])#将工程目录下的一级目录添加到python搜索路径中
sys.path.extend(syspath)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutotestWebD.settings")# project_name 项目名称
django.setup()
from all_models.models import *
from AutotestWebD.settings import *
from apps.common.func.CommonFunc import *
import django.utils.timezone

class VersionService(object):

    @staticmethod
    def isCurrentVersion(request):
        if request.session.get("version") == "CurrentVersion":
            return True
        else:
            return False

    @staticmethod
    def setToCurrentVersion(request):

        versionObj = TbVersion.objects.filter(type=2)
        if versionObj:
            request.session["CurrentVersion"] = versionObj[0].versionName
            request.session["version"] = "CurrentVersion"
            return True
        elif len(TbVersion.objects.all()) == 0:
            request.session["CurrentVersion"] = "V2.2"
            request.session["version"] = "CurrentVersion"
            return True
        else:
            return False

    @staticmethod
    def setLastVersionSession(request):
        versionObj = TbVersion.objects.filter(type=1).order_by("-closeTime")
        if versionObj:
            request.session["LastVersion"] = versionObj[0].versionName
            return True
        else:
            request.session["LastVersion"] = ""
            return False

    @staticmethod
    def setToHistoryVersion(request,versionName):
        versionHistorySets = TbVersion.objects.filter(type=1).order_by("-closeTime")
        isVersionExist = False
        for tmpVersion in versionHistorySets:
            if tmpVersion.versionName == versionName:
                isVersionExist = True
        if isVersionExist:
            request.session["version"] = versionName
            return True
        else:
            return False

    @staticmethod
    def getVersionName(request):
        return request.session.get("version")