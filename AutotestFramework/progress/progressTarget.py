import traceback
from runfunc.runGlobalVars import isCluster
from core.const.Do import *
from runfunc.initial import *
from core.const.Protocol import Protocol
from allmodels.DubboInterface import DubboInterface
from allmodels.DubboTestcase import DubboTestcase




def taskStetusProregss(taskStatusList,taskQueueList,taskCancelQueueList,serviceList):
    while True:
        try:
            taskStatusIndex = 0
            if len(taskStatusList) > taskStatusIndex:
                dataDict = taskStatusList[taskStatusIndex]
                if dataDict[Do.KEY_DO] == Do.TYPE_TASK_EXECUTE:
                    alreadyExecute = False
                    taskQueueIndex = 0
                    while taskQueueIndex < len(taskQueueList):
                        taskQueueIndexDict = taskQueueList[taskQueueIndex]
                        if dataDict[Do.KEY_TASK_EXECUTE_ID] == taskQueueIndexDict[Do.KEY_TASK_EXECUTE_ID]:
                            alreadyExecute = True
                            break
                        taskQueueIndex += 1
                    if not alreadyExecute:
                        logging.info("可以执行 加入list %s " % dataDict)
                        taskQueueList.append(dataDict)
                    else:
                        logging.info("!!!不可以执行 加入list %s " % dataDict)
                        logging.info("当前执行的是 %s " % taskQueueList)

                #任务初始化完毕
                elif dataDict[Do.KEY_DO] == Do.TYPE_TASK_INIT_DONE:
                    dataDict[isCluster] = isClusterConf.runTaskInitDone
                    taskQueueIndex = 0
                    while taskQueueIndex < len(taskQueueList):
                        taskQueueIndexDict = taskQueueList[taskQueueIndex]
                        if taskQueueIndexDict[Do.KEY_TASK_EXECUTE_ID] == dataDict[Do.KEY_TASK_EXECUTE_ID] and taskQueueIndexDict[Do.TYPE_PROTOCOL] == dataDict[Do.TYPE_PROTOCOL]:
                            if taskQueueIndexDict[isCluster] == isClusterConf.runTcpSend:
                                taskQueueIndexDict[isCluster] = isClusterConf.runTaskInitDone
                                taskQueueList[taskQueueIndex] = taskQueueIndexDict
                                logging.info("任务%s 初始化完成" % dataDict[Do.KEY_TASK_EXECUTE_ID])
                            break
                        taskQueueIndex += 1

                #任务执行完毕
                elif dataDict[Do.KEY_DO] == Do.TYPE_TASK_EXECUTE_DONE:
                    logging.info("Main:任务执行完成 %s " % dataDict)
                    dataDict[isCluster] = isClusterConf.runTaskDone
                    taskQueueIndex = 0
                    while taskQueueIndex < len(taskQueueList):
                        taskQueueIndexDict = taskQueueList[taskQueueIndex]
                        if dataDict[Do.KEY_TASK_EXECUTE_ID] == taskQueueIndexDict[Do.KEY_TASK_EXECUTE_ID]:
                            taskQueueIndexDict[isCluster] = isClusterConf.runTaskDone
                            taskQueueList[taskQueueIndex] = taskQueueIndexDict
                            logging.info("任务状态监听进程已经安排为执行完毕 %s " % dataDict)
                            break
                        taskQueueIndex += 1
                    for serviceIndex in range(0, len(serviceList)):
                        tmpServiceIndex = serviceList[serviceIndex]
                        if "%s_%s" % (dataDict[Do.TYPE_PROTOCOL], dataDict[Do.KEY_TASK_EXECUTE_ID]) in tmpServiceIndex[
                            Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST]:
                            tmpServiceIndex[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST].remove("%s_%s" % (dataDict[Do.TYPE_PROTOCOL], dataDict[Do.KEY_TASK_EXECUTE_ID]))
                            tmpServiceIndex[Do.KEY_RUN_SERVICE_CURRENT_TASK_PROGRESS_NUM] -= 1
                            serviceList[serviceIndex] = tmpServiceIndex
                            break
                    if Do.KEY_TASK_SUITE_EXECUTE_ID in dataDict.keys() and int(dataDict[Do.KEY_TASK_SUITE_EXECUTE_ID]) != 0:
                        lastTask = True
                        taskSuiteExecuteId = dataDict[Do.KEY_TASK_SUITE_EXECUTE_ID]
                        lastTaskExecuteId = dataDict[Do.KEY_TASK_EXECUTE_ID]
                        redisCache = RedisTool()
                        redisCache.initRedisConf()
                        if dataDict[Do.TYPE_PROTOCOL] == Protocol.HTTP_PROTOCOL:
                            taskExecuteTableName = "tb_task_execute"
                            taskSuiteExecuteTableName = "tb_task_suite_execute"
                        elif dataDict[Do.TYPE_PROTOCOL] == Protocol.DUBBO_PROTOCOL:
                            taskExecuteTableName = "tb2_dubbo_task_execute"
                            taskSuiteExecuteTableName = "tb2_dubbo_task_suite_execute"
                        else:
                            lastTask = False
                        try:
                            taskSuiteExecuteData = json.loads(redisCache.get_data("%s_taskSuiteExecuteId_%s" % (dataDict[Do.TYPE_PROTOCOL], taskSuiteExecuteId)))
                        except:
                            db = DBTool()
                            db.initGlobalDBConf()
                            try:
                                tmpTaskExecuteIdList = db.execute_sql( "select taskExecuteIdList from %s where id = %s" % (taskSuiteExecuteTableName, taskSuiteExecuteId))[0]["taskExecuteIdList"].split(",")
                                taskSuiteExecuteData = {"taskExecuteIdList":tmpTaskExecuteIdList}
                            except:
                                taskSuiteExecuteData = {"taskExecuteIdList": []}
                            finally:
                                db.release()

                        progressList = []
                        testResultList = []
                        for taskIndex in taskSuiteExecuteData["taskExecuteIdList"]:
                            try:
                                taskExecStatus = json.loads(redisCache.get_data("%s_taskSuite_%s_task_%s" % (dataDict[Do.TYPE_PROTOCOL], taskSuiteExecuteId, taskIndex)))
                                testResultList.append(taskExecStatus["testResult"])
                                if taskExecStatus["execStatus"] != ExecStatus.DONE:
                                    if taskExecStatus["execStatus"] != ExecStatus.EXCEPTION:
                                        if taskExecStatus["execStatus"] != ExecStatus.CANCELED:
                                            lastTask = False
                                            progressList.append(int(taskExecStatus["progress"]))
                            except:
                                db = DBTool()
                                db.initGlobalDBConf()
                                #拿不到 说明还没开始执行
                                try:
                                    testResultList.append(db.execute_sql("select execStatus from %s where id=%s" % (taskExecuteTableName, taskIndex))[0]["testResult"])
                                except:
                                    progressList.append(0)
                                    logging.info("检测到同一任务集 有的执行完了 %s还没开始  将任务集执行进度设置为0 taskExecuteTableName:  %s " % (taskIndex,taskExecuteTableName))
                                    lastTask = False
                                db.release()
                        if lastTask:
                            try:
                                db = DBTool()
                                db.initGlobalDBConf()

                                taskListTestResult = {}
                                taskListTestResult["testResult"] = ""
                                taskListTestResult["task"] = {}
                                taskListTestResult["task"]["total"] = 0
                                taskListTestResult["task"][ResultConst.PASS] = 0
                                taskListTestResult["task"][ResultConst.FAIL] = 0
                                taskListTestResult["task"][ResultConst.ERROR] = 0
                                taskListTestResult["task"][ResultConst.EXCEPTION] = 0
                                taskListTestResult["task"][ResultConst.CANCELED] = 0
                                taskListTestResult["caseTotal"] = 0
                                taskListTestResult["casePass"] = 0
                                taskListTestResult["caseFail"] = 0
                                taskListTestResult["caseError"] = 0
                                taskListTestResult["caseNnotrun"] = 0
                                taskListTestResult["casePerformanceTotal"] = 0
                                taskListTestResult["casePerformancePass"] = 0
                                taskListTestResult["casePerformanceFail"] = 0
                                taskListTestResult["taskList"] = []

                                for taskIndex in taskSuiteExecuteData["taskExecuteIdList"]:
                                    redisCache.del_data("%s_taskSuite_%s_task_%s" % (dataDict[Do.TYPE_PROTOCOL], taskSuiteExecuteId, taskIndex))
                                    thisTask = db.execute_sql("select id,title,taskId,testResult,testResultMsg,testReportUrl,httpConfKey from %s where id=%s" % (taskExecuteTableName, taskIndex))

                                    if thisTask[0]["testResult"] not in taskListTestResult["task"].keys():
                                        taskListTestResult["task"][thisTask[0]["testResult"]] = 0
                                    try:
                                        thisTaskResultMsg = json.loads(thisTask[0]["testResultMsg"])
                                        taskListTestResult["caseTotal"] += thisTaskResultMsg["totalExecuteSummary"]['total']
                                        taskListTestResult["casePass"] += thisTaskResultMsg["totalExecuteSummary"]['pass']
                                        taskListTestResult["caseFail"] += thisTaskResultMsg["totalExecuteSummary"]['fail']
                                        taskListTestResult["caseError"] += thisTaskResultMsg["totalExecuteSummary"]['error']
                                        taskListTestResult["caseNnotrun"] += thisTaskResultMsg["totalExecuteSummary"]['notrun']
                                        if dataDict[Do.TYPE_PROTOCOL] == Protocol.HTTP_PROTOCOL:
                                            taskListTestResult["casePerformanceTotal"] += thisTaskResultMsg["actualTotalPerformanceDict"]['total']
                                            taskListTestResult["casePerformancePass"] += thisTaskResultMsg["actualTotalPerformanceDict"]['pass']
                                            taskListTestResult["casePerformanceFail"] += thisTaskResultMsg["actualTotalPerformanceDict"]['fail']
                                            actualTotalPerformanceDict = thisTaskResultMsg["actualTotalPerformanceDict"]
                                        else:
                                            actualTotalPerformanceDict = {}

                                        taskListTestResult["taskList"].append(
                                            {"id": thisTask[0]["id"], "taskId": thisTask[0]["taskId"],
                                             "testResult": thisTask[0]["testResult"],
                                             "executeSummary": thisTaskResultMsg["totalExecuteSummary"],
                                             "testReportUrl": thisTask[0]["testReportUrl"],
                                             "taskName": thisTask[0]["title"],
                                             "httpConfKey": thisTask[0]["httpConfKey"],
                                             "actualTotalPerformanceDict": actualTotalPerformanceDict})
                                    except Exception:
                                        taskListTestResult["taskList"].append({"taskId": thisTask[0]["taskId"], "testResult": "CANCEL"})
                                    taskListTestResult["task"][thisTask[0]["testResult"]] += 1
                                    taskListTestResult["task"]["total"] += 1
                                redisCache.del_data("%s_taskSuiteExecuteId_%s" % (dataDict[Do.TYPE_PROTOCOL], taskSuiteExecuteId))
                                if ResultConst.CANCELED in testResultList:
                                    testResult = ResultConst.CANCELED
                                elif ResultConst.ERROR in testResultList:
                                    testResult = ResultConst.ERROR
                                elif ResultConst.EXCEPTION in testResultList:
                                    testResult = ResultConst.EXCEPTION
                                elif ResultConst.FAIL in testResultList:
                                    testResult = ResultConst.FAIL
                                elif ResultConst.WARNING in testResultList:
                                    testResult = ResultConst.WARNING
                                else:
                                    testResult = ResultConst.PASS
                                taskListTestResult["testResult"] = testResult
                                taskSuiteResult = db.execute_sql("select execTime from %s where id = %s" % (taskSuiteExecuteTableName, taskSuiteExecuteId))[0]
                                lastTaskData = db.execute_sql("select execFinishTime from %s where id=%s" % (taskExecuteTableName, lastTaskExecuteId))[0]
                                execTakeTime = (lastTaskData["execFinishTime"] - taskSuiteResult["execTime"]).seconds
                                db.execute_sql("update %s set testResult = '%s',testResultMsg = '%s',execTakeTime = '%s',execFinishTime = '%s' where id = %s" % (
                                        taskSuiteExecuteTableName, testResult,
                                        json.dumps(taskListTestResult, ensure_ascii=False), execTakeTime,
                                        lastTaskData["execFinishTime"], taskSuiteExecuteId))
                                taskSuiteResult = db.execute_sql("select * from %s where id = %s" % (taskSuiteExecuteTableName, taskSuiteExecuteId))[0]
                                taskSuiteResult['testResultMsg'] = json.dumps(taskListTestResult, ensure_ascii=False)
                                # 生成报告
                                result, url = generateHttpReport(taskSuiteResult)
                                if result:
                                    db.execute_sql(
                                        "update %s set execStatus = %s,testReportUrl = '%s' where id = %s" % (
                                            taskSuiteExecuteTableName, ExecStatus.DONE, url, taskSuiteExecuteId))
                                else:
                                    db.execute_sql(
                                        "update %s set execStatus = %s,testReportUrl = '%s' where id = %s" % (
                                            taskSuiteExecuteTableName, ExecStatus.EXCEPTION, url, taskSuiteExecuteId))
                                # 发送邮件
                                if int(taskSuiteResult["isSendEmail"]) > 0 and taskSuiteResult["emailList"] != "" and len(taskListTestResult["taskList"]) > 0:
                                    sendEmailToExecutor(taskSuiteResult)

                            except Exception:
                                logging.error("任务集报告生成失败%s" % traceback.format_exc())
                                db.execute_sql("update %s set testResult = '%s',execStatus = %s where id = %s" % (
                                        taskSuiteExecuteTableName, ResultConst.ERROR, ExecStatus.EXCEPTION,taskSuiteExecuteId))
                            finally:
                                db.release()
                        else:

                            progressList.sort(reverse=True)
                            try:
                                taskSuiteExecuteData["progress"] = progressList[0]
                            except Exception:
                                taskSuiteExecuteData["progress"] = 0
                            redisCache.set_data("%s_taskSuiteExecuteId_%s" % (dataDict[Do.TYPE_PROTOCOL], taskSuiteExecuteId),json.dumps(taskSuiteExecuteData))

                elif dataDict[Do.KEY_DO] == Do.TYPE_TASK_CANCEL:

                    if dataDict not in taskCancelQueueList:
                        taskQueueIndex = 0
                        while taskQueueIndex < len(taskQueueList):
                            taskQueueIndexDict = taskQueueList[taskQueueIndex]
                            if taskQueueIndexDict[Do.KEY_TASK_EXECUTE_ID] == dataDict[Do.KEY_TASK_EXECUTE_ID]:
                                if taskQueueIndexDict[isCluster] == isClusterConf.notRun:
                                    taskQueueIndexDict[isCluster] = isClusterConf.toCancel
                                    taskQueueList[taskQueueIndex] = taskQueueIndexDict
                                break
                            taskQueueIndex += 1
                        taskCancelQueueList.append(dataDict)
                    if Do.KEY_TASK_SUITE_EXECUTE_ID in dataDict.keys() and int(dataDict[Do.KEY_TASK_SUITE_EXECUTE_ID]) != 0:
                        redisCache = RedisTool()
                        redisCache.initRedisConf()
                        try:
                            taskSuiteExecuteData = json.loads(redisCache.get_data("%s_taskSuiteExecuteId_%s" % (
                                dataDict[Do.TYPE_PROTOCOL], dataDict[Do.KEY_TASK_SUITE_EXECUTE_ID])))
                        except:
                            taskSuiteExecuteData = {"taskExecuteIdList": [], "execStatus": 1, "progress": 0}
                        taskSuiteExecuteData["execStatus"] = ExecStatus.CANCELED
                        redisCache.set_data(
                            "%s_taskSuiteExecuteId_%s" % (dataDict[Do.TYPE_PROTOCOL], dataDict[Do.KEY_TASK_SUITE_EXECUTE_ID]),
                            json.dumps(taskSuiteExecuteData))
                        cancelTaskSuite(dataDict)
                    logging.debug("startServer: 任务取消加入taskCancelQueue！")


                #任务取消完毕
                elif dataDict[Do.KEY_DO] == Do.TYPE_TASK_CANCEL_DONE:
                    print("============================")
                    taskQueueIndex = 0
                    while taskQueueIndex < len(taskQueueList):
                        taskQueueIndexDict = taskQueueList[taskQueueIndex]
                        if taskQueueIndexDict[Do.KEY_TASK_EXECUTE_ID] == dataDict[Do.KEY_TASK_EXECUTE_ID]:
                            taskQueueIndexDict[isCluster] = isClusterConf.cancelTaskDone
                            taskQueueList[taskQueueIndex] = taskQueueIndexDict

                        taskQueueIndex += 1
                    for serviceIndex in range(0, len(serviceList)):
                        tmpServiceIndex = serviceList[serviceIndex]
                        if "%s_%s" % (dataDict[Do.TYPE_PROTOCOL], dataDict[Do.KEY_TASK_EXECUTE_ID]) in tmpServiceIndex[
                            Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST]:
                            tmpServiceIndex[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST].remove(
                                "%s_%s" % (dataDict[Do.TYPE_PROTOCOL], dataDict[Do.KEY_TASK_EXECUTE_ID]))
                            tmpServiceIndex[Do.KEY_RUN_SERVICE_CURRENT_TASK_PROGRESS_NUM] -= 1
                            serviceList[serviceIndex] = tmpServiceIndex
                    if Do.KEY_TASK_SUITE_EXECUTE_ID in dataDict.keys() and int(dataDict[Do.KEY_TASK_SUITE_EXECUTE_ID]) != 0:
                        try:
                            redisCache = RedisTool()
                            redisCache.initRedisConf()
                            redisCache.del_data("%s_taskSuiteExecuteId_%s" % (dataDict[Do.TYPE_PROTOCOL], dataDict[Do.KEY_TASK_SUITE_EXECUTE_ID]))
                            cancelTaskSuite(dataDict)

                        except Exception:
                            print(traceback.format_exc())
                            logging.error("任务取消时设置任务集状态失败")
                    logging.info("taskExecuteDone: 任务取消完毕 %s " % dataDict)
                elif dataDict[Do.KEY_DO] == Do.TYPE_WEB_DELETE_SERVICE_INDEX:
                    taskQueueIndex = 0
                    while taskQueueIndex < len(taskQueueList):
                        taskQueueIndexDict = taskQueueList[taskQueueIndex]
                        if dataDict[Do.KEY_TASK_EXECUTE_ID] == taskQueueIndexDict[Do.KEY_TASK_EXECUTE_ID]:
                            taskQueueIndexDict[isCluster] = isClusterConf.runTaskDone
                            taskQueueList[taskQueueIndex] = taskQueueIndexDict
                            logging.info("任务状态监听进程已经安排为执行完毕 %s " % dataDict)
                            break
                        taskQueueIndex += 1
                #执行完 删除元素
                taskStatusList.pop(taskStatusIndex)
                logging.info("taskStatusList 删除后 ： %s"  % taskStatusList )

            else:
                time.sleep(1)
        except Exception as e:
            logging.error("taskStatusList发生异常 %s " % traceback.format_exc())

