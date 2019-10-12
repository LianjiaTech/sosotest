from runfunc.runProcess import *
from runfunc.mainProcess import *
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from threads.mainTCPThreads import *

@catch_exception
@take_time
def startServer(ip,port,maxRequestCount,recvLength,runTaskQueueList,runTaskCancelQueueList,serverDataDict,debugQueueList,debugDubboQueueList,runTaskDubboQueueList,runTaskDubboCancelQueueList):
    #DONE 启动server监听新消息
    retryTime = 0
    while True:
        #========TCP=====================
        try:
            # 开启ip和端口
            ip_port = (ip,port)
            # 生成句柄
            socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socketServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 就是它，在bind前加
            socket.setdefaulttimeout(timeConf.socketDefaultTime)

            # 绑定端口
            socketServer.bind(ip_port)
            # 最多连接数
            socketServer.listen(TcpServerConf.maxRequestCount)
        except Exception as e:
            logging.error(traceback.format_exc())
            os._exit(0)
            if retryTime > 10:
                os._exit(0)
            else:
                retryTime += 1
                time.sleep(3)
                continue
        # 等待信息
        retryTime = 0
        # 开启死循环监听队列
        while True:
            try:
                logging.debug("****************************************监听中...****************************************")
                # 阻塞
                conn, addr = socketServer.accept()
                # 获取客户端请求数据
                data = conn.recv(recvLength)
                # 打印接受数据 注：当浏览器访问的时候，接受的数据的浏览器的信息等。
                dataString = data.decode("utf8")
                if isJson(dataString):
                    dataDict = json.loads(dataString)
                    # print(dataDict)
                    logging.debug("startServer: 请求数据：%s" % dataDict)
                    logging.debug("startServer: 请求者地址信息：%s" % str(addr))
                    if Do.KEY_DO not in dataDict.keys():
                        conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_DO, 'utf8'))

                    elif dataDict[Do.KEY_DO] == Do.TYPE_DEBUG_INTERFACE:
                        if Do.KEY_INTERFACE_DEBUG_ID not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_INTERFACE_DEBUG_ID, 'utf8'))
                        elif Do.TYPE_PROTOCOL not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.TYPE_PROTOCOL, 'utf8'))
                        else:

                            # if isInt(dataDict[Do.KEY_INTERFACE_DEBUG_ID]) == False:
                            #     conn.send(bytes('ERROR:字段[%s]必须是整数类型！' % Do.KEY_INTERFACE_DEBUG_ID, 'utf8'))
                            #     logging.debug('startServer: ERROR:字段[%s]必须是整数类型！' % Do.KEY_INTERFACE_DEBUG_ID)
                            #     continue
                            if dataDict[Do.TYPE_PROTOCOL] == Protocol.HTTP_PROTOCOL:
                                debugQueueList.append(dataDict)
                            elif dataDict[Do.TYPE_PROTOCOL] == Protocol.DUBBO_PROTOCOL:
                                debugDubboQueueList.append(dataDict)
                            else:
                                conn.send(bytes('ERROR:协议暂不支持[%s]！' % dataDict[Do.TYPE_PROTOCOL], 'utf8'))
                                continue
                            logging.debug("startServer: 调试接口加入debugQueue！")
                            conn.send(bytes('ok', 'utf8'))
                            continue

                    elif dataDict[Do.KEY_DO] == Do.TYPE_DEBUG_CASE:

                        if Do.KEY_CASE_DEBUG_ID not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_CASE_DEBUG_ID, 'utf8'))
                            continue

                        elif Do.KEY_CASE_STEP_DEBUG_ID_LIST not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_CASE_STEP_DEBUG_ID_LIST, 'utf8'))
                            continue
                        elif Do.TYPE_PROTOCOL not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.TYPE_PROTOCOL, 'utf8'))
                            continue
                        else:
                            if dataDict[Do.TYPE_PROTOCOL] == Protocol.HTTP_PROTOCOL:
                                debugQueueList.append(dataDict)
                            elif dataDict[Do.TYPE_PROTOCOL] == Protocol.DUBBO_PROTOCOL:
                                debugDubboQueueList.append(dataDict)
                            else:
                                conn.send(bytes('ERROR:协议暂不支持[%s]！' % dataDict[Do.TYPE_PROTOCOL], 'utf8'))
                                continue
                            logging.debug("startServer: 调试用例加入debugQueue！")
                            conn.send(bytes('ok', 'utf8'))

                    elif dataDict[Do.KEY_DO] == Do.TYPE_TASK_EXECUTE:
                        #任务执行
                        if Do.KEY_TASK_EXECUTE_ID not in dataDict.keys():
                            tmpText = "ERROR:缺少必要字段！"
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_TASK_EXECUTE_ID, 'utf8'))
                            continue
                        elif Do.KEY_TASK_EXECUTE_ENV not in dataDict.keys():
                            tmpText = "ERROR:缺少必要字段！"
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_TASK_EXECUTE_ENV, 'utf8'))
                            continue
                        elif Do.KEY_TASK_ID not in dataDict.keys():
                            tmpText = "ERROR:缺少必要字段！"
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_TASK_ID, 'utf8'))
                            continue
                        elif isInt(dataDict[Do.KEY_TASK_EXECUTE_ID]) == False:
                            conn.send(bytes('ERROR:字段[%s]必须是整数类型！' % Do.KEY_TASK_EXECUTE_ID, 'utf8'))
                            logging.debug('startServer: ERROR:字段[%s]必须是整数类型！' % Do.KEY_TASK_EXECUTE_ID)
                            continue
                        else:
                            dataDict["isCluster"] = 0
                            if dataDict[Do.TYPE_PROTOCOL] == Protocol.HTTP_PROTOCOL:
                                runTaskQueueList.append(dataDict)
                            elif dataDict[Do.TYPE_PROTOCOL] == Protocol.DUBBO_PROTOCOL:
                                runTaskDubboQueueList.append(dataDict)
                            else:
                                conn.send(bytes('ERROR:协议暂不支持[%s]！' % dataDict[Do.TYPE_PROTOCOL], 'utf8'))
                                continue
                            logging.debug("startServer: 任务执行加入taskQueue！")
                            logging.debug("startServer: 任务执行加入taskQueue！%s " % dataDict)
                            conn.send(bytes('ok', 'utf8'))
                            continue

                    elif dataDict[Do.KEY_DO] == Do.TYPE_TASK_CANCEL:
                        #任务取消
                        if Do.KEY_TASK_EXECUTE_ID not in dataDict.keys():
                            tmpText = "ERROR:缺少必要字段！"
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_TASK_EXECUTE_ID, 'utf8'))
                            continue
                        if Do.TYPE_PROTOCOL not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.TYPE_PROTOCOL, 'utf8'))
                            continue
                        else:
                            if dataDict[Do.TYPE_PROTOCOL] == Protocol.HTTP_PROTOCOL:
                                runTaskCancelQueueList.append(dataDict)
                            elif dataDict[Do.TYPE_PROTOCOL] == Protocol.DUBBO_PROTOCOL:
                                runTaskDubboCancelQueueList.append(dataDict)
                            else:
                                conn.send(bytes('ERROR:协议暂不支持[%s]！' % dataDict[Do.TYPE_PROTOCOL], 'utf8'))
                                continue
                            logging.debug("startServer: 任务取消加入taskCancelQueue！")
                            conn.send(bytes('ok', 'utf8'))
                            continue
                    elif dataDict[Do.KEY_DO] == Do.TYPE_MASTER_GET_SERVICE_DATA:
                        conn.send(bytes('ok', 'utf8'))
                        tmpDict = {}
                        for index in serverDataDict.keys():
                            tmpDict[index] = serverDataDict[index]
                        tmpDict["do"] = Do.TYPE_RUN_SERVICE_DATA_REPORT
                        tmpDict[Do.KEY_RUN_SERVICE_IP] = ip
                        tmpDict[Do.KEY_RUN_SERVICE_PORT] = port
                        dataReportTcpStr = json.dumps(tmpDict)
                        if sendTcp(TcpServerConf.ip,TcpServerConf.port,dataReportTcpStr):
                            logging.info("发送数据上报成功")
                        else:
                            logging.error("发送数据上报失败")

                    elif dataDict[Do.KEY_DO] == Do.TYPE_MASTER_SET_SERVICE_DATA:
                        # print(1111111111111111)
                        # print(dataDict)
                        if Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM, 'utf8'))
                        elif Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM, 'utf8'))
                        else:
                            serverDataDict[Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM] = dataDict[Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM]
                            serverDataDict[Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM] = dataDict[Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM]
                            conn.send(bytes('ok', 'utf8'))
                    else:
                        logging.debug("startServer: 非法请求！") #每个Service配置有一个线程，多个ServiceConf可并发执行任务。
                        conn.send(bytes('ERROR:非法请求！', 'utf8'))
                else:
                    tmpText = "ERROR:请求的必须是json字符串，请按照协议进行请求。"
                    logging.debug("startServer: %s" % tmpText)
                    # 向对方发送数据
                    conn.send(bytes(tmpText, 'utf8'))
            except Exception as e:
                logging.error("服务监听出现异常：%s" % traceback.format_exc())
                # break
            finally:
                if conn:
                    conn.close()
                logging.debug("**************************************请求处理结束**************************************")

        time.sleep(6)

