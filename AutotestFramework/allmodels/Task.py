import os,requests
from allmodels.HttpInterface import HttpInterface
from allmodels.HttpTestcase import HttpTestcase
from core.decorator.normal_functions import *
from core.model.TaskBase import TaskBase
from core.tools.CommonFunc import *
from core.tools.DBTool import DBTool
from core.tools.UsualTool import UsualTool
from report.HttpReport import HttpReport
from core.const.GlobalConst import ExecStatus,TestCaseStepSwitch
from core.config.InitConfig import CommonConf,TcpServerConf,EnvConfig,isReleaseEnv,RunTcpServerConf
from core.const.Do import Do

class Task(TaskBase):
    """
    任务表，包括任务执行，报告生成等。
    """
    def __init__(self):
        super(Task, self).__init__()
        self.taskSuiteExecuteId = 0

        self.id = 0 #tb_task的主键id
        self.taskId = ""
        self.taskExecuteId = 0 #tb_task_execute的主键id

        self.title = ""
        self.taskDesc = ""
        self.protocol = "HTTP"
        self.businessLineGroup = ""
        self.modulesGroup = ""
        self.sourceGroup = ""
        self.taskLevel = ""
        self.status = ""

        #任务执行的服务器IP地址，用于判断报告是否回传
        self.runTaskServiceIp = ""

        self.busiDict = {}
        self.moduleDict = {}

        self.businessLineExecuteSummayDict = {} # {"businessLineName":{"total": 0, "pass": 0, "fail": 0, "error": 0,"notrun": 0,"failedCaseList":[]}}
        self.moduleExecuteSummayDict = {} # {"businessLine":{"module":{"total": 0, "pass": 0, "fail": 0, "error": 0,"notrun": 0,"failedCaseList":[]}}}




    @take_time
    def execute(self):
        """
        任务执行
        Returns:
            无
        """
        try:

            logging.debug("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$任务执行ID[%d]任务ID[%s]开始执行在环境httpConfKey[%s]执行人[%s]$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$" % (int(self.taskExecuteId),self.taskId,self.httpConfKey,self.addBy))
            self.execStatus = ExecStatus.RUNNING
            self.updateExecuteStatusToDB()  # 将执行中状态写入到数据库 供前端使用
            ######执行时间
            self.execTime = get_current_time()
            self.updateExecuteStartTime()

            super(Task, self).execute()

            # DONE 生成报告
            resGenerateReport = self.generateHttpReport()
            # DONE 写入数据库测试结果 PASS 数据统计已执行接口数量，用例数量，错误率等。 报告url等  执行结果
            resUpdateResults = self.updateExecResultsByTaskExecuteId()
            # DONE 更新状态为已完成 判断报告是否完成，结果是否写入数据库，如果正常状态是DONE，否则状态是EXCEPTION
            if resGenerateReport and resUpdateResults:
                self.execStatus = ExecStatus.DONE
            else:
                self.execStatus = ExecStatus.EXCEPTION
            self.updateExecuteStatusToDB()  # 将执行中状态写入到数据库 供前端使用
            self.generateTaskExecuteSummaryDict()
            #删除redis中本任务的执行进度
            self.serviceRedis.initRedisConf()
            self.serviceRedis.del_data("%s_taskExecute_%s" % (self.protocol,self.taskExecuteId))
            self.serviceRedis.del_data("%s_taskExecuteStatus_%s" % (self.protocol,self.taskExecuteId))
            if int(self.taskSuiteExecuteId) > 0:
                redisValue = {"progress":100,"testResult":self.testResult,"execStatus":self.execStatus}
                self.serviceRedis.set_data("%s_taskSuite_%s_task_%s" % (self.protocol,self.taskSuiteExecuteId,self.taskExecuteId),json.dumps(redisValue),60*60*12)
            #####################执行完成并生成报告#########################
            # 根据执行结果将接口执行信息加入到历史纪录
            if self.isSaveHistory == 1:
                self.insertInterfaceInfosToDB()
            if self.isSendEmail > 0:
                self.sendEmailToExecutor()
            tcpStr = '{"do":%s,"TaskExecuteId":%s,"%s":"%s","%s":%s}' % (Do.TYPE_TASK_EXECUTE_DONE,self.taskExecuteId,Do.TYPE_PROTOCOL,self.protocol,Do.KEY_TASK_SUITE_EXECUTE_ID,self.taskSuiteExecuteId)
            if not sendTcp(TcpServerConf.ip,TcpServerConf.port,tcpStr):
                logging.error("任务执行完毕TCP回调函数发生异常！ %s " % tcpStr)
            logging.debug("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$任务[%s]结束执行$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$" % self.taskId)
        except Exception as e:
            logging.error("任务执行函数发生异常！")
            logging.error(traceback.format_exc())


    @catch_exception
    def generateByTaskExecuteId(self):
        """
        生成任务通过 任务执行id从tb_task_execute查询任务属性
        Returns:
            无
        """
        self.globalDB.initGlobalDBConf()
        self.taskExecuteId = int(self.taskExecuteId)
        sqlTasExec = "select * from tb_task_execute where id=%d" % int(self.taskExecuteId)
        resTaskExec = self.globalDB.execute_sql(sqlTasExec)


        if resTaskExec:
            tmpResTaskInfo = resTaskExec[0]
            self.id = tmpResTaskInfo['id'] #tb_task的主键id
            self.taskId = tmpResTaskInfo['taskId']
            self.traceId = md5("%s-%s" % (self.taskId, get_current_time()))

            self.taskSuiteExecuteId = tmpResTaskInfo["taskSuiteExecuteId"]

            self.title = tmpResTaskInfo['title']
            self.taskDesc = tmpResTaskInfo['taskdesc']
            self.protocol = tmpResTaskInfo['protocol']
            self.businessLineGroup = tmpResTaskInfo['businessLineGroup']
            self.modulesGroup = tmpResTaskInfo['modulesGroup']
            self.sourceGroup = tmpResTaskInfo['sourceGroup']
            self.taskLevel = tmpResTaskInfo['taskLevel']
            self.status = tmpResTaskInfo['status']

            self.version= tmpResTaskInfo['version']

            self.interfaceCount = int(tmpResTaskInfo['interfaceCount'])
            self.taskInterfaces = tmpResTaskInfo['taskInterfaces'] #Done 需要根据列表生成对应的用例任务集合列表taskinterfaceList
            self.caseCount = int(tmpResTaskInfo['caseCount'])
            self.taskCases = tmpResTaskInfo['taskTestcases'] #Done 需要根据列表生成对应的用例任务集合列表taskcasesList
            #TODO 此处应当生成优先变量
            self.caseLevel = tmpResTaskInfo["caseLevel"]
            self.httpConfKey = tmpResTaskInfo['httpConfKey']
            self.confHttpLayer.key = self.httpConfKey
            self.confHttpLayer.generate_http_conf_by_key()

            self.highPriorityVARSStr = tmpResTaskInfo['highPriorityVARS']
            # self.highPriorityVARSStr = "[CONF=common]areal = 1;$IMPORT[testkey];myGReal = $GVAR[WJL_TEST_GVAR_KEY];[ENDCONF]"  # 通过Str生成dict

            self.highPriorityVARSDict = {}  # 优先变量

            self.isSendEmail = int(tmpResTaskInfo['isSendEmail'])
            self.isCodeRate = int(tmpResTaskInfo['isCodeRate'])
            self.isSaveHistory = int(tmpResTaskInfo['isSaveHistory'])
            self.execComments = tmpResTaskInfo['execComments']

            self.retryCount = int(tmpResTaskInfo['retryCount']) #重试次数，默认是0
            self.execType = tmpResTaskInfo['execType']
            self.execTime = tmpResTaskInfo['execTime']
            self.execFinishTime = tmpResTaskInfo['execFinishTime']
            self.execBy = tmpResTaskInfo['execBy']
            self.execStatus = tmpResTaskInfo['execStatus']
            self.execProgressData = tmpResTaskInfo['execProgressData']
            self.execPlatform = tmpResTaskInfo['execPlatform']
            self.execLevel = int(tmpResTaskInfo['execLevel'])

            self.testResult = tmpResTaskInfo['testResult']
            self.testResultMsg = tmpResTaskInfo['testResultMsg']
            self.testReportUrl = tmpResTaskInfo['testReportUrl']
            self.performanceResult = tmpResTaskInfo['performanceResult']

            self.state = tmpResTaskInfo['state']
            self.addBy = tmpResTaskInfo['addBy']
            self.modBy = tmpResTaskInfo['modBy']
            self.addTime = tmpResTaskInfo['addTime']
            self.modTime = tmpResTaskInfo['modTime']

            #根据version来获取
            if self.version == "CurrentVersion":
                self.taskTestcaseList = []
                caseIdList = self.taskCases.split(",")
                getCaseListSql = ""
                for tmpCaseId in caseIdList:
                    getCaseListSql += "select * from tb_http_testcase where state = 1 and caseId='%s' union all " % tmpCaseId
                getCaseListSql = getCaseListSql[:-11]
                resCaseListData = self.globalDB.execute_sql(getCaseListSql)

                caseListForIn = ""
                for tCid in caseIdList:
                    caseListForIn += "'%s'," % tCid
                caseListForIn = caseListForIn[:-1]
                sqlCaseSteps = "select * from tb_http_testcase_step where state = 1 and caseId in (%s) order by stepNum asc" % caseListForIn
                resCaseStepData = self.globalDB.execute_sql(sqlCaseSteps)
                resCaseStepDict = {}
                for tmpCaseStep in resCaseStepData:
                    if tmpCaseStep['stepSwitch'] == TestCaseStepSwitch.NOT_SWITCH:
                        continue
                    if tmpCaseStep['caseId'] not in resCaseStepDict.keys():
                        resCaseStepDict[tmpCaseStep['caseId']] = []
                    tmpCaseStep['version'] = self.version
                    resCaseStepDict[tmpCaseStep['caseId']].append(tmpCaseStep)

                for tmpCaseDict in resCaseListData:
                    if tmpCaseDict['caseId'] == "":
                        continue
                    tmpHttpCase = HttpTestcase()
                    tmpHttpCase.confHttpLayer = self.confHttpLayer
                    tmpHttpCase.version = self.version
                    tmpCaseDict['version'] = self.version

                    tmpHttpCase.generateByCaseDict(tmpCaseDict,resCaseStepDict[tmpCaseDict['caseId']])
                    self.taskTestcaseList.append(tmpHttpCase)

                self.taskInterfaceList = []
                interfaceIdList = self.taskInterfaces.split(",")
                getInterfaceListSql = ""
                for tmpInterfaceId in interfaceIdList:
                    getInterfaceListSql += " SELECT * FROM tb_http_interface where state = 1 and interfaceId = '%s' union all " % (tmpInterfaceId)
                getInterfaceListSql = getInterfaceListSql[:-11]
                resInterfaceListData = self.globalDB.execute_sql(getInterfaceListSql)
                for tmpInterfacceDict in resInterfaceListData:
                    if tmpInterfacceDict['interfaceId'] == "":
                        continue
                    tmpInterface = HttpInterface()
                    tmpInterface.confHttpLayer = self.confHttpLayer
                    tmpInterface.version = self.version
                    tmpInterfacceDict['version'] = self.version

                    tmpInterface.generateByInterfaceDict(tmpInterfacceDict)
                    self.taskInterfaceList.append( tmpInterface )
            else:
                #去version表获取
                self.taskTestcaseList = []
                caseIdList = self.taskCases.split(",")
                getCaseListSql = ""
                for tmpCaseId in caseIdList:
                    getCaseListSql += "select * from tb_version_http_testcase where state = 1 and caseId='%s' and versionName='%s' union all " % (tmpCaseId,self.version)
                getCaseListSql = getCaseListSql[:-11]
                resCaseListData = self.globalDB.execute_sql(getCaseListSql)

                caseListForIn = ""
                for tCid in caseIdList:
                    caseListForIn += "'%s'," % tCid
                caseListForIn = caseListForIn[:-1]
                sqlCaseSteps = "select * from tb_version_http_testcase_step where state = 1 and caseId in (%s)  and versionName='%s' order by stepNum asc" % (caseListForIn,self.version)
                resCaseStepData = self.globalDB.execute_sql(sqlCaseSteps)
                resCaseStepDict = {}
                for tmpCaseStep in resCaseStepData:
                    if tmpCaseStep['caseId'] not in resCaseStepDict.keys():
                        resCaseStepDict[tmpCaseStep['caseId']] = []
                    tmpCaseStep['version'] = self.version
                    resCaseStepDict[tmpCaseStep['caseId']].append(tmpCaseStep)

                for tmpCaseDict in resCaseListData:
                    if tmpCaseDict['caseId'] == "":
                        continue
                    tmpHttpCase = HttpTestcase()
                    tmpHttpCase.confHttpLayer = self.confHttpLayer
                    tmpHttpCase.version = self.version
                    tmpCaseDict['version'] = self.version
                    tmpHttpCase.generateByCaseDict(tmpCaseDict, resCaseStepDict[tmpCaseDict['caseId']])
                    self.taskTestcaseList.append(tmpHttpCase)

                self.taskInterfaceList = []
                interfaceIdList = self.taskInterfaces.split(",")
                getInterfaceListSql = ""
                for tmpInterfaceId in interfaceIdList:
                    getInterfaceListSql += " SELECT * FROM tb_version_http_interface where state = 1 and interfaceId = '%s' and versionName='%s'  union all " % (tmpInterfaceId,self.version)
                getInterfaceListSql = getInterfaceListSql[:-11]
                resInterfaceListData = self.globalDB.execute_sql(getInterfaceListSql)
                for tmpInterfacceDict in resInterfaceListData:
                    if tmpInterfacceDict['interfaceId'] == "":
                        continue
                    tmpInterface = HttpInterface()
                    tmpInterface.confHttpLayer = self.confHttpLayer
                    tmpInterface.version = self.version
                    tmpInterfacceDict['version'] = self.version

                    tmpInterface.generateByInterfaceDict(tmpInterfacceDict)
                    self.taskInterfaceList.append(tmpInterface)

        self.globalDB.release()

    @catch_exception
    def generateHttpReport(self):
        """
        生成测试报告
        Returns:

        """
        reportFolderName = "reports"
        reportFolder = "%s/%s" % (LogConfig.dirfilePath,reportFolderName)
        if os.path.exists(reportFolder) == False:
            os.mkdir(reportFolder)
        dateFolderName = get_current_time_YYYYMMDD()
        dateFolder = "%s/%s" % (reportFolder, dateFolderName)
        if os.path.exists(dateFolder) == False:
            os.mkdir(dateFolder)
        fileName = "HTTP_%s_%s_%s.html" % (self.taskExecuteId,self.taskId,get_current_time_YYYYMMDDHHMMSS())
        self.testReportFilePath = "%s/%s" % (dateFolder,fileName)
        if HttpReport().createHttpReportByTask(self,self.testReportFilePath):
            self.testReportUrl = "/%s/%s/%s" % (reportFolderName, dateFolderName, fileName)
            if isReleaseEnv:
                pass
            else:
                #非正式环境，要把测试报告传回本机
                if self.runTaskServiceIp != TcpServerConf.ip:
                #当前执行机不是main主机，要把测试报告发送回去
                    if sendFtp(TcpServerConf.ip,"setAPITaskReports","setAPITaskReports",dateFolderName,fileName,self.testReportFilePath):
                        print("测试报告从执行机传输到主服务器执行完毕")
                    else:
                        logging.error("测试报告从执行机传输到主服务器失败")
                else:
                    print("当前执行机为主服务器，不执行传输操作")
            return True
        else:
            return False

    @catch_exception
    def updateExecResultsByTaskExecuteId(self):
        """
        更新任务执行结果到数据库，根据任务执行id
        Returns:

        """
        self.globalDB.initGlobalDBConf()
        progressStr = "%d:%d:%d:%d:%d" % (self.actualTotal, self.passCount, self.failCount, self.errorCount, self.norunCount)
        #处理结果，增加shell解析字段。
        if(isJson(self.testResultMsg)):
            testResultMsgDict = json.loads(self.testResultMsg)
            shellStr = "%s|%s|%s|%s|%s" %(
                testResultMsgDict['testResult'],
                testResultMsgDict['totalExecuteSummary']['total'],
                testResultMsgDict['totalExecuteSummary']['pass'],
                testResultMsgDict['totalExecuteSummary']['fail'],
                testResultMsgDict['totalExecuteSummary']['error'],
            )
            testResultMsgDict['testResultMsgForShell'] = shellStr
            self.testResultMsg = json.dumps(testResultMsgDict,ensure_ascii=False)

        sqlTasExec = "UPDATE tb_task_execute SET highPriorityVARS='%s',execTime='%s',execFinishTime = '%s' ,execTakeTime = %d ,testResult = '%s',testResultMsg = '%s',testReportUrl = '%s' , performanceResult = '%s',execProgressData = '%s' where id=%d" \
                     % ( replacedForIntoDB(self.highPriorityVARSFinalStr),
                        self.execTime,
                        self.execFinishTime,
                        self.taskExecTakeTime,
                        replacedForIntoDB(self.testResult),
                        replacedForIntoDB(self.testResultMsg),
                        replacedForIntoDB(self.testReportUrl),
                        self.performanceResult,
                         progressStr,
                         int(self.taskExecuteId))
        logging.debug(sqlTasExec)
        if self.globalDB.execute_sql(sqlTasExec) == False:
            sqlTasExec2 = "UPDATE tb_task_execute SET execTime='%s',execFinishTime = '%s' ,execTakeTime = %d ,testResult = '%s',testResultMsg = '%s',testReportUrl = '%s' where id=%d" \
                         % (self.execTime,
                            self.execFinishTime,
                            self.taskExecTakeTime,
                            replacedForIntoDB(self.testResult),
                            "EXCEPTION:任务执行后数据更新时发生异常，请联系管理员定位问题。",
                            replacedForIntoDB(self.testReportUrl),
                            int(self.taskExecuteId))
            self.globalDB.execute_sql(sqlTasExec2)
            self.globalDB.release()
            return False
        else:
            self.globalDB.release()
            return True

    @catch_exception
    def updateExecuteStatusToDB(self):
        """
        更新任务执行状态到数据库
        Returns:
            执行结果
        """
        self.globalDB.initGlobalDBConf()
        sqlTasExec = "UPDATE tb_task_execute SET execStatus = %d where id=%d" % (int(self.execStatus),int(self.taskExecuteId))
        retRes = self.globalDB.execute_sql(sqlTasExec)
        self.globalDB.release()
        return retRes

    @catch_exception
    def updateExecuteStartTime(self):
        self.globalDB.initGlobalDBConf()
        self.execFinishTime = get_current_time()
        progressStr = "%d:%d:%d:%d:%d" % (self.actualTotal,self.passCount,self.failCount,self.errorCount,self.norunCount) # ALL:PASS:FAIL:ERROR:NOTRUN
        sqlTasExec = "UPDATE tb_task_execute SET execTime='%s' where id=%d" % (self.execTime,int(self.taskExecuteId))
        res = self.globalDB.execute_update_sql(sqlTasExec)
        self.globalDB.release()
        return res

    @catch_exception
    def insertInterfaceInfosToDB(self):
        """
        更新任务执行中所有接口的统计到数据库，用来历史追述
        :return:
        """
        self.globalDB.initGlobalDBConf()
        taskExecuteId = self.id
        taskId = self.taskId
        title = self.title
        taskDesc = self.taskDesc
        protocol = self.protocol
        httpConfKey = self.httpConfKey
        execBy = self.execBy
        testReportUrl = self.testReportUrl
        addBy = self.execBy
        modBy = self.execBy
        for tmpKey,tmpValue in self.totalInterfaceCountDict.items():
            interfaceUrl = tmpKey
            requestHost = tmpValue['host']
            totalCount = tmpValue['total']
            passCount = tmpValue['pass']
            failCount = tmpValue['fail']
            errorCount = tmpValue['error']
            exceptionCount = tmpValue['exception']
            if requestHost.strip() != "":
                tmpsql = """INSERT INTO tb_interface_execute_history(interfaceUrl,requestHost,totalCount,passCount,failCount,errorCount,exceptionCount,taskExecuteId,taskId,title,taskDesc,protocol,httpConfKey,execBy,testReportUrl,addBy,modBy,addTime,modTime,state) 
                         VALUES("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s",%d)""" % \
                         (replacedForIntoDB(interfaceUrl),replacedForIntoDB(requestHost),totalCount,passCount,failCount,errorCount,exceptionCount,taskExecuteId,taskId,replacedForIntoDB(title),replacedForIntoDB(taskDesc),
                          protocol,httpConfKey,execBy,replacedForIntoDB(testReportUrl),addBy,modBy,get_current_time(),get_current_time(),1)
                res = self.globalDB.execute_sql(tmpsql)
                if len(res) >= 0:
                    logging.debug("插入成功[%s][%s][%s]!" %(taskExecuteId,taskId,interfaceUrl))
                else:
                    logging.debug("插入失败[%s][%s][%s]!" % (taskExecuteId, taskId, interfaceUrl))

        self.globalDB.release()

    @catch_exception
    def sendEmailToExecutor(self):
        self.globalDB.initGlobalDBConf()
        res = self.globalDB.execute_sql("select email from tb_user where loginName='%s' " % self.execBy)
        resEmailList = self.globalDB.execute_sql("select emailList from tb_task_execute where id=%d" % int(self.taskExecuteId))
        self.globalDB.release()
        if res:
            emailList = ""
            if resEmailList:
                resEmList = resEmailList[0]['emailList'].split(",")
                for tmpMail in resEmList:
                    emailList = emailList +";" + tmpMail
            subject = "[%s]任务[%s:%s]测试报告" % (self.testResult,self.taskId, self.title)
            if emailList == "":
                logging.info("邮箱列表为空，不执行邮件发送")
                return
            #开始生成emailText的html###############################################################################
            """
（一）测试报告概况：
任务ID：HTTP_TASK_62
执行环境：预发布灰度
执行结果：FAIL
执行耗时：36秒
任务名称：SFA-CPQ团队-自动化测试【staging灰度环境】
任务描述：（1）【产品】PC端和APP端 （2）【价格表】&【价格表明细】PC端和APP端（3）【合同】PC端和APP端
包含ywx：['SFA']
包含mk：['产品', '合同', '价格表']
备注：在jenkins上执行自动化测试任务
 
所有统计：

（1）用例统计：用例总数10个，通过7，失败3，通过率70%。【说明：因为任务中的用例都会被执行，通过率 = 通过数量 / 总数量】
（2）接口统计：接口总数500个，通过400个，失败50个，未执行50个，通过率80%。【说明：接口总数包含独立接口和用例接口之和。因为用例的靠前的接口可能失败，靠后的接口不会被执行，通过率定义方式大家可以多提建议。通过率 =  通过数量 / 总数量】
（二）失败的所有接口汇总：【说明：包含独立接口和用例接口】
（1）mk：【产品】
接口[/json/crm_product/save.action]：已执行4次，通过0，失败4，通过率0.00%。
（2）mk：【合同】
接口[/mobile/common/search.action]：已执行2次，通过1，失败1，通过率50.00%。
接口[/json/crm_common_detail/lock-data.action]：已执行1次，通过0，失败1，通过率0.00%。
 详情见附件。
            """
            bgColor = "#f2dede"
            if self.testResult == "PASS":
                bgColor = "#dff0d8"
            emailText =   "<html><body style='background-color:%s;display:block;'>" % bgColor

            #1、测试报告概况
            emailText = emailText + ("""
            <h1>（一）测试报告概况</h1>
            <h2>任务基本信息</h2>
            <table border="1px" cellpadding="3px" width="80%%">
            <tr><th width="20%%"  align="left">任务ID</th><td width="80%%">%s</td></tr>
            <tr><th align="left">创建人</th><td>%s</td></tr>
            <tr><th align="left">执行环境</th><td>%s(%s)</td></tr>
            <tr><th align="left">执行时间</th><td>%s</td></tr>
            <tr><th align="left">执行结果</th><td>%s</td></tr>
            <tr><th align="left">执行耗时</th><td>%s秒</td></tr>
            <tr><th align="left">任务名称</th><td>%s</td></tr>
            <tr><th align="left">任务描述</th><td>%s</td></tr>
            <tr><th align="left">包含%s</th><td>%s</td></tr>
            <tr><th align="left">包含%s</th><td>%s</td></tr>
            <tr><th align="left">备注</th><td>%s</td></tr>
            </table>""" % (self.taskId,self.addBy,self.confHttpLayer.alias,self.confHttpLayer.key,self.execTime,self.testResult,self.taskExecTakeTime,self.title,self.taskDesc,CommonConf.groupLevel1,self.businessLineGroup,CommonConf.groupLevel2,self.modulesGroup,(self.execComments.strip()=="" and "无" or self.execComments.strip())))
            if isDictJson(self.testResultMsg):
                resDict = json.loads(self.testResultMsg)
                #所有统计信息开始################################################################
                emailText = emailText + "<h2>所有统计</h2>"
                emailText = emailText + """<table border="1px" cellpadding="3px" width="80%%">"""

                if resDict['totalExecuteSummary']['total'] > 0:
                    emailText = emailText + """<tr><th align="left" width="20%%">所有接口统计</th><td width="80%%">接口总数%d个，已执行接口%d个，通过%d，失败%d，未执行%d个，通过率%.2f%%。</td></tr>""" \
                                            % (resDict['interfaceExecuteSummary']['total']+resDict['testcaseStepExecuteSummary']['total'],
                                               (resDict['interfaceExecuteSummary']['total']+resDict['testcaseStepExecuteSummary']['total']-resDict['interfaceExecuteSummary']['notrun'] - resDict['testcaseStepExecuteSummary']['notrun']),
                                               resDict['interfaceExecuteSummary']['pass']+resDict['testcaseStepExecuteSummary']['pass'],
                                               resDict['interfaceExecuteSummary']['fail'] + resDict['testcaseStepExecuteSummary']['fail'],
                                               resDict['interfaceExecuteSummary']['notrun'] + resDict['testcaseStepExecuteSummary']['notrun'],
                                               ((float(resDict['interfaceExecuteSummary']['pass']+resDict['testcaseStepExecuteSummary']['pass']) / float(resDict['interfaceExecuteSummary']['total']+resDict['testcaseStepExecuteSummary']['total'])) * 100))
                if resDict['interfaceExecuteSummary']['total'] > 0:
                    emailText = emailText + """<tr><th align="left">独立接口统计</th><td>已执行接口%d个，通过%d，失败%d，通过率%.2f%%。</td></tr>""" % (resDict['interfaceExecuteSummary']['total'], resDict['interfaceExecuteSummary']['pass'], resDict['interfaceExecuteSummary']['fail'],((float(resDict['interfaceExecuteSummary']['pass']) / float(resDict['interfaceExecuteSummary']['total'])) * 100))
                if resDict['testcaseExecuteSummary']['total'] > 0:
                    emailText = emailText + """<tr><th align="left">用例统计</th><td>已执行用例%d个，通过%d，失败%d，通过率%.2f%%。</td></tr>""" % (resDict['testcaseExecuteSummary']['total'], resDict['testcaseExecuteSummary']['pass'], resDict['testcaseExecuteSummary']['fail'],((float(resDict['testcaseExecuteSummary']['pass']) / float(resDict['testcaseExecuteSummary']['total'])) * 100))

                emailText = emailText + """</table>"""
                #所有统计信息结束################################################################

                #yewuxian mokuai统计信息#################################
                emailText = emailText + "<h2>%s%s统计</h2>" % (CommonConf.groupLevel1,CommonConf.groupLevel2)
                emailText = emailText + """<table border="1px" cellpadding="3px" width="80%%">"""
                for k,v in self.businessLineExecuteSummayDict.items():
                    emailText = emailText + """<tr><th align="left">%s</th><td>接口总数%d个，已执行接口%d个，通过%d，失败%d，未执行%d个，通过率%.2f%%。</td></tr>""" %(
                        k,v['total'],(v['total']-v['notrun']),v['pass'],v['fail'],v['notrun'],((float(v['pass']) / float(v['total'])) * 100)
                    )
                    for km,vm in self.moduleExecuteSummayDict[k].items():
                        emailText = emailText + """<tr><th align="left">%s->%s</th><td>接口总数%d个，已执行接口%d个，通过%d，失败%d，未执行%d个，通过率%.2f%%。</td></tr>""" % (
                            k,km, vm['total'],(vm['total']-vm['notrun']), vm['pass'], vm['fail'], vm['notrun'], ((float(vm['pass']) / float(vm['total'])) * 100)
                        )
                emailText = emailText + """</table>"""
                #ywwuxian mokuai统计信息结束#################################

                #失败接口汇总
                if self.testResult != ResultConst.PASS:
                    emailText = emailText + "<h1>（二）失败的所有接口汇总</h1>"
                    emailText = emailText + "<h2>按照%s%s统计失败的接口和用例</h2>" % (CommonConf.groupLevel1,CommonConf.groupLevel2)
                    # 列出失败的接口+===========================================================================
                    emailText = emailText + """<table border="1px" cellpadding="3px" width="80%%">"""
                    emailText = emailText + """<tr><th width="20%%" align="left">%s->%s</th><th width="20%%" align="left">接口/用例ID</th><th width="50%%" align="left">描述</th><th width="10%%" align="left">结果</th></tr>""" % (CommonConf.groupLevel1,CommonConf.groupLevel2)

                    for tmpInterface in self.taskInterfaceList:
                        if tmpInterface.testResult != ResultConst.PASS:
                            emailText = emailText + ("<tr><td>%s->%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (self.busiDict[str(tmpInterface.businessLineId)],self.moduleDict[str(tmpInterface.modules)],tmpInterface.interfaceId, tmpInterface.title,tmpInterface.testResult))

                    for tmpTestcase in self.taskTestcaseList:
                        if tmpTestcase.testResult != ResultConst.PASS:
                            emailText = emailText + ("<tr><td>%s->%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (self.busiDict[str(tmpTestcase.businessLineId)],self.moduleDict[str(tmpTestcase.moduleId)],tmpTestcase.caseId, tmpTestcase.title,tmpTestcase.testResult))
                            for i in range(0,len(tmpTestcase.stepTestcaseList)):
                                emailText = emailText + ("<tr><td></td><td>步骤：%s</td><td>%s</td><td>%s</td></tr>" % (tmpTestcase.stepTestcaseList[i].stepNum, tmpTestcase.stepTestcaseList[i].desc,tmpTestcase.stepTestcaseList[i].testResult))
                                if tmpTestcase.stepTestcaseList[i].testResult!=ResultConst.PASS:
                                    break
                    emailText = emailText + """</table>"""
                    #列出失败的接口结束+=======================================================================
                    #显示失败接口的执行通过率。
                    interfaceCountDict = resDict['interfaceCountDict']
                    testcaseStepInterfaceCountDict = resDict['testcaseStepInterfaceCountDict']
                    totalInterfaceCountDict = resDict['totalInterfaceCountDict']
                    if len(interfaceCountDict) > 0 :
                        emailText = emailText + "<h2>接口中失败接口执行详情</h2>"
                        emailText = emailText + """<table border="1px" cellpadding="3px" width="80%%">"""
                        for k,v in interfaceCountDict.items():
                            if v['total'] != v['pass']:
                                emailText = emailText + "<tr><th width=40%% align='left'>%s</th><td width=60%% >已执行%d次，通过%d，失败%d，通过率%.2f%%。</td></tr>" % (k,v['total'],v['pass'],v['fail'],((float(v['pass']) / float(v['total'])) * 100))

                        emailText = emailText + """</table>"""

                    if len(testcaseStepInterfaceCountDict) > 0:
                        emailText = emailText + "<h2>用例中失败接口执行详情</h2>"
                        emailText = emailText + """<table border="1px" cellpadding="3px" width="80%%">"""

                        for k,v in testcaseStepInterfaceCountDict.items():
                            if v['total'] != v['pass']:
                                emailText = emailText + "<tr><th width=40%% align='left'>%s</th><td width=60%% >已执行%d次，通过%d，失败%d，通过率%.2f%%。</td></tr>" % (k,v['total'],v['pass'],v['fail'],((float(v['pass']) / float(v['total'])) * 100))

                        emailText = emailText + """</table>"""

                    if len(totalInterfaceCountDict) > 0 and len(interfaceCountDict) > 0 and len(testcaseStepInterfaceCountDict) > 0:
                        emailText = emailText + "<h2>所有接口失败执行详情</h2>"
                        emailText = emailText + """<table border="1px" cellpadding="3px" width="80%%">"""

                        for k,v in totalInterfaceCountDict.items():
                            if v['total'] != v['pass']:
                                emailText = emailText + "<tr><th width=40%% align='left'>%s</th><td width=60%% >已执行%d次，通过%d，失败%d，通过率%.2f%%。</td></tr>" % (k,v['total'],v['pass'],v['fail'],((float(v['pass']) / float(v['total'])) * 100))

                        emailText = emailText + """</table>"""

            else:
                # task 执行结果 结果没有返回正常的json
                emailText = emailText + self.testResultMsg +"<br>"

            #self.isSendEmail  是否发送是否带附件PassFailErrorException
            isSendMailStr = str(self.isSendEmail)
            #不够6位后面补1
            addOneCount = 6 - len(isSendMailStr)
            for i in range(0,addOneCount):
                isSendMailStr = isSendMailStr+"1"
            if int(isSendMailStr[1]) == 1:
                emailText = emailText + "<br>详情见附件。"
            else:
                if CommonConf.http_report_to_AWS == "1":
                    tmpurl = self.testReportUrl
                else:
                    tmpurl = EnvConfig.WEB_URI + self.testReportUrl

                emailText = emailText + ("<br>详情见:&nbsp;&nbsp;<a href='%s'>%s</a>" % (tmpurl,tmpurl))

            emailText = emailText + "</body></html>"
            #结束生成emailText的html###############################################################################
            #开始发送邮件
            def subSendMail():
                if int(isSendMailStr[1]) == 1:
                    # 发送附件
                    UsualTool.send_mail(emailList, subject, emailText, self.testReportFilePath, subType="html")
                else:
                    # 不发送附件
                    UsualTool.send_mail(emailList, subject, emailText, subType="html")

            if self.testResult == ResultConst.PASS and int(isSendMailStr[2]) == 1:
                subSendMail()
            elif self.testResult == ResultConst.FAIL and int(isSendMailStr[3]) == 1:
                subSendMail()
            elif self.testResult == ResultConst.ERROR and int(isSendMailStr[4]) == 1:
                subSendMail()
            elif self.testResult == ResultConst.EXCEPTION and int(isSendMailStr[5]) == 1:
                subSendMail()
        else:
            emailList = EmailConfig.sender# ;分号间隔
            subject = "[%s]任务[%s:%s]测试报告，没有找到收件人，执行者为%s" % (self.testResult,self.taskId, self.title,self.execBy)
            emailText = "[%s]任务[%s:%s]测试报告，没有找到收件人，执行者为%s" % (self.testResult,self.taskId, self.title,self.execBy)
            UsualTool.send_mail(emailList, subject, emailText,subType="html")

    @catch_exception
    def generateInterfaceCoverageRate(self):
        self.globalDB.initGlobalDBConf()
        self.globalDB.execute_sql("select * from tb_standard_interface where state = 1")
        self.globalDB.release()

    @catch_exception
    def getAllBusinessLine(self):
        self.globalDB.initGlobalDBConf()
        resList = self.globalDB.execute_sql("select id,bussinessLineName from tb_business_line order by id ",auto_release=True)
        retDict = {}
        for tmp in resList:
            retDict[str(tmp['id'])] = tmp['bussinessLineName']
        return retDict

    @catch_exception
    def getAllModule(self):
        self.globalDB.initGlobalDBConf()
        resList = self.globalDB.execute_sql("select id,moduleName from tb_modules order by id ",auto_release=True)
        retDict = {}
        for tmp in resList:
            retDict[str(tmp['id'])] = tmp['moduleName']
        return retDict

    @catch_exception
    def generateTaskExecuteSummaryDict(self):
        busiDict = self.getAllBusinessLine() #key是id value是名字
        moduleDict = self.getAllModule() #key是id，value是名字
        self.busiDict = busiDict
        self.moduleDict = moduleDict
        for i in range(0,len(self.taskInterfaceList)):
            tmpInterface = self.taskInterfaceList[i]
            tmpBusi = busiDict[str(tmpInterface.businessLineId)]
            tmpModule = moduleDict[str(tmpInterface.modules)]
            #初始化key
            if tmpBusi not in self.businessLineExecuteSummayDict.keys():
                self.businessLineExecuteSummayDict[tmpBusi] = {"total": 0, "pass": 0, "fail": 0, "error": 0,"notrun": 0,"failedCaseList":[]}
            if tmpBusi not in self.moduleExecuteSummayDict.keys():
                self.moduleExecuteSummayDict[tmpBusi] = {}
            if tmpModule not in self.moduleExecuteSummayDict[tmpBusi].keys():
                self.moduleExecuteSummayDict[tmpBusi][tmpModule] = {"total": 0, "pass": 0, "fail": 0, "error": 0,"notrun": 0,"failedCaseList":[]}
            if tmpInterface.testResult == ResultConst.PASS:
                self.businessLineExecuteSummayDict[tmpBusi]['total'] += 1
                self.businessLineExecuteSummayDict[tmpBusi]['pass'] += 1
                self.moduleExecuteSummayDict[tmpBusi][tmpModule]['total'] += 1
                self.moduleExecuteSummayDict[tmpBusi][tmpModule]['pass'] += 1
            elif tmpInterface.testResult == ResultConst.FAIL:
                self.businessLineExecuteSummayDict[tmpBusi]['total'] += 1
                self.businessLineExecuteSummayDict[tmpBusi]['fail'] += 1
                self.businessLineExecuteSummayDict[tmpBusi]['failedCaseList'].append(tmpInterface)
                self.moduleExecuteSummayDict[tmpBusi][tmpModule]['total'] += 1
                self.moduleExecuteSummayDict[tmpBusi][tmpModule]['fail'] += 1
                self.moduleExecuteSummayDict[tmpBusi][tmpModule]['failedCaseList'].append(tmpInterface)
            elif tmpInterface.testResult == ResultConst.ERROR:
                self.businessLineExecuteSummayDict[tmpBusi]['total'] += 1
                self.businessLineExecuteSummayDict[tmpBusi]['error'] += 1
                self.businessLineExecuteSummayDict[tmpBusi]['failedCaseList'].append(tmpInterface)
                self.moduleExecuteSummayDict[tmpBusi][tmpModule]['total'] += 1
                self.moduleExecuteSummayDict[tmpBusi][tmpModule]['error'] += 1
                self.moduleExecuteSummayDict[tmpBusi][tmpModule]['failedCaseList'].append(tmpInterface)
            else:
                self.businessLineExecuteSummayDict[tmpBusi]['total'] += 1
                self.businessLineExecuteSummayDict[tmpBusi]['notrun'] += 1
                # self.businessLineExecuteSummayDict[tmpBusi]['failedCaseList'].append(tmpInterface)
                self.moduleExecuteSummayDict[tmpBusi][tmpModule]['total'] += 1
                self.moduleExecuteSummayDict[tmpBusi][tmpModule]['notrun'] += 1
                # self.moduleExecuteSummayDict[tmpBusi][tmpModule]['failedCaseList'].append(tmpInterface)

        for i in range(0,len(self.taskTestcaseList)):
            tmpCase = self.taskTestcaseList[i]
            for tmpStep in tmpCase.stepTestcaseList:
                tmpInterface = tmpStep
                tmpBusi = busiDict[str(tmpInterface.businessLine)]
                tmpModule = moduleDict[str(tmpInterface.modules)]
                # 初始化key
                if tmpBusi not in self.businessLineExecuteSummayDict.keys():
                    self.businessLineExecuteSummayDict[tmpBusi] = {"total": 0, "pass": 0, "fail": 0, "error": 0, "notrun": 0, "failedCaseList": []}
                if tmpBusi not in self.moduleExecuteSummayDict.keys():
                    self.moduleExecuteSummayDict[tmpBusi] = {}
                if tmpModule not in self.moduleExecuteSummayDict[tmpBusi].keys():
                    self.moduleExecuteSummayDict[tmpBusi][tmpModule] = {"total": 0, "pass": 0, "fail": 0, "error": 0, "notrun": 0, "failedCaseList": []}
                if tmpInterface.testResult == ResultConst.PASS:
                    self.businessLineExecuteSummayDict[tmpBusi]['total'] += 1
                    self.businessLineExecuteSummayDict[tmpBusi]['pass'] += 1
                    self.moduleExecuteSummayDict[tmpBusi][tmpModule]['total'] += 1
                    self.moduleExecuteSummayDict[tmpBusi][tmpModule]['pass'] += 1
                elif tmpInterface.testResult == ResultConst.FAIL:
                    self.businessLineExecuteSummayDict[tmpBusi]['total'] += 1
                    self.businessLineExecuteSummayDict[tmpBusi]['fail'] += 1
                    self.businessLineExecuteSummayDict[tmpBusi]['failedCaseList'].append(tmpInterface)
                    self.moduleExecuteSummayDict[tmpBusi][tmpModule]['total'] += 1
                    self.moduleExecuteSummayDict[tmpBusi][tmpModule]['fail'] += 1
                    self.moduleExecuteSummayDict[tmpBusi][tmpModule]['failedCaseList'].append(tmpInterface)
                elif tmpInterface.testResult == ResultConst.ERROR:
                    self.businessLineExecuteSummayDict[tmpBusi]['total'] += 1
                    self.businessLineExecuteSummayDict[tmpBusi]['error'] += 1
                    self.businessLineExecuteSummayDict[tmpBusi]['failedCaseList'].append(tmpInterface)
                    self.moduleExecuteSummayDict[tmpBusi][tmpModule]['total'] += 1
                    self.moduleExecuteSummayDict[tmpBusi][tmpModule]['error'] += 1
                    self.moduleExecuteSummayDict[tmpBusi][tmpModule]['failedCaseList'].append(tmpInterface)
                else:
                    self.businessLineExecuteSummayDict[tmpBusi]['total'] += 1
                    self.businessLineExecuteSummayDict[tmpBusi]['notrun'] += 1
                    # self.businessLineExecuteSummayDict[tmpBusi]['failedCaseList'].append(tmpInterface)
                    self.moduleExecuteSummayDict[tmpBusi][tmpModule]['total'] += 1
                    self.moduleExecuteSummayDict[tmpBusi][tmpModule]['notrun'] += 1
                    # self.moduleExecuteSummayDict[tmpBusi][tmpModule]['failedCaseList'].append(tmpInterface)
