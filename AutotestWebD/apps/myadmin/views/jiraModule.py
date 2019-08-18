
from urllib import parse

from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from all_models.models import *
from apps.myadmin.TeamService import TeamService
from apps.myadmin.service.JiraModuleService import JiraModuleService
from apps.myadmin.service.TeamPermissionRelationService import TeamPermissionRelationService
from apps.myadmin.service.TeamUserRelationService import TeamUserRelationService


logger = logging.getLogger("django")

def jiraModuleCheckPage(request):
    context = {}

    context["jiraModule_check"] = "active"

    return render(request,"myadmin/jiraModule/admin_jiraModule_check.html",context)

def getJiraModule(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy", "")
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "单接口管理->查看用例->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT u.* from tb_webPortal_jira_module u WHERE 1=1  "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and u.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.userPageNum)
    response = render(request, "myadmin/jiraModule/subPages/jiraModule_sub_page.html", context)
    return response


def getJiraModuleForId(request):
    jiraModuleId = request.POST.get("jiraModuleId")
    try:
        jiraModuleData = TbjiraModule.objects.get(id=jiraModuleId)
    except Exception as e:
        message = "jira模块查询出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())
    return HttpResponse(ApiReturn(body=dbModelToDict(jiraModuleData)).toJson())

def addJiraModule(request):
    jiraModuleRequest = json.loads(request.POST.get("jiraModuleData"))
    logger.info("addJiraModule %s" % request.POST.get("jiraModuleData"))
    moduleName = jiraModuleRequest["moduleName"]
    print("1111:", moduleName)
    searchResult = TbjiraModule.objects.filter(moduleName=moduleName)
    '''如果jiraModule没有添加过，那么就新建'''
    if len(searchResult) == 0:
        result = TbjiraModule()
        result.moduleName = jiraModuleRequest["moduleName"]
        result.moduleDesc = jiraModuleRequest["moduleDesc"]
        result.save()
        if result:
            logger.info("addJiraModule jiraModule创建成功 %s" % result)
        return HttpResponse(ApiReturn().toJson())
    else:
        '''如果jiraModule有添加过，但是被删除了，那么更新'''
        jiraModule = dbModelListToListDict(searchResult)[0]
        if jiraModule["state"] == 0:
            jiraModule["state"] = 1
            JiraModuleService.updateJiraModule(jiraModule)

            return HttpResponse(ApiReturn().toJson())
        else:
            logger.info("addJiraModule jiraModule创建失败")
            return HttpResponse(
                ApiReturn(code=ApiReturn.CODE_WARNING, message="jiraModule创建失败,请检查moduleName是否重复").toJson())


def editJiraModule(request):
    try:
        requestDict =json.loads(request.POST.get("jiraModuleData"))
        JiraModuleService.updateJiraModule(requestDict)
    except Exception as e:
        print(traceback.format_exc())
        message = "编辑jira模块发生异常 %s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())

    return HttpResponse(ApiReturn().toJson())

def delJiraModule(request):
    jiraModuleId = request.POST.get("jiraModuleId", "")
    if not jiraModuleId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="jiraModuleId参数错误").toJson())
    try:
        jiraModuleData = TbjiraModule.objects.get(state=1, id=jiraModuleId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="teamId查询错误 %s" % e).toJson())
    jiraModuleData.state = 0
    jiraModuleData.save()

    return HttpResponse(ApiReturn().toJson())

def resetJiraModule(request):
    jiraModuleId = request.POST.get("jiraModuleId", "")
    if not jiraModuleId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="jiraModuleId参数错误").toJson())
    try:
        jiraModuleData = TbjiraModule.objects.get(state=0, id=jiraModuleId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="jiraModuleId查询错误 %s" % e).toJson())
    jiraModuleData.state = 1
    jiraModuleData.save()
    return HttpResponse(ApiReturn().toJson())
