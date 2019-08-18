from runfunc.initial import *
from core.config.InitConfig import isClusterConf
from core.const.Protocol import *
from allmodels.DubboTask import *
from progress.globalValFunc import *
# lock = threading.RLock() #线程锁

@catch_exception
@take_time
# @set_logging
def process_allocating_task(taskQueueList,taskCancelQueueList,serviceList):
    while True:
        #判断taskQueue是否为空，否则把队列中的任务拿到本线程的数组里
        taskStartIndex = 0
        while len(taskQueueList) > taskStartIndex:
            # print("""taskQueueList["taskQueueList"]""",taskQueueList[taskStartIndex])
            try:
                # # 如果有任务已经执行完
                if taskQueueList[taskStartIndex][isCluster] == isClusterConf.runTaskDone:
                    logging.info("process_allocating_task  检测到任务执行完毕 %s" % taskQueueList[taskStartIndex])
                    for serviceIndex in serviceList:
                        if Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST not in serviceIndex.keys():
                            serviceIndex[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST] = []
                        if "%s_%s" % (taskQueueList[taskStartIndex][Do.TYPE_PROTOCOL],taskQueueList[taskStartIndex][Do.KEY_TASK_EXECUTE_ID]) in serviceIndex[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST]:
                            serviceIndex[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST].remove("%s_%s" % (taskQueueList[taskStartIndex][Do.TYPE_PROTOCOL],taskQueueList[taskStartIndex][Do.KEY_TASK_EXECUTE_ID]))
                            serviceIndex[Do.KEY_RUN_SERVICE_CURRENT_TASK_PROGRESS_NUM] -= 1

                    taskQueueList.remove(taskQueueList[taskStartIndex])
                    break

                #如果任务已取消
                if taskQueueList[taskStartIndex][isCluster] == isClusterConf.cancelTaskDone:
                    if len(taskCancelQueueList) == 0:
                        taskQueueList.remove(taskQueueList[taskStartIndex])
                    taskStartIndex += 1
                    continue

                #查出所有在执行中的任务和自己比较
                taskIndexIsStart = True
                for taskIndex in taskQueueList:
                    if taskIndex[isCluster] != isClusterConf.notRun:
                        if taskQueueList[taskStartIndex][Do.KEY_TASK_EXECUTE_ENV] == taskIndex[Do.KEY_TASK_EXECUTE_ENV]:
                            if taskQueueList[taskStartIndex][Do.KEY_TASK_ID] == taskIndex[Do.KEY_TASK_ID]:
                                taskIndexIsStart = False

                #没有同环境同任务执行，可以立即执行
                if taskIndexIsStart:
                    # print("""taskQueueList["taskQueueList"]""", taskQueueList[taskStartIndex])
                    # logging.info("thread_process_allocating_task: Processed_taskQueue : %s " % serviceList)
                    # logging.info("thread_process_allocating_task: 开始处理 : %s " % taskQueueList[taskStartIndex])
                    availableServiceCount = 0
                    tmpServiceList = []
                    for serviceIndex in range(0,len(serviceList)):
                        tmpService = serviceList[serviceIndex]
                        if taskQueueList[taskStartIndex][Do.TYPE_PROTOCOL] in tmpService[Do.KEY_RUN_SERVICE_PROTOCOL]:
                            if Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST not in tmpService.keys():
                                tmpService[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST] = []
                            if tmpService[Do.KEY_RUN_SERVICE_CURRENT_TASK_PROGRESS_NUM] < tmpService[Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM]:
                                tmpService[Do.KEY_RUN_SERVICE_AVAILABLE_TASK_PROGRESS_NUM] = tmpService[Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM] - tmpService[Do.KEY_RUN_SERVICE_CURRENT_TASK_PROGRESS_NUM]
                                availableServiceCount += 1
                            else:
                                tmpService[Do.KEY_RUN_SERVICE_AVAILABLE_TASK_PROGRESS_NUM] = 0
                            serviceList[serviceIndex] = tmpService
                            tmpServiceList.append(tmpService)

                    logging.debug("当前可用的servers数量 %s " % availableServiceCount)
                    logging.debug("当前所有的的server %s " % serviceList)
                    #现在没有可用的执行服务器
                    if availableServiceCount == 0:
                        break
                    else:
                        #通过可执行的线程数量获取出可执行线程数量最多的服务器
                        tmpServiceList.sort(key=lambda x:x[Do.KEY_RUN_SERVICE_AVAILABLE_TASK_PROGRESS_NUM],reverse=True)
                        # tcpStr = '{"do":3,"TaskExecuteId":%s,"TaskExecuteEnv":"%s","TaskId":"%s","%s":"%s"}'%(
                        #     taskQueueList[taskStartIndex][Do.KEY_TASK_EXECUTE_ID],taskQueueList[taskStartIndex][Do.KEY_TASK_EXECUTE_ENV]
                        #     ,taskQueueList[taskStartIndex][Do.KEY_TASK_ID],Do.TYPE_PROTOCOL,taskQueueList[taskStartIndex][Do.TYPE_PROTOCOL])
                        taskQueueList[taskStartIndex][Do.KEY_TASK_ID] = 3
                        tcpStr = json.dumps(taskQueueList[taskStartIndex])
                        #发送tcp请求
                        sendTcpService = tmpServiceList[0]
                        for tmpServiceListIndex in tmpServiceList:
                            tmpTaskQueueIndex = taskQueueList[taskStartIndex]
                            if tmpTaskQueueIndex[isCluster] == isClusterConf.notRun:
                                tmpTaskQueueIndex[isCluster] = isClusterConf.runTcpSend
                                if sendTcp(tmpServiceListIndex[Do.KEY_RUN_SERVICE_IP],tmpServiceListIndex[Do.KEY_RUN_SERVICE_PORT],tcpStr):
                                    tmpServiceListIndex[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST].append("%s_%s" % (tmpTaskQueueIndex[Do.TYPE_PROTOCOL],tmpTaskQueueIndex[Do.KEY_TASK_EXECUTE_ID]))
                                    tmpServiceListIndex[Do.KEY_RUN_SERVICE_CURRENT_TASK_PROGRESS_NUM] += 1
                                    #设置serviceListQueue
                                    tmpTaskQueueIndex[isCluster] = isClusterConf.runTcpSend
                                    sendTcpService = tmpServiceListIndex
                                    taskQueueList[taskStartIndex] = tmpTaskQueueIndex
                                    break
                                else:
                                    logging.error("任务执行的TCP发送失败！%s" % tcpStr)
                                    tmpTaskQueueIndex[isCluster] = isClusterConf.notRun
                                    taskQueueList[taskStartIndex] = tmpTaskQueueIndex
                                    continue

                        for serviceListIndex in range(0, len(serviceList)):
                            tmpServiceListData = serviceList[serviceListIndex]
                            if tmpServiceListData[Do.KEY_RUN_SERVICE_IP] == sendTcpService[Do.KEY_RUN_SERVICE_IP] and tmpServiceListData[Do.KEY_RUN_SERVICE_PORT] == sendTcpService[Do.KEY_RUN_SERVICE_PORT]:
                                serviceList[serviceListIndex] = sendTcpService
                taskStartIndex += 1
            except Exception:
                print(traceback.format_exc())
                break
            continue

        time.sleep(1)

