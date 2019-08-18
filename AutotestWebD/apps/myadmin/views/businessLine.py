from urllib import parse

# Create your views here.
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from apps.myadmin.service.BusinessLineService import BusinessLineService

logger = logging.getLogger("django")

def businessLineCheckPage(request):
    context = {}
    context["businessLine_check"] = "active"
    return render(request, "myadmin/businessLine/admin_businessLine_check.html",context)

def getBusinessLine(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy","")
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "单接口管理->查看用例->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT u.* from tb_business_line u WHERE 1=1  "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and u.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql,attrList=checkList,page=page,pageNum=commonWebConfig.userPageNum)
    response = render(request, "myadmin/businessLine/subPages/businessLine_sub_page.html",context)
    return response

def getBusinessLineForId(request):
    businessLineId = request.POST.get("businessLineId")
    try:
        businessLineData = TbBusinessLine.objects.get(id=businessLineId)
        requestDict = dbModelToDict(businessLineData)
    except Exception as e:
        message = "查询业务线出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())
    return HttpResponse(ApiReturn(body=requestDict).toJson())


def addBusinessLine(request):
    businessLineRequest = json.loads(request.POST.get("businessLineData"))
    logger.info("addBusinessLine %s" % request.POST.get("businessLineData"))
    businessLineRequest["addTime"] = datetime.datetime.now()
    searchResult = dbModelListToListDict(TbBusinessLine.objects.filter(bussinessLineName=businessLineRequest["businessLineName"]))

    try:
        if len(searchResult) == 0:
            result = TbBusinessLine()
            result.bussinessLineName = businessLineRequest["businessLineName"]
            result.bussinessLineDesc = businessLineRequest["businessLineDesc"]
            result.save()
            if result:
                logger.info("addBusinessLine 业务线添加成功 %s" % result)
            return HttpResponse(ApiReturn().toJson())
        else:
            if searchResult[0]["state"] == 0:
                #如果新建的业务线名称和已经删除的业务线名称一样，进行更新数据
                if searchResult[0]["bussinessLineName"] == businessLineRequest["businessLineName"]:
                    searchResult[0]["state"] = 1
                    searchResult[0]["bussinessLineDesc"] = businessLineRequest["businessLineDesc"]
                    BusinessLineService.updateBusinessLine(searchResult[0])
                    return HttpResponse(ApiReturn().toJson())
                else:
                    logger.info("addBusinessLine 业务线创建失败")
                    return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="业务线创建失败,请检查账号是否重复").toJson())
            else:
                logger.info("addBusinessLine 管理员创建失败")
                return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="业务线创建失败,请检查账号是否重复").toJson())
    except Exception as e:
        message = "添加业务线失败 :%s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="业务线创建失败,请检查账号是否重复").toJson())


def editBusinessLine(request):
    try:
        requestDict = json.loads(request.POST.get("businessLineData"))
        requestDict["modTime"] = datetime.datetime.now()
        requestDict["bussinessLineName"] = requestDict["businessLineName"]
        requestDict["bussinessLineDesc"] = requestDict["businessLineDesc"]
        del requestDict["businessLineName"]
        del requestDict["businessLineDesc"]
        BusinessLineService.updateBusinessLine(requestDict)

    except Exception as e:
        print(traceback.format_exc())
        message = "编辑用户数据发生异常 %s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())

    return HttpResponse(ApiReturn().toJson())

def delBusinessLine(request):
    businessLineId = request.POST.get("businessLineId","")
    if not businessLineId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="businessLineId参数错误").toJson())
    try:
        businessLineData = TbBusinessLine.objects.get(state=1, id=businessLineId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="businessLineId查询错误 %s" % e).toJson())
    businessLineData.state = 0
    businessLineData.save()

    return HttpResponse(ApiReturn().toJson())

def resetBusinessLine(request):
    businessLineId = request.POST.get("businessLineId","")
    if not businessLineId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="businessLineId参数错误").toJson())
    try:
        businessLineData = TbBusinessLine.objects.get(state=0, id=businessLineId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="businessLineId查询错误 %s" % e).toJson())
    businessLineData.state = 1
    businessLineData.save()

    return HttpResponse(ApiReturn().toJson())




