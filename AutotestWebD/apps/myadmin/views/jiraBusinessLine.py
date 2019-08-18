
from urllib import parse

from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from all_models.models import *
from apps.myadmin.TeamService import TeamService
from apps.myadmin.service.JiraBusinessLineService import JiraBusinessLineService


logger = logging.getLogger("django")

def jiraBusinessLineCheckPage(request):
    context = {}

    context["jiraBusinessLine_check"] = "active"

    return render(request, "myadmin/jiraBusinessLine/admin_jiraBusinessLine_check.html", context)

def getJiraBusinessLine(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy", "")
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "单接口管理->查看用例->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT u.* from tb_webPortal_jira_business_line u WHERE 1=1  "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and u.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.userPageNum)
    response = render(request, "myadmin/jiraBusinessLine/subPages/jiraBusinessLine_sub_page.html", context)
    return response


def getJiraBusinessLineForId(request):
    jiraBusinessLineId = request.POST.get("jiraBusinessLineId")
    try:
        jiraBusinessLineData = TbJiraBusinessLine.objects.get(id=jiraBusinessLineId)
    except Exception as e:
        message = "jira业务线查询出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())
    return HttpResponse(ApiReturn(body=dbModelToDict(jiraBusinessLineData)).toJson())

def addJiraBusinessLine(request):
    jiraBusinessLineRequest = json.loads(request.POST.get("jiraBusinessLineData"))
    logger.info("addJiraBusinessLine %s" % request.POST.get("jiraBusinessLineData"))
    businessLineName = jiraBusinessLineRequest["businessLineName"]
    searchResult = TbJiraBusinessLine.objects.filter(businessLineName=businessLineName)
    '''如果jiraBusinessLine没有添加过，那么就新建'''
    if len(searchResult) == 0:
        result = TbJiraBusinessLine()
        result.businessLineName = jiraBusinessLineRequest["businessLineName"]
        result.businessLineDesc = jiraBusinessLineRequest["businessLineDesc"]
        result.save()
        if result:
            logger.info("addJiraBusinessLine jiraBusinessLine创建成功 %s" % result)
        return HttpResponse(ApiReturn().toJson())
    else:
        '''如果jiraBusinessLine有添加过，但是被删除了，那么更新'''
        jiraBusinessLine = dbModelListToListDict(searchResult)[0]
        if jiraBusinessLine["state"] == 0:
            jiraBusinessLine["state"] = 1
            JiraBusinessLineService.updateJiraBusinessLine(jiraBusinessLine)

            return HttpResponse(ApiReturn().toJson())
        else:
            logger.info("addJiraBusinessLine jiraBusinessLine创建失败")
            return HttpResponse(
                ApiReturn(code=ApiReturn.CODE_WARNING, message="addJiraBusinessLine创建失败,请检查businessLineName是否重复").toJson())


def editJiraBusinessLine(request):
    try:
        requestDict =json.loads(request.POST.get("jiraBusinessLineData"))
        JiraBusinessLineService.updateJiraBusinessLine(requestDict)
    except Exception as e:
        print(traceback.format_exc())
        message = "编辑jira业务线发生异常 %s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())

    return HttpResponse(ApiReturn().toJson())

def delJiraBusinessLine(request):
    jiraBusinessLineId = request.POST.get("jiraBusinessLineId", "")
    if not jiraBusinessLineId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="jiraBusinessLineId参数错误").toJson())
    try:
        jiraBusinessLineData = TbJiraBusinessLine.objects.get(state=1, id=jiraBusinessLineId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="jiraBusinessLineId查询错误 %s" % e).toJson())
    jiraBusinessLineData.state = 0
    jiraBusinessLineData.save()

    return HttpResponse(ApiReturn().toJson())

def resetJiraBusinessLine(request):
    jiraBusinessLineId = request.POST.get("jiraBusinessLineId", "")
    if not jiraBusinessLineId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="jiraBusinessLineId参数错误").toJson())
    try:
        jiraBusinessLineData = TbJiraBusinessLine.objects.get(state=0, id=jiraBusinessLineId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="jiraBusinessLineId查询错误 %s" % e).toJson())
    jiraBusinessLineData.state = 1
    jiraBusinessLineData.save()
    return HttpResponse(ApiReturn().toJson())
