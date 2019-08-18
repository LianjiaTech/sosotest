from django.conf.urls import url
from apps.data_keyword.views import main_view

urlpatterns = [
    #add page
    url(r'^datakeyword/listPage$', main_view.listPage, name="DATAKEYWORD_listPage"),
    url(r'^datakeyword/addPage$', main_view.addPage, name="DATAKEYWORD_addPage"),
    url(r'^datakeyword/addData$', main_view.addData, name="DATAKEYWORD_addData"),

    #chakan page
    url(r'^datakeyword/listData$', main_view.listData, name="DATAKEYWORD_listData"),
    url(r'^datakeyword/delData$', main_view.delData, name="DATAKEYWORD_delData"),
    url(r'^datakeyword/operationCheck$', main_view.operationCheck, name="DATAKEYWORD_operationCheck"),
    url(r'^datakeyword/operationCheckByKey$', main_view.operationCheckByKey, name="DATAKEYWORD_operationCheckByKey$"),

    url(r'^datakeyword/getDataById$', main_view.getDataById,name="DATAKEYWORD_getDataById"),
    url(r'^datakeyword/saveEditData$', main_view.saveEditData, name="DATAKEYWORD_saveEditData"),
]