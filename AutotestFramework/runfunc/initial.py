import logging.handlers
from concurrent_log_handler import ConcurrentRotatingFileHandler as LogHandler
import socket,os,threading
from core.const.Do import Do
# from core.tools.UsualTool import UsualTool

from allmodels.HttpInterface import HttpInterface
from allmodels.HttpTestcase import HttpTestcase
from allmodels.Task import Task
from core.config.InitConfig import TcpServerConf,isClusterConf
from core.const.GlobalConst import ExecStatus
from core.decorator.normal_functions import *
from core.tools.DBTool import DBTool
from core.tools.RedisTool import RedisTool
from core.tools.TypeTool import TypeTool
from runfunc.runGlobalVars import *
from threads.CaseDebugThread import CaseDebugThread
from threads.TaskThread import TaskThread
from progress.TaskProgress import TaskProgress
from core.tools.CommonFunc import *
from progress.CaseDebugProcess import CaseDebugProcess
from progress.globalValFunc import *
from report.HttpTaskSuiteReport import HttpTaskSuiteReport
from core.config.InitConfig import *
from core.const.Protocol import *

@catch_exception
def init_logging(logFilePath = "test.log",level = logging.DEBUG):
    #################################################################################################
    logging.basicConfig(level=level)
    #################################################################################################
    #################################################################################################
    # 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
    Rthandler = LogHandler(logFilePath, maxBytes=10 * 1024 * 1024, backupCount=5)
    Rthandler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    Rthandler.setFormatter(formatter)
    logging.root.addHandler(Rthandler)
    #################################################################################################

# @catch_exception
# @take_time
# def init_debug_queue_interface(db):
#     colsStr = "id,addBy,httpConfKey"
#     tbName = "tb_http_interface_debug"
#     whereStr = "execStatus = %d" % ExecStatus.NOTRUN
#     orderBy = "addTime asc"
#     sql = "select %s from %s where %s order by %s" % (colsStr, tbName, whereStr, orderBy)
#     res = db.execute_sql(sql)
#     if res == False:
#         logging.error("init_debug_queue_interface: 初始化调试接口队列失败！")
#         return False
#     logging.debug("init_debug_queue_interface: 初始化tb_http_interface_debug结果：%s" % str(res))
#     for tRes in res:
#         tmpData = {}
#         tmpData[Do.KEY_DO] = Do.TYPE_DEBUG_INTERFACE
#         tmpData[Do.KEY_INTERFACE_DEBUG_ID] = tRes['id']
#         debugQueue.append(tmpData)
#         logging.debug("init_debug_queue_interface: debugQueue加入新data:%s 。来源表：%s" % (tmpData,tbName))
#         logging.debug("init_debug_queue_interface: debugQueue:%s" % debugQueue)
#
#     logging.info("init_debug_queue_interface: 初始化接口调试表完成debugQueue:%s" % debugQueue)
#
# @catch_exception
# @take_time
# def init_debug_queue_case(db):
#     #TODO 初始化 case debug
#     colsStr = "id,caseId,addBy"
#     tbName = "tb_http_testcase_debug"
#     whereStr = "execStatus = %d" % ExecStatus.NOTRUN
#     orderBy = "addTime asc"
#     sql = "select %s from %s where %s order by %s" % (colsStr, tbName, whereStr, orderBy)
#     res = db.execute_sql(sql)
#     logging.debug("init_debug_queue_case: 初始化tb_http_testcase_debug结果：%s" % str(res))
#     if res == False:
#         logging.error("init_debug_queue_case: 初始化调试用例队列失败！")
#         return False
#     for tRes in res:
#         tmpData = {}
#         tmpData[Do.KEY_DO] = Do.TYPE_DEBUG_CASE
#         tmpData[Do.KEY_CASE_DEBUG_ID] = tRes['id']
#
#         colsStr = "id"
#         tbName = "tb_http_testcase_step_debug"
#         whereStr = "caseId='%s' and addBy='%s'" % (tRes['caseId'], tRes['addBy'])
#         orderBy = "stepNum asc"
#         sql = "select %s from %s where %s order by %s" % (colsStr, tbName, whereStr, orderBy)
#         resSteps = db.execute_sql(sql)
#         caseStepDebugIdList = []
#         for tmpStepInfo in resSteps:
#             caseStepDebugIdList.append(int(tmpStepInfo['id']))
#
#         tmpData[Do.KEY_CASE_STEP_DEBUG_ID_LIST] = caseStepDebugIdList
#         debugQueue.append(tmpData)
#         logging.debug("init_debug_queue_case: debugQueue加入新data:%s 。来源表：%s" % (tmpData, tbName))
#         logging.debug("init_debug_queue_case: debugQueue:%s" % debugQueue)
#
#     logging.info("init_debug_queue_case: 初始化用例调试表完成debugQueue:%s" % debugQueue)

