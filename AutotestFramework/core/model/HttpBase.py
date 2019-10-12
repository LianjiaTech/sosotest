import urllib,requests
from copy import deepcopy
from core.model.CommonAttr import CommonAttr
from core.processor.HttpProcesserV2 import HttpProcesserV2
from core.processor.KP import KP
from core.tools.CommonFunc import *

from core.const.GlobalConst import DBConst
from core.const.GlobalConst import ExecStatus
from core.const.GlobalConst import MethodConst
from core.decorator.normal_functions import *
from core.keywords import DBKeyword
from core.model.ConfHttpLayer import ConfHttpLayer
from core.processor.Assert import Assert
from core.processor.CP import CP
from core.processor.BP import BP
from core.tools.DBTool import DBTool
from core.tools.TypeTool import TypeTool

from core.keywords import *

class HttpBase(CommonAttr):
    """
    Http基础处理类，接口/步骤都继承此类，包含HTTP请求的所有通用属性。
    """
    def __init__(self):
        super(HttpBase, self).__init__()
        # 设置协议
        self.protocol = "HTTP"
        #HTTP执行信息
        self.varsPre = "" #前置变量

        self.uri = ""
        self.url = "" #接口 interface
        self.method = "GET"
        self.header = "{}"
        self.params = "" #key1=value1&key2=value2
        self.bodyType = "" # raw x-www-url-encode form-date etc.
        self.bodyContent = "" # body的内容

        self.httprequestTimeout = 20
        self.varsPost = "" #后置变量
        #执行
        self.execStatus = ExecStatus.NOTRUN
        #结果展示使用的
        self.varsPreFinalStr = ""

        self.urlRedirectStatus = True #重定向
        self.urlRedirect = 1 #重定向
        self.useCustomUri = 0  #是否使用自定义请求地址  0 否 1 是
        self.customUri = ""
        self.uriFinalStr = ""
        self.urlFinalStr = ""
        self.paramsFinalStr = ""
        self.headerFinalStr = ""
        self.bodyContentFinalStr = ""

        self.varsPostFinalStr = ""

        self.actualResult = "" #实际结果 #TODO json {"status_code":200,headers:{},"content":""}
        self.assertResult = "" #断言结果
        self.testResult = ResultConst.NOTRUN #测试结果

        self.beforeExecuteTakeTime = 0.0
        self.afterExecuteTakeTime = 0.0
        self.executeTakeTime = 0.0
        self.totalTakeTime = 0.0

        #通用信息
        self.state = 1
        self.addBy = ""
        self.modBy = ""
        self.addTime = ""
        self.modTime = ""


        #全局使用的，上下文关联的
        self.host = ""
        self.serviceDB = DBTool()

        self.response = requests.models.Response()  # 最近HTTP请求返回的response对象，提供给各个方法使用
        self.interface_response = requests.models.Response()  # 要测试的接口返回的response，供断言使用。
        self.calledInterfaceRecurDict = {} #存放循环的dict。

        self.headerDict = {}  # TODO 实际的request的header信息：预期将此结果写入headerDict 请求的头信息

        #Task/Testcase/Step/Interface/HttpBase全局传递变量
        self.varsPool = {} #变量dict 变量池，累加，从外部集成，包括varsPre的和varsPost的
        self.varsKeyList = [] #变量列表，保存变量前后顺序。
        self.isRequested = False
        self.exitExecStatusList = [ResultConst.FAIL,ResultConst.EXCEPTION,ResultConst.ERROR]

    @catch_exception
    def execute(self):
        """
        执行函数，包括整个接口/步骤的执行过程。
        Returns:
            无。
        """
        logging.info("#########################HTTP_BASE执行开始[%s]interfaceId[%s]traceId[%s]#########################" % (self.addBy, self.interfaceId,self.traceId))
        try:
            logging.info("★1===traceId[%s]★★★★★" % self.traceId)
            if self.processBeforeExecute() == False:
                return
            logging.info("★★2===traceId[%s]★★★★★" % self.traceId)
            #DONE 5、处理 url method header parmas中的变量替换、关键字处理
            self.processExecuteAttrAndRun(True)
            logging.info("★★★3===traceId[%s]★★★★★" % self.traceId)
            if self.testResult in self.exitExecStatusList :
                self.assertResult = "执行HTTP请求时出现错误或者异常：\n%s" % self.assertResult
                return
            logging.info("★★★★4===traceId[%s]★★★★★" % self.traceId)
            if self.processAfterExecute() == False:
                return
            logging.info("★★★★★5===traceId[%s]★★★★★" % self.traceId)

        except Exception as e:
            logging.error(traceback.format_exc())
        finally:
            self.releaseDB() #释放数据库连接，防止mysql连接过多错误
            logging.debug("测试结果： %s" % self.testResult)
            logging.debug("单接口或步骤执行时间： %f" % self.totalTakeTime)
            logging.info("#########################HTTP_BASE执行结束[%s]interfaceId[%s]traceId[%s]#########################"  % (self.addBy, self.interfaceId, self.traceId))

    def initRequestHostAndResults(self):
        """
        执行前初始化的一些基本信息
        Returns:
            无。
        """
        super(HttpBase, self).initRequestHostAndResults()
        try:
            if self.uri.lower().strip().startswith("http://") or self.uri.lower().strip().startswith("https://"):
                self.host = self.uri.lower().strip()
                return
            self.host = self.getRequestAddr(self.uri)
            if self.host == "":
                self.setERROR("环境[%s]没有配置服务[%s]的请求地址，请前往%s/interfaceTest/HTTP_EnvUriConf进行配置。" % (self.confHttpLayer.key,self.uri,EnvConfig.WEB_URI))
            elif not (self.host.strip().lower().startswith("http://") or self.host.strip().lower().startswith("https://")):
                self.setERROR("环境[%s]配置服务[%s]的请求地址[%s]配置错误，必须是http://或者https://开头，请前往%s/interfaceTest/HTTP_EnvUriConf进行修改。" % (self.confHttpLayer.key,self.uri,self.host,EnvConfig.WEB_URI))
        except Exception as e:
            self.host = self.uri
            self.setERROR("当前环境下没有配置服务[%s]的请求地址，请前往%s/interfaceTest/HTTP_EnvUriConf进行配置。" % (self.uri,EnvConfig.WEB_URI))

    def checkAllInfosAfterTest(self):
        super(HttpBase, self).checkAllInfosAfterTest()
        self.params = (self.params == None or self.params.strip() == "" ) and "未设置参数" or self.params
        self.header = (self.header == None or self.header.strip() == "" or self.header.strip() == "{}") and "未设置头信息" or self.header

    @take_time
    @catch_exception
    def validate(self):
        """
        对属性的一些验证，如果不如何条件那么将ERROR，不继续执行。
        Returns:
            处理结果False/True。
        """
        super(HttpBase, self).validate()
        if len(self.url) == 0 :
            msg = "必须有接口url。"
            self.setERROR(msg)
            return False
        if len(self.method) == 0 :
            msg = "必须有请求方法method。"
            self.setERROR(msg)
            return False

        return True


    @catch_exception
    def sendHttpRequest(self,whetherSetResult = True):
        """
        发送http请求
        Returns:
            发送请求结果 False/True
        """
        try:
            httpProcesser = HttpProcesserV2(method=self.method, host = self.host, url = self.url, headers = self.header, params = self.params,bodyType = self.bodyType, bodyContent = self.bodyContent,  sess=self.current_session, timeout = int(self.httprequestTimeout),allow_redirects=self.urlRedirectStatus)
            requestStartTime = time.time()
            self.interface_response = httpProcesser.sendRequest()
            requestEndTime = time.time()
            self.executeTakeTime = int((requestEndTime - requestStartTime) * 1000)

            if TypeTool.is_requests_Response(self.interface_response):
                self.response = self.interface_response
                self.method = self.response.request.method
                respReqUrl = self.response.request.url
                headerHost = respReqUrl.replace("http://","").replace("https://","").split("/")[0]
                realFinalUrlList = respReqUrl.split("?")

                if len(realFinalUrlList) >= 1:
                    self.urlFinalStr = realFinalUrlList[0]

                if len(realFinalUrlList) >= 2:
                    finPStr = ""
                    for pStrIndex in range(1,len(realFinalUrlList)):
                        if pStrIndex == len(realFinalUrlList) - 1:
                            finPStr += realFinalUrlList[pStrIndex]
                        else:
                            finPStr += realFinalUrlList[pStrIndex]+"?"
                    self.paramsFinalStr = finPStr

                self.headerDict = {}
                self.headerDict['Host'] = headerHost
                self.headerDict.update(self.response.request.headers)
                self.header = json.dumps(dict(self.headerDict))
                self.headerFinalStr = json.dumps(dict(self.headerDict))

                #开始处理实际request的请求体
                if self.response.request.body == None:
                    self.bodyContentFinalStr = ""
                else:
                    #处理最新的request
                    request = self.response.request
                    theEncoding = "utf8"
                    try:
                        reqBody = urllib.parse.unquote(bytes.decode(request.body, encoding=theEncoding))
                    except:
                        # 转码失败的话， reqBody就设置为空
                        processedReqHeader = request.headers
                        if "Content-Type" in processedReqHeader.keys() and processedReqHeader['Content-Type'].startswith("multipart/form-data"):
                            # s = a.encode("raw_unicode_escape")  变成bytes，并且带着中文的编码
                            # formdata 类型
                            boundary = processedReqHeader['Content-Type'].split("boundary=")[1]
                            splitBoundary = ("--%s" % boundary).encode(theEncoding)
                            startStr0 = 'filename="'.encode(theEncoding)
                            startStr = "Content-Type: application".encode(theEncoding)
                            splitBList = request.body.split(splitBoundary)
                            reqBodyBytes = splitBoundary
                            for bindex in range(1, len(splitBList) - 1):
                                if startStr0 in splitBList[bindex]:
                                    # 是文件类型 舍弃后面的二进制
                                    reqBodyBytes = reqBodyBytes + splitBList[bindex].split(startStr)[0] + b'\r\n\r\nIgnore the real bytes when request is file...\r\n' + splitBoundary
                                else:
                                    # 不是文件类型，直接拼接
                                    reqBodyBytes = reqBodyBytes + splitBList[bindex] + splitBoundary
                            reqBodyBytes += splitBList[-1]
                            try:
                                reqBody = urllib.parse.unquote(reqBodyBytes.decode(theEncoding))
                            except:
                                # 如果转码失败，那么就是处理后没有文件的也失败了，进行截取操作
                                tobeProcessedBody = str(reqBodyBytes)
                                reqBody = tobeProcessedBody[2:-1] if len(tobeProcessedBody) < 1000 else tobeProcessedBody[2:999] + "\r\n(请求体超长，后续省略...)"  # 去掉开头的b' 和 结尾的 ' 最多拿1000个字符。
                        else:
                            # 入股不是formdata，那么就直接byte转换看效果
                            tobeProcessedBody = str(request.body)
                            reqBody = tobeProcessedBody[2:-1] if len(tobeProcessedBody) < 1000 else tobeProcessedBody[2:999] + "\r\n(请求体超长，后续省略...)"  # 去掉开头的b' 和 结尾的 ' 最多拿1000个字符。
                    finally:
                        self.bodyContentFinalStr = reqBody

                respDict = {}
                respDict['status_code'] = int(getRespCodeByResponse( self.response))
                respDict['reason'] = getRespReasonByResponse( self.response)
                respDict['headers'] = getRespHeaderDictByResponse(self.response)
                respDict['content'] = getRespTextByResponse(self.response)
                self.actualResult = json.dumps(dict(respDict))
            elif TypeTool.is_str(self.interface_response):
                self.headerDict = {}
                self.headerDict['Host'] = self.host.split("://")[1]
                if isDictJson(self.header):
                    self.headerDict.update(json.loads(self.header))
                self.header = json.dumps(dict(self.headerDict))
                self.headerFinalStr = json.dumps(dict(self.headerDict))

                self.bodyContentFinalStr = self.bodyContent
                if self.interface_response == "TIMEOUT":
                    if whetherSetResult:
                        self.setFAIL("HTTP请求超时，超时时间[%s秒]内没有响应。" % self.httprequestTimeout)
                    else:
                        self.actualResult = "HTTP请求超时，超时时间[%s秒]内没有响应。" % self.httprequestTimeout
                else:
                    if whetherSetResult:
                        self.setERROR("HTTP请求异常，没有正常返回。返回内容是：%s" % self.interface_response)
                    else:
                        self.actualResult = "HTTP请求异常，没有正常返回。返回内容是：%s" % self.interface_response
            elif TypeTool.is_ValueError(self.interface_response):
                self.headerDict = {}
                self.headerDict['Host'] = self.host.split("://")[1]
                if isDictJson(self.header):
                    self.headerDict.update(json.loads(self.header))
                self.header = json.dumps(dict(self.headerDict))
                self.headerFinalStr = json.dumps(dict(self.headerDict))

                self.bodyContentFinalStr = self.bodyContent
                if whetherSetResult:
                    self.setERROR(str(self.interface_response))
                else:
                    self.actualResult = str(self.interface_response)
            else:
                if whetherSetResult:
                    self.setERROR("HTTP请求异常，没有返回预期类型和数据，返回的类型是[%s]。" % type(self.interface_response) )
                else:
                    self.actualResult = "HTTP请求异常，没有返回预期类型和数据，返回的类型是[%s]。" % type(self.interface_response)
        except Exception as e:
            self.headerDict = {}
            tmpHostList = self.host.split("://")
            if len(tmpHostList) == 2:
                self.headerDict['Host'] = tmpHostList[1]
            else:
                self.headerDict['Host'] = "<ERROR: 错误的请求主机：%s>" % str(self.host)

            if isDictJson(self.header):
                self.headerDict.update(json.loads(self.header))
            self.header = json.dumps(dict(self.headerDict))
            self.headerFinalStr = json.dumps(dict(self.headerDict))

            self.bodyContentFinalStr = self.bodyContent
            if whetherSetResult:
                self.setERROR("%s: HTTP请求异常[%s]" % (ResultConst.ERROR, e))
            else:
                self.actualResult =  "%s: HTTP请求异常[%s]" % (ResultConst.ERROR, e)
        finally:
            self.isRequested = True

    @catch_exception
    def processExecuteAttrAndRun(self,whetherSetResult = True):
        super(HttpBase, self).processExecuteAttrAndRun()
        # DONE 5、处理 url method header parmas中的变量替换、关键字处理
        logging.debug("EXECUTE_HTTP_STEP_4: 处理uri/url/method/header/parmas中的变量替换、关键字处理。")

        baseUrl = self.url
        self.url = self.processKPWithNoneTag(self.url)
        self.processedUrl = self.url
        if self.testResult in self.exitExecStatusList:
            self.assertResult = "处理请求信息中的URL中的变量替换、关键字处理时出现错误：\n%s" % self.assertResult
            return

        baseMethod = self.method
        self.method = self.processKPWithNoneTag(self.method)
        self.processedMethod = self.method
        if self.testResult in self.exitExecStatusList:
            self.assertResult = "处理请求信息中的METHOD中的变量替换、关键字处理时出现错误：\n%s" % self.assertResult
            return

        baseHeader = self.header
        self.header = self.processKPWithNoneTag(self.header)
        self.processedHeader = self.header
        if self.testResult in self.exitExecStatusList:
            self.assertResult = "处理请求信息中的HEADER中的变量替换、关键字处理时出现错误：\n%s" % self.assertResult
            return

        baseParams = self.params
        self.params = self.processKPWithNoneTag(self.params)
        self.processedParams = self.params
        if self.testResult in self.exitExecStatusList:
            self.assertResult = "处理请求信息中的PARAMS中的变量替换、关键字处理时出现错误：\n%s" % self.assertResult
            return

        baseBodyContent = self.bodyContent
        if self.bodyType == "form-data":
            if isJson(self.bodyContent):
                tmpBodyContentDictList = json.loads(self.bodyContent)
                for tmpBodyContentDict in tmpBodyContentDictList:
                    for tmpBodyKey,tmpBodyValue in tmpBodyContentDict.items():
                        if isinstance(tmpBodyValue,str):
                            tmpBodyContentDict[tmpBodyKey] = self.processKPWithNoneTag(tmpBodyValue)
                        else:
                            tmpBodyContentDict[tmpBodyKey] = tmpBodyValue
                self.bodyContent = json.dumps(tmpBodyContentDictList)
        else:
            self.bodyContent = self.processKPWithNoneTag(self.bodyContent)
        self.processedBodyContent = self.bodyContent
        if self.testResult in self.exitExecStatusList:
            self.assertResult = "处理请求信息中的BODY中的变量替换、关键字处理时出现错误：\n%s" % self.assertResult
            return

        # DONE 6、执行http请求
        logging.debug("EXECUTE_HTTP_STEP_5: 执行HTTP请求。")
        self.sendHttpRequest(whetherSetResult)
        if whetherSetResult:
            pass
        else:
            #还原
            self.url = baseUrl
            self.method = baseMethod
            self.header = baseHeader
            self.params = baseParams
            self.bodyContent = baseBodyContent
