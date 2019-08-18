from runfunc.initial import *
from allmodels.DubboTask import DubboTask
from progress.DubboTaskProgress import *
from progress.DubboCaseDebugProgress import *
from core.config.InitConfig import isClusterConf,rootDir
# lock = threading.RLock() #线程锁

@catch_exception
@take_time
def progress_process_debug_queue(debugQueueList):
    #DONE 处理调试队列 debugQueue  从这里实现多线程的分发，哪些user已经调试中需要停止线程等等。
    while True:
        if len(debugQueueList) > 0:
            try:
                logging.info("thread_process_debug_queue: debugQueue:%s" % debugQueueList)
                thisDebugData = debugQueueList[0]
                debugType = thisDebugData[Do.KEY_DO]
                logging.info("thread_process_debug_queue: 开始处理调试：%s" % thisDebugData)

                if debugType == Do.TYPE_DEBUG_INTERFACE:
                    #进行接口调试
                    interfaceDebugId = thisDebugData[Do.KEY_INTERFACE_DEBUG_ID]

                    tmpProcess = CaseDebugProcess(debugType=debugType,interfaceDebugId=interfaceDebugId)
                    tmpProcess.start()
                    debugQueueList.remove(debugQueueList[0])
                    # debugThreadDict[addBy] = tmpThread
                elif debugType == Do.TYPE_DEBUG_CASE:
                    #进行用例调试
                    caseDebugId = thisDebugData[Do.KEY_CASE_DEBUG_ID]
                    caseStepDebugIdList = thisDebugData[Do.KEY_CASE_STEP_DEBUG_ID_LIST]

                    tmpProcess = CaseDebugProcess(debugType=debugType,testCaseDebugId=caseDebugId,testCaseStepDebugId=caseStepDebugIdList)
                    tmpProcess.start()
                    debugQueueList.remove(debugQueueList[0])
                    # debugThreadDict[addBy] = tmpThread
                else:
                    #错误的调试类型
                    logging.error("错误的类型！")
                # debugQueue.remove(debugQueue[0])
                logging.info ("thread_process_debug_queue: 调试处理完毕" )
            except Exception as e:
                logging.error("不可知异常：%s" % traceback.format_exc())
                logging.error("当前队列为数量为%s " % debugQueueList)
                continue
                # debugQueue.remove(debugQueue[0])
        else:
            time.sleep(1)

