import threading

from core.const.Do import Do

from allmodels.HttpInterface import HttpInterface
from allmodels.HttpTestcase import HttpTestcase
from core.decorator.normal_functions import *
from service.HttpService import HttpService

class CaseDebugThread(threading.Thread):

    def __init__(self,debugType = Do.TYPE_DEBUG_INTERFACE, httpInterface = HttpInterface(), httpCase = HttpTestcase()):
        super(CaseDebugThread, self).__init__()
        self.debugType = debugType
        self.httpInterface = httpInterface
        self.httpCase = httpCase

    @catch_exception
    @take_time
    def run(self):
        if self.debugType == Do.TYPE_DEBUG_INTERFACE:
            self.debugInterface()
        elif self.debugType == Do.TYPE_DEBUG_CASE:
            self.debugCase()
        else:
            logging.error("错误的调试类型debugType.")

    @catch_exception
    @take_time
    def debugInterface(self):
        logging.debug("开始进行接口调试！")
        HttpService().execute_debug_interface(self.httpInterface)
        logging.debug('接口调试Done!')

    @catch_exception
    @take_time
    def debugCase(self):
        logging.debug("开始进行用例调试！")
        HttpService().execute_debug_testcases(self.httpCase)
        logging.debug('CASE debug Done!')