@catch_exception
@take_time
def init_task_queue(db,redis,taskQueueList):
    #DONE 初始化 taskrun  {'do': 3, 'TaskExecuteId': '1'}
    colsStr = "id,taskId,httpConfKey,protocol,taskSuiteExecuteId"
    tbName = "tb_task_execute"
    whereStr = "execStatus = %d or execStatus = %d " % (ExecStatus.NOTRUN, ExecStatus.RUNNING)
    orderBy = "addTime asc"
    sql = "select %s from %s where %s order by %s" % (colsStr, tbName, whereStr, orderBy)
    res = db.execute_sql(sql)
    logging.debug("init_task_queue: 初始化tb_task_execute结果：%s" % str(res))
    if res == False:
        logging.error("init_task_queue: 初始化任务执行队列失败！")
        return False
    for tRes in res:
        tmpData = {}
        tmpData[Do.KEY_DO] = Do.TYPE_TASK_EXECUTE
        tmpData[Do.KEY_TASK_EXECUTE_ID] = tRes['id']
        tmpData[Do.KEY_TASK_ID] = tRes['taskId']
        tmpData[Do.KEY_TASK_EXECUTE_ENV] = tRes['httpConfKey']
        tmpData[Do.TYPE_PROTOCOL] = tRes['protocol']
        tmpData[Do.KEY_TASK_SUITE_EXECUTE_ID] = tRes['taskSuiteExecuteId']
        tmpData["isCluster"] = 0
        taskQueueList.append(tmpData)

        logging.info("init_task_queue: taskQueue加入新data:%s 。来源表：%s" % (tmpData,tbName))
        logging.info("init_task_queue: taskQueue:%s" % taskQueueList)

        #查到的数据加到缓存里
        redis.set_data("taskExecute_%s" % tRes['id'])

    logging.info("init_task_queue: 初始化任务执行表完成taskQueue:%s" % taskQueueList)

@catch_exception
@take_time
def init_task_cancel_queue(db,redis,taskCancelQueueList):
    #DONE 初始化 taskrun  {'do': 3, 'TaskExecuteId': '1'}
    colsStr = "id,protocol"
    tbName = "tb_task_execute"
    whereStr = "execStatus = %d" % ExecStatus.CANCELING
    orderBy = "addTime asc"
    sql = "select %s from %s where %s order by %s" % (colsStr, tbName, whereStr, orderBy)
    res = db.execute_sql(sql)
    logging.debug("init_task_cancel_queue: 初始化tb_task_execute取消结果：%s" % str(res))
    if res == False:
        logging.error("init_task_cancel_queue: 初始化任务取消队列失败！")
        return False
    for tRes in res:
        tmpData = {}
        tmpData[Do.KEY_DO] = Do.TYPE_TASK_CANCEL
        tmpData[Do.KEY_TASK_EXECUTE_ID] = tRes['id']
        tmpData[Do.TYPE_PROTOCOL] = tRes['protocol']
        tmpData[isCluster] = isClusterConf.toCancel
        taskCancelQueueList.append(tmpData)
        logging.debug("init_task_cancel_queue: taskCancelQueue加入新data:%s 。来源表：%s" % (tmpData,tbName))
        logging.debug("init_task_cancel_queue: taskCancelQueue:%s" % taskCancelQueueList)

        #加入redis
        redis.set_data("taskExecute_%s" % tRes['id'])

    logging.info("init_task_cancel_queue: 初始化任务取消表完成taskCancelQueue:%s" % taskCancelQueueList)


