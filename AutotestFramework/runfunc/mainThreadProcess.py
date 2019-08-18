from runfunc.initial import *
from core.config.InitConfig import ServiceConf,isClusterConf
# lock = threading.RLock() #线程锁

@catch_exception
@take_time
def thread_process_allocating_task():
    while True:
        taskStartIndex = 0
        while len(taskClusterQueue) > taskStartIndex:
            try:
                # # 如果有任务已经执行完或已删除
                if taskClusterQueue[taskStartIndex][isCluster] == isClusterConf.runTaskDone or taskClusterQueue[taskStartIndex][isCluster] == isClusterConf.cancelTaskDone:
                    for serviceIndex in ServiceConf.serviceConfList:
                        if Do.KEY_TASK_EXECUTE_ID_LIST not in serviceIndex.keys():
                            serviceIndex[Do.KEY_TASK_EXECUTE_ID_LIST] = []
                        if int(taskClusterQueue[taskStartIndex][Do.KEY_TASK_EXECUTE_ID]) in serviceIndex[Do.KEY_TASK_EXECUTE_ID_LIST]:
                            serviceIndex[Do.KEY_TASK_EXECUTE_ID_LIST].remove(int(taskClusterQueue[taskStartIndex][Do.KEY_TASK_EXECUTE_ID]))
                            serviceIndex["currentThreadNum"] -= 1
                    taskClusterQueue.remove(taskClusterQueue[taskStartIndex])
                    break

                #查出所有在执行中的任务和自己比较
                taskIndexIsStart = True
                for taskIndex in taskClusterQueue:
                    if taskIndex[isCluster] != isClusterConf.notRun:
                        if taskClusterQueue[taskStartIndex][Do.KEY_TASK_EXECUTE_ENV] == taskIndex[Do.KEY_TASK_EXECUTE_ENV]:
                            if taskClusterQueue[taskStartIndex][Do.KEY_TASK_ID] == taskIndex[Do.KEY_TASK_ID]:
                                taskIndexIsStart = False

                #没有同环境同任务执行，可以立即执行
                if taskIndexIsStart:
                    logging.info("thread_process_allocating_task: Processed_taskQueue : %s " % ServiceConf.serviceConfList)
                    logging.info("thread_process_allocating_task: 开始处理 : %s " % taskClusterQueue[taskStartIndex])
                    availableServiceList = []
                    for serviceIndex in ServiceConf.serviceConfList:
                        if Do.KEY_TASK_EXECUTE_ID_LIST not in serviceIndex.keys():
                            serviceIndex[Do.KEY_TASK_EXECUTE_ID_LIST] = []
                        if serviceIndex["currentThreadNum"] < serviceIndex["maxThreadNum"]:
                            serviceIndex["availableThreadNum"] = serviceIndex["maxThreadNum"] - serviceIndex["currentThreadNum"]
                            availableServiceList.append(serviceIndex)
                    logging.debug("当前可用的server %s " % availableServiceList)
                    logging.debug("当前所有的的server %s " % ServiceConf.serviceConfList)
                    #现在没有可用的执行服务器
                    if len(availableServiceList) == 0:
                        taskStartIndex += 1
                        continue
                    else:
                        #通过可执行的线程数量获取出可执行线程数量最多的服务器
                        availableServiceList.sort(key=lambda x:x['availableThreadNum'],reverse=True)
                        tcpStr = '{"do":3,"TaskExecuteId":"%s","TaskExecuteEnv":"%s","TaskId":"%s"}'%(taskClusterQueue[taskStartIndex][Do.KEY_TASK_EXECUTE_ID],taskClusterQueue[taskStartIndex][Do.KEY_TASK_EXECUTE_ENV],taskClusterQueue[taskStartIndex][Do.KEY_TASK_ID])
                        #发送tcp请求
                        for availableServiceIndex in availableServiceList:
                            if taskClusterQueue[taskStartIndex][isCluster] == isClusterConf.notRun:
                                taskClusterQueue[taskStartIndex][isCluster] = isClusterConf.runTcpSend
                                if sendTcp(availableServiceList[0]["ip"],availableServiceIndex["port"],tcpStr):
                                    availableServiceIndex[Do.KEY_TASK_EXECUTE_ID_LIST].append(int(taskClusterQueue[taskStartIndex][Do.KEY_TASK_EXECUTE_ID]))
                                    availableServiceIndex["currentThreadNum"] += 1
                                    taskClusterQueue[taskStartIndex]["ip"] = availableServiceIndex["ip"]
                                    taskClusterQueue[taskStartIndex]["port"] = availableServiceIndex["port"]
                                    break
                                else:
                                    logging.error("任务执行的TCP发送失败！%s" % tcpStr)
                                    taskClusterQueue[taskStartIndex][isCluster] = isClusterConf.notRun
                                    continue

                else:
                    taskStartIndex += 1
                    continue
            except Exception:
                logging.error(traceback.format_exc())
                break

