from django.conf.urls import url
from django.contrib import admin
from apps.webportal.views import WebPortalViews, updateWebPortal, getEnvVersion, webPortalAction

urlpatterns = [
    url(r'^webportal$', WebPortalViews.mainPage),
    url(r'^webportal/httpTestPage$', WebPortalViews.httpTestSubPage),
    url(r'^webportal/unitTestPage$', WebPortalViews.unitTestSubPage),
    url(r'^webportal/rmiTestPage$', WebPortalViews.rmiTestSubPage),
    url(r'^webportal/uiTestPage$', WebPortalViews.uiTestSubPage),
    url(r'^webportal/openApiTestPage$', WebPortalViews.openApiTestSubPage),
    url(r'^webportal/updateWebPortalData$', updateWebPortal.updateWebPortalData),
    url(r'^webportal/getEnvVersion$', getEnvVersion.getEnvVersion),
    url(r'^webportal/invokeGetEnvVersion$', getEnvVersion.invokeGetEnvVersion),
    url(r'^webportal/lineGraph$', WebPortalViews.lineGraph),
    url(r'^webportal/updateTaskToCurrentVersion$', updateWebPortal.updateTaskToCurrentVersion),
    url(r'^webportal/getAllEnv$', WebPortalViews.getAllEnv),
    url(r'^webportal/getEnvVersionRelation$', WebPortalViews.getEnvVersionRelation),
    url(r'^webportal/getRecentSevenDays$', WebPortalViews.getRecentSevenDays),
    url(r'^webportal/getAllPassRate$', WebPortalViews.getAllPassRate),
    url(r'^webportal/getAllHttpConf$', WebPortalViews.getAllHttpConf),
    url(r'^webportal/getRencentDays$', WebPortalViews.getRencentDays),
    url(r'^webportal/getBusinessLinesActionPassRate$', WebPortalViews.getBusinessLinesActionPassRate),
    url(r'^webportal/getBusinessLineNameId$', WebPortalViews.getBusinessLineNameId),
    url(r'^webportal/httpTestCoveragePage$', WebPortalViews.httpTestCoverageSubPage)


]