def debugStatusProgress(debugStatusList,debugQueueList,serviceList):
    while True:
        try:
            debugStatusIndex = 0
            if len(debugStatusList) > debugStatusIndex:
                dataDict = debugStatusList[debugStatusIndex]

                #接口调试请求
                if dataDict[Do.KEY_DO] == Do.TYPE_DEBUG_INTERFACE:
                    if dataDict[Do.TYPE_PROTOCOL] == Protocol.HTTP_PROTOCOL:
                        httpInterface = HttpInterface(interfaceDebugId=dataDict[Do.KEY_INTERFACE_DEBUG_ID])
                        httpInterface.generateByInterfaceDebugId()
                        if httpInterface.execStatus != 1:
                            logging.info("没有查到接口调试信息interfaceDebugId[%s]" % dataDict[Do.KEY_INTERFACE_DEBUG_ID])
                        else:
                            dataDict[isCluster] = isClusterConf.notRun
                            debugQueueList.append(dataDict)
                    elif dataDict[Do.TYPE_PROTOCOL] == Protocol.DUBBO_PROTOCOL:
                        dubboInterface = DubboInterface(interfaceDebugId=dataDict[Do.KEY_INTERFACE_DEBUG_ID])
                        dubboInterface.generateByInterfaceDebugIdForRedis()
                        if dubboInterface.execStatus != 1:
                            logging.info("没有查到接口调试信息interfaceDebugId[%s]" % dataDict[Do.KEY_INTERFACE_DEBUG_ID])
                        else:
                            dataDict[isCluster] = isClusterConf.notRun
                            debugQueueList.append(dataDict)
                elif dataDict[Do.KEY_DO] == Do.TYPE_DEBUG_INTERFACE_DONE:
                    for debugIndex in range(0, len(debugQueueList)):
                        tmpDebugIndex = debugQueueList[debugIndex]
                        if Do.KEY_INTERFACE_DEBUG_ID in tmpDebugIndex.keys() and tmpDebugIndex[
                            Do.KEY_INTERFACE_DEBUG_ID] == dataDict[
                            Do.KEY_INTERFACE_DEBUG_ID] and tmpDebugIndex[Do.TYPE_PROTOCOL] == dataDict[
                            Do.TYPE_PROTOCOL]:
                            tmpDebugIndex[isCluster] = isClusterConf.runDebugDone
                            debugQueueList[debugIndex] = tmpDebugIndex
                            break

                    for serviceIndex in range(0, len(serviceList)):
                        tmpServiceIndex = serviceList[serviceIndex]
                        if "%s_%s" % (dataDict[Do.TYPE_PROTOCOL], dataDict[Do.KEY_INTERFACE_DEBUG_ID]) in \
                                tmpServiceIndex[
                                    Do.KEY_RUN_SERVICE_CURRENT_CASE_LIST]:
                            tmpServiceIndex[Do.KEY_RUN_SERVICE_CURRENT_CASE_LIST].remove(
                                "%s_%s" % (dataDict[Do.TYPE_PROTOCOL], dataDict[Do.KEY_INTERFACE_DEBUG_ID]))
                            tmpServiceIndex[Do.KEY_RUN_SERVICE_CURRENT_CASE_PROGRESS_NUM] -= 1
                            serviceList[serviceIndex] = tmpServiceIndex
                            break
                elif dataDict[Do.KEY_DO] == Do.TYPE_DEBUG_CASE:
                    if dataDict[Do.TYPE_PROTOCOL] == Protocol.HTTP_PROTOCOL:
                        httpTestCase = HttpTestcase()
                        httpTestCase.generateByCaseDebugIdAndCaseStepDebugIdList(dataDict[Do.KEY_CASE_DEBUG_ID],
                                                                                 dataDict[
                                                                                     Do.KEY_CASE_STEP_DEBUG_ID_LIST])
                        if httpTestCase.execStatus != 1:
                            logging.error("没有查到用例调试信息caseDebugId[%s]" % dataDict[Do.KEY_CASE_DEBUG_ID])
                            # conn.send(bytes("没有查到用例调试信息caseDebugId[%s]" % dataDict[Do.KEY_CASE_DEBUG_ID], 'utf8'))
                        elif len(httpTestCase.stepTestcaseList) == 0:
                            logging.error("用例步骤数量为0 caseDebugId[%s]" % dataDict[Do.KEY_CASE_DEBUG_ID])
                            # conn.send(bytes("用例步骤数量为0 caseDebugId[%s]" % dataDict[Do.KEY_CASE_DEBUG_ID], 'utf8'))
                        else:
                            dataDict[isCluster] = isClusterConf.notRun
                            debugQueueList.append(dataDict)
                    elif dataDict[Do.TYPE_PROTOCOL] == Protocol.DUBBO_PROTOCOL:
                        dubboTestCase = DubboTestcase()
                        dubboTestCase.generateByCaseDebugIdAndCaseStepDebugIdList(dataDict[Do.KEY_CASE_DEBUG_ID],
                                                                                  dataDict[
                                                                                      Do.KEY_CASE_STEP_DEBUG_ID_LIST])
                        if dubboTestCase.execStatus != 1:
                            logging.error("没有查到用例调试信息caseDebugId[%s]" % dataDict[Do.KEY_CASE_DEBUG_ID])
                            # conn.send(bytes("没有查到用例调试信息caseDebugId[%s]" % dataDict[Do.KEY_CASE_DEBUG_ID], 'utf8'))
                        elif len(dubboTestCase.stepTestcaseList) == 0:
                            logging.error("用例步骤数量为0 caseDebugId[%s]" % dataDict[Do.KEY_CASE_DEBUG_ID])
                            # conn.send(bytes("用例步骤数量为0 caseDebugId[%s]" % dataDict[Do.KEY_CASE_DEBUG_ID], 'utf8'))
                        else:
                            dataDict[isCluster] = isClusterConf.notRun
                            debugQueueList.append(dataDict)
                elif dataDict[Do.KEY_DO] == Do.TYPE_DEBUG_CASE_DONE:
                    for debugIndex in range(0, len(debugQueueList)):
                        tmpDebugIndex = debugQueueList[debugIndex]
                        if Do.KEY_CASE_DEBUG_ID in tmpDebugIndex.keys() and tmpDebugIndex[Do.KEY_CASE_DEBUG_ID] == \
                                dataDict[
                                    Do.KEY_CASE_DEBUG_ID] and tmpDebugIndex[Do.TYPE_PROTOCOL] == dataDict[
                            Do.TYPE_PROTOCOL]:
                            tmpDebugIndex[isCluster] = isClusterConf.runDebugDone
                            debugQueueList[debugIndex] = tmpDebugIndex
                            break

                    for serviceIndex in range(0, len(serviceList)):
                        tmpServiceIndex = serviceList[serviceIndex]
                        if "%s_%s" % (dataDict[Do.TYPE_PROTOCOL], dataDict[Do.KEY_CASE_DEBUG_ID]) in tmpServiceIndex[
                            Do.KEY_RUN_SERVICE_CURRENT_CASE_LIST]:
                            tmpServiceIndex[Do.KEY_RUN_SERVICE_CURRENT_CASE_LIST].remove(
                                "%s_%s" % (dataDict[Do.TYPE_PROTOCOL], dataDict[Do.KEY_CASE_DEBUG_ID]))
                            tmpServiceIndex[Do.KEY_RUN_SERVICE_CURRENT_CASE_PROGRESS_NUM] -= 1
                            serviceList[serviceIndex] = tmpServiceIndex
                            break
                debugStatusList.pop(debugStatusIndex)
            else:
                time.sleep(1)
        except:
            print(traceback.format_exc())

