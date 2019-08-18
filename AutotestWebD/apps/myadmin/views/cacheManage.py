from urllib import parse

# Create your views here.
from apps.common.model.RedisDBConfig import RedisCache
from apps.common.func.WebFunc import *

logger = logging.getLogger("django")

def cacheManageCheckPage(request):
    context = {}
    context["cacheManage_check"] = "active"
    return render(request, "myadmin/cacheManage/admin_cacheManage_check.html",context)

def addCacheData(request):
    cacheData = json.loads(request.POST.get("cacheData"))
    try:
        RedisCache().set_data(cacheData["cacheKey"], cacheData["cacheValue"])
        return HttpResponse(ApiReturn().toJson())
    except ValueError:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="给缓存添加数据异常，请联系管理员。").toJson())


def getCacheManage(request):
    context = {}
    checkArr = parse.unquote(request.POST.get("checkArr", None))

    if "t" in (json.dumps(checkArr)).lower():
        try:
            checkArrDict = json.loads(checkArr)
            if checkArrDict["cachekey"] != "":
                try:
                    value = RedisCache().get_data(checkArrDict["cachekey"])
                    context["pageDatas"] = [{"key":checkArrDict["cachekey"], "values":value}]
                except ValueError:
                    context = {}

                response = render(request, "myadmin/cacheManage/subPages/cacheManage_sub_page.html", context)
                return response
        except Exception:
            return render(request, "myadmin/cacheManage/subPages/cacheManage_sub_page.html", context)

    try:
        allKeys, allDatas = RedisCache().getAllDatas()
    except ValueError:
        print(traceback.format_exc())
        return render(request, "myadmin/cacheManage/subPages/cacheManage_sub_page.html", context)

    allDatasDict = dict(zip(allKeys, allDatas))
    valuesList = []
    for key in allDatasDict:
        valuesDict = {}
        valuesDict["key"] = key
        valuesDict["values"] = allDatasDict[key]
        valuesList.append(valuesDict)
    context["pageDatas"] = valuesList
    response = render(request, "myadmin/cacheManage/subPages/cacheManage_sub_page.html", context)
    return response

def getCacheValueForCacheKey(request):
    cacheDataKey = request.POST.get("cacheDataKey", None)
    dataDict = {}
    if cacheDataKey:
        try:
            value = RedisCache().get_data(cacheDataKey)
            dataDict["cacheKey"] = cacheDataKey
            dataDict["cacheValue"] = value
            return HttpResponse(ApiReturn(body=dataDict).toJson())
        except ValueError:
            return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="查询缓存出错，请联系管理员").toJson())
    else:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="查询缓存出错，请联系管理员").toJson())

def editCacheData(request):
    cacheData = json.loads(request.POST.get("cacheData"))
    try:
        RedisCache().set_data(cacheData["cacheKey"], cacheData["cacheValue"])
        return HttpResponse(ApiReturn().toJson())
    except ValueError:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="编辑缓存出错，请联系管理员").toJson())
        

def deleteCacheData(request):
    cacheDataKey = request.POST.get("cacheDataKey",None)
    if cacheDataKey:
        try:
            RedisCache().del_data(cacheDataKey)
            return HttpResponse(ApiReturn().toJson())
        except ValueError as e:
            print(traceback.format_exc())
            message = "删除数据错误，请联系管理员 %s" % e
            logger.error(message)
            return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())

def flushAllDatas(request):
    try:
        RedisCache().flushall()
        return HttpResponse(ApiReturn().toJson())
    except ValueError as e:
        print(traceback.format_exc())
        message = "清空所有数据出错，请联系管理员 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())


