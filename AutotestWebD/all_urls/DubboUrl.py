from django.conf.urls import url
from apps.user_login.views import user_login

from apps.dubbo_interface.views import dubbo_interface,dubbo_interface_debug
from apps.dubbo_testcase.views import dubbo_testcase,dubbo_testcase_step,dubbo_testcasedebug
from apps.dubbo_task.views import dubbo_task,testReport,batchTask
from apps.dubbo_task_suite.views import dubbo_task_suite

urlpatterns = [
    ####interface######################
    url(r'^dubbo/interfaceList$', dubbo_interface.dubbo_interfaceCheck, name="dubboInterfaceList"),
    url(r'^dubbo/interfaceAddPage$', dubbo_interface.interfaceAddPage, name="dubboInterfaceAdd"),
    url(r'^dubbo/interfaceAdd$', dubbo_interface.interfaceAdd, name="dubboInterfaceDoAdd"),
    url(r'^dubbo/interfaceListDesc$', dubbo_interface.dubbo_interfaceListCheck, name="dubboInterfaceListDesc"),

    url(r'^dubbo/getDubboServices$', dubbo_interface.getDubboServices, name="dubboGetServices"),
    url(r'^dubbo/getDubboMethods$', dubbo_interface.getDubboMethodsInService, name="dubboGetMethods"),

    url(r'^dubbo/operationInterface$', dubbo_interface.operationInterface, name="dubboOperationInterface"),
    url(r'^dubbo/operationInterfaceByInterfaceId$', dubbo_interface.operationInterfaceByInterfaceId, name="dubboOperationInterfaceByInterfaceId"),
    url(r'^dubbo/getInterfaceDataById$', dubbo_interface.getInterfaceDataById, name="dubboGetInterfaceDataById"),
    url(r'^dubbo/interfaceSaveEdit$', dubbo_interface.interfaceSaveEdit, name="dubboInterfaceSaveEdit"),
    url(r'^dubbo/interfaceDel$', dubbo_interface.interfaceDel, name="dubboInterfaceDel"),
    url(r'^dubbo/interfaceQueryPeopleInterface$', dubbo_interface.queryPeopleInterface,name="dubboQueryPeopleInterface"),

    #debug
    url(r'^dubbo/interfaceDebugAdd$', dubbo_interface_debug.interfaceDebugAdd, name="dubboInterfaceDebugAdd"),
    url(r'^dubbo/sendDebugInterfaceTcpMsg$', dubbo_interface_debug.sendDebugInterfaceTcpMsg, name="dubboSendDebugInterfaceTcpMsg"),
    url(r'^dubbo/getDebugResult$', dubbo_interface_debug.getDebugResult,name="dubboGetDebugResult"),
    #dubbo 快速调试
    url(r'^dubbo/quickDebugPage$', dubbo_interface.interfaceQuickDebugPage, name="dubboQuickDebugPage"),
    url(r'^dubbo/getRequestAddr$', dubbo_interface.dubboGetRequestAddr, name="dubboGetRequestAddr"),
    url(r'^dubbo/getDubboServicesByAddr$', dubbo_interface.getDubboServicesByAddr, name="dubboGetDubboServicesByAddr"),
    url(r'^dubbo/getParamByServiceMethod$', dubbo_interface.getParamByServiceMethod, name="dubboGetParamByServiceMethod"),
    url(r'^dubbo/quickDebug$', dubbo_interface.quickDebug, name="dubboQuickDebug"),
    url(r'^dubbo/getRbecentQueryDebug$', dubbo_interface.getRbecentQueryDebug, name="dubboGetRbecentQueryDebug"),
    url(r'^dubbo/doTelnetCommand$', dubbo_interface.doTelnetCommand, name="dubboDoTelnetCommand"),

    ##########testcase##############################
    url(r'^dubbo/testcaseList$', dubbo_testcase.dubbo_testCaseCheck, name="dubboTestcaseList"),
    url(r'^dubbo/TestcaseListCheck$', dubbo_testcase.dubbo_testCaseListCheck, name="dubboTestcaseListCheck"),
    url(r'^dubbo/queryPeopleTestCase$', dubbo_testcase.queryPeopleTestCase, name="dubboDueryPeopleTestCase"),
    url(r'^dubbo/testCaseAddPage$', dubbo_testcase.testCaseAddPage, name="dubbo_TestCaseAddPage"),
    url(r'^dubbo/TestCaseAddPage/TestCaseStep$', dubbo_testcase.testCaseStepPage, name="dubbo_TestCaseStepPage"),
    url(r'^dubbo/TestCaseAddPage/TestCaseStepDetail$', dubbo_testcase.testCaseStepDetailPage,name="dubbo_TestCaseStepDetailPage"),
    url(r'^dubbo/TestCaseAdd$', dubbo_testcase.testCaseAdd, name="dubbo_testCaseAdd"),
    url(r'^dubbo/SelectInterfaceAddStep$', dubbo_testcase.selectInterfaceAddStep,name="dubbo_SelectInterfaceAddStep"),
    url(r'^dubbo/TestCaseSelectInterfaceList$', dubbo_testcase.testCaseSelectInterfaceCheckList,name="dubbo_TestCaseSelectInterfaceListCheck"),
    url(r'^dubbo/operationTestCase$', dubbo_testcase.operationTestCase, name="dubbo_operationTestCase"),
    url(r'^dubbo/getTestCaseDataForId$', dubbo_testcase.getTestCaseDataForId, name="dubbo_GetTestCaseDataForId"),
    url(r'^dubbo/TestCaseSaveEdit$', dubbo_testcase.testCaseSaveEdit, name="dubbo_testCaseSaveEdit"),
    url(r'^dubbo/TestCaseDel$', dubbo_testcase.testCaseDel, name="dubbo_testCaseDel"),
    url(r'^dubbo/TestCaseDebugAdd', dubbo_testcasedebug.testCaseDebugAdd, name="dubbo_TestCaseDebugAdd"),
    url(r'^dubbo/TestCaseDebug$', dubbo_testcasedebug.debugTestCase, name="dubbo_TestCaseDebug"),
    url(r'^dubbo/TestCaseDebugGetResult$', dubbo_testcasedebug.getDebugResult,name="dubbo_TestCaseDebugGetResult"),
    url(r'^dubbo/InterfaceDelTip$', dubbo_interface.interfaceGetSyncTestCaseStep, name="dubbo_InterfaceDelTip"),

    #task
    url(r'^dubbo/TaskCheck$', dubbo_task.dubbo_testCheck, name="dubbo_taskCheck"),
    url(r'^dubbo/TaskListCheck$', dubbo_task.dubbo_taskListCheck,name="dubbo_TaskListCheck"),
    url(r'^dubbo/TaskGetTaskFotTaskId$', dubbo_task.getTaskForTaskId, name="dubbo_TaskGetTaskFotTaskId"),
    url(r'^dubbo/TaskAddPage$', dubbo_task.taskAdd, name="dubbo_TaskAddPage"),
    url(r'^dubbo/TaskQueryPeopleTask$', dubbo_task.queryPeopleTask, name="dubbo_queryPeopleTask"),
    url(r'^dubbo/TaskSelectInterfacePage$', dubbo_task.TestCaseSelectInterfaceCheckList, name="dubbo_TaskSelectInterfacePage"),
    url(r'^dubbo/TaskSelectTestCasePage$', dubbo_task.dubboTaskSelectTestCaseCheckList,name="dubbo_TaskSelectTestCasePage"),
    url(r'^dubbo/TaskAddData$', dubbo_task.taskAddData,name="dubbo_TaskAddData"),
    url(r'^dubbo/operationTask$', dubbo_task.operationTask, name="dubbo_operationTask"),
    url(r'^dubbo/getTaskDataForTaskId$', dubbo_task.getTaskData, name="dubbo_taskGetTaskData"),
    url(r'^dubbo/TaskSaveEdit$', dubbo_task.taskDataEdit, name="dubbo_TaskSaveEdit"),
    url(r'^dubbo/TaskDel$', dubbo_task.taskDel, name="dubbo_TaskDel"),
    url(r'^dubbo/TaskDelTheSameCase$', dubbo_task.taskDelTheSameCase, name="dubbo_TaskDelTheSameCase"),
    url(r'^dubbo/getInterfaceListDataForTask$', dubbo_task.getInterfeceListDataForTask, name="dubboGetInterfaceListDataForTask"),
    url(r'^dubbo/getTestCaseListDataForTask$', dubbo_task.getTestCaseListDataForTask, name="dubboGetTestCaseListDataForTask"),
    url(r'^dubbo/TaskExecuteResult$', dubbo_task.taskResultCheck, name="dubbo_TaskExecuteResult"),
    url(r'^dubbo/TaskExecuteQueryPeopleTask$', dubbo_task.queryPeopleTaskExecute, name="dubbo_queryPeopleTaskExecute"),
    url(r'^dubbo/getTaskExecuteResult$', dubbo_task.getTaskResultList, name="dubbo_getTaskExecuteResult"),
    url(r'^dubbo/getTaskExecuteResultData$', dubbo_task.getTaskRestltDetail, name="dubbo_getTaskExecuteResultData"),
    url(r'^dubbo/getInterfaceListData$', dubbo_task.getInterfeceListData, name="dubbo_getInterfaceListData"),
    url(r'^dubbo/getTestCaseListData$', dubbo_task.getTestCaseListData, name="dubbo_getTestCaseListData"),
    url(r'^dubbo/TaskAgainRunTask$', dubbo_task.againRunTask, name="dubbo_TaskAgainRunTask"),
    url(r'^dubbo/TaskStopTaskRun$', dubbo_task.stopTaskRun, name="dubbo_TaskStopTaskRun"),
    url(r'^dubbo/TaskRunTask$', dubbo_task.taskRunAdd, name="dubbo_TaskRunTask"),
    url(r'^dubbo/GetSelectExecuteStatus$', dubbo_task.getSelectExecuteStatus, name="dubbo_GetSelectExecuteStatus"),
    url(r'^dubbo/UpdateTaskExecuteProgressData$', dubbo_task.updateTaskExecuteProgressData,
        name="dubbo_UpdateTaskExecuteProgressData"),

    #taskSuite
#taskSuite
    url(r'^dubbo/TaskSuiteCheck$', dubbo_task_suite.dubboTaskSuiteCheck, name="dubbo_taskSuiteCheck"),
    url(r'^dubbo/TaskSuiteListCheck$', dubbo_task_suite.dubbo_taskSuiteListCheck, name="dubbo_TaskSuiteListCheck"),
    url(r'^dubbo/TaskSuiteGetTaskSuiteFotTaskId$', dubbo_task.getTaskForTaskId, name="dubbo_TaskSuiteGetTaskSuiteFotTaskId"),
    url(r'^dubbo/TaskSuiteAddPage$', dubbo_task_suite.taskSuiteAdd, name="dubbo_TaskSuiteAddPage"),
    url(r'^dubbo/TaskSuiteSelectTaskPage$', dubbo_task_suite.dubboTaskSuiteSelectTaskList,name="dubbo_TaskSuiteSelectTaskPage"),
    url(r'^dubbo/TaskSuiteAddData$', dubbo_task_suite.taskSuiteAddData, name="dubbo_TaskSuiteAddData"),
    url(r'^dubbo/TaskSuiteSaveEdit$', dubbo_task_suite.taskSuitSaveEdit, name="dubbo_TaskSuiteSaveEdit"),
    url(r'^dubbo/operationTaskSuite$', dubbo_task_suite.operationTaskSuite, name="dubbo_operationTaskSuite"),
    url(r'^dubbo/getTaskSuiteDataForTaskSuiteId$', dubbo_task_suite.getTaskSuiteForTaskSuiteId, name="dubbo_getTaskSuiteForTaskSuiteId"),
    url(r'^dubbo/getTaskSuiteData$', dubbo_task_suite.getTaskSuiteData, name="dubbo_taskSuiteGetTaskSuiteData"),
    url(r'^dubbo/TaskSuiteDel$', dubbo_task_suite.taskSuiteDel, name="dubbo_TaskSuiteDel"),
    url(r'^dubbo/getTaskListDataForTaskSuite$', dubbo_task_suite.getTaskListDataForTaskSuite,
        name="dubbo_getTaskListDataForTaskSuite"),
    url(r'^dubbo/TaskSuiteExecuteResult$', dubbo_task_suite.taskSuiteResultCheck, name="dubbo_TaskSuiteExecuteResult"),
    url(r'^dubbo/getTaskSuiteExecuteResult$', dubbo_task_suite.getTaskSuiteResultList, name="dubbo_getTaskSuiteExecuteResult"),
    url(r'^dubbo/UpdateTaskSuiteExecuteProgressData$', dubbo_task_suite.updateTaskSuiteExecuteProgressData,
        name="dubbo_UpdateTaskSuiteExecuteProgressData"),
    url(r'^dubbo/TaskSuiteRunTask$', dubbo_task_suite.taskSuiteRunAdd, name="dubbo_TaskSuiteRunTask"),
    url(r'^dubbo/getTaskSuiteExecuteResultData$', dubbo_task_suite.getTaskSuiteRestltDetail, name="dubbo_getTaskSuiteExecuteResultData"),
    url(r'^dubbo/TaskSuiteAgainRun$', dubbo_task_suite.againRunTaskSuite, name="dubbo_TaskSuiteAgainRun"),
    url(r'^dubbo/TaskStopTaskSuiteRun$', dubbo_task_suite.stopTaskSuiteRun, name="dubbo_TaskStopTaskSuiteRun"),
    url(r'^dubbo/TaskSuiteGetSelectExecuteStatus$', dubbo_task_suite.getSelectExecuteStatus,
        name="dubbo_TaskSuiteGetSelectExecuteStatus"),

    ##########################未完成##################################
    url(r'^dubbo/testCaseAddPage$', dubbo_testcase.testCaseAddPage, name="dubbo_TestCaseStepCheck"),

    url(r'^dubbo/testCaseAddPage$', dubbo_testcase.testCaseAddPage, name="dubbo_History"),
    url(r'^dubbo/testCaseAddPage$', dubbo_testcase.testCaseAddPage, name="dubbo_SrcFileAnalyze"),
    url(r'^dubbo/testCaseAddPage$', dubbo_testcase.testCaseAddPage, name="dubbo_SrcFileCoverCheck"),
    url(r'^dubbo/testCaseAddPage$', dubbo_testcase.testCaseAddPage, name="dubbo_GlobalVarsConf"),
    url(r'^dubbo/testCaseAddPage$', dubbo_testcase.testCaseAddPage, name="dubbo_GlobalTextConf"),

    url(r'^dubbo/importLogPage$', dubbo_interface.importLogPage, name="dubbo_importLogPage"),
    url(r'^dubbo/saveLogDataToDubboInterfaces$', dubbo_interface.saveLogDataToDubboInterfaces, name="dubbo_saveLogDataToDubboInterfaces"),

]