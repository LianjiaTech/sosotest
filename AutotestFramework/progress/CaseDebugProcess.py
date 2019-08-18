import multiprocessing

from core.const.Do import Do

from allmodels.HttpInterface import HttpInterface
from allmodels.HttpTestcase import HttpTestcase
from core.decorator.normal_functions import *
from service.HttpService import HttpService

class CaseDebugProcess(multiprocessing.Process):

    def __init__(self,debugType = Do.TYPE_DEBUG_INTERFACE, interfaceDebugId = 0,testCaseDebugId = 0,testCaseStepDebugId = 0):
        # super(CaseDebugProcess, self).__init__()
        multiprocessing.Process.__init__(self)
        self.debugType = debugType
        self.interfaceDebugId = interfaceDebugId
        self.testCaseDebugId = testCaseDebugId
        self.testCaseStepDebugId = testCaseStepDebugId

        # self.httpInterface = httpInterface
        # self.httpCase = httpCase

    @catch_exception
    @take_time
    def run(self):

        if self.debugType == Do.TYPE_DEBUG_INTERFACE:
            self.httpInterface = HttpInterface(interfaceDebugId=self.interfaceDebugId)
            self.httpInterface.generateByInterfaceDebugId()
            if self.httpInterface.execStatus != 1:
                logging.info("没有查到接口调试信息interfaceDebugId[%s]" % self.interfaceDebugId)
                return
            self.debugInterface()
        elif self.debugType == Do.TYPE_DEBUG_CASE:
            self.httpCase = HttpTestcase()
            self.httpCase.generateByCaseDebugIdAndCaseStepDebugIdList(self.testCaseDebugId, self.testCaseStepDebugId)
            if len(self.httpCase.stepTestcaseList) == 0:
                logging.info("用例步骤数量为0，不进行用例调试")
                return
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



