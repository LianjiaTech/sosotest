from runfunc.ui_initial import *
lock = threading.RLock() #线程锁

def thread_process_ui_task_queue():
    global executingUITaskThreadNum,maxUITaskThreadNums,maxWebThreadNums,maxAndroidThreadNums,maxAndroidThreadNums,executingAndroidThreadNum,executingIosThreadNum,executingWebThreadNum
    while True:
        taskStartIndex = 0
        while len(uiTaskQueue) > taskStartIndex :
            logging.info("thread_process_ui_task_queue: Processed_uiTaskQueue:%s" % uiTaskQueue)
            logging.info("thread_process_ui_task_queue: 开始处理任务：%s" % uiTaskQueue[taskStartIndex])
            if Do.KEY_UI_TEST_TASK_OBJECT in uiTaskQueue[taskStartIndex].keys():
                #存在对象,之前查询过了
                taskObject = uiTaskQueue[taskStartIndex][Do.KEY_UI_TEST_TASK_OBJECT]
                taskExecId = taskObject.taskExecuteId
            else:
                #第一次进入,没有UITestTaskObject生成,从数据库查询并生成赋值到dict中
                taskObject = UITestTask()
                taskExecId = int(uiTaskQueue[taskStartIndex][Do.KEY_UITASK_EXEC_ID])
                taskObject.taskExecuteId = taskExecId
                taskObject.generateByTaskExecuteId()
                if taskObject.taskExecuteId <= 0 :
                    logging.info("thread_process_task_queue: 没有查到任务执行信息taskExecId[%s]。" % taskExecId)
                    # if lock.acquire():
                    uiTaskQueue.remove(uiTaskQueue[taskStartIndex])
                    # lock.release()
                    continue
                else:
                    #将查询到的任务执行数据保存，下次不必查询。
                    # if lock.acquire():
                    uiTaskQueue[taskStartIndex][Do.KEY_UI_TEST_TASK_OBJECT] = taskObject
                    # lock.release()

            try:
                # 根据executintUITaskThreadDict的thread状态生成当前Alive数量
                executingUITaskThreadNum = 0
                executingIosThreadNum = 0
                executingWebThreadNum = 0
                executingAndroidThreadNum = 0

                keyList = deepcopy(list(executintUITaskThreadDict.keys()))
                for tmpExecutingTaskExecId in keyList:
                    tmpThread = executintUITaskThreadDict[tmpExecutingTaskExecId]
                    if tmpThread.is_alive():
                        executingUITaskThreadNum += 1
                    else:
                        executintUITaskThreadDict.pop(tmpExecutingTaskExecId)

                #   web线程数量
                webKeyList = deepcopy(list(executintWebThreadDict.keys()))
                for tmpExecutingWebExecId in webKeyList:
                    tmpWebThread = executintWebThreadDict[tmpExecutingWebExecId]
                    if tmpWebThread.is_alive():
                        executingWebThreadNum += 1

                #Android线程数量
                androidKeyList = deepcopy(list(executintAndroidThreadDict.keys()))
                for tmpExecutingAndroidExecId in androidKeyList:
                    tmpAndroidThread = executintAndroidThreadDict[tmpExecutingAndroidExecId]
                    if tmpAndroidThread.is_alive():
                        executingAndroidThreadNum += 1

                #ios线程数量
                iosKeyList = deepcopy(list(executintIosThreadDict))
                for tmpExecutingIosExecId in iosKeyList:
                    tmpIosThread = executintIosThreadDict[tmpExecutingIosExecId]
                    if tmpIosThread.is_alive():
                        executingIosThreadNum += 1
                logging.info("现在一共起了%s 个线程" % executingUITaskThreadNum)
                logging.info("ios线程数量为 %s" % executingIosThreadNum)
                logging.info("Android线程数量为 %s" % executingAndroidThreadNum)
                logging.info("web线程数量为 %s" % executingWebThreadNum)

                if executingUITaskThreadNum < maxUITaskThreadNums:
                    #如果是web端
                    if uiTaskQueue[taskStartIndex][Do.KEY_UI_TEST_TASK_OBJECT].sourceGroup == webTypeKey:
                        if executingWebThreadNum >= maxWebThreadNums:
                            taskStartIndex += 1
                            continue
                    if uiTaskQueue[taskStartIndex][Do.KEY_UI_TEST_TASK_OBJECT].sourceGroup == androidTypeKey:
                        if executingAndroidThreadNum >= maxAndroidThreadNums:
                            taskStartIndex += 1
                            continue
                    if uiTaskQueue[taskStartIndex][Do.KEY_UI_TEST_TASK_OBJECT].sourceGroup == iosTypeKey:
                        if executingIosThreadNum >= maxIosThreadNums:
                            taskStartIndex += 1
                            continue

                    #如果没有达到最大上限，开始执行
                    tmpThread = UITaskThread(task=uiTaskQueue[taskStartIndex][Do.KEY_UI_TEST_TASK_OBJECT])
                    tmpThread.start()
                    executintUITaskThreadDict[str(taskObject.taskExecuteId)] = tmpThread

                    # 如果是web端
                    if uiTaskQueue[taskStartIndex][Do.KEY_UI_TEST_TASK_OBJECT].sourceGroup == webTypeKey:
                        executintWebThreadDict[str(taskObject.taskExecuteId)] = tmpThread
                    if uiTaskQueue[taskStartIndex][Do.KEY_UI_TEST_TASK_OBJECT].sourceGroup == androidTypeKey:
                        executintAndroidThreadDict[str(taskObject.taskExecuteId)] = tmpThread
                    if uiTaskQueue[taskStartIndex][Do.KEY_UI_TEST_TASK_OBJECT].sourceGroup == iosTypeKey:
                        executintIosThreadDict[str(taskObject.taskExecuteId)] = tmpThread

                    uiTaskQueue.remove(uiTaskQueue[taskStartIndex]) #已经处理的任务从uiTaskQueue中删除
                    lock.acquire()
                    executingUITaskThreadNum += 1
                    lock.release()
                    break
                else:
                    #达到执行上限了，资源不足不继续执行，排队等待,执行下一个
                    taskStartIndex += 1
            except Exception as e:
                logging.error(traceback.format_exc())
            finally:
                pass
                # mutex.release()
        #如果退出第一遍遍历，并启动完线程，需要休眠1s
        time.sleep(1)


def thread_process_ui_task_cancel_queue():
    while True:
        if len(uiTaskCancelQueue) > 0 :
            logging.info("thread_process_ui_task_cancel_queue: taskCancelQueue:%s" % uiTaskCancelQueue)
            taskType = uiTaskCancelQueue[0][Do.KEY_DO]
            taskExecuteId = int(uiTaskCancelQueue[0][Do.KEY_UITASK_EXEC_ID])
            logging.info("thread_process_ui_task_cancel_queue: 开始处理UI任务取消：%s" % uiTaskCancelQueue[0])
            if taskType == Do.TYPE_UITASK_CANCEL:
                #进行接口调试
                # 处理已经存在的线程
                try:
                    if str(taskExecuteId) in executintUITaskThreadDict.keys():
                        tmpThread = executintUITaskThreadDict[str(taskExecuteId)]
                        if tmpThread.is_alive():
                            # 执行线程结束操作
                            logging.debug("thread_process_ui_task_cancel_queue: 结束任务执行线程开始【%s】" % taskExecuteId)
                            stop_thread(tmpThread)
                            logging.debug("thread_process_ui_task_cancel_queue: 结束任务执行线程结束【%s】" % taskExecuteId)
                except Exception as e:
                    logging.error(traceback.format_exc())
                finally:
                    pass
                    # mutex.release()

                logging.debug("thread_process_ui_task_cancel_queue: 任务%s开始取消！" % taskExecuteId)
                tmpTask = UITestTask()
                tmpTask.taskExecuteId = taskExecuteId
                tmpTask.generateByTaskExecuteId()
                tmpTask.resetAppiumServer()
                res = tmpTask.cancelTask()
                logging.debug("thread_process_ui_task_cancel_queue: 任务取消返回结果：%s" % str(res))
                if res:
                    #取消成功
                    logging.info("thread_process_ui_task_cancel_queue: 任务执行ID[%s]取消成功！" % taskExecuteId)
                else:
                    logging.error("thread_process_ui_task_cancel_queue: 任务执行ID[%s]取消失败，请检查错误！" % taskExecuteId)
            else:
                #错误的调试类型
                logging.error("thread_process_ui_task_cancel_queue: 错误的类型！")

            # if lock.acquire():
            uiTaskCancelQueue.remove(uiTaskCancelQueue[0]) #从取消列表中删除数据
            # lock.release()

            for i in range(0,len(uiTaskQueue)):
                if int(uiTaskQueue[i][Do.KEY_UITASK_EXEC_ID]) == int(taskExecuteId):
                    # if lock.acquire():
                    uiTaskQueue.remove(uiTaskQueue[i])
                    # lock.release()
                    break

            logging.info ("thread_process_ui_task_cancel_queue: UI测试任务%s取消完毕" % taskExecuteId )
        else:
            time.sleep(1)
