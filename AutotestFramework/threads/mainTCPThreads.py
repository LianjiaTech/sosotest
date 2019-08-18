# import threading
# from core.tools.DBTool import *
# from core.tools.RedisTool import *
# from core.const.Do import *
# from core.const.Protocol import *
# from runfunc.runGlobalVars import isCluster
# from runfunc.initial import *
# from allmodels.DubboInterface import DubboInterface
# from allmodels.DubboTestcase import DubboTestcase
#
#
#
# def typeRunServiceDataReport(dataDict,serviceList,taskQueueList):
#     serviceFlag = False
#     for serviceIndex in range(0, len(serviceList)):
#         tmpServiceIndex = serviceList[serviceIndex]
#         if dataDict[Do.KEY_RUN_SERVICE_IP] == tmpServiceIndex[Do.KEY_RUN_SERVICE_IP] and dataDict[
#             Do.KEY_RUN_SERVICE_PORT] == tmpServiceIndex[Do.KEY_RUN_SERVICE_PORT]:
#             serviceFlag = True
#             if dataDict[Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM] != tmpServiceIndex[
#                 Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM] or dataDict[Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM] != \
#                     tmpServiceIndex[Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM]:
#                 # 执行机上的最大进程数与master不符，更新执行机数量
#                 tcpStr = '{"do":%s,"%s":%s,"%s":%s}' % (
#                 Do.TYPE_MASTER_SET_SERVICE_DATA, Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM,
#                 tmpServiceIndex[Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM], Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM,
#                 tmpServiceIndex[Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM])
#                 if sendTcp(dataDict[Do.KEY_RUN_SERVICE_IP], dataDict[Do.KEY_RUN_SERVICE_PORT], tcpStr):
#                     logging.info("执行机上的任务最大进程数与master不符，更新执行机数量成功")
#                 else:
#                     logging.error("执行机上的任务最大进程数与master不符，更新执行机数量失败")
#                 if dataDict[Do.KEY_RUN_SERVICE_PROTOCOL] != tmpServiceIndex[Do.KEY_RUN_SERVICE_PROTOCOL]:
#                     tmpServiceIndex[Do.KEY_RUN_SERVICE_PROTOCOL] = dataDict[Do.KEY_RUN_SERVICE_PROTOCOL]
#                     serviceList[serviceIndex] = tmpServiceIndex
#
#     db = DBTool()
#     db.initGlobalDBConf()
#
#     # servicelist中没有这个服务器,判断表中是否有，如果表中没有，加入到servicelist表中记录
#
#     sqlRes = db.execute_sql("select * from tb_run_server_conf where serviceIp = '%s' and servicePort = %s" % (
#     dataDict[Do.KEY_RUN_SERVICE_IP], dataDict[Do.KEY_RUN_SERVICE_PORT]))
#
#     if len(sqlRes) > 0:
#         if not serviceFlag:
#             tcpStr = '{"do":%s,"%s":%s,"%s":%s}' % (
#                 Do.TYPE_MASTER_SET_SERVICE_DATA,
#                 Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM,
#                 sqlRes[0]["maxTaskProgressNum"],
#                 Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM,
#                 sqlRes[0]["maxCaseProgressNum"])
#             if sendTcp(dataDict[Do.KEY_RUN_SERVICE_IP], dataDict[Do.KEY_RUN_SERVICE_PORT],
#                        tcpStr):
#                 logging.info("执行机上的任务最大进程数与master不符，更新执行机数量成功")
#             else:
#                 logging.error("执行机上的任务最大进程数与master不符，更新执行机数量失败")
#             serviceData = {}
#             serviceData[Do.KEY_RUN_SERVICE_IP] = sqlRes[0]["serviceIp"]
#             serviceData[Do.KEY_RUN_SERVICE_PORT] = sqlRes[0]["servicePort"]
#             serviceData[Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM] = sqlRes[0]["maxTaskProgressNum"]
#             serviceData[Do.KEY_RUN_SERVICE_CURRENT_TASK_PROGRESS_NUM] = dataDict[
#                 Do.KEY_RUN_SERVICE_CURRENT_TASK_PROGRESS_NUM]
#             serviceData[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST] = dataDict[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST]
#             serviceData[Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM] = sqlRes[0]["maxCaseProgressNum"]
#             serviceData[Do.KEY_RUN_SERVICE_CURRENT_CASE_PROGRESS_NUM] = dataDict[
#                 Do.KEY_RUN_SERVICE_CURRENT_CASE_PROGRESS_NUM]
#             serviceData[Do.KEY_RUN_SERVICE_CURRENT_CASE_LIST] = dataDict[Do.KEY_RUN_SERVICE_CURRENT_CASE_LIST]
#             serviceData[Do.KEY_RUN_SERVICE_PROTOCOL] = dataDict[Do.KEY_RUN_SERVICE_PROTOCOL]
#
#             serviceData[Do.KEY_RUN_SERVICE_LAST_UPDATE_TIME] = datetime.datetime.now()
#             serviceList.append(serviceData)
#         res = db.execute_sql("UPDATE tb_run_server_conf SET STATUS = 1 WHERE serviceIp = '%s' AND servicePort = %s" % (
#         dataDict[Do.KEY_RUN_SERVICE_IP], dataDict[Do.KEY_RUN_SERVICE_PORT]))
#
#         if res == False:
#             logging.error(
#                 "%s:%s 状态设为在线失败! %s" % (dataDict[Do.KEY_RUN_SERVICE_IP], dataDict[Do.KEY_RUN_SERVICE_PORT], res))
#
#         else:
#             logging.info(
#                 "%s:%s 状态设为在线! %s" % (dataDict[Do.KEY_RUN_SERVICE_IP], dataDict[Do.KEY_RUN_SERVICE_PORT], dataDict))
#         db.release()
#     else:
#         currentTime = get_current_time()
#         res = db.execute_sql(
#             "insert into tb_run_server_conf (serviceName,serviceIp,servicePort,maxTaskProgressNum,maxCaseProgressNum,status,state,addBy,addTime,modTime) VALUES ('%s','%s',%s,%s,%s,1,1,'master','%s','%s');"
#             % (dataDict[Do.KEY_RUN_SERVICE_IP], dataDict[Do.KEY_RUN_SERVICE_IP], dataDict[Do.KEY_RUN_SERVICE_PORT],
#                dataDict[Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM], dataDict[Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM],
#                currentTime, currentTime))
#         db.release()
#         if res == False:
#             logging.error("数据插入失败！")
#         else:
#             logging.info("数据插入成功")
#             service = {}
#             service[Do.KEY_RUN_SERVICE_IP] = dataDict[Do.KEY_RUN_SERVICE_IP]
#             service[Do.KEY_RUN_SERVICE_PORT] = dataDict[Do.KEY_RUN_SERVICE_PORT]
#             service[Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM] = dataDict[Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM]
#             service[Do.KEY_RUN_SERVICE_CURRENT_TASK_PROGRESS_NUM] = dataDict[
#                 Do.KEY_RUN_SERVICE_CURRENT_TASK_PROGRESS_NUM]
#             service[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST] = dataDict[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST]
#             service[Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM] = dataDict[Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM]
#             service[Do.KEY_RUN_SERVICE_CURRENT_CASE_PROGRESS_NUM] = dataDict[
#                 Do.KEY_RUN_SERVICE_CURRENT_CASE_PROGRESS_NUM]
#             service[Do.KEY_RUN_SERVICE_CURRENT_CASE_LIST] = dataDict[Do.KEY_RUN_SERVICE_CURRENT_CASE_LIST]
#             service[Do.KEY_RUN_SERVICE_PROTOCOL] = dataDict[Do.KEY_RUN_SERVICE_PROTOCOL]
#             service[Do.KEY_RUN_SERVICE_LAST_UPDATE_TIME] = datetime.datetime.now()
#             serviceList.append(service)
#     taskQueueIndex = 0
#     while taskQueueIndex < len(taskQueueList):
#         # for taskQueueIndex in range(0,len(taskQueueList)):
#         #     try:
#         tmpTaskQueue = taskQueueList[taskQueueIndex]
#         # except Exception:
#         #     break
#         if "%s_%s" % (tmpTaskQueue[Do.TYPE_PROTOCOL], tmpTaskQueue[Do.KEY_TASK_EXECUTE_ID]) in dataDict.keys():
#             tmpTaskQueue[isCluster] = int(
#                 dataDict["%s_%s" % (tmpTaskQueue[Do.TYPE_PROTOCOL], tmpTaskQueue[Do.KEY_TASK_EXECUTE_ID])])
#             taskQueueList[taskQueueIndex] = tmpTaskQueue
#             break
#         taskQueueIndex += 1
#
# def typeTaskCancelDone(dataDict,serviceList,taskQueueList):
#     taskQueueIndex = 0
#     while taskQueueIndex < len(taskQueueList):
#         # for taskQueueIndex in range(0,len(taskQueueList)):
#         #     try:
#         taskQueueIndexDict = taskQueueList[taskQueueIndex]
#         # except Exception:
#         #     break
#         if taskQueueIndexDict[Do.KEY_TASK_EXECUTE_ID] == dataDict[Do.KEY_TASK_EXECUTE_ID]:
#             taskQueueIndexDict[isCluster] = isClusterConf.cancelTaskDone
#             taskQueueList[taskQueueIndex] = taskQueueIndexDict
#         taskQueueIndex += 1
#     for serviceIndex in range(0, len(serviceList)):
#         tmpServiceIndex = serviceList[serviceIndex]
#         if "%s_%s" % (dataDict[Do.TYPE_PROTOCOL], dataDict[Do.KEY_TASK_EXECUTE_ID]) in tmpServiceIndex[
#             Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST]:
#             tmpServiceIndex[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST].remove(
#                 "%s_%s" % (dataDict[Do.TYPE_PROTOCOL], dataDict[Do.KEY_TASK_EXECUTE_ID]))
#             tmpServiceIndex[Do.KEY_RUN_SERVICE_CURRENT_TASK_PROGRESS_NUM] -= 1
#             serviceList[serviceIndex] = tmpServiceIndex
#     if Do.KEY_TASK_SUITE_EXECUTE_ID in dataDict.keys() and int(dataDict[Do.KEY_TASK_SUITE_EXECUTE_ID]) != 0:
#         try:
#             redisCache = RedisTool()
#             redisCache.initRedisConf()
#             # taskSuiteExecuteData = json.loads(
#             #     redisCache.get_data("%s_taskSuiteExecuteId_%s" % (dataDict[Do.TYPE_PROTOCOL],dataDict[Do.KEY_TASK_SUITE_EXECUTE_ID])))
#             # taskSuiteExecuteData["execStatus"] = ExecStatus.CANCELED
#             # redisCache.set_data("%s_taskSuiteExecuteId_%s" % (dataDict[Do.TYPE_PROTOCOL],dataDict[Do.KEY_TASK_SUITE_EXECUTE_ID]),
#             #                     json.dumps(taskSuiteExecuteData))
#             redisCache.del_data("%s_taskSuiteExecuteId_%s" % (dataDict[Do.TYPE_PROTOCOL],dataDict[Do.KEY_TASK_SUITE_EXECUTE_ID]))
#             cancelTaskSuite(dataDict)
#
#         except Exception:
#             print(traceback.format_exc())
#             logging.error("任务取消时设置任务集状态失败")
#     logging.info("taskExecuteDone: 任务取消完毕 %s " % dataDict)
#
# def typeTaskExecuteDone(dataDict,serviceList,taskQueueList):
#     dataDict[isCluster] = isClusterConf.runTaskDone
#     # print(1111111111111111)
#     taskQueueIndex = 0
#     while taskQueueIndex < len(taskQueueList):
#         # for taskQueueIndex in range(0,len(taskQueueList)):
#         #     try:
#         taskQueueIndexDict = taskQueueList[taskQueueIndex]
#         # except Exception:
#         #     break
#         if dataDict[Do.KEY_TASK_EXECUTE_ID] == taskQueueIndexDict[Do.KEY_TASK_EXECUTE_ID]:
#             taskQueueIndexDict[isCluster] = isClusterConf.runTaskDone
#             taskQueueList[taskQueueIndex] = taskQueueIndexDict
#             break
#         taskQueueIndex += 1
#     # print(22222222222222)
#     for serviceIndex in range(0, len(serviceList)):
#         tmpServiceIndex = serviceList[serviceIndex]
#         if "%s_%s" % (dataDict[Do.TYPE_PROTOCOL], dataDict[Do.KEY_TASK_EXECUTE_ID]) in tmpServiceIndex[
#             Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST]:
#             tmpServiceIndex[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST].remove(
#                 "%s_%s" % (dataDict[Do.TYPE_PROTOCOL], dataDict[Do.KEY_TASK_EXECUTE_ID]))
#             tmpServiceIndex[Do.KEY_RUN_SERVICE_CURRENT_TASK_PROGRESS_NUM] -= 1
#             serviceList[serviceIndex] = tmpServiceIndex
#             break
#     # print(333333333333)
#     if Do.KEY_TASK_SUITE_EXECUTE_ID in dataDict.keys() and int(dataDict[Do.KEY_TASK_SUITE_EXECUTE_ID]) != 0:
#         taskSuiteExecuteId = dataDict[Do.KEY_TASK_SUITE_EXECUTE_ID]
#         lastTaskExecuteId = dataDict[Do.KEY_TASK_EXECUTE_ID]
#         redisCache = RedisTool()
#         redisCache.initRedisConf()
#         if dataDict[Do.TYPE_PROTOCOL] == Protocol.HTTP_PROTOCOL:
#             # print(777777777777777)
#             taskExecuteTableName = "tb_task_execute"
#             taskSuiteExecuteTableName = "tb_task_suite_execute"
#         elif dataDict[Do.TYPE_PROTOCOL] == Protocol.DUBBO_PROTOCOL:
#             taskExecuteTableName = "tb2_dubbo_task_execute"
#             taskSuiteExecuteTableName = "tb2_dubbo_task_suite_execute"
#         else:
#             return
#         try:
#             taskSuiteExecuteData = json.loads(redisCache.get_data("%s_taskSuiteExecuteId_%s" % (dataDict[Do.TYPE_PROTOCOL],taskSuiteExecuteId)))
#         except:
#             db = DBTool()
#             db.initGlobalDBConf()
#             try:
#                 taskSuiteExecuteData = {"taskExecuteIdList":db.execute_sql("select taskExecuteIdList from %s where id = %s" % (taskSuiteExecuteTableName, taskSuiteExecuteId))[0]["taskExecuteIdList"].split(",")}
#             except:
#                 taskSuiteExecuteData = {"taskExecuteIdList":[]}
#             finally:
#                 db.release()
#         lastTask = True
#         progressList = []
#         testResultList = []
#         # print(4444444444444)
#         for taskIndex in taskSuiteExecuteData["taskExecuteIdList"]:
#             try:
#                 taskExecStatus = json.loads(
#                     redisCache.get_data("%s_taskSuite_%s_task_%s" % (dataDict[Do.TYPE_PROTOCOL],taskSuiteExecuteId, taskIndex)))
#                 testResultList.append(taskExecStatus["testResult"])
#             except:
#                 testResultList.append(db.execute_sql("select execStatus from %s where id=%s" % (taskExecuteTableName, taskIndex))[0]["execStatus"])
#
#             if taskExecStatus["execStatus"] != ExecStatus.DONE and taskExecStatus[
#                 "execStatus"] != ExecStatus.EXCEPTION and \
#                             taskExecStatus["execStatus"] != ExecStatus.CANCELED:
#                 lastTask = False
#                 progressList.append(int(taskExecStatus["progress"]))
#         # print(5555555555555555)
#         if lastTask:
#             # print(6666666666666666666666)
#             try:
#                 db = DBTool()
#                 db.initGlobalDBConf()
#
#                 taskListTestResult = {}
#                 taskListTestResult["testResult"] = ""
#                 taskListTestResult["task"] = {}
#                 taskListTestResult["task"]["total"] = 0
#                 taskListTestResult["task"][ResultConst.PASS] = 0
#                 taskListTestResult["task"][ResultConst.FAIL] = 0
#                 taskListTestResult["task"][ResultConst.ERROR] = 0
#                 taskListTestResult["task"][ResultConst.EXCEPTION] = 0
#                 taskListTestResult["task"][ResultConst.CANCELED] = 0
#                 taskListTestResult["caseTotal"] = 0
#                 taskListTestResult["casePass"] = 0
#                 taskListTestResult["caseFail"] = 0
#                 taskListTestResult["caseError"] = 0
#                 taskListTestResult["caseNnotrun"] = 0
#                 taskListTestResult["casePerformanceTotal"] = 0
#                 taskListTestResult["casePerformancePass"] = 0
#                 taskListTestResult["casePerformanceFail"] = 0
#                 taskListTestResult["taskList"] = []
#                 # print(taskSuiteExecuteData)
#
#                 for taskIndex in taskSuiteExecuteData["taskExecuteIdList"]:
#                     redisCache.del_data("%s_taskSuite_%s_task_%s" % (dataDict[Do.TYPE_PROTOCOL],taskSuiteExecuteId, taskIndex))
#
#                     thisTask = db.execute_sql(
#                         "select id,title,taskId,testResult,testResultMsg,testReportUrl,httpConfKey from %s where id=%s" % (taskExecuteTableName,taskIndex))
#
#                     if thisTask[0]["testResult"] not in taskListTestResult["task"].keys():
#                         taskListTestResult["task"][thisTask[0]["testResult"]] = 0
#
#                     try:
#                         thisTaskResultMsg = json.loads(thisTask[0]["testResultMsg"])
#                         taskListTestResult["caseTotal"] += thisTaskResultMsg["totalExecuteSummary"]['total']
#                         taskListTestResult["casePass"] += thisTaskResultMsg["totalExecuteSummary"]['pass']
#                         taskListTestResult["caseFail"] += thisTaskResultMsg["totalExecuteSummary"]['fail']
#                         taskListTestResult["caseError"] += thisTaskResultMsg["totalExecuteSummary"]['error']
#                         taskListTestResult["caseNnotrun"] += thisTaskResultMsg["totalExecuteSummary"]['notrun']
#                         if dataDict[Do.TYPE_PROTOCOL] == Protocol.HTTP_PROTOCOL:
#                             taskListTestResult["casePerformanceTotal"] += thisTaskResultMsg["actualTotalPerformanceDict"][
#                                 'total']
#                             taskListTestResult["casePerformancePass"] += thisTaskResultMsg["actualTotalPerformanceDict"][
#                                 'pass']
#                             taskListTestResult["casePerformanceFail"] += thisTaskResultMsg["actualTotalPerformanceDict"][
#                                 'fail']
#                             actualTotalPerformanceDict = thisTaskResultMsg["actualTotalPerformanceDict"]
#                         else:
#                             actualTotalPerformanceDict = {}
#
#                         taskListTestResult["taskList"].append({"id": thisTask[0]["id"], "taskId": thisTask[0]["taskId"],
#                                                                "testResult": thisTask[0]["testResult"],
#                                                                "executeSummary": thisTaskResultMsg[
#                                                                    "totalExecuteSummary"],
#                                                                "testReportUrl": thisTask[0]["testReportUrl"],
#                                                                "taskName": thisTask[0]["title"],
#                                                                "httpConfKey": thisTask[0]["httpConfKey"],
#                                                                "actualTotalPerformanceDict": actualTotalPerformanceDict})
#                     except Exception:
#                         print(traceback.format_exc())
#                         taskListTestResult["taskList"].append({"taskId": thisTask[0]["taskId"], "testResult": "CANCEL"})
#                     taskListTestResult["task"][thisTask[0]["testResult"]] += 1
#                     taskListTestResult["task"]["total"] += 1
#                 redisCache.del_data("%s_taskSuiteExecuteId_%s" % (dataDict[Do.TYPE_PROTOCOL],taskSuiteExecuteId))
#                 # print(testResultList)
#                 # print(taskSuiteExecuteTableName)
#                 # print(taskExecuteTableName)
#                 # taskSuiteResult = db.execute_sql(
#                 # "select * from tb_task_suite_execute where id = %s" % taskSuiteExecuteId)
#                 #
#                 # if taskSuiteResult:
#                 if ResultConst.CANCELED in testResultList:
#                     testResult = ResultConst.CANCELED
#                 elif ResultConst.ERROR in testResultList:
#                     testResult = ResultConst.ERROR
#                 elif ResultConst.EXCEPTION in testResultList:
#                     testResult = ResultConst.EXCEPTION
#                 elif ResultConst.FAIL in testResultList:
#                     testResult = ResultConst.FAIL
#                 elif ResultConst.WARNING in testResultList:
#                     testResult = ResultConst.WARNING
#                 else:
#                     testResult = ResultConst.PASS
#                 taskListTestResult["testResult"] = testResult
#                 taskSuiteResult = \
#                 db.execute_sql("select execTime from %s where id = %s" % (taskSuiteExecuteTableName,taskSuiteExecuteId))[0]
#                 # print(11111111111111111111111111111)
#                 lastTaskData = \
#                 db.execute_sql("select execFinishTime from %s where id=%s" % (taskExecuteTableName,lastTaskExecuteId))[0]
#                 execTakeTime = (lastTaskData["execFinishTime"] - taskSuiteResult["execTime"]).seconds
#                 # print(2222222222222222222222222222)
#                 db.execute_sql(
#                     "update %s set testResult = '%s',testResultMsg = '%s',execTakeTime = '%s',execFinishTime = '%s' where id = %s" % (
#                         taskSuiteExecuteTableName,testResult, json.dumps(taskListTestResult, ensure_ascii=False), execTakeTime,
#                         lastTaskData["execFinishTime"], taskSuiteExecuteId))
#                 # print(3333333333333333333333333333333)
#                 taskSuiteResult = \
#                 db.execute_sql("select * from %s where id = %s" % (taskSuiteExecuteTableName,taskSuiteExecuteId))[0]
#                 taskSuiteResult['testResultMsg'] = json.dumps(taskListTestResult, ensure_ascii=False)
#                 # 生成报告
#                 result, url = generateHttpReport(taskSuiteResult)
#                 # print(result)
#                 # print(url)
#                 # print(44444444444444444444)
#                 # print(url)
#                 if result:
#                     db.execute_sql(
#                         "update %s set execStatus = %s,testReportUrl = '%s' where id = %s" % (
#                             taskSuiteExecuteTableName,ExecStatus.DONE, url, taskSuiteExecuteId))
#                 else:
#                     db.execute_sql(
#                         "update %s set execStatus = %s,testReportUrl = '%s' where id = %s" % (
#                             taskSuiteExecuteTableName,url, ExecStatus.EXCEPTION, ""))
#                 # print(5555555555555555555555555555555)
#                 # 发送邮件
#                 if int(taskSuiteResult["isSendEmail"]) > 0 and taskSuiteResult["emailList"] != "" and len(taskListTestResult["taskList"]) > 0 :
#                     sendEmailToExecutor(taskSuiteResult)
#
#             except Exception:
#                 print("任务集报告生成失败%s" % traceback.format_exc())
#                 db.execute_sql(
#                     "update %s set testResult = '%s',execStatus = %s where id = %s" % (
#                         taskSuiteExecuteTableName,ResultConst.ERROR, ExecStatus.EXCEPTION, taskSuiteExecuteId))
#             finally:
#                 db.release()
#
#         else:
#             progressList.sort(reverse=True)
#             taskSuiteExecuteData["progress"] = progressList[0]
#             redisCache.set_data("%s_taskSuiteExecuteId_%s" % (dataDict[Do.TYPE_PROTOCOL],taskSuiteExecuteId), json.dumps(taskSuiteExecuteData))
#
# def typeTaskCancel(dataDict,taskQueueList,taskCancelQueueList):
#     if dataDict not in taskCancelQueueList:
#         taskQueueIndex = 0
#         while taskQueueIndex < len(taskQueueList):
#             # for taskQueueIndex in range(0,len(taskQueueList)):
#             #     try:
#             taskQueueIndexDict = taskQueueList[taskQueueIndex]
#             # except Exception:
#             #     break
#             # taskQueueIndexDict = taskQueueList[taskQueueIndex]
#             if taskQueueIndexDict[Do.KEY_TASK_EXECUTE_ID] == dataDict[Do.KEY_TASK_EXECUTE_ID]:
#                 if taskQueueIndexDict[isCluster] == isClusterConf.notRun:
#                     taskQueueIndexDict[isCluster] = isClusterConf.toCancel
#                     taskQueueList[taskQueueIndex] = taskQueueIndexDict
#                 break
#             taskQueueIndex += 1
#         taskCancelQueueList.append(dataDict)
#     if Do.KEY_TASK_SUITE_EXECUTE_ID in dataDict.keys() and int(dataDict[Do.KEY_TASK_SUITE_EXECUTE_ID]) != 0:
#         redisCache = RedisTool()
#         redisCache.initRedisConf()
#         try:
#             taskSuiteExecuteData = json.loads(
#                 redisCache.get_data("%s_taskSuiteExecuteId_%s" % (dataDict[Do.TYPE_PROTOCOL],dataDict[Do.KEY_TASK_SUITE_EXECUTE_ID])))
#         except:
#             taskSuiteExecuteData = {"taskExecuteIdList": [], "execStatus": 1, "progress": 0}
#         taskSuiteExecuteData["execStatus"] = ExecStatus.CANCELED
#         redisCache.set_data("%s_taskSuiteExecuteId_%s" % (dataDict[Do.TYPE_PROTOCOL],dataDict[Do.KEY_TASK_SUITE_EXECUTE_ID]),
#                             json.dumps(taskSuiteExecuteData))
#         cancelTaskSuite(dataDict)
#     logging.debug("startServer: 任务取消加入taskCancelQueue！")
#
# def typeTaskInitDone(dataDict,taskQueueList):
#     dataDict[isCluster] = isClusterConf.runTaskInitDone
#     taskQueueIndex = 0
#     while taskQueueIndex < len(taskQueueList):
#         # for taskQueueIndex in range(0,len(taskQueueList)):
#         #     try:
#         taskQueueIndexDict = taskQueueList[taskQueueIndex]
#         # except Exception:
#         #     break
#         if taskQueueIndexDict[Do.KEY_TASK_EXECUTE_ID] == dataDict[Do.KEY_TASK_EXECUTE_ID] and taskQueueIndexDict[
#             Do.TYPE_PROTOCOL] == dataDict[Do.TYPE_PROTOCOL]:
#             if taskQueueIndexDict[isCluster] == isClusterConf.runTcpSend:
#                 taskQueueIndexDict[isCluster] = isClusterConf.runTaskInitDone
#                 taskQueueList[taskQueueIndex] = taskQueueIndexDict
#                 logging.info("任务%s 初始化完成" % dataDict[Do.KEY_TASK_EXECUTE_ID])
#             break
#         taskQueueIndex += 1
#
# def typeDebugInterface(dataDict,debugQueueList):
#     if dataDict[Do.TYPE_PROTOCOL] == Protocol.HTTP_PROTOCOL:
#         httpInterface = HttpInterface(interfaceDebugId=dataDict[Do.KEY_INTERFACE_DEBUG_ID])
#         httpInterface.generateByInterfaceDebugId()
#         if httpInterface.execStatus != 1:
#             logging.info("没有查到接口调试信息interfaceDebugId[%s]" % dataDict[Do.KEY_INTERFACE_DEBUG_ID])
#         else:
#             dataDict[isCluster] = isClusterConf.notRun
#             debugQueueList.append(dataDict)
#     elif dataDict[Do.TYPE_PROTOCOL] == Protocol.DUBBO_PROTOCOL:
#         dubboInterface = DubboInterface(interfaceDebugId=dataDict[Do.KEY_INTERFACE_DEBUG_ID])
#         dubboInterface.generateByInterfaceDebugId()
#         if dubboInterface.execStatus != 1:
#             logging.info("没有查到接口调试信息interfaceDebugId[%s]" % dataDict[Do.KEY_INTERFACE_DEBUG_ID])
#         else:
#             dataDict[isCluster] = isClusterConf.notRun
#             debugQueueList.append(dataDict)
#
# def typeDebugInterfaceDone(dataDict,serviceList,debugQueueList):
#     for debugIndex in range(0, len(debugQueueList)):
#         tmpDebugIndex = debugQueueList[debugIndex]
#         if Do.KEY_INTERFACE_DEBUG_ID in tmpDebugIndex.keys() and tmpDebugIndex[Do.KEY_INTERFACE_DEBUG_ID] == dataDict[
#             Do.KEY_INTERFACE_DEBUG_ID] and tmpDebugIndex[Do.TYPE_PROTOCOL] == dataDict[Do.TYPE_PROTOCOL]:
#             tmpDebugIndex[isCluster] = isClusterConf.runDebugDone
#             debugQueueList[debugIndex] = tmpDebugIndex
#             break
#
#     for serviceIndex in range(0, len(serviceList)):
#         tmpServiceIndex = serviceList[serviceIndex]
#         if "%s_%s" % (dataDict[Do.TYPE_PROTOCOL], dataDict[Do.KEY_INTERFACE_DEBUG_ID]) in tmpServiceIndex[
#             Do.KEY_RUN_SERVICE_CURRENT_CASE_LIST]:
#             tmpServiceIndex[Do.KEY_RUN_SERVICE_CURRENT_CASE_LIST].remove(
#                 "%s_%s" % (dataDict[Do.TYPE_PROTOCOL], dataDict[Do.KEY_INTERFACE_DEBUG_ID]))
#             tmpServiceIndex[Do.KEY_RUN_SERVICE_CURRENT_CASE_PROGRESS_NUM] -= 1
#             serviceList[serviceIndex] = tmpServiceIndex
#             break
#
# def typeDebugCase(dataDict,debugQueueList):
#     if dataDict[Do.TYPE_PROTOCOL] == Protocol.HTTP_PROTOCOL:
#         httpTestCase = HttpTestcase()
#         httpTestCase.generateByCaseDebugIdAndCaseStepDebugIdList(dataDict[Do.KEY_CASE_DEBUG_ID],
#                                                                  dataDict[Do.KEY_CASE_STEP_DEBUG_ID_LIST])
#         if httpTestCase.execStatus != 1:
#             logging.error("没有查到用例调试信息caseDebugId[%s]" % dataDict[Do.KEY_CASE_DEBUG_ID])
#             # conn.send(bytes("没有查到用例调试信息caseDebugId[%s]" % dataDict[Do.KEY_CASE_DEBUG_ID], 'utf8'))
#         elif len(httpTestCase.stepTestcaseList) == 0:
#             logging.error("用例步骤数量为0 caseDebugId[%s]" % dataDict[Do.KEY_CASE_DEBUG_ID])
#             # conn.send(bytes("用例步骤数量为0 caseDebugId[%s]" % dataDict[Do.KEY_CASE_DEBUG_ID], 'utf8'))
#         else:
#             dataDict[isCluster] = isClusterConf.notRun
#             debugQueueList.append(dataDict)
#     elif dataDict[Do.TYPE_PROTOCOL] == Protocol.DUBBO_PROTOCOL:
#         dubboTestCase = DubboTestcase()
#         dubboTestCase.generateByCaseDebugIdAndCaseStepDebugIdList(dataDict[Do.KEY_CASE_DEBUG_ID],
#                                                                   dataDict[Do.KEY_CASE_STEP_DEBUG_ID_LIST])
#         if dubboTestCase.execStatus != 1:
#             logging.error("没有查到用例调试信息caseDebugId[%s]" % dataDict[Do.KEY_CASE_DEBUG_ID])
#             # conn.send(bytes("没有查到用例调试信息caseDebugId[%s]" % dataDict[Do.KEY_CASE_DEBUG_ID], 'utf8'))
#         elif len(dubboTestCase.stepTestcaseList) == 0:
#             logging.error("用例步骤数量为0 caseDebugId[%s]" % dataDict[Do.KEY_CASE_DEBUG_ID])
#             # conn.send(bytes("用例步骤数量为0 caseDebugId[%s]" % dataDict[Do.KEY_CASE_DEBUG_ID], 'utf8'))
#         else:
#             dataDict[isCluster] = isClusterConf.notRun
#             debugQueueList.append(dataDict)
#
#
# def typeDebugCaseDone(dataDict,serviceList,debugQueueList):
#     for debugIndex in range(0, len(debugQueueList)):
#         tmpDebugIndex = debugQueueList[debugIndex]
#         if Do.KEY_CASE_DEBUG_ID in tmpDebugIndex.keys() and tmpDebugIndex[Do.KEY_CASE_DEBUG_ID] == dataDict[
#             Do.KEY_CASE_DEBUG_ID] and tmpDebugIndex[Do.TYPE_PROTOCOL] == dataDict[Do.TYPE_PROTOCOL]:
#             tmpDebugIndex[isCluster] = isClusterConf.runDebugDone
#             debugQueueList[debugIndex] = tmpDebugIndex
#             break
#
#     for serviceIndex in range(0, len(serviceList)):
#         tmpServiceIndex = serviceList[serviceIndex]
#         if "%s_%s" % (dataDict[Do.TYPE_PROTOCOL], dataDict[Do.KEY_CASE_DEBUG_ID]) in tmpServiceIndex[
#             Do.KEY_RUN_SERVICE_CURRENT_CASE_LIST]:
#             tmpServiceIndex[Do.KEY_RUN_SERVICE_CURRENT_CASE_LIST].remove(
#                 "%s_%s" % (dataDict[Do.TYPE_PROTOCOL], dataDict[Do.KEY_CASE_DEBUG_ID]))
#             tmpServiceIndex[Do.KEY_RUN_SERVICE_CURRENT_CASE_PROGRESS_NUM] -= 1
#             serviceList[serviceIndex] = tmpServiceIndex
#             break
