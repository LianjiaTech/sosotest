import json
from urllib import parse

# Create your views here.
from all_models.models import TbUser, TbAdminTeam, TbAdminUserTeamRelation
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from apps.myadmin.TeamService import TeamService
from apps.myadmin.service.TeamUserRelationService import TeamUserRelationService

logger = logging.getLogger("django")

def teamCheckPage(request):
    context = {}
    context["team_check"] = "active"
    return render(request,"myadmin/user/admin_team_check.html",context)

def getAllTeammates(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy","")
    page = request.POST.get("page")

    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "单接口管理->查看用例->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT t.* from tb_admin_user_team_relation t WHERE 1=1 and t.state=1 "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and t.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql,attrList=checkList,page=page,pageNum=commonWebConfig.userPageNum)

    response = render(request, "myadmin/user/subPages/userRole_sub_page.html",context)
    return response


def getTeamForId(request):
    teamId = request.POST.get("teamId")
    try:
        teamData = TbAdminTeam.objects.get(id=teamId)
    except Exception as e:
        message = "小组查询出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())
    return HttpResponse(ApiReturn(body=dbModelToDict(teamData)).toJson())

def addTeam(request):
    teamRequest = json.loads(request.POST.get("teamData"))
    logger.info("addTeam %s" % request.POST.get("teamData"))
    teamRequest["addTime"] = datetime.datetime.now()

    try:
        try:
            searchResult = TbAdminTeam.objects.get(teamKey=teamRequest["teamKey"])
            searchResultDict = dbModelToDict(searchResult)
            if searchResult:
                if searchResultDict["state"] == 0:
                    # 如果新建的小组名称和已经删除的小组名称一样，进行更新数据
                    if searchResultDict["teamName"] == teamRequest["teamName"]:
                        searchResultDict["state"] = 1
                        TeamService.updateTeam(searchResultDict)
                    else:
                        logger.info("addTeam 小组创建失败")
                        return HttpResponse(
                            ApiReturn(code=ApiReturn.CODE_WARNING, message="小组创建失败,请检查小组key是否重复").toJson())
                else:
                    logger.info("addTeam 小组创建失败")
                    return HttpResponse(
                        ApiReturn(code=ApiReturn.CODE_WARNING, message="小组创建失败,请检查小组key是否重复").toJson())
        except:
            result = TbAdminTeam.objects.create(**teamRequest)
            if result:
                logger.info("addTeam 小组创建成功 %s" % result)
    except Exception as e:
        logger.info("addTeam 小组创建失败 %s" % e)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="小组创建失败 %s,请检查小组key是否重复" % e).toJson())
    return HttpResponse(ApiReturn().toJson())


def editTeam(request):
    try:
        requestDict =json.loads(request.POST.get("teamData"))
        requestDict["modTime"] = datetime.datetime.now()
        TeamService.updateTeam(requestDict)
    except Exception as e:
        print(traceback.format_exc())
        message = "编辑小组数据发生异常 %s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())

    return HttpResponse(ApiReturn().toJson())

def delTeam(request):
    teamId = request.POST.get("teamId", "")
    if not teamId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="teamId参数错误").toJson())
    try:
        teamData = TbAdminTeam.objects.get(state=1, id=teamId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="teamId查询错误 %s" % e).toJson())
    teamData.state = 0
    teamData.save()

    return HttpResponse(ApiReturn().toJson())

def addUsersToTeam(request):
    teamRequest = json.loads(request.POST.get("teamUsersData"))
    logger.info("addTeam %s" % request.POST.get("teamUsersData"))
    teamId = teamRequest["teamId"]
    try:
        teamData = TbAdminTeam.objects.get(id=teamId)
        teamDict = dbModelToDict(teamData)
        teamKey = teamDict["teamKey"]
        loginNames = teamRequest["loginNames"]
        userTeamData = {}
        for loginName in loginNames:
            userTeamData["teamKey"] = teamKey
            userTeamData["loginName"] = loginName
            data = TbAdminUserTeamRelation.objects.filter(loginName=loginName)
            teamMate = dbModelListToListDict(data)
            for user in teamMate:
                if user["teamKey"] == teamKey:
                    if user["state"] == 0:
                        TeamUserRelationService.updateTeamUser(userTeamData)
                    else:
                        logger.info("addTeamUser 添加小组成员失败")
                        return HttpResponse(
                            ApiReturn(code=ApiReturn.CODE_WARNING, message="小组创建失败,请检查小组成员是否已经存在").toJson())
                else:
                    result = TbAdminUserTeamRelation.objects.create(**userTeamData)
                    if result:
                        logger.info("addTeamUser 添加小组成员成功 %s" % result)
    except:
        result = TbAdminUserTeamRelation.objects.create(**userTeamData)
        if result:
            logger.info("addTeamUser 添加小组成员成功 %s" % result)
    return HttpResponse(ApiReturn().toJson())


def getAllUsers(request):
    try:
        usersResult = TbUser.objects.filter(state=1)
        usersDict = dbModelListToListDict(usersResult)
    except Exception as e:
        message = "查询用户出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())
    return HttpResponse(ApiReturn(body=usersDict).toJson())


