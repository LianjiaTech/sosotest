from django.conf.urls import url
from apps.mock_server.views import http_server
from apps.mock_server.views import http_interface

urlpatterns = [
    url(r'^mock/([\w\-\.]+)/([\w\-\.]+)/([\w\-\.]+)([\w\-\.\/]+)$', http_server.mock),
    url(r'^mockserver/readme$', http_server.readme, name="MOCK_HTTP_readme"),

    #add page
    url(r'^mockserver/HTTP_InterfaceCheck$', http_interface.http_interfaceCheck, name="MOCK_HTTP_InterfaceCheck"),
    url(r'^mockserver/HTTP_InterfaceAddPage$', http_interface.interfaceAddPage, name="MOCK_HTTP_InterfaceAddPage"),
    url(r'^mockserver/HTTP_InterfaceAdd$', http_interface.interfaceAdd, name="MOCK_HTTP_InterfaceAdd"),

    #chakan page
    url(r'^mockserver/HTTP_InterfaceListCheck$', http_interface.http_interfaceListCheck, name="MOCK_HTTP_InterfaceListCheck"),
    url(r'^mockserver/HTTP_InterfaceDel$', http_interface.interfaceDel, name="MOCK_HTTP_InterfaceDel"),
    url(r'^mockserver/HTTP_operationInterface$', http_interface.operationInterface, name="MOCK_HTTP_operationInterface"),
    url(r'^mockserver/HTTP_getInterfaceDataForId$', http_interface.getInterfaceDataForId,name="MOCK_getInterfaceDataForId"),
    url(r'^mockserver/HTTP_InterfaceSaveEdit$', http_interface.interfaceSaveEdit, name="MOCK_HTTP_InterfaceSaveEdit"),
    url(r'^mockserver/RunContrackTask$', http_interface.runContrackTask, name="MOCK_RunContrackTask"),
    url(r'^mockserver/getContrackTaskRecentExecInfos$', http_interface.getContrackTaskRecentExecInfos, name="MOCK_getContrackTaskRecentExecInfos"),
    url(r'^mockserver/follow$', http_interface.follow, name="MOCK_follow"),
]