@catch_exception
@take_time
def init_dubbo_task_queue(db,taskQueueList):
    #DONE 初始化 taskrun  {'do': 3, 'TaskExecuteId': '1'}
    colsStr = "id,taskId,httpConfKey,protocol,taskSuiteExecuteId"
    tbName = "tb2_dubbo_task_execute"
    whereStr = "execStatus = %d or execStatus = %d " % (ExecStatus.NOTRUN, ExecStatus.RUNNING)
    orderBy = "addTime asc"
    sql = "select %s from %s where %s order by %s" % (colsStr, tbName, whereStr, orderBy)
    res = db.execute_sql(sql)
    logging.debug("init_task_queue: 初始化tb_task_execute结果：%s" % str(res))
    if res == False:
        logging.error("init_task_queue: 初始化任务执行队列失败！")
        return False
    for tRes in res:
        tmpData = {}
        tmpData[Do.KEY_DO] = Do.TYPE_TASK_EXECUTE
        tmpData[Do.KEY_TASK_EXECUTE_ID] = tRes['id']
        tmpData[Do.KEY_TASK_ID] = tRes['taskId']
        tmpData[Do.KEY_TASK_EXECUTE_ENV] = tRes['httpConfKey']
        tmpData[Do.TYPE_PROTOCOL] = tRes['protocol']
        tmpData[Do.KEY_TASK_SUITE_EXECUTE_ID] = tRes['taskSuiteExecuteId']
        tmpData["isCluster"] = 0
        taskQueueList.append(tmpData)
        logging.info("init_task_queue: taskQueue加入新data:%s 。来源表：%s" % (tmpData,tbName))
        logging.info("init_task_queue: taskQueue:%s" % taskQueueList)

    logging.info("init_task_queue: 初始化任务执行表完成taskQueue:%s" % taskQueueList)

@catch_exception
@take_time
def init_dubbo_task_cancel_queue(db,taskCancelQueueList):
    #DONE 初始化 taskrun  {'do': 3, 'TaskExecuteId': '1'}
    colsStr = "id,protocol"
    tbName = "tb2_dubbo_task_execute"
    whereStr = "execStatus = %d" % ExecStatus.CANCELING
    orderBy = "addTime asc"
    sql = "select %s from %s where %s order by %s" % (colsStr, tbName, whereStr, orderBy)
    res = db.execute_sql(sql)
    logging.debug("init_task_cancel_queue: 初始化tb_task_execute取消结果：%s" % str(res))
    if res == False:
        logging.error("init_task_cancel_queue: 初始化任务取消队列失败！")
        return False
    for tRes in res:
        tmpData = {}
        tmpData[Do.KEY_DO] = Do.TYPE_TASK_CANCEL
        tmpData[Do.KEY_TASK_EXECUTE_ID] = tRes['id']
        tmpData[Do.TYPE_PROTOCOL] = tRes['protocol']
        tmpData[isCluster] = isClusterConf.toCancel
        taskCancelQueueList.append(tmpData)
        logging.debug("init_task_cancel_queue: taskCancelQueue加入新data:%s 。来源表：%s" % (tmpData,tbName))
        logging.debug("init_task_cancel_queue: taskCancelQueue:%s" % taskCancelQueueList)

    logging.info("init_task_cancel_queue: 初始化任务取消表完成taskCancelQueue:%s" % taskCancelQueueList)

