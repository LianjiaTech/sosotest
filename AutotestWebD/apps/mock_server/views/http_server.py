from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import urllib,json
from all_models_for_mock.models import *
from apps.common.func.CommonFunc import *
from threading import Thread
import logging,traceback,re
from apps.mock_server.services.mock_http_service import MockHttpService
import requests
from apps.common.model.HttpProcesserV2 import HttpProcesserV2
import chardet
import django.core.handlers.wsgi
from apps.common.func.ExecFunc import *

logger = logging.getLogger("django")

def djangoReqGetDictToParamStr(requestGet):
    retStr = ""
    for k,v in requestGet.items():
        retStr += "%s=%s&" %(k,v)

    if retStr!= "":
        return urllib.parse.unquote(retStr[:-1])
    else:
        return retStr

def isRegMatch(regStr,matchedString):
    try:
        if regStr == "/":
            matchRes = False
        else:
            matchRes = re.compile(r'%s' % regStr).match(matchedString)
    except:
        matchRes = False
    finally:
        return matchRes

def getCorrectMockModel(request,service,tagKey,url):
    uriKey = service
    reqMethod = request.method
    reqUrl = urllib.parse.unquote(url)
    reqParam = urllib.parse.unquote(request.META["QUERY_STRING"])

    #先处理header
    processedReqHeader = {}
    for pk, pv in request.META.items():
        if pk.startswith("HTTP_"):
            processedReqHeader[pk[5:]] = pv

    # 处理特殊header，content type等
    processedReqHeader['Content-Type'] = request.META['CONTENT_TYPE']

    theEncoding = request.encoding
    if theEncoding == None:
        theEncoding = "utf8"
    try:
        reqBody = urllib.parse.unquote(bytes.decode(request.body, encoding=theEncoding))
    except:
        # 转码失败的话， reqBody就设置为空
        if "Content-Type" in processedReqHeader.keys() and processedReqHeader['Content-Type'].startswith("multipart/form-data"):
            # s = a.encode("raw_unicode_escape")  变成bytes，并且带着中文的编码
            #formdata 类型
            boundary = processedReqHeader['Content-Type'].split("boundary=")[1]
            splitBoundary = ("--%s" % boundary).encode(theEncoding)
            startStr0 = 'filename="'.encode(theEncoding)
            startStr = "Content-Type: application".encode(theEncoding)
            splitBList = request.body.split(splitBoundary)
            reqBodyBytes = splitBoundary
            for bindex in range(1,len(splitBList)-1):
                if startStr0 in splitBList[bindex]:
                    #是文件类型 舍弃后面的二进制
                    reqBodyBytes = reqBodyBytes+splitBList[bindex].split(startStr)[0]+ b'\r\n\r\nIgnore the real bytes when request is file...\r\n' +splitBoundary
                else:
                    #不是文件类型，直接拼接
                    reqBodyBytes = reqBodyBytes+splitBList[bindex]+splitBoundary
            reqBodyBytes += splitBList[-1]
            try:
                reqBody = urllib.parse.unquote(reqBodyBytes.decode(theEncoding))
            except:
                #如果转码失败，那么就是处理后没有文件的也失败了，进行截取操作
                tobeProcessedBody = str(reqBodyBytes)
                reqBody = tobeProcessedBody[2:-1] if len(tobeProcessedBody) < 1000 else tobeProcessedBody[2:999] + "\r\n(请求体超长，后续省略...)"  # 去掉开头的b' 和 结尾的 ' 最多拿1000个字符。
        else:
            #入股不是formdata，那么就直接byte转换看效果
            tobeProcessedBody = str(request.body)
            reqBody = tobeProcessedBody[2:-1] if len(tobeProcessedBody) < 1000 else tobeProcessedBody[2:999]+"\r\n(请求体超长，后续省略...)" #去掉开头的b' 和 结尾的 ' 最多拿1000个字符。

    mockHttpList = Tb4MockHttp.objects.filter(uriKey=uriKey, reqMethod=reqMethod, reqUrl=reqUrl,tagKey=tagKey, state=1)
    if len(mockHttpList) == 0:
        mockHttpList = Tb4MockHttp.objects.filter(uriKey=uriKey, reqMethod=reqMethod, tagKey=tagKey, state=1)
        regMockModelList = [] #保存正则匹配上的url
        for tmpMockNoUrlInfo in mockHttpList:
            dbUrl = tmpMockNoUrlInfo.reqUrl
            if dbUrl.startswith("^/"):
                if isRegMatch(dbUrl,reqUrl):
                    regMockModelList.append(tmpMockNoUrlInfo)

        if len(regMockModelList) == 0:
            #没有找到mock数据
            return False,HttpResponse("MOCK SERVER ALERT: No mock data found! Please check!"),processedReqHeader,reqUrl,reqParam,reqBody
        else:
            mockHttpList = regMockModelList

    if len(mockHttpList) == 1:
        #如果只有1条记录，直接返回对应的记录即可
        return True,mockHttpList[0],processedReqHeader,reqUrl,reqParam,reqBody

    # 如果不是1条记录，那么就有多条记录，就要处理多条记录通过包含和正则匹配数量最多的获取最佳匹配项
    mostPipeiDict = {}
    maxPipeiCount = 0
    for tmpMockInfo in mockHttpList:
        # 判断每个mock信息是否符合此请求
        tmpPipeiCount = 0
        sReqParam = tmpMockInfo.reqParam
        if sReqParam != "" and ( (sReqParam in reqParam) or isRegMatch(sReqParam,reqParam) ):
            tmpPipeiCount += 1

        sReqBody = tmpMockInfo.reqBody
        if sReqBody != "" and ( (sReqBody in reqBody) or isRegMatch(sReqBody,reqBody)):
            tmpPipeiCount += 1

        sReqHeader = tmpMockInfo.reqHeader
        if sReqHeader != "" and sReqHeader != "{}" and isJson(sReqHeader):
            sReqHeaderDict = json.loads(sReqHeader)
            tmpPipeiHeader = True
            for sreqhk, sreqhv in sReqHeaderDict.items():
                sreqhk = sreqhk.upper()
                if sreqhk not in processedReqHeader.keys() or (processedReqHeader[sreqhk] != sreqhv and isRegMatch(sreqhv,processedReqHeader[sreqhk])):
                    tmpPipeiHeader = False
            if tmpPipeiHeader:
                tmpPipeiCount += 1

        if tmpPipeiCount > maxPipeiCount:
            maxPipeiCount = tmpPipeiCount
        if tmpPipeiCount == 0:
            if sReqParam == "" and sReqBody == "" and (sReqHeader == "" or sReqHeader == "{}"):
                mostPipeiDict[str(tmpPipeiCount)] = tmpMockInfo
        else:
            if str(tmpPipeiCount) not in mostPipeiDict.keys():
                mostPipeiDict[str(tmpPipeiCount)] = tmpMockInfo

    # 判断最大匹配的是否存在
    if str(maxPipeiCount) in mostPipeiDict.keys():
        mostPipeiMockInfo = mostPipeiDict[str(maxPipeiCount)]
        return True,mostPipeiMockInfo,processedReqHeader,reqUrl,reqParam,reqBody
    else:
        if len(mockHttpList) >= 1:
            # 如果Y有多条记录
            return True, mockHttpList[0], processedReqHeader, reqUrl, reqParam, reqBody
        else:
            return False,HttpResponse("MOCK SERVER ALERT: No match mock info found!"),processedReqHeader,reqUrl,reqParam,reqBody

