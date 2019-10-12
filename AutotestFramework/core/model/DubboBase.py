import urllib,requests
from copy import deepcopy
from core.model.CommonAttr import CommonAttr
from core.processor.HttpProcesserV2 import HttpProcesserV2
from core.processor.KP import KP
from core.tools.CommonFunc import *

from core.const.GlobalConst import DBConst
from core.const.GlobalConst import ExecStatus
from core.decorator.normal_functions import *
from core.processor.Assert import Assert
from core.processor.CP import CP
from core.processor.BP import BP
from core.tools.DBTool import DBTool
from core.tools.TypeTool import TypeTool

from core.keywords import *
import telnetlib,chardet

class DubboBase(CommonAttr):
    """
    Http基础处理类，接口/步骤都继承此类，包含HTTP请求的所有通用属性。
    """
    def __init__(self):
        super(DubboBase, self).__init__()
        #设置协议
        self.protocol = "DUBBO"
        #HTTP执行信息
        self.varsPre = "" #前置变量

        self.useCustomUri = 0
        self.customUri = ""
        self.dubboSystem = ""
        self.dubboService = ""
        self.dubboMethod = ""
        self.dubboParam = ""
        self.encoding = "gb18030"

        self.requestTimeout = 20
        self.varsPost = "" #后置变量
        #执行
        self.execStatus = ExecStatus.NOTRUN
        #结果展示使用的
        self.varsPreFinalStr = ""
        self.varsPostFinalStr = ""

        self.actualResult = "" #实际结果 #return result with time
        self.assertResult = "" #断言结果
        self.testResult = ResultConst.NOTRUN #测试结果

        self.beforeExecuteTakeTime = 0.0
        self.afterExecuteTakeTime = 0.0
        self.executeTakeTime = 0.0
        self.totalTakeTime = 0.0
        # self.taskExecTakeTime = 0.0

        #通用信息
        self.state = 1
        self.addBy = ""
        self.modBy = ""
        self.addTime = ""
        self.modTime = ""


        #全局使用的，上下文关联的
        self.dubboTelnetHost = ""
        self.dubboTelnetPort = 0
        ###数据库相关的
        self.serviceDB = DBTool()
        self.serviceDBDict = {}
        self.calledInterfaceRecurDict = {} #存放循环的dict。

        #Task/Testcase/Step/Interface/HttpBase全局传递变量
        self.varsPool = {} #变量dict 变量池，累加，从外部集成，包括varsPre的和varsPost的
        self.varsKeyList = [] #变量列表，保存变量前后顺序。

        self.dubboResponseString = ""#返回的结果，也就是最近执行的dubbo接口返回的结果
        self.isRequested = False
        self.exitExecStatusList = [ResultConst.FAIL,ResultConst.EXCEPTION,ResultConst.ERROR]

    @catch_exception
    def execute(self):
        """
        执行函数，包括整个接口/步骤的执行过程。
        Returns:
            无。
        """
        logging.debug("#########################DUBBO_BASE执行开始[%s]#########################" % (self.addBy))
        try:
            if self.processBeforeExecute() == False:
                return
            #DONE 5、处理 url method header parmas中的变量替换、关键字处理
            self.processExecuteAttrAndRun(True)
            if self.testResult in self.exitExecStatusList :
                self.assertResult = "执行DUBBO请求时出现错误或者异常：\n%s" % self.assertResult
                return

            if self.processAfterExecute() == False:
                return

        except Exception as e:
            logging.error(traceback.format_exc())
        finally:
            self.releaseDB() #释放数据库连接，防止mysql连接过多错误
            logging.debug("测试结果： %s" % self.testResult)
            logging.debug("断言结果： %s" % self.assertResult)
            logging.debug("单接口或步骤执行时间： %f" % self.totalTakeTime)
            logging.debug("#########################DUBBO_BASE执行结束[%s]#########################"  % self.addBy)

    def initRequestHostAndResults(self):
        """
        执行前初始化的一些基本信息
        Returns:
            无。
        """
        super(DubboBase, self).initRequestHostAndResults()
        try:
            systemValue = ""
            if self.useCustomUri == 0:
                systemValue = self.getRequestAddr(self.dubboSystem)
                telnetHostInfoList = systemValue.split(":")
                if len(telnetHostInfoList) == 2:
                    self.dubboTelnetHost = telnetHostInfoList[0].strip()
                    self.dubboTelnetPort = int(telnetHostInfoList[1].strip())
                else:
                    self.setERROR("环境[%s]的服务[%s]的请求地址[%s]配置错误，请前往%s/interfaceTest/HTTP_EnvUriConf进行配置。" % (
                    self.confHttpLayer.key, self.dubboSystem, systemValue, EnvConfig.WEB_URI))
            else:
                systemValue = self.customUri
                telnetHostInfoList = systemValue.split(":")
                if len(telnetHostInfoList) == 2:
                    self.dubboTelnetHost = telnetHostInfoList[0].strip()
                    self.dubboTelnetPort = int(telnetHostInfoList[1].strip())
                else:
                    self.setERROR("自定义请求地址[%s]配置错误，请前往接口用例中进行配置。" % (
                        systemValue))
            print(self.dubboTelnetHost )
            print(self.dubboTelnetPort )
        except Exception as e:
            logging.error(traceback.format_exc())
            self.dubboTelnetHost = self.dubboSystem
            self.setERROR("<ERROR:系统错误：当前系统%s的配置是%s.>" % (self.dubboSystem,systemValue))


    def checkAllInfosAfterTest(self):
        super(DubboBase, self).checkAllInfosAfterTest()
        self.dubboSystem = (self.dubboSystem == None or self.dubboSystem.strip() == "" ) and "未发现系统" or self.dubboSystem
        self.dubboService = (self.dubboService == None or self.dubboService.strip() == "" ) and "未发现服务" or self.dubboService
        self.dubboMethod = (self.dubboMethod == None or self.dubboMethod.strip() == "" ) and "未发现接口" or self.dubboMethod

    @take_time
    @catch_exception
    def validate(self):
        """
        对属性的一些验证，如果不如何条件那么将ERROR，不继续执行。
        Returns:
            处理结果False/True。
        """

        return True


    @catch_exception
    def invokeDubboRequest(self,whetherSetResult = True):
        """
        发送http请求
        Returns:
            发送请求结果 False/True
        """
        requestStartTime = time.time()
        try:
            self.actualResult = ""
            command = """invoke %s.%s(%s)""" % (self.dubboService,self.dubboMethod,self.dubboParam)
            doInvokeStarttime = time.time()
            retMsg,takeTime = self.do_telnet(self.dubboTelnetHost,self.dubboTelnetPort,command)
            doInvokeEndtime = time.time()
            import core.processor.CP
            self.actualResult = core.processor.CP.confuseAllStr(retMsg)
            self.dubboResponseString = retMsg
            self.executeTakeTime = int((doInvokeEndtime-doInvokeStarttime)*1000) if takeTime == 0 else takeTime
        except Exception as e:
            if whetherSetResult:
                self.setERROR("%s: 请求异常[%s]" % (ResultConst.ERROR, traceback.format_exc()))
            else:
                self.actualResult = "%s: 请求异常[%s]" % (ResultConst.ERROR, traceback.format_exc())
        finally:
            requestEndTime = time.time()
            self.isRequested = True
            if self.executeTakeTime == 0:
                self.executeTakeTime = int((requestEndTime - requestStartTime) * 1000)

    def do_telnet( self,host, port, command, finish = b'dubbo>'):
            """执行telnet命令
            :param host:
            :param port:
            :param finish:
            :param command:
            :return:
            """
            # 连接Telnet服务器
            try:
                myOsEncoding = self.encoding
                tn=""
                is_conn_telnet = False
                tn = telnetlib.Telnet(host, port, timeout=10)
                tn.set_debuglevel(0)  # 设置debug输出级别  0位不输出，越高输出越多
                # 输入回车
                tn.write(b'\r\n')
                # 执行命令 增加默认时间30s
                none_until = tn.read_until(finish,timeout=10).decode(myOsEncoding)
                if none_until.strip() == finish :
                    is_conn_telnet = True
                tn.write(b'%s\r\n' % command.encode(myOsEncoding))
                # 执行完毕后，终止Telnet连接（或输入exit退出）
                return_msg_bytes = tn.read_until(finish, timeout=self.requestTimeout)
                try:
                    return_msg = return_msg_bytes.decode(myOsEncoding)
                except:
                    return_msg = str(return_msg_bytes)

                if len(return_msg) == 0:
                    self.setERROR("<ERROR: DUBBO请求%s秒内没有返回，请求超时！或者解码错误！>" % self.requestTimeout)
                    return "<ERROR: DUBBO请求%s秒内没有返回，请求超时！或者解码错误！>" % self.requestTimeout, 0

                if "elapsed:" in return_msg:
                    msgList = return_msg.split("elapsed:")
                    return msgList[0],int(msgList[1].split("ms")[0].strip())
                else:
                    return return_msg,0
            except Exception as e:
                logging.error(traceback.format_exc())
                if is_conn_telnet:
                    return "请求参数错误等异常，导致请求返回异常。",0
                else:
                    return "TELNET_ERROR: Telnet请求时发生网络问题或者接口错误，请确认。",0
            finally:
                if type(tn) != type(""):
                    tn.close()

    @catch_exception
    def processExecuteAttrAndRun(self,whetherSetResult = True):
        super(DubboBase, self).processExecuteAttrAndRun()
        logging.debug("EXECUTE_HTTP_STEP_4: 处理dubboService/dubboMethod/dubboParam/中的变量替换、关键字处理。")
        baseDubboService = self.dubboService
        self.dubboService = self.processKPWithNoneTag(self.dubboService)
        self.processedDubboService = self.dubboService
        if self.testResult in self.exitExecStatusList:
            self.assertResult = "处理请求信息中的服务Service中的变量替换、关键字处理时出现错误：\n%s" % self.assertResult
            return
        baseDubboMethod = self.dubboService
        self.dubboMethod = self.processKPWithNoneTag(self.dubboMethod)
        self.processedDubboMethod = self.dubboMethod
        if self.testResult in self.exitExecStatusList:
            self.assertResult = "处理请求信息中的接口Method中的变量替换、关键字处理时出现错误：\n%s" % self.assertResult
            return

        baseDubboParam = self.dubboParam
        self.dubboParam = self.processKPWithNoneTag(self.dubboParam)
        self.processedDubboParam = self.dubboParam
        if self.testResult in self.exitExecStatusList:
            self.assertResult = "处理请求信息中的PARAMS中的变量替换、关键字处理时出现错误：\n%s" % self.assertResult
            return

        # DONE 6、执行http请求
        logging.debug("EXECUTE_HTTP_STEP_5: 执行dubbo请求。")
        self.invokeDubboRequest(whetherSetResult)  ####执行dubbo请求
        if whetherSetResult:
            pass
        else:
            self.dubboService = baseDubboService
            self.dubboMethod = baseDubboMethod
            self.dubboParam = baseDubboParam