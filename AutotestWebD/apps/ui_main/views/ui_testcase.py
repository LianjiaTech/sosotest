from apps.common.func.CommonFunc import *
from apps.common.func.LanguageFunc import *
from django.shortcuts import render, HttpResponse
from urllib import parse
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from apps.ui_globals.services.global_textService import global_textService
from apps.config.services.serviceConfService import ServiceConfService
import json
from apps.version_manage.services.common_service import VersionService

def index(request):
    langDict = getLangTextDict(request)
    context = {}

    context["uiUserCenterGlobalTextPage"] = "current-page"
    context["userName"] = request.session.get("userName")
    if not isRelease:
        context["env"] = "test"
    # 文本
    text = {}
    text["pageTitle"] = langDict["web"]["httpUserCenterGlobalTextPageTitle"]
    text["subPageTitle"] = langDict["web"]["httpUserCenterGlobalTextSubPageTitle"]

    context["text"] = text

    context.update(getHttpConfForUI())
    context["page"] = 1
    return render(request, "ui_globals/global_text_conf.html", context)