def serviceStatusProgress(serviceStatusList,taskQueueList,serviceList):
    while True:
        try:
            serviceStatusIndex = 0
            if len(serviceStatusList) > serviceStatusIndex:
                dataDict = serviceStatusList[serviceStatusIndex]

                #服务重启
                if dataDict[Do.KEY_DO] == Do.TYPE_RUN_SERVICE_RESTART:
                    serviceFlag = False
                    for serviceIndex in range(0, len(serviceList)):
                        tmpServiceIndex = serviceList[serviceIndex]
                        if dataDict[Do.KEY_RUN_SERVICE_IP] == tmpServiceIndex[Do.KEY_RUN_SERVICE_IP] and dataDict[
                            Do.KEY_RUN_SERVICE_PORT] == tmpServiceIndex[Do.KEY_RUN_SERVICE_PORT]:
                            serviceFlag = True
                            logging.info("重启服务当前执行的任务为：%s " % tmpServiceIndex[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST])
                            taskQueueIndex = 0
                            while taskQueueIndex < len(taskQueueList):
                                # for taskQueueIndex in range(0,len(taskQueueList)):
                                #     try:
                                tmpTask = taskQueueList[taskQueueIndex]
                                # except Exception:
                                #     break
                                # tmpTask = taskQueueList[taskQueueIndex]
                                if "%s_%s" % (tmpTask[Do.TYPE_PROTOCOL], tmpTask["TaskExecuteId"]) in tmpServiceIndex[
                                    Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST]:
                                    tmpTask[isCluster] = isClusterConf.notRun
                                    taskQueueList[taskQueueIndex] = tmpTask
                                    break
                                taskQueueIndex += 1
                            tmpServiceIndex[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST] = []
                            tmpServiceIndex[Do.KEY_RUN_SERVICE_CURRENT_TASK_PROGRESS_NUM] = 0
                            tmpServiceIndex[Do.KEY_RUN_SERVICE_CURRENT_CASE_LIST] = []
                            tmpServiceIndex[Do.KEY_RUN_SERVICE_CURRENT_CASE_PROGRESS_NUM] = 0
                            tmpServiceIndex[Do.KEY_RUN_SERVICE_LAST_UPDATE_TIME] = datetime.datetime.now()
                            serviceList[serviceIndex] = tmpServiceIndex
                            break

                    if not serviceFlag:
                        tcpStr = '{"do":%s}' % Do.TYPE_MASTER_GET_SERVICE_DATA
                        if sendTcp(dataDict[Do.KEY_RUN_SERVICE_IP], dataDict[Do.KEY_RUN_SERVICE_PORT], tcpStr):
                            print("服务端未发现此service 要求数据上报 请求发送成功")
                        else:
                            logging.error("服务端未发现此service 要求数据上报 请求发送失败")

                #服务数据上报
                elif dataDict[Do.KEY_DO] == Do.TYPE_RUN_SERVICE_DATA_REPORT:
                    serviceFlag = False
                    for serviceIndex in range(0, len(serviceList)):
                        tmpServiceIndex = serviceList[serviceIndex]
                        if dataDict[Do.KEY_RUN_SERVICE_IP] == tmpServiceIndex[Do.KEY_RUN_SERVICE_IP] and dataDict[
                            Do.KEY_RUN_SERVICE_PORT] == tmpServiceIndex[Do.KEY_RUN_SERVICE_PORT]:
                            serviceFlag = True
                            if dataDict[Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM] != tmpServiceIndex[
                                Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM] or dataDict[
                                Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM] != \
                                    tmpServiceIndex[Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM]:
                                # 执行机上的最大进程数与master不符，更新执行机数量
                                tcpStr = '{"do":%s,"%s":%s,"%s":%s}' % (
                                    Do.TYPE_MASTER_SET_SERVICE_DATA, Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM,
                                    tmpServiceIndex[Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM],
                                    Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM,
                                    tmpServiceIndex[Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM])
                                if sendTcp(dataDict[Do.KEY_RUN_SERVICE_IP], dataDict[Do.KEY_RUN_SERVICE_PORT], tcpStr):
                                    logging.info("执行机上的任务最大进程数与master不符，更新执行机数量成功")
                                else:
                                    logging.error("执行机上的任务最大进程数与master不符，更新执行机数量失败")
                                if dataDict[Do.KEY_RUN_SERVICE_PROTOCOL] != tmpServiceIndex[
                                    Do.KEY_RUN_SERVICE_PROTOCOL]:
                                    tmpServiceIndex[Do.KEY_RUN_SERVICE_PROTOCOL] = dataDict[Do.KEY_RUN_SERVICE_PROTOCOL]
                                    serviceList[serviceIndex] = tmpServiceIndex

                    db = DBTool()
                    db.initGlobalDBConf()

                    # servicelist中没有这个服务器,判断表中是否有，如果表中没有，加入到servicelist表中记录

                    sqlRes = db.execute_sql(
                        "select * from tb_run_server_conf where serviceIp = '%s' and servicePort = %s" % (
                            dataDict[Do.KEY_RUN_SERVICE_IP], dataDict[Do.KEY_RUN_SERVICE_PORT]))

                    if len(sqlRes) > 0:
                        if not serviceFlag:
                            tcpStr = '{"do":%s,"%s":%s,"%s":%s}' % (
                                Do.TYPE_MASTER_SET_SERVICE_DATA,
                                Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM,
                                sqlRes[0]["maxTaskProgressNum"],
                                Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM,
                                sqlRes[0]["maxCaseProgressNum"])
                            if sendTcp(dataDict[Do.KEY_RUN_SERVICE_IP], dataDict[Do.KEY_RUN_SERVICE_PORT],
                                       tcpStr):
                                logging.info("执行机上的任务最大进程数与master不符，更新执行机数量成功")
                            else:
                                logging.error("执行机上的任务最大进程数与master不符，更新执行机数量失败")
                            serviceData = {}
                            serviceData[Do.KEY_RUN_SERVICE_IP] = sqlRes[0]["serviceIp"]
                            serviceData[Do.KEY_RUN_SERVICE_PORT] = sqlRes[0]["servicePort"]
                            serviceData[Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM] = sqlRes[0]["maxTaskProgressNum"]
                            serviceData[Do.KEY_RUN_SERVICE_CURRENT_TASK_PROGRESS_NUM] = dataDict[
                                Do.KEY_RUN_SERVICE_CURRENT_TASK_PROGRESS_NUM]
                            serviceData[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST] = dataDict[
                                Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST]
                            serviceData[Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM] = sqlRes[0]["maxCaseProgressNum"]
                            serviceData[Do.KEY_RUN_SERVICE_CURRENT_CASE_PROGRESS_NUM] = dataDict[
                                Do.KEY_RUN_SERVICE_CURRENT_CASE_PROGRESS_NUM]
                            serviceData[Do.KEY_RUN_SERVICE_CURRENT_CASE_LIST] = dataDict[
                                Do.KEY_RUN_SERVICE_CURRENT_CASE_LIST]
                            serviceData[Do.KEY_RUN_SERVICE_PROTOCOL] = dataDict[Do.KEY_RUN_SERVICE_PROTOCOL]

                            serviceData[Do.KEY_RUN_SERVICE_LAST_UPDATE_TIME] = datetime.datetime.now()
                            serviceList.append(serviceData)
                        res = db.execute_sql(
                            "UPDATE tb_run_server_conf SET STATUS = 1 WHERE serviceIp = '%s' AND servicePort = %s" % (
                                dataDict[Do.KEY_RUN_SERVICE_IP], dataDict[Do.KEY_RUN_SERVICE_PORT]))

                        if res == False:
                            logging.error(
                                "%s:%s 状态设为在线失败! %s" % (
                                dataDict[Do.KEY_RUN_SERVICE_IP], dataDict[Do.KEY_RUN_SERVICE_PORT], res))

                        else:
                            logging.info(
                                "%s:%s 状态设为在线! %s" % (
                                dataDict[Do.KEY_RUN_SERVICE_IP], dataDict[Do.KEY_RUN_SERVICE_PORT], dataDict))
                        db.release()
                    else:
                        currentTime = get_current_time()
                        res = db.execute_sql(
                            "insert into tb_run_server_conf (serviceName,serviceIp,servicePort,maxTaskProgressNum,maxCaseProgressNum,status,state,addBy,addTime,modTime) VALUES ('%s','%s',%s,%s,%s,1,1,'master','%s','%s');"
                            % (dataDict[Do.KEY_RUN_SERVICE_IP], dataDict[Do.KEY_RUN_SERVICE_IP],
                               dataDict[Do.KEY_RUN_SERVICE_PORT],
                               dataDict[Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM],
                               dataDict[Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM],
                               currentTime, currentTime))
                        db.release()
                        if res == False:
                            logging.error("数据插入失败！")
                        else:
                            logging.info("数据插入成功")
                            service = {}
                            service[Do.KEY_RUN_SERVICE_IP] = dataDict[Do.KEY_RUN_SERVICE_IP]
                            service[Do.KEY_RUN_SERVICE_PORT] = dataDict[Do.KEY_RUN_SERVICE_PORT]
                            service[Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM] = dataDict[
                                Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM]
                            service[Do.KEY_RUN_SERVICE_CURRENT_TASK_PROGRESS_NUM] = dataDict[
                                Do.KEY_RUN_SERVICE_CURRENT_TASK_PROGRESS_NUM]
                            service[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST] = dataDict[
                                Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST]
                            service[Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM] = dataDict[
                                Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM]
                            service[Do.KEY_RUN_SERVICE_CURRENT_CASE_PROGRESS_NUM] = dataDict[
                                Do.KEY_RUN_SERVICE_CURRENT_CASE_PROGRESS_NUM]
                            service[Do.KEY_RUN_SERVICE_CURRENT_CASE_LIST] = dataDict[
                                Do.KEY_RUN_SERVICE_CURRENT_CASE_LIST]
                            service[Do.KEY_RUN_SERVICE_PROTOCOL] = dataDict[Do.KEY_RUN_SERVICE_PROTOCOL]
                            service[Do.KEY_RUN_SERVICE_LAST_UPDATE_TIME] = datetime.datetime.now()
                            serviceList.append(service)
                    taskQueueIndex = 0
                    while taskQueueIndex < len(taskQueueList):
                        # for taskQueueIndex in range(0,len(taskQueueList)):
                        #     try:
                        tmpTaskQueue = taskQueueList[taskQueueIndex]
                        # except Exception:
                        #     break
                        if "%s_%s" % (
                        tmpTaskQueue[Do.TYPE_PROTOCOL], tmpTaskQueue[Do.KEY_TASK_EXECUTE_ID]) in dataDict.keys():
                            tmpTaskQueue[isCluster] = int(
                                dataDict[
                                    "%s_%s" % (tmpTaskQueue[Do.TYPE_PROTOCOL], tmpTaskQueue[Do.KEY_TASK_EXECUTE_ID])])
                            taskQueueList[taskQueueIndex] = tmpTaskQueue
                            break
                        taskQueueIndex += 1

                #更新服务信息
                elif dataDict[Do.KEY_DO] == Do.TYPE_MASTER_UPDATE_MESSAGE:
                    slaveIsOnline = False
                    for serviceIndex in range(0, len(serviceList)):
                        tmpService = serviceList[serviceIndex]
                        if dataDict[Do.KEY_RUN_SERVICE_IP] == tmpService[Do.KEY_RUN_SERVICE_IP] and dataDict[
                            Do.KEY_RUN_SERVICE_PORT] == tmpService[Do.KEY_RUN_SERVICE_PORT]:
                            tmpService[Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM] = dataDict[
                                Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM]
                            tmpService[Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM] = dataDict[
                                Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM]
                            serviceList[serviceIndex] = tmpService
                            slaveIsOnline = True
                            break

                    if slaveIsOnline:
                        # 向服务端告知MAX更新
                        tcpStr = '{"do":%s,"%s":%s,"%s":%s}' % (
                        Do.TYPE_MASTER_SET_SERVICE_DATA, Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM,
                        dataDict[Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM],
                        Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM, dataDict[Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM])
                        if sendTcp(dataDict[Do.KEY_RUN_SERVICE_IP], dataDict[Do.KEY_RUN_SERVICE_PORT], tcpStr):
                            print("向服务端告知MAX更新成功")
                            # logging.info("向服务端告知MAX更新成功")
                        else:
                            logging.error("向服务端告知MAX更新失败")

                serviceStatusList.pop(serviceStatusIndex)

            else:
                time.sleep(1)
        except:
            print(traceback.format_exc())

