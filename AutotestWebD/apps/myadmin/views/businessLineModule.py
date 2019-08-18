from urllib import parse

# Create your views here.
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *

logger = logging.getLogger("django")

def businessLineModuleCheckPage(request):
    context = {}
    context["businessLine_module_check"] = "active"
    return render(request, "myadmin/businessLineModule/admin_businessLine_module_check.html", context)


def getBusinessLineModule(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy","")
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT u.* from tb_businessLine_module_relation u WHERE 1=1  "
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
        businessLineName = TbBusinessLine.objects.get(id=pageData["businessLineId"]).bussinessLineName
        pageData["businessLineName"] = businessLineName
        moduleName = TbModules.objects.get(id=pageData["moduleId"]).moduleName
        pageData["moduleName"] = moduleName
    response = render(request, "myadmin/businessLineModule/subPages/businessLine_module_sub_page.html",context)
    return response


def getAllBusinessLines(request):
    businessLineNames = []
    businessLineList = TbBusinessLine.objects.filter(state=1)
    if len(businessLineList) == 0:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="没有可用业务线,请联系管理员").toJson())
    for businessLine in businessLineList:
        if businessLine.bussinessLineName not in businessLineNames:
            businessLineNames.append(businessLine.bussinessLineName)
    return HttpResponse(ApiReturn(body=businessLineNames).toJson())


def getAllModuleNames(request):
    moduleNames = []
    moduleList = TbModules.objects.filter(state=1)
    if len(moduleList) == 0:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="没有可用模块，请联系管理员").toJson())
    for module in moduleList:
        if module.moduleName not in moduleNames:
            moduleNames.append(module.moduleName)
    return HttpResponse(ApiReturn(body=moduleNames).toJson())


def addBusinessLineModule(request):
    businessLineModuleData = json.loads(request.POST.get("businessLineModuleData"))
    businessLine = businessLineModuleData["businessLine"]
    module = businessLineModuleData["module"]
    level = businessLineModuleData["level"]

    businessLineModule = TbBusinessLineModuleRelation()
    businessLineModule.businessLineId = TbBusinessLine.objects.get(bussinessLineName=businessLine, state=1)
    businessLineModule.moduleId = TbModules.objects.get(moduleName=module, state=1)
    businessLineModule.level = level
    businessLineModuleRelation = TbBusinessLineModuleRelation.objects.filter(businessLineId=businessLineModule.businessLineId, moduleId=businessLineModule.moduleId)
    if len(businessLineModuleRelation) == 0:
        businessLineModule.save()
        return HttpResponse(ApiReturn().toJson())
    else:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="数据已存在，请重新添加").toJson())


def getBusinessLineModuleForId(request):
    businessLineModuleId = request.POST.get("businessLineModuleId")
    businessLineModule = TbBusinessLineModuleRelation.objects.get(id=businessLineModuleId)
    bussinessLineName = businessLineModule.businessLineId.bussinessLineName
    moduleName = businessLineModule.moduleId.moduleName
    businessLineDict = {}
    businessLineDict["bussinessLineName"] = bussinessLineName
    businessLineDict["moduleName"] = moduleName
    businessLineDict["level"] = businessLineModule.level
    return HttpResponse(ApiReturn(body=businessLineDict).toJson())

def delBusinessLineModule(request):
    businessLineModuleId = request.POST.get("businessLineModuleId")
    TbBusinessLineModuleRelation.objects.get(id=businessLineModuleId).delete()
    return HttpResponse(ApiReturn().toJson())

def editBusinessLineModule(request):
    businessLineModuleData = json.loads(request.POST.get("businessLineModuleData"))
    bussinessLineId = TbBusinessLine.objects.get(bussinessLineName=businessLineModuleData["businessLine"])
    moduleId = TbModules.objects.get(moduleName=businessLineModuleData["module"])
    businessLineModule = TbBusinessLineModuleRelation.objects.get(id=businessLineModuleData["id"])
    businessLineModule.businessLineId = bussinessLineId
    businessLineModule.moduleId = moduleId
    businessLineModule.level = businessLineModuleData["level"]
    businessLineModule.save()
    return HttpResponse(ApiReturn().toJson())

def getBusinessLineId(request):
    businessLineName = request.POST.get("businessLineName")
    businessLineId = TbBusinessLine.objects.filter(bussinessLineName=businessLineName).values('id')
    if len(businessLineId) == 0:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="输入的业务线名称不正确，请重新输入。").toJson())
    businessLineIdList = []
    businessLineIdList.append(businessLineId[0]["id"])
    return HttpResponse(ApiReturn(body=businessLineIdList).toJson())

def getModuleId(request):
    moduleName = request.POST.get("moduleName")
    moduleId = TbModules.objects.get(moduleName=moduleName).values('id')
    moduleIdList = []
    return HttpResponse(ApiReturn(body=moduleIdList.append(moduleId[0]["id"])).toJson())