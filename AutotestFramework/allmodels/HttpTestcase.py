from allmodels.HttpTestcaseStep import HttpTestcaseStep
from core.const.GlobalConst import CaseLevel
from core.const.GlobalConst import CaseStatus
from core.const.GlobalConst import CaseTypeConst
from core.const.GlobalConst import ExecStatus
from core.const.GlobalConst import PerformanceConst
from core.const.GlobalConst import TestCaseStepSwitch
from core.decorator.normal_functions import *
from core.tools.DBTool import DBTool
from core.tools.CommonFunc import *
from core.model.CommonAttr import CommonAttr
import requests
from core.const.GlobalConst import ObjTypeConst
from core.config.InitConfig import *

class HttpTestcase(CommonAttr):
    """
    HTTP用例类
    """
    def __init__(self,id = 0, caseId = "", caseDebugId = 0,caseStepDebugId = 0):
        super(HttpTestcase, self).__init__()
        self.objType = ObjTypeConst.TESTCASE

        self.id = id
        self.caseId = caseId
        self.caseDebugId = caseDebugId
        self.caseStepDebugId = caseStepDebugId
        self.title = ""
        self.desc = ""
        self.businessLineId = 0
        self.moduleId = 0
        self.caseLevel = CaseLevel.MIDIUM
        self.status = CaseStatus.UN_AUDIT
        self.stepCount = 0
        self.caseType = CaseTypeConst.GROUP
        self.stepTestcaseList = [] #HttpTestcaseStep的列表

        self.protocol = "HTTP"

        self.execStatus = ExecStatus.NOTRUN
        self.assertResult = "" #断言结果
        self.testResult = ResultConst.NOTRUN #测试结果
        self.testcasePerformanceResult = PerformanceConst.NA

        self.beforeExecuteTakeTime = 0.0
        self.afterExecuteTakeTime = 0.0
        self.executeTakeTime = 0.0
        self.totalTakeTime = 0.0

        self.state = 1
        self.addBy = ""
        self.modBy = ""
        self.addTime = ""
        self.modTime = ""


    @take_time
    def execute(self):
        """
        执行用例
        Returns:
            无
        """
        logging.debug("****************************************用例TESTCASE[%s]开始执行在环境[%s]执行人[%s]***********************************************" % (self.caseId,self.confHttpLayer.key,self.addBy))
        for i in range(0,len(self.stepTestcaseList)):
            #执行步骤前传递变量等
            self.transferAttrsFrom1Pto2P(self,self.stepTestcaseList[i],isTrans_calledInterfaceRecurDict=True)
            self.stepTestcaseList[i].interfaceId = "%s-%s" % (self.caseId, self.stepTestcaseList[i].stepNum)
            # 执行步骤
            self.stepTestcaseList[i].executeStep()
            #执行步骤后的信息传递给
            self.transferAttrsFrom1Pto2P(self.stepTestcaseList[i],self,isTrans_calledInterfaceRecurDict=True)

            if self.stepTestcaseList[i].testResult != ResultConst.PASS:
                #当前步骤测试未通过,那么退出循环,不执行后续步骤.
                break

        # 根据个步骤执行结果给Testcase赋值
        self.execStatus = ExecStatus.DONE
        self.assertResult = ""
        self.testResult = ResultConst.NOTRUN #测试结果

        self.beforeExecuteTakeTime = 0
        self.afterExecuteTakeTime = 0
        self.executeTakeTime = 0
        self.totalTakeTime = 0
        self.testcasePerformanceResult = PerformanceConst.PASS
        #记录有没有性能时间超出

        for tmpStepIndex in range(0,len(self.stepTestcaseList)):
            tmpStepResult = self.stepTestcaseList[tmpStepIndex]
            self.beforeExecuteTakeTime += tmpStepResult.beforeExecuteTakeTime
            self.afterExecuteTakeTime += tmpStepResult.afterExecuteTakeTime
            self.executeTakeTime += tmpStepResult.executeTakeTime
            self.totalTakeTime += tmpStepResult.totalTakeTime

            self.testResult = tmpStepResult.testResult
            if tmpStepResult.testResult == ResultConst.PASS:
                self.assertResult = "[%s]所有步骤测试通过。" % ResultConst.PASS
                if not performanceTime(tmpStepResult.executeTakeTime,tmpStepResult.performanceTime):
                    self.testcasePerformanceResult = PerformanceConst.FAIL


                continue
            elif tmpStepResult.testResult == ResultConst.FAIL:
                self.assertResult = "[%s]步骤[%s]失败。" % (ResultConst.FAIL,tmpStepResult.stepNum)
                self.testcasePerformanceResult = PerformanceConst.NA
                break
            elif tmpStepResult.testResult == ResultConst.ERROR:
                self.assertResult = "[%s]步骤[%s]发生错误。" % (ResultConst.ERROR,tmpStepResult.stepNum)
                self.testcasePerformanceResult = PerformanceConst.NA
                break
            elif tmpStepResult.testResult == ResultConst.EXCEPTION:
                self.assertResult = "[%s]步骤[%s]发生异常。" % (ResultConst.EXCEPTION,tmpStepResult.stepNum)
                self.testcasePerformanceResult = PerformanceConst.NA
                break
            elif tmpStepResult.testResult == ResultConst.NOTRUN:
                self.testResult = ResultConst.EXCEPTION
                self.assertResult = "[%s]步骤[%s]未执行。" % (ResultConst.NOTRUN,tmpStepResult.stepNum)
                self.testcasePerformanceResult = PerformanceConst.NA
                break
            else:
                self.assertResult = "步骤[%s]不识别的执行结果！[%s]。" % (tmpStepResult.stepNum,self.testResult)
                self.testcasePerformanceResult = PerformanceConst.NA
                break
        logging.debug("****************************************用例[%s]结束执行***********************************************%s" % (self.caseId,self.testcasePerformanceResult))

    @catch_exception
    def generateByCaseDebugIdAndCaseStepDebugIdList(self,caseDebugId="", caseStepDebugIdList=[]):
        """
        通过caseDebugId和caseStepDebugIdList获取要测试的用例
        Args:
            caseDebugId: tb_http_testcase_debug中的id
            caseStepDebugIdList:tb_http_testcase_step_debug中的id LIST

        Returns:
            无
        """
        # sqlCaseDebug = "select * from tb_http_testcase_debug where id = %d" % int(caseDebugId)
        # logging.debug(sqlCaseDebug)
        # self.globalDB.initGlobalDBConf()
        # resCaseDebug = self.globalDB.execute_sql(sqlCaseDebug)
        # self.globalDB.release()
        # logging.debug(resCaseDebug)
        # if resCaseDebug:
        #     caseDebugInfo = resCaseDebug[0]
        #     self.id = caseDebugInfo['id']
        #     self.caseId = caseDebugInfo['caseId']
        #     self.caseDebugId = caseDebugInfo['id']
        #     self.title = caseDebugInfo['title']
        #     self.desc = caseDebugInfo['casedesc']
        #     self.stepCount = caseDebugInfo['stepCount']
        #
        #     self.version = caseDebugInfo['version'].strip()
        #
        #     self.state = caseDebugInfo['state']
        #     self.addBy = caseDebugInfo['addBy']
        #     self.modBy = caseDebugInfo['modBy']
        #     self.addTime = caseDebugInfo['addTime']
        #     self.modTime = caseDebugInfo['modTime']
        #
        #     self.confHttpLayer.key = caseDebugInfo['httpConfKey']
        #     self.confHttpLayer.generate_http_conf_by_key()
        self.serviceRedis.initRedisConf()
        caseDebugInfo = json.loads(str(self.serviceRedis.get_data(caseDebugId)))
        if caseDebugInfo["execStatus"] == 1:
            self.caseId = caseDebugInfo['caseId']
            self.caseDebugId = caseDebugId
            self.caseStepDebugId = caseStepDebugIdList
            self.title = caseDebugInfo['title']
            self.desc = caseDebugInfo['casedesc']
            self.stepCount = caseDebugInfo['stepCount']
            self.version = caseDebugInfo['version'].strip()
            self.execStatus = caseDebugInfo['execStatus']
            # self.state = caseDebugInfo['state']
            # self.addBy = caseDebugInfo['addBy']
            # self.modBy = caseDebugInfo['modBy']
            # self.addTime = caseDebugInfo['addTime']
            # self.modTime = caseDebugInfo['modTime']
            self.confHttpLayer.key = caseDebugInfo['httpConfKey']
            self.confHttpLayer.generate_http_conf_by_key()

        caseStepDebugIdList = json.loads(self.serviceRedis.get_data(caseStepDebugIdList))

        for tmpStepDebugId in caseStepDebugIdList:
            if int(tmpStepDebugId["stepSwitch"]) == TestCaseStepSwitch.USE_SWITCH:
                httpCaseStep = HttpTestcaseStep()
                # httpCaseStep.id = tmpStepDebugId
                httpCaseStep.caseStepDebugData = tmpStepDebugId
                httpCaseStep.generateByCaseStepDebugData()

                httpCaseStep.confHttpLayer = self.confHttpLayer
                self.addStep(httpCaseStep)

    @catch_exception
    def addStep(self,stepCase = HttpTestcaseStep()):
        """
        添加步骤
        Args:
            stepCase: 要添加的step对象

        Returns:
            无
        """
        if type(stepCase) == type(HttpTestcaseStep()):
            self.stepTestcaseList.append(stepCase)

    @catch_exception
    def updateByCaseDebugId(self):
        """
        根据id更新tb_http_testcase_debug表的测试结果，包括步骤结果
        Returns:
            无。
        """
        self.serviceRedis.initRedisConf()
        testCaseDebugData = json.loads(self.serviceRedis.get_data(self.caseDebugId))

        #根据Testcase信息更新数据库
        # colstr = "id, httpConfKey, serviceConfKey, alias, httpConfDesc, httpConf, state, addBy, modBy, addTime, modTime"
        # sql = """ UPDATE tb_http_testcase_debug SET testResult='%s',assertResult='%s',
        #         beforeExecuteTakeTime=%d,afterExecuteTakeTime=%d, executeTakeTime=%d, totalTakeTime=%d, execStatus = 3,modTime='%s' WHERE id=%d""" \
        #             % (replacedForIntoDB(self.testResult),replacedForIntoDB(self.assertResult),
        #                int(self.beforeExecuteTakeTime),int(self.afterExecuteTakeTime),int(self.executeTakeTime),int(self.totalTakeTime),get_current_time(),self.caseDebugId)
        # self.globalDB.initGlobalDBConf()
        # res = self.globalDB.execute_sql(sql)
        # self.globalDB.release()
        testCaseDebugData["testResult"] = self.testResult
        testCaseDebugData["assertResult"] = self.assertResult
        testCaseDebugData["beforeExecuteTakeTime"] = self.beforeExecuteTakeTime
        testCaseDebugData["afterExecuteTakeTime"] = self.afterExecuteTakeTime
        testCaseDebugData["executeTakeTime"] = self.executeTakeTime
        testCaseDebugData["totalTakeTime"] = self.totalTakeTime
        testCaseDebugData["execStatus"] = 3

        testCaseStepDebugDataList = []
        # 更新各个步骤的结果
        for tmpCaseStepDebug in self.stepTestcaseList:
            tmpCaseStepDebug.updateByStepDebugId()
            testCaseStepDebugDataList.append(tmpCaseStepDebug.caseStepDebugData)
        self.serviceRedis.set_data(self.caseStepDebugId,json.dumps(testCaseStepDebugDataList),60*60)
        self.serviceRedis.set_data(self.caseDebugId,json.dumps(testCaseDebugData),60*60)
        tcpStr = '{"do":10,"CaseDebugId":"%s","protocol":"%s"}' % (self.caseDebugId, self.protocol)
        if sendTcp(TcpServerConf.ip, TcpServerConf.port, tcpStr):
            logging.info("%s 调试完毕通知主服务成功" % self.caseDebugId)
        else:
            logging.info("%s 调试完毕通知主服务失败" % self.caseDebugId)
    @catch_exception
    def generateByCaseId(self):
        """
        通过caseId获取testcase对象。
        Returns:
            无
        """
        tmpCaseId = self.caseId
        sqlGetCase = "select * from tb_http_testcase where caseId='%s' and state = 1" % tmpCaseId
        # logging.debug(sqlGetCase)
        self.globalDB.initGlobalDBConf()
        resCaseResult = self.globalDB.execute_sql(sqlGetCase)
        if resCaseResult:
            resCase = resCaseResult[0]
            self.id = int(resCase['id'])
            self.title = resCase['title']
            self.desc = resCase['casedesc']
            self.businessLineId = resCase['businessLineId']
            self.moduleId = resCase['moduleId']
            self.caseLevel = resCase['caselevel']
            self.status = resCase['status']
            self.stepCount = resCase['stepCount']

            self.state = resCase['state']
            self.addBy = resCase['addBy']
            self.modBy = resCase['modBy']
            self.addTime = resCase['addTime']
            self.modTime = resCase['modTime']

            self.execStatus = ExecStatus.NOTRUN
            self.assertResult = "" #断言结果
            self.testResult = ResultConst.NOTRUN #测试结果

            self.beforeExecuteTakeTime = 0.0
            self.afterExecuteTakeTime = 0.0
            self.executeTakeTime = 0.0
            self.totalTakeTime = 0.0

            self.caseType = CaseTypeConst.GROUP
            self.stepTestcaseList = [] #HttpTestcaseStep的列表

            #生成步骤
            sqlGetStep = "select * from tb_http_testcase_step where caseId='%s' and state=1 order by stepNum asc" % tmpCaseId
            resCaseStep = self.globalDB.execute_sql(sqlGetStep)

            # logging.debug("caseStepsFromDB:%s" % resCaseStep)
            for tmpCaseStepDict in resCaseStep:
                tmpHttpCaseStep = HttpTestcaseStep()
                tmpHttpCaseStep.confHttpLayer = self.confHttpLayer
                tmpHttpCaseStep.generateByStepDict(tmpCaseStepDict)
                self.addStep(tmpHttpCaseStep)
        self.globalDB.release()

    @catch_exception
    def generateByCaseDict(self,caseDict,stepList):
        """
        通过caseId获取testcase对象。
        Returns:
            无
        """

        resCase = caseDict

        self.id = int(resCase['id'])
        self.caseId = resCase['caseId']
        self.title = resCase['title']
        self.desc = resCase['casedesc']
        self.businessLineId = resCase['businessLineId']
        self.moduleId = resCase['moduleId']
        self.caseLevel = resCase['caselevel']
        self.status = resCase['status']
        self.stepCount = resCase['stepCount']

        self.state = resCase['state']
        self.addBy = resCase['addBy']
        self.modBy = resCase['modBy']
        self.addTime = resCase['addTime']
        self.modTime = resCase['modTime']
        self.version = resCase['version']
        self.execStatus = ExecStatus.NOTRUN
        self.assertResult = "" #断言结果
        self.testResult = ResultConst.NOTRUN #测试结果

        self.beforeExecuteTakeTime = 0.0
        self.afterExecuteTakeTime = 0.0
        self.executeTakeTime = 0.0
        self.totalTakeTime = 0.0


        self.caseType = CaseTypeConst.GROUP
        self.stepTestcaseList = [] #HttpTestcaseStep的列表

        # logging.debug("caseStepsFromDB:%s" % resCaseStep)
        for tmpCaseStepDict in stepList:
            tmpHttpCaseStep = HttpTestcaseStep()
            tmpHttpCaseStep.confHttpLayer = self.confHttpLayer
            tmpHttpCaseStep.generateByStepDict(tmpCaseStepDict)
            self.addStep(tmpHttpCaseStep)


