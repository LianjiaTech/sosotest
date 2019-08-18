import threading

from core.const.Do import Do

from allmodels.DubboTestcase import DubboTestcase
from allmodels.DubboInterface import DubboInterface
from core.decorator.normal_functions import *
from service.HttpService import HttpService

class DubboCaseDebugThread(threading.Thread):

    def __init__(self,debugType = Do.TYPE_DEBUG_INTERFACE, dubboInterface = DubboInterface(), dubboCase = DubboTestcase()):
        super(DubboCaseDebugThread, self).__init__()
        self.debugType = debugType
        self.dubboInterface = dubboInterface
        self.dubboCase = dubboCase

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
        self.dubboInterface.executeInterface()
        self.dubboInterface.updateByInterfaceDebugId()
        logging.debug('接口调试Done!')

    @catch_exception
    @take_time
    def debugCase(self):
        logging.debug("开始进行用例调试！")
        self.dubboCase.execute()
        self.dubboCase.updateByCaseDebugId()
        logging.debug('CASE debug Done!')