@catch_exception
@take_time
def init_task_suite_queue(db,protocol):
    if protocol == "HTTP":
        taskSuiteTbName = "tb_task_suite_execute"
        taskTbName = "tb_task_execute"
    elif protocol == "DUBBO":
        taskSuiteTbName = "tb2_dubbo_task_suite_execute"
        taskTbName = "tb2_dubbo_task_execute"
    else:
        return
    colsStr = "id,taskExecuteIdList"
    whereStr = "execStatus = 1 or execStatus = 2 or execStatus = 10"
    orderBy = "addTime asc"
    sql = "select %s from %s where %s order by %s" % (colsStr, taskSuiteTbName, whereStr, orderBy)
    res = db.execute_sql(sql)
    for resIndex in res:
        if resIndex['taskExecuteIdList'] == "":
            upSql = "update %s set testResult = 'ERROR' , execStatus = 4 where id=%s" % (taskSuiteTbName,resIndex["id"])
            db.execute_sql(upSql)
        else:
            try:
                taskExecuteList = resIndex['taskExecuteIdList'].split(",")
                isDone = True
                testResultList = []
                for taskIndex in taskExecuteList:
                    taskSql = "select execStatus,testResult from %s where id = %s " % (taskTbName,taskIndex)
                    taskRes = db.execute_sql(taskSql)
                    testResultList.append(taskRes[0]["testResult"])
                    if taskRes[0]["execStatus"] == 11:
                        upSql = "update %s set testResult = 'CANCELED' , execStatus = 11 where id=%s" % (taskSuiteTbName,resIndex["id"])
                        db.execute_sql(upSql)
                        return
                    if taskRes[0]["execStatus"] != 3 and taskRes[0]["execStatus"] != 4:
                        isDone = False
                if isDone:
                    redisObj = RedisTool()
                    redisObj.initRedisConf()
                    for taskIndex in taskExecuteList:
                        try:
                            redisObj.del_data("%s_taskExecute_%s"%(protocol,taskIndex))
                            redisObj.del_data("%s_taskExecuteStatus_%s"%(protocol,taskIndex))
                            redisObj.del_data("%s_taskSuite_%s_task_%s"%(protocol,resIndex["id"],taskIndex))
                        except:
                            continue
                    print("isDone",isDone)
                    if ResultConst.ERROR in testResultList:
                        testResult = ResultConst.ERROR
                    elif ResultConst.EXCEPTION in testResultList:
                        testResult = ResultConst.EXCEPTION
                    elif ResultConst.FAIL in testResultList:
                        testResult = ResultConst.FAIL
                    elif ResultConst.WARNING in testResultList:
                        testResult = ResultConst.WARNING
                    else:
                        testResult = ResultConst.PASS
                    upSql = "update %s set testResult = '%s' , execStatus = 4 where id=%s" % (taskSuiteTbName,testResult,resIndex["id"])
                    db.execute_sql(upSql)

            except Exception:
                logging.error("任务集初始化失败")

                raise ValueError("任务集初始化失败")



@catch_exception
@take_time
def init_global_queue(taskQueueList,taskCancelQueueList):
    # taskQueue.put([])
    # taskCancelQueue.put([])
    # serviceListQueue.put([])
    redis = RedisTool()
    redis.initRedisConf()
    db = DBTool()
    db.initGlobalDBConf()
    #启动时将所有执行服务器设置为离线
    db.execute_sql("UPDATE tb_run_server_conf SET STATUS = 0 ")
    #======加入未执行的接口调试 数据表tb_http_interface_debug
    # init_debug_queue_interface(db)
    # init_debug_queue_case(db)
    init_task_queue(db,redis,taskQueueList)
    init_task_cancel_queue(db,redis,taskCancelQueueList)
    init_dubbo_task_queue(db,taskQueueList)
    init_dubbo_task_cancel_queue(db,taskCancelQueueList)
    init_task_suite_queue(db,"HTTP")
    init_task_suite_queue(db,"DUBBO")
    db.release()



