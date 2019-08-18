from urllib import parse

# Create your views here.
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from apps.myadmin.service.UserLogService import UserLogService

logger = logging.getLogger("django")

def userLogCheckPage(request):
    context = {}
    context["userLog_check"] = "active"
    return render(request, "myadmin/userLog/admin_userLog_check.html", context)

def getUserLog(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy","")
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT u.* from tb_user_log u WHERE 1=1  "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and u.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.userPageNum)
    response = render(request, "myadmin/userLog/subPages/userLog_sub_page.html", context)
    return response

def addUserLog(request):
    userLogData = json.loads(request.POST.get("userLogData"))
    loginName = userLogData["loginName"]
    userName = userLogData["userName"]
    operationUrl = userLogData["operationUrl"]
    operationDesc = userLogData["operationDesc"]
    operationResult = userLogData["operationResult"]
    fromHostIp = userLogData["fromHostIp"]

    searchResult = dbModelListToListDict(TbUserLog.objects.filter(loginName=loginName, userName=userName, operationUrl=operationUrl, operationDesc=operationDesc, operationResult=operationResult, fromHostIp=fromHostIp))
    if len(searchResult) == 0:
        result = TbUserLog()
        result.loginName = loginName
        result.userName = userName
        result.operationUrl = operationUrl
        result.operationDesc = operationDesc
        result.operationResult = operationResult
        result.fromHostIp = fromHostIp
        result.save()
        if result:
            logger.info("addUserLog userLog创建成功 %s" % result)
        return HttpResponse(ApiReturn().toJson())
    else:
        searchResultDict = searchResult[0]
        if searchResultDict["state"] == 0:
            searchResultDict["state"] = 1
            searchResultDict["loginName"] = loginName
            searchResultDict["userName"] = userName
            searchResultDict["operationUrl"] = operationUrl
            searchResultDict["operationDesc"] = operationDesc
            searchResultDict["operationResult"] = operationResult
            searchResultDict["fromHostIp"] = fromHostIp
            UserLogService.updateUserLogService(searchResultDict)
            return HttpResponse(ApiReturn().toJson())
        else:
            logger.info("addUserLog userLog创建失败")
            return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="userLog创建失败,请检查数据是否重复").toJson())

    return HttpResponse(ApiReturn().toJson())


def getUserLogForId(request):
    userLogId = request.POST.get("userLogId")
    print("userLogId:", eval(userLogId))
    try:
        userLogData = TbUserLog.objects.get(id=eval(userLogId))
    except Exception as e:
        message = "userLog查询出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())
    return HttpResponse(ApiReturn(body=dbModelToDict(userLogData)).toJson())


def editUserLog(request):
    try:
        userLogData =json.loads(request.POST.get("userLogData"))
        UserLogService.updateUserLogService(userLogData)
    except Exception as e:
        print(traceback.format_exc())
        message = "编辑userLog发生异常 %s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())
    return HttpResponse(ApiReturn().toJson())

def deleteUserLog(request):
    userLogId = request.POST.get("userLogId", "")
    if not userLogId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="userLogId参数错误").toJson())
    try:
        userLogData = TbUserLog.objects.get(state=1, id=userLogId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="userLogId查询错误 %s" % e).toJson())
    userLogData.state = 0
    userLogData.save()
    return HttpResponse(ApiReturn().toJson())

def resetUserLog(request):
    userLogId = request.POST.get("userLogId", "")
    if not userLogId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="userLogId参数错误").toJson())
    try:
        userLogData = TbUserLog.objects.get(state=0, id=userLogId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="userLogId查询错误 %s" % e).toJson())
    userLogData.state = 1
    userLogData.save()

    return HttpResponse(ApiReturn().toJson())
