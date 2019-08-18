import requests  # python处理http相关的类库
import urllib,os,socket
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from core.tools.TypeTool import TypeTool
from core.tools.CommonFunc import *
from core.config.InitConfig import TcpServerConf,rootDir,ServiceConf,RunTcpServerConf
from copy import deepcopy
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class HttpProcesserV2(object):
    """
    Http处理器，
    根据host url params构建类对象并校验对象合法性，并且提供GET POST请求。处理并校验host、url、params
    """
    def __init__(self,method = "POST",host = "",url = "/",headers = None,params = None,bodyType = None,bodyContent=None,sess = requests.session(),timeout = 20,allow_redirects = True):
        self.supportMethodList = ["get", "post", "options", "head", "put", "patch", "delete"]
        self.bodyTypeList = ["form-data","x-www-form-urlencoded","raw","binary","none"]
        self.formdataTypeList = ["text", "file"]
        self.rawTypeList = ["text","text/plain","text/xml","text/html","application/json","application/javascript","application/xml"]

        #请求信息
        self.method = method
        self.host = host
        self.url = url
        self.headers = headers
        self.params = params
        self.bodyType = bodyType

        self.bodyContent = bodyContent
        #上下文控制信息
        self.sess = sess
        self.timeout = timeout
        self.allow_redirects = allow_redirects

    @property
    def host(self):
        return self.__host.strip()

    @host.setter
    def host(self,host):
        self.__host = host.strip().lower()
        #host应校验末尾是数字或字母，并且开头是http://,否则host格式不合法，创建对象失败,验证host。如果host 斜杠结束那么去掉斜杠
        while True:
            if self.__host[-1:] == "/":
                self.__host = self.__host[0:-1]
            else:
                break

        if ((self.__host[-1:].isalpha() or self.__host[-1:].isdigit()) and (self.__host[0:7]=="http://" or self.__host[0:8]=="https://") ):
            pass
        else:
            raise ValueError(u"EXCEPTION: 参数host格式不正确，请检查。 host: %s" % self.__host)

    @property
    def url(self):
        return self.__url.strip()

    @url.setter
    def url(self,url):
        if url == None:
            self.__url = ""
            return
        #url应校验是/开头
        self.__url = url.strip()
        #url应校验是/开头
        if self.__url=="" or self.__url[0:1]=="/" :
            pass
        else:
            raise ValueError(u"EXCEPTION: 参数url格式不正确，请检查。 url: %s" % self.__url)

    @property
    def params(self):
        return self.__params

    @params.setter
    def params(self,params):
        if params == None:
            self.__params = ""
        else:
            self.__params = params.strip().replace(" ","%20")

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self,headers):
        self.__headers = {}
        if headers == None  or headers.strip() == "":
            self.__headers['User-Agent'] = ServiceConf.framework_version
            return
        try:
            if isDictJson(headers):
                header_dict = json.loads(headers)
                if "User-Agent" not in header_dict.keys():
                    header_dict['User-Agent'] = ServiceConf.framework_version
            else:
                try:
                    header_dict = eval(headers)
                    if TypeTool.is_dict(header_dict) == False:
                        raise ValueError(u"EXCEPTION: 参数headers类型不正确,应为合法JSON字符串，实际是：\n%s。" % headers)
                except Exception as e:
                    raise ValueError(u"EXCEPTION: 参数headers类型不正确,应为合法JSON字符串，实际是：\n%s。" % headers)
        except Exception as e:
            raise ValueError(u"EXCEPTION: 处理头信息发生异常：请检查,应该为合法JSON字符串，实际是：\n%s。" % str(headers))
        if TypeTool.is_dict(header_dict):
            self.__headers = {}
            for k,v in header_dict.items():
                if isContainCN(k):
                    k = urllib.parse.quote(k,encoding="utf-8")
                if isContainCN(v):
                    v= urllib.parse.quote(v,encoding="utf-8").replace("%3D","=")
                self.__headers[k] = v
        else:
            raise ValueError(u"EXCEPTION: 参数headers转换后类型不正确，请检查,应该为dict类型。实际是%s。" % type(header_dict))

    @property
    def sess(self):
        return self.__sess

    @sess.setter
    def sess(self,sess):
        if TypeTool.is_requests_session(sess):
            self.__sess = sess
        else:
            raise ValueError(u"EXCEPTION: 参数sess类型不正确，请检查,应该为requests.session()类型。")

    @property
    def timeout(self):
        return self.__timeout

    @timeout.setter
    def timeout(self,timeout):
        try:
            if int(timeout) >= 0:
                self.__timeout = int(timeout)
            else:
                raise ValueError(u"EXCEPTION: 参数timeout类型不正确，请检查,应该为大于等于0的整数类型。")
        except Exception as e:
            raise ValueError(u"EXCEPTION: 参数timeout类型不正确，请检查,应该为大于等于0的整数类型。")

    @property
    def method(self):
        return self.__method

    @method.setter
    def method(self,method):
        lowerMethod = method.lower()
        if lowerMethod in self.supportMethodList:
            self.__method = lowerMethod
        else:
            raise ValueError(u"EXCEPTION: 参数method[%s]类型不支持。" % method)

    @property
    def bodyType(self):
        return self.__bodyType

    @bodyType.setter
    def bodyType(self, bodyType):
        if self.method == self.supportMethodList[0] or self.method == self.supportMethodList[3]:
            #get head方法没有请求体
            self.__bodyType = None
            return

        if bodyType in self.bodyTypeList:
            self.__bodyType = bodyType
        else:
            raise ValueError(u"EXCEPTION: 目前支持请求体类型%s" % self.bodyTypeList)

    @property
    def bodyContent(self):
        return self.__bodyContent

    @bodyContent.setter
    def bodyContent(self, bodyContent):
        if self.method == self.supportMethodList[0] or self.method == self.supportMethodList[3] or bodyContent == None :
            #get head请求的时候没有body体
            self.__bodyContent = None
            return

        if self.bodyType == self.bodyTypeList[0]:
            #form-data
            self.__bodyContent = [] #如果是fordmdata就是设置一个list
            #去掉content-type相关的错误的header，formdata需要自己生成header
            if TypeTool.is_dict(self.headers) == False:
                raise ValueError(u"EXCEPTION: headers类型错误！应为字典，实际是[%s]。" %(type(self.headers)))

            headerKeysList = deepcopy(list(self.headers.keys()))
            for k in headerKeysList:
                if k.lower() == "content-type":
                    self.headers.pop(k)
            # logging.debug("bodyContent:%s"% bodyContent)
            if bodyContent == "" or bodyContent == None:
                return
            if TypeTool.is_str(bodyContent) == False:
                raise ValueError(u"EXCEPTION: 参数bodyType为%s时，bodyContent必须是字符串。" % (self.bodyType))

            if isListJson(bodyContent) == False:
                raise ValueError(u"EXCEPTION: 参数bodyType为%s时，bodyContent必须是合法的json列表字符串。" % (self.bodyType))

            bodyContentList = json.loads(bodyContent)

            #遍历formdata数据列表
            for tmpFormAttrDict in bodyContentList:
                if TypeTool.is_dict(tmpFormAttrDict) == False:
                    #元素必须是字典
                    raise ValueError(u"EXCEPTION: 参数bodyType为%s时，列表中的每个元素必须是字典。" % (self.bodyType))

                if "key" not in tmpFormAttrDict.keys() or "type" not in tmpFormAttrDict.keys() or "value" not in tmpFormAttrDict.keys():
                    #必须包含必要的key
                    raise ValueError(u"EXCEPTION: 参数bodyType为%s时，元素缺少必要字段，必须包含key，type，value这些字段。" % (self.bodyType))

                tmpKey = tmpFormAttrDict['key']
                tmpType = tmpFormAttrDict['type']
                tmpValue = tmpFormAttrDict['value']
                if isContainCN(tmpKey):
                    tmpKey = urllib.parse.quote(tmpKey,encoding="utf-8") #key urlencode中文，key不能有中文字符。


                if tmpType == self.formdataTypeList[0]:
                    # text
                    try:
                        if TypeTool.is_dict(tmpValue):
                            # 如果是字段dump成字符串
                            tmpValue = json.dumps(tmpValue,ensure_ascii=False)
                        # tmpValue = tmpValue
                        # tmpValue = urllib.parse.quote(tmpValue,encoding="utf-8")  #urlencode中文不适用quote，
                        # 20180122 HTTP_INTERFACE_2001上进行测试，测试结果：文本类型不适用quote，不会出现错误，可以正常测试。
                        # 问题是如果这里不用quote，接触出来的请求头中的文件名等中文的话就是编码而不是文字显示。
                        self.__bodyContent.append((tmpKey, (None, tmpValue, "text/plain; charset=UTF-8")))  # 判断是否是utf8
                    except Exception as e:
                        raise ValueError(u"EXCEPTION: 参数bodyType为%s时，类型为text时，value无法转换为utf8。" % self.bodyType)

                elif tmpType == self.formdataTypeList[1]:
                    # file
                    if TypeTool.is_dict(tmpValue) :
                        #必须是字典，包含对应的值
                        if "filename" not in tmpValue.keys() or "realPath" not in tmpValue.keys()  or "fileType" not in tmpValue.keys() :
                            raise ValueError(u"EXCEPTION: 参数bodyType为%s时，元素的value缺少必要字段。" % (self.bodyType))
                        if RunTcpServerConf.ip != TcpServerConf.ip:
                            filePath = "%s/%s" % (LogConfig.uploadsRoot,tmpValue['realPath'].split("/uploads/")[-1])
                            dirPath = "/".join(filePath.split("/")[:-1])
                            if not getFTPFile(TcpServerConf.ip,"getUploadFile","getUploadFile",dirPath,filePath,tmpValue['realPath'].split("/uploads/")[-1]):
                                raise ValueError(u"EXCEPTION: 执行机非主服务器时，文件获取失败")
                            tmpValue['realPath'] = filePath
                        if os.path.isfile(tmpValue['realPath']):
                            #如果存在文件，加入file #如果不quote直接用中文是否报错？
                            #20180122 HTTP_INTERFACE_2001上进行测试，测试结果：文件类型如果不使用quote，在上传中文文件的时候，就返回错                 误。所以必须使用quote
                            if isContainCN(tmpValue['filename']):
                                fileName = urllib.parse.quote(tmpValue['filename'],encoding="utf-8")
                            else:
                                fileName = tmpValue['filename']

                            # fileName = tmpValue['filename']
                            self.__bodyContent.append((tmpKey, (fileName, open(tmpValue['realPath'], "rb"), tmpValue['fileType'])))
                        else:
                            #文件不存在抛出异常
                            raise ValueError(u"EXCEPTION: 参数bodyType为%s时，服务器端未找到对应的文件，请重新上传或者联系管理员。" % (self.bodyType))
                    else:
                        #不是字典
                        raise ValueError(u"EXCEPTION: 参数bodyType为%s时，元素的value必须是字典。" % (self.bodyType))
                else:
                    #类型错误抛出异常
                    raise ValueError(u"EXCEPTION: 参数bodyType为%s时，content只支持%s，不支持当前类型%s。" % (self.bodyType,self.formdataTypeList,tmpType))

        elif self.bodyType == self.bodyTypeList[1] or self.bodyType == self.bodyTypeList[2]:
            # x-www-form-urlencoded
            # raw
            try:
                if TypeTool.is_str(bodyContent):
                    #如果是字符串，转换成utf8字节码
                    if self.bodyType == self.bodyTypeList[1]:
                        # x-www-form-urlencoded  如果是urlencode的，要进行urlencode
                        # self.__bodyContent = urllib.parse.quote(bodyContent).encode('utf8')  # 转到utf8
                        bodyvaluelist = bodyContent.split("&")
                        processedBodyContent = ""
                        for totalvalueindex in range(0,len(bodyvaluelist)):
                            subkvlist = bodyvaluelist[totalvalueindex].split("=")
                            subk = subkvlist[0]
                            subv = ""
                            whetherHasEqual = False
                            for subvindex in range(1,len(subkvlist)):
                                whetherHasEqual = True
                                if subvindex != len(subkvlist)-1:
                                    subv += "%s=" % subkvlist[subvindex]
                                else:
                                    subv += "%s" % subkvlist[subvindex]

                            if whetherHasEqual:
                                processedtotalvalue = "%s=%s" % (urllib.parse.quote(subk),urllib.parse.quote(subv))
                            else:
                                processedtotalvalue = urllib.parse.quote(subk)

                            if totalvalueindex != len(bodyvaluelist) -1:
                                processedBodyContent += "%s&" % processedtotalvalue
                            else:
                                processedBodyContent += "%s" % processedtotalvalue

                        self.__bodyContent = processedBodyContent.encode('utf8')  # 转到utf8
                    else:
                        # raw
                        self.__bodyContent = bodyContent.encode('utf8') #转到utf8
                elif TypeTool.is_bytes(bodyContent):
                    #如果是字节码，直接赋值
                    self.__bodyContent = bodyContent
                else:
                    raise ValueError(u"EXCEPTION: bodyContent必须是UTF-8字符集的字符串或有效的字节码。" % (bodyContent))

            except Exception as e:
                raise ValueError(u"EXCEPTION: 参数bodyType为%s时，内容content格式错误。" % self.bodyType)

        elif self.bodyType == self.bodyTypeList[3]:
            #binary
            try:
                if TypeTool.is_bytes(bodyContent):
                    #如果是字节码，直接赋值
                    self.__bodyContent = bodyContent
                elif TypeTool.is_str(bodyContent) and isDictJson(bodyContent):
                    bodyContentDict = json.loads(bodyContent)
                    if ("realPath" in bodyContentDict.keys()) and TypeTool.is_str(bodyContentDict['realPath']):
                        #binary方式字符串正确
                        if os.path.isfile(bodyContentDict['realPath']):
                            #服务器端存在文件
                            self.__bodyContent = open(bodyContentDict['realPath'], "rb")
                        else:
                            #服务器端不存在文件
                            raise ValueError(u"EXCEPTION: 参数bodyType为%s时，内容content文件realPath路径错误，不存在此文件。" % self.bodyType)
                    else:
                        #binary方式json字符串格式错误
                        raise ValueError(u"EXCEPTION: 参数bodyType为%s时，内容content格式错误。" % self.bodyType)
                else:
                    #不正确的bodycontent格式，必须是字节码或者有效的json字符串。
                    raise ValueError(u"EXCEPTION: 参数bodyType为%s时，内容必须是json或者字节码。" % self.bodyType)

            except Exception as e:
                #未知异常
                logging.error("EXCEPTION: 参数bodys的type为%s时，内容content出现未知异常如下：\r\n%s" % (self.bodyType,traceback.format_exc()))
                raise ValueError("EXCEPTION: 参数bodys的type为%s时，内容content出现未知异常如下：\r\n%s" % (self.bodyType,e))
        elif self.bodyType == self.bodyTypeList[4]:
            self.__bodyContent = None


    def sendRequest(self):
        # print("#############请求类型：%s" % self.method)
        if self.method in self.supportMethodList :
            #发送请求post get
            #还有 options head put  patch delete
            logging.debug(u"发送%s请求%s" % (self.method.upper(),self.url))
            logging.debug(u"Host是%s" % self.host)
            logging.debug(u"头信息是%s" % self.headers)
            logging.debug(u"参数是%s" % self.params)
            logging.debug(u"请求类型是%s" % self.bodyType)
            logging.debug(u"请求体是%s" % self.bodyContent)
            logging.debug(u"超时时间是%s" % self.timeout)
            #self.headers['Host'] = self.host.lower().replace("http://","").replace("https://","").split("/")[0]
            try:
                paramStr = ""
                if self.params != "":
                    paramStr = "?%s" % self.params
                if self.bodyType == self.bodyTypeList[0]:
                    #form-data
                    return self.sess.request(method = self.method, url =self.host + self.url+paramStr, headers=self.headers, files=self.bodyContent,timeout=self.timeout, verify=False, allow_redirects = self.allow_redirects)
                elif self.bodyType in self.bodyTypeList or self.bodyType == None:
                    # x-www-form-urlencode  ==raw json text xml  ==binary
                    return self.sess.request(method = self.method, url =self.host + self.url+paramStr, headers=self.headers, data= self.bodyContent,timeout=self.timeout, verify=False, allow_redirects = self.allow_redirects)
                else:
                    return ValueError(u"EXCEPTION: 不支持的bodyType类型[%s],目前仅支持%s." % (self.bodys['type'], self.bodyTypeList))
            except requests.exceptions.ConnectTimeout as timeoutE:
                logging.debug("请求连接超时[ConnectTimeout]：%s" % traceback.format_exc())
                return "TIMEOUT"
            except requests.exceptions.ReadTimeout as timeoutE2:
                logging.debug("请求超时[ReadTimeout]：%s" % traceback.format_exc())
                return "TIMEOUT"
            except Exception as e:
                logging.debug(type(e))
                return ValueError("EXCEPTION: 请求时发生异常：%s" % e)
            except socket.gaierror as e:
                logging.debug(type(e))
                return ValueError("EXCEPTION: 找不到服务：%s" % e)

        else:
            return ValueError("EXCEPTION: 目前支持请求%s" % self.supportMethodList)