############################单环境并发执行所需变量#####################################################
from core.config.InitConfig import CommonConf
maxRuntaskThreadNums = CommonConf.runtaskMaxThreadNums  #任务执行做多的线程数
maxTaskNumsInSingleEnv = CommonConf.singleServiceEnvRunTaskNumber  #单环境执行最多任务数量
############################单环境并发执行所需变量#####################################################
@catch_exception
@take_time
def process_task_queue_SingleEnvToMultiTask(runTaskQueueList,runTaskCancelQueueList,serviceProgressDict,serverDataDict):
    #TODO 单环境可同时执行多任务
    while True:
        #将进程队列中的任务拿到本进程的list中
        try:
            taskStartIndex = 0
            # while len(runTaskQueueList) > taskStartIndex :
            if len(runTaskQueueList) > taskStartIndex:

                taskObject = Task()
                taskExecId = runTaskQueueList[taskStartIndex][Do.KEY_TASK_EXECUTE_ID]
                taskObject.taskExecuteId = taskExecId
                #这里是设置task执行的地方 ~！！！！
                taskObject.generateByTaskExecuteId()
                if taskObject.taskId == None or taskObject.taskId.strip() =="":
                    logging.info("thread_process_task_queue: 没有查到任务执行信息taskExecId[%s]。" % taskExecId)
                    runTaskQueueList.remove(runTaskQueueList[taskStartIndex])
                    continue

                serviceConfKey = taskObject.confHttpLayer.key
                #通过执行查询结果找到confServiceKey作为多线程的主键,如果存在且alive阻塞,开始执行下一个
                if serviceConfKey == None or serviceConfKey.strip() == "":
                    logging.error("thread_process_task_queue: 任务执行获取不到执行环境，请检查错误。")
                    runTaskQueueList.remove(runTaskQueueList[taskStartIndex])
                    continue

                taskExecuteId = taskObject.taskExecuteId #之前已经检测过taskId，不需要重复检测
                try:

                    if serviceConfKey not in serviceProgressDict.keys():
                        serviceProgressDict[serviceConfKey] = {"AliveProgressCount": 0}

                    serviceProgressDict["AliveProgressCount"] = 0
                    for tmpEnvKey in list(serviceProgressDict.keys()):
                        if tmpEnvKey != "AliveProgressCount":
                            serviceProgressDict[tmpEnvKey]["AliveProgressCount"] = 0
                            for tmpTaskKey in list(serviceProgressDict[tmpEnvKey].keys()):
                                if tmpTaskKey != "AliveProgressCount":
                                    if serviceProgressDict[tmpEnvKey][tmpTaskKey]["progress"].is_alive():
                                        serviceProgressDict["AliveProgressCount"] += 1
                                        serviceProgressDict[tmpEnvKey]["AliveProgressCount"] += 1
                                    else:
                                        serviceProgressDict[tmpEnvKey].pop(tmpTaskKey)

                    tmpTaskQueue = runTaskQueueList[taskStartIndex]
                    tmpServiceList = serverDataDict[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST]
                    tmpServiceList.append("%s_%s" % (tmpTaskQueue[Do.TYPE_PROTOCOL],tmpTaskQueue[Do.KEY_TASK_EXECUTE_ID]))
                    serverDataDict[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST] = tmpServiceList
                    serverDataDict["%s_%s" % (tmpTaskQueue[Do.TYPE_PROTOCOL],tmpTaskQueue[Do.KEY_TASK_EXECUTE_ID])] = isClusterConf.runTcpSend
                    # serverDataDict[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST] =
                    serverDataDict[Do.KEY_RUN_SERVICE_CURRENT_TASK_PROGRESS_NUM] += 1
                    tmpProgress = TaskProgress(taskExecuteId=taskExecId,runTaskServiceIp=serverDataDict[Do.KEY_RUN_SERVICE_IP],taskSuiteExecuteId=runTaskQueueList[taskStartIndex][Do.KEY_TASK_SUITE_EXECUTE_ID],serverDataDict=serverDataDict)
                    tmpProgress.start()
                    runTaskQueueList.remove(runTaskQueueList[taskStartIndex])
                    tcpStr = '{"do":%s,"TaskExecuteId":%s,"%s":"%s"}' % (Do.TYPE_TASK_INIT_DONE,taskObject.taskExecuteId,Do.TYPE_PROTOCOL,taskObject.protocol)
                    if not sendTcp(TcpServerConf.ip, TcpServerConf.port, tcpStr):
                        logging.error("任务初始化完毕 TCP回调函数发生异常！ %s " % tcpStr)

                    tmpServiceDict = serviceProgressDict[serviceConfKey]
                    tmpServiceDict[taskExecuteId] = {}
                    tmpServiceDict[taskExecuteId]['progress'] = tmpProgress
                    tmpServiceDict[taskExecuteId]['taskExecuteId'] = taskExecId
                    serviceProgressDict[serviceConfKey] = tmpServiceDict
                    logging.info("thread_process_task_queue: 任务%s处理完毕,开始执行" % taskExecId)


                except Exception as e:
                    logging.error(traceback.format_exc())
                finally:
                    pass

            if len(runTaskCancelQueueList) > taskStartIndex:
                tmpTask = Task()
                tmpTask.taskExecuteId = runTaskCancelQueueList[taskStartIndex]["TaskExecuteId"]
                tmpTask.generateByTaskExecuteId()
                if serviceConfKey in serviceProgressDict.keys():
                    if tmpTask.taskExecuteId in serviceProgressDict[serviceConfKey].keys():
                        taskDict = serviceProgressDict[serviceConfKey][tmpTask.taskExecuteId]
                        tmpProgress = serviceProgressDict[serviceConfKey][tmpTask.taskExecuteId]['progress']
                        if int(taskDict['taskExecuteId']) == int(tmpTask.taskExecuteId) and tmpProgress.is_alive():
                            # 执行线程结束操作
                            stop_progress(tmpProgress)
                            logging.debug("thread_process_task_cancel: 结束任务执行线程【%s】" % tmpTask.taskExecuteId)
                        serviceProgressDict[serviceConfKey].pop(tmpTask.taskExecuteId)
                res = tmpTask.cancelTask()
                tmpRunTaskCancelQueue = runTaskCancelQueueList[taskStartIndex]
                tmpExecuteId = "%s_%s" % (tmpRunTaskCancelQueue[Do.TYPE_PROTOCOL],tmpRunTaskCancelQueue[Do.KEY_TASK_EXECUTE_ID])
                if tmpExecuteId in serverDataDict.keys():
                    serverDataDict.pop(tmpExecuteId)

                if tmpExecuteId in serverDataDict[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST]:
                    tmpTaskList = serverDataDict[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST]
                    tmpTaskList.remove(tmpExecuteId)
                    serverDataDict[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST] = tmpTaskList
                    if serverDataDict[Do.KEY_RUN_SERVICE_CURRENT_TASK_PROGRESS_NUM] > 0:
                        serverDataDict[Do.KEY_RUN_SERVICE_CURRENT_TASK_PROGRESS_NUM] -= 1

                if res != 0 and res == False:
                    logging.error("thread_process_task_cancel: 任务执行ID[%s]取消失败，请检查错误！" % tmpTask.taskExecuteId)
                else:
                    # 取消成功
                    logging.info("thread_process_task_cancel: 任务执行ID[%s]取消成功！" % tmpTask.taskExecuteId)

                runTaskCancelQueueList.remove(runTaskCancelQueueList[0])
                for i in range(0,len(runTaskQueueList)):
                    if runTaskQueueList[i][Do.KEY_TASK_EXECUTE_ID] == tmpTask.taskExecuteId:
                        runTaskQueueList.remove(runTaskQueueList[i])
                tcpStr = '{"do":%s,"TaskExecuteId":%s,"%s":"%s","%s":"%s"}' % (Do.TYPE_TASK_CANCEL_DONE, tmpTask.taskExecuteId,Do.TYPE_PROTOCOL,tmpTask.protocol,Do.KEY_TASK_SUITE_EXECUTE_ID,tmpTask.taskSuiteExecuteId)
                if not sendTcp(TcpServerConf.ip, TcpServerConf.port, tcpStr):
                    logging.error("任务取消完毕 TCP回调函数发生异常！ %s " % tcpStr)
                continue
        except:
            logging.error(traceback.format_exc())
            continue
        if len(runTaskQueueList) != 0 or len(runTaskCancelQueueList) != 0:
            continue
        #如果退出第一遍遍历，并启动完线程，需要休眠1s
        time.sleep(1)





