from all_models.models import TbUser
from apps.common.lang_text.language import *

def setLanguage(request,response,language,loginName=""):
    response.set_cookie(KEY_LANGUAGE,language)
    request.session[KEY_LANGUAGE] = language
    if loginName != "":
        #持久化到db
        userData = TbUser.objects.filter(loginName=loginName)
        if userData:
            userData = userData[0]
            userData[KEY_LANGUAGE] = language
            TbUser.objects.update(**userData)

def getLanguage(request):
    if request.session.get(KEY_LANGUAGE,"") in LANGUAGE_LIST:
        return request.session.get(KEY_LANGUAGE,"")
    elif request.COOKIES.get(KEY_LANGUAGE,"") in LANGUAGE_LIST:
        return request.COOKIES.get(KEY_LANGUAGE, "")
    elif request.GET.get(KEY_LANGUAGE,"") in LANGUAGE_LIST:
        return request.GET.get(KEY_LANGUAGE, "")
    else:
        loginName = request.session.get("loginName","")
        if loginName != "":
            userData = TbUser.objects.filter(loginName=loginName)
            if userData and userData[0].language in LANGUAGE_LIST:
                return userData[0].language
            else:
                #都没有找到，默认返回中文
                return DEFAULT_LANGUAGE
        else:
            return DEFAULT_LANGUAGE

def getLangTextDictByLanguage(language):
    if language not in LANGUAGE_LIST:
        #出错默认返回中文
        langClassStr = DEFAULT_LANGUAGE.upper()
    else:
        langClassStr = language.upper()

    return eval("%s.textDict" % langClassStr)

def getLangTextDict(request):
    return getLangTextDictByLanguage(getLanguage(request))
