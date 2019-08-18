from allmodels.DubboInterface import DubboInterface
from allmodels.DubboTestcase import DubboTestcase
from allmodels.DubboTask import DubboTask
from core.decorator.normal_functions import *


class DubboService(object):

    @catch_exception
    @take_time
    def executeTask(self,task = DubboTask()):
        task.execute()
        return task

    @catch_exception
    @take_time
    def execute_debug_interface(self,interface = DubboInterface()):
        #data process DBINFO
        interface.executeInterface()
        interface.updateByInterfaceDebugId()
        return interface

    @catch_exception
    @take_time
    def execute_debug_testcases(self,testcase = DubboTestcase()):
        testcase.execute()
        testcase.updateByCaseDebugId()
        return testcase

