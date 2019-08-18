import multiprocessing

from core.const.Do import Do

from allmodels.DubboTestcase import DubboTestcase
from allmodels.DubboInterface import DubboInterface
from core.decorator.normal_functions import *
from service.DubboService import DubboService
from service.HttpService import HttpService

class DubboCaseDebugProgress(multiprocessing.Process):

    def __init__(self,debugType = Do.TYPE_DEBUG_INTERFACE, interfaceDebugId = "", caseDebugId = "",caseDebugStepId = ""):
        multiprocessing.Process.__init__(self)
        # super(DubboCaseDebugThread, self).__init__()
        self.debugType = debugType
        self.interfaceDebugId = interfaceDebugId
        self.caseDebugId = caseDebugId
        self.caseStepDebugId = caseDebugStepId
        # if self.debugType == Do.TYPE_DEBUG_INTERFACE:
        #     self.dubboInterface = DubboInterface(interfaceDebugId=interfaceDebugId)
        #     if self.dubboInterface.execStatus != 1:
        #         logging.info("没有查到接口调试信息interfaceDebugId[%s]" % interfaceDebugId)
        #         return
        #     # self.dubboInterface.interfaceDebugId = interfaceDebugId
        #     self.dubboInterface.generateByInterfaceDebugIdForRedis()
        # elif self.debugType == Do.TYPE_DEBUG_CASE:
        #     self.dubboCase = DubboTestcase()
        #     # self.dubboCase.caseDebugId = caseDebugId
        #     # self.dubboCase.caseStepList = stepTestcaseList
        #     self.dubboCase.generateByCaseDebugIdAndCaseStepDebugIdList(caseDebugId,stepTestcaseList)
    @catch_exception
    @take_time
    def run(self):
        if self.debugType == Do.TYPE_DEBUG_INTERFACE:
            self.dubboInterface = DubboInterface(interfaceDebugId=self.interfaceDebugId)
            self.dubboInterface.generateByInterfaceDebugIdForRedis()
            if self.dubboInterface.execStatus != 1:
                logging.info("没有查到接口调试信息interfaceDebugId[%s]" % self.interfaceDebugId)
                return
            self.debugInterface(self.dubboInterface)
        elif self.debugType == Do.TYPE_DEBUG_CASE:
            # self.debugCase()
            self.dubboCase = DubboTestcase()
            self.dubboCase.generateByCaseDebugIdAndCaseStepDebugIdList(self.caseDebugId, self.caseStepDebugId)
            if len(self.dubboCase.stepTestcaseList) == 0:
                logging.info("用例步骤数量为0，不进行用例调试")
                return
            self.debugCase(self.dubboCase)
        else:
            logging.error("错误的调试类型debugType.")

    @catch_exception
    @take_time
    def debugInterface(self,dubboInterface):
        logging.debug("开始进行接口调试！")
        # dubboInterface.executeInterface()
        # dubboInterface.updateByInterfaceDebugId()
        DubboService().execute_debug_interface(interface=self.dubboInterface)
        logging.debug('接口调试Done!')

    @catch_exception
    @take_time
    def debugCase(self,dubboTestCase):
        logging.debug("开始进行用例调试！")
        # self.dubboCase.execute()
        # self.dubboCase.updateByCaseDebugId()

        DubboService().execute_debug_testcases(testcase=self.dubboCase)
        logging.debug('CASE debug Done!')