@catch_exception
@take_time
@set_logging
def startMainServer(taskQueueList,serviceList,taskStatusList,debugStatusList,serviceStatusList,heartBeatList):
    #DONE 启动server监听新消息
    retryTime = 0
    while True:
        #========TCP=====================
        try:
            # 开启ip和端口
            ip_port = (TcpServerConf.ip, TcpServerConf.port)
            # 生成句柄
            socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socketServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 就是它，在bind前加
            socket.setdefaulttimeout(timeConf.socketDefaultTime)

            # socketServer.setblocking(0)
            # 绑定端口
            socketServer.bind(ip_port)
            # 最多连接数
            socketServer.listen(TcpServerConf.maxRequestCount)
        except Exception as e:
            logging.error(traceback.format_exc())
            os._exit(0)
            if retryTime > 10:
                os._exit(0)
            else:
                retryTime += 1
                time.sleep(3)
                continue
        # 等待信息
        retryTime = 0
        # 开启死循环监听队列
        while True:
            try:
                logging.debug("****************************************监听中...****************************************")
                # 阻塞
                conn, addr = socketServer.accept()
                # 获取客户端请求数据
                # data = conn.recv(recvLength)
                data = conn.recv(TcpServerConf.recvLength)
                # 打印接受数据 注：当浏览器访问的时候，接受的数据的浏览器的信息等。
                dataString = data.decode("utf8")
                if isJson(dataString):
                    dataDict = json.loads(dataString)
                    # print("TCPTCPTCPTCPTCPTCP%s" % dataString)
                    # print(dataDict)
                    # print(serviceList)
                    if Do.KEY_DO in dataDict.keys() and dataDict[Do.KEY_DO] != 200:
                        logging.info("startServer: 请求数据：%s" % dataDict)
                    logging.debug("startServer: 请求数据：%s" % dataDict)
                    logging.debug("startServer: 请求者地址信息：%s" % str(addr))
                    if Do.KEY_DO not in dataDict.keys():
                        conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_DO, 'utf8'))
                    elif dataDict[Do.KEY_DO] == Do.TYPE_DEBUG_INTERFACE:
                        if Do.KEY_INTERFACE_DEBUG_ID not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_INTERFACE_DEBUG_ID, 'utf8'))
                        elif Do.TYPE_PROTOCOL not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.TYPE_PROTOCOL, 'utf8'))
                        else:
                            debugStatusList.append(dataDict)
                            # threading.Thread(target=typeDebugInterface,args=(dataDict,debugQueueList)).start()
                            conn.send(bytes('ok', 'utf8'))
                            # logging.debug("startServer: 调试接口加入debugQueue！ %s" % debugQueueList)

                    elif dataDict[Do.KEY_DO] == Do.TYPE_DEBUG_INTERFACE_DONE:
                        debugStatusList.append(dataDict)
                        # threading.Thread(target=typeDebugInterfaceDone,args=(dataDict,serviceList,debugQueueList)).start()
                        conn.send(bytes('ok', 'utf8'))
                    elif dataDict[Do.KEY_DO] == Do.TYPE_DEBUG_CASE:

                        if Do.KEY_CASE_DEBUG_ID not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_CASE_DEBUG_ID, 'utf8'))

                        elif Do.KEY_CASE_STEP_DEBUG_ID_LIST not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_CASE_STEP_DEBUG_ID_LIST, 'utf8'))
                        elif Do.TYPE_PROTOCOL not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.TYPE_PROTOCOL, 'utf8'))
                        else:
                            debugStatusList.append(dataDict)
                            # threading.Thread(target=typeDebugCase,args=(dataDict,debugQueueList)).start()
                            logging.debug("startServer: 调试用例加入debugQueue！")
                            conn.send(bytes('ok', 'utf8'))
                    elif dataDict[Do.KEY_DO] == Do.TYPE_DEBUG_CASE_DONE:
                        debugStatusList.append(dataDict)
                        # threading.Thread(target=typeDebugCaseDone,args=(dataDict,serviceList,debugQueueList)).start()
                        conn.send(bytes('ok', 'utf8'))
                    elif dataDict[Do.KEY_DO] == Do.TYPE_TASK_EXECUTE:
                        #任务执行
                        if Do.KEY_TASK_EXECUTE_ID not in dataDict.keys():
                            tmpText = "ERROR:缺少必要字段！"
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_TASK_EXECUTE_ID, 'utf8'))
                        elif Do.KEY_TASK_EXECUTE_ENV not in dataDict.keys():
                            tmpText = "ERROR:缺少必要字段！"
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_TASK_EXECUTE_ENV, 'utf8'))
                        elif Do.KEY_TASK_ID not in dataDict.keys():
                            tmpText = "ERROR:缺少必要字段！"
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_TASK_ID, 'utf8'))
                        elif Do.TYPE_PROTOCOL not in dataDict.keys():
                            tmpText = "ERROR:缺少必要字段！"
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.TYPE_PROTOCOL, 'utf8'))
                        else:
                            if Do.KEY_TASK_SUITE_EXECUTE_ID not in dataDict.keys():
                                dataDict[Do.KEY_TASK_SUITE_EXECUTE_ID] = 0
                            dataDict[isCluster] = isClusterConf.notRun
                            taskStatusList.append(dataDict)
                            logging.debug("startServer: 任务执行加入taskQueue111！")
                            logging.debug("startServer: 任务执行加入taskQueue222！%s " % taskQueueList)
                            conn.send(bytes('ok', 'utf8'))

                    elif dataDict[Do.KEY_DO] == Do.TYPE_TASK_INIT_DONE:
                        if Do.KEY_TASK_EXECUTE_ID not in dataDict.keys():
                            tmpText = "ERROR:缺少必要字段！"
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_TASK_EXECUTE_ID, 'utf8'))
                        elif not isInt(dataDict[Do.KEY_TASK_EXECUTE_ID]):
                            conn.send(bytes('ERROR:必须是整数类型[%s]！' % Do.KEY_TASK_EXECUTE_ID, 'utf8'))
                        else:
                            taskStatusList.append(dataDict)
                            # threading.Thread(target=typeTaskInitDone,args=(dataDict,taskQueueList)).start()
                            logging.info("TYPE_TASK_INIT_DONE 返回 ")
                            conn.send(bytes('ok', 'utf8'))

                    elif dataDict[Do.KEY_DO] == Do.TYPE_TASK_CANCEL:
                        #任务取消
                        if Do.KEY_TASK_EXECUTE_ID not in dataDict.keys():
                            tmpText = "ERROR:缺少必要字段！"
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_TASK_EXECUTE_ID, 'utf8'))
                        elif not isInt(dataDict[Do.KEY_TASK_EXECUTE_ID]):
                            conn.send(bytes('ERROR:必须是整数类型[%s]！' % Do.KEY_TASK_EXECUTE_ID, 'utf8'))
                        elif  Do.TYPE_PROTOCOL not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.TYPE_PROTOCOL, 'utf8'))
                        else:
                            taskStatusList.append(dataDict)
                            # threading.Thread(target=typeTaskCancel,args=(dataDict,taskQueueList,taskCancelQueueList)).start()
                            conn.send(bytes('ok', 'utf8'))

                    elif dataDict[Do.KEY_DO] == Do.TYPE_TASK_CANCEL_DONE:
                        if Do.KEY_TASK_EXECUTE_ID not in dataDict.keys():
                            tmpText = "ERROR:缺少必要字段！"
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_TASK_EXECUTE_ID, 'utf8'))
                        else:
                            taskStatusList.append(dataDict)
                            # threading.Thread(target=typeTaskCancelDone,args=(dataDict,serviceList,taskQueueList)).start()

                            conn.send(bytes('ok', 'utf8'))

                    elif dataDict[Do.KEY_DO] == Do.TYPE_TASK_EXECUTE_DONE:
                        if Do.KEY_TASK_EXECUTE_ID not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_TASK_EXECUTE_ID, 'utf8'))
                        elif not isInt(dataDict[Do.KEY_TASK_EXECUTE_ID]):
                            conn.send(bytes('ERROR:必须是整数类型[%s]！' % Do.KEY_TASK_EXECUTE_ID, 'utf8'))
                        else:
                            conn.send(bytes('ok', 'utf8'))
                            taskStatusList.append(dataDict)
                            # threading.Thread(target=typeTaskExecuteDone,args=(dataDict,serviceList,taskQueueList)).start()

                    elif dataDict[Do.KEY_DO] == Do.TYPE_RUN_SERVICE_RESTART:
                        #服务端重启，将服务端已经获取的任务状态重置为未执行
                        if Do.KEY_RUN_SERVICE_IP not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_RUN_SERVICE_IP, 'utf8'))
                        elif Do.KEY_RUN_SERVICE_PORT not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_RUN_SERVICE_PORT, 'utf8'))
                        elif dataDict[Do.KEY_RUN_SERVICE_IP] == "127.0.0.1" and dataDict[Do.KEY_RUN_SERVICE_IP] == "0.0.0.0":
                            conn.send(bytes('ERROR:[%s]参数不能为127.0.0.1或0.0.0.0！' % dataDict[Do.KEY_RUN_SERVICE_IP], 'utf8'))
                        else:
                            logging.info("收到执行服务重启的请求，%s" % dataDict)
                            serviceStatusList.append(dataDict)

                            conn.send(bytes('ok', 'utf8'))
                    elif dataDict[Do.KEY_DO] == Do.TYPE_RUN_SERVICE_HEART_BEAT:
                        if Do.KEY_RUN_SERVICE_IP not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_RUN_SERVICE_IP, 'utf8'))
                        elif Do.KEY_RUN_SERVICE_PORT not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_RUN_SERVICE_PORT, 'utf8'))
                        else:
                            heartBeatList.append(dataDict)
                            conn.send(bytes('ok', 'utf8'))
                            # inServiceList = False
                            # for serviceIndex in range(0,len(serviceList)):
                            #     if dataDict[Do.KEY_RUN_SERVICE_IP] == serviceList[serviceIndex][Do.KEY_RUN_SERVICE_IP] and dataDict[Do.KEY_RUN_SERVICE_PORT] == serviceList[serviceIndex][Do.KEY_RUN_SERVICE_PORT]:
                            #         inServiceList = True
                            #         tmpServiceIndex = serviceList[serviceIndex]
                            #         tmpServiceIndex[Do.KEY_RUN_SERVICE_LAST_UPDATE_TIME] = datetime.datetime.now()
                            #         tmpServiceIndex[Do.KEY_RUN_SERVICE_PROTOCOL] = dataDict[Do.KEY_RUN_SERVICE_PROTOCOL]
                            #         serviceList[serviceIndex] = tmpServiceIndex
                            #         break
                            # if not inServiceList:
                            #
                            #     #服务端未发现此service 要求数据上报
                            #     tcpStr = '{"do":%s}' % Do.TYPE_MASTER_GET_SERVICE_DATA
                            #     if sendTcp(dataDict[Do.KEY_RUN_SERVICE_IP],dataDict[Do.KEY_RUN_SERVICE_PORT],tcpStr):
                            #         print("服务端未发现此service 要求数据上报 请求发送成功")
                            #         # logging.info("服务端未发现此service 要求数据上报 请求发送成功2222222")
                            #     else:
                            #         logging.error("服务端未发现此service 要求数据上报 请求发送失败")

                    elif dataDict[Do.KEY_DO] == Do.TYPE_RUN_SERVICE_DATA_REPORT:
                        if Do.KEY_RUN_SERVICE_IP not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_RUN_SERVICE_IP, 'utf8'))
                        elif Do.KEY_RUN_SERVICE_PORT not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_RUN_SERVICE_PORT, 'utf8'))
                        elif Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM, 'utf8'))
                        elif Do.KEY_RUN_SERVICE_CURRENT_TASK_PROGRESS_NUM not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_RUN_SERVICE_CURRENT_TASK_PROGRESS_NUM, 'utf8'))
                        elif Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST, 'utf8'))
                        elif Do.KEY_RUN_SERVICE_CURRENT_CASE_LIST not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_RUN_SERVICE_CURRENT_CASE_LIST, 'utf8'))
                        elif Do.KEY_RUN_SERVICE_PROTOCOL not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_RUN_SERVICE_PROTOCOL, 'utf8'))
                        else:
                            serviceStatusList.append(dataDict)
                            conn.send(bytes('ok', 'utf8'))
                            print("收到服务数据上报 %s" % dataDict)
                            # logging.info("收到服务数据上报 %s" % dataDict)
                            # tmpThread = threading.Thread(target=typeRunServiceDataReport,args=(dataDict,serviceList,taskQueueList))
                            # tmpThread.start()
                            # tmpThread.join()
                            # print("完事了",taskQueueList)
                    elif dataDict[Do.KEY_DO] == Do.TYPE_MASTER_UPDATE_MESSAGE:
                        if Do.KEY_RUN_SERVICE_IP not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_RUN_SERVICE_IP, 'utf8'))
                        elif Do.KEY_RUN_SERVICE_PORT not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_RUN_SERVICE_PORT, 'utf8'))
                        elif Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_RUN_SERVICE_MAX_TASK_PROGRESS_NUM, 'utf8'))
                        elif Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_RUN_SERVICE_MAX_CASE_PROGRESS_NUM, 'utf8'))
                        else:
                            serviceStatusList.append(dataDict)
                            conn.send(bytes('ok', 'utf8'))
                    elif dataDict[Do.KEY_DO] == Do.TYPE_WEB_GET_SERVICE_LIST:
                        tmpServiceList = []
                        for index in serviceList:
                            tmpServiceList.append(index)
                        redisTool = RedisTool()
                        redisTool.initRedisConf()
                        redisTool.set_data("RUN_SERVICE_LIST",json.dumps(tmpServiceList,cls=DateEncoder))
                        conn.send(bytes('ok', 'utf8'))
                    elif dataDict[Do.KEY_DO] == Do.TYPE_WEB_GET_SERVICE_TASK_LIST:
                        redisTool = RedisTool()
                        redisTool.initRedisConf()
                        tmpStatusList = []
                        for index in taskQueueList:
                            tmpStatusList.append(index)
                        redisTool.set_data("TASK_STATUS_LIST", json.dumps(tmpStatusList, cls=DateEncoder))
                        conn.send(bytes('ok', 'utf8'))
                    elif dataDict[Do.KEY_DO] == Do.TYPE_WEB_DELETE_SERVICE_INDEX:
                        if Do.KEY_TASK_EXECUTE_ID not in dataDict.keys():
                            conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_TASK_EXECUTE_ID, 'utf8'))

                        taskStatusList.append(dataDict)
                        conn.send(bytes('ok', 'utf8'))
                    else:
                        logging.debug("startServer: 非法请求！") #每个Service配置有一个线程，多个ServiceConf可并发执行任务。
                        conn.send(bytes('ERROR:非法请求！', 'utf8'))
                else:
                    tmpText = "ERROR:请求的必须是json字符串，请按照协议进行请求。"
                    logging.debug("startServer: %s" % tmpText)
                    # 向对方发送数据
                    conn.send(bytes(tmpText, 'utf8'))
            except Exception as e:
                logging.error("服务监听出现异常：%s" % traceback.format_exc())
                # break #出现异常，继续处理下一个请求，不重新监听端口。
            finally:
                if conn:
                    conn.close()
                logging.debug("**************************************请求处理结束**************************************")

        time.sleep(6)

