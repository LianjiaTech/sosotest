from runfunc.ui_threadProcess import *


def startUIServer():
    #DONE 启动server监听新消息
    while True:
        retryTime = 0
        #========TCP=====================
        try:
            # 开启ip和端口
            ip_port = (TcpServerConf.ip, TcpServerConf.uiport)
            # 生成句柄
            socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
                conn = False
                logging.debug("****************************************UIServer监听中...****************************************")
                # 阻塞
                conn, addr = socketServer.accept()
                # 获取客户端请求数据
                data = conn.recv(TcpServerConf.recvLength)
                # 打印接受数据 注：当浏览器访问的时候，接受的数据的浏览器的信息等。
                dataString = data.decode("utf8")
                logging.debug("收到请求：%s" % dataString)
                if isJson(dataString):
                    dataDict = json.loads(dataString)
                    logging.debug("startUIServer: 请求数据：%s" % dataDict)
                    if Do.KEY_DO not in dataDict.keys():
                        logging.debug('ERROR:缺少必要字段[%s]！' % Do.KEY_DO)
                        conn.send(bytes('ERROR:缺少必要字段[%s]！' % Do.KEY_DO, 'utf8'))
                    elif dataDict[Do.KEY_DO] == Do.TYPE_UITASK_EXECUTE:
                        #UITASK执行
                        if Do.KEY_UITASK_EXEC_ID in dataDict.keys() and isInt(dataDict[Do.KEY_UITASK_EXEC_ID]):
                            uiTaskQueue.append(dataDict)
                            conn.send(bytes("ok", 'utf8'))
                            logging.debug("新增uiTaskQueue %s" % uiTaskQueue)
                        else:
                            #task执行id不合法或者不存在
                            tmpText = "ERROR:请求的TaskExecId不存在或者不是int。"
                            logging.debug("startUIServer: %s" % tmpText)
                            conn.send(bytes(tmpText, 'utf8'))

                    elif dataDict[Do.KEY_DO] == Do.TYPE_UITASK_CANCEL:
                        #UITASK取消
                        if Do.KEY_UITASK_EXEC_ID in dataDict.keys() and isInt(dataDict[Do.KEY_UITASK_EXEC_ID]):
                            uiTaskCancelQueue.append(dataDict)
                            conn.send(bytes("ok", 'utf8'))
                            logging.debug("新增uiTaskCancelQueue %s" % uiTaskCancelQueue)

                        else:
                            #task执行id不合法或者不存在
                            tmpText = "ERROR:请求的TaskExecId不存在或者不是int。"
                            logging.debug("startUIServer: %s" % tmpText)
                            conn.send(bytes(tmpText, 'utf8'))
                    else:
                        #类型错误
                        tmpText = "ERROR:请求的do必须是31[UITaskExecute]或者32[UITaskCancel]。"
                        logging.debug("startUIServer: %s" % tmpText)
                        conn.send(bytes(tmpText, 'utf8'))
                else:
                    tmpText = "ERROR:请求的必须是json字符串，请按照协议进行请求。"
                    logging.debug("startUIServer: %s" % tmpText)
                    # 向对方发送数据
                    conn.send(bytes(tmpText, 'utf8'))
            except Exception as e:
                logging.error("服务监听出现异常：%s" % traceback.format_exc())
            finally:
                if conn:
                    conn.close()
                logging.debug("**************************************UIServer请求处理结束**************************************")

        time.sleep(6)