def serviceHeartBeat(heartBeatList,serviceList):
    while True:
        try:
            heartBeatIndex = 0
            if len(heartBeatList) > heartBeatIndex:
                dataDict = heartBeatList[heartBeatIndex]
                # 服务心跳
                inServiceList = False
                for serviceIndex in range(0, len(serviceList)):
                    if dataDict[Do.KEY_RUN_SERVICE_IP] == serviceList[serviceIndex][Do.KEY_RUN_SERVICE_IP] and dataDict[Do.KEY_RUN_SERVICE_PORT] == serviceList[serviceIndex][Do.KEY_RUN_SERVICE_PORT]:
                        inServiceList = True
                        tmpServiceIndex = serviceList[serviceIndex]
                        tmpServiceIndex[Do.KEY_RUN_SERVICE_LAST_UPDATE_TIME] = datetime.datetime.now()
                        tmpServiceIndex[Do.KEY_RUN_SERVICE_PROTOCOL] = dataDict[Do.KEY_RUN_SERVICE_PROTOCOL]
                        serviceList[serviceIndex] = tmpServiceIndex
                        break
                if not inServiceList:
                    # 服务端未发现此service 要求数据上报
                    tcpStr = '{"do":%s}' % Do.TYPE_MASTER_GET_SERVICE_DATA
                    if sendTcp(dataDict[Do.KEY_RUN_SERVICE_IP], dataDict[Do.KEY_RUN_SERVICE_PORT], tcpStr):
                        print("服务端未发现此service 要求数据上报 请求发送成功")
                        # logging.info("服务端未发现此service 要求数据上报 请求发送成功2222222")
                    else:
                        logging.error("服务端未发现此service 要求数据上报 请求发送失败")

                heartBeatList.pop(heartBeatIndex)
            else:
                time.sleep(1)

        except:
            print(traceback.format_exc())