@catch_exception
@take_time
def process_allocating_task_cancel(taskQueueList,taskCancelQueueList,serviceList):
    while True:
        if len(taskCancelQueueList) > 0 :
            try:
                isCancel = True
                for taskQueueCount in range(0,len(taskQueueList)):
                    logging.info("thread_process_allocating_task_cancel ： 开始处理取消任务：%s " % taskCancelQueueList[0])
                    taskQueueIndex = taskQueueList[taskQueueCount]
                    if int(taskCancelQueueList[0][Do.KEY_TASK_EXECUTE_ID]) != int(taskQueueIndex[Do.KEY_TASK_EXECUTE_ID]):
                        continue

                    if taskQueueIndex[isCluster] == isClusterConf.cancelTcpSend:
                        isCancel = False
                        break

                    if taskQueueIndex[isCluster] == isClusterConf.cancelTaskDone or taskQueueIndex[isCluster] == isClusterConf.notRun:
                        taskCancelQueueList.remove(taskCancelQueueList[0])
                        taskQueueList.remove(taskQueueList[taskQueueCount])
                        isCancel = False
                        break
                    tcpIp = ""
                    tcpPort = 0
                    for serviceConfIndex in serviceList:
                        if "%s_%s" % (taskCancelQueueList[0][Do.TYPE_PROTOCOL],taskCancelQueueList[0][Do.KEY_TASK_EXECUTE_ID]) in serviceConfIndex[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST]:
                            tcpIp = serviceConfIndex[Do.KEY_RUN_SERVICE_IP]
                            tcpPort = serviceConfIndex[Do.KEY_RUN_SERVICE_PORT]
                            break
                    if tcpIp != "":
                        tcpStr = '{"do":%s,"TaskExecuteId":%s,"%s":"%s"}' % (Do.TYPE_TASK_CANCEL, taskCancelQueueList[0][Do.KEY_TASK_EXECUTE_ID],Do.TYPE_PROTOCOL,taskCancelQueueList[0][Do.TYPE_PROTOCOL])

                        if taskQueueIndex[isCluster] == isClusterConf.toCancel or taskQueueIndex[isCluster] == isClusterConf.runTaskInitDone:
                            logging.debug("%s 的状态为 %s" % (taskCancelQueueList[0][Do.KEY_TASK_EXECUTE_ID],taskQueueIndex[isCluster]))
                            taskQueueIndex[isCluster] = isClusterConf.cancelTcpSend
                            taskQueueList[taskQueueCount] = taskQueueIndex
                            if sendTcp(tcpIp, tcpPort, tcpStr):
                                logging.info("取消TCP发送泡%s成功" % taskCancelQueueList[0])

                                isCancel = False
                                break
                            else:
                                isCancel = True
                                logging.error("任务取消 TCP 发送失败")
                        else:
                            isCancel = False
                            logging.info("任务状态为%s,暂时不可取消，等待下次" % taskQueueIndex[isCluster])
                    else:
                        isCancel = True
                        logging.info("未获取到TCP信息，主服务执行取消")

                if isCancel:
                    for taskQueueIndex in range (0,len(taskQueueList)):
                        # cancelTaskSuite(taskQueueList[taskQueueIndex][Do.KEY_TASK_SUITE_EXECUTE_ID], taskQueueList[taskQueueIndex][Do.KEY_TASK_EXECUTE_ID])
                        taskQueueIndexDict = taskQueueList[taskQueueIndex]
                        if int(taskCancelQueueList[0][Do.KEY_TASK_EXECUTE_ID]) == int(taskQueueIndexDict[Do.KEY_TASK_EXECUTE_ID]):
                            taskQueueIndexDict[isCluster] = isClusterConf.cancelTaskDone
                            taskQueueList[taskQueueIndex] = taskQueueIndexDict
                    if taskCancelQueueList[0][Do.TYPE_PROTOCOL] == Protocol.HTTP_PROTOCOL:
                        tmpTask = Task()
                        tmpTask.taskExecuteId = taskCancelQueueList[0][Do.KEY_TASK_EXECUTE_ID]
                        tmpTask.generateByTaskExecuteId()
                        res = tmpTask.cancelTask()
                    elif taskCancelQueueList[0][Do.TYPE_PROTOCOL] == Protocol.DUBBO_PROTOCOL:
                        tmpTask = DubboTask()
                        tmpTask.taskExecuteId = taskCancelQueueList[0][Do.KEY_TASK_EXECUTE_ID]
                        tmpTask.generateByTaskExecuteId()
                        res = tmpTask.cancelTask()
                    if res:
                        logging.info("%s 任务取消成功" % taskCancelQueueList[0][Do.KEY_TASK_EXECUTE_ID])
                    else:
                        logging.error("%s 任务取消失败 " % taskCancelQueueList[0][Do.KEY_TASK_EXECUTE_ID])
                        logging.error("%s 任务取消失败 " % res)
                    taskCancelQueueList.remove(taskCancelQueueList[0])
            except Exception:
                logging.error(traceback.format_exc())
                taskCancelQueueList.remove(taskCancelQueueList[0])
                continue
        time.sleep(1)

