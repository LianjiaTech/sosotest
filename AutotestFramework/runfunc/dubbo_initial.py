import logging.handlers
import socket,os,threading
from core.const.Do import Do

from allmodels.HttpInterface import HttpInterface
from allmodels.HttpTestcase import HttpTestcase
from allmodels.DubboInterface import DubboInterface
from allmodels.DubboTestcase import DubboTestcase

from allmodels.Task import Task
from allmodels.DubboTask import DubboTask
from core.config.InitConfig import TcpServerConf
from core.const.GlobalConst import ExecStatus
from core.decorator.normal_functions import *
from core.tools.DBTool import DBTool
from core.tools.TypeTool import TypeTool
# from runfunc.runGlobalVars import *
from threads.DubboCaseDebugThread import DubboCaseDebugThread
from threads.DubboTaskThread import DubbpTaskThread
from core.tools.CommonFunc import *


######################################
###dubbo相关
debugThreadDict = {} # 哪些调试线程在执行，key是username，value是正在调试的debugId
serviceThreadDict = {"AliveThreadCount":0}
debugQueue = []
taskQueue = []
taskCancelQueue = []
#####################################
@catch_exception
def init_logging(logFilePath = "test.log",level = logging.DEBUG):
    #################################################################################################
    logging.basicConfig(level=level)
    #################################################################################################
    #################################################################################################
    # 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
    Rthandler = logging.handlers.RotatingFileHandler(logFilePath, maxBytes=10 * 1024 * 1024, backupCount=5)
    Rthandler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    Rthandler.setFormatter(formatter)
    logging.getLogger('').addHandler(Rthandler)
    #################################################################################################

@catch_exception
@take_time
def init_debug_queue_interface(db):
    colsStr = "id,addBy,httpConfKey"
    tbName = "tb_http_interface_debug"
    whereStr = "execStatus = %d" % ExecStatus.NOTRUN
    orderBy = "addTime asc"
    sql = "select %s from %s where %s order by %s" % (colsStr, tbName, whereStr, orderBy)
    res = db.execute_sql(sql)
    if res == False:
        logging.error("init_debug_queue_interface: 初始化调试接口队列失败！")
        return False
    logging.debug("init_debug_queue_interface: 初始化tb_http_interface_debug结果：%s" % str(res))
    for tRes in res:
        tmpData = {}
        tmpData[Do.KEY_DO] = Do.TYPE_DEBUG_INTERFACE
        tmpData[Do.KEY_INTERFACE_DEBUG_ID] = tRes['id']
        debugQueue.append(tmpData)
        logging.debug("init_debug_queue_interface: debugQueue加入新data:%s 。来源表：%s" % (tmpData,tbName))
        logging.debug("init_debug_queue_interface: debugQueue:%s" % debugQueue)

    logging.info("init_debug_queue_interface: 初始化接口调试表完成debugQueue:%s" % debugQueue)

@catch_exception
@take_time
def init_debug_queue_case(db):
    #TODO 初始化 case debug
    colsStr = "id,caseId,addBy"
    tbName = "tb_http_testcase_debug"
    whereStr = "execStatus = %d" % ExecStatus.NOTRUN
    orderBy = "addTime asc"
    sql = "select %s from %s where %s order by %s" % (colsStr, tbName, whereStr, orderBy)
    res = db.execute_sql(sql)
    logging.debug("init_debug_queue_case: 初始化tb_http_testcase_debug结果：%s" % str(res))
    if res == False:
        logging.error("init_debug_queue_case: 初始化调试用例队列失败！")
        return False
    for tRes in res:
        tmpData = {}
        tmpData[Do.KEY_DO] = Do.TYPE_DEBUG_CASE
        tmpData[Do.KEY_CASE_DEBUG_ID] = tRes['id']

        colsStr = "id"
        tbName = "tb_http_testcase_step_debug"
        whereStr = "caseId='%s' and addBy='%s'" % (tRes['caseId'], tRes['addBy'])
        orderBy = "stepNum asc"
        sql = "select %s from %s where %s order by %s" % (colsStr, tbName, whereStr, orderBy)
        resSteps = db.execute_sql(sql)
        caseStepDebugIdList = []
        for tmpStepInfo in resSteps:
            caseStepDebugIdList.append(int(tmpStepInfo['id']))

        tmpData[Do.KEY_CASE_STEP_DEBUG_ID_LIST] = caseStepDebugIdList
        debugQueue.append(tmpData)
        logging.debug("init_debug_queue_case: debugQueue加入新data:%s 。来源表：%s" % (tmpData, tbName))
        logging.debug("init_debug_queue_case: debugQueue:%s" % debugQueue)

    logging.info("init_debug_queue_case: 初始化用例调试表完成debugQueue:%s" % debugQueue)

