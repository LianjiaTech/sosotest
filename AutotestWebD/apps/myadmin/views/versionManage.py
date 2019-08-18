from urllib import parse

# Create your views here.
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from apps.myadmin.service.VersionManageService import VersionManageService

logger = logging.getLogger("django")

def versionManageCheckPage(request):
    context = {}
    context["versionManage_check"] = "active"
    return render(request, "myadmin/versionManage/admin_versionManage_check.html", context)

def getVersionManage(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy","")
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT u.* from tb_version u WHERE 1=1  "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and u.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.userPageNum)
    response = render(request, "myadmin/versionManage/subPages/versionManage_sub_page.html", context)
    return response

def addVersionManage(request):
    versionManageData = json.loads(request.POST.get("versionManageData"))
    versionName = versionManageData["versionName"]
    versionDesc = versionManageData["versionDesc"]
    type = versionManageData["type"]
    closeTime = versionManageData["closeTime"]


    searchResult = dbModelListToListDict(TbVersion.objects.filter(versionName=versionName))
    if len(searchResult) == 0:
        result = TbVersion()
        result.versionName = versionName
        result.versionDesc = versionDesc
        result.type = type
        result.closeTime = closeTime
        result.save()
        if result:
            logger.info("addVersionManage versionManage创建成功 %s" % result)
        return HttpResponse(ApiReturn().toJson())
    else:
        searchResultDict = searchResult[0]
        if searchResultDict["state"] == 0:
            searchResultDict["state"] = 1
            searchResultDict["versionName"] = versionName
            searchResultDict["versionDesc"] = versionDesc
            searchResultDict["type"] = type
            searchResultDict["closeTime"] = closeTime
            VersionManageService.updateVersionManage(searchResultDict)
            return HttpResponse(ApiReturn().toJson())
        else:
            logger.info("addVersionManage versionManage创建失败")
            return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="versionManage创建失败,请检查数据是否重复").toJson())

    return HttpResponse(ApiReturn().toJson())


def getVersionManageForId(request):
    versionManageId = request.POST.get("versionManageId")
    try:
        versionManageData = TbVersion.objects.get(id=versionManageId)
        data = dbModelToDict(versionManageData)
        timeList = data["closeTime"].split(" ")
        del data["closeTime"]
        data["closeTime"] = timeList[0]+"T"+timeList[1]
    except Exception as e:
        message = "version查询出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())
    return HttpResponse(ApiReturn(body=data).toJson())


def editVersionManage(request):
    try:
        versionManageData =json.loads(request.POST.get("versionManageData"))
        print("111:", versionManageData)
        VersionManageService.updateVersionManage(versionManageData)
    except Exception as e:
        print(traceback.format_exc())
        message = "编辑version发生异常 %s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())
    return HttpResponse(ApiReturn().toJson())


def deleteVersionManage(request):
    versionManageId = request.POST.get("versionManageId", "")
    if not versionManageId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="versionManageId参数错误").toJson())
    try:
        print("333333")
        versionManageData = TbVersion.objects.get(state=1, id=versionManageId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="versionManageId查询错误 %s" % e).toJson())
    versionManageData.state = 0
    versionManageData.save()
    return HttpResponse(ApiReturn().toJson())

def resetVersionManage(request):
    versionManageId = request.POST.get("versionManageId", "")
    if not versionManageId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="versionManageId参数错误").toJson())
    try:
        versionManageData = TbVersion.objects.get(state=0, id=versionManageId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="versionManageId查询错误 %s" % e).toJson())
    versionManageData.state = 1
    versionManageData.save()

    return HttpResponse(ApiReturn().toJson())