@catch_exception
@take_time
def progress_allocating_debug(debugQueueList,serviceList):
    while True:
        startDebugIndex = 0
        while len(debugQueueList) > startDebugIndex:
            try:
                thisDebugData = debugQueueList[startDebugIndex]
                if thisDebugData[isCluster] == isClusterConf.runTcpSend:
                    startDebugIndex += 1
                    continue

                if thisDebugData[isCluster] == isClusterConf.runDebugDone:
                    debugQueueList.remove(debugQueueList[startDebugIndex])
                    continue

                logging.info("当前处理的debug数据 %s" % thisDebugData)

                availableServiceCount = 0
                tmpServiceList = []
                for serviceIndex in range(0, len(serviceList)):
                    tmpService = serviceList[serviceIndex]
                    if thisDebugData[Do.TYPE_PROTOCOL] in tmpService[Do.KEY_RUN_SERVICE_PROTOCOL]:
                        if Do.KEY_RUN_SERVICE_CURRENT_CASE_LIST not in tmpService.keys():
                            tmpService[Do.KEY_RUN_SERVICE_CURRENT_CASE_LIST] = []
                        if tmpService[Do.KEY_RUN_SERVICE_CURRENT_CASE_PROGRESS_NUM] < tmpService[Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM]:
                            tmpService[Do.KEY_RUN_SERVICE_AVAILABLE_CASE_PROGRESS_NUM] = tmpService[Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM] - tmpService[Do.KEY_RUN_SERVICE_CURRENT_CASE_PROGRESS_NUM]
                            availableServiceCount += 1
                        else:
                            tmpService[Do.KEY_RUN_SERVICE_AVAILABLE_CASE_PROGRESS_NUM] = 0
                        serviceList[serviceIndex] = tmpService
                        tmpServiceList.append(tmpService)
                logging.debug("当前可用的servers数量 %s " % availableServiceCount)
                logging.debug("当前所有的的server %s " % serviceList)
                if availableServiceCount == 0:
                    continue
                else:
                    # 通过可执行的线程数量获取出可执行线程数量最多的服务器
                    tmpServiceList.sort(key=lambda x: x[Do.KEY_RUN_SERVICE_AVAILABLE_CASE_PROGRESS_NUM], reverse=True)

                sendTcpService = tmpServiceList[0]
                tmpCaseQueueIndex = debugQueueList[startDebugIndex]
                for tmpServiceListIndex in tmpServiceList:
                    if tmpCaseQueueIndex[isCluster] == isClusterConf.notRun:
                        tmpCaseQueueIndex[isCluster] = isClusterConf.runTcpSend
                        if sendTcp(tmpServiceListIndex[Do.KEY_RUN_SERVICE_IP], tmpServiceListIndex[Do.KEY_RUN_SERVICE_PORT], json.dumps(debugQueueList[startDebugIndex])):
                            if debugQueueList[startDebugIndex][Do.KEY_DO] == Do.TYPE_DEBUG_INTERFACE:
                                tmpServiceListIndex[Do.KEY_RUN_SERVICE_CURRENT_CASE_LIST].append("%s_%s" % (tmpCaseQueueIndex[Do.TYPE_PROTOCOL],tmpCaseQueueIndex[Do.KEY_INTERFACE_DEBUG_ID]))
                                tmpServiceListIndex[Do.KEY_RUN_SERVICE_CURRENT_CASE_PROGRESS_NUM] += 1
                            elif debugQueueList[startDebugIndex][Do.KEY_DO] == Do.TYPE_DEBUG_CASE:
                                tmpServiceListIndex[Do.KEY_RUN_SERVICE_CURRENT_CASE_LIST].append("%s_%s" % (tmpCaseQueueIndex[Do.TYPE_PROTOCOL],tmpCaseQueueIndex[Do.KEY_CASE_DEBUG_ID]))
                                tmpServiceListIndex[Do.KEY_RUN_SERVICE_CURRENT_CASE_PROGRESS_NUM] += 1
                            # 设置serviceListQueue
                            tmpCaseQueueIndex[isCluster] = isClusterConf.runTcpSend
                            sendTcpService = tmpServiceListIndex
                            debugQueueList[startDebugIndex] = tmpCaseQueueIndex
                            break
                        else:
                            logging.error("任务执行的TCP发送失败！%s" % json.dumps(debugQueueList[0]))
                            tmpCaseQueueIndex[isCluster] = isClusterConf.notRun
                            debugQueueList[startDebugIndex] = tmpCaseQueueIndex
                            continue
                for serviceListIndex in range(0, len(serviceList)):
                    tmpServiceListData = serviceList[serviceListIndex]
                    if tmpServiceListData[Do.KEY_RUN_SERVICE_IP] == sendTcpService[Do.KEY_RUN_SERVICE_IP] and \
                                    tmpServiceListData[Do.KEY_RUN_SERVICE_PORT] == sendTcpService[Do.KEY_RUN_SERVICE_PORT]:
                        serviceList[serviceListIndex] = sendTcpService

                startDebugIndex += 1
            except:
                logging.error(traceback.format_exc())
                continue
        else:
            time.sleep(1)