@catch_exception
@take_time
def init_task_queue(db):
    #DONE 初始化 taskrun  {'do': 3, 'TaskExecuteId': '1'}
    colsStr = "id"
    tbName = "tb2_dubbo_task_execute"
    whereStr = "execStatus = %d or execStatus = %d " % (ExecStatus.NOTRUN, ExecStatus.RUNNING)
    orderBy = "addTime asc"
    sql = "select %s from %s where %s order by %s" % (colsStr, tbName, whereStr, orderBy)
    res = db.execute_sql(sql)
    logging.debug("init_task_queue: 初始化tb_task_execute结果：%s" % str(res))
    if res == False:
        logging.error("init_task_queue: 初始化任务执行队列失败！")
        return False
    for tRes in res:
        tmpData = {}
        tmpData[Do.KEY_DO] = Do.TYPE_TASK_EXECUTE
        tmpData[Do.KEY_TASK_EXECUTE_ID] = tRes['id']
        taskQueue.append(tmpData)
        logging.info("init_task_queue: taskQueue加入新data:%s 。来源表：%s" % (tmpData,tbName))
        logging.info("init_task_queue: taskQueue:%s" % taskQueue)

    logging.info("init_task_queue: 初始化任务执行表完成taskQueue:%s" % taskQueue)

@catch_exception
@take_time
def init_task_cancel_queue(db):
    #DONE 初始化 taskrun  {'do': 3, 'TaskExecuteId': '1'}
    colsStr = "id"
    tbName = "tb2_dubbo_task_execute"
    whereStr = "execStatus = %d" % ExecStatus.CANCELING
    orderBy = "addTime asc"
    sql = "select %s from %s where %s order by %s" % (colsStr, tbName, whereStr, orderBy)
    res = db.execute_sql(sql)
    logging.debug("init_task_cancel_queue: 初始化tb_task_execute取消结果：%s" % str(res))
    if res == False:
        logging.error("init_task_cancel_queue: 初始化任务取消队列失败！")
        return False
    for tRes in res:
        tmpData = {}
        tmpData[Do.KEY_DO] = Do.TYPE_TASK_CANCEL
        tmpData[Do.KEY_TASK_EXECUTE_ID] = tRes['id']
        taskCancelQueue.append(tmpData)
        logging.debug("init_task_cancel_queue: taskCancelQueue加入新data:%s 。来源表：%s" % (tmpData,tbName))
        logging.debug("init_task_cancel_queue: taskCancelQueue:%s" % taskCancelQueue)

    logging.info("init_task_cancel_queue: 初始化任务取消表完成taskCancelQueue:%s" % taskCancelQueue)

@catch_exception
@take_time
def init_global_queue():
    db = DBTool()
    db.initGlobalDBConf()
    #======加入未执行的接口调试 数据表tb_http_interface_debug
    # init_debug_queue_interface(db)
    # init_debug_queue_case(db)
    init_task_queue(db)
    init_task_cancel_queue(db)
    db.release()
