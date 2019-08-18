from django.shortcuts import render,HttpResponse
from urllib import parse
from apps.interface.services.HTTP_interfaceService import HTTP_interfaceService
from apps.common.config import commonWebConfig
from apps.common.func.CommonFunc import *
from apps.common.func.LanguageFunc import *
from apps.config.services.businessLineService import BusinessService
from apps.config.services.modulesService import ModulesService
from apps.config.services.sourceService import SourceService
from apps.config.services.uriService import UriService
from apps.config.services.serviceConfService import ServiceConfService
from apps.config.services.http_confService import HttpConfService
from apps.config.views.http_conf import getDebugBtn
from apps.common.helper.ApiReturn import ApiReturn
from apps.common.func.WebFunc import *
from AutotestWebD.settings import isRelease
import json,traceback
from django.shortcuts import render,HttpResponse
from urllib import parse
from apps.interface.services.HTTP_interfaceService import HTTP_interfaceService
from apps.common.config import commonWebConfig
from apps.common.func.CommonFunc import *
from apps.common.func.LanguageFunc import *
from apps.config.services.businessLineService import BusinessService
from apps.config.services.modulesService import ModulesService
from apps.config.services.sourceService import SourceService
from apps.config.services.uriService import UriService
from apps.config.services.serviceConfService import ServiceConfService
from apps.config.services.http_confService import HttpConfService
from apps.config.views.http_conf import getDebugBtn
from apps.common.helper.ApiReturn import ApiReturn
from apps.common.func.WebFunc import *
from AutotestWebD.settings import isRelease
import json,traceback
from all_models.models.A0011_version_manage import *
from apps.version_manage.services.common_service import VersionService

retmsg = ""
logger = logging.getLogger("web")

def current_version(request):
    langDict = getLangTextDict(request)
    context = {}
    if not isRelease:
        context["env"] = "test"
    context["current_version"] = "current-page"
    context["userName"] = request.session.get("userName")
    #文本
    text = {}
    text["pageTitle"] = "当前版本信息查看"#langDict["web"]["httpInterfacePageHeadings_check"]
    context["text"] = text


    versionObj = TbVersion.objects.filter(type=2)
    context["versionName"] = "没有找到版本"
    context["versionDesc"] = "没有找到版本"
    context["closeTime"] = "None"

    if versionObj:
        context["versionName"] = versionObj[0].versionName
        context["versionDesc"] = versionObj[0].versionDesc
        context["closeTime"] = versionObj[0].closeTime
    return render(request,"InterfaceTest/version_manage/current_version.html",context)

def history_version(request):
    langDict = getLangTextDict(request)
    context = {}
    if not isRelease:
        context["env"] = "test"
    context["history_version"] = "current-page"
    context["userName"] = request.session.get("userName")
    # 文本
    text = {}
    text["pageTitle"] = "历史版本信息查看"  # langDict["web"]["httpInterfacePageHeadings_check"]
    context["text"] = text

    versionObj = TbVersion.objects.filter(type=1).order_by("-closeTime")
    context["versionList"] = []

    for tmpVersion in versionObj:
        tmpVersionInfo = {}
        tmpVersionInfo['versionName'] = tmpVersion.versionName
        tmpVersionInfo['versionDesc'] = tmpVersion.versionDesc
        tmpVersionInfo['closeTime'] = tmpVersion.closeTime
        context["versionList"].append(tmpVersionInfo)
    return render(request, "InterfaceTest/version_manage/history_version.html", context)

def change_version(request):
    langDict = getLangTextDict(request)
    context = {}
    if not isRelease:
        context["env"] = "test"

    versionName = request.GET.get("version","CurrentVersion")

    versionHistorySets = TbVersion.objects.filter(type=1).order_by("-closeTime")
    isVersionExist = False
    for tmpVersion in versionHistorySets:
        if tmpVersion.versionName == versionName:
            isVersionExist = True

    VersionService.setLastVersionSession(request)
    if versionName == "CurrentVersion" or isVersionExist == False:
        VersionService.setToCurrentVersion(request)
        context["current_version"] = "current-page"
        context["userName"] = request.session.get("userName")
        # 文本
        text = {}
        text["pageTitle"] = "当前版本信息查看"  # langDict["web"]["httpInterfacePageHeadings_check"]
        context["text"] = text

        versionObj = TbVersion.objects.filter(type=2)
        context["versionName"] = "没有找到版本"
        context["versionDesc"] = "没有找到版本"
        context["closeTime"] = "没有封板时间"

        if versionObj:
            context["versionName"] = versionObj[0].versionName
            context["versionDesc"] = versionObj[0].versionDesc
            context["closeTime"] = versionObj[0].closeTime

        templatePath = "InterfaceTest/version_manage/current_version.html"

    else:
        VersionService.setToHistoryVersion(request,versionName)
        context["history_version"] = "current-page"
        context["userName"] = request.session.get("userName")
        # 文本
        text = {}
        text["pageTitle"] = "历史版本信息查看"  # langDict["web"]["httpInterfacePageHeadings_check"]
        context["text"] = text

        versionObj = TbVersion.objects.filter(type=1).order_by("-closeTime")
        context["versionList"] = []

        for tmpVersion in versionObj:
            tmpVersionInfo = {}
            tmpVersionInfo['versionName'] = tmpVersion.versionName
            tmpVersionInfo['versionDesc'] = tmpVersion.versionDesc
            tmpVersionInfo['closeTime'] = tmpVersion.closeTime
            context["versionList"].append(tmpVersionInfo)

        templatePath = "InterfaceTest/version_manage/history_version.html"
    return render(request,templatePath , context)