@catch_exception
@take_time
def progress_process_dubbo_task(runTaskDubboQueueList,runTaskDubboCancelQueueList,serviceDubboProgressDict,serverDataDict):
    while True:
        try:
            # 将进程队列中的任务拿到本进程的list中
            taskStartIndex = 0
            # while len(runTaskQueueList) > taskStartIndex :
            if len(runTaskDubboQueueList) > taskStartIndex:

                taskObject = DubboTask()
                taskExecId = runTaskDubboQueueList[taskStartIndex][Do.KEY_TASK_EXECUTE_ID]
                taskObject.taskExecuteId = taskExecId
                # 这里是设置task执行的地方 ~！！！！
                taskObject.generateByTaskExecuteId()
                if taskObject.taskId == None or taskObject.taskId.strip() == "":
                    logging.info("thread_process_task_queue: 没有查到任务执行信息taskExecId[%s]。" % taskExecId)
                    runTaskDubboQueueList.remove(runTaskDubboQueueList[taskStartIndex])
                    continue

                serviceConfKey = taskObject.confHttpLayer.key
                # 通过执行查询结果找到confServiceKey作为多线程的主键,如果存在且alive阻塞,开始执行下一个
                if serviceConfKey == None or serviceConfKey.strip() == "":
                    logging.error("thread_process_task_queue: 任务执行获取不到执行环境，请检查错误。")
                    runTaskDubboQueueList.remove(runTaskDubboQueueList[taskStartIndex])
                    continue

                taskExecuteId = taskObject.taskExecuteId  # 之前已经检测过taskId，不需要重复检测
                try:

                    if serviceConfKey not in serviceDubboProgressDict.keys():
                        serviceDubboProgressDict[serviceConfKey] = {"AliveProgressCount": 0}

                    serviceDubboProgressDict["AliveProgressCount"] = 0
                    for tmpEnvKey in list(serviceDubboProgressDict.keys()):
                        if tmpEnvKey != "AliveProgressCount":
                            serviceDubboProgressDict[tmpEnvKey]["AliveProgressCount"] = 0
                            for tmpTaskKey in list(serviceDubboProgressDict[tmpEnvKey].keys()):
                                if tmpTaskKey != "AliveProgressCount":
                                    if serviceDubboProgressDict[tmpEnvKey][tmpTaskKey]["progress"].is_alive():
                                        serviceDubboProgressDict["AliveProgressCount"] += 1
                                        serviceDubboProgressDict[tmpEnvKey]["AliveProgressCount"] += 1
                                    else:
                                        serviceDubboProgressDict[tmpEnvKey].pop(tmpTaskKey)


                    tmpTaskQueue = runTaskDubboQueueList[taskStartIndex]
                    tmpServiceList = serverDataDict[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST]
                    tmpServiceList.append("%s_%s" % (tmpTaskQueue[Do.TYPE_PROTOCOL], tmpTaskQueue[Do.KEY_TASK_EXECUTE_ID]))
                    serverDataDict[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST] = tmpServiceList
                    serverDataDict["%s_%s" % (
                    tmpTaskQueue[Do.TYPE_PROTOCOL], tmpTaskQueue[Do.KEY_TASK_EXECUTE_ID])] = isClusterConf.runTcpSend
                    serverDataDict[Do.KEY_RUN_SERVICE_CURRENT_TASK_PROGRESS_NUM] += 1
                    tmpProgress = DubboTaskProgress(taskExecuteId=taskExecId,runTaskServiceIp=serverDataDict[Do.KEY_RUN_SERVICE_IP],taskSuiteExecuteId=runTaskDubboQueueList[taskStartIndex][Do.KEY_TASK_SUITE_EXECUTE_ID],serverDataDict=serverDataDict)
                    tmpProgress.start()



                    runTaskDubboQueueList.remove(runTaskDubboQueueList[taskStartIndex])
                    tcpStr = '{"do":%s,"TaskExecuteId":%s,"%s":"%s"}' % (Do.TYPE_TASK_INIT_DONE, taskObject.taskExecuteId,Do.TYPE_PROTOCOL,taskObject.protocol)
                    if not sendTcp(TcpServerConf.ip, TcpServerConf.port, tcpStr):
                        logging.error("任务初始化完毕 TCP回调函数发生异常！ %s " % tcpStr)

                    tmpServiceDict = serviceDubboProgressDict[serviceConfKey]
                    tmpServiceDict[taskExecuteId] = {}
                    tmpServiceDict[taskExecuteId]['progress'] = tmpProgress
                    tmpServiceDict[taskExecuteId]['taskExecuteId'] = taskExecId
                    serviceDubboProgressDict[serviceConfKey] = tmpServiceDict
                    logging.info("thread_process_task_queue: 任务%s处理完毕" % taskExecId)
                    continue

                except Exception as e:
                    logging.error(traceback.format_exc())
                finally:
                    pass
            if len(runTaskDubboCancelQueueList) > taskStartIndex:
                tmpTask = DubboTask()
                tmpTask.taskExecuteId = runTaskDubboCancelQueueList[taskStartIndex]["TaskExecuteId"]
                tmpTask.generateByTaskExecuteId()
                if serviceConfKey in serviceDubboProgressDict.keys():
                    if tmpTask.taskExecuteId in serviceDubboProgressDict[serviceConfKey].keys():
                        taskDict = serviceDubboProgressDict[serviceConfKey][tmpTask.taskExecuteId]
                        tmpProgress = serviceDubboProgressDict[serviceConfKey][tmpTask.taskExecuteId]['progress']
                        if int(taskDict['taskExecuteId']) == int(tmpTask.taskExecuteId) and tmpProgress.is_alive():
                            # 执行线程结束操作
                            stop_progress(tmpProgress)
                            logging.debug("thread_process_task_cancel: 结束任务执行线程【%s】" % tmpTask.taskExecuteId)
                        serviceDubboProgressDict[serviceConfKey].pop(tmpTask.taskExecuteId)
                res = tmpTask.cancelTask()
                tmpRunTaskCancelQueue = runTaskDubboCancelQueueList[taskStartIndex]
                tmpExecuteId = "%s_%s" % (tmpRunTaskCancelQueue[Do.TYPE_PROTOCOL], tmpRunTaskCancelQueue[Do.KEY_TASK_EXECUTE_ID])
                if tmpExecuteId in serverDataDict.keys():
                    serverDataDict.pop(tmpExecuteId)

                if tmpExecuteId in serverDataDict[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST]:
                    tmpTaskList = serverDataDict[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST]
                    tmpTaskList.remove(tmpExecuteId)
                    serverDataDict[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST] = tmpTaskList
                    if serverDataDict[Do.KEY_RUN_SERVICE_CURRENT_TASK_PROGRESS_NUM] > 0:
                        serverDataDict[Do.KEY_RUN_SERVICE_CURRENT_TASK_PROGRESS_NUM] -= 1
                if res != 0 and res == False:
                    logging.error("thread_process_task_cancel: 任务执行ID[%s]取消失败，请检查错误！" % tmpTask.taskExecuteId)
                else:
                    # 取消成功
                    logging.info("thread_process_task_cancel: 任务执行ID[%s]取消成功！" % tmpTask.taskExecuteId)

                runTaskDubboCancelQueueList.remove(runTaskDubboCancelQueueList[0])
                for i in range(0, len(runTaskDubboQueueList)):
                    if runTaskDubboQueueList[i][Do.KEY_TASK_EXECUTE_ID] == tmpTask.taskExecuteId:
                        runTaskDubboQueueList.remove(runTaskDubboQueueList[i])
                tcpStr = '{"do":%s,"TaskExecuteId":%s,"%s":"%s"}' % (Do.TYPE_TASK_CANCEL_DONE, tmpTask.taskExecuteId,Do.TYPE_PROTOCOL,tmpTask.protocol)
                if not sendTcp(TcpServerConf.ip, TcpServerConf.port, tcpStr):
                    logging.error("任务取消完毕 TCP回调函数发生异常！ %s " % tcpStr)
                continue
        except:
            logging.error(traceback.format_exc())
            continue

        if len(runTaskDubboQueueList) != 0 or len(runTaskDubboCancelQueueList) != 0:
            continue
        # 如果退出第一遍遍历，并启动完线程，需要休眠1s
        time.sleep(1)