@catch_exception
@take_time
def ftpServer():
    # 实例化用户授权管理
    authorizer = DummyAuthorizer()
    authorizer.add_user('getUploadFile', 'getUploadFile',"%s/uploads" % LogConfig.dirfilePath, perm='elradfmwMT')  # 添加用户 参数:username,password,允许的路径,权限
    authorizer.add_user('setAPITaskReports', 'setAPITaskReports',"%s/reports" % LogConfig.dirfilePath, perm='elradfmwMT')  # 添加用户 参数:username,password,允许的路径,权限
    # authorizer.add_anonymous("%s/AutotestWebD/reports" % rootDir, perm='elradfmwMT')  # 这里是允许匿名用户,如果不允许删掉此行即可

    # 实例化FTPHandler
    handler = FTPHandler
    handler.authorizer = authorizer

    # 设定一个客户端链接时的标语
    handler.banner = "pyftpdlib based ftpd ready."

    # handler.masquerade_address = '151.25.42.11'#指定伪装ip地址
    # handler.passive_ports = range(60000, 65535)#指定允许的端口范围

    address = (TcpServerConf.ip, TcpServerConf.ftpport)  # FTP一般使用21,20端口
    server = FTPServer(address, handler)  # FTP服务器实例

    # set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 5

    # 开启服务器
    server.serve_forever(handle_exit=False)



