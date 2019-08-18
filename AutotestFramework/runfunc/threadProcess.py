from runfunc.initial import *
from core.config.InitConfig import isClusterConf,rootDir
# lock = threading.RLock() #线程锁

@catch_exception
@take_time
def process_debug_queue(debugQueue):
    #DONE 处理调试队列 debugQueue  从这里实现多线程的分发，哪些user已经调试中需要停止线程等等。
    while True:
        if debugQueue.qsize() > 0:
            try:
                logging.info("thread_process_debug_queue: debugQueue:%s" % debugQueue)
                thisDebugData = debugQueue.get()
                print("thisDebugData",thisDebugData)
                debugType = thisDebugData[Do.KEY_DO]
                logging.info("thread_process_debug_queue: 开始处理调试：%s" % thisDebugData)

                if debugType == Do.TYPE_DEBUG_INTERFACE:
                    #进行接口调试
                    # interfaceDebugId = int(debugQueue[0][Do.KEY_INTERFACE_DEBUG_ID])
                    interfaceDebugId = thisDebugData[Do.KEY_INTERFACE_DEBUG_ID]


                    # addBy = httpInterface.addBy
                    # if httpInterface.execStatus == ExecStatus.DONE or httpInterface.execStatus == ExecStatus.EXCEPTION:
                    #     debugQueue.remove(debugQueue[0])
                    #     logging.error("ERROR：队列中的接口在数据库中状态是已完成或异常，请检查结果！")
                    #     continue
                    # if addBy in debugThreadDict.keys() and debugThreadDict[addBy].is_alive() :
                    #     stop_thread(debugThreadDict[addBy])
                    # tmpThread = CaseDebugThread(debugType=debugType,httpInterface = httpInterface)
                    # tmpThread.start()
                    tmpProcess = CaseDebugProcess(debugType=debugType,interfaceDebugId=interfaceDebugId)
                    tmpProcess.start()
                    # debugThreadDict[addBy] = tmpThread
                elif debugType == Do.TYPE_DEBUG_CASE:
                    #进行用例调试
                    caseDebugId = thisDebugData[Do.KEY_CASE_DEBUG_ID]
                    caseStepDebugIdList = thisDebugData[Do.KEY_CASE_STEP_DEBUG_ID_LIST]


                    # if httpCase.addBy == None or httpCase.addBy.strip() == "":
                    #     logging.info("没有查到用例调试信息caseDebugId[%s]" % caseDebugId)
                    #     debugQueue.remove(debugQueue[0])
                    #     continue

                    # addBy = httpCase.addBy
                    # if addBy in debugThreadDict.keys() and debugThreadDict[addBy].is_alive() :
                    #     stop_thread(debugThreadDict[addBy])

                    tmpProcess = CaseDebugProcess(debugType=debugType,testCaseDebugId=caseDebugId,testCaseStepDebugId=caseStepDebugIdList)
                    tmpProcess.start()
                    # debugThreadDict[addBy] = tmpThread
                else:
                    #错误的调试类型
                    logging.error("错误的类型！")
                # debugQueue.remove(debugQueue[0])
                logging.info ("thread_process_debug_queue: 调试处理完毕" )
            except Exception as e:
                logging.error("不可知异常：%s" % traceback.format_exc())
                logging.error("当前队列为数量为%s " % debugQueue.qsize())
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
def thread_process_task_queue_SingleEnvToMultiTask(runTaskQueue):
    #TODO 单环境可同时执行多任务
    while True:
        taskStartIndex = 0
        while len(taskQueue) > taskStartIndex :
            if Do.KEY_TASK_OBJECT in taskQueue[taskStartIndex].keys():
                #存在对象,之前查询过了
                taskObject = taskQueue[taskStartIndex][Do.KEY_TASK_OBJECT]
                taskExecId = taskObject.taskExecuteId
            else:
                #第一次进入,没有TaskObject生成,从数据库查询并生成赋值到dict中
                taskObject = Task()
                taskExecId = taskQueue[taskStartIndex][Do.KEY_TASK_EXECUTE_ID]
                taskObject.taskExecuteId = taskExecId
                #这里是设置task执行的地方 ~！！！！
                taskObject.generateByTaskExecuteId()
                if taskObject.taskId == None or taskObject.taskId.strip() =="":
                    logging.info("thread_process_task_queue: 没有查到任务执行信息taskExecId[%s]。" % taskExecId)
                    # if lock.acquire():
                    taskQueue.remove(taskQueue[taskStartIndex])
                    # lock.release()
                    continue
                else:
                    #将查询到的任务执行数据保存，下次不必查询。
                    # if lock.acquire():
                    taskQueue[taskStartIndex][Do.KEY_TASK_OBJECT] = taskObject
                    # lock.release()
            # serviceConfKey = taskObject.confHttpLayer.confServiceLayer.key
            serviceConfKey = taskObject.confHttpLayer.key
            #通过执行查询结果找到confServiceKey作为多线程的主键,如果存在且alive阻塞,开始执行下一个
            if serviceConfKey == None or serviceConfKey.strip() == "":
                logging.error("thread_process_task_queue: 任务执行获取不到执行环境，请检查错误。")
                # if lock.acquire():
                taskQueue.remove(taskQueue[taskStartIndex])
                # lock.release()
                break

            taskId = taskObject.taskId #之前已经检测过taskId，不需要重复检测
            try:
                # mutex.acquire()
                #看当前http环境是否已经有数据，没有数据就初始化。
                # if serviceConfKey  not in serviceThreadDict.keys():
                #     serviceThreadDict[serviceConfKey] = {}
                #     serviceThreadDict[serviceConfKey]['AliveThreadCount'] = 0
                #
                # #根据thread状态生成当前Alive数量
                # serviceThreadDict["AliveThreadCount"] = 0
                # for tmpEnvKey in list(serviceThreadDict.keys()):
                #     if tmpEnvKey  != "AliveThreadCount":
                #         serviceThreadDict[tmpEnvKey]['AliveThreadCount'] = 0
                #         for tmpTaskKey in list(serviceThreadDict[tmpEnvKey].keys()):
                #             if tmpTaskKey != "AliveThreadCount":
                #                 if serviceThreadDict[tmpEnvKey][tmpTaskKey]['thread'].isAlive():
                #                     #如果线程或者计入统计
                #                     serviceThreadDict["AliveThreadCount"] += 1 #总共的加1
                #                     serviceThreadDict[tmpEnvKey]['AliveThreadCount'] += 1 #当前环境的加1
                #                 else:
                #                     #如果线程死了，从字典中删除，已经是无效的了
                #                     serviceThreadDict[tmpEnvKey].pop(tmpTaskKey)
                # if serviceConfKey not in serviceThreadDict.keys():
                #     serviceProgressDict[serviceConfKey] = {"AliveProgressCount": 0}

                serviceProgressDict["AliveProgressCount"] = 0
                for tmpEnvKey in list(serviceProgressDict.keys()):
                    if tmpEnvKey != "AliveProgressCount":
                        serviceProgressDict[tmpEnvKey]["AliveProgressCount"] = 0

                        for tmpTaskKey in list(serviceProgressDict[tmpEnvKey].keys()):
                            if tmpEnvKey != "AliveProgressCount":
                                if serviceProgressDict[tmpEnvKey][tmpTaskKey]["progress"].isAlive():
                                    serviceProgressDict["AliveProgressCount"] += 1
                                    serviceProgressDict[tmpTaskKey]["AliveProgressCount"] += 1
                                else:
                                    serviceProgressDict[tmpEnvKey].pop(tmpTaskKey)

                # # 判断线程数是否超过配置，减去AliveThread后，判断是否超过配置要求。
                # if serviceThreadDict['AliveThreadCount'] >= maxRuntaskThreadNums:
                #     # 如果所执行任务总线程超过了，退出当前循环，休息1秒，从头开始便利
                #     break
                # # 先判断当前环境下任务是否已经足额，足额不执行，继续便利下一个，不足额，执行
                # if serviceThreadDict[serviceConfKey]['AliveThreadCount'] >= maxTaskNumsInSingleEnv:
                #     # 如果当前环境的任务执行总数到了，继续便利下一个，不退出当前循环。
                #     taskStartIndex += 1
                #     continue

                #任务id如果不在当前环境下，不需要排队，并且如果任务已经结束，那么进入执行
                # if taskId not in serviceThreadDict[serviceConfKey].keys() or (serviceThreadDict[serviceConfKey][taskId]['thread'].isAlive() == False):
                #没有超过配置要求，启动线程测试，并且相关配置+1并记录。
                # tmpThread = TaskThread(task=taskQueue[taskStartIndex][Do.KEY_TASK_OBJECT])
                # tmpThread.start()
                # # if lock.acquire():
                # taskQueue.remove(taskQueue[taskStartIndex])

                # tmpProgress =

                tcpStr = '{"do":%s,"TaskExecuteId":%s}' % (Do.TYPE_TASK_INIT_DONE,taskObject.taskExecuteId)
                if not sendTcp(TcpServerConf.ip, TcpServerConf.port, tcpStr):
                    logging.error("任务初始化完毕 TCP回调函数发生异常！ %s " % tcpStr)

                # lock.release()
                serviceThreadDict[serviceConfKey][taskId] = {}
                # serviceThreadDict[serviceConfKey][taskId]['thread'] = tmpThread
                serviceThreadDict[serviceConfKey][taskId]['taskExecuteId'] = taskExecId
                logging.info("thread_process_task_queue: 任务%s处理完毕" % taskExecId)
                break
                # else:
                #     #有进程且活着不执行当前任务,执行下一个
                #     taskStartIndex += 1
                #     continue
            except Exception as e:
                logging.error(traceback.format_exc())
            finally:
                pass
                # mutex.release()
        #如果退出第一遍遍历，并启动完线程，需要休眠1s
        time.sleep(1)