@catch_exception
@take_time
def thread_process_allocating_task_cancel():
    while True:
        if len(taskClusterCancelQueue) > 0:
            logging.info("thread_process_allocating_task_cancel ： 开始处理取消任务：%s " % taskClusterCancelQueue[0])
            logging.info("thread_process_allocating_task_cancel ： 开始处理取消任务：%s " % taskClusterQueue)
            logging.info("thread_process_allocating_task_cancel ：取消任务：%s " % ServiceConf.serviceConfList)
            isCancel = True
            for taskClusterQueueIndex in taskClusterQueue:
                if taskClusterCancelQueue[0][Do.KEY_TASK_EXECUTE_ID] != taskClusterQueueIndex[Do.KEY_TASK_EXECUTE_ID]:
                    continue
                tcpIp = ""
                tcpPort = 0
                for serviceConfIndex in ServiceConf.serviceConfList:
                    if taskClusterCancelQueue[0][Do.KEY_TASK_EXECUTE_ID] in serviceConfIndex[Do.KEY_TASK_EXECUTE_ID_LIST]:
                        print(serviceConfIndex[Do.KEY_TASK_EXECUTE_ID_LIST])
                        tcpIp = serviceConfIndex["ip"]
                        tcpPort = serviceConfIndex["port"]
                if tcpIp != "":
                    tcpStr = '{"do":%s,"TaskExecuteId":%s}' % (Do.TYPE_TASK_CANCEL, taskClusterCancelQueue[0][Do.KEY_TASK_EXECUTE_ID])
                    if taskClusterQueueIndex[isCluster] == isClusterConf.toCancel or taskClusterQueueIndex[isCluster] == isClusterConf.runTaskInitDone:
                        logging.debug("%s 的状态为 %s" % (taskClusterCancelQueue[0][Do.KEY_TASK_EXECUTE_ID],taskClusterQueueIndex[isCluster]))
                        taskClusterQueueIndex[isCluster] = isClusterConf.cancelTcpSend
                        if sendTcp(tcpIp, tcpPort, tcpStr):
                            logging.info("取消%s成功" % taskClusterCancelQueue[0])
                            taskClusterCancelQueue.remove(taskClusterCancelQueue[0])
                            taskClusterQueueIndex[isCluster] = isClusterConf.cancelTaskDone
                            isCancel = False
                            break
                        else:
                            isCancel = True
                            logging.error("任务取消 TCP 发送失败")
                    else:
                        isCancel = False
                        logging.info("任务状态为%s,暂时不可取消，等待下次" % taskClusterQueueIndex[isCluster])
                else:
                    isCancel = True
                    logging.info("未获取到TCP信息，主服务执行取消")


            if isCancel:
                for taskClusterQueueIndex in taskClusterQueue:
                    if int(taskClusterCancelQueue[0][Do.KEY_TASK_EXECUTE_ID]) == int(taskClusterQueueIndex[Do.KEY_TASK_EXECUTE_ID]):
                        taskClusterQueueIndex[isCluster] = isClusterConf.cancelTaskDone
                        break
                tmpTask = Task()
                tmpTask.taskExecuteId = taskClusterCancelQueue[0][Do.KEY_TASK_EXECUTE_ID]
                tmpTask.generateByTaskExecuteId()
                res = tmpTask.cancelTask()
                if res:
                    logging.info("%s 任务取消成功" % taskClusterCancelQueue[0][Do.KEY_TASK_EXECUTE_ID])

                else:
                    logging.error("%s 任务取消失败" % taskClusterCancelQueue[0][Do.KEY_TASK_EXECUTE_ID])
                taskClusterCancelQueue.remove(taskClusterCancelQueue[0])
