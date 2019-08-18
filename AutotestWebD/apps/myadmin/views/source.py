from urllib import parse

# Create your views here.
from all_models.models import *
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from apps.myadmin.service.SourceService import SourceService


logger = logging.getLogger("django")

def sourceCheckPage(request):
    context = {}
    context["source_check"] = "active"
    return render(request, "myadmin/source/admin_source_check.html",context)

def getSource(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy","")
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT u.* from tb_source u WHERE 1=1"
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and u.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql,attrList=checkList,page=page,pageNum=commonWebConfig.userPageNum)
    response = render(request, "myadmin/source/subPages/source_sub_page.html",context)
    return response

def getSourceForId(request):
    sourceId = request.POST.get("sourceId")
    try:
        sourceData = TbSource.objects.get(id=sourceId)
        requestDict = dbModelToDict(sourceData)
    except Exception as e:
        message = "查询来源出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())
    return HttpResponse(ApiReturn(body=requestDict).toJson())


def addSource(request):
    sourceRequest = json.loads(request.POST.get("sourceData"))
    logger.info("addSource %s" % request.POST.get("sourceData"))
    sourceRequest["addTime"] = datetime.datetime.now()
    searchResult = dbModelListToListDict(TbSource.objects.filter(sourceName=sourceRequest["sourceName"]))

    try:
        if len(searchResult) == 0:
            result = TbSource()
            result.sourceName = sourceRequest["sourceName"]
            result.sourceDesc = sourceRequest["sourceDesc"]
            result.save()
            if result:
                logger.info("addSource 来源添加成功 %s" % result)
            return HttpResponse(ApiReturn().toJson())
        else:
            searchData = searchResult[0]
            if searchData["state"] == 0:
                searchData["state"] = 1
                searchData["sourceDesc"] = sourceRequest["sourceDesc"]
                SourceService.updateSource(searchData)
                return HttpResponse(ApiReturn().toJson())
            else:
                logger.info("addSource 来源创建失败")
                return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="来源创建失败,请检查账号是否重复").toJson())
    except Exception as e:
        message = "添加来源失败 :%s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="来源创建失败,请检查账号是否重复").toJson())


def editSource(request):
    try:
        requestDict = json.loads(request.POST.get("sourceData"))
        requestDict["modTime"] = datetime.datetime.now()
        SourceService.updateSource(requestDict)

    except Exception as e:
        print(traceback.format_exc())
        message = "编辑来源发生异常 %s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())

    return HttpResponse(ApiReturn().toJson())

def delSource(request):
    sourceId = request.POST.get("sourceId","")
    if not sourceId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="sourceId参数错误").toJson())
    try:
        sourceData = TbSource.objects.get(state=1, id=sourceId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="moduleId查询错误 %s" % e).toJson())
    sourceData.state = 0
    sourceData.save()

    return HttpResponse(ApiReturn().toJson())


def resetSource(request):
    sourceId = request.POST.get("sourceId","")
    if not sourceId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="sourceId参数错误").toJson())
    try:
        sourceData = TbSource.objects.get(state=0, id=sourceId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="moduleId查询错误 %s" % e).toJson())
    sourceData.state = 1
    sourceData.save()

    return HttpResponse(ApiReturn().toJson())