@catch_exception
@take_time
def thread_process_task_cancel_SingleEnvToMultiTask():
    #TODO 单环境可同时执行多任务 取消任务
    while True:
        if len(taskCancelQueue) > 0 :
            logging.info("thread_process_task_cancel: taskCancelQueue:%s" % taskCancelQueue)
            taskType = taskCancelQueue[0][Do.KEY_DO]
            taskExecuteId = taskCancelQueue[0][Do.KEY_TASK_EXECUTE_ID]
            logging.info("thread_process_task_cancel: 开始处理任务取消：%s" % taskCancelQueue[0])
            if taskType == Do.TYPE_TASK_CANCEL:
                #进行接口调试
                tmpTask = Task()
                tmpTask.taskExecuteId = taskExecuteId
                tmpTask.generateByTaskExecuteId()
                # 处理已经存在的线程
                # serviceConfKey = tmpTask.confHttpLayer.confServiceLayer.key
                serviceConfKey = tmpTask.confHttpLayer.key
                try:
                    # mutex.acquire()
                    if serviceConfKey in serviceThreadDict.keys():
                        if tmpTask.taskId in serviceThreadDict[serviceConfKey].keys():
                            taskDict = serviceThreadDict[serviceConfKey][tmpTask.taskId]
                            tmpThread = serviceThreadDict[serviceConfKey][tmpTask.taskId]['thread']
                            if int(taskDict['taskExecuteId']) == int(taskExecuteId) and tmpThread.is_alive():
                                # 执行线程结束操作
                                stop_thread(tmpThread)
                                logging.debug("thread_process_task_cancel: 结束任务执行线程【%s】" % taskExecuteId)
                except Exception as e:
                    logging.error(traceback.format_exc())
                finally:
                    pass
                    # mutex.release()

                logging.debug("thread_process_task_cancel: 任务%s开始取消！" % taskExecuteId)
                res = tmpTask.cancelTask()
                logging.debug("thread_process_task_cancel: 任务取消返回结果：%s" % str(res))
                if res:
                    #取消成功
                    logging.info("thread_process_task_cancel: 任务执行ID[%s]取消成功！" % taskExecuteId)

                else:
                    logging.error("thread_process_task_cancel: 任务执行ID[%s]取消失败，请检查错误！" % taskExecuteId)
            else:
                #错误的调试类型
                logging.error("thread_process_task_cancel: 错误的类型！")
            # if lock.acquire():
            taskCancelQueue.remove(taskCancelQueue[0])
            # lock.release()

            for i in range(0,len(taskQueue)):
                if taskQueue[i][Do.KEY_TASK_EXECUTE_ID] == taskExecuteId:
                    # if lock.acquire():
                    taskQueue.remove(taskQueue[i])
                    # lock.release()
                    break

            logging.info ("thread_process_task_cancel: 任务%s取消完毕" % taskExecuteId )
        else:
            time.sleep(1)
