from django.shortcuts import render,HttpResponse
from urllib import parse
from apps.common.func.CommonFunc import *
import datetime,time
from urllib.parse import urlparse
from apps.common.model.RedisDBConfig import *

def test_case_plug_in(request):
    try:
        redisKey = "%s" % (round(time.time() * 1000))
        try:
            requestList = json.loads(request.POST.get("request"))
        except Exception:
            return HttpResponse(ApiReturn(code=10001,message="无法解析为json对象，请联系管理员").toJson())
        tmpTestCaseDict = {}
        tmpTestCaseDict["title"] = "[自动录制]%s_%s" % (request.session.get("loginName"),datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f"))
        tmpTestCaseDict["casedesc"] = tmpTestCaseDict["title"]
        tmpTestCaseDict["businessLineId_id"] = 1
        tmpTestCaseDict["moduleId_id"] = 1
        tmpTestCaseDict["sourceId_id"] = 1
        tmpTestCaseDict["caselevel"] = 5
        tmpTestCaseDict["stepCount"] = len(requestList)
        tmpTestCaseDict["fromInterfaceId"] = ""
        tmpTestCaseDict["isSync"] = 0
        tmpTestCaseDict["step"] = []
        for index in range(0,len(requestList)):
            tmpRequest = requestList[index]
            print(tmpRequest)
            tmpUrl = urlparse(tmpRequest["url"])
            tmpStepDict = {}
            tmpStepDict["stepNum"] = index + 1
            tmpStepDict["title"] = "[自动录制] %s" % tmpUrl.path
            tmpStepDict["stepDesc"] = "[自动录制] %s" % tmpUrl.path
            tmpStepDict["businessLineId_id"] = 1
            tmpStepDict["moduleId_id"] = 1
            tmpStepDict["sourceId_id"] = 1
            tmpStepDict["caseType"] = 2
            tmpStepDict["fromInterfaceId"] = ""
            tmpStepDict["isSync"] = 0
            tmpStepDict["varsPre"] = ""
            tmpStepDict["bodyContent"] = ""

            tmpStepDict["timeout"] = 20
            tmpStepDict["varsPost"] = ""

            try:
                tmpStepDict["uri"] = TbEnvUriConf.objects.filter(requestAddr="%s://%s" % (tmpUrl.scheme,tmpUrl.netloc))[0].uriKey
            except:
                tmpStepDict["uri"] = ""
            tmpStepDict["method"] = tmpRequest["method"].upper()

            #form-data  header为空
            # tmpStepDict["header"] = ""
            if "postData" in tmpRequest.keys():
                prePostData = tmpRequest["postData"]
                mimeType = ''
                if "mimeType" in prePostData.keys():
                    mimeType = prePostData["mimeType"]

                if mimeType.startswith("multipart/form-data"):
                    #form-data类型
                    tmpStepDict["bodyType"] = "form-data"

                    tmpBodyContent = []
                    for contentIndex in prePostData["params"]:
                        if tmpStepDict["varsPre"] == "":
                            tmpStepDict["varsPre"] = "body_%s = %s;" % (contentIndex["name"],contentIndex["value"])
                        else:
                            tmpStepDict["varsPre"] = "%s\nbody_%s = %s;" % (tmpStepDict["varsPre"],contentIndex["name"], contentIndex["value"])
                        tmpContent = {}
                        tmpContent["key"] = contentIndex["name"]
                        tmpContent["type"] = "text"
                        tmpContent["value"] = "$VAR[body_%s]" % contentIndex["name"]
                        tmpBodyContent.append(tmpContent)

                    tmpStepDict["bodyContent"] = json.dumps(tmpBodyContent)
                elif "x-www-form-urlencoded" in mimeType:
                    #www-form=urlencode
                    tmpStepDict["bodyType"] = "x-www-form-urlencoded"

                    if len(tmpRequest["headers"]) > 0:
                        try:
                            tmpStepDict["header"] = json.dumps(tmpRequest["headers"][0])
                        except:
                            pass
                    else:
                        tmpStepDict["header"] = "{}"

                    for tmpPreIndex in prePostData['params']:
                        if tmpStepDict["varsPre"] == "":
                            tmpStepDict["varsPre"] = "body_%s = %s;" % (tmpPreIndex["name"], tmpPreIndex["value"])
                        else:
                            tmpStepDict["varsPre"] = "%s\nbody_%s = %s;" % (tmpStepDict["varsPre"], tmpPreIndex["name"], tmpPreIndex["value"])

                        if tmpStepDict["bodyContent"] == "":
                            tmpStepDict["bodyContent"] = "%s=$VAR[body_%s]" % (tmpPreIndex["name"],tmpPreIndex["name"])
                        else:
                            tmpStepDict["bodyContent"] = "%s&%s=$VAR[body_%s]" % (tmpStepDict["bodyContent"],tmpPreIndex["name"], tmpPreIndex["name"])
                else:
                    #raw
                    tmpStepDict["bodyType"] = "raw"

                    if len(tmpRequest["headers"]) > 0:
                        try:
                            tmpStepDict["header"] = json.dumps(tmpRequest["headers"][0])
                        except:
                            pass
                    else:
                        tmpStepDict["header"] = "{}"

                    tmpStepDict["bodyContent"] = prePostData["text"]

            else:
                tmpStepDict["bodyType"] = ""


            tmpStepDict["url"] = tmpUrl.path
            tmpQueryString = ""
            for quertyIndex in tmpRequest["queryString"]:
                if tmpStepDict["varsPre"] == "":
                    tmpStepDict["varsPre"] = "query_%s = %s;" % (quertyIndex["name"], quertyIndex["value"])
                else:
                    tmpStepDict["varsPre"] = "%s\nquery_%s = %s;" % (
                        tmpStepDict["varsPre"], quertyIndex["name"], quertyIndex["value"])
                if tmpQueryString == "":
                    tmpQueryString = "%s=$VAR[query_%s]" % (quertyIndex["name"],quertyIndex["name"])
                else:
                    tmpQueryString = "%s&%s=$VAR[query_%s]" % (tmpQueryString,quertyIndex["name"],quertyIndex["name"])
            tmpStepDict["params"] = tmpQueryString

            if "response" in tmpRequest.keys():
                tmpStepDict["varsPost"] = "ASSERT(%s)" % tmpRequest['response']

            tmpStepDict["performanceTime"] = 1

            tmpTestCaseDict["step"].append(tmpStepDict)

        RedisCache().set_data("%s_testCase_%s" % (request.session.get("loginName"),redisKey),json.dumps(tmpTestCaseDict),60*60)
        # print(json.dumps(tmpTestCaseDict))
    except Exception:
        logger.error(traceback.format_exc())
    return HttpResponse(ApiReturn(body=redisKey).toJson())


def getRedisTestCase(request):
    try:
        redisKey = request.GET.get("dataKey")
        testCaseData = RedisCache().get_data("%s_testCase_%s" % (request.session.get("loginName"),redisKey))
        RedisCache().del_data("%s_testCase_%s" % (request.session.get("loginName"),redisKey))
    except Exception:
        logger.error(traceback.format_exc())
        return HttpResponse(ApiReturn(code=10001,message="%s 不存在" % redisKey).toJson())


    return HttpResponse(ApiReturn(body=testCaseData).toJson())
