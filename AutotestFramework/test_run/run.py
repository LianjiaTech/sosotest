import os
import sys,io

import multiprocessing
from optparse import OptionParser
rootpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\","/")
syspath=sys.path
sys.path=[]
sys.path.append(rootpath) #指定搜索路径绝对目录
sys.path.extend([rootpath+i for i in os.listdir(rootpath) if i[0]!="."])#将工程目录下的一级目录添加到python搜索路径中
sys.path.extend(syspath)

from runfunc.listenserver import *
from core.config.InitConfig import *
from core.const.Protocol import *


if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("--ip",type="string",help="指定此服务使用的IP地址")
    parser.add_option("--port",type="int",help="指定此服务使用的端口")
    parser.add_option("--protocol",type="string",help="指定此服务可使用的协议")
    (options,args) = parser.parse_args()
    runServerIp = ""
    runServerPort = 0
    protocol = []
    if not options.ip :
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        runServerIp = s.getsockname()[0]
        s.close()
    else:
        runServerIp = options.ip
    if not options.port:
        runServerPort = 9898
    else:
        runServerPort = options.port

    if not options.protocol:
        protocol = [Protocol.HTTP_PROTOCOL,Protocol.DUBBO_PROTOCOL]
    else:
        protocol = options.protocol.split(",")
        for index in protocol:
            if index == Protocol.HTTP_PROTOCOL or index == Protocol.DUBBO_PROTOCOL:
                pass
            else:
                print("协议错误,目前支持的协议为HTTP、DUBBO 收到的protocol参数为%s " % protocol)
                exit()
    #初始化logger
    try:
        manager = multiprocessing.Manager()
        runTaskQueueList = manager.list()
        runTaskCancelQueueList = manager.list()
        debugQueueList = manager.list()

        #dubbo使用的队列
        runTaskDubboQueueList = manager.list()
        runTaskDubboCancelQueueList = manager.list()
        debugDubboQueueList = manager.list()

        #记录本机执行任务
        serviceProgressDict = {}

        #记录本机执行DUBBO任务
        serviceDubboProgressDict = {}

        #记录本机配置信息，用于数据上报
        serverDataDict = manager.dict()
        serverDataDict[Do.KEY_RUN_SERVICE_IP] = runServerIp
        serverDataDict[Do.KEY_RUN_SERVICE_PORT] = runServerPort
        serverDataDict[Do.KEY_RUN_SERVICE_PROTOCOL] = protocol
        serverDataDict[Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM] = 1
        serverDataDict[Do.KEY_RUN_SERVICE_CURRENT_TASK_PROGRESS_NUM] = 0
        serverDataDict[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST] = []
        serverDataDict[Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM] = 1
        serverDataDict[Do.KEY_RUN_SERVICE_CURRENT_CASE_PROGRESS_NUM] = 0
        serverDataDict[Do.KEY_RUN_SERVICE_CURRENT_CASE_LIST] = []

        init_logging(logFilePath=LogConfig.FILE,level= LogConfig.LEVEL ) #LogConfig.LEVEL
        logging.info("=========================开始启动任务队列=========================")
        if Protocol.HTTP_PROTOCOL in protocol:
            process_task_queue = multiprocessing.Process(target=process_task_queue_SingleEnvToMultiTask, args=(runTaskQueueList,runTaskCancelQueueList,serviceProgressDict,serverDataDict))
            process_task_queue.start()
            logging.info("run.py_main: 任务执行启动完成！")

            #用例调试启动完成
            process_debug_queue = multiprocessing.Process(target=progress_process_debug_queue, args=(debugQueueList,))
            process_debug_queue.start()

        ###############################################DUBBO####################################################
        if Protocol.DUBBO_PROTOCOL in protocol:
            process_dubbo_debug_queue = multiprocessing.Process(target=progress_process_dubbo_debug_queue, args=(debugDubboQueueList,))
            process_dubbo_debug_queue.start()

            progress_dubbo_task = multiprocessing.Process(target=progress_process_dubbo_task,args=(runTaskDubboQueueList,runTaskDubboCancelQueueList,serviceDubboProgressDict,serverDataDict))
            progress_dubbo_task.start()


        # 开启监听
        startServer = multiprocessing.Process(target=startServer, args=(runServerIp, runServerPort, TcpServerConf.maxRequestCount, TcpServerConf.recvLength, runTaskQueueList,
        runTaskCancelQueueList, serverDataDict, debugQueueList,debugDubboQueueList,runTaskDubboQueueList,runTaskDubboCancelQueueList))
        startServer.start()
        logging.info("run.py_main: 实时监听启动完成！ip:%s  port:%s" % (runServerIp,runServerPort))

        process_runServerHeartBeat = multiprocessing.Process(target=runServerHeartBeat,args=(runServerIp, runServerPort,protocol))
        process_runServerHeartBeat.start()

        # 上报服务重启
        run_server_restart(serverDataDict)

        startServer.join()
        process_runServerHeartBeat.join()
    except Exception as e:
        logging.error("run.py_main:主进程发现异常！异常信息为：%s" % traceback.format_exc())
