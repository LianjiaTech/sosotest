from django.conf.urls import url
from apps.statistic_task.views import main_view,statistic_view

urlpatterns = [
    #add page
    url(r'^statistictask/listPage$', main_view.listPage, name="statistictask_listPage"),
    url(r'^statistictask/execlistPage$', main_view.executeListPage, name="statistictask_execlistPage"),
    url(r'^statistictask/addPage$', main_view.addPage, name="statistictask_addPage"),
    url(r'^statistictask/addData$', main_view.addData, name="statistictask_addData"),

    #chakan page
    url(r'^statistictask/listData$', main_view.listData, name="statistictask_listData"),
    url(r'^statistictask/execlistData$', main_view.executeListData, name="statistictask_execlistData"),
    url(r'^statistictask/delData$', main_view.delData, name="statistictask_delData"),
    url(r'^statistictask/operationCheck$', main_view.operationCheck, name="statistictask_operationCheck"),
    url(r'^statistictask/getDataById$', main_view.getDataById,name="statistictask_getDataById"),
    url(r'^statistictask/saveEditData$', main_view.saveEditData, name="statistictask_saveEditData"),

    url(r'^statistictask/setReason$', main_view.setReason, name="statistictask_execSetReason"),
    url(r'^statistictask/operationExecCheck$', main_view.operationExecCheck, name="statistictask_operationExecCheck"),

    #统计接口
    url(r'^statistic/alltask$', statistic_view.getStatisticForAllTask, name="statistic_data_getStatisticAllTask"),

]