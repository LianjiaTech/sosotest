from core.tools.DBTool import DBTool
from core.const.GlobalConst import ResultConst
from core.tools.CommonFunc import *
from core.config.InitConfig import *
import pickle
from core.tools.UsualTool import UsualTool

class UITestTask(object):

    reportFileName = "report.html"
    logFileName = "report.log"
    pickleFileName = "unquitdriverlist.pkl"
    def __init__(self):
        #基本信息
        self.id = 0
        self.taskExecuteId = 0

        self.taskId = ""
        self.title = ""
        self.taskdesc = ""
        self.businessLineId = ""
        self.businessLineName = ""
        self.moduleId = ""
        self.moduleName = ""
        self.sourceGroup = ""

        self.fileName = ""
        self.fileAddBy = ""
        self.sheetName = ""
        self.httpConfKey = ""
        self.reportDir = ""

        self.packageId = ""
        self.serverId = ""
        #执行信息
        self.execStatus = 1 # 1 新建排队中未执行 2执行中 3执行完成 4执行异常
        self.execCommand = ""
        self.execStartTime = ""
        self.execEndTime = ""
        self.execTakeTime = ""
        self.execProgressString = ""
        #执行结果信息
        self.testResult = ""
        self.testResultMessage = ""

        self.execComments = ""
        self.isSendEmail = 0
        self.emailList = ""

        #通用信息
        self.state = 1
        self.addBy = ""
        self.modBy = ""
        self.addTime = ""
        self.modTime = ""

        self.globalDB = DBTool()



    def generateByTaskExecuteId(self):
        self.globalDB.initGlobalDBConf()
        self.taskExecuteId = int(self.taskExecuteId)
        sqlTasExec = "select * from tb_ui_test_execute where id=%d" % int(self.taskExecuteId)
        resTaskExec = self.globalDB.execute_sql(sqlTasExec)
        if resTaskExec:
            tmpResTaskInfo = resTaskExec[0]
            self.id = tmpResTaskInfo['id']

            self.taskId = tmpResTaskInfo['taskId']
            self.title = tmpResTaskInfo['title']
            self.taskdesc = tmpResTaskInfo['taskdesc']
            self.businessLineId = tmpResTaskInfo['businessLineId']
            self.moduleId = tmpResTaskInfo['moduleId']
            self.sourceGroup = tmpResTaskInfo['sourceGroup']

            self.fileName = tmpResTaskInfo['fileName']
            self.fileAddBy = tmpResTaskInfo["fileAddBy"]
            self.sheetName = tmpResTaskInfo['sheetName']
            self.httpConfKey = tmpResTaskInfo['httpConfKey']
            self.reportDir = tmpResTaskInfo['reportDir'].strip()
            self.addBy = tmpResTaskInfo['addBy']

            self.packageId = tmpResTaskInfo['packageId'].strip()
            self.serverId = tmpResTaskInfo["serverId"]

            self.execComments = tmpResTaskInfo['execComments']
            self.isSendEmail = int(tmpResTaskInfo['isSendEmail'])
            self.emailList = tmpResTaskInfo['emailList']

            self.testResult = tmpResTaskInfo['testResult']
            self.execStatus = tmpResTaskInfo['execStatus']

            self.generateBusinessLineAndModuleName()
        else:
            self.taskExecuteId = -1
        self.globalDB.release()


    def generateBusinessLineAndModuleName(self):
        self.globalDB.connect()
        businessLineDict = self.globalDB.execute_sql("select * from tb_business_line where id=%d" % (int(self.businessLineId)))
        moduleDict = self.globalDB.execute_sql("select * from tb_modules where id=%d" % (int(self.moduleId)))
        self.globalDB.release()
        self.businessLineName =  businessLineDict[0]['bussinessLineName']
        self.moduleName = moduleDict[0]['moduleName']

    def getPackageInfo(self):
        self.globalDB.connect()
        packageInfo = self.globalDB.execute_sql("select * from tb_ui_package where packageId='%s'" % self.packageId)
        if packageInfo:
            return packageInfo[0]
        else:
            return False

    def bindTaskMobileServer(self,taskExecuteId,serverId):
        self.globalDB.connect()
        self.globalDB.execute_sql("UPDATE tb_ui_test_execute SET serverId = %s WHERE id = %s" % (taskExecuteId,serverId))

    def getDevice(self,serverType):
        self.globalDB.connect()
        if serverType.lower() == "android":
            typeKey = 1
        elif serverType.lower() == "ios":
            typeKey = 2
        mobileServer = self.globalDB.execute_sql("select * from tb_ui_mobile_server where state = 1 and status = 0 and serverType = %s" % typeKey)
        if mobileServer:
            self.serverId = mobileServer[0]["id"]
            self.globalDB.execute_sql("UPDATE tb_ui_mobile_server SET STATUS = 1 WHERE id = %s" % mobileServer[0]["id"])
            self.globalDB.execute_sql("UPDATE tb_ui_test_execute SET serverId = %s WHERE id = %s" % (mobileServer[0]["id"],self.taskExecuteId))
            return mobileServer[0]
        else:
            return False

    def resetAppiumServer(self):
        self.globalDB.connect()
        if self.serverId != 0:
            self.globalDB.execute_sql("update tb_ui_mobile_server set status=0 where id=%d" % (int(self.serverId)))

    def execute(self):
        if self.taskExecuteId == -1:
            self.execStatus = 4
            self.setExecStatus()
            return

        self.execStatus = 2
        if self.reportDir.strip() == "":
            self.reportDir = "%s_%s" % (self.taskExecuteId , get_current_time_YYYYMMDD_HHMMSS())
        self.execStartTime = get_current_time()
        self.testResult = ResultConst.NOTRUN
        self.saveToDB()
        taskExecStartTimestamp = time.time()
        reportBaseDir = "%s/static/ui_test/reports/%s/" % (EnvConfig.WEB_ROOT, self.reportDir)  # 必须有/结尾
        excelBaseDir = "%s/ui_file_uploads/%s" % (EnvConfig.WEB_ROOT, self.fileAddBy)

        appParamString = ""
        if self.packageId != "":
            #设置定制的appParamString
            pacInfo = self.getPackageInfo()
            if pacInfo:
                if pacInfo['packageType'] == 1:
                    #android
                    appUrl = "%s/static/ui_test/app_uploads/%s/%s" % (EnvConfig.WEB_URI, pacInfo['addBy'], pacInfo['appFileName'])
                    appParamString = "--app=%s--appPackage=%s--appActivity=%s" % (appUrl,pacInfo['appPackage'],pacInfo['appActivity'])
                elif pacInfo['packageType'] == 2:
                    # iPhone
                    appUrl = "%s/static/ui_test/app_uploads/%s/%s" % (EnvConfig.WEB_URI, pacInfo['addBy'], pacInfo['appFileName'])
                    appParamString = "--app=%s--bundleId=%s" % (appUrl, pacInfo['bundleId'])
                elif pacInfo['packageType'] == 3:
                    # iPad
                    appUrl = "%s/static/ui_test/app_uploads/%s/%s" % (EnvConfig.WEB_URI, pacInfo['addBy'], pacInfo['appFileName'])
                    appParamString = "--app=%s--bundleId=%s" % (appUrl, pacInfo['bundleId'])

        execAnfReportParamInfoStr = "--filepath=%s/%s--sheetName=%s--httpConfKey=%s--reportFolder=%s" % (
            excelBaseDir,self.fileName,self.sheetName,self.httpConfKey,reportBaseDir  )

        dbParamInfoStr = "--dbMode=true--dbHost=%s--dbPort=%s--dbUsername=%s--dbPassword=%s--dbName=%s--dbTaskExecuteId=%d" % (
            DBConf.dbHost,DBConf.dbPort,DBConf.dbUsername,DBConf.dbPassword,DBConf.dbName,int(self.taskExecuteId))
        driverConfigConfStr = "--driverConfigPath=%s/RobotUiTest/DriverConfig.conf" % EnvConfig.PLATFORM_ROOT
        #如果不是app
        if self.sourceGroup == webTypeKey:
            logging.debug("web任务！")
            if isReleaseEnv:
                driverConfigConfStr = "%s--ip=%s--port=%s" % (driverConfigConfStr,driverConfDict["hub"]["ip"],driverConfDict["hub"]["port"])
            logging.debug("driverConfigConfStr %s" % driverConfigConfStr)
        if self.sourceGroup == androidTypeKey:
            logging.debug("android任务！")
            androidServer = self.getDevice("Android")
            if androidServer:
                logging.debug("发现Android设备 %s "  % androidServer["id"])
                self.bindTaskMobileServer(self.taskExecuteId,androidServer["id"])
                appParamString = "%s--ip=%s--port=%s--udid=%s--deviceName=%s" % (appParamString,androidServer["serverIp"],androidServer["serverPort"],androidServer["udid"],androidServer["deviceName"])
            else:
                #这就是没有获取到模拟器
                logging.error("没有发现Android设备 ")
                self.testResultMessage = "没获取到模拟器"
                self.execStatus = 4
                self.setExecStatus()
                self.globalDB.release()
        if self.sourceGroup == iosTypeKey:
            logging.debug("ios任务！")
            iosServer = self.getDevice("IOS")
            if iosServer:
                logging.debug("发现ios设备 %s "  % iosServer["id"])
                self.bindTaskMobileServer(self.taskExecuteId,iosServer["id"])
                appParamString = "%s--ip=%s--port=%s--udid=%s--deviceName=%s--wdaLocalPort=%s" % (appParamString,iosServer["serverIp"],iosServer["serverPort"],iosServer["udid"],iosServer["deviceName"],iosServer["wdaLocalPort"])
            else:
                #这就是没有获取到模拟器
                logging.error("没获取到ios设备 ")
                self.testResultMessage = "没获取到模拟器"
                self.execStatus = 4
                self.setExecStatus()
                self.globalDB.release()
        # if self.sourceGroup == iosTypeKey:
        #     appParamString = "%s--ip=%s--port=%s--udid=%s" % (appParamString,"10.10.20.229","9966","127.0.0.1:21503")
        pythoneExecuteString = "python3 %s/test_run/runUITest.py --print=0%s%s%s%s" %(
            EnvConfig.UI_FRAMEWORK_ROOT,execAnfReportParamInfoStr,dbParamInfoStr,driverConfigConfStr,appParamString)

        print(pythoneExecuteString)
        if isLinuxSystem():
            order =  "%s > /dev/null 2>&1 " % pythoneExecuteString
        else:
            order = "start /b %s " % pythoneExecuteString
        logging.debug(order)
        self.execCommand = "python3 runUITest.py %s%s" %( execAnfReportParamInfoStr,appParamString  ) #去掉数据库等敏感信息
        self.saveToDB()
        try:
            os.popen(order)
        except Exception as e:
            logging.error("发生执行异常")
            self.globalDB.release()
        #开始循环判断执行状态，如果状态是结束，那么结束。a d
        try:
            self.globalDB.initGlobalDBConf()
            while True:
                res = self.globalDB.execute_sql("select * from tb_ui_test_execute where id=%d" % (int(self.taskExecuteId)))
                if res:
                    resUITaskDict = res[0]
                    self.execStatus = resUITaskDict['execStatus']
                    if self.execStatus == 2 :
                        #如果在执行中，等待一会。
                        time.sleep(1)
                        continue
                    else:
                        #如果不是执行中，那就是框架反写到数据库中执行状态执行结束了。
                        self.testResult = resUITaskDict['testResult']
                        self.testResultMessage = resUITaskDict['testResultMessage']
                        #判断如果使用了模拟器把模拟器设为可用
                        break
                else:
                    #如果没有找到对应的执行状态，报异常。
                    self.execStatus = 4
                    self.testResult = ResultConst.EXCEPTION
                    self.testResultMessage = "执行异常，没有找到任务执行数据！"
                    self.saveToDB()
        finally:
            self.execEndTime = get_current_time()
            taskExecEndTimestamp = time.time()
            self.execTakeTime = str(taskExecEndTimestamp - taskExecStartTimestamp)
            self.saveExecEndTimeAndTaskTakeTimeToDB()
            if self.isSendEmail > 0:
                self.sendEmailToExecutor()
            if self.serverId != 0:
                self.resetAppiumServer()
            self.globalDB.release()



    def setExecStatus(self):
        self.globalDB.initGlobalDBConf()
        self.taskExecuteId = int(self.taskExecuteId)
        sqlTasExec = "update tb_ui_test_execute set execStatus=%d where id=%d" % (self.execStatus,int(self.taskExecuteId))
        resTaskExec = self.globalDB.execute_update_sql(sqlTasExec)
        self.globalDB.release()

    def saveReportDirToDB(self):
        self.globalDB.initGlobalDBConf()
        self.taskExecuteId = int(self.taskExecuteId)
        sqlTasExec = "update tb_ui_test_execute set reportDir='%s' where id=%d" % (self.reportDir,int(self.taskExecuteId))
        resTaskExec = self.globalDB.execute_update_sql(sqlTasExec)
        self.globalDB.release()

    def saveProgressToDB(self):
        self.globalDB.initGlobalDBConf()
        self.taskExecuteId = int(self.taskExecuteId)
        sqlTasExec = "update tb_ui_test_execute set execProgressString='%s' where id=%d" % (self.execProgressString,int(self.taskExecuteId))
        resTaskExec = self.globalDB.execute_update_sql(sqlTasExec)
        self.globalDB.release()

    def saveExecEndTimeAndTaskTakeTimeToDB(self):
        self.globalDB.initGlobalDBConf()
        self.taskExecuteId = int(self.taskExecuteId)
        saveAttrString = "execStatus=%d," % self.execStatus
        if self.execEndTime != "":
            saveAttrString += "execEndTime = '%s'," % self.execEndTime
        if self.execTakeTime != "":
            saveAttrString += "execTakeTime = '%s'," % self.execTakeTime
        try:
            if saveAttrString != "":
                saveAttrString = saveAttrString[:-1]
                sqlTasExec = "update tb_ui_test_execute set %s where id=%d" % (saveAttrString, int(self.taskExecuteId))
                res = self.globalDB.execute_update_sql(sqlTasExec)
                return res
            else:
                return False
        finally:
            self.globalDB.release()

    def cancelTask(self):
        try:
            logging.debug("当前执行状态：%s" % self.execStatus)
            if self.execStatus == 2 or self.execStatus == 10:
                if self.serverId != 0:
                    self.resetAppiumServer()
                reportBaseDir = "%s/static/ui_test/reports/%s/" % (EnvConfig.WEB_ROOT, self.reportDir)  # 必须有/结尾
                reportFileRealPath = "%s%s" % (reportBaseDir,UITestTask.reportFileName)
                pickleFileRealPath = "%s%s" % (reportBaseDir,UITestTask.pickleFileName)

                #STEP1 杀进程
                if isLinuxSystem():
                    #linux下杀进程
                    getPidCommand = "ps -ef |grep %s |grep -v grep |grep -v /dev/null" % reportBaseDir
                    logging.debug(getPidCommand)
                    pidPopenRes = os.popen(getPidCommand)
                    pidOutput = pidPopenRes.read().strip()
                    logging.debug(pidOutput)
                    retResList = pidOutput.split(" ")
                    logging.debug(retResList)
                    pidTobeKilled = 0
                    for tmpPid in retResList:
                        if isInt(tmpPid.strip()):
                            pidTobeKilled = int(tmpPid.strip())
                            break
                    logging.debug("PidTobeKilledInLinux:%d" % pidTobeKilled)
                    if pidTobeKilled > 0:
                        killRes = os.popen("kill -9 %d" % pidTobeKilled)
                        killOutputStr = killRes.read()
                        logging.info("进程[%d]killed！%s" % (pidTobeKilled,killOutputStr))
                else:
                    #windows下杀进程
                    getPidCommand = """wmic process where caption="python3.exe" get handle,caption,commandline /value"""
                    pidRes = os.popen(getPidCommand)
                    outPidTaskString = pidRes.read()
                    handleStringList = outPidTaskString.split("Handle=")
                    for i in range(0,len(handleStringList)):
                        if reportBaseDir in handleStringList[i]:
                            realWindowsPid = get_sub_string(handleStringList[i+1],"","\n").strip()
                            if isInt(realWindowsPid):
                                killRes = os.popen("taskkill /pid %s -f" % realWindowsPid)
                                kilResOutput = killRes.read()
                                logging.info("进程[%s]killed！%s" % (realWindowsPid, kilResOutput))
                # step3 更新状态先更新状态再ui出driver，因为退出driver比较慢。
                self.execStatus = 11
                self.testResult = "CANCEL"
                self.saveToDB()
                #STEP2退出未推出的driver
                try:
                    # 反序列化退出所有有效的driver
                    if os.path.exists(pickleFileRealPath) and os.path.isfile(pickleFileRealPath):
                        logging.info("任务【%s】取消，发现pickle文件！" % self.taskExecuteId)
                        # 先判断有没有pkl文件
                        #存在pkl，进行退出
                        with open(pickleFileRealPath, 'rb') as f:
                            aa = pickle.load(f)
                        for tmpDriver in aa:
                            try:
                                tmpDriver.quit()
                                logging.info("WebDriver quited!")
                            except Exception as e:
                                logging.info("WebDriver unquited! Exception occured when quit!")
                                logging.debug(traceback.format_exc())

                        os.remove(pickleFileRealPath)
                    else:
                        logging.info("任务【%s】取消，没有发现pickle文件！" % self.taskExecuteId)
                except Exception as e:
                    logging.error(str(e))





            return True
        except Exception as e:
            return False
        finally:
            self.globalDB.release()

    def saveToDB(self):
        self.globalDB.initGlobalDBConf()
        self.taskExecuteId = int(self.taskExecuteId)
        saveAttrString = "execStatus=%d," % self.execStatus
        if self.reportDir != "":
            saveAttrString += "reportDir = '%s'," % self.reportDir
        if self.execStartTime != "":
            saveAttrString += "execStartTime = '%s'," % self.execStartTime
        if self.execEndTime != "":
            saveAttrString += "execEndTime = '%s'," % self.execEndTime
        if self.execTakeTime != "":
            saveAttrString += "execTakeTime = '%s'," % self.execTakeTime
        if self.execProgressString != "":
            saveAttrString += "execProgressString = '%s'," % self.execProgressString
        if self.testResult != "":
            saveAttrString += "testResult = '%s'," % self.testResult
        if self.testResultMessage != "":
            saveAttrString += "testResultMessage = '%s'," % self.testResultMessage
        if self.execCommand != "":
            saveAttrString += "execCommand = '%s'," % self.execCommand
        try:
            if saveAttrString != "":
                saveAttrString = saveAttrString[:-1]
                sqlTasExec = "update tb_ui_test_execute set %s where id=%d" % (saveAttrString,int(self.taskExecuteId))
                res = self.globalDB.execute_update_sql(sqlTasExec)
                return res
            else:
                return False
        finally:
            self.globalDB.release()

    def sendEmailToExecutor(self):
        self.globalDB.initGlobalDBConf()
        res = self.globalDB.execute_sql("select email from tb_user where loginName='%s' " % self.addBy)
        self.globalDB.release()
        resEmailList = self.emailList
        print("self.emailList",self.emailList)
        if res:
            emailList = ""  # ;分号间隔
            if resEmailList.strip() != "":
                resEmList = resEmailList.split(",")
                for tmpMail in resEmList:
                    emailList = emailList + ";" + tmpMail
            subject = "[%s]UI任务[%s:%s]测试报告" % (self.testResult, self.taskId, self.title)
            # 开始生成emailText的html###############################################################################
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
            emailText = "<html><body style='background-color:%s;display:block;'>" % bgColor

            # 1、测试报告概况
            emailText = emailText + ("""
            <h1>（一）UI测试报告概况</h1>
            <h2>任务基本信息</h2>
            <table border="1px" cellpadding="3px" width="80%%">
            <tr><th width="20%%"  align="left">任务ID</th><td width="80%%">%s</td></tr>
            <tr><th align="left">执行环境</th><td>%s</td></tr>
            <tr><th align="left">执行时间</th><td>%s</td></tr>
            <tr><th align="left">执行结果</th><td>%s</td></tr>
            <tr><th align="left">执行耗时</th><td>%s秒</td></tr>
            <tr><th align="left">任务名称</th><td>%s</td></tr>
            <tr><th align="left">任务描述</th><td>%s</td></tr>
            <tr><th align="left">包含%s</th><td>%s</td></tr>
            <tr><th align="left">包含%s</th><td>%s</td></tr>
            <tr><th align="left">备注</th><td>%s</td></tr>
            </table>""" % (self.taskId, self.httpConfKey, self.execStartTime, self.testResult, self.execTakeTime, self.title, self.taskdesc, CommonConf.groupLevel1,
                           self.businessLineName, CommonConf.groupLevel2, self.moduleName, (self.execComments.strip() == "" and "无" or self.execComments.strip())))
            if isDictJson(self.testResultMessage):
                resDict = json.loads(self.testResultMessage)
                if resDict['caseTotalCount'] == 0:
                    caseRate = 0.00
                else:
                    caseRate = float(resDict['casePassCount'])/float(resDict['caseTotalCount'])

                if resDict['caseStepTotalCount'] == 0:
                    stepRate = 0.00
                else:
                    stepRate = float(resDict['caseStepPassCount'])/float(resDict['caseStepTotalCount'])

                # 所有统计信息开始################################################################
                emailText = emailText + "<h2>结果统计信息</h2>"
                emailText = emailText + """
    <table border="1px" cellpadding="3px" width="80%%">  
        <thead>
            <tr style="background-color:#fcf8e3;"> 
                <th width="5%%"></th>
                <th width="10%%">总计</th>
                <th width="10%%">PASS</th>
                <th width="10%%">FAIL</th>
                <th width="10%%">WARNING</th>
                <th width="10%%">通过率</th>
            </tr>
        </thead>
        <tbody>
            <tr style="background-color:%s;" id="total_summay"><td>用例</td>
                <td><bdi id="summay_totalCount">%s</bdi></td>
                <td><bdi id="summay_passCount">%s</bdi>
                <td><bdi id="summay_failCount">%s</bdi></td>
                <td><bdi id="summay_failCount">%s</bdi></td>
                <td><bdi id="summay_passPercent">%.2f%%</bdi></td></tr>
            <tr style="background-color:%s;" id="total_summay"><td>步骤</td> 
                <td><bdi id="summay_totalCount">%s</bdi></td>
                <td><bdi id="summay_passCount">%s</bdi></td>
                <td><bdi id="summay_failCount">%s</bdi></td>
                <td><bdi id="summay_failCount">%s</bdi></td>
                <td><bdi id="summay_passPercent">%.2f%%</bdi></td></tr>
        </tbody>
    </table>"""  % (bgColor,resDict['caseTotalCount'],resDict['casePassCount'],resDict['caseFailCount'],resDict['caseWarningCount'],caseRate*100,
                    bgColor,resDict['caseStepTotalCount'],resDict['caseStepPassCount'],resDict['caseStepFailCount'],resDict['caseStepWarningCount'],stepRate*100)

            else:
                # task 执行结果 结果没有返回正常的json
                emailText = emailText + self.testResultMessage + "<br>"

            # self.isSendEmail  是否发送是否带附件PassFailErrorException
            isSendMailStr = str(self.isSendEmail)
            # 不够6位后面补1
            addOneCount = 6 - len(isSendMailStr)
            for i in range(0, addOneCount):
                isSendMailStr = isSendMailStr + "1"
            if int(isSendMailStr[1]) == 1:
                emailText = emailText + "<br>详情见附件。"
            else:
                tmpurl = "%s/static/ui_test/reports/%s/report.html" % (EnvConfig.WEB_URI, self.reportDir)
                emailText = emailText + ("<br>详情见:&nbsp;&nbsp;<a href='%s'>%s</a>" % (tmpurl, tmpurl))

            emailText = emailText + "</body></html>"

            # 结束生成emailText的html###############################################################################
            # 开始发送邮件
            def subSendMail():
                if int(isSendMailStr[1]) == 1:
                    # 发送附件
                    testReportFilePath = "%s/static/ui_test/reports/%s/report.html" % (EnvConfig.WEB_ROOT, self.reportDir)
                    UsualTool.send_mail(emailList, subject, emailText,testReportFilePath, subType="html")
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
            emailList = EmailConfig.sender  # ;分号间隔
            subject = "[%s]任务[%s:%s]测试报告，没有找到收件人，执行者为%s" % (self.testResult, self.taskId, self.title, self.addBy)
            emailText = "[%s]任务[%s:%s]测试报告，没有找到收件人，执行者为%s" % (self.testResult, self.taskId, self.title, self.addBy)
            UsualTool.send_mail(emailList, subject, emailText, subType="html")


if __name__ == '__main__':
    task = UITestTask()
    task.taskExecuteId = 78
    task.generateByTaskExecuteId()
    # task.execute()
    task.cancelTask()