#
# @catch_exception
# @take_time
# def progress_allocating_taskSuite(taskSuiteList,serviceList):
#     while True:
#         startTaskSuiteIndex = 0
#         while startTaskSuiteIndex < len(taskSuiteList):
#             thisTaskSuiteData = taskSuiteList[startTaskSuiteIndex]
#             if thisTaskSuiteData[isCluster] == isClusterConf.runTcpSend:
#                 startTaskSuiteIndex += 1
#                 continue
#
#             if thisTaskSuiteData[isCluster] == isClusterConf.runDebugDone:
#                 taskSuiteList.remove(taskSuiteList[startTaskSuiteIndex])
#                 continue
#
#             logging.info("当前处理的debug数据 %s" % thisTaskSuiteData)
#
#             availableServiceCount = 0
#             tmpServiceList = []
#             for serviceIndex in range(0, len(serviceList)):
#                 tmpService = serviceList[serviceIndex]
#                 if thisTaskSuiteData[Do.TYPE_PROTOCOL] in tmpService[Do.KEY_RUN_SERVICE_PROTOCOL]:
#                     if Do.KEY_RUN_SERVICE_CURRENT_CASE_LIST not in tmpService.keys():
#                         tmpService[Do.KEY_RUN_SERVICE_CURRENT_CASE_LIST] = []
#                     if tmpService[Do.KEY_RUN_SERVICE_CURRENT_CASE_PROGRESS_NUM] < tmpService[
#                         Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM]:
#                         tmpService[Do.KEY_RUN_SERVICE_AVAILABLE_CASE_PROGRESS_NUM] = tmpService[
#                                                                                          Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM] - \
#                                                                                      tmpService[
#                                                                                          Do.KEY_RUN_SERVICE_CURRENT_CASE_PROGRESS_NUM]
#                         availableServiceCount += 1
#                     else:
#                         tmpService[Do.KEY_RUN_SERVICE_AVAILABLE_CASE_PROGRESS_NUM] = 0
#                     serviceList[serviceIndex] = tmpService
#                     tmpServiceList.append(tmpService)
#             logging.debug("当前可用的servers数量 %s " % availableServiceCount)
#             logging.debug("当前所有的的server %s " % serviceList)
#             if availableServiceCount == 0:
#                 continue
#             else:
#                 # 通过可执行的线程数量获取出可执行线程数量最多的服务器
#                 tmpServiceList.sort(key=lambda x: x[Do.KEY_RUN_SERVICE_AVAILABLE_CASE_PROGRESS_NUM], reverse=True)
#
#             sendTcpService = tmpServiceList[0]
#             for tmpServiceListIndex in tmpServiceList:
#                 if thisTaskSuiteData[isCluster] == isClusterConf.notRun:
#                     thisTaskSuiteData[isCluster] = isClusterConf.runTcpSend
#                     if sendTcp(tmpServiceListIndex[Do.KEY_RUN_SERVICE_IP], tmpServiceListIndex[Do.KEY_RUN_SERVICE_PORT],
#                                json.dumps(thisTaskSuiteData)):
#
#                         tmpServiceListIndex[Do.KEY_RUN_SERVICE_CURRENT_CASE_LIST].append("%s_%s" % (
#                         tmpCaseQueueIndex[Do.TYPE_PROTOCOL], tmpCaseQueueIndex[Do.KEY_CASE_DEBUG_ID]))
#                         tmpServiceListIndex[Do.KEY_RUN_SERVICE_CURRENT_CASE_PROGRESS_NUM] += 1
#                         # 设置serviceListQueue
#                         tmpCaseQueueIndex[isCluster] = isClusterConf.runTcpSend
#                         sendTcpService = tmpServiceListIndex
#                         debugQueueList[startDebugIndex] = tmpCaseQueueIndex
#                         break
#                     else:
#                         logging.error("任务执行的TCP发送失败！%s" % json.dumps(debugQueueList[0]))
#                         tmpCaseQueueIndex[isCluster] = isClusterConf.notRun
#                         debugQueueList[startDebugIndex] = tmpCaseQueueIndex
#                         continue
#             for serviceListIndex in range(0, len(serviceList)):
#                 tmpServiceListData = serviceList[serviceListIndex]
#                 if tmpServiceListData[Do.KEY_RUN_SERVICE_IP] == sendTcpService[Do.KEY_RUN_SERVICE_IP] and \
#                                 tmpServiceListData[Do.KEY_RUN_SERVICE_PORT] == sendTcpService[Do.KEY_RUN_SERVICE_PORT]:
#                     serviceList[serviceListIndex] = sendTcpService
#
#             startDebugIndex += 1
#         else:
#             time.sleep(1)