from core.tools.DBTool import DBTool
from core.tools.RedisTool import RedisTool
from core.tools.MongoTool import MongoTool
from core.model.ConfHttpLayer import ConfHttpLayer
from core.const.GlobalConst import ObjTypeConst,testLevelConst
import requests
from core.decorator.normal_functions import *

import urllib,requests
from copy import deepcopy
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
from core.tools.RedisTool import RedisTool
from core.tools.TypeTool import TypeTool

from core.keywords import *
import telnetlib,chardet
from core.tools.VerifyTool import VerifyTool

class CommonAttr(object):

    def __init__(self):
        self.interfaceId = "" # 接口用例就是直接显示id，case步骤是显示 caseId-stepNum
        self.version = ""
        self.protocol = ""
        self.objType = ObjTypeConst.UNKNOWN

        self.traceId = ""

        self.globalDB = DBTool()
        self.serviceDB = DBTool()
        self.serviceDBDict = {}
        self.serviceRedis = RedisTool()
        self.serviceRedisDict = {}
        self.serviceMongoDBDict = {}

        self.highPriorityVARSStr = ""  # 通过Str生成dict
        self.highPriorityVARSDict = {}  # 优先变量，当存在优先变量时，GVAR和VAR先调用优先变量，优先级最高，当调用$GVAR[key]或者$VAR[key]时，先看着里面是否有，如果存在将忽略db中的GVAR和变量列表中的变量。
        self.highPriorityVARSFinalStr = ""

        self.httpConfKey = ""
        self.confHttpLayer = ConfHttpLayer()

        self.varsPool = {} # 里面有 varkey PathVarkey 以及python模式相关的变量，没有声明路径的
        self.calledVarsKeyList = [] # {"key":"来源"}  这个只在本接口或者步骤内生效。

        self.current_session = requests.session()
        self.kw_LOGIN_ParamList = []
        self.context_data_list = []
        self.context_data_dict = {}

        self.version = "CurrentVersion"
        self.caseLevel = testLevelConst.RUNALL

        self.response = requests.models.Response()  # 最近HTTP请求返回的response对象，提供给各个方法使用
        self.interface_response = requests.models.Response()  # 要测试的接口返回的response，供断言使用。
        self.dubboResponseString = ""#返回的结果，也就是最近执行的dubbo接口返回的结果

        self.testResult = ResultConst.NOTRUN
        self.actualResult = ""
        self.assertResult = ""
        self.exitExecStatusList = [ResultConst.FAIL, ResultConst.EXCEPTION, ResultConst.ERROR]
        self.isRequested = False

        self.pythonModeStrPrefix = "python"
        self.pythonModeExecuteLog = ""
        self.pythonLogVarsPre = ""
        self.pythonLogVarsPost = ""
        self.noneTag = "@NONE@"
        self.validResultList = [ResultConst.ERROR,ResultConst.PASS,ResultConst.FAIL,ResultConst.NOTRUN,ResultConst.EXCEPTION,ResultConst.NO_ASSERT]

        self.varCallCountDict = {"GVAR":{},"VAR":{},"TEXT":{},"imports":{}} #设置GVAR 和 VAR
        self.calledInterfaceRecurDict = {}

        self.isPythonModePre = False
        self.isPythonModePost = False

        self.retryList = []



    def generateResultWhenNotRequsted(self):
        if self.isRequested == False:
            if self.protocol == "HTTP":
                self.interface_response = self.assertResult
                self.response = self.interface_response
            elif self.protocol == "DUBBO":
                self.dubboResponseString = self.assertResult

    @catch_exception
    def initDB(self):
        """
        执行前初始化的一些数据库信息
        Returns:
            无。
        """
        # 初始化serviceDB
        if "DB" in self.confHttpLayer.confServiceLayer.confDict.keys():
            logging.debug("○○21★1===traceId[%s]★★★★★" % self.traceId)
            serviceDBDict = self.confHttpLayer.confServiceLayer.confDict['DB']
            # 加载被测各个单点系统的数据库
            for tmpDbKey in serviceDBDict.keys():
                logging.debug("○○21★★2===traceId[%s] %s★★★★★" % (self.traceId, serviceDBDict[tmpDbKey]))
                logging.debug("○○21★★★3===traceId[%s] tmpDbKey[%s]★★★★★" % (self.traceId, tmpDbKey))
                tmpHost = serviceDBDict[tmpDbKey]["host"]
                logging.debug("○○21★★★★4===traceId[%s] tmpDbKey[%s]★★★★★" % (self.traceId, tmpDbKey))
                if tmpHost != "0.0.0.0" and tmpHost != "":
                    tmpPort = int(serviceDBDict[tmpDbKey]["port"])
                    tmpUsername = serviceDBDict[tmpDbKey]["username"]
                    tmpPassword = serviceDBDict[tmpDbKey]["password"]
                    tmpServiceDB = DBTool(host=tmpHost,
                                          port=tmpPort,
                                          username=tmpUsername,
                                          password=tmpPassword,
                                          isDictCursor=False)
                    self.serviceDBDict[tmpDbKey] = tmpServiceDB

    @catch_exception
    def initRedis(self):
        """
        执行前初始化的一些数据库信息
        Returns:
            无。
        """
        # 初始化平台db
        # 初始化serviceDB
        if "REDIS" in self.confHttpLayer.confServiceLayer.confDict.keys():
            serviceDBDict = self.confHttpLayer.confServiceLayer.confDict['REDIS']
            # 加载被测各个单点系统的数据库
            for tmpDbKey in serviceDBDict.keys():
                tmpHost = serviceDBDict[tmpDbKey]["host"]
                if tmpHost != "0.0.0.0" and tmpHost != "":
                    tmpPort = int(serviceDBDict[tmpDbKey]["port"])
                    tmpPassword = serviceDBDict[tmpDbKey]["password"] if "password" in serviceDBDict[tmpDbKey].keys() else ""
                    tmpServiceDB = RedisTool(host=tmpHost,
                                          port=tmpPort,
                                          password=tmpPassword)
                    self.serviceRedisDict[tmpDbKey] = tmpServiceDB

    @catch_exception
    def initMongoDB(self):
        """
        执行前初始化的一些mongodb信息
        Returns:
            无。
        """
        # 初始化平台db
        # 初始化serviceDB

        if "MONGO" in self.confHttpLayer.confServiceLayer.confDict.keys():
            logging.debug("○○23★1 mongo===traceId[%s]★★★★★" % self.traceId)

            serviceDBDict = self.confHttpLayer.confServiceLayer.confDict['MONGO']
            logging.debug("○○23★★2 mongo===traceId[%s]★★★★★" % self.traceId)

            # 加载被测各个单点系统的数据库
            for tmpDbKey in serviceDBDict.keys():
                logging.debug("○○23★★★3 mongo===traceId[%s] %s ★★★★★" % (self.traceId, serviceDBDict[tmpDbKey]))
                if serviceDBDict[tmpDbKey]['host'] != "0.0.0.0" and serviceDBDict[tmpDbKey]['host'] != "":
                    self.serviceMongoDBDict[tmpDbKey] = MongoTool(host=serviceDBDict[tmpDbKey]['host'],
                                            port=int(serviceDBDict[tmpDbKey]['port']),
                                            username=serviceDBDict[tmpDbKey]['username'] if "username" in serviceDBDict[tmpDbKey].keys() else None,
                                            password= serviceDBDict[tmpDbKey]['password'] if "password" in serviceDBDict[tmpDbKey].keys() else None)

    @catch_exception
    def releaseDB(self):
        """
        执行完释放数据库连接
        Returns:
            无。
        """
        self.globalDB.release()
        for tmpServiceDbKey,tmpServiceDbValue in self.serviceDBDict.items():
            tmpServiceDbValue.release()

    @take_time
    @catch_exception
    def setResult(self,result = ResultConst.ERROR,errorMsg = ""):
        """
        设置测试结果
        Args:
            result: 测试结果    PASS FAIL等
            errorMsg: 测试消息。

        Returns:
            无。
        """
        if result not in self.validResultList:
            self.testResult = ResultConst.ERROR
            self.assertResult = "%s: %s" % (ResultConst.ERROR, "不是合法的测试结果[%s]" % result)
            self.actualResult = "不是合法的测试结果[%s]" % result
            return

        self.assertResult = "%s: %s\n%s\n" % (result,errorMsg,self.assertResult)
        if TypeTool.is_str(self.actualResult) and self.actualResult == "":
            self.actualResult = errorMsg
        self.testResult = result

    def setPASS(self,errorMsg = ""):
        self.setResult(ResultConst.PASS,errorMsg)

    def setFAIL(self, errorMsg=""):
        self.setResult(ResultConst.FAIL, errorMsg)

    def setERROR(self, errorMsg=""):
        self.setResult(ResultConst.ERROR, errorMsg)

    def setEXCEPTION(self, errorMsg=""):
        self.setResult(ResultConst.EXCEPTION, errorMsg)

    def updateCalledVarkeyList(self,updateKey):
        if updateKey in self.calledVarsKeyList:
            self.calledVarsKeyList.remove(updateKey)
        self.calledVarsKeyList.append(updateKey)

    def checkAllInfosAfterTest(self):
        self.testResult = (self.testResult == None or  self.testResult == "") and "没有测试结果" or self.testResult
        self.actualResult = (self.actualResult == None or self.actualResult == "") and "没有实际返回结果" or self.actualResult
        self.assertResult = (self.assertResult == None or self.assertResult == "" ) and "没有断言结果" or self.assertResult

        self.varsPre = (self.varsPre == None or self.varsPre.strip() == "") and "无准备数据" or self.varsPre
        self.varsPost = (self.varsPost == None or self.varsPost.strip() == "" ) and "无断言恢复数据" or self.varsPost


    @catch_exception
    def processData(self, dataString):
        """
        处理初始化和恢复的方法。
        Args:
            dataString: 要处理的字符串，比如
                        LOGIN();
                        REDIS();

        Returns:
            处理后的
        """
        dataStringList = splitStringToListByTag(dataString, ";")
        retString = ""
        for i in range(0, len(dataStringList)):
            if dataStringList[i].strip() == "":
                continue
            if dataStringList[i].strip()[0:1] == "#":
                retString += dataStringList[i].strip() + ";\n"
                continue
            tmpValue = dataStringList[i]
            tmpValue = BP.process_branch_IF(tmpValue, self)
            dataStringList[i] = self.processKPWithNoneTag(tmpValue)  # 变量替换，处理keyword
            retString += dataStringList[i].strip() + ";\n"
            if self.testResult in self.exitExecStatusList:
                if self.isRequested == False:
                    self.generateResultWhenNotRequsted()
                return retString[:-1]
        return retString[:-1]

    def setFinalAssertMsg(self):
        """
        设置最终断言结果。
        Returns:
            无
        """
        if self.testResult == ResultConst.PASS:
            self.assertResult = "[%s]: %s\n\n%s" % (ResultConst.PASS,"全部断言通过！",self.assertResult.strip())
        elif self.testResult == ResultConst.FAIL:
            self.assertResult = "[%s]: %s\n\n%s" % (ResultConst.FAIL,"断言失败！",self.assertResult.strip())
        elif self.testResult == ResultConst.ERROR:
            self.assertResult = "[%s]: %s\n\n%s" % (ResultConst.ERROR,"出现ERROR！",self.assertResult.strip())
        elif self.testResult == ResultConst.NOTRUN:
            self.testResult = ResultConst.ERROR
            self.assertResult = "[%s]: %s\n\n%s" % (ResultConst.ERROR, "执行结果是NOTRUN，请反馈给管理员！", self.assertResult.strip())
        elif self.testResult == ResultConst.NO_ASSERT:
            self.testResult = ResultConst.ERROR
            self.assertResult = "[%s]: %s\n\n%s" % (ResultConst.ERROR, "执行结果是NO_ASSERT，没有进行断言，请加入断言！", self.assertResult.strip())
        else:
            self.assertResult = "[%s]: %s\n\n%s" % (ResultConst.EXCEPTION, "结果【%s】异常，请反馈给管理员！" % self.testResult, self.assertResult.strip())
            self.testResult = ResultConst.EXCEPTION

    ###变量 string json dict之间的转换函数
    @catch_exception
    def getVarsKeyListByVarsList(self, varsList):
        """
        通过varsList得到keylist
        Args:
            varsList: 处理过后的varslist，例如
                    ["k1=v1","k2=v2","k3=v3"]

        Returns:
            keyList,例如 ["k1","k2","k3"]
        """
        varsKeyList = []
        varsValueList = []
        for i in range(0, len(varsList)):
            tmpVarKeyValue = varsList[i].strip()
            if tmpVarKeyValue[0:1] == "#":
                #判断属于注释
                tmpkey = "[ANNOTATION]"
                tmpValue = tmpVarKeyValue
                varsKeyList.append(tmpkey.strip())
                varsValueList.append(tmpValue.strip())
            else:
                # 判断是否是关键字开头，如果是关键字开头，进入EXECUTE而不是变量拆分
                isExecuteKeywork = False
                for tmpKeyworkMethodName in kwKeyList:
                    if tmpVarKeyValue.startswith(tmpKeyworkMethodName+"("):
                        # 属于没有key的，只有执行作用，类似于执行前准备。
                        tmpkey = "[EXECUTE]"
                        tmpValue = tmpVarKeyValue
                        if tmpValue.strip() != "":
                            varsKeyList.append(tmpkey.strip())
                            varsValueList.append(tmpValue.strip())
                        isExecuteKeywork = True
                        break
                if isExecuteKeywork == False:
                    #如果内置关键字没有匹配到，看看自定义关键字有没有匹配。
                    selfKwList, selfKwDict = SelfKeywordProcesser.getSelfKeywordDict()
                    for tmpKeyworkMethodName in selfKwList:
                        if tmpVarKeyValue.startswith(tmpKeyworkMethodName+"("):
                            # 属于没有key的，只有执行作用，类似于执行前准备。
                            tmpkey = "[EXECUTE]"
                            tmpValue = tmpVarKeyValue
                            if tmpValue.strip() != "":
                                varsKeyList.append(tmpkey.strip())
                                varsValueList.append(tmpValue.strip())
                            isExecuteKeywork = True
                            break

                # 不是所有类型关键字开头的，然后切割进行判断。
                if isExecuteKeywork == False:
                    tmpVarList = tmpVarKeyValue.split("=")
                    if len(tmpVarList) >= 2:
                        # 合法的key value并且不是#开头的注释语句，加入dict
                        tmpkey = tmpVarList[0].strip()
                        tmpValue = tmpVarList[1].strip()
                        for j in range(2, len(tmpVarList)):
                            tmpValue = tmpValue + "=" + tmpVarList[j]
                        # 结束key 和 value赋值
                        #判断key是否合法。
                        if not VerifyTool.IsVarMatch(tmpkey):
                            self.setERROR("变量key[%s]不合法，只允许大小写字母数字加-_，且只能字母开头！" % tmpkey)
                            return varsKeyList, varsValueList
                        varsKeyList.append(tmpkey.strip())
                        varsValueList.append(tmpValue.strip())
                    elif len(tmpVarList) == 1:
                        # 属于没有key的，只有执行作用，类似于执行前准备。
                        tmpkey = "[EXECUTE]"
                        tmpValue = tmpVarList[0].strip()
                        if tmpValue.strip() != "":
                            varsKeyList.append(tmpkey.strip())
                            varsValueList.append(tmpValue.strip())

        return varsKeyList, varsValueList

    @catch_exception
    def getVarsKeyListByVarsString(self,varsString):
        """
        得到通过varsString得到varkeyList
        Args:
            varsString: 比如
                    k1=v1;
                    k2=v2;
                    k3=v3;

        Returns:
            varskeyList，例如 ["k1","k2","k3"]
        """
        varsList = splitStringToListByTag(varsString,";")
        return self.getVarsKeyListByVarsList(varsList)

    @catch_exception
    def processKPWithNoneTag(self,tmpValue):
        return KP.getProcessedValue(tmpValue, self).replace(self.noneTag, "")

    @catch_exception
    def get_processed_value(self, tmpValue):
        return self.processKPWithNoneTag(tmpValue)

    @catch_exception
    def generateVarsKeyListAndVarsPool(self, varsPreorPost):
        """
        生成变量列表和变量池 varsPool
        Args:
            varsPreorPost: 最初始的未经过任何处理的varsPreorPost,比如varsPre和varsPost。格式如下：
                        [CONF=conmmon]
                        k1=v1;
                        [ENDCONF]
                        [CONF=testenv1]
                        k2=v2;
                        [ENDCONF]

        Returns:
            生成和varsPool。
        """
        # # 从 [CONF=ServiceKey][ENDCONF]中截取对应的变量 如果没有截取到直接返回varsString
        varsString = varsPreorPost.strip()
        varsKeyList, varsValueList = self.getVarsKeyListByVarsString(varsString)
        for i in range(0, len(varsKeyList)):
            tmpKey = varsKeyList[i]
            tmpValue = varsValueList[i]
            # DONE 处理tmpValue，可以使用oldVarsDict中的任意变量，自己输入的;要带转义符
            if tmpKey == "[ANNOTATION]":
                # 是注释，不需要做任何操作。
                # 开始变量处理
                baseTmpKey = "[ANNOTATION]"
                while True:
                    # 循环处理，生成唯一的key
                    tmpKey = baseTmpKey + str(random.randint(1, 9999999)) + genereateAnEnStr(8)  # 产生一个随机数key
                    if tmpKey in self.varsPool.keys():
                        # 如果存在，重新生成
                        tmpKey = baseTmpKey + str(random.randint(1, 9999999)) + genereateAnEnStr(8)  # 产生一个随机数key
                    else:
                        # 不存在退出
                        break
                # 给全局变量池赋值
                self.varsPool[tmpKey] = tmpValue
                self.varsPool[self.getVarkeyPathKey(tmpKey)] = "[%s]" % (self.interfaceId)
                self.updateCalledVarkeyList(tmpKey)
            elif tmpKey == "[EXECUTE]":
                # 只执行，不生成变量。
                pedValue = self.processKPWithNoneTag(tmpValue)
                baseTmpKey = "[EXECUTE]"
                while True:
                    # 循环处理，生成唯一的key
                    tmpKey = baseTmpKey + str(random.randint(1, 9999999)) + genereateAnEnStr(8)  # 产生一个随机数key
                    if tmpKey in self.varsPool.keys():
                        # 如果存在，重新生成
                        tmpKey = baseTmpKey + str(random.randint(1, 9999999)) + genereateAnEnStr(8)  # 产生一个随机数key
                    else:
                        # 不存在退出
                        break
                # 将处理完成的变量加入到oldVarsDict中
                self.varsPool[tmpKey] = "已执行：%s，执行结果:\n%s" % (tmpValue,pedValue if len(pedValue) < 50 else (pedValue[:48]+"..."))
                self.varsPool[self.getVarkeyPathKey(tmpKey)] = "[%s]" % (self.interfaceId)
                self.updateCalledVarkeyList(tmpKey)
            else:
                # 正常变量
                self.setVar(tmpKey,self.processKPWithNoneTag(tmpValue))
                self.updateCalledVarkeyList(tmpKey)

            #如果出错了做什么,停止执行
            if self.testResult in self.exitExecStatusList or ("IS_CONTINUE" in self.varsPool.keys() and self.varsPool["IS_CONTINUE"] == False):
                if self.isRequested == False:
                    self.generateResultWhenNotRequsted()
                return

    @catch_exception
    def generateVarsStringByVarsPoolAndVarsKeyList(self):
        """
        根据varsPool生成当前的变量列表。
        Returns:
            当前变量列表
        """
        retStr = ""
        for tmpKey in self.calledVarsKeyList:
            if tmpKey.startswith("[ANNOTATION]") or tmpKey.startswith("[EXECUTE]"):
                #注释值显示后面部分不显示key：
                retStr += "%s ;(来源：%s)\n" % (str(self.varsPool[tmpKey]).replace(";", "\\;"),self.varsPool[self.getVarkeyPathKey(tmpKey)] if self.getVarkeyPathKey(tmpKey) in self.varsPool.keys() else "无")
            else:
                #不是注释和执行类，正常变量的话
                try:
                    if TypeTool.is_list(self.varsPool[tmpKey]) or TypeTool.is_dict(self.varsPool[tmpKey]):
                        strToBerepalced = json.dumps(self.varsPool[tmpKey])
                    else:
                        strToBerepalced = str(self.varsPool[tmpKey])
                except:
                    strToBerepalced = str(self.varsPool[tmpKey])
                retStr += "%s = %s ;(来源：%s)\n" %(tmpKey,strToBerepalced.replace(";","\\;"),self.varsPool[self.getVarkeyPathKey(tmpKey)] if self.getVarkeyPathKey(tmpKey) in self.varsPool.keys() else "无")
        return retStr.strip()

    def initRequestHostAndResults(self):
        """
                执行前初始化的一些基本信息
                Returns:
                    无。
                """
        self.beforeExecuteTakeTime = 0
        self.afterExecuteTakeTime = 0
        self.executeTakeTime = 0
        self.totalTakeTime = 0
        self.testResult = ResultConst.NO_ASSERT
        self.actualResult = ""
        self.assertResult = ""

    def validate(self):
        pass

    def processVarsstring(self,varsstring):
        # 获取对应的String，判断是纯python模式还是普通模式
        # 纯python模式指的是执行python代码，python代码中可以调用一些函数来达到与平台互通的目的，使用更为高级
        # 普通模式是以平台语法为框架，可以调用python代码。
        varsPreEnvString = varsstring.strip()
        tagStr = varsPreEnvString.split("\n")[0].strip()
        if tagStr.startswith("#") and tagStr.replace("#","").replace(";","").strip() == self.pythonModeStrPrefix:
            return True,BP.process_python_code(varsPreEnvString,self)
        else:
            self.generateVarsKeyListAndVarsPool(varsstring)  # DONE 处理完varsPre，生成对应的varsPool
            return False,""

    def appendPythonModeLog(self,isPythonMode,pythonModeLog):
        if isPythonMode:
            return "\n\n############################################################\npython日志：\n%s" % pythonModeLog
        else:
            return ""

    @catch_exception
    def processBeforeExecute(self):
        logging.debug("○1===traceId[%s]★★★★★" % self.traceId)
        self.initRequestHostAndResults()  # 初始化uri，供全局使用
        logging.debug("○○2===traceId[%s]★★★★★" % self.traceId)

        if self.testResult in self.exitExecStatusList:
            self.assertResult = "处理initRequestHostAndResults时出现错误：\n%s" % self.assertResult
            return False

        self.globalDB.initGlobalDBConf()
        self.globalDB.setCursorDict(False)

        logging.debug("★★★★★★★★★★★★★★★★★★★★★ %s" % self.serviceDBDict)
        if self.serviceDBDict == {}:
            self.initDB()  # 初始化数据库，共全局使用
            logging.debug("○○21===traceId[%s]★★★★★" % self.traceId)

        if self.serviceRedisDict == {}:
            self.initRedis() #初始化redis
            logging.debug("○○22===traceId[%s]★★★★★" % self.traceId)

        if self.serviceMongoDBDict == {}:
            self.initMongoDB() #初始化mongodb
            logging.debug("○○23===traceId[%s]★★★★★" % self.traceId)


        logging.debug("○○○3===traceId[%s]★★★★★" % self.traceId)

        if self.testResult in self.exitExecStatusList:
            # y应该不会出现，出现了就是程序见鬼了
            self.assertResult = "初始化时出现错误或者异常。\n%s" % self.assertResult
            return False
        # DONE 1、验证基本数据
        logging.debug("EXECUTE_HTTP_STEP_1: 验证基本数据。")
        if self.validate() == False:
            self.assertResult = "执行前验证基本数据出现错误或者异常。\n%s" % self.assertResult
            return False
        # DONE pre 先对所有字段进行全局变量和组合文本替换 varsPre uri url method header parmas varsPost
        # 对所有字段进行全局文本处理。
        # 在函数中直接增加了错误信息，不需要继续增加assertResult信息
        if self.testResult in self.exitExecStatusList:
            return False
        # DONE 2、处理varsPool,varsPre  前置变量处理
        # DONE 3、处理变量中的关键字 关键字包括全局变量替换、组合文本替换等。
        logging.debug("EXECUTE_HTTP_STEP_2: 处理[准备]阶段。")
        dataInitStartTime = time.time()
        self.pythonModeExecuteLog = ""
        logging.debug("○○○○4===traceId[%s]★★★★★" % self.traceId)
        self.isPythonModePre,isContinue = self.processVarsstring(self.varsPre)
        logging.debug("○○○○○5===traceId[%s]★★★★★" % self.traceId)

        if self.isPythonModePre:
            self.pythonLogVarsPre = self.pythonModeExecuteLog #TODO 这里是临时方案，这个到时候考虑放到某个地方展示。
            if isContinue == False:
                if self.generateVarsStringByVarsPoolAndVarsKeyList().strip() != "":
                    self.varsPre = self.generateVarsStringByVarsPoolAndVarsKeyList().strip() + self.appendPythonModeLog(self.isPythonModePre,self.pythonLogVarsPre)  # 对生成的varsPool和varKey重新赋值给varsPre
                else:
                    self.varsPre = self.appendPythonModeLog(self.isPythonModePre,self.pythonLogVarsPre).strip()  # 对生成的varsPool和varKey重新赋值给varsPre

                self.checkAllInfosAfterTest()
                return False
        logging.debug("○○○○○○6===traceId[%s]★★★★★" % self.traceId)

        dataInitEndTime = time.time()
        if self.generateVarsStringByVarsPoolAndVarsKeyList().strip() != "":
            self.varsPre = self.generateVarsStringByVarsPoolAndVarsKeyList().strip() + self.appendPythonModeLog(
                self.isPythonModePre, self.pythonLogVarsPre)  # 对生成的varsPool和varKey重新赋值给varsPre
        else:
            self.varsPre = self.appendPythonModeLog(self.isPythonModePre,
                                                    self.pythonLogVarsPre).strip()  # 对生成的varsPool和varKey重新赋值给varsPre

        self.beforeExecuteTakeTime = int((dataInitEndTime - dataInitStartTime) * 1000)
        logging.debug("○○○○○○○7===traceId[%s]★★★★★" % self.traceId)

        if self.testResult in self.exitExecStatusList:
            self.checkAllInfosAfterTest()
            self.assertResult = "%s: 处理[准备]阶段时出现错误：\n%s" % (self.testResult,self.assertResult)
            return False
        return True

    @catch_exception
    def processAfterExecute(self):
        #先处理执行过程中调用的数据
        if self.generateVarsStringByVarsPoolAndVarsKeyList().strip() != "":
            self.varsPre = self.generateVarsStringByVarsPoolAndVarsKeyList().strip() + self.appendPythonModeLog(
                self.isPythonModePre, self.pythonLogVarsPre)  # 对生成的varsPool和varKey重新赋值给varsPre
        else:
            self.varsPre = self.appendPythonModeLog(self.isPythonModePre,
                                                    self.pythonLogVarsPre).strip()  # 对生成的varsPool和varKey重新赋值给varsPre
        #生成之后开始处理后置
        self.calledVarsKeyList = []
        self.pythonModeExecuteLog = ""
        # DONE 7、处理varsPool varsPost处理后置变量
        # DONE 8、处理varsPool中的关键字
        logging.debug("EXECUTE_HTTP_STEP_6: 处理[断言恢复]阶段。")
        dataRecoverStartTime = time.time()
        self.isPythonModePost, isContinue = self.processVarsstring(self.varsPost)
        if self.isPythonModePost:
            self.pythonLogVarsPost = self.pythonModeExecuteLog  # TODO 这里是临时方案，这个到时候考虑放到某个地方展示。
            if isContinue == False:
                if self.generateVarsStringByVarsPoolAndVarsKeyList().strip() != "":
                    self.varsPost = self.generateVarsStringByVarsPoolAndVarsKeyList() + self.appendPythonModeLog(self.isPythonModePost,self.pythonLogVarsPost) # 对生成的varsPool和varKey重新赋值给varsPre
                else:
                    self.varsPost = self.appendPythonModeLog(self.isPythonModePost,self.pythonLogVarsPost).strip() # 对生成的varsPool和varKey重新赋值给varsPre

                self.checkAllInfosAfterTest()
                return False

        if self.generateVarsStringByVarsPoolAndVarsKeyList().strip() != "":
            self.varsPost = self.generateVarsStringByVarsPoolAndVarsKeyList() + self.appendPythonModeLog(
                self.isPythonModePost, self.pythonLogVarsPost)  # 对生成的varsPool和varKey重新赋值给varsPre
        else:
            self.varsPost = self.appendPythonModeLog(self.isPythonModePost,
                                                     self.pythonLogVarsPost).strip()  # 对生成的varsPool和varKey重新赋值给varsPre

        self.setFinalAssertMsg()
        # DONE 10、处理数据恢复中的变量替换、关键字处理
        logging.debug("EXECUTE_HTTP_STEP_8: 处理现场恢复。")
        dataRecoverEndTime = time.time()
        self.afterExecuteTakeTime = int((dataRecoverEndTime - dataRecoverStartTime) * 1000)
        self.totalTakeTime = self.beforeExecuteTakeTime + self.executeTakeTime + self.afterExecuteTakeTime
        self.checkAllInfosAfterTest()
        return True

    def getVarkeyPathKey(self,varkey):
        return "PaTh-_-%s" % varkey

    def setVar(self,varkey,value):
        if not VerifyTool.IsVarMatch(varkey) :
            #如果不是合法的varkey和value，讲不设置到变量池。
            self.setERROR("<ERROR:不合法的变量key[%s]>" % varkey)
            return
        if not VerifyTool.IsValidVarValue(value):
            self.setERROR("<ERROR:不合法的变量value类型[%s],可赋值类型：int/float/str/dict/list>" % type(value))
            return
        pathVarkey = self.getVarkeyPathKey(varkey)
        historyPath = ""
        valueSub = str(value) if len(str(value)) < 20 else str(value)[:19]+"..."
        currentPath = "[%s:%s]" % (self.interfaceId, valueSub)
        if varkey in self.varsPool.keys():
            if varkey in ["VAR","retStr"]:
                #EXEC_PYTHON的变量池，旧版。什么也不用做。
                return
            if varkey in ["DEBUG_MODE","IS_CONTINUE","context","ASSERT_MODE"]:
                #不用设置Path，因为是pythonmode的三个常量，都是当前生效。
                self.varsPool[varkey] = value
                return
            if self.varsPool[varkey] == value:
                #不用设置，变量池中的跟当前的一致
                if pathVarkey not in self.varsPool.keys():
                    self.varsPool[pathVarkey] = currentPath
                return
            if pathVarkey in self.varsPool.keys():
                historyPath = self.varsPool[pathVarkey]

        hisPathList = historyPath.split("->")
        if historyPath != "":
            if len(hisPathList) >= 2:
                thisPath = "%s->%s->%s" % (hisPathList[-2], hisPathList[-1], currentPath)
            else:
                thisPath = "%s->%s" % (hisPathList[-1], currentPath)
        else:
            thisPath = currentPath
        self.varsPool[varkey] =value
        self.varsPool[pathVarkey] = thisPath

    def getRequestAddr(self,uriKey):
        with DBTool() as tmpdb:
            reqAddr = tmpdb.execute_sql("select requestAddr from tb_env_uri_conf where httpConfKey='%s' and uriKey='%s'" % (self.confHttpLayer.key,uriKey))
        if reqAddr:
            return reqAddr[0]['requestAddr']
        else:
            return ""

    def get_python_mode_buildIn_functions(self):
        return getPythonThirdLib() + "\n" + getPythonModeBuildInFromScriptFile()

    def processExecuteAttrAndRun(self,whetherSetResult = True):
        pass

    def transferAttrsFrom1Pto2P(self,param1,param2,isTrans_calledInterfaceRecurDict = False):
        # 执行前全局属性传递,需要回传
        param2.current_session = param1.current_session
        param2.kw_LOGIN_ParamList = param1.kw_LOGIN_ParamList
        # 不需要回传
        param2.highPriorityVARSStr = param1.highPriorityVARSStr
        param2.highPriorityVARSDict = param1.highPriorityVARSDict
        # 传递整个变量池varsPool
        param2.varsPool = param1.varsPool
        param2.httpConfKey = param1.httpConfKey
        param2.confHttpLayer = param1.confHttpLayer

        param2.context_data_list = param1.context_data_list
        param2.context_data_dict = param1.context_data_dict

        param2.serviceDBDict = param1.serviceDBDict
        param2.serviceRedisDict = param1.serviceRedisDict
        param2.serviceMongoDBDict = param1.serviceMongoDBDict

        param2.serviceMongoDBDict = param1.serviceMongoDBDict
        param2.serviceMongoDBDict = param1.serviceMongoDBDict
        param2.serviceMongoDBDict = param1.serviceMongoDBDict

        if isTrans_calledInterfaceRecurDict:
            param2.calledInterfaceRecurDict = param1.calledInterfaceRecurDict

    def updateVarWhichNoPath(self):
        #更新没有Path的varkey，重要是一些python模式执行时没有设置varkeyPath的python变量
        varsPoolCurrentKeysList = deepcopy(list(self.varsPool.keys()))
        for tmpKey in varsPoolCurrentKeysList:
            if tmpKey in ["VAR", "retStr","DEBUG_MODE", "IS_CONTINUE", "context", "ASSERT_MODE"]:
                continue
            if not tmpKey.startswith("PaTh-_-") and VerifyTool.IsVarMatch(tmpKey) and VerifyTool.IsValidVarValue(self.varsPool[tmpKey]):
                self.setVar(tmpKey,self.varsPool[tmpKey])
                #这里没有想好，如果是python模式中的变量，但是没有被引用过，要不要暴露出来？
                self.updateCalledVarkeyList(tmpKey)



