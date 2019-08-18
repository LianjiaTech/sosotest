import requests
from copy import deepcopy
from core.const.GlobalConst import ExecStatus,testLevelConst
from core.decorator.normal_functions import *
from core.model.ConfHttpLayer import ConfHttpLayer
from core.tools.CommonFunc import *
from core.processor.VP import VP
from core.tools.DBTool import DBTool
from core.model.CommonAttr import CommonAttr
from core.const.GlobalConst import ObjTypeConst
class DubboTaskBase(CommonAttr):
    """
    任务表，包括任务执行，报告生成等。
    """
    def __init__(self):
        super(DubboTaskBase, self).__init__()
        self.objType = ObjTypeConst.TASK
        self.taskExecuteId = 0
        self.taskSuiteExecuteId = 0

        self.interfaceCount = 0
        self.taskInterfaces = ""
        self.caseCount = 0
        self.taskCases = ""

        self.isSendEmail = 0
        self.isCodeRate = 0
        self.isSaveHistory = 0
        self.execComments = ""
        self.execType = ""
        self.execTime = ""
        self.execFinishTime = ""
        self.execBy = ""
        self.execStatus = ExecStatus.NOTRUN
        self.execProgressData = "" # ALL:PASS:FAIL:ERROR:NOTRUN
        self.execPlatform = ""
        self.execLevel = 5

        self.testResult = ResultConst.NOTRUN
        self.testResultMsg = ""
        self.testReportUrl = ""
        self.testReportFilePath = ""

        self.state = 1
        self.addBy = ""
        self.modBy = ""
        self.addTime = ""
        self.modTime = ""

        self.taskTestcaseList = []
        self.taskInterfaceList = []
        #接口执行统计
        self.actualTotalInterfaces = 0
        self.interfacePassCount = 0
        self.interfaceFailCount = 0
        self.interfaceErrorCount = 0
        self.interfaceNorunCount = 0
        self.interfaceNotRunLevelCount = 0
        self.actualInterfaceExecuteSummayDict = {"total": 0, "pass": 0, "fail": 0, "error": 0,"notrun": 0,"notrunlevel":0}
        #用例执行统计
        self.actualTotalTestcases = 0
        self.testcasePassCount = 0
        self.testcaseFailCount = 0
        self.testcaseErrorCount = 0
        self.testcaseNorunCount = 0
        self.testcaseNotRunLevelCount = 0
        self.actualTestcaseExecuteSummayDict = {"total": 0, "pass": 0, "fail": 0, "error": 0,"notrun": 0,"notrunlevel":0}
        #用例中的步骤执行统计
        self.actualTotalTestcaseSteps = 0
        self.testcaseStepPassCount = 0
        self.testcaseStepFailCount = 0
        self.testcaseStepErrorCount = 0
        self.testcaseStepNorunCount = 0
        self.testcaseStepExceptionCount = 0
        self.testcaseStepNotRunLevelCount = 0
        self.actualTestcaseStepExecuteSummayDict = {"total": 0, "pass": 0, "fail": 0, "error": 0,"notrun": 0,"norrunlevel":0}

        self.actualTotal = 0
        self.passCount = 0
        self.failCount = 0
        self.errorCount = 0
        self.norunCount = 0
        self.notRunLevelCount = 0
        self.actualTotalExecuteSummayDict = {"total": 0, "pass": 0, "fail": 0, "error": 0,"notrun": 0,"norrunlevel":0}

        self.errorIdList = []
        self.taskExecTakeTime = 0.0

        self.interfaceCountDict = {}
        self.testcaseStepInterfaceCountDict = {}
        self.totalInterfaceCountDict = {}


    @take_time
    def execute(self):
        """
        任务执行
        Returns:
            无
        """
        try:
            logging.debug("$$$$$$$$$$$TaskBase.py###在环境httpConfKey[%s]执行人[%s]$$$$$$$$$$$$$" % (self.httpConfKey, self.addBy))
            taskStartTime = time.time()

            self.initTaskBeforeExecute()
            #把初始进度写进缓存
            self.updateExecutePorgressData()
            #开始执行接口
            self.executeInterfaces()
            #开始执行用例
            self.executeTestcases()
            #生成统计dict
            self.generateAllExecuteSummaryDicts()
            #生成整体接口统计
            self.generateTotalInterfaceCountDict()
            taskEndTime = time.time()
            self.taskExecTakeTime = int(taskEndTime - taskStartTime) #获取任务执行时长
            self.execFinishTime = get_current_time() #得到任务执行完成时间
            # 分析结果 PASS FAIL MESSAGE
            self.analyzeTestResults()
        except Exception as e:
            logging.debug(traceback.format_exc())
        finally:
            self.globalDB.release() #最终释放连接
            logging.debug("$$$$$$$$$$$$$$TaskBase.py####结束执行$$$$$$$$$$$$$$$$$$$$$$$$" )

    @catch_exception
    def initTaskBeforeExecute(self):
        """
        任务执行前初始化数据
        Returns:
            无
        """
        self.globalDB.initGlobalDBConf() #先初始化数据库

        # 初始化任务执行接口的情况 数据统计
        self.actualTotalInterfaces = len(self.taskInterfaceList)
        self.interfacePassCount = 0
        self.interfaceFailCount = 0
        self.interfaceErrorCount = 0
        self.interfaceNorunCount = self.actualTotalInterfaces

        self.actualTotalTestcases = len(self.taskTestcaseList)
        self.testcasePassCount = 0
        self.testcaseFailCount = 0
        self.testcaseErrorCount = 0
        self.testcaseNorunCount = self.actualTotalTestcases

        self.actualTotal = self.actualTotalInterfaces + self.actualTotalTestcases
        self.passCount = 0
        self.failCount = 0
        self.errorCount = 0
        self.norunCount = self.actualTotal

        # 执行总结果初始化
        self.testResult = ResultConst.NOTRUN
        self.testResultMsg = ""
        self.testReportUrl = ""

        #生成高优先级变量dict
        self.globalDB.setCursorDict(False)
        self.highPriorityVARSDict = VP.generateHighPriorityVARSDict(self.highPriorityVARSStr,self)
        self.globalDB.setCursorDict(True)
        for k,v in self.highPriorityVARSDict.items():
            self.highPriorityVARSFinalStr += ("%s = %s ;\n" % (k,v))


    @catch_exception
    def executeInterfaces(self):
        """
        执行任务所有接口
        Returns:
            无
        """
        for i in range(0,len(self.taskInterfaceList)):
            if self.caseLevel != testLevelConst.RUNALL and self.taskInterfaceList[i].level > self.caseLevel:
                self.taskInterfaceList[i].assertResult = "优先级未覆盖，跳过运行"
                self.notRunLevelCount += 1
                self.actualTotal -= 1

                self.interfaceNorunCount -= 1
                self.interfaceNotRunLevelCount += 1
                self.actualTotalInterfaces -= 1
                self.taskInterfaceList[i].testResult = ResultConst.NOTRUNLEVEL
                continue

            if self.retryCount > 0:
                bakedInterfaceCase = deepcopy(self.taskInterfaceList[i])

            self.transferAttrsFrom1Pto2P(self,self.taskInterfaceList[i])
            #开始执行接口
            self.taskInterfaceList[i].executeInterface()
            self.transferAttrsFrom1Pto2P(self.taskInterfaceList[i],self)

            tmpInterfaceDictKey =  "%s_%s.%s" % (self.taskInterfaceList[i].dubboSystem,self.taskInterfaceList[i].dubboService,self.taskInterfaceList[i].dubboMethod)

            #结果分析和处理
            if tmpInterfaceDictKey not in self.interfaceCountDict.keys():
                tmpInterface = self.taskInterfaceList[i]
                requestHost = "%s[%s:%s]" % (tmpInterface.dubboSystem,tmpInterface.dubboTelnetHost,tmpInterface.dubboTelnetPort)
                interfaceStr = "%s.%s" % (tmpInterface.dubboService,tmpInterface.dubboMethod)
                self.interfaceCountDict[tmpInterfaceDictKey] = {"total":0,"pass":0,"fail":0,"error":0,"exception":0,"notrun":0, "requestHost":requestHost,"interfaceStr":interfaceStr }

            if self.interfaceCountDict[tmpInterfaceDictKey]['requestHost'].strip() == "" and self.taskInterfaceList[i].dubboSystem.strip() != "":
                self.interfaceCountDict[tmpInterfaceDictKey]['requestHost'] = self.taskInterfaceList[i].dubboSystem.strip()

            if self.taskInterfaceList[i].testResult != ResultConst.NOTRUN:
                self.interfaceCountDict[tmpInterfaceDictKey]['total'] += 1

            if self.taskInterfaceList[i].testResult == ResultConst.PASS or self.taskInterfaceList[i].testResult == ResultConst.NO_ASSERT:
                self.passCount += 1
                self.norunCount -= 1
                self.interfacePassCount += 1
                self.interfaceNorunCount -= 1
                self.interfaceCountDict[tmpInterfaceDictKey]['pass'] += 1
            elif self.taskInterfaceList[i].testResult == ResultConst.FAIL:
                self.failCount += 1
                self.norunCount -= 1
                self.interfaceFailCount += 1
                self.interfaceNorunCount -= 1
                self.interfaceCountDict[tmpInterfaceDictKey]['fail'] += 1
            elif self.taskInterfaceList[i].testResult == ResultConst.ERROR:
                self.errorCount += 1
                self.norunCount -= 1
                self.interfaceErrorCount += 1
                self.interfaceNorunCount -= 1
                self.interfaceCountDict[tmpInterfaceDictKey]['error'] += 1
                if self.taskInterfaceList[i].interfaceId not in self.errorIdList:
                    self.errorIdList.append(self.taskInterfaceList[i].interfaceId)
            elif self.taskInterfaceList[i].testResult == ResultConst.EXCEPTION:
                self.errorCount += 1
                self.norunCount -= 1
                self.interfaceErrorCount += 1
                self.interfaceNorunCount -= 1
                self.interfaceCountDict[tmpInterfaceDictKey]['exception'] += 1
                if self.taskInterfaceList[i].interfaceId not in self.errorIdList:
                    self.errorIdList.append(self.taskInterfaceList[i].interfaceId)
            elif self.taskInterfaceList[i].testResult == ResultConst.NOTRUN:
                self.interfaceCountDict[tmpInterfaceDictKey]['notrun'] += 1
                logging.debug("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE接口执行后结果是NOTRUN。EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
            else:
                logging.debug("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE接口执行后结果不合法。EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")


            if self.retryCount > 0 and self.taskInterfaceList[i].testResult != ResultConst.PASS:
                #进入重试
                for retryIndex in range(0,self.retryCount):
                    currentExecuteInterface = deepcopy(bakedInterfaceCase)
                    self.transferAttrsFrom1Pto2P(self,currentExecuteInterface)
                    # 开始执行接口
                    currentExecuteInterface.executeInterface()
                    self.transferAttrsFrom1Pto2P(currentExecuteInterface,self)
                    self.taskInterfaceList[i].retryList.append(currentExecuteInterface)

            self.updateExecutePorgressData()


    @catch_exception
    def executeTestcases(self):
        """
        执行任务所有用例
        Returns:
            无
        """
        for i in range(0,len(self.taskTestcaseList)):
            if self.caseLevel != testLevelConst.RUNALL and self.taskTestcaseList[i].caseLevel > self.caseLevel:
                self.taskTestcaseList[i].assertResult = "优先级未覆盖，跳过运行"
                self.taskTestcaseList[i].testResult = ResultConst.NOTRUNLEVEL
                self.testcaseNotRunLevelCount += 1
                self.testcaseNorunCount -= 1
                self.actualTotalTestcases -= 1

                for stepIndex in self.taskTestcaseList[i].stepTestcaseList:
                    stepIndex.testResult = ResultConst.NOTRUNLEVEL
                    stepIndex.assertResult = "优先级未覆盖，跳过运行"
                    self.notRunLevelCount += 1
                    self.actualTotal -= 1

                    self.testcaseStepNorunCount -= 1
                    self.testcaseStepNotRunLevelCount += 1
                    self.actualTotalTestcaseSteps -= 1
                continue

            if self.retryCount > 0:
                bakedCase = deepcopy(self.taskTestcaseList[i])

            #执行前全局属性传递，需要回传
            self.transferAttrsFrom1Pto2P(self,self.taskTestcaseList[i])
            #开始执行
            logging.debug("###########执行用例序号[%d]环境httpConfKey[%s]#########" % ((i + 1),self.taskTestcaseList[i].confHttpLayer.key))
            self.taskTestcaseList[i].execute()
            self.transferAttrsFrom1Pto2P(self.taskTestcaseList[i],self)


            #处理直接结果
            if self.taskTestcaseList[i].testResult == ResultConst.PASS:
                self.passCount += 1
                self.norunCount -= 1
                self.testcasePassCount += 1
                self.testcaseNorunCount -= 1
            elif self.taskTestcaseList[i].testResult == ResultConst.FAIL:
                self.failCount += 1
                self.norunCount -= 1
                self.testcaseFailCount += 1
                self.testcaseNorunCount -= 1
            elif self.taskTestcaseList[i].testResult == ResultConst.ERROR:
                self.errorCount += 1
                self.norunCount -= 1
                self.testcaseErrorCount += 1
                self.testcaseNorunCount -= 1
                if self.taskTestcaseList[i].caseId not in self.errorIdList:
                    self.errorIdList.append(self.taskTestcaseList[i].caseId)
            elif self.taskTestcaseList[i].testResult == ResultConst.EXCEPTION:
                self.errorCount += 1
                self.norunCount -= 1
                self.testcaseErrorCount += 1
                self.testcaseNorunCount -= 1
                if self.taskTestcaseList[i].caseId not in self.errorIdList:
                    self.errorIdList.append(self.taskTestcaseList[i].caseId)
            elif self.taskTestcaseList[i].testResult == ResultConst.NOTRUN:
                logging.debug("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE用例执行后结果是NOTRUN。EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
            else:
                logging.debug("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE用例执行后结果不合法。EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")

            #对用例步骤进行分析，抽取接口测试结果              #用例步骤执行信息统计 TestcaseStep统计
            for tmpStep in self.taskTestcaseList[i].stepTestcaseList:
                tmpStepDictKey =  "%s_%s.%s" % (tmpStep.dubboSystem,tmpStep.dubboService,tmpStep.dubboMethod)


                if tmpStepDictKey not in self.testcaseStepInterfaceCountDict.keys():
                    requestHost = "%s[%s:%s]" % (tmpStep.dubboSystem, tmpStep.dubboTelnetHost, tmpStep.dubboTelnetPort)
                    interfaceStr = "%s.%s" % (tmpStep.dubboService, tmpStep.dubboMethod)

                    self.testcaseStepInterfaceCountDict[tmpStepDictKey] = {"total": 0, "pass": 0, "fail": 0, "error": 0, "exception": 0,"notrun": 0, "requestHost":requestHost,"interfaceStr":interfaceStr }

                if tmpStep.dubboTelnetHost.strip() != "" and self.testcaseStepInterfaceCountDict[tmpStepDictKey]['requestHost'].strip() == "":
                    self.testcaseStepInterfaceCountDict[tmpStepDictKey]['requestHost'] = tmpStep.dubboSystem

                if tmpStep.testResult != ResultConst.NOTRUN:
                    self.testcaseStepInterfaceCountDict[tmpStepDictKey]['total'] += 1

                if tmpStep.testResult == ResultConst.PASS:
                    self.testcaseStepInterfaceCountDict[tmpStepDictKey]['pass'] += 1
                    self.actualTotalTestcaseSteps+=1
                    self.testcaseStepPassCount+=1
                elif tmpStep.testResult == ResultConst.FAIL:
                    self.testcaseStepInterfaceCountDict[tmpStepDictKey]['fail'] += 1
                    self.actualTotalTestcaseSteps+=1
                    self.testcaseStepFailCount+=1
                elif tmpStep.testResult == ResultConst.ERROR:
                    self.testcaseStepInterfaceCountDict[tmpStepDictKey]['error'] += 1
                    self.actualTotalTestcaseSteps+=1
                    self.testcaseStepErrorCount+=1
                elif tmpStep.testResult == ResultConst.EXCEPTION:
                    self.testcaseStepInterfaceCountDict[tmpStepDictKey]['exception'] += 1
                    self.actualTotalTestcaseSteps += 1
                    self.testcaseStepExceptionCount += 1
                elif tmpStep.testResult == ResultConst.NOTRUN:
                    logging.debug("用例[%s]步骤%s未执行。" % (self.taskTestcaseList[i].caseId,tmpStep.stepNum))
                    self.testcaseStepInterfaceCountDict[tmpStepDictKey]['notrun'] += 1
                    self.actualTotalTestcaseSteps += 1
                    self.testcaseStepNorunCount += 1
                else:
                    logging.debug("用例[%s]步骤%s执行状态[%s]异常。" % (self.taskTestcaseList[i].caseId,tmpStep.stepNum,tmpStep.testResult))

            # 如果执行结果不是PASS，那么将进行重试。
            # 如果是进行了重试，要重新执行 bakedInterfaceCase ，并将执行结果加入到retryList
            if self.retryCount > 0 and self.taskTestcaseList[i].testResult != ResultConst.PASS:
                # 进入重试
                for retryIndex in range(0, self.retryCount):
                    currentCase = deepcopy(bakedCase)
                    self.transferAttrsFrom1Pto2P(self,currentCase)
                    # 开始执行
                    currentCase.execute()
                    self.transferAttrsFrom1Pto2P(currentCase,self)

                    self.taskTestcaseList[i].retryList.append(currentCase)

            self.updateExecutePorgressData() #将执行后的结果持久化到数据库，供前段显示进度使用。


    @catch_exception
    def generateAllExecuteSummaryDicts(self):
        """
        生成执行结果的预览字典
        :return:
        """
        #接口
        self.actualInterfaceExecuteSummayDict['total'] = self.actualTotalInterfaces
        self.actualInterfaceExecuteSummayDict['pass'] = self.interfacePassCount
        self.actualInterfaceExecuteSummayDict['fail'] = self.interfaceFailCount
        self.actualInterfaceExecuteSummayDict['error'] = self.interfaceErrorCount
        self.actualInterfaceExecuteSummayDict['notrun'] = self.interfaceNorunCount
        self.actualInterfaceExecuteSummayDict['notrunlevel'] = self.interfaceNotRunLevelCount
        #用例
        self.actualTestcaseExecuteSummayDict['total'] = self.actualTotalTestcases
        self.actualTestcaseExecuteSummayDict['pass'] = self.testcasePassCount
        self.actualTestcaseExecuteSummayDict['fail'] = self.testcaseFailCount
        self.actualTestcaseExecuteSummayDict['error'] = self.testcaseErrorCount
        self.actualTestcaseExecuteSummayDict['notrun'] = self.testcaseNorunCount
        self.actualTestcaseExecuteSummayDict['notrunlevel'] = self.testcaseNotRunLevelCount
        # 用例步骤
        self.actualTestcaseStepExecuteSummayDict['total'] = self.actualTotalTestcaseSteps
        self.actualTestcaseStepExecuteSummayDict['pass'] = self.testcaseStepPassCount
        self.actualTestcaseStepExecuteSummayDict['fail'] = self.testcaseStepFailCount
        self.actualTestcaseStepExecuteSummayDict['error'] = self.testcaseStepErrorCount
        self.actualTestcaseStepExecuteSummayDict['notrun'] = self.testcaseStepNorunCount
        self.actualTestcaseStepExecuteSummayDict['notrunlevel'] = self.testcaseStepNotRunLevelCount
        # total
        self.actualTotalExecuteSummayDict['total'] = self.actualTotal
        self.actualTotalExecuteSummayDict['pass'] = self.passCount
        self.actualTotalExecuteSummayDict['fail'] = self.failCount
        self.actualTotalExecuteSummayDict['error'] = self.errorCount
        self.actualTotalExecuteSummayDict['notrun'] = self.norunCount
        self.actualTotalExecuteSummayDict['notrunlevel'] = self.notRunLevelCount

    @catch_exception
    def generateTotalInterfaceCountDict(self):
        """
        生成总的接口统计详情
        :return:
        """
        totalInterfaceCountDict = deepcopy( self.testcaseStepInterfaceCountDict)
        for interfaceKey, interfaceValue in self.interfaceCountDict.items():
            if interfaceKey in totalInterfaceCountDict.keys():
                if totalInterfaceCountDict[interfaceKey]['requestHost'] == interfaceValue['requestHost']:
                    totalInterfaceCountDict[interfaceKey]['total'] += interfaceValue['total']
                    totalInterfaceCountDict[interfaceKey]['pass'] += interfaceValue['pass']
                    totalInterfaceCountDict[interfaceKey]['fail'] += interfaceValue['fail']
                    totalInterfaceCountDict[interfaceKey]['error'] += interfaceValue['error']
                    totalInterfaceCountDict[interfaceKey]['exception'] += interfaceValue['exception']
                else:
                    totalInterfaceCountDict[interfaceKey+"_newhost"] = interfaceValue
            else:
                totalInterfaceCountDict[interfaceKey] = interfaceValue

        self.totalInterfaceCountDict = totalInterfaceCountDict

    @catch_exception
    def analyzeTestResults(self):
        """
        根据接口和用例执行结果判断任务最终结果
        Returns:
            无
        """
        #判断执行接口和用例总数量是否是0
        if len(self.taskInterfaceList) == 0 and len(self.taskTestcaseList) == 0 :
            self.testResult = ResultConst.ERROR
            testResultDict = {}
            testResultDict['testResult'] = self.testResult
            testResultDict['testResultMsg'] = "任务中的可测试接口和用例数量为0，请检查任务中的接口和用例是否已经被删除。"
            testResultDict['interfaceExecuteSummary'] = self.actualInterfaceExecuteSummayDict
            testResultDict['testcaseExecuteSummary'] = self.actualTestcaseExecuteSummayDict
            testResultDict['testcaseStepExecuteSummary'] = self.actualTestcaseStepExecuteSummayDict
            testResultDict['totalExecuteSummary'] = self.actualTotalExecuteSummayDict
            testResultDict['interfaceCountDict'] = self.interfaceCountDict
            testResultDict['testcaseStepInterfaceCountDict'] = self.testcaseStepInterfaceCountDict
            testResultDict['totalInterfaceCountDict'] = self.totalInterfaceCountDict
            self.testResultMsg = json.dumps(testResultDict)
            return

        #生成任务执行结果
        if self.passCount == self.actualTotal:
            self.testResult = ResultConst.PASS
        elif self.actualTotal != self.passCount + self.failCount + self.errorCount:
            self.testResult = ResultConst.EXCEPTION
        elif self.errorCount > 0 :
            self.testResult = ResultConst.ERROR
        elif self.failCount > 0:
            self.testResult = ResultConst.FAIL
        else:
            self.testResult = ResultConst.EXCEPTION

        #生成任务执行结果统计
        testResultDict = {}
        testResultDict['testResult'] = self.testResult
        testResultDict['interfaceExecuteSummary'] = self.actualInterfaceExecuteSummayDict
        testResultDict['testcaseExecuteSummary'] = self.actualTestcaseExecuteSummayDict
        testResultDict['testcaseStepExecuteSummary'] = self.actualTestcaseStepExecuteSummayDict
        testResultDict['totalExecuteSummary'] = self.actualTotalExecuteSummayDict
        testResultDict['interfaceCountDict'] = self.interfaceCountDict
        testResultDict['testcaseStepInterfaceCountDict'] = self.testcaseStepInterfaceCountDict
        testResultDict['totalInterfaceCountDict'] = self.totalInterfaceCountDict
        self.testResultMsg = json.dumps(testResultDict)

    @catch_exception
    def updateExecutePorgressData(self):
        """
        更新执行进度到数据库供前端查看分析进度。
        Returns:

        """
        progressStr = "%d:%d:%d:%d:%d" % (self.actualTotal, self.passCount, self.failCount, self.errorCount,
                                          self.norunCount)  # ALL:PASS:FAIL:ERROR:NOTRUN

        try:
            self.serviceRedis.initRedisConf()
            self.serviceRedis.set_data("%s_taskExecute_%s" % (self.protocol,self.taskExecuteId),progressStr,60*60*12)
            # print("ccccccccccccccccccccccccccccccc")
            # print("%s_taskExecute_%s" % (self.protocol,self.taskExecuteId))
            self.serviceRedis.set_data("%s_taskExecuteStatus_%s" % (self.protocol,self.taskExecuteId),self.execStatus,60*60*12)
            # print("cccccccccccccccccccccccccc")
            # print(self.taskSuiteExecuteId)
            # print(self.taskExecuteId)
            if int(self.taskSuiteExecuteId) > 0:
                # print("czzzzzzzzzzzzzzzzzzzzzzzzzz")
                redisValue = {"progress":int((self.passCount+self.failCount+self.errorCount)/self.actualTotal * 100),"testResult":self.testResult,"execStatus":self.execStatus}
                # print(redisValue)
                self.serviceRedis.set_data("%s_taskSuite_%s_task_%s" % (self.protocol,self.taskSuiteExecuteId,self.taskExecuteId),json.dumps(redisValue),60*60*12)

        except:
            self.globalDB.initGlobalDBConf()
            sqlTasExec = "UPDATE tb2_dubbo_task_execute SET execProgressData = '%s' where id=%d" % (progressStr,int(self.taskExecuteId))
            self.globalDB.execute_sql(sqlTasExec,auto_release=True)
            self.globalDB.release()

    @catch_exception
    def cancelTask(self):
        self.globalDB.initGlobalDBConf()
        self.execFinishTime = get_current_time()
        sqlTasExec = "UPDATE tb2_dubbo_task_execute SET execStatus = %d,execFinishTime='%s' where id=%d" % (ExecStatus.CANCELED,self.execFinishTime,int(self.taskExecuteId))
        print(sqlTasExec)
        res = self.globalDB.execute_update_sql(sqlTasExec,auto_release=True)
        self.globalDB.release()
        return res