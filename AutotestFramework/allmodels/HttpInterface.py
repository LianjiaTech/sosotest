from core.model.HttpBase import HttpBase
from core.decorator.normal_functions import *
from core.tools.DBTool import DBTool
from core.tools.CommonFunc import *
from core.const.GlobalConst import CaseLevel
from core.const.GlobalConst import CaseStatus
from core.const.GlobalConst import ObjTypeConst
from core.const.GlobalConst import PerformanceConst
from core.config.InitConfig import *

class HttpInterface(HttpBase):
    """
    Http接口类，继承HttpBase，并添加接口特殊属性。
    """
    def __init__(self,id = 0, interfaceId = "", interfaceDebugId = 0):
        super(HttpInterface, self).__init__()
        self.objType = ObjTypeConst.INTERFACE

        self.id = id
        self.interfaceId = interfaceId
        self.interfaceDebugId = interfaceDebugId
        #基本信息
        self.title = ""
        self.desc = ""
        self.businessLine = "" #ywx
        self.modules = ""  #mk
        self.level = CaseLevel.MIDIUM  #优先级
        self.status = CaseStatus.UN_AUDIT #用例状态 未审核 审核通过 审核未通过  任务添加只能添加审核通过的用例

        self.interfacePerformanceResult = PerformanceConst.NA

    @take_time
    @catch_exception
    def generateByInterfaceDebugId(self):
        """
        根据interfaceDebugId从tb_http_interface_debug获取调试数据。
        Returns:
            执行结果
        """
        # colstr = "id, httpConfKey, serviceConfKey, alias, httpConfDesc, httpConf, state, addBy, modBy, addTime, modTime"
        # sql = """ SELECT * FROM tb_http_interface_debug where id = %d """ % (self.interfaceDebugId)
        # self.globalDB.initGlobalDBConf()
        # res = self.globalDB.execute_sql(sql)
        # self.globalDB.release()
        self.serviceRedis.initRedisConf()
        try:
            tmpInterface = json.loads(self.serviceRedis.get_data(self.interfaceDebugId))
        except Exception as e:
            return False
        if tmpInterface:
            # tmpInterface = res[0]
            # self.id = tmpInterface['id']
            if "interfaceId" in tmpInterface.keys():
                self.interfaceId = tmpInterface['interfaceId']
            else:
                self.interfaceId = ""

            self.traceId = md5("%s-%s" % (self.interfaceId, get_current_time()))

            self.execStatus = tmpInterface['execStatus']

            self.title = tmpInterface['title']
            self.desc = tmpInterface['casedesc']
            # self.state = tmpInterface['state']
            # self.addBy = tmpInterface['addBy']
            # self.modBy = tmpInterface['modBy']
            # self.addTime = tmpInterface['addTime']
            # self.modTime = tmpInterface['modTime']
            self.urlRedirect = tmpInterface['urlRedirect']
            if int(tmpInterface['urlRedirect']) == 0:
                self.urlRedirectStatus = False
            self.businessLineId = tmpInterface['businessLineId']
            self.modules = tmpInterface['moduleId']
            self.level = tmpInterface['caselevel']   # 优先级
            # self.status = tmpInterface['status']   # 用例状态 未审核 审核通过 审核未通过  任务添加只能添加审核通过的用例
            self.varsPre = tmpInterface['varsPre']  # 前置变量
            if int(tmpInterface['useCustomUri']) == 1:
                self.uri = tmpInterface['customUri']
            else:
                self.uri = tmpInterface['uri']
            self.url = tmpInterface['url']   # 接口 interface
            self.method = tmpInterface['method']
            self.header = tmpInterface['header']
            self.params = tmpInterface['params']  # key1=value1&key2=value2
            self.bodyType = tmpInterface['bodyType'].strip()  # bodyType
            self.bodyContent = tmpInterface['bodyContent'].strip()  # bodyContent

            self.version = tmpInterface['version'].strip()

            self.varsPost = tmpInterface['varsPost']   # 后置变量
            self.httprequestTimeout = tmpInterface['timeout']
            self.performanceTime = tmpInterface['performanceTime'] * 1000

            self.actualResult = tmpInterface['actualResult']  # 实际结果
            self.assertResult = tmpInterface['assertResult']   # 断言结果
            self.testResult = tmpInterface['testResult']   # 测试结果

            self.beforeExecuteTakeTime = tmpInterface['beforeExecuteTakeTime']
            self.afterExecuteTakeTime = tmpInterface['afterExecuteTakeTime']
            self.executeTakeTime = tmpInterface['executeTakeTime']
            self.totalTakeTime = tmpInterface['totalTakeTime']

            self.httpConfKey = tmpInterface['httpConfKey']
            self.confHttpLayer.key = self.httpConfKey
            self.confHttpLayer.generate_http_conf_by_key()

            self.varsStr = ""  # 变量string
            self.varsPool = {}  # 变量dict 变量池，包括varsPre的和varsPost的
            self.headerDict = {} #header json字符串转换成的dict
            return True
        else:
            return False

    def generateByInterfaceId(self):
        """
        从tb_http_interface表根绝interfaceId获取并给属性赋值。
        Returns:
            执行结果
        """
        # colstr = "id, httpConfKey, serviceConfKey, alias, httpConfDesc, httpConf, state, addBy, modBy, addTime, modTime"
        self.traceId = md5("%s-%s" % (self.interfaceId, get_current_time()))

        if self.version == "CurrentVersion":
            sql = """ SELECT * FROM tb_http_interface where interfaceId = '%s' and state = 1 """ % (self.interfaceId)
        else:
            sql = """ SELECT * FROM tb_version_http_interface where interfaceId = '%s' and versionName='%s' and state = 1 """ % (self.interfaceId,self.version)

        self.globalDB.initGlobalDBConf()
        res = self.globalDB.execute_sql(sql)
        self.globalDB.release()
        if res:
            tmpInterface = res[0]
            self.id = tmpInterface['id']
            self.title = tmpInterface['title']
            self.desc = tmpInterface['casedesc']
            self.state = tmpInterface['state']
            self.addBy = tmpInterface['addBy']
            self.modBy = tmpInterface['modBy']
            self.addTime = tmpInterface['addTime']
            self.modTime = tmpInterface['modTime']

            self.urlRedirect = tmpInterface['urlRedirect']
            if int(tmpInterface['urlRedirect']) == 0:
                self.urlRedirectStatus = False
            self.businessLineId = tmpInterface['businessLineId']
            self.modules = tmpInterface['moduleId']
            self.level = tmpInterface['caselevel']   # 优先级
            self.status = tmpInterface['status']   # 用例状态 未审核 审核通过 审核未通过  任务添加只能添加审核通过的用例
            self.varsPre = tmpInterface['varsPre']   # 前置变量
            if int(tmpInterface['useCustomUri']) == 1:
                self.uri = tmpInterface['customUri']
            else:
                self.uri = tmpInterface['uri']
            self.url = tmpInterface['url']   # 接口 interface
            self.method = tmpInterface['method']
            self.header = tmpInterface['header']
            self.params = tmpInterface['params']  # key1=value1&key2=value2
            self.bodyType = tmpInterface['bodyType'].strip()  # key1=value1&key2=value2
            self.bodyContent = tmpInterface['bodyContent'].strip()  # key1=value1&key2=value2
            self.performanceTime = tmpInterface['performanceTime'] * 1000

            self.varsPost = tmpInterface['varsPost']   # 后置变量
            self.httprequestTimeout = tmpInterface['timeout']
            return True
        else:
            return False

    def generateByInterfaceDict(self,interfaceDict):
        """
        根据传入的interfaceDict生成interface对象。
        Returns:
            执行结果
        """
        tmpInterface = interfaceDict
        self.id = tmpInterface['id']
        self.interfaceId = tmpInterface['interfaceId']
        self.traceId = md5("%s-%s" % (self.interfaceId, get_current_time()))

        self.title = tmpInterface['title']
        self.desc = tmpInterface['casedesc']
        self.state = tmpInterface['state']
        self.addBy = tmpInterface['addBy']
        self.modBy = tmpInterface['modBy']
        self.addTime = tmpInterface['addTime']
        self.modTime = tmpInterface['modTime']

        self.businessLineId =  tmpInterface['businessLineId']
        self.modules = tmpInterface['moduleId']
        self.level = tmpInterface['caselevel']   # 优先级
        self.status = tmpInterface['status']   # 用例状态 未审核 审核通过 审核未通过  任务添加只能添加审核通过的用例
        self.varsPre = tmpInterface['varsPre']   # 前置变量

        self.urlRedirect = tmpInterface['urlRedirect']
        if int(tmpInterface['urlRedirect']) == 0:
            self.urlRedirectStatus = False
        if int(tmpInterface['useCustomUri']) == 1:
            self.uri = tmpInterface['customUri']
        else:
            self.uri = tmpInterface['uri']
        self.url = tmpInterface['url']   # 接口 interface
        self.method = tmpInterface['method']
        self.header = tmpInterface['header']
        self.params = tmpInterface['params']  # key1=value1&key2=value2
        self.bodyType = tmpInterface['bodyType'].strip()  # key1=value1&key2=value2
        self.bodyContent = tmpInterface['bodyContent'].strip()  # key1=value1&key2=value2

        self.varsPost = tmpInterface['varsPost']   # 后置变量
        self.httprequestTimeout = tmpInterface['timeout']
        self.performanceTime = tmpInterface['performanceTime'] * 1000

        self.version = tmpInterface['version']


    @catch_exception
    def updateByInterfaceDebugId(self):
        """
        更新执行结果到tb_http_interface_debug表
        Returns:
            无
        """

        self.testResult = self.testResult == None and "没有生成测试结果" or self.testResult
        self.actualResult = self.actualResult == None and "没有实际返回结果" or self.actualResult
        self.assertResult = self.assertResult == None and "没有断言结果" or self.assertResult
        self.varsPre = self.varsPre == None and "未发现前置变量" or self.varsPre
        self.varsPost = self.varsPost == None and "未发现后置变量" or self.varsPost
        self.params = self.params == None and "没有参数" or self.params
        self.header = self.header == None and "没有头信息" or self.header
        self.uri = self.host

        try:
            redisDictData = json.loads(self.serviceRedis.get_data(self.interfaceDebugId))
            redisDictData["testResult"] = self.testResult
            redisDictData["method"] = self.method
            redisDictData["actualResult"] = self.actualResult
            redisDictData["assertResult"] = self.assertResult
            redisDictData["varsPre"] = self.varsPre
            redisDictData["varsPost"] = self.varsPost
            redisDictData["params"] = self.paramsFinalStr
            redisDictData["header"] = self.headerFinalStr
            redisDictData["uri"] = self.uri
            redisDictData["url"] = self.urlFinalStr
            redisDictData["urlRedirect"] = self.urlRedirect
            redisDictData["execStatus"] = 3
            redisDictData["bodyContent"] = self.bodyContentFinalStr
            redisDictData["beforeExecuteTakeTime"] = self.beforeExecuteTakeTime
            redisDictData["afterExecuteTakeTime"] = self.afterExecuteTakeTime
            redisDictData["executeTakeTime"] = self.executeTakeTime
            redisDictData["totalTakeTime"] = self.totalTakeTime
            self.serviceRedis.set_data(self.interfaceDebugId,json.dumps(redisDictData),60*60)

        except Exception as e:
            logging.error("测试结果写入缓存发生异常 %s " % traceback.format_exc())
            logging.error("测试结果写入缓存发生异常")

        tcpStr = '{"do":9,"InterfaceDebugId":"%s","protocol":"%s"}' % (self.interfaceDebugId,self.protocol)
        if sendTcp(TcpServerConf.ip,TcpServerConf.port,tcpStr):
            logging.info("%s 调试完毕通知主服务成功" % self.interfaceDebugId)
            # logging.info("",TcpServerConf.ip,TcpServerConf.port)
        else:
            logging.info("%s 调试完毕通知主服务失败" % self.interfaceDebugId)

    @take_time
    def executeInterface(self):
        """
        执行接口
        Returns:
            无
        """
        logging.debug("####################################################接口用例INTERFACE：%s开始执行在环境[%s]执行人[%s]####################################################" % (self.interfaceId,self.confHttpLayer.key,self.addBy))
        super(HttpInterface, self).execute()
        logging.debug("####################################################接口用例：%s结束执行[%s]####################################################" % (self.interfaceId,self.addBy))


if __name__ == "__main__":
    httpInterface = HttpInterface()
    httpInterface.interfaceId = "HTTP_INTERFACE_1"
    httpInterface.generateByInterfaceId()
    print (httpInterface.desc)
