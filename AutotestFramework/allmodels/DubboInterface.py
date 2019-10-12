from core.model.DubboBase import DubboBase
from core.decorator.normal_functions import *
from core.tools.DBTool import DBTool
from core.tools.CommonFunc import *
from core.const.GlobalConst import CaseLevel
from core.const.GlobalConst import CaseStatus
from core.const.GlobalConst import ObjTypeConst
from runfunc.initial import *

class DubboInterface(DubboBase):
    """
    Http接口类，继承HttpBase，并添加接口特殊属性。
    """
    def __init__(self,id = 0, interfaceId = "", interfaceDebugId = ""):
        super(DubboInterface, self).__init__()
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

    @take_time
    @catch_exception
    def generateByInterfaceDebugId(self):
        """
        根据interfaceDebugId从tb_http_interface_debug获取调试数据。
        Returns:
            执行结果
        """
        # colstr = "id, httpConfKey, serviceConfKey, alias, httpConfDesc, httpConf, state, addBy, modBy, addTime, modTime"
        sql = """ SELECT * FROM tb2_dubbo_interface_debug where id = %d """ % (self.interfaceDebugId)
        self.globalDB.initGlobalDBConf()
        res = self.globalDB.execute_sql(sql)
        self.globalDB.release()
        if res:
            tmpInterface = res[0]
            self.id = tmpInterface['id']

            if "interfaceId" in tmpInterface.keys():
                self.interfaceId = tmpInterface['interfaceId']
            else:
                self.interfaceId = ""
            self.traceId = md5("%s-%s" % (self.interfaceId, get_current_time()))

            self.execStatus = tmpInterface['execStatus']

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
            self.varsPre = tmpInterface['varsPre']  # 前置变量

            self.useCustomUri = tmpInterface['useCustomUri']
            self.customUri = tmpInterface['customUri']
            self.dubboSystem = tmpInterface['dubboSystem']
            self.dubboService = tmpInterface['dubboService']   # 接口 interface
            self.dubboMethod = tmpInterface['dubboMethod']
            self.dubboParam = tmpInterface['dubboParams']  # key1=value1&key2=value2
            self.encoding = tmpInterface['encoding']  # key1=value1&key2=value2

            self.version = tmpInterface['version'].strip()

            self.varsPost = tmpInterface['varsPost']   # 后置变量
            self.httprequestTimeout = tmpInterface['timeout']

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

    @take_time
    @catch_exception
    def generateByInterfaceDebugIdForRedis(self):
        """
        根据interfaceDebugId从tb_http_interface_debug获取调试数据。
        Returns:
            执行结果
        """
        self.serviceRedis.initRedisConf()
        try:
            tmpInterface = json.loads(self.serviceRedis.get_data(self.interfaceDebugId))
        except Exception as e:
            return False
        if tmpInterface:
            if "interfaceId" in tmpInterface.keys():
                self.interfaceId = tmpInterface['interfaceId']
            else:
                self.interfaceId = ""
            self.traceId = md5("%s-%s" % (self.interfaceId, get_current_time()))

            self.execStatus = tmpInterface['execStatus']

            self.title = tmpInterface['title']
            self.desc = tmpInterface['casedesc']

            self.businessLineId = tmpInterface['businessLineId']
            self.modules = tmpInterface['moduleId']
            self.level = tmpInterface['caselevel']  # 优先级
            # self.status = tmpInterface['status']  # 用例状态 未审核 审核通过 审核未通过  任务添加只能添加审核通过的用例
            self.varsPre = tmpInterface['varsPre']  # 前置变量

            self.useCustomUri = tmpInterface['useCustomUri']
            self.customUri = tmpInterface['customUri']
            self.dubboSystem = tmpInterface['dubboSystem']
            self.dubboService = tmpInterface['dubboService']  # 接口 interface
            self.dubboMethod = tmpInterface['dubboMethod']
            self.dubboParam = tmpInterface['dubboParams']  # key1=value1&key2=value2
            self.encoding = tmpInterface['encoding']  # key1=value1&key2=value2

            self.version = tmpInterface['version'].strip()

            self.varsPost = tmpInterface['varsPost']  # 后置变量
            self.httprequestTimeout = tmpInterface['timeout']

            self.actualResult = tmpInterface['actualResult']  # 实际结果
            self.assertResult = tmpInterface['assertResult']  # 断言结果
            self.testResult = tmpInterface['testResult']  # 测试结果

            self.beforeExecuteTakeTime = tmpInterface['beforeExecuteTakeTime']
            self.afterExecuteTakeTime = tmpInterface['afterExecuteTakeTime']
            self.executeTakeTime = tmpInterface['executeTakeTime']
            self.totalTakeTime = tmpInterface['totalTakeTime']

            self.httpConfKey = tmpInterface['httpConfKey']
            self.confHttpLayer.key = self.httpConfKey
            self.confHttpLayer.generate_http_conf_by_key()

            self.varsStr = ""  # 变量string
            self.varsPool = {}  # 变量dict 变量池，包括varsPre的和varsPost的
            self.headerDict = {}  # header json字符串转换成的dict
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
            sql = """ SELECT * FROM tb2_dubbo_interface where interfaceId = '%s' and state = 1 """ % (self.interfaceId)
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

            self.businessLineId =  tmpInterface['businessLineId']
            self.modules = tmpInterface['moduleId']
            self.level = tmpInterface['caselevel']   # 优先级
            self.status = tmpInterface['status']   # 用例状态 未审核 审核通过 审核未通过  任务添加只能添加审核通过的用例
            self.varsPre = tmpInterface['varsPre']   # 前置变量

            self.useCustomUri = tmpInterface['useCustomUri']
            self.customUri = tmpInterface['customUri']
            self.dubboSystem = tmpInterface['dubboSystem']
            self.dubboService = tmpInterface['dubboService']   # 接口 interface
            self.dubboMethod = tmpInterface['dubboMethod']
            self.dubboParam = tmpInterface['dubboParams']  # key1=value1&key2=value2
            self.encoding = tmpInterface['encoding']

            self.varsPost = tmpInterface['varsPost']   # 后置变量
            self.requestTimeout = tmpInterface['timeout']
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

        self.dubboSystem = tmpInterface['dubboSystem']
        self.dubboService = tmpInterface['dubboService']   # 接口 interface
        self.dubboMethod = tmpInterface['dubboMethod']   # 接口 interface
        self.dubboParam = tmpInterface['dubboParams']  # key1=value1&key2=value2
        self.encoding = tmpInterface['encoding']

        self.varsPost = tmpInterface['varsPost']   # 后置变量
        self.dubborequestTimeout = tmpInterface['timeout']

        self.version = tmpInterface['version']

    @catch_exception
    def updateByInterfaceDebugId(self):
        """
        更新执行结果到tb_http_interface_debug表
        Returns:
            无
        """
        # colstr = "id, httpConfKey, serviceConfKey, alias, httpConfDesc, httpConf, state, addBy, modBy, addTime, modTime"
        self.testResult = self.testResult == None and "没有生成测试结果" or self.testResult
        self.actualResult = self.actualResult == None and "没有实际返回结果" or self.actualResult
        self.assertResult = self.assertResult == None and "没有断言结果" or self.assertResult
        self.varsPre = self.varsPre == None and "未发现前置变量" or self.varsPre
        self.varsPost = self.varsPost == None and "未发现后置变量" or self.varsPost
        #
        # sql = """ UPDATE tb2_dubbo_interface_debug SET dubboSystem='%s',dubboService='%s',dubboMethod='%s',dubboParams = '%s',testResult='%s',actualResult='%s',assertResult='%s',
        #         beforeExecuteTakeTime=%d,afterExecuteTakeTime=%d, executeTakeTime=%d, totalTakeTime=%d,varsPre='%s',varsPost='%s', execStatus = 3,modTime='%s' WHERE id=%d""" \
        #             % ("%s(%s:%s)" % (self.dubboSystem,self.dubboTelnetHost,str(self.dubboTelnetPort)),replacedForIntoDB(self.dubboService),replacedForIntoDB(self.dubboMethod),replacedForIntoDB(self.dubboParam) ,self.testResult,self.actualResult,self.assertResult,int(self.beforeExecuteTakeTime),int(self.afterExecuteTakeTime),int(self.executeTakeTime),
        #                int(self.totalTakeTime),self.varsPre,self.varsPost,get_current_time(),self.interfaceDebugId)
        # logging.debug(sql)
        try:
        #     self.globalDB.initGlobalDBConf()
        #     res = self.globalDB.execute_sql(sql)
        #     if res == False:
        #         sql = """ UPDATE tb2_dubbo_interface_debug SET dubboSystem='%s',dubboService='%s',dubboMethod='%s',dubboParams = '%s',testResult='%s',actualResult='%s',assertResult='%s',
        #         beforeExecuteTakeTime=%d,afterExecuteTakeTime=%d, executeTakeTime=%d, totalTakeTime=%d,varsPre='%s',varsPost='%s', execStatus = 3,modTime='%s' WHERE id=%d""" \
        #             % ("%s(%s:%s)" % (self.dubboSystem,self.dubboTelnetHost,str(self.dubboTelnetPort)),self.dubboService,self.dubboMethod,replacedForIntoDB(self.dubboParam) ,"EXCEPTION:请联系管理员！",
        #                "EXCEPTION:请联系管理员！","EXCEPTION:请联系管理员！",
        #                int(self.beforeExecuteTakeTime),int(self.afterExecuteTakeTime),int(self.executeTakeTime),
        #                int(self.totalTakeTime),"EXCEPTION:请联系管理员！","EXCEPTION:请联系管理员！",
        #                get_current_time(),self.interfaceDebugId)
        #
        #         self.globalDB.execute_sql(sql)

            redisDictData = json.loads(self.serviceRedis.get_data(self.interfaceDebugId))

            redisDictData['execStatus'] = 3

            redisDictData['dubboSystem'] = "%s(%s:%s)" % (self.dubboSystem,self.dubboTelnetHost,str(self.dubboTelnetPort))
            redisDictData['dubboService'] = self.dubboService
            redisDictData['dubboParams'] = self.dubboParam
            redisDictData['dubboMethod'] = self.dubboMethod
            redisDictData['version'] = self.version

            redisDictData['varsPre'] = self.varsPre  # 后置变量
            redisDictData['varsPost'] = self.varsPost  # 后置变量
            redisDictData['timeout'] = self.httprequestTimeout

            redisDictData['actualResult'] = self.actualResult  # 实际结果
            redisDictData['assertResult'] = self.assertResult   # 断言结果
            redisDictData['testResult'] = self.testResult   # 测试结果

            redisDictData['beforeExecuteTakeTime'] = self.beforeExecuteTakeTime
            redisDictData['afterExecuteTakeTime'] = self.afterExecuteTakeTime
            redisDictData['executeTakeTime'] = self.executeTakeTime
            redisDictData['totalTakeTime'] = self.totalTakeTime

            self.serviceRedis.set_data(self.interfaceDebugId, json.dumps(redisDictData), 60 * 60)

        except Exception as e:
            logging.error(traceback.format_exc())
        finally:

            tcpStr = '{"do":9,"InterfaceDebugId":"%s","protocol":"%s"}' % (self.interfaceDebugId, self.protocol)
            if sendTcp(TcpServerConf.ip, TcpServerConf.port, tcpStr):
                logging.info("%s 调试完毕通知主服务成功" % self.interfaceDebugId)
            else:
                logging.info("%s 调试完毕通知主服务失败" % self.interfaceDebugId)
            self.globalDB.release()

    @take_time
    def executeInterface(self):
        """
        执行接口
        Returns:
            无
        """
        logging.debug("####################################################DUBBO接口用例INTERFACE：%s开始执行在环境[%s]执行人[%s]####################################################" % (self.interfaceId,self.confHttpLayer.key,self.addBy))
        super(DubboInterface, self).execute()
        logging.debug("####################################################DUBBO接口用例：%s结束执行[%s]####################################################" % (self.interfaceId,self.addBy))


if __name__ == "__main__":
    pass