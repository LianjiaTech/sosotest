from django.shortcuts import render
from django.shortcuts import HttpResponse
from apps.common.helper.ApiReturn import ApiReturn
from all_models.models import *
from apps.common.func.CommonFunc import *
from apps.common.func.LanguageFunc import *
from django.forms.models import model_to_dict

from apps.webportal.services import webPortalService
from apps.webportal.services.webPortalService import WebPortalService
import time,logging
from apps.common.func.WebFunc import *
#web看板的主页面

now_time = datetime.datetime.now()
yes_time = now_time + datetime.timedelta(days=-1)
yes_time_bofore = yes_time.strftime('%Y-%m-%d 00:00:00')
yes_time_after = yes_time.strftime('%Y-%m-%d 23:59:59')
logger = logging.getLogger("django")

def mainPage(request):
    context = {}
    waitTime = request.GET.get("waitTime",2)
    if isInt(waitTime) == False:
        waitTime = 2
    if int(waitTime) < 2:
        waitTime = 2

    context['waitTime'] = waitTime
    return render(request,"webportal/main.html",context)

def httpTestSubPage(request):
    #taskIdList 标准任务集，计入到平台统计的有效的任务集，必须支持从集成开始的5个环境。
    context = {}
    #获取概况
    generalSituation = dbModelListToListDict(WebPortalService.getHttpTestGeneralSituation())
    if generalSituation:
        generalSituation[-1]["statisticalDetail"] = json.loads(generalSituation[-1]["statisticalDetail"])
        context["generalSituation"] = generalSituation[-1]

    else:
        context["generalSituation"] = []

    #获取执行情况
    interfaceTest = WebPortalService.getInterfaceTest()
    if interfaceTest:
        context["interfaceTest"] = interfaceTest
    else:
        context["interfaceTest"] = []

    allBlDict = dbModelListToListDict(TbBusinessLine.objects.filter(state=1).exclude(bussinessLineName="营销云"))
    context["allBl"] = allBlDict

    allEnv = dbModelListToListDict(TbWebPortalStandardEnv.objects.filter(state=1,actionIsShow=1).order_by("lineSort"))
    context["allEnv"] = allEnv
    #获取覆盖度
    coverageRate = WebPortalService.getCoverageRate()
    context["coverageRate"] = coverageRate

    return render(request, "webportal/subpages/httpTestPage.html", context)


def getBusinessLineNameId(request):
    resultList = []
    businessLines = TbWebPortalBusinessLine.objects.filter(isShow=1, state=1).order_by("level")
    for businessLine in businessLines:
        resultDict = {}
        id = businessLine.bussinessLine + "ActionPassrateChart"
        resultDict["name"] = businessLine.bussinessLine
        resultDict["id"] = id
        resultList.append(resultDict)
    return HttpResponse(ApiReturn(body=resultList).toJson())


def unitTestSubPage(request):
    #taskIdList 标准任务集，计入到平台统计的有效的任务集，必须支持从集成开始的5个环境。

    testDict = dbModelToDict(TbWebPortalUnitTestGeneralSituation.objects.last())
    testDetail = json.loads(testDict["unitTestDetail"])
    leftNum = math.ceil(len(testDetail["serviceList"])/2)
    # rightNum = math.floor(len(testDetail))
    leftList = []
    rightList= []
    for index in range(0,len(testDetail["serviceList"])):
        if index < leftNum:
            leftList.append(testDetail["serviceList"][index])
        else:
            rightList.append(testDetail["serviceList"][index])

    context = {}
    context['codeNum'] = testDict["codeNum"]
    context['coverage'] = testDict["coverage"]
    context['coverageRate'] = testDict["coverageRate"]

    context["leftList"] = leftList
    context["rightList"] = rightList
    return render(request,"webportal/subpages/unittestPage.html",context)

def rmiTestSubPage(request):
    #taskIdList 标准任务集，计入到平台统计的有效的任务集，必须支持从集成开始的5个环境。
    context = {}
    context["serviceList"] = dbModelListToListDict(TbWebPortalRmiStandardService.objects.all())
    serviceCoverage = {}
    for index in context["serviceList"]:
        serviceCoverage[index["serviceName"]] = dbModelToDict(TbWebPorRMIServiceTest.objects.filter(service=index["serviceName"]).last())

    context["serviceCoverage"] = serviceCoverage
    allEnv = dbModelListToListDict(TbWebPortalStandardEnv.objects.filter(state=1,rmiIsShow=1).order_by("lineSort"))
    context["allEnv"] = allEnv
    context["generalSituation"] = dbModelToDict(TbWebPortRMIGeneralSituation.objects.last())
    context["interfaceTest"] = dbModelToDict(TbWebPortRMIInterfaceTest.objects.last())
    context["interfaceTest"]["interfaceDetail"] = json.loads(context["interfaceTest"]["interfaceDetail"])
    context["uri"] = "http://0.0.0.0/"
    return render(request,"webportal/subpages/rmitestPage.html",context)


