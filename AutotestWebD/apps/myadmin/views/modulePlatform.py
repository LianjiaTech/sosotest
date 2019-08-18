from urllib import parse

# Create your views here.
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *

logger = logging.getLogger("django")

def modulePlatformCheckPage(request):
    context = {}
    context["modulePlatform_check"] = "active"
    return render(request, "myadmin/modulePlatform/admin_modulePlatform_check.html", context)


def getModulePlatform(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy","")
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT u.* from tb_webPortal_jira_module_platform_relation u WHERE 1=1  "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and u.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.userPageNum)
    for pageData in context["pageDatas"]:
        jiraModule = TbjiraModule.objects.get(id=pageData["jiraModuleId"]).moduleName
        pageData["jiraModule"] = jiraModule
        moduleName = TbModules.objects.get(id=pageData["platformModuleId"]).moduleName
        pageData["platform"] = moduleName
    response = render(request, "myadmin/modulePlatform/subPages/modulePlatform_sub_page.html",context)
    return response


def getAllJiraModules(request):
    jiraModules = []
    jiraModuleList = TbjiraModule.objects.filter(state=1)
    if len(jiraModuleList) == 0:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="没有可用jira模块,请联系管理员").toJson())
    for jiraModule in jiraModuleList:
        if jiraModule.moduleName not in jiraModules:
            jiraModules.append(jiraModule.moduleName)
    return HttpResponse(ApiReturn(body=jiraModules).toJson())


def getAllModuleNames(request):
    moduleNames = []
    moduleList = TbModules.objects.filter(state=1)
    if len(moduleList) == 0:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="没有可用模块，请联系管理员").toJson())
    for module in moduleList:
        if module.moduleName not in moduleNames:
            moduleNames.append(module.moduleName)
    return HttpResponse(ApiReturn(body=moduleNames).toJson())


def addModulePlatform(request):
    modulePlatformData = json.loads(request.POST.get("modulePlatformData"))
    jiraModule = modulePlatformData["jiraModule"]
    module = modulePlatformData["platform"]

    jiraModulePlatform = TbJiraModulePlatFormRelation()
    jiraModulePlatform.jiraModuleId = TbjiraModule.objects.get(moduleName=jiraModule, state=1)
    jiraModulePlatform.platformModuleId = TbModules.objects.get(moduleName=module, state=1)
    modulePlatform = TbJiraModulePlatFormRelation.objects.filter(jiraModuleId=jiraModulePlatform.jiraModuleId, platformModuleId=jiraModulePlatform.platformModuleId)
    if len(modulePlatform) == 0:
        jiraModulePlatform.save()
        return HttpResponse(ApiReturn().toJson())
    else:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="数据已存在，请重新添加").toJson())


def getModulePlatformForId(request):
    modulePlatformId = request.POST.get("modulePlatformId")
    jiraModulePlatform = TbJiraModulePlatFormRelation.objects.get(id=modulePlatformId)
    jiraModuleName = jiraModulePlatform.jiraModuleId.moduleName
    moduleName = jiraModulePlatform.platformModuleId.moduleName
    modulePlatformDict = {}
    modulePlatformDict["jiraModule"] = jiraModuleName
    modulePlatformDict["platform"] = moduleName

    return HttpResponse(ApiReturn(body=modulePlatformDict).toJson())

def deleteModulePlatform(request):
    modulePlatformId = request.POST.get("modulePlatformId")
    TbJiraModulePlatFormRelation.objects.get(id=modulePlatformId).delete()
    return HttpResponse(ApiReturn().toJson())

def editModulePlatform(request):
    modulePlatformData = json.loads(request.POST.get("modulePlatformData"))
    jiraModule = TbjiraModule.objects.get(moduleName=modulePlatformData["jiraModule"])
    platform = TbModules.objects.get(moduleName=modulePlatformData["platform"])
    jiraModulePlatform = TbJiraModulePlatFormRelation.objects.get(id=modulePlatformData["id"])
    jiraModulePlatform.jiraModuleId = jiraModule
    jiraModulePlatform.platformModuleId = platform
    jiraModulePlatform.save()
    return HttpResponse(ApiReturn().toJson())

def getJiraModuleId(request):
    jiraModule = request.POST.get("jiraModule")
    jiraModuleId = TbjiraModule.objects.filter(moduleName=jiraModule).values('id')
    if len(jiraModuleId) == 0:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="输入的jira模块名称不正确，请重新输入。").toJson())
    jiraModuleIdList = []
    jiraModuleIdList.append(jiraModuleId[0]["id"])
    return HttpResponse(ApiReturn(body=jiraModuleIdList).toJson())

def getModuleId(request):
    moduleName = request.POST.get("moduleName")
    moduleId = TbModules.objects.get(moduleName=moduleName).values('id')
    moduleIdList = []
    return HttpResponse(ApiReturn(body=moduleIdList.append(moduleId[0]["id"])).toJson())