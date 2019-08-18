import os
import sys,io

import threading,logging
rootpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\","/")
syspath=sys.path
sys.path=[]
sys.path.append(rootpath) #指定搜索路径绝对目录
sys.path.extend([rootpath+i for i in os.listdir(rootpath) if i[0]!="."])#将工程目录下的一级目录添加到python搜索路径中
sys.path.extend(syspath)

from runfunc.ui_listenserver import *

if __name__ == '__main__':
    #初始化logger

    init_logging(logFilePath=LogConfig.FILE_UILOG,level= LogConfig.LEVEL ) #LogConfig.LEVEL
    logging.info("=========================开始启动任务队列=========================")
    #从数据库中初始化队列
    init_ui_task_queue()
    init_cancel_ui_task_queue()
    logging.info("run.py_main: UItask队列初始化完毕！")
    # 开启监听
    threading.Thread(target=startUIServer, args=()).start()
    logging.info("run.py_main: UI实时实时监听启动完成！") #t
    threading.Thread(target=thread_process_ui_task_queue, args=()).start()
    logging.info("run.py_main: UI任务执行启动完成！")
    threading.Thread(target=thread_process_ui_task_cancel_queue, args=()).start()
    logging.info("run.py_main: UI任务取消启动完成！")

    logging.info("=========================所有任务执行完毕=========================")