def openApiTestSubPage(request):
    #taskIdList 标准任务集，计入到平台统计的有效的任务集，必须支持从集成开始的5个环境。
    context = {}

    context["generalSituation"] = dbModelToDict(TbWebPortOpenApiGeneralSituation.objects.last())

    # openAPIDBData = TbWebPortOpenApiGeneralSituation.objects.filter()
    context['businessLine'] = dbModelListToListDict(TbOpenApiBusinessLine.objects.filter(state=1))
    context["allEnv"] = dbModelListToListDict(TbWebPortalStandardEnv.objects.filter(state=1,openapiIsShow=1).order_by("lineSort"))
    context["interfaceTest"] = WebPortalService.getOpenApiIntrefaceTest()

    context["openApiBlTest"] = WebPortalService.getOpenApiBlTest()



    return render(request,"webportal/subpages/openApitestPage.html",context)



def uiTestSubPage(request):
    #taskIdList 标准任务集，计入到平台统计的有效的任务集，必须支持从集成开始的5个环境。
    context = {}

    context["allEnv"] = dbModelListToListDict(TbWebPortalStandardEnv.objects.filter(state=1, uiIsShow=1).order_by("lineSort"))
    generalSituation = TbWebPortalUIGeneralSituation.objects.last()
    context["generalSituation"] = json.loads(generalSituation.generalSituationDetail)
    context["uiTest"] = json.loads(dbModelToDict(TbWebPortalUITest.objects.last())["testDetail"])

    context["uiCovered"] = dbModelToDict(TbWebPortalUiCovered.objects.last())
    context["uiCovered"]["coverDetail"] = json.loads(context["uiCovered"]["coverDetail"])
    return render(request,"webportal/subpages/uitestPage.html", context)


def lineGraph(request):
    return render(request,"webportal/subpages/lineGraph.html")


def getAllEnv(request):
    allEnvlist = TbWebPortalStandardEnv.objects.filter(state=1, actionIsShow=1).order_by("lineSort")
    aliasList = []
    for env in allEnvlist:
        if env.alias not in aliasList:
            aliasList.append(env.alias + "(" + env.version + ")")
    return HttpResponse(ApiReturn(body=aliasList).toJson())

def getAllHttpConf(request):
    envList = WebPortalService.getAllHttpConf()
    return HttpResponse(ApiReturn(body=envList).toJson())


def getAllPassRate(request):
    allPassRate = list(TbWebPortalAllPassRate.objects.all())[-7:]
    passRateListForEnv = []
    envList = []
    passRateEnvDict = {}
    aliasList = []
    for passRate in allPassRate:
        testResultList = passRate.testResultMsg
        for testResult in json.loads(testResultList):
            if testResult["env"] not in envList:
                envList.append(testResult["env"])

    envAliasDict = WebPortalService.getAllEnvAlias()
    '''根据最新一条数据中的testResultMessage获得aliasList'''
    for envAlias in envAliasDict:
        aliasList.append(envAliasDict[envAlias])


    '''获得每个环境7天的通过'''
    for env in envList:
        passRateList = []
        for passRate in allPassRate:
            testResultList = passRate.testResultMsg
            for testResult in json.loads(testResultList):
                if env == testResult["env"]:
                    passRateList.append(testResult["passRate"])
        passRateListForEnv.append(passRateList)

    passRateEnvDict["envList"] = aliasList
    passRateEnvDict["passRateDict"] = dict(zip(aliasList, passRateListForEnv))

    return HttpResponse(ApiReturn(body=passRateEnvDict).toJson())

