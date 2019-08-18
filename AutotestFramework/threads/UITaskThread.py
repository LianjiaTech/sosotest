import threading

from allmodels_ui.UITestTask import UITestTask
from core.decorator.normal_functions import *


class UITaskThread(threading.Thread):
    def __init__(self,task = UITestTask()):
        super(UITaskThread, self).__init__()
        self.task = task

    @catch_exception
    @take_time
    def run(self):
        logging.debug("开始进行任务执行！")
        self.task.execute()
        logging.debug('TaskThread Done!')

