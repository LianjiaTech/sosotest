import threading

from allmodels.DubboTask import DubboTask
from core.decorator.normal_functions import *
from service.DubboService import DubboService


class DubbpTaskThread(threading.Thread):
    def __init__(self,task = DubboTask()):
        super(DubbpTaskThread, self).__init__()
        self.task = task

    @catch_exception
    @take_time
    def run(self):
        logging.debug("开始进行任务执行！")
        self.task = DubboService().executeTask(self.task)
        logging.debug('TaskThread Done!')