def getBusinessLinesActionPassRate(request):
    resultDict = {}
    resultList = []
    envAliasDict = WebPortalService.getAllEnvAlias()
    businessLines = TbWebPortalBusinessLine.objects.filter(isShow=1, state=1).order_by("level")
    for businessLine in businessLines:
        allPassRate = list(TbWebPortalBusinessLineActionPassRate.objects.filter(businessLine=businessLine.bussinessLine, state=1))[-7:]
        passRateListForEnv = []
        envList = []
        passRateEnvDict = {}
        aliasList = []

        for passRate in allPassRate:
            testResultList = passRate.testResultMsg
            for testResult in json.loads(testResultList):
                if testResult["env"] not in envList:
                    envList.append(testResult["env"])

        for envAlias in envAliasDict:
            aliasList.append(envAliasDict[envAlias])

        for env in envList:
            passRateList = []
            for passRate in allPassRate:
                testResultList = passRate.testResultMsg
                for testResult in json.loads(testResultList):
                    if env == testResult["env"]:
                        passRateList.append(testResult["passRate"])
            passRateListForEnv.append(passRateList)

        passRateEnvDict["envList"] = aliasList
        passRateEnvDict["passRateDict"] = dict(zip(aliasList, passRateListForEnv))

        resultDict[businessLine.bussinessLine] = passRateEnvDict

    resultList.append(resultDict)

    return HttpResponse(ApiReturn(body=resultList).toJson())



def getEnvVersionRelation(request):
    aliasList = json.loads(request.POST.get("aliasList", None))
    envVersionList = []
    if aliasList:
        for alias in aliasList:
            version = TbWebPortalStandardEnv.objects.get(state=1, alias=alias).version
            envVersionList.append(alias + "(" + version + ")")
        return HttpResponse(ApiReturn(body=envVersionList).toJson())
    else:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="没有可用的环境, 请联系管理员").toJson())


def getRecentSevenDays(request):
    now = datetime.date.today().strftime('%Y-%m-%d')
    dateList = [now]
    numList = [-1, -2, -3, -4, -5, -6]
    for num in numList:
        date = (datetime.date.today() + datetime.timedelta(days=num)).strftime('%Y-%m-%d')
        dateList.append(date)
    return HttpResponse(ApiReturn(body=dateList).toJson())


def getAllBusinessLines(request):
    businessLines = TbBusinessLine.objects.filter(state=1)
    businessLineList = []
    if len(businessLines) == 0:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="没有可用的业务线 请联系管理员").toJson())
    for tmpBusinessLine in businessLines:
        businessLineList.append(tmpBusinessLine.bussinessLineName)
    return HttpResponse(ApiReturn(body=businessLineList).toJson())


def getRencentDays(request):
    recentDays = WebPortalService.getRencentDays()
    return HttpResponse(ApiReturn(body=recentDays).toJson())


def httpTestCoverageSubPage(request):
    #taskIdList 标准任务集，计入到平台统计的有效的任务集，必须支持从集成开始的5个环境。
    context = {}
    #获取概况
    generalSituation = dbModelListToListDict(WebPortalService.getHttpTestGeneralSituation())
    if generalSituation:
        generalSituation[-1]["statisticalDetail"] = json.loads(generalSituation[-1]["statisticalDetail"])
        context["generalSituation"] = generalSituation[-1]

    else:
        context["generalSituation"] = []

    #获取执行情况
    interfaceTest = WebPortalService.getInterfaceTest()
    if interfaceTest:
        context["interfaceTest"] = interfaceTest
    else:
        context["interfaceTest"] = []

    allBlDict = dbModelListToListDict(TbBusinessLine.objects.filter(state=1).exclude(bussinessLineName="营销云"))
    context["allBl"] = allBlDict

    allEnv = dbModelListToListDict(TbWebPortalStandardEnv.objects.filter(state=1,actionIsShow=1).order_by("lineSort"))
    context["allEnv"] = allEnv
    #获取覆盖度
    coverageRate = WebPortalService.getCoverageRate()
    context["coverageRate"] = coverageRate

    serviceNum = 0
    coverageList = TbWebPortalServiceInterfaceCovered.objects.filter(state=1).order_by("-coverage")
    coverageDictList = []
    for coverage in coverageList:
        serviceNum += 1
        coverageDict = {}
        coverageDict["serviceName"] = coverage.serviceName
        coverageDict["totalNum"] = coverage.standardInterfaceNum
        coverageDict["coverageNum"] = coverage.coveredInterfaceNum
        coverageDict["coverage"] = coverage.coverage
        coverageDictList.append(coverageDict)

    leftNum = math.ceil(serviceNum / 2)
    leftList = []
    rightList = []
    for index in range(0, serviceNum):
            if index < leftNum:
                leftList.append(coverageDictList[index])
            else:
                rightList.append(coverageDictList[index])

    context["leftList"] = leftList
    context["rightList"] = rightList
    return render(request, "webportal/subpages/httpTestCoveragePage.html", context)