@catch_exception
def generateHttpReport(taskSuiteDict):
    """
    生成测试报告
    Returns:

    """
    reportFolderName = "reports"

    reportFolder = "%s/%s" % (LogConfig.dirfilePath, reportFolderName)
    if os.path.exists(reportFolder) == False:
        os.mkdir(reportFolder)
    dateFolderName = get_current_time_YYYYMMDD()
    dateFolder = "%s/%s" % (reportFolder, dateFolderName)
    if os.path.exists(dateFolder) == False:
        os.mkdir(dateFolder)
    fileName = "HTTP_TASK_SUITE_%s_%s_%s.html" % (taskSuiteDict["id"],taskSuiteDict["taskSuiteId"],get_current_time_YYYYMMDDHHMMSS())
    testReportFilePath = "%s/%s" % (dateFolder,fileName)
    testReportUrl = "/%s/%s/%s" % (reportFolderName, dateFolderName, fileName)
    try:
        if HttpTaskSuiteReport().createHttpReportByTask(taskSuiteDict,testReportFilePath):
            if isReleaseEnv:
                if CommonConf.http_report_to_AWS == "1":
                    try:
                        os.system("aws s3 cp %s s3://test-team/http_interface_report/" % testReportFilePath)
                        testReportUrl = "https://test.domain.com/http_interface_report/%s" % fileName
                    except:
                        logging.error("scp到AWS发生异常%s" % traceback.format_exc())
                        testReportUrl = "/%s/%s/%s" % (reportFolderName, dateFolderName, fileName)
            else:
                #非正式环境，要把测试报告传回本机
                #当前执行机不是main主机，要把测试报告发送回去
                if sendFtp(TcpServerConf.ip,"setAPITaskReports","setAPITaskReports",dateFolderName,fileName,testReportFilePath):
                    # logging.info("测试报告从执行机传输到主服务器执行完毕")
                    pass
                else:
                    logging.error("测试报告从执行机传输到主服务器失败")
            taskSuiteDict["testReportUrl"] = testReportUrl
            return True,testReportUrl
        else:
            return False,testReportUrl
    except Exception:
        logging.error(traceback.format_exc())
        return False,testReportUrl


