import threading

from allmodels.Task import Task
from core.decorator.normal_functions import *
from service.HttpService import HttpService


class TaskThread(threading.Thread):
    def __init__(self,task = Task()):
        super(TaskThread, self).__init__()
        self.task = task

    @catch_exception
    @take_time
    def run(self):
        logging.debug("开始进行任务执行！")
        self.task = HttpService().executeTask(self.task)
        logging.debug('TaskThread Done!')