@catch_exception
@take_time
def runServerHeartBeat(ip,port,protocol):
    while True:
        time.sleep(timeConf.runServerHeartBeat)
        tcpDict = {}
        tcpDict[Do.KEY_DO] = Do.TYPE_RUN_SERVICE_HEART_BEAT
        tcpDict[Do.KEY_RUN_SERVICE_IP] = ip
        tcpDict[Do.KEY_RUN_SERVICE_PORT] = port
        tcpDict[Do.KEY_RUN_SERVICE_PROTOCOL] = protocol
        tcpStr = json.dumps(tcpDict)

        if sendTcp(TcpServerConf.ip, TcpServerConf.port, tcpStr):
            #print("心跳发送成功心跳发送成功心跳发送成功心跳发送成功")
            # logging.info("%s:%s 心跳发送成功")
            # print("%s:%s 心跳发送成功" )
            pass
        else:
            logging.error("%s:%s 心跳发送失败")



@catch_exception
@take_time
def mainServerHeartBeat(serviceList,taskQueueList):
    while True:
        nowTime = datetime.datetime.now()
        for serviceIndex in range(0,len(serviceList)):
            if len(serviceList) > serviceIndex:
                tmpService = serviceList[serviceIndex]
                if (nowTime - tmpService[Do.KEY_RUN_SERVICE_LAST_UPDATE_TIME]).seconds > timeConf.mainServerHeartBeat:
                    # tmpService[Do.KEY_RUN_SERVICE_STATE] = Do.TYPE_SERVICE_OFFLINE
                    # serviceList[serviceIndex] = tmpService
                    serviceList.remove(tmpService)
                    print("服务离线服务离线服务离线服务离线服务离线%s" % tmpService)
                    #有服务离线 将此服务执行中的任务设为未执行
                    taskQueueIndex = 0
                    while taskQueueIndex < len(taskQueueList):
                    # for taskQueueIndex in range(0,len(taskQueueList)):
                    #     try:
                        tmpTaskQueue = taskQueueList[taskQueueIndex]
                        # except Exception:
                        #     break
                        if "%s_%s" % (tmpTaskQueue[Do.TYPE_PROTOCOL],tmpTaskQueue[Do.KEY_TASK_EXECUTE_ID]) in tmpService[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST]:
                            if tmpTaskQueue[isCluster] == isClusterConf.cancelTcpSend:
                                tmpTask = Task()
                                tmpTask.taskExecuteId = tmpTaskQueue[Do.KEY_TASK_EXECUTE_ID]
                                tmpTask.cancelTask()
                            else:
                                tmpTaskQueue[isCluster] = isClusterConf.notRun
                                taskQueueList[taskQueueIndex] = tmpTaskQueue
                        taskQueueIndex += 1
                    db = DBTool()
                    db.initGlobalDBConf()
                    res = db.execute_sql(
                        "UPDATE tb_run_server_conf SET STATUS = 0 WHERE serviceIp = '%s' AND servicePort = %s" % (tmpService[Do.KEY_RUN_SERVICE_IP], tmpService[Do.KEY_RUN_SERVICE_PORT]))
                    if res == False:
                        logging.error("服务设置为离线失败")
                    else:
                        print("服务设置为离线")
                        # logging.info("服务设置为离线")
                    db.release()
        time.sleep(10)