@catch_exception
@take_time
def progress_process_dubbo_debug_queue(debugQueueList):
    # DONE 处理调试队列 debugQueue  从这里实现多线程的分发，哪些user已经调试中需要停止线程等等。
    while True:
        if len(debugQueueList) > 0:
            try:
                logging.info("thread_process_debug_queue: debugQueue:%s" % debugQueueList)
                thisDebugData = debugQueueList[0]
                debugType = thisDebugData[Do.KEY_DO]
                logging.info("thread_process_debug_queue: 开始处理调试：%s" % thisDebugData)

                if debugType == Do.TYPE_DEBUG_INTERFACE:
                    # 进行接口调试
                    interfaceDebugId = thisDebugData[Do.KEY_INTERFACE_DEBUG_ID]

                    tmpProcess = DubboCaseDebugProgress(debugType=debugType, interfaceDebugId=interfaceDebugId)
                    tmpProcess.start()
                    debugQueueList.remove(debugQueueList[0])
                    # debugThreadDict[addBy] = tmpThread
                elif debugType == Do.TYPE_DEBUG_CASE:
                    # 进行用例调试
                    caseDebugId = thisDebugData[Do.KEY_CASE_DEBUG_ID]
                    caseDebugStepId = thisDebugData[Do.KEY_CASE_STEP_DEBUG_ID_LIST]
                    tmpProcess = DubboCaseDebugProgress(debugType=debugType, caseDebugId=caseDebugId,caseDebugStepId=caseDebugStepId)
                    tmpProcess.start()
                    debugQueueList.remove(debugQueueList[0])
                    # debugThreadDict[addBy] = tmpThread
                else:
                    # 错误的调试类型
                    logging.error("错误的类型！")
                # debugQueue.remove(debugQueue[0])
                logging.info("thread_process_debug_queue: 调试处理完毕")
            except Exception as e:
                logging.error("不可知异常：%s" % traceback.format_exc())
                logging.error("当前队列为数量为%s " % debugQueueList)
                continue
        else:
            time.sleep(1)