@catch_exception
def sendEmailToExecutor(taskSuiteDict):
    resEmailList = taskSuiteDict["emailList"].split(",")
    if len(resEmailList) > 0:
        emailList = ""
        for tmpMail in resEmailList:
            emailList = emailList + ";" + tmpMail
        subject = "[%s]任务[%s:%s]测试报告" % (taskSuiteDict["testResult"], taskSuiteDict["taskSuiteId"], taskSuiteDict["title"])
        if emailList == "":
            logging.info("邮箱列表为空，不执行邮件发送")
            return
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
        if taskSuiteDict["testResult"] == "PASS":
            bgColor = "#dff0d8"
        emailText = "<html><body style='background-color:%s;display:block;'>" % bgColor

        # 1、测试报告概况
        emailText = emailText + ("""
            <h1>（一）测试报告概况</h1>
            <h2>任务集基本信息</h2>
            <table border="1px" cellpadding="3px" width="80%%">
            <tr><th width="20%%"  align="left">任务集ID</th><td width="80%%">%s</td></tr>
            <tr><th align="left">执行环境</th><td>%s</td></tr>
            <tr><th align="left">执行结果</th><td>%s</td></tr>
            <tr><th align="left">任务集名称</th><td>%s</td></tr>
            <tr><th align="left">任务集描述</th><td>%s</td></tr>
            <tr><th align="left">备注</th><td>%s</td></tr>
            </table>""" % (
            taskSuiteDict["taskSuiteId"], taskSuiteDict["httpConfKeyAliasList"],  taskSuiteDict["testResult"],
            taskSuiteDict["title"], taskSuiteDict["taskSuiteDesc"],
        (taskSuiteDict["execComments"].strip() == "" and "无" or taskSuiteDict["execComments"].strip())))
        if isDictJson(taskSuiteDict["testResultMsg"]):
            resDict = json.loads(taskSuiteDict["testResultMsg"])
            # 所有统计信息开始################################################################
            emailText = emailText + "<h2>所有统计</h2>"
            emailText = emailText + """<table border="1px" cellpadding="3px" width="80%%">"""

            if resDict['task']['total'] > 0:
                emailText = emailText + """<tr><th align="left" width="20%%">所有任务统计</th><td width="80%%">任务总数%d个，通过%d，失败%d，通过率%.2f%%。</td></tr>""" \
                                        % (resDict['task']['total'],
                                           resDict['task']['PASS'],
                                           resDict['task']['FAIL'],
                                           (float(resDict['task']['PASS']) / float(resDict['task']['total']) * 100)
                                           )

            emailText = emailText + """</table>"""
            # 所有统计信息结束################################################################

            emailText = emailText + "<h1>任务列表</h1>"
            # 列出失败的接口+===========================================================================
            emailText = emailText + """<table border="1px" cellpadding="3px" width="80%%">"""
            emailText = emailText + """<tr><th width="20%%" align="left">任务ID</th>
            <th width="15%%" align="left">名称</th>
            <th width="15%%" align="left">环境</th>
            <th width="15%%" align="left">通过率</th>
            <th width="15%%" align="left">结果</th>
            <th width="20%%" align="left">报告</th></tr>"""
            for tmpTask in resDict["taskList"]:
                emailText = emailText + ("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s%%</td><td>%s</td><td><a href='%s' target='_blank'>查看报告</a></td></tr>" % (
                    tmpTask["taskId"],
                    tmpTask["taskName"],
                    tmpTask["httpConfKey"],
                    tmpTask['executeSummary']['total'] > 0 and "%.2f" % (float(tmpTask['executeSummary']['pass']) / float(tmpTask['executeSummary']['total']) * 100)
                    or 0,
                    tmpTask["testResult"],
                    tmpTask["testReportUrl"].startswith("http") and tmpTask["testReportUrl"] or EnvConfig.WEB_URI + tmpTask["testReportUrl"]))


            emailText = emailText + """</table>"""
            # 列出失败的接口结束+=======================================================================


        else:
            # task 执行结果 结果没有返回正常的json
            emailText = emailText + taskSuiteDict["testResultMsg"] + "<br>"

        # self.isSendEmail  是否发送是否带附件PassFailErrorException
        isSendMailStr = str(taskSuiteDict["isSendEmail"])
        # 不够6位后面补1
        addOneCount = 6 - len(isSendMailStr)
        for i in range(0, addOneCount):
            isSendMailStr = isSendMailStr + "1"
        if int(isSendMailStr[1]) == 1:
            emailText = emailText + "<br>详情见链接。"
        else:
            if isReleaseEnv and CommonConf.http_report_to_AWS == "1":
                    tmpurl = taskSuiteDict["testReportUrl"]
            else:
                tmpurl = EnvConfig.WEB_URI + taskSuiteDict["testReportUrl"]
            emailText = emailText + ("<br>详情见:&nbsp;&nbsp;<a href='%s'>%s</a>" % (tmpurl, tmpurl))

        emailText = emailText + "</body></html>"

        # 结束生成emailText的html###############################################################################
        # 开始发送邮件
        from core.tools.UsualTool import UsualTool

        def subSendMail():
            # if int(isSendMailStr[1]) == 1:
            #     # 发送附件
            #     UsualTool.send_mail(emailList, subject, emailText, self.testReportFilePath, subType="html")
            # else:
            #     # 不发送附件
            UsualTool.send_mail(emailList, subject, emailText, subType="html")

        if taskSuiteDict["testResult"] == ResultConst.PASS and int(isSendMailStr[2]) == 1:
            subSendMail()
        elif taskSuiteDict["testResult"] == ResultConst.FAIL and int(isSendMailStr[3]) == 1:
            subSendMail()
        elif taskSuiteDict["testResult"] == ResultConst.ERROR and int(isSendMailStr[4]) == 1:
            subSendMail()
        elif taskSuiteDict["testResult"] == ResultConst.EXCEPTION and int(isSendMailStr[5]) == 1:
            subSendMail()
    else:
        emailList = EmailConfig.sender  # ;分号间隔
        subject = "[%s]任务[%s:%s]测试报告，没有找到收件人，执行者为%s" % (taskSuiteDict["testResult"], taskSuiteDict["taskSuiteId"], taskSuiteDict["title"], taskSuiteDict["execBy"])
        emailText = "[%s]任务[%s:%s]测试报告，没有找到收件人，执行者为%s" % (taskSuiteDict["testResult"], taskSuiteDict["taskSuiteId"], taskSuiteDict["title"], taskSuiteDict["execBy"])
        from core.tools.UsualTool import UsualTool
        UsualTool.send_mail(emailList, subject, emailText, subType="html")


