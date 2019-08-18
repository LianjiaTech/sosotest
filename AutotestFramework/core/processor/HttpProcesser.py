import json
import logging
import traceback

import requests  # python处理http相关的类库
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from core.tools.CommonFunc import *
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from core.tools.TypeTool import TypeTool

class HttpProcesser(object):
    """
    Http处理器，
    根据host url params构建类对象并校验对象合法性，并且提供GET POST请求。处理并校验host、url、params
    """
    def __init__(self,host = "",url = "/",header = "{}",params = "",sess = requests.session(),timeout = 20):
        self.sess = sess
        self.timeout = timeout
        #host应校验末尾是数字或字母，并且开头是http://,否则host格式不合法，创建对象失败,验证host。如果host 斜杠结束那么去掉斜杠
        host = host.strip().lower()
        if host[-1:] == "/":
            host = host[0:-1]
        if ((host[-1:].isalpha() or host[-1:].isdigit()) and (host[0:7]=="http://" or host[0:8]=="https://") ):
            self.__host = host
        else:
            raise ValueError(u"EXCEPTION: 参数host格式不正确，请检查。 host: %s" % host)
        #url应校验是/开头
        if (url[0:1]=="/" and url[-1:]!="/") or url=="/" or url=="":
            self.__url = url
        else:
            raise ValueError(u"EXCEPTION: 参数url格式不正确，请检查。 url: %s" % url)
        #params companyKey=874d8c821358a5e26f2524b10f43a292&https=0&ajax=1  需要处理为map类型
        self.__params = {}
        self.paramType = ""
        logging.debug("得到的参数是：%s" % params)
        if params.strip() != "":
            if isJson(params):
                self.paramType = "json"
                self.__params = json.loads(params) #如果是json给param赋值
            else:
                self.paramType = "x-www-form-urlencoded"
                keyvaluelist = params.split("&")
                for keyvalue in keyvaluelist:
                    tmplist = keyvalue.split("=")
                    if len(tmplist) == 2:
                        self.__params[tmplist[0]]=tmplist[1]
                    elif len(tmplist)<2:
                        raise ValueError(u"EXCEPTION: 参数params格式不正确，请检查[参数%s的长度为%d.]。 params: %s" % (tmplist[0],len(tmplist),params))
                    elif len(tmplist)>2:
                        tag = 0
                        key = tmplist[0]
                        value=tmplist[1]
                        for tmp in tmplist:
                            if tag==0 or tag==1:
                                tag+=1
                            else:
                                value += "="+ tmp
                        self.__params[key]=value
            if TypeTool.is_dict(self.__params) == False:
                raise ValueError(u"EXCEPTION: 参数params类型不正确，请检查,目前支Content-Type[application/x-www-form-urlencoded]或者[application/json]")
        else:
            logging.debug("没有参数需要处理！")

        #应为map类型
        try:
            header = header.strip()=="" and "{}" or header
            header_dict = json.JSONDecoder().decode(header)
        except Exception as e:
            # logging.error(traceback.format_exc())
            raise ValueError(u"EXCEPTION: 参数header类型不正确，请检查,应该为合法JSON字符串。")
        if TypeTool.is_dict(header_dict) :
            self.__header = header_dict
        else:
            raise ValueError(u"EXCEPTION: 参数header类型不正确，请检查,应该为dict类型。")

    @property
    def host(self):
        return self.__host.strip()

    @host.setter
    def host(self,host):
        #host应校验末尾是数字或字母，并且开头是http://,否则host格式不合法，创建对象失败
        if ((host[-1:].isalpha() or host[-1:].isdigit()) and host[0:7]=="http://" ):
            self.__host = host
        else:
            raise ValueError(u"EXCEPTION: 参数host格式不正确，请检查。 host: %s" % host)

    @property
    def url(self):
        return self.__url.strip()

    @url.setter
    def url(self,url):
        #url应校验是/开头
        if (url[0:1]=="/" ):
            self.__url = url
        else:
            raise ValueError(u"EXCEPTION: 参数url格式不正确，请检查。 url: %s" % url)

    @property
    def params(self):
        return self.__params

    @params.setter
    def params(self,params):
        #params companyKey=874d8c821358a5e26f2524b10f43a292&https=0&ajax=1  需要处理为map类型
        keyvaluelist = params.split("&")
        self.__params={}
        for keyvalue in keyvaluelist:
            tmplist = keyvalue.split("=")
            if len(tmplist) == 2:
                self.__params[tmplist[0]]=tmplist[1]
            elif len(tmplist)<2:
                raise ValueError(u"EXCEPTION: 参数params格式不正确，请检查[参数%s的长度为%d.]。 params: %s" % (tmplist[0],len(tmplist),params))
            elif len(tmplist)>2:
                tag = 0
                key = tmplist[0]
                value=tmplist[1]
                for tmp in tmplist:
                    if tag==0 or tag==1:
                        tag+=1
                    else:
                        value += "="+ tmp
                self.__params[key]=value

    @property
    def header(self):
        return self.__header

    @header.setter
    def header(self,headers):
        #应为map类型
        if TypeTool.is_dict(headers) :
            self.__header = headers
        else:
            raise ValueError(u"EXCEPTION: 参数headers类型不正确，请检查,应该为dict类型。")

    def get(self):
        try:
            self.header['Content-Type'] = "application/x-www-form-urlencoded"
            logging.debug(u"Host是%s" % self.host)
            logging.debug( u"发送GET请求%s" % self.url)
            logging.debug( u"参数是%s" % self.params)
            logging.debug(u"头信息是%s" % self.header)
            logging.debug(u"超时时间是%s" % self.timeout)
            result = self.sess.get(self.host + self.url,headers=self.header,params=self.params, timeout=self.timeout, verify=False)
            return result
        except Exception as e:
            # logging.error(traceback.format_exc())
            raise ValueError(u"EXCEPTION: GET请求时发生异常：%s" % e)

    def post(self):
        if self.paramType == "json":
            return self.postJson()
        elif self.paramType == "x-www-form-urlencoded":
            return self.postUrlencode()
        else:
            return self.postUrlencode()

    def postUrlencode(self):
        try:
            self.header['Content-Type'] = "application/x-www-form-urlencoded"
            logging.debug(u"Host是[%s]" % self.host)
            logging.debug( u"发送postUrlencode请求[%s]" % self.url)
            logging.debug( u"参数是%s" % self.params)
            logging.debug( u"头信息是%s" % self.header)
            logging.debug(u"超时时间是%s" % self.timeout)
            result = self.sess.post(self.host + self.url, headers=self.header, data=self.params, timeout=self.timeout, verify=False)
            return result
        except Exception as e:
            # logging.error(traceback.format_exc())
            raise ValueError(u"EXCEPTION: POST请求时发生异常：%s" % e)

    def postJson(self):
        try:
            self.header['Content-Type'] = "application/json"
            logging.debug(u"Host是[%s]" % self.host)
            logging.debug( u"发送postJson请求[%s]" % self.url)
            logging.debug( u"参数是%s" % self.params)
            logging.debug( u"头信息是%s" % self.header)
            logging.debug(u"超时时间是%s" % self.timeout)
            result = self.sess.post(self.host + self.url, headers=self.header, json=self.params, timeout=self.timeout, verify=False)
            return result
        except Exception as e:
            # logging.error(traceback.format_exc())
            raise ValueError(u"EXCEPTION: POST请求时发生异常：%s" % e)

    def put(self):
        if self.paramType == "json":
            return self.putJson()
        elif self.paramType == "x-www-form-urlencoded":
            return self.putUrlencode()
        else:
            return self.putUrlencode()

    def putUrlencode(self):
        try:
            self.header['Content-Type'] = "application/x-www-form-urlencoded"
            result = self.sess.put(self.host + self.url, headers=self.header, data=self.params, timeout=self.timeout, verify=False)
            logging.debug(u"Host是%s" % self.host)
            logging.debug( u"发送PUT请求%s" % self.url)
            logging.debug( u"参数是%s" % self.params)
            logging.debug( u"头信息是%s" % self.header)
            return result
        except Exception as e:
            # logging.error(traceback.format_exc())
            raise ValueError(u"EXCEPTION: PUT请求时发生异常：%s" % e)

    def putJson(self):
        try:
            self.header['Content-Type'] = "application/json"
            result = self.sess.put(self.host + self.url, headers=self.header, json=self.params, timeout=self.timeout, verify=False)
            logging.debug(u"Host是%s" % self.host)
            logging.debug( u"发送PUT请求%s" % self.url)
            logging.debug( u"参数是%s" % self.params)
            logging.debug( u"头信息是%s" % self.header)
            return result
        except Exception as e:
            # logging.error(traceback.format_exc())
            raise ValueError(u"EXCEPTION: PUT请求时发生异常：%s" % e)

    def delete(self):
        if self.paramType == "json":
            return self.deleteJson()
        elif self.paramType == "x-www-form-urlencoded":
            return self.deleteUrlencode()
        else:
            return self.deleteUrlencode()

    def deleteUrlencode(self):
        try:
            self.header['Content-Type'] = "application/x-www-form-urlencoded"
            result = self.sess.delete(self.host + self.url, headers=self.header, data=self.params, timeout=self.timeout,
                                   verify=False)
            logging.debug(u"Host是%s" % self.host)
            logging.debug(u"发送DELETE请求%s" % self.url)
            logging.debug(u"参数是%s" % self.params)
            logging.debug(u"头信息是%s" % self.header)
            return result
        except Exception as e:
            # logging.error(traceback.format_exc())
            raise ValueError(u"EXCEPTION: DELETE请求时发生异常：%s" % e)

    def deleteJson(self):
        try:
            self.header['Content-Type'] = "application/json"
            result = self.sess.delete(self.host + self.url, headers=self.header, json=self.params, timeout=self.timeout,
                                   verify=False)
            logging.debug(u"Host是%s" % self.host)
            logging.debug(u"发送DELETE请求%s" % self.url)
            logging.debug(u"参数是%s" % self.params)
            logging.debug(u"头信息是%s" % self.header)
            return result
        except Exception as e:
            # logging.error(traceback.format_exc())
            raise ValueError(u"EXCEPTION: DELETE请求时发生异常：%s" % e)

    def postMobile(self):
        # mutipart/data param
        # urlparam
        # bodyparam
        #
        files = {  'source': ( None,'2',"text/plain; charset=UTF-8") }
        response = self.sess.post(self.host+self.url, params=self.params ,files = files, verify=False)
        return response
