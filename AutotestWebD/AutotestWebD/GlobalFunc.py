from AutotestWebD.settings import *
def menu(request):
    menuGroup = ""
    httpGroupUrlList = [
        "/interfaceTest/HTTP_InterfaceCheck",
        "/interfaceTest/HTTP_InterfaceAddPage",
        "/interfaceTest/importPostmanPage",
        "/interfaceTest/HTTP_TestCaseCheck",
        "/interfaceTest/HTTP_TestCaseStepCheck",
        "/interfaceTest/HTTP_TestCaseAddPage",
        "/interfaceTest/HTTP_TaskCheck",
        "/interfaceTest/HTTP_TaskAddPage",
        "/interfaceTest/HTTP_TaskSuiteCheck",
        "/interfaceTest/HTTP_TaskSuiteAddPage",
        "/interfaceTest/HTTP_TaskExecuteResult",
        "/interfaceTest/HTTP_TaskSuiteExecuteResult",
        "/interfaceTest/HTTP_History",
        "/interfaceTest/HTTP_Statistics",
        "/interfaceTest/HTTP_operationInterface",
        "/interfaceTest/HTTP_operationTestCase",
        "/interfaceTest/importLogPage",
        "/interfaceTest/HTTP_operationTask",
        "/interfaceTest/HTTP_operationTaskSuite",
    ]
    dubboGroupUrlList = [
        "/dubbo/interfaceList",
        "/dubbo/interfaceAddPage",
        "/dubbo/testcaseList",
        "/dubbo/testCaseAddPage",
        "/dubbo/TaskCheck",
        "/dubbo/TaskAddPage",
        "/dubbo/TaskSuiteCheck",
        "/dubbo/TaskSuiteAddPage",
        "/dubbo/TaskExecuteResult",
        "/dubbo/TaskSuiteExecuteResult",
        "/dubbo/quickDebugPage",
        "/dubbo/operationInterface",
        "/dubbo/operationTestCase",
        "/dubbo/importLogPage",
        "/dubbo/operationTask",
        "/dubbo/operationTaskSuite",
    ]
    dataGroupUrlList = [
        "/mockserver/HTTP_InterfaceCheck",
        "/mockserver/HTTP_InterfaceAddPage",
        "/mockserver/readme",
        "/statistictask/execlistPage",
        "/statistictask/addPage",
        "/statistictask/listPage",
        "/mockserver/HTTP_operationInterface",
        "/statistictask/operationCheck",
        "/interfaceTest/HTTP_GlobalVarsConf",
        "/interfaceTest/HTTP_GlobalTextConf",
        "/datakeyword/listPage",
        "/datakeyword/addPage",
        "/datakeyword/operationCheck",
    ]
    configGroupUrlList = [
        "/interfaceTest/HTTP_EnvUriConf",
        "/interfaceTest/HTTP_UserHttpConf",
        "/interfaceTest/HTTP_UriConf",
        "/interfaceTest/HTTP_UserServiceConf",
        "/interfaceTest/HTTP_UserCI",
        "/interfaceTest/HTTP_UserToken",
        "/interfaceTest/HTTP_UserInvoke",
        "/interfaceTest/JenkinsPlugin",
        "/versionManage/HTTP_CurrentVersion",
        "/versionManage/HTTP_HistoryVersion",
    ]
    uiGroupUrlList = [
        "/uiShowSimpleTask",
        "/UITest",
        "/uiAddSimpleTaskPage",
        "/uiTestResultPage",
        "/uiAppPackageCheckPage",
        "/uiAppPackagePage",
        "/ui/pageObjectAddIndex",
    ]
    url = request.META.get("PATH_INFO")
    if url in httpGroupUrlList:
        menuGroup = "HTTP_TEST"
    elif url in dubboGroupUrlList:
        menuGroup = "DUBBO_TEST"
    elif url in dataGroupUrlList:
        menuGroup = "DATA_SERVICE"
    elif url in configGroupUrlList:
        menuGroup = "CONFIG"
    elif url in uiGroupUrlList:
        menuGroup = "UI_TEST"


    return {"menu":showMenuConfig,"deployment_tool":deployment_tool_insettings,"menuGroup":menuGroup}

def site(request):
    return {"site_name":SITE_NAME,"static_version":STATIC_VERSION,
            "groupLevel1":groupLevel1,"groupLevel2":groupLevel2,
            "isReleaseEnv":isRelease}
