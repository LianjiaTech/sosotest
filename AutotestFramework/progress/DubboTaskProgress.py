import multiprocessing

from allmodels.DubboTask import DubboTask
from core.decorator.normal_functions import *
from core.const.Do import *
from service.DubboService import DubboService
from core.config.InitConfig import isClusterConf

class DubboTaskProgress(multiprocessing.Process):
    def __init__(self,taskExecuteId = 0,runTaskServiceIp="",taskSuiteExecuteId = 0,serverDataDict = {}):
        multiprocessing.Process.__init__(self)
        # super(DubbpTaskThread, self).__init__()
        # self.task = task
        self.task = DubboTask()
        self.task.taskSuiteExecuteId = taskSuiteExecuteId
        self.task.taskExecuteId = taskExecuteId
        self.task.runTaskServiceIp = runTaskServiceIp
        self.task.generateByTaskExecuteId()
        self.serverDataDict = serverDataDict

    @catch_exception
    @take_time
    def run(self):
        tmpExecuteId = "%s_%s" % (self.task.protocol, self.task.taskExecuteId)
        if tmpExecuteId in self.serverDataDict[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST]:
            self.serverDataDict[tmpExecuteId] = isClusterConf.runTaskInitDone
        logging.debug("开始进行任务执行！")
        self.task = DubboService().executeTask(self.task)

        if tmpExecuteId in self.serverDataDict.keys():
            self.serverDataDict.pop(tmpExecuteId)

        if tmpExecuteId in self.serverDataDict[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST]:
            tmpTaskList = self.serverDataDict[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST]
            tmpTaskList.remove(tmpExecuteId)
            self.serverDataDict[Do.KEY_RUN_SERVICE_CURRENT_TASK_LIST] = tmpTaskList
            if self.serverDataDict[Do.KEY_RUN_SERVICE_CURRENT_TASK_PROGRESS_NUM] > 0:
                self.serverDataDict[Do.KEY_RUN_SERVICE_CURRENT_TASK_PROGRESS_NUM] -= 1
        logging.debug('TaskThread Done!')