def addMockInvokeHistory(request,mostPipeiMockInfo,reqUrl,reqParam,reqBody,processedReqHeader,respStatusCode,respStatusReason,respContentType,respCharset,respContent,respCookie):
    mockHistory = Tb4MockHttpInvokeHistory()
    ip = ""
    if 'HTTP_X_FORWARDED_FOR' in request.META.keys():
        ip = request.META['HTTP_X_FORWARDED_FOR']
    elif 'REMOTE_ADDR' in request.META.keys():
        ip = request.META['REMOTE_ADDR']
    else:
        ip = "unknown"
    mockHistory.fromHostIp = ip
    mockHistory.mockId = mostPipeiMockInfo.mockId
    mockHistory.title = mostPipeiMockInfo.title
    mockHistory.businessLineId = mostPipeiMockInfo.businessLineId
    mockHistory.moduleId = mostPipeiMockInfo.moduleId

    mockHistory.uriKey = mostPipeiMockInfo.uriKey

    mockHistory.reqMethod = mostPipeiMockInfo.reqMethod
    mockHistory.reqUrl = mostPipeiMockInfo.reqUrl
    mockHistory.reqParam = mostPipeiMockInfo.reqParam
    mockHistory.reqHeader = mostPipeiMockInfo.reqHeader
    mockHistory.reqBody = mostPipeiMockInfo.reqBody

    mockHistory.respStatusCode = mostPipeiMockInfo.respStatusCode
    mockHistory.respCookie = mostPipeiMockInfo.respCookie
    mockHistory.respCharset = mostPipeiMockInfo.respCharset
    mockHistory.respBody = mostPipeiMockInfo.respBody
    mockHistory.respContentType = mostPipeiMockInfo.respContentType
    mockHistory.respStatusReason = mostPipeiMockInfo.respStatusReason
    mockHistory.mockMode = mostPipeiMockInfo.mockMode
    mockHistory.advancedPythonCode = mostPipeiMockInfo.advancedPythonCode

    mockHistory.actualReqUrl = reqUrl[0:255] if len(reqUrl) > 255 else reqUrl
    mockHistory.actualReqParam = reqParam[0:255] if len(reqParam) > 255 else reqParam
    mockHistory.actualReqHeader = processedReqHeader
    mockHistory.actualReqBody = reqBody
    mockHistory.actualRespStatusCode = respStatusCode
    mockHistory.actualRespStatusReason = respStatusReason
    mockHistory.actualRespContentType = "" if respContentType == None else respContentType
    mockHistory.actualRespBody = respContent
    mockHistory.actualRespCookie = respCookie
    mockHistory.actualRespCharset =  "" if respCharset == None else respCharset

    mockHistory.addBy = mostPipeiMockInfo.addBy
    mockHistory.modBy = mostPipeiMockInfo.modBy
    mockHistory.save(force_insert=True)

