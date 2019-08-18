from allmodels.HttpInterface import HttpInterface
from allmodels.HttpTestcase import HttpTestcase
from allmodels.Task import Task
from core.decorator.normal_functions import *


class HttpService(object):

    @catch_exception
    @take_time
    def executeTask(self,task = Task()):
        task.execute()
        return task

    @catch_exception
    @take_time
    def execute_debug_interface(self,interface = HttpInterface()):
        #data process DBINFO
        interface.executeInterface()
        interface.updateByInterfaceDebugId()
        return interface

    @catch_exception
    @take_time
    def execute_debug_testcases(self,testcase = HttpTestcase()):
        testcase.execute()
        testcase.updateByCaseDebugId()
        return testcase