# @catch_exception
# @take_time
# def process_task_cancel_SingleEnvToMultiTask(runTaskCancelQueueList,runTaskQueueList,serviceProgressDict):
#     #TODO 单环境可同时执行多任务 取消任务
#     while True:
#         print("runTaskCancelQueueList",runTaskCancelQueueList)
#         if len(runTaskCancelQueueList) > 0 :
#             logging.info("thread_process_task_cancel: taskCancelQueue:%s" % runTaskCancelQueueList)
#             taskType = runTaskCancelQueueList[0][Do.KEY_DO]
#             taskExecuteId = runTaskCancelQueueList[0][Do.KEY_TASK_EXECUTE_ID]
#             logging.info("thread_process_task_cancel: 开始处理任务取消：%s" % runTaskCancelQueueList[0])
#             if taskType == Do.TYPE_TASK_CANCEL:
#                 #进行接口调试
#                 tmpTask = Task()
#                 tmpTask.taskExecuteId = taskExecuteId
#                 tmpTask.generateByTaskExecuteId()
#                 # 处理已经存在的线程
#                 # serviceConfKey = tmpTask.confHttpLayer.confServiceLayer.key
#                 serviceConfKey = tmpTask.confHttpLayer.key
#                 try:
#                     # mutex.acquire()
#                     if serviceConfKey in serviceProgressDict.keys():
#                         if tmpTask.taskId in serviceProgressDict[serviceConfKey].keys():
#                             taskDict = serviceProgressDict[serviceConfKey][tmpTask.taskId]
#                             tmpProgress = serviceProgressDict[serviceConfKey][tmpTask.taskId]['progress']
#                             if int(taskDict['taskExecuteId']) == int(taskExecuteId) and tmpProgress.is_alive():
#                                 # 执行线程结束操作
#                                 stop_progress(tmpProgress)
#                                 logging.debug("thread_process_task_cancel: 结束任务执行线程【%s】" % taskExecuteId)
#                 except Exception as e:
#                     logging.error(traceback.format_exc())
#                 finally:
#                     pass
#                     # mutex.release()
#
#                 logging.debug("thread_process_task_cancel: 任务%s开始取消！" % taskExecuteId)
#                 res = tmpTask.cancelTask()
#                 logging.debug("thread_process_task_cancel: 任务取消返回结果：%s" % str(res))
#                 if res:
#                     #取消成功
#                     logging.info("thread_process_task_cancel: 任务执行ID[%s]取消成功！" % taskExecuteId)
#
#                 else:
#                     logging.error("thread_process_task_cancel: 任务执行ID[%s]取消失败，请检查错误！" % taskExecuteId)
#             else:
#                 #错误的调试类型
#                 logging.error("thread_process_task_cancel: 错误的类型！")
#             # if lock.acquire():
#             runTaskCancelQueueList.remove(runTaskCancelQueueList[0])
#             # lock.release()
#             for i in range(0,len(runTaskQueueList)):
#                 if runTaskQueueList[i][Do.KEY_TASK_EXECUTE_ID] == taskExecuteId:
#                     # if lock.acquire():
#                     tmpRunTaskData = runTaskQueueList[i]
#                     tmpRunTaskData[isCluster] = isClusterConf.cancelTaskDone
#                     runTaskQueueList[i] = tmpRunTaskData
#                     # lock.release()
#                     break
#
#             logging.info ("thread_process_task_cancel: 任务%s取消完毕" % taskExecuteId )
#         else:
#             time.sleep(1)