def getRespVarsByMockModel(mostPipeiMockInfo):
    respContent = mostPipeiMockInfo.respBody

    if mostPipeiMockInfo.respStatusCode != "" and mostPipeiMockInfo.respStatusCode != None:
        respStatusCode = mostPipeiMockInfo.respStatusCode
    else:
        respStatusCode = 200

    if mostPipeiMockInfo.respStatusReason != "" and mostPipeiMockInfo.respStatusReason != None:
        respStatusReason = mostPipeiMockInfo.respStatusReason
    else:
        respStatusReason = "OK"

    if mostPipeiMockInfo.respCharset != "":
        respCharset = mostPipeiMockInfo.respCharset
    else:
        respCharset = None

    if mostPipeiMockInfo.respContentType != "":
        respContentType = mostPipeiMockInfo.respContentType
    else:
        respContentType = None

    if mostPipeiMockInfo.respCookie != None:
        respCookie = mostPipeiMockInfo.respCookie
    else:
        respCookie = ""

    if mostPipeiMockInfo.respHeader != None:
        respHeader = mostPipeiMockInfo.respHeader
    else:
        respHeader = ""

    return respStatusCode,respStatusReason,respContentType,respCharset,respContent,respCookie,respHeader

def processAdvancedMode(mostPipeiMockInfo,request,reqUrl,reqParam,reqBody,processedReqHeader,respStatusCode, respStatusReason, respContentType, respCharset, respContent, respCookie,respHeader):
    mockMode = mostPipeiMockInfo.mockMode
    if mockMode == 1:
        #如果是高级模式，进入python执行层面。
        nameDict = {
            "reqMethod":request.method,  #请求的method GET POST PUT DELTE 等等
            "reqUrl":reqUrl, # mock的接口url
            "reqParam":reqParam, #请求行中的参数字符串 k=1&m=2
            "reqBody": reqBody,  # request body
            "reqHeader": processedReqHeader,  # 请求header dict key都是大写

            "GET": request.GET, # GET dict
            "POST": request.POST, # POST dict

            "isResp": False, #是否使用代码中的 resp相关的数据，不使用就使用默认的
            "respStatusCode":respStatusCode, #返回的状态码，默认 200
            "respStatusReason":respStatusReason, #返回的reason，默认 OK
            "respContentType":respContentType, #返回的数据类型，默认None
            "respCharset":respCharset, #返回的字符集，默认None
            "respContent":respContent, #返回的响应体
            "respCookie":respCookie, # json string 或者 ""空字符串
            "respHeader":respHeader, # json string 或者 ""空字符串
            }

        advancedPythonCode = mostPipeiMockInfo.advancedPythonCode
        importStr = getPythonThirdLib().strip()  #import的默认包
        timeout = getKeywordExecPythonTimeout("timoutForMockAdvancedMode") #最多执行多久
        if "import " in advancedPythonCode:
            return HttpResponse("MOCK SERVER ALERT: Advance mode cannot use import!!!")
        exec(importStr, nameDict)
        execFinalPythonStr = "%s" % (advancedPythonCode)
        class TimeLimited(Thread):
            def __init__(self):
                Thread.__init__(self)
            def run(self):
                try:
                    exec(execFinalPythonStr, nameDict)
                except:
                    nameDict["isResp"] = True
                    nameDict["respContent"] = traceback.format_exc()

        t = TimeLimited()
        t.start()
        t.join(timeout=timeout)
        if t.is_alive():
            stop_thread(t)
        if nameDict['isResp']:
            respStatusCode = nameDict['respStatusCode']
            respStatusReason = nameDict['respStatusReason']
            respContentType = nameDict['respContentType']
            respCharset = nameDict['respCharset']
            respContent = str(nameDict['respContent']) if nameDict['respContent']!= None else ""
            respCookie = nameDict['respCookie']
            respHeader = nameDict['respHeader']

    return respStatusCode, respStatusReason, respContentType, respCharset, respContent, respCookie,respHeader

