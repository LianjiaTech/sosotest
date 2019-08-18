from urllib import parse

# Create your views here.
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *

logger = logging.getLogger("django")

def jiraBusinessLinePlatformCheckPage(request):
    context = {}
    context["jiraBusinessLinePlatform_check"] = "active"
    return render(request, "myadmin/jiraBusinessLinePlatformRelation/admin_jiraBusinessLinePlatform_check.html", context)


def getJiraBusinessLinePlatform(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy","")
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT u.* from tb_webPortal_jira_business_line_platform_relation u WHERE 1=1  "
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
        jiraBusinessLine = TbJiraBusinessLine.objects.get(id=pageData["jiraBusinessLineId"]).businessLineName
        pageData["jiraBusinessLine"] = jiraBusinessLine
        platformBusinessLine = TbBusinessLine.objects.get(id=pageData["platformBusinessLineId"]).bussinessLineName
        pageData["platformBusinessLine"] = platformBusinessLine
    response = render(request, "myadmin/jiraBusinessLinePlatformRelation/subPages/jiraBusinessLinePlatform_sub_page.html",context)
    return response


def getAllJiraBusinessLines(request):
    jiraBusinessLines = []
    jiraBusinessLineList = TbJiraBusinessLine.objects.filter(state=1)
    if len(jiraBusinessLineList) == 0:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="没有可用jira业务线,请联系管理员").toJson())
    for jiraBusinessLine in jiraBusinessLineList:
        if jiraBusinessLine.businessLineName not in jiraBusinessLines:
            jiraBusinessLines.append(jiraBusinessLine.businessLineName)
    return HttpResponse(ApiReturn(body=jiraBusinessLines).toJson())


def getAllPlatformBusinessLines(request):
    platformBusinessLines = []
    platformBusinessLineList = TbBusinessLine.objects.filter(state=1)
    if len(platformBusinessLineList) == 0:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="没有可用平台业务线，请联系管理员").toJson())
    for platformBusinessLine in platformBusinessLineList:
        if platformBusinessLine.bussinessLineName not in platformBusinessLines:
            platformBusinessLines.append(platformBusinessLine.bussinessLineName)
    return HttpResponse(ApiReturn(body=platformBusinessLines).toJson())


def addJiraBusinessLinePlatform(request):
    jiraBusinessLinePlatformData = json.loads(request.POST.get("jiraBusinessLinePlatformData"))
    jiraBusinessLine = jiraBusinessLinePlatformData["jiraBusinessLine"]
    platformBusinessLine = jiraBusinessLinePlatformData["platformBusinessLine"]

    jiraBusinessLinePlatform = TbJiraBusinessLinePlatFormRelation()
    jiraBusinessLinePlatform.jiraBusinessLineId = TbJiraBusinessLine.objects.get(businessLineName=jiraBusinessLine, state=1)
    jiraBusinessLinePlatform.platformBusinessLineId = TbBusinessLine.objects.get(bussinessLineName=platformBusinessLine, state=1)
    jiraBusinessLinePlatformRelation = TbJiraBusinessLinePlatFormRelation.objects.filter(jiraBusinessLineId=jiraBusinessLinePlatform.jiraBusinessLineId, platformBusinessLineId=jiraBusinessLinePlatform.platformBusinessLineId)
    if len(jiraBusinessLinePlatformRelation) == 0:
        jiraBusinessLinePlatform.save()
        return HttpResponse(ApiReturn().toJson())
    else:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="数据已存在，请重新添加").toJson())


def getJiraBusinessLinePlatformForId(request):
    jiraBusinessLinePlatformId = request.POST.get("jiraBusinessLinePlatformId")
    jiraBusinessLinePlatform = TbJiraBusinessLinePlatFormRelation.objects.get(id=jiraBusinessLinePlatformId)
    jiraBusinessLineName = jiraBusinessLinePlatform.jiraBusinessLineId.businessLineName
    platformBusinessLineName = jiraBusinessLinePlatform.platformBusinessLineId.bussinessLineName
    jiraBusinessLinePlatformDict = {}
    jiraBusinessLinePlatformDict["jiraBusinessLine"] = jiraBusinessLineName
    jiraBusinessLinePlatformDict["platformBusinessLine"] = platformBusinessLineName

    return HttpResponse(ApiReturn(body=jiraBusinessLinePlatformDict).toJson())

def deleteJiraBusinessLinePlatform(request):
    jiraBusinessLinePlatformId = request.POST.get("jiraBusinessLinePlatformId")
    TbJiraBusinessLinePlatFormRelation.objects.get(id=jiraBusinessLinePlatformId).delete()
    return HttpResponse(ApiReturn().toJson())

def editJiraBusinessLinePlatform(request):
    jiraBusinessLinePlatformData = json.loads(request.POST.get("jiraBusinessLinePlatformData"))
    jiraBusinessLine = TbJiraBusinessLine.objects.get(businessLineName=jiraBusinessLinePlatformData["jiraBusinessLine"])
    platformBusinessLine = TbBusinessLine.objects.get(bussinessLineName=jiraBusinessLinePlatformData["platformBusinessLine"])
    jiraBusinessLinePlatform = TbJiraBusinessLinePlatFormRelation.objects.get(id=jiraBusinessLinePlatformData["id"])
    jiraBusinessLinePlatform.jiraBusinessLineId = jiraBusinessLine
    jiraBusinessLinePlatform.platformBusinessLineId = platformBusinessLine
    jiraBusinessLinePlatform.save()
    return HttpResponse(ApiReturn().toJson())

def getJiraBusinessLineId(request):
    jiraBusinessLine = request.POST.get("jiraBusinessLine")
    businessLineId = TbJiraBusinessLine.objects.filter(businessLineName=jiraBusinessLine).values('id')
    if len(businessLineId) == 0:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="输入的jira业务线名称不正确，请重新输入。").toJson())
    businessLineIdList = []
    businessLineIdList.append(businessLineId[0]["id"])
    return HttpResponse(ApiReturn(body=businessLineIdList).toJson())