@catch_exception
@take_time
def cancelTaskSuite(dataDict):
    try:
        redisCache = RedisTool()
        redisCache.initRedisConf()

        db = DBTool()
        db.initGlobalDBConf()

        # taskExecStatus = json.loads(redisCache.get_data("%s_taskSuite_%s_task_%s" % (dataDict[Do.TYPE_PROTOCOL],dataDict[Do.KEY_TASK_SUITE_EXECUTE_ID], dataDict[Do.KEY_TASK_EXECUTE_ID])))
        # taskExecStatus["execStatus"] = ExecStatus.CANCELED
        # redisCache.set_data("%s_taskSuite_%s_task_%s" % (dataDict[Do.TYPE_PROTOCOL],dataDict[Do.KEY_TASK_SUITE_EXECUTE_ID], dataDict[Do.KEY_TASK_EXECUTE_ID]),json.dumps(taskExecStatus),60*60*12)
        redisCache.del_data("%s_taskSuite_%s_task_%s" % (dataDict[Do.TYPE_PROTOCOL],dataDict[Do.KEY_TASK_SUITE_EXECUTE_ID], dataDict[Do.KEY_TASK_EXECUTE_ID]))

    finally:
    #将任务集设置为已取消
        if dataDict[Do.TYPE_PROTOCOL] == Protocol.HTTP_PROTOCOL:
            db.execute_sql("UPDATE tb_task_suite_execute SET execStatus = '%s' where id = %s" % (ExecStatus.CANCELED,dataDict[Do.KEY_TASK_SUITE_EXECUTE_ID]))
        elif dataDict[Do.TYPE_PROTOCOL] == Protocol.DUBBO_PROTOCOL:
            db.execute_sql("UPDATE tb2_dubbo_task_suite_execute SET execStatus = '%s' where id = %s" % (ExecStatus.CANCELED, dataDict[Do.KEY_TASK_SUITE_EXECUTE_ID]))
        db.release()

@catch_exception
@take_time
def run_server_restart(serverDataDict):
    tcpStr = '{"do":%s,"%s":"%s","%s":%s}' % (Do.TYPE_RUN_SERVICE_RESTART,Do.KEY_RUN_SERVICE_IP,serverDataDict[Do.KEY_RUN_SERVICE_IP],Do.KEY_RUN_SERVICE_PORT,serverDataDict[Do.KEY_RUN_SERVICE_PORT])
    if sendTcp(TcpServerConf.ip,TcpServerConf.port,tcpStr):
        logging.info("重启请求发送成功")
        # #发送数据上报
        # dataReportTcpStr = '{"do":%s,"%s":"%s","%s":%s,"%s":%s,"%s":%s,"%s":%s,"%s":%s}' % (
        #     Do.TYPE_RUN_SERVICE_DATA_REPORT,Do.KEY_RUN_SERVICE_IP,serverDataDict[Do.KEY_RUN_SERVICE_IP],Do.KEY_RUN_SERVICE_PORT,serverDataDict[Do.KEY_RUN_SERVICE_PORT],Do.KEY_RUN_SERVICE_MAX_PROGRESS_NUM,
        #     serverDataDict[Do.KEY_RUN_SERVICE_MAX_PROGRESS_NUM],Do.KEY_RUN_SERVICE_CURRENT_PROGRESS_NUM,
        #     serverDataDict[Do.KEY_RUN_SERVICE_CURRENT_PROGRESS_NUM],Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST,
        #     serverDataDict[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST],Do.KEY_RUN_SERVICE_CURRENT_CASE_LIST,serverDataDict[Do.KEY_RUN_SERVICE_CURRENT_CASE_LIST])
        # if sendTcp(TcpServerConf.ip,TcpServerConf.port,dataReportTcpStr):
        #     logging.info("服务数据上报发送成功")
        # else:
        #     logging.error("服务数据上报发送失败")

    else:
        logging.error("服务重启请求发送失败")