@csrf_exempt
def mock(request,service,tagKey,httpConfKey,url):
    if request.method == "OPTIONS":
        #处理嗅探
        reqOrigin = request.META.get("HTTP_ORIGIN")
        response = HttpResponse(status=204)
        response['Access-Control-Allow-Methods'] = "POST,GET,PUT,DELETE,HEAD,OPTIONS,PATCH"  # 支持那些请求方法，可以根据实际情况配置如 "POST, GET ,OPTIONS"
        response['Access-Control-Allow-Origin'] = reqOrigin  # 实际操作中本人无法获取请求头中的Origin参数，所以这里我实际上是配置成了 "*",但是不建议这样操作,后续会有问题,可以根据实际情况写成固定的也可以 "完整域名"
        response["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept, Connection, User-Agent, Cookie,X-CSRFToken"  # 如果配置接收的请求头有遗漏，当发送OPTIONS方法成功后，发送正式请求时将会在浏览器报错，可以根据浏览器中consolo的报错内容添加进去即可, 我这里需要配置的就是这两个
        response["Access-Control-Allow-Credentials"] = "true"  # reqOrigin  # 实际操作中本人无法获取请求头中的Origin参数，所以这里我实际上是配置成了 "*",但是不建议这样操作,后续会有问题,可以根据实际情况写成固定的也可以 "完整域名"
        return response

    #httpConfKey应该包含 test1---rec-all-header-param-body
    whetherRecHeader = False # 录制到db的时候是否录制header
    whetherRecParam = False # 录制到db的时候是否录制param
    whetherRecBody = False # 录制到db的时候是否录制body
    whetherRec = True  # 未记录的接口是否录制到db
    recEnvList = httpConfKey.split("---rec")
    if len(recEnvList) == 1:
        httpConfKey = recEnvList[0].strip()
    elif len(recEnvList) == 2:
        httpConfKey = recEnvList[0].strip()
        #分析recEnvList[1]
        if "-no" in recEnvList[1]:
            whetherRec = False

        if "-all" in recEnvList[1]:
            whetherRecHeader = True
            whetherRecParam = True
            whetherRecBody = True
        else:
            if "-header" in recEnvList[1]:
                whetherRecHeader = True
            if "-param" in recEnvList[1]:
                whetherRecParam = True
            if "-body" in recEnvList[1]:
                whetherRecBody = True

    retBl,mostPipeiMockInfo,processedReqHeader,reqUrl,reqParam,reqBody = getCorrectMockModel(request,service,tagKey,url)
    # print("###################################################")
    # print(retBl)
    # if retBl:
    #     print(mostPipeiMockInfo.mockId)
    # print(processedReqHeader)
    # print(reqUrl)
    # print(reqParam)
    # print(reqBody)
    # print("###################################################")
    if retBl == False:
        #没有匹配到mock数据，开始从环境来拿数据。
        reqHost = MockHttpService.getUri(httpConfKey,service)
        if reqHost == "":
            return HttpResponse("Cannot find mockinfo, and cannot recode request because reqHost[%s]  not found in env [%s]." % (service,httpConfKey))

        if reqBody:
            bodyType = "raw"
            bodyContent = reqBody
        else:
            bodyType = None
            bodyContent = None

        if "HOST" in processedReqHeader.keys():
            del processedReqHeader['HOST']
        tcResp = HttpProcesserV2(method = request.method.upper(),
                                 host = reqHost,
                                 url = url,
                                 headers = json.dumps(processedReqHeader),
                                 params = request.META.get("QUERY_STRING"),
                                 bodyType = bodyType,
                                 bodyContent=bodyContent).sendRequest()
        print(tcResp.request.url)
        if "requests.models.Response" in str(type(tcResp)):
            respContentText = getRespTextByResponse(tcResp)
            resp = HttpResponse(content=respContentText, status=tcResp.status_code, reason=tcResp.reason)
            # 设置cookie
            for ck, cv in tcResp.cookies.get_dict().items():
                resp.set_cookie(ck, cv)


            # 设置header
            allowdHeaderKeyList = ["content-type"]
            respHeaderDict = {}
            for ck, cv in tcResp.headers.items():
                if ck.lower() in allowdHeaderKeyList:
                    resp[ck] = cv
                    respHeaderDict[ck] = cv
            if whetherRec:
                #如果选择不记录到db，那么就不执行。
                mockInfoAuto = {}
                mockInfoAuto['title'] = "[自动录制]%s" % tcResp.url
                mockInfoAuto['businessLineId'] = 1
                mockInfoAuto['moduleId'] = 1
                mockInfoAuto['uriKey'] = service
                mockInfoAuto['tagKey'] = tagKey

                mockInfoAuto['reqMethod'] = request.method.upper()
                mockInfoAuto['reqUrl'] = url

                if whetherRecHeader:
                    mockInfoAuto['reqHeader'] = json.dumps(processedReqHeader)
                else:
                    #如果不录制header，假设contenttype是formdata,依然记录form data的值。
                    if "Content-Type" in processedReqHeader.keys():
                        #如果是formdata，就只记录content type，否则不记录
                        recContentType = processedReqHeader['Content-Type']
                        if recContentType.startswith("multipart/form-data"):
                            tmpHeader = {"Content-Type":recContentType}
                            mockInfoAuto['reqHeader'] = json.dumps(tmpHeader)

                if whetherRecParam:
                    mockInfoAuto['reqParam'] = reqParam
                if whetherRecBody:
                    mockInfoAuto['reqBody'] = reqBody

                mockInfoAuto['respStatusCode'] = tcResp.status_code
                mockInfoAuto['respStatusReason'] = tcResp.reason
                mockInfoAuto['respBody'] = respContentText
                mockInfoAuto['respHeader'] = json.dumps(respHeaderDict)
                mockInfoAuto['respCookie'] = json.dumps(tcResp.cookies.get_dict())
                MockHttpService.addHttpMockInfo(mockInfoAuto,"")
            return resp
        else:
            return HttpResponse(str(tcResp),status=509,reason="Invalid mock rec response")
    #通过人会的mockModel来获取数据并判断
    respStatusCode, respStatusReason, respContentType, respCharset, respContent, respCookie,respHeader = getRespVarsByMockModel(mostPipeiMockInfo)
    # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # print(respStatusCode, respStatusReason, respContentType, respCharset, respCookie,respHeader)
    # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # 添加invoke历史
    #处理高级模式
    respStatusCode, respStatusReason, respContentType, respCharset, respContent, respCookie,respHeader = processAdvancedMode(mostPipeiMockInfo,request,reqUrl,reqParam,reqBody,processedReqHeader,respStatusCode, respStatusReason, respContentType, respCharset, respContent, respCookie,respHeader)
    #生成response并返回
    resp = HttpResponse(content=respContent,status=respStatusCode, reason=respStatusReason,charset=respCharset,content_type=respContentType)

    ###解决跨域问题
    reqOrigin = request.META.get("HTTP_ORIGIN")
    if reqOrigin:
        resp["Access-Control-Allow-Methods"] = "POST,GET,PUT,DELETE,HEAD,OPTIONS,PATCH"  # 支持那些请求方法，可以根据实际情况配置如 "POST, GET ,OPTIONS"
        resp["Access-Control-Allow-Origin"] = reqOrigin  # 实际操作中本人无法获取请求头中的Origin参数，所以这里我实际上是配置成了 "*",但是不建议这样操作,后续会有问题,可以根据实际情况写成固定的也可以 "完整域名"
        resp["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept, Connection, User-Agent, Cookie,X-CSRFToken"  # 如果配置接收的请求头有遗漏，当发送OPTIONS方法成功后，发送正式请求时将会在浏览器报错，可以根据浏览器中consolo的报错内容添加进去即可, 我这里需要配置的就是这两个
        resp["Access-Control-Allow-Credentials"] = "true"  # reqOrigin  # 实际操作中本人无法获取请求头中的Origin参数，所以这里我实际上是配置成了 "*",但是不建议这样操作,后续会有问题,可以根据实际情况写成固定的也可以 "完整域名"

    resp['mockinfo'] = "mockId[%s]addBy[%s]addTime[%s]url[%s]" % (mostPipeiMockInfo.mockId,mostPipeiMockInfo.addBy,mostPipeiMockInfo.addTime,mostPipeiMockInfo.reqUrl)
    #设置cookie
    if respCookie != "" and isJson(respCookie):
        cookieDict = json.loads(respCookie)
        for ck,cv in cookieDict.items():
            resp.set_cookie(ck,cv)

    #设置header
    if respHeader != "" and isJson(respHeader):
        headerDict = json.loads(respHeader)
        for ck,cv in headerDict.items():
            resp[ck] = cv
    try:
        addMockInvokeHistory(request,mostPipeiMockInfo,reqUrl,reqParam,reqBody,processedReqHeader,respStatusCode,respStatusReason,respContentType,respCharset,respContent,respCookie)
    except:
        print(traceback.format_exc())
    return resp

@csrf_exempt
def readme(request):
    context = {}
    context["mockreadme"] = "current-page"
    context["pageTitle"] = "MOCK使用帮助"
    context["subPageTitle"] = "如何调用MOCK服务"
    return render(request,"mock_server/http/readme.html",context=context)