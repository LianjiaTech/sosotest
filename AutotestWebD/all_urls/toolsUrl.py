from django.conf.urls import url
from apps.deployment_tool.views import  deployment_tool


urlpatterns = [
    url(r'^tools/deployment$', deployment_tool.deploymentPage,name="deploymentPage"),
    url(r'^tools/initGetText$', deployment_tool.initGetText,name="initGetText"),
    url(r'^tools/doDeployment$', deployment_tool.doDeployment,name="doDeployment"),
    url(r'^tools/deploymentCallBack$', deployment_tool.deploymentCallBack),
    url(r'^tools/deploymentCheck$', deployment_tool.deploymentCheck,name="deploymentCheck"),
    url(r'^tools/deploymentListCheck$', deployment_tool.deploymentListCheck,name="deploymentListCheck"),
]