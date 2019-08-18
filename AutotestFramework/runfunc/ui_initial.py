import logging
import logging.handlers
import socket,os,threading
from core.const.Do import Do

from core.const.GlobalConst import ExecStatus
from core.tools.DBTool import DBTool
from core.tools.TypeTool import TypeTool

from runfunc.initial import init_logging
from runfunc.ui_threadProcess import *
from core.config.InitConfig import *
import socket,traceback,os
from core.tools.CommonFunc import *

from allmodels_ui.UITestTask import UITestTask
from threads.UITaskThread import UITaskThread

from copy import deepcopy
##########################################################################################################
##########################################################################################################
##########################################################################################################
uiTaskQueue = []
uiTaskCancelQueue = []
maxUITaskThreadNums = 7  #最大能并行的UI测试任务数量
maxWebThreadNums = 5
maxAndroidThreadNums = 3
maxIosThreadNums = 4
executingWebThreadNum = 0  #当前执行中的UI测试任务数量
executingIosThreadNum = 0  #当前执行中的UI测试任务数量
executingAndroidThreadNum = 0  #当前执行中的UI测试任务数量
executingUITaskThreadNum = 0  #当前执行中的UI测试任务数量
executintUITaskThreadDict = {} #当前活着的threadDict
executintWebThreadDict = {} #当前活着的threadDict
executintIosThreadDict = {} #当前活着的threadDict
executintAndroidThreadDict = {} #当前活着的threadDict



##########################################################################################################
##########################################################################################################
##########################################################################################################

def init_ui_task_queue():
    db = DBTool().initGlobalDBConf()
    # DONE 初始化 taskrun  {'do': 3, 'TaskExecuteId': '1'}
    colsStr = "id"
    tbName = "tb_ui_test_execute"
    whereStr = "execStatus = %d or execStatus = %d " % (ExecStatus.NOTRUN, ExecStatus.RUNNING)
    orderBy = "addTime asc"
    sql = "select %s from %s where %s order by %s" % (colsStr, tbName, whereStr, orderBy)
    res = db.execute_sql(sql)
    #重置所有模拟器
    mobileServer = db.execute_sql("UPDATE tb_ui_mobile_server SET STATUS = 0")

    db.release()
    logging.debug("init_ui_task_queue: 初始化tb_ui_test_execute结果：%s" % str(res))
    if res == False:
        logging.error("init_ui_task_queue: 初始化任务执行队列失败！")
        return False
    if mobileServer == False:
        logging.error("init_ui_task_queue: 初始化模拟器状态失败！")
        return False
    for tRes in res:
        tmpData = {}
        tmpData[Do.KEY_DO] = Do.TYPE_UITASK_EXECUTE
        tmpData[Do.KEY_UITASK_EXEC_ID] = tRes['id']
        uiTaskQueue.append(tmpData)
        logging.info("init_ui_task_queue: uiTaskQueue加入新data:%s 。来源表：%s" % (tmpData, tbName))
        logging.info("init_ui_task_queue: uiTaskQueue:%s" % uiTaskQueue)

    logging.info("init_ui_task_queue: 初始化任务执行表完成uiTaskQueue:%s" % uiTaskQueue)

def init_cancel_ui_task_queue():
    db = DBTool().initGlobalDBConf()
    # DONE 初始化 taskrun  {'do': 3, 'TaskExecuteId': '1'}
    colsStr = "id"
    tbName = "tb_ui_test_execute"
    whereStr = "execStatus = %d " % (ExecStatus.CANCELING)
    orderBy = "addTime asc"
    sql = "select %s from %s where %s order by %s" % (colsStr, tbName, whereStr, orderBy)
    res = db.execute_sql(sql)
    db.release()
    logging.debug("init_cancel_ui_task_queue: 初始化tb_ui_test_execute结果：%s" % str(res))
    if res == False:
        logging.error("init_cancel_ui_task_queue: 初始化任务执行队列失败！")
        return False
    for tRes in res:
        tmpData = {}
        tmpData[Do.KEY_DO] = Do.TYPE_UITASK_CANCEL
        tmpData[Do.KEY_UITASK_EXEC_ID] = tRes['id']
        uiTaskCancelQueue.append(tmpData)
        logging.info("init_cancel_ui_task_queue: uiTaskCancelQueue加入新data:%s 。来源表：%s" % (tmpData, tbName))
        logging.info("init_cancel_ui_task_queue: uiTaskCancelQueue:%s" % uiTaskCancelQueue)

    logging.info("init_cancel_ui_task_queue: 初始化任务执行表完成uiTaskCancelQueuee:%s" % uiTaskCancelQueue)
