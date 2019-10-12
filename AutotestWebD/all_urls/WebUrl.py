from django.conf.urls import url
from apps.user_login.views import user_login
from apps.interface.views import http_interface, http_interface_debug,http_interface_plug_in
from apps.test_case.views import http_test_case, http_test_case_debug, http_test_case_step,http_test_case_plug_in
from apps.task.views import http_task,http_CICD_task
from apps.user_center.views import global_vars_conf, global_text_conf, user_http_conf,user_service_conf
from apps.history_statistics.views import http_history, http_statistics
from apps.config.views import service, http_conf, businessLine_module_relation
from apps.task.views import testReport
from apps.user_center.views import user_token, user_invoke, user_CI,user_uri_conf
from apps.src_file_analyze.views import src_file, src_file_cover, src_task_file_cover
from apps.help_docs.views import public_key_details
from apps.version_manage.views import version_show

from apps.task_suite.views import http_task_suite
from apps.config.views import page_error

urlpatterns = [
    url(r'^$', user_login.index, ),
    url(r'^user/login$', user_login.index),
    url(r'^user/logout$', user_login.logout, name="logout"),
    url(r'^user/dologin$', user_login.userLogin, name="dologin"), # 测试环境登录

    url(r'^user/updatePwd$', user_login.updatePwd, name="updatePwd"),
    url(r'^userLoginTestGetCookie$', user_login.userLoginTestGetCookie),
    url(r'^service/getServiceConf$', service.getServiceConf, name="getServiceConf"),
    url(r'^config/getDebugBtn$', http_conf.getDebugBtn, name="getDebugBtn"),
    # uploads
    url(r'^reports/([\w\-\.\/]+)$', testReport.testreport),
    # interface
    url(r'^interfaceTest/HTTP_InterfaceCheck$', http_interface.http_interfaceCheck, name="HTTP_InterfaceCheck"),
    url(r'^interfaceTest/HTTP_InterfaceListCheck$', http_interface.http_interfaceListCheck,
        name="HTTP_InterfaceListCheck"),
    url(r'^interfaceTest/HTTP_InterfaceAddPage$', http_interface.interfaceAddPage, name="HTTP_InterfaceAddPage"),
    url(r'^interfaceTest/HTTP_InterfaceDel$', http_interface.interfaceDel, name="HTTP_InterfaceDel"),
    url(r'^interfaceTest/HTTP_InterfaceDelTip$', http_interface.interfaceGetSyncTestCaseStep,
        name="HTTP_InterfaceDelTip"),
    url(r'^interfaceTest/HTTP_operationInterface$', http_interface.operationInterface, name="HTTP_operationInterface"),
    url(r'^interfaceTest/HTTP_operationInterfaceByInterfaceId$', http_interface.operationInterfaceByInterfaceId, name="HTTP_operationInterfaceByInterfaceId$"),
    url(r'^interfaceTest/HTTP_getInterfaceDataForId$', http_interface.getInterfaceDataForId,
        name="getInterfaceDataForId"),
    url(r'^interfaceTest/HTTP_InterfaceAdd$', http_interface.interfaceAdd, name="HTTP_InterfaceAdd"),
    url(r'^interfaceTest/HTTP_InterfaceDebugAdd$', http_interface_debug.interfaceDebugAdd,
        name="HTTP_InterfaceDebugAdd"),
    url(r'^interfaceTest/HTTP_InterfaceDebug$', http_interface_debug.debugInterface, name="HTTP_InterfaceDebug"),
    url(r'^interfaceTest/HTTP_InterfaceDebugGetResult$', http_interface_debug.getDebugResult,
        name="HTTP_InterfaceDebugGetResult"),
    url(r'^interfaceTest/HTTP_InterfaceQueryPeopleInterface$', http_interface.queryPeopleInterface,
        name="queryPeopleInterface"),
    url(r'^interfaceTest/queryPeopleInterfaceByTableName$', http_interface.queryPeopleInterfaceByTableName,
        name="queryPeopleInterfaceByTableName"),
    url(r'^interfaceTest/HTTP_InterfaceSaveEdit$', http_interface.interfaceSaveEdit, name="HTTP_InterfaceSaveEdit"),
    url(r'^interfaceTest/HTTP_InterfaceGetAutoFillData$', http_interface.interfaceGetAutoFillData, name="HTTP_InterfaceGetAutoFillData"),

    # 插件录入
    url(r'^interfaceTest/HTTP_InterfacePlugIn$', http_interface_plug_in.interface_plug_in ),
    url(r'^interfaceTest/HTTP_InterfacePlugInGetData$', http_interface_plug_in.getRedisIntrerface,name="getRedisInterfaceData"),

    # testCase
    url(r'^interfaceTest/HTTP_TestCaseCheck$', http_test_case.http_testCaseCheck, name="HTTP_testCaseCheck"),
    url(r'^interfaceTest/HTTP_TestCaseListCheck$', http_test_case.http_testCaseListCheck,
        name="HTTP_testCaseListCheck"),
    url(r'^interfaceTest/HTTP_TestCaseAddPage$', http_test_case.testCaseAddPage, name="HTTP_TestCaseAddPage"),
    url(r'^interfaceTest/HTTP_TestCaseAddPage/TestCaseStep$', http_test_case.testCaseStepPage,
        name="HTTP_TestCaseStepPage"),
    url(r'^interfaceTest/HTTP_TestCaseAddPage/TestCaseStepDetail$', http_test_case.testCaseStepDetailPage,
        name="HTTP_TestCaseStepDetailPage"),
    url(r'^interfaceTest/HTTP_InterfaceQueryPeopleTestCase$', http_test_case.queryPeopleTestCase,
        name="queryPeopleTestCase"),
    url(r'^interfaceTest/HTTP_getTestCaseDataForId$', http_test_case.getTestCaseDataForId, name="getTestCaseDataForId"),
    url(r'^interfaceTest/HTTP_operationTestCase$', http_test_case.operationTestCase, name="HTTP_operationTestCase"),
    url(r'^interfaceTest/HTTP_SelectInterfaceAddStep$', http_test_case.selectInterfaceAddStep,
        name="HTTP_SelectInterfaceAddStep"),
    url(r'^interfaceTest/HTTP_TestCaseAdd$', http_test_case.testCaseAdd, name="HTTP_testCaseAdd"),
    url(r'^interfaceTest/HTTP_TestCaseDel$', http_test_case.testCaseDel, name="HTTP_testCaseDel"),
    url(r'^interfaceTest/HTTP_TestCaseSaveEdit$', http_test_case.testCaseSaveEdit, name="HTTP_testCaseSaveEdit"),
    url(r'^interfaceTest/HTTP_TestCaseDebugAdd', http_test_case_debug.testCaseDebugAdd, name="HTTP_TestCaseDebugAdd"),
    url(r'^interfaceTest/HTTP_TestCaseDebug$', http_test_case_debug.debugTestCase, name="HTTP_TestCaseDebug"),
    url(r'^interfaceTest/HTTP_TestCaseDebugGetResult$', http_test_case_debug.getDebugResult,
        name="HTTP_TestCaseDebugGetResult"),
    url(r'^interfaceTest/HTTP_TestCaseSelectInterfaceList$', http_test_case.http_testCaseSelectInterfaceCheckList,
        name="HTTP_TestCaseSelectInterfaceListCheck"),

    url(r'^interfaceTest/HTTP_TestCaseStepCheck$', http_test_case_step.http_testCaseStepCheck,
        name="HTTP_TestCaseStepCheck"),
    url(r'^interfaceTest/HTTP_TestCaseStepListCheck$', http_test_case_step.http_testCaseStepListCheck,
        name="HTTP_TestCaseStepListCheck"),

    #插件录入
    url(r'^interfaceTest/HTTP_TestCasePlugIn$', http_test_case_plug_in.test_case_plug_in,),
    url(r'^interfaceTest/HTTP_TestCasePlugInGetData$', http_test_case_plug_in.getRedisTestCase,name="getRedisTestCaseData"),

    # task
    url(r'^interfaceTest/HTTP_TaskCheck$', http_task.http_teskCheck, name="HTTP_taskCheck"),
    url(r'^interfaceTest/HTTP_TaskListCheck$', http_task.http_taskListCheck, name="HTTP_TaskListCheck"),
    url(r'^interfaceTest/HTTP_TaskGetTaskFotTaskId$', http_task.getTaskForId, name="HTTP_TaskGetTaskFotTaskId"),
    url(r'^interfaceTest/HTTP_TaskAddPage$', http_task.taskAdd, name="HTTP_TaskAddPage"),
    url(r'^interfaceTest/HTTP_TaskQueryPeopleTask$', http_task.queryPeopleTask, name="queryPeopleTask"),
    url(r'^interfaceTest/HTTP_TaskSelectInterfacePage$', http_task.httpTestCaseSelectInterfaceCheckList,
        name="HTTP_TaskSelectInterfacePage"),
    url(r'^interfaceTest/HTTP_TaskSelectTestCasePage$', http_task.httpTaskSelectTestCaseCheckList,
        name="HTTP_TaskSelectTestCasePage"),
    url(r'^interfaceTest/HTTP_TaskAddData$', http_task.taskAddData, name="HTTP_TaskAddData"),
    url(r'^interfaceTest/HTTP_operationTask$', http_task.operationTask, name="HTTP_operationTask"),
    url(r'^interfaceTest/getTaskDataForId$', http_task.getTaskData, name="HTTP_taskGetTaskData"),
    url(r'^interfaceTest/HTTP_TaskSaveEdit$', http_task.taskDataSaveEdit, name="HTTP_TaskSaveEdit"),
    url(r'^interfaceTest/HTTP_TaskDel$', http_task.taskDel, name="HTTP_TaskDel"),
    url(r'^interfaceTest/HTTP_TaskDelTheSameCase$', http_task.taskDelTheSameCase, name="HTTP_TaskDelTheSameCase"),
    url(r'^interfaceTest/getInterfaceListDataForTask$', http_task.getInterfeceListDataForTask,
        name="getInterfaceListDataForTask"),
    url(r'^interfaceTest/getTestCaseListDataForTask$', http_task.getTestCaseListDataForTask,
        name="getTestCaseListDataForTask"),
    url(r'^interfaceTest/HTTP_TaskExecuteResult$', http_task.taskResultCheck, name="HTTP_TaskExecuteResult"),
    url(r'^interfaceTest/HTTP_TaskExecuteQueryPeopleTask$', http_task.queryPeopleTaskExecute,
        name="queryPeopleTaskExecute"),
    url(r'^interfaceTest/getTaskExecuteResult$', http_task.getTaskResultList, name="getTaskExecuteResult"),
    url(r'^interfaceTest/getTaskExecuteResultData$', http_task.getTaskRestltDetail, name="getTaskExecuteResultData"),
    url(r'^interfaceTest/getTaskExecuteId$', http_task.executeIdforTask, name="getTaskExecuteId"),
    url(r'^interfaceTest/getInterfaceListData$', http_task.getInterfeceListData, name="getInterfaceListData"),
    url(r'^interfaceTest/getTestCaseListData$', http_task.getTestCaseListData, name="getTestCaseListData"),
    url(r'^interfaceTest/HTTP_TaskAgainRunTask$', http_task.againRunTask, name="HTTP_TaskAgainRunTask"),
    url(r'^interfaceTest/HTTP_TaskStopTaskRun$', http_task.stopTaskRun, name="HTTP_TaskStopTaskRun"),
    url(r'^interfaceTest/HTTP_TaskRunTask$', http_task.taskRunAdd, name="HTTP_TaskRunTask"),
    url(r'^interfaceTest/HTTP_GetSelectExecuteStatus$', http_task.getSelectExecuteStatus,
        name="HTTP_GetSelectExecuteStatus"),
    # task从缓存获取数据
    url(r'^interfaceTest/HTTP_UpdateTaskExecuteProgressData$', http_task.updateTaskExecuteProgressData,name="HTTP_UpdateTaskExecuteProgressData"),


    #taskSuite
    url(r'^interfaceTest/HTTP_TaskSuiteCheck$', http_task_suite.httpTaskSuiteCheck, name="HTTP_taskSuiteCheck"),
    url(r'^interfaceTest/HTTP_TaskSuiteListCheck$', http_task_suite.http_taskSuiteListCheck, name="HTTP_TaskSuiteListCheck"),
    url(r'^interfaceTest/HTTP_TaskSuiteGetTaskSuiteForId$', http_task.getTaskForId, name="HTTP_TaskSuiteGetTaskSuiteForId"),
    url(r'^interfaceTest/HTTP_TaskSuiteAddPage$', http_task_suite.taskSuiteAdd, name="HTTP_TaskSuiteAddPage"),
    url(r'^interfaceTest/HTTP_TaskSuiteSelectTaskPage$', http_task_suite.httpTaskSuiteSelectTaskList,name="HTTP_TaskSuiteSelectTaskPage"),
    url(r'^interfaceTest/HTTP_TaskSuiteAddData$', http_task_suite.taskSuiteAddData, name="HTTP_TaskSuiteAddData"),
    url(r'^interfaceTest/HTTP_TaskSuiteSaveEdit$', http_task_suite.taskSuiteSaveEdit, name="HTTP_TaskSuiteSaveEdit"),
    url(r'^interfaceTest/HTTP_operationTaskSuite$', http_task_suite.operationTaskSuite, name="HTTP_operationTaskSuite"),
    url(r'^interfaceTest/getTaskSuiteDataForId$', http_task_suite.getTaskSuiteForId, name="HTTP_getTaskSuiteForId"),
    url(r'^interfaceTest/getTaskSuiteData$', http_task_suite.getTaskSuiteData, name="HTTP_taskSuiteGetTaskSuiteData"),
    url(r'^interfaceTest/HTTP_TaskSuiteDel$', http_task_suite.taskSuiteDel, name="HTTP_TaskSuiteDel"),
    url(r'^interfaceTest/getTaskListDataForTaskSuite$', http_task_suite.getTaskListDataForTaskSuite,
        name="getTaskListDataForTaskSuite"),
    url(r'^interfaceTest/HTTP_TaskSuiteExecuteResult$', http_task_suite.taskSuiteResultCheck, name="HTTP_TaskSuiteExecuteResult"),
    url(r'^interfaceTest/getTaskSuiteExecuteResult$', http_task_suite.getTaskSuiteResultList, name="HTTP_getTaskSuiteExecuteResult"),
    url(r'^interfaceTest/HTTP_UpdateTaskSuiteExecuteProgressData$', http_task_suite.updateTaskSuiteExecuteProgressData,
        name="HTTP_UpdateTaskSuiteExecuteProgressData"),
    url(r'^interfaceTest/HTTP_TaskSuiteRunTask$', http_task_suite.taskSuiteRunAdd, name="HTTP_TaskSuiteRunTask"),
    url(r'^interfaceTest/getTaskSuiteExecuteResultData$', http_task_suite.getTaskSuiteRestltDetail, name="getTaskSuiteExecuteResultData"),
    url(r'^interfaceTest/HTTP_TaskSuiteAgainRun$', http_task_suite.againRunTaskSuite, name="HTTP_TaskSuiteAgainRun"),
    url(r'^interfaceTest/HTTP_TaskStopTaskSuiteRun$', http_task_suite.stopTaskSuiteRun, name="HTTP_TaskStopTaskSuiteRun"),
    url(r'^interfaceTest/HTTP_TaskSuiteGetSelectExecuteStatus$', http_task_suite.getSelectExecuteStatus,
        name="HTTP_TaskSuiteGetSelectExecuteStatus"),

    # task 结果对比
    url(r'^interfaceTest/HTTP_ContrastTaskResult$', http_task.contrastTaskResult, name="HTTP_ContrastTaskResult"),
    url(r'^interfaceTest/HTTP_mergeTask$', http_task.mergeTask, name="HTTP_MergeTask"),
    # 历史统计
    url(r'^interfaceTest/HTTP_History$', http_history.http_historyCheck, name="HTTP_History"),
    url(r'^interfaceTest/HTTP_History_queryHistory$', http_history.queryHistory, name="HTTP_History_queryHistory"),
    url(r'^interfaceTest/HTTP_Statistics$', http_statistics.http_statisticsCheck, name="HTTP_Statistics"),
    url(r'^interfaceTest/HTTP_History_queryStatistics$', http_statistics.queryStatistics,
        name="HTTP_History_queryStatistics"),
    url(r'^interfaceTest/getHttpConf', http_conf.getHttpConf, name="getHttpConf"),
    # 全局变量
    url(r'^interfaceTest/HTTP_GlobalVarsConf$', global_vars_conf.globalVarsCheck, name="HTTP_GlobalVarsConf"),
    url(r'^interfaceTest/HTTP_GlobalVarsConfListPage$', global_vars_conf.queryVars, name="HTTP_GlobalVarsConfListPage"),
    url(r'^interfaceTest/HTTP_GlobalVarsAdd$', global_vars_conf.varsConfAdd, name="HTTP_GlobalVarsAdd"),
    url(r'^interfaceTest/HTTP_GlobalVarsDel$', global_vars_conf.varsConfDel, name="HTTP_GlobalVarsDel"),
    url(r'^interfaceTest/HTTP_GlobalVarsEdit$', global_vars_conf.varsConfEdit, name="HTTP_GlobalVarsEdit"),

    #获取单个全局变量
    url(r'^interfaceTest/HTTP_GlobalVarsGetForId$', global_vars_conf.getGlobalVarForVarKey, name="HTTP_GlobalVarsGetForId"),
    url(r'^interfaceTest/HTTP_GlobalVarsSetForId$', global_vars_conf.setGlobalVarForVarKey, name="HTTP_GlobalVarsSetForId"),

    # 组合文本
    url(r'^interfaceTest/HTTP_GlobalTextConf$', global_text_conf.globalTextCheck, name="HTTP_GlobalTextConf"),
    url(r'^interfaceTest/HTTP_GlobalTextConfListPage$', global_text_conf.queryText, name="HTTP_GlobalTextConfListPage"),
    url(r'^interfaceTest/HTTP_GlobalTextAdd$', global_text_conf.textConfAdd, name="HTTP_GlobalTextAdd"),
    url(r'^interfaceTest/HTTP_GlobalTextDel$', global_text_conf.textConfDel, name="HTTP_GlobalTextDel"),
    url(r'^interfaceTest/HTTP_GlobalTextEdit$', global_text_conf.textConfEdit, name="HTTP_GlobalTextEdit"),

    #获取单个组合文本
    url(r'^interfaceTest/HTTP_GlobalTextGetForId$', global_text_conf.getGlobalTextForVarKey, name="HTTP_GlobalTextGetForId"),
    url(r'^interfaceTest/HTTP_GlobalTextSetForId$', global_text_conf.setGlobalTextForVarKey, name="HTTP_GlobalTextSetForId"),

    # 数据service配置
    url(r'^interfaceTest/HTTP_UserServiceConf$', user_service_conf.userHttpConfCheck, name="HTTP_UserServiceConf"),
    url(r'^interfaceTest/HTTP_UserServiceConfListCheck$', user_service_conf.queryUserHttpConf,name="HTTP_UserServiceConfListCheck"),
    url(r'^interfaceTest/HTTP_UserServiceConfAddUserHttpConf$', user_service_conf.addUserHttpConf,name="HTTP_UserServiceConfAddUserHttpConf"),
    url(r'^interfaceTest/HTTP_ServiceConfAdd$', user_service_conf.httpConfAdd, name="HTTP_ServiceConfAdd"),
    url(r'^interfaceTest/HTTP_ServiceConfDel$', user_service_conf.delHttpConfKey, name="HTTP_ServiceConfDel"),
    url(r'^interfaceTest/HTTP_ServiceConfEdit$', user_service_conf.httpConfSaveEdit, name="HTTP_ServiceConfEdit"),

    # 环境配置
    url(r'^interfaceTest/HTTP_UserHttpConf$', user_http_conf.userHttpConfCheck, name="HTTP_UserHttpConf"),
    url(r'^interfaceTest/HTTP_UserHttpConfListCheck$', user_http_conf.queryUserHttpConf,
        name="HTTP_UserHttpConfListCheck"),
    url(r'^interfaceTest/HTTP_UserHttpConfAddUserHttpConf$', user_http_conf.addUserHttpConf,name="HTTP_UserHttpConfAddUserHttpConf"),
    url(r'^interfaceTest/HTTP_HttpConfAdd$', user_http_conf.httpConfAdd, name="HTTP_HttpConfAdd"),
    url(r'^interfaceTest/HTTP_HttpConfDel$', user_http_conf.delHttpConfKey, name="HTTP_HttpConfDel"),
    url(r'^interfaceTest/HTTP_HttpConfEdit$', user_http_conf.httpConfSaveEdit, name="HTTP_HttpConfEdit"),
    url(r'^interfaceTest/HTTP_delAllUserHttpConf$', user_http_conf.delAllUserHttpConf, name="HTTP_DelAllUserHttpConf"),
    #服务配置
    url(r'^interfaceTest/HTTP_UriConf$', user_uri_conf.userUriCheck, name="HTTP_UserUriConf"),
    url(r'^interfaceTest/HTTP_UserUriConfListCheck$', user_uri_conf.queryUserUriConf,name="HTTP_UserUriConfListCheck"),
    url(r'^interfaceTest/HTTP_UserAddUserUriSort$', user_uri_conf.addUserUriSort,name="HTTP_UserAddUserUriSort"),
    url(r'^interfaceTest/HTTP_HttpUriAddApply', user_uri_conf.addUserUriApply, name="HTTP_HttpUriAddApply"),
    url(r'^interfaceTest/HTTP_UriConfEdit', user_uri_conf.saveUriEdit, name="HTTP_UriConfEdit"),
    url(r'^interfaceTest/HTTP_UriConfDel', user_uri_conf.delUri, name="HTTP_UriConfDel"),

    # 环境服务配置
    url(r'^interfaceTest/HTTP_EnvUriConf$', user_uri_conf.userEnvUriCheck, name="HTTP_UserEnvUriConf"),
    url(r'^interfaceTest/HTTP_UserEnvUriConfListCheck$', user_uri_conf.queryUserEnvUriConf, name="HTTP_UserEnvUriConfListCheck"),
    url(r'^interfaceTest/HTTP_DelEnvUri', user_uri_conf.delEnvUri, name="HTTP_DelEnvUri"),
    url(r'^interfaceTest/HTTP_SaveEditEnvUri', user_uri_conf.saveEditEnvUri, name="HTTP_SaveEditEnvUri"),
    url(r'^interfaceTest/HTTP_saveEnvUri', user_uri_conf.saveEnvUri, name="HTTP_saveEnvUri"),

    url(r'^interfaceTest/HTTP_delAllUserUri$', user_uri_conf.delAllUserUri, name="HTTP_DelAllUserUri"),

    # token
    url(r'^interfaceTest/JenkinsPlugin$', user_token.jenkinsPlugin, name="JenkinsPluginPage"),
    url(r'^interfaceTest/HTTP_UserToken$', user_token.user_token, name="HTTP_UserToken"),
    url(r'^interfaceTest/HTTP_UserInvoke$', user_invoke.user_invoke, name="HTTP_UserInvoke"),
    url(r'^interfaceTest/HTTP_UserCI$', user_CI.user_CI, name="HTTP_UserCI"),
    url(r'^interfaceTest/HTTP_UserUpdateToken$', user_token.updateUserToken, name="HTTP_UserUpdateToken"),
    url(r'^interfaceTest/HTTP_GetVarsConf', global_vars_conf.getVarsConf, name="getVarsConf"),
    url(r'^interfaceTest/HTTP_GetTextConf', global_text_conf.getTextConf, name="getTextConf"),
    url(r'^interfaceTest/HTTP_getHttpConfData$', user_http_conf.getHttpConfData, name="getHttpConfData"),

    # 接口覆盖率
    url(r'^interfaceTest/HTTP_SrcFileAnalyze$', src_file.srcFileCheck, name="HTTP_SrcFileAnalyze"),
    url(r'^interfaceTest/HTTP_SrcFileAnalyzeList$', src_file.srcFileList, name="HTTP_SrcFileAnalyzeList"),
    url(r'^interfaceTest/HTTP_SrcFileRefresh$', src_file.refreshSrcFile, name="HTTP_SrcFileRefresh"),
    url(r'^GetAllInterfaceCount$', src_file.getAllInterfaceCounts, name="HTTP_GetAllSrcCount"),  # 获取所有的接口数量详情
    url(r'^GetAllApiCount$', src_file.getAllApiCountsNum, name="GetAllApiCount"),  # 获取所有的接口数量仅仅数量，没有详情
    url(r'^GenerateAllApi$', src_file.generateAllInterfacesByAnno, name="HTTP_GenerateAllInterfacesByAnno"),  # 生成所有接口详情

    url(r'^interfaceTest/HTTP_SrcTaskFileAnalyze$', src_task_file_cover.srcTaskFileCoverCheck,
        name="HTTP_SrcTaskFileAnalyze"),
    url(r'^interfaceTest/HTTP_SrcTaskFileAnalyzeList$', src_task_file_cover.srcTaskFileCoverList,
        name="HTTP_SrcTaskFileAnalyzeList"),
    url(r'^interfaceTest/GetTaskList$', src_task_file_cover.http_taskListCheck, name="GetTaskList"),
    url(r'^interfaceTest/HTTP_SrcFileCoverCheck$', src_file_cover.srcFileCoverCheck, name="HTTP_SrcFileCoverCheck"),
    url(r'^interfaceTest/HTTP_SrcFileCoverList$', src_file_cover.srcFileCoverList, name="HTTP_SrcFileCoverList"),
    url(r'^interfaceTest/PublicKeyDetails', public_key_details.PublicKeyDetails, name="PublicKeyDetails"),
    url(r'^readme$', public_key_details.ReadMeDetails, name="readme"),
    url(r'^pythonModeDetails$', public_key_details.pythonModeDetails, name="pythonModeDetails"),

    # 版本管理
    url(r'^versionManage/HTTP_CurrentVersion$', version_show.current_version, name="HTTP_CurrentVersion"),
    url(r'^versionManage/HTTP_HistoryVersion$', version_show.history_version, name="HTTP_HistoryVersion"),
    url(r'^versionManage/HTTP_ChangeVersion$', version_show.change_version, name="HTTP_ChangeVersion"),

    # 业务线 模块 联动
    url(r'^config/bmRelation$', businessLine_module_relation.getBusinessLineAndModuleRelation, name="bmRelation"),

    # 更新接口和用例的优先级的接口 不需要登录即可访问
    url(r'^updateLevel/updateInterfaceLevel$', http_interface.updateInterfaceLevel),
    url(r'^updateLevel/updateTestCaseLevel$', http_test_case.updateTestCaseLevel),

    # 根据域名获取uriKey
    url(r'^getUrikeyByConfigInfo$', http_interface.getUrikeyByUrihost, name="HTTP_getUrikeyByConfigInfo"),

    #postman 导入相关
    url(r'^interfaceTest/importPostmanPage$', http_interface.importPostmanPage, name="HTTP_importPostmanPage"),
    url(r'^interfaceTest/savePostmanDataToHttpInterface$', http_interface.savePostmanDataToHttpInterface, name="HTTP_savePostmanDataToHttpInterface"),

    #CICD展示页面
    url(r'^interfaceTest/HTTP_taskCICDCheck$', http_CICD_task.http_task_CICD_check, name="HTTP_TASK_CICD_CHECK"),
    url(r'^interfaceTest/HTTP_taskGetCICDSubPage$', http_CICD_task.http_task_get_CICD_sub_page, name="http_task_get_CICD_sub_page"),
    url(r'^interfaceTest/test$', http_CICD_task.test),


    url(r'^interfaceTest/page_404$', page_error.page_404),
    url(r'^interfaceTest/not_permission$', page_error.not_permission),

    url(r'^interfaceTest/importLogPage$', http_interface.importLogPage, name="HTTP_importLogPage"),
    url(r'^interfaceTest/saveLogDataToHttpInterfaces$', http_interface.saveLogDataToHttpInterfaces,name="HTTP_saveLogDataToHttpInterfaces"),

]