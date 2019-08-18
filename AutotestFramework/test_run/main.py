import os
import sys,io

import threading,multiprocessing
rootpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\","/")
syspath=sys.path
sys.path=[]
sys.path.append(rootpath) #指定搜索路径绝对目录
sys.path.extend([rootpath+i for i in os.listdir(rootpath) if i[0]!="."])#将工程目录下的一级目录添加到python搜索路径中
sys.path.extend(syspath)

from runfunc.listenserver import *
from core.config.InitConfig import LogConfig
from progress.globalValFunc import *
from progress.progressTarget import *

if __name__ == '__main__':
    #初始化logger
    try:
        manager = multiprocessing.Manager()

        serviceList = manager.list()
        #HTTP协议相关
        taskQueueList = manager.list()
        taskCancelQueueList = manager.list()
        debugQueueList = manager.list()
        taskSuiteList = manager.list()
        taskStatusList = manager.list()  #存储任务状态变更的数组
        debugStatusList = manager.list() #存储调试状态变更的数组
        serviceStatusList = manager.list() #存储对接多服务状态变更的数组
        heartBeatList = manager.list() #服务心跳

        # serviceListQueueLock = multiprocessing.Lock()
        # taskQueueLock = multiprocessing.Lock()
        # taskCancelQueueLock = multiprocessing.Lock()

        init_logging(logFilePath=LogConfig.MainFILE,level= LogConfig.LEVEL ) #LogConfig.LEVEL
        logging.info("=========================开始启动任务队列=========================")
        #开启ftp
        multiprocessing.Process(target=ftpServer,args=()).start()
        logging.info("main.py :ftp服务启动完成！")
        #从数据库中初始化队列
        init_global_queue(taskQueueList,taskCancelQueueList)

        # 开启监听 TODO 有时候会绑定端口失败
        startMainServer = multiprocessing.Process(target=startMainServer, args=(taskQueueList, serviceList,taskStatusList,debugStatusList,serviceStatusList,heartBeatList))
        startMainServer.start()

        #启动时等待10S 所有slave上报后 更新master本地信息
        time.sleep(10)

        #开启自动分配调试进程
        process_allocating_debug = multiprocessing.Process(target=progress_allocating_debug,args=(debugQueueList,serviceList))
        process_allocating_debug.start()

        # #开启自动分配任务进程
        process_allocating_task = multiprocessing.Process(target=process_allocating_task, args=(taskQueueList,taskCancelQueueList,serviceList))
        process_allocating_task.start()
        # logging.info("run.py_main: 任务分配启动完成！%s" % taskQueueList)
        #
        # #开启自动分配任务取消的进程
        process_allocating_task_cancel = multiprocessing.Process(target=process_allocating_task_cancel,args=(taskQueueList,taskCancelQueueList,serviceList))
        process_allocating_task_cancel.start()
        # logging.info("run.py_main: 任务取消分配启动完成！")

        #开启任务执行过程监听
        Process_task_status = multiprocessing.Process(target=taskStetusProregss,args=(taskStatusList,taskQueueList,taskCancelQueueList,serviceList))
        Process_task_status.start()

        #开启调试执行过程监听
        Progress_debug_status = multiprocessing.Process(target=debugStatusProgress,args=(debugStatusList,debugQueueList,serviceList))
        Progress_debug_status.start()

        #开启服务监听模式
        Progress_service_status = multiprocessing.Process(target=serviceStatusProgress,args=(serviceStatusList,taskQueueList,serviceList))
        Progress_service_status.start()

        #处理多服务心跳信息
        Progress_service_heart_beat = multiprocessing.Process(target=serviceHeartBeat,args=(heartBeatList,serviceList))
        Progress_service_heart_beat.start()

        #判断服务是否离线
        mainServerHeartBeat = multiprocessing.Process(target=mainServerHeartBeat, args=(serviceList,taskQueueList))
        mainServerHeartBeat.start()
        # logging.info("心跳检测服务启动完成!")


        startMainServer.join()
        process_allocating_task.join()
        process_allocating_debug.join()
        mainServerHeartBeat.join()
        # process_allocating_task_cancel.join()
        # process_debug_queue.join()
        logging.info("=========================所有任务执行完毕=========================")
    except Exception as e:
        print("main.py_main:主进程发现异常！异常信息为：%s" % traceback.format_exc())
        logging.error("run.py_main:主进程发现异常！异常信息为：%s" % traceback.format_exc())
