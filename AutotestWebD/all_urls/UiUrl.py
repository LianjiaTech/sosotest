from django.conf.urls import url
from apps.ui_test.views import ui_test,ui_test_result,ui_package,ui_show
from  apps.ui_task.views import ui_task_simple

urlpatterns = [
    url(r'^UITest$', ui_test.uiTestPage,name="UITest"),
    url(r'^userIsFileShowSubPage$', ui_test.userIsFileShowSubPage, name="userIsFileShowSubPage"),
    url(r'^createDir$', ui_test.createDir, name="createDir"),
    url(r'^fileExists$', ui_test.fileExists, name="fileExists"),
    url(r'^fileUpload$', ui_test.fileUpload, name="fileUpload"),
    url(r'^checkFileList$', ui_test.checkFileList, name="checkFileList"),
    url(r'^runTest$', ui_test.runTest, name="runTest"),
    url(r'^downLoadExcel$', ui_test.file_download, name="downLoadExcel"),
    url(r'^file_delete$', ui_test.file_delete, name="file_delete"),

    url(r'^uiTestResultPage$', ui_test_result.ui_test_result_page, name="uiTestResultPage"),
    url(r'^uiTestResultListCheck$', ui_test_result.ui_test_resultListCheck, name="uiTestResultListCheck"),
    #ui测试的
    url(r'^ui_report$', ui_test_result.ui_report, name="ui_report"),
    url(r'^cancelUiTask$', ui_test_result.cancelExecuteUiTask, name="cancelUiTask"),
    url(r'^checkUiTestLog$', ui_test_result.checkUiTestLog, name="checkUiTestLog"),
    url(r'^uiAddSimpleTaskPage$', ui_task_simple.uiAddSimpleTaskPage, name="uiAddSimpleTaskPage"),
    url(r'^uiSaveSimpleTask$', ui_task_simple.saveSimpleTask, name="uiSaveSimpleTask"),
    url(r'^uiShowSimpleTask$', ui_task_simple.show_ui_simple_task_page, name="uiShowSimpleTask"),
    url(r'^uiTaskShowresultListCheck$', ui_task_simple.show_ui_test_resultListCheck, name="uiTaskShowresultListCheck"),
    url(r'^uiSimpleTaskExecute$', ui_task_simple.executeSimpleTask, name="uiSimpleTaskExecute"),
    url(r'^ui_operationTask$', ui_task_simple.ui_operationTask, name="ui_operationTask"),
    url(r'^getTaskForTaskId$', ui_task_simple.getTaskForTaskId, name="getTaskForTaskId"),
    url(r'^uiDelSimpleTask$', ui_task_simple.delSimpleTask, name="uiDelSimpleTask"),
    url(r'^uiAgainRunTask$', ui_test_result.againRunTask, name="uiAgainRunTask"),
    url(r'^uiAppPackagePage$', ui_package.appPackagePage, name="uiAppPackagePage"),
    url(r'^appPackageIsExist$', ui_package.appPackageIsExist, name="appPackageIsExist"),
    url(r'^uiAppPackage$', ui_package.addPackage, name="uiAppPackage"),
    url(r'^uiAppPackageCheckPage$', ui_package.appPackageCheckPage, name="uiAppPackageCheckPage"),
    url(r'^uiAppPackageCheckSubPage$', ui_package.appPackageCheckSunPage, name="uiAppPackageCheckSubPage"),
    url(r'^uiAppPackageDel$', ui_package.delAppPackage, name="delAppPackage"),
    url(r'^editAppPackagePage$', ui_package.editAppPackagePage, name="editAppPackagePage"),
    url(r'^getAppPackage$', ui_package.getAppPackage, name="getAppPackage"),
    url(r'^saveEditAppPackage$', ui_package.saveEditAppPackage, name="saveEditAppPackage"),
    url(r'^uploadAPK$', ui_package.uploadAPK),
    url(r'^uploadAPP$', ui_package.uploadAPP),

    url(r'^ui/showTaskExecuteProgressing$', ui_show.uiShowProgressing, name="ui_showTaskExecuteProgressing"),
    url(r'^ui/showUiTaskProgressIndex$', ui_show.uiShowPorgressIndex, name="ui_showUiTaskProgressIndex"),
    url(r'^ui/showUiTaskProgressData$', ui_show.uiGetTaskProgressData, name="ui_uiGetTaskProgressData"),

    url(r'^ui/UITaskGetTaskFotTaskId$', ui_task_simple.getTaskRunDetailsForTaskId, name="UITaskGetTaskFotTaskId"),
    url(r'^ui/addPageObject$', ui_task_simple.addPageObject, name="addPageObject"),
    url(r'^ui/getPageObject$', ui_task_simple.getPageObject, name="getPageObject"),
    url(r'^ui/getPageObjectForId$', ui_task_simple.getPageObjectForId, name="getPageObjectForId"),
    url(r'^ui/editPageObject$', ui_task_simple.editPageObject, name="editPageObject"),
    url(r'^ui/delPageObject$', ui_task_simple.delPageObject, name="delPageObject"),
    url(r'^ui/resetPageObject$', ui_task_simple.resetPageObject, name="resetPageObject"),
]