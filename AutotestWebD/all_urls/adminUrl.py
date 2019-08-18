from django.conf.urls import url

from apps.myadmin.views import login, user, team, role,  teamUserRelation, userRole, adminUser, businessLine, \
    interfaceModule, interfacePermission, moduleManage, source, changeLog, businessLineModule, configService, \
    jiraModule, modulePlatform, jiraBusinessLine, jiraBusinessLinePlatform, configUri, configHttp, httpInterfaceDebug, \
    httpTestcaseDebug, exePython, standardTask, openApiBusinessLine, openApiUri, unitTestService, uiMobileServer, \
    versionManage, userLog, adminManagePermission, standardEnv, cacheManage, webportalBusinessLine, dataStorage,adminServiceConf

'''url规则：myadmin/***/check， 中间件会过滤中间的module'''
urlpatterns = [
    url(r'^myadmin/$', login.loginPage, name="admin_login"),
    url(r'^myadmin/login$', login.loginPage,name="admin_login"),
    url(r'^myadmin/doLogin$', login.doLogin,name="admin_doLogin"),
    url(r'^myadmin/changePassword$', login.changePassword, name="admin_changePassword"),
    url(r'^myadmin/logout$', login.logout, name="admin_logout"),
    url(r'^myadmin/home$', login.home, name="admin_home"),

    #user
    url(r'^myadmin/user/check$', user.userCheckPage, name="admin_user_check"),
    url(r'^myadmin/user/getUserSubPage$', user.getUser, name="admin_user_get_user_sub_page"),
    url(r'^myadmin/user/addUser$', user.addUser, name="admin_add_user"),
    url(r'^myadmin/user/getUserForId$', user.getUserForId, name="getUserForId"),
    url(r'^myadmin/user/editUser$', user.editUser, name="admin_edit_user"),
    url(r'^myadmin/user/delUser$', user.delUser, name="admin_del_user"),
    url(r'^myadmin/user/addPermissionsToUser$', user.addPermissionsToUser, name="admin_add_permissions_to_user"),
    url(r'^myadmin/user/addPermissionsToAllUsers$', user.addPermissionsToAllUsers, name="admin_add_permissions_to_all_users"),
    url(r'^myadmin/interfacePermission/getUserPermissionKeys$', user.getUserPermission),

    #team
    url(r'^myadmin/team/check$', team.teamCheckPage, name="admin_team_check"),
    url(r'^myadmin/team/getTeamSubPage$', team.getTeam, name="admin_team_get_team_sub_page"),
    url(r'^myadmin/team/addTeam$', team.addTeam, name="admin_add_Team"),
    url(r'^myadmin/team/getTeamForId$', team.getTeamForId, name="getTeamForId"),
    url(r'^myadmin/team/editTeam$', team.editTeam, name="admin_edit_team"),
    url(r'^myadmin/team/delTeam$', team.delTeam, name="admin_del_team"),
    url(r'^myadmin/team/resetTeam$', team.resetTeam, name="admin_reset_team"),
    url(r'^myadmin/team/getAllUsers$', team.getAllUsers, name="admin_get_all_users"),
    url(r'^myadmin/team/addUsersToTeam$', team.addUsersToTeam, name="admin_add_users_to_team"),
    url(r'^myadmin/team/getAllSelectedUsers$', team.getAllSelectedUsers, name="admin_get_all_selected_users"),
    url(r'^myadmin/team/deleteSelectedUsers$', team.deleteSelectedUsers, name="admin_delete_selected_users"),
    url(r'^myadmin/team/addPermissionsToTeam$', team.addPermissionsToTeam, name="admin_add_permissions_to_team"),
    url(r'^myadmin/team/getTeammates$', team.getTeammates, name="admin_get_teammates"),
    url(r'^myadmin/team/tansferData$', team.tansferData, name="admin_tansferData"),
    url(r'^myadmin/interfacePermission/getTeamPermissionKeys$', team.getTeamPermission),
    url(r'^myadmin/interfacePermission/reload$', team.permissionReload),

    #role
    url(r'^myadmin/role/check$', role.roleCheckPage, name="admin_role_check"),
    url(r'^myadmin/role/getRoleSubPage$', role.getRole, name="admin_role_get_role_sub_page"),
    url(r'^myadmin/role/addRole$', role.addRole, name="admin_add_Role"),
    url(r'^myadmin/role/getRoleForId$', role.getRoleForId, name="getRoleForId"),
    url(r'^myadmin/role/editRole$', role.editRole, name="admin_edit_role"),
    url(r'^myadmin/role/delRole$', role.delRole, name="admin_del_role"),
    url(r'^myadmin/role/resetRole$', role.resetRole, name="admin_reset_role"),
    url(r'^myadmin/role/addUsersToRole$', role.addUsersToRole, name="admin_add_user_to_role"),

    #adminManagePermission
    url(r'^myadmin/adminManagePermission/check$', adminManagePermission.permissionCheckPage, name="admin_adminManagePermission_check"),
    url(r'^myadmin/adminManagePermission/getPermissionSubPage$', adminManagePermission.getPermission, name="admin_permission_get_permission_sub_page"),
    url(r'^myadmin/adminManagePermission/addPermission$', adminManagePermission.addPermission, name="admin_add_Permission"),
    url(r'^myadmin/adminManagePermission/getPermissionForId$', adminManagePermission.getPermissionForId, name="getPermissionForId"),
    url(r'^myadmin/adminManagePermission/editPermission$', adminManagePermission.editPermission, name="admin_edit_permission"),
    url(r'^myadmin/adminManagePermission/delPermission$', adminManagePermission.delPermission, name="admin_del_permission"),
    url(r'^myadmin/adminManagePermission/resetPermission$', adminManagePermission.resetPermission, name="admin_reset_permission"),
    url(r'^myadmin/adminManagePermission/getAllPermissions$', adminManagePermission.getAllPermissions, name="admin_get_all_permissions"),
    url(r'^myadmin/adminManagePermission/getAllSelectedPermissions$', adminManagePermission.getAllSelectedPermissions, name="admin_get_all_selected_permissions"),
    url(r'^myadmin/adminManagePermission/getAllSelectedTeamPermissions$', adminManagePermission.getAllSelectedTeamPermissions, name="admin_get_all_selected_team_permissions"),
    url(r'^myadmin/adminManagePermission/getAllUsersSelectedPermissions$', adminManagePermission.getAllUsersSelectedPermissions, name="admin_get_all_users_selected_team_permissions"),

    #teamUser
    url(r'^myadmin/team/getTeammateSubPage$', teamUserRelation.getAllTeammates, name="admin_team_get_teammate_sub_page"),

    #userRole
    url(r'^myadmin/userRole/userRoleCheckPage$', userRole.userRoleCheckPage, name="admin_user_role_check_page"),
    url(r'^myadmin/userRole/getUserRoleSubPage$', userRole.getUserRole, name="admin_team_get_team_sub_page"),
    url(r'^myadmin/userRole/setTeamLeader$', userRole.setTeamLeader, name="admin_set_team_leader"),
    url(r'^myadmin/userRole/delTeamLeader$', userRole.delTeamLeader, name="admin_del_team_leader"),

    #adminUser
    url(r'^myadmin/admin/check$', adminUser.adminUserCheckPage, name="admin_admin_user_check"),
    url(r'^myadmin/admin/getAdminUserSubPage$', adminUser.getAdminUser, name="admin_get_admin_user_sub_page"),
    url(r'^myadmin/admin/addAdminUser$', adminUser.addAdminUser, name="admin_add_adminUser"),
    url(r'^myadmin/admin/getAdminUserForId$', adminUser.getAdminUserForId, name="admin_get_adminUser_for_id"),
    url(r'^myadmin/admin/editAdminUser$', adminUser.editAdminUser, name="admin_edit_adminUser"),
    url(r'^myadmin/admin/delAdminUser$', adminUser.delAdminUser, name="admin_del_adminUser"),
    url(r'^myadmin/admin/resetAdminUser$', adminUser.resetAdminUser, name="admin_reset_adminUser"),
    url(r'^myadmin/admin/addPermissionsToUser$', adminUser.addPermissionsToUser, name="admin_add_permissions_to_user"),

    #businessLine
    url(r'^myadmin/businessLine/check$', businessLine.businessLineCheckPage, name="admin_business_line_check"),
    url(r'^myadmin/businessLine/getBusinessLineSubPage$', businessLine.getBusinessLine, name="admin_get_business_line_sub_page"),
    url(r'^myadmin/businessLine/addBusinessLine$', businessLine.addBusinessLine, name="admin_add_business_line"),
    url(r'^myadmin/businessLine/getBusinessLineForId$', businessLine.getBusinessLineForId, name="admin_get_businessLine_for_id"),
    url(r'^myadmin/businessLine/editBusinessLine$', businessLine.editBusinessLine, name="admin_edit_businessLine"),
    url(r'^myadmin/businessLine/delBusinessLine$', businessLine.delBusinessLine, name="admin_del_businessLine"),
    url(r'^myadmin/businessLine/resetBusinessLine$', businessLine.resetBusinessLine, name="admin_reset_businessLine"),

    # webportalBusinessLine
    url(r'^myadmin/webportalBusinessLine/check$', webportalBusinessLine.businessLineCheckPage, name="admin_webportalBusinessLine_line_check"),
    url(r'^myadmin/webportalBusinessLine/getBusinessLineSubPage$', webportalBusinessLine.getBusinessLine, name="admin_get_webportalBusinessLine_line_sub_page"),
    url(r'^myadmin/webportalBusinessLine/addBusinessLine$', webportalBusinessLine.addBusinessLine, name="admin_add_webportalBusinessLine_line"),
    url(r'^myadmin/webportalBusinessLine/getBusinessLineForId$', webportalBusinessLine.getBusinessLineForId, name="admin_get_webportalBusinessLine_for_id"),
    url(r'^myadmin/webportalBusinessLine/editBusinessLine$', webportalBusinessLine.editBusinessLine, name="admin_edit_webportalBusinessLine"),
    url(r'^myadmin/webportalBusinessLine/delBusinessLine$', webportalBusinessLine.delBusinessLine, name="admin_del_webportalBusinessLine"),
    url(r'^myadmin/webportalBusinessLine/resetBusinessLine$', webportalBusinessLine.resetBusinessLine, name="admin_reset_webportalBusinessLine"),
    url(r'^myadmin/webportalBusinessLine/getAllBusinessLines$', webportalBusinessLine.getAllBusinessLines, name="admin_get_allBusinessLines"),

    
    #interfaceModule
    # url(r'^myadmin/interfaceModule/check$', interfaceModule.interfaceModuleCheckPage, name="admin_interface_module_check"),
    # url(r'^myadmin/interfaceModule/getInterfaceModuleSubPage$', interfaceModule.getInterfaceModule, name="admin_get_interface_module_sub_page"),
    # url(r'^myadmin/interfaceModule/addInterfaceModule$', interfaceModule.addInterfaceModule, name="admin_add_interface_module"),
    # url(r'^myadmin/interfaceModule/getInterfaceModuleForId$', interfaceModule.getInterfaceModuleForId, name="admin_get_interface_module_for_id"),
    # url(r'^myadmin/interfaceModule/editInterfaceModule$', interfaceModule.editInterfaceModule, name="admin_edit_interfaceModule"),
    # url(r'^myadmin/interfaceModule/delInterfaceModule$', interfaceModule.delInterfaceModule, name="admin_del_interfaceModule"),
    # url(r'^myadmin/interfaceModule/resetInterfaceModule$', interfaceModule.resetInterfaceModule, name="admin_reset_interfaceModule"),

    #interfacePermission
    url(r'^myadmin/interfacePermission/check$', interfacePermission.interfacePermissionCheckPage, name="admin_interface_permission_check"),
    url(r'^myadmin/interfacePermission/getInterfacePermissionSubPage$', interfacePermission.getInterfacePermission, name="admin_get_interface_permission_sub_page"),
    url(r'^myadmin/interfacePermission/addInterfacePermission$', interfacePermission.addInterfacePermission, name="admin_add_interface_permission"),
    url(r'^myadmin/interfacePermission/getInterfacePermissionForId$', interfacePermission.getInterfacePermissionForId, name="admin_get_interface_permission_for_id"),
    url(r'^myadmin/interfacePermission/editInterfacePermission$', interfacePermission.editInterfacePermission, name="admin_edit_interfacePermission"),
    url(r'^myadmin/interfacePermission/delInterfacePermission$', interfacePermission.delInterfacePermission, name="admin_del_interfacePermission"),
    url(r'^myadmin/interfacePermission/resetInterfacePermission$', interfacePermission.resetInterfacePermission, name="admin_del_interfacePermission"),
    # url(r'^myadmin/interfacePermission/getAllInterface$', interfacePermission.getAllInterface, name="admin_get_allInterface"),
    url(r'^myadmin/interfacePermission/getAllPermissionKeys$', interfacePermission.getAllPermissionKeys, name="admin_get_allPermissionKeys"),

    #module
    url(r'^myadmin/moduleManage/check$', moduleManage.moduleManageCheckPage, name="admin_module_manage_check"),
    url(r'^myadmin/moduleManage/getModuleManageSubPage$', moduleManage.getModuleManage, name="admin_get_module_manage_sub_page"),
    url(r'^myadmin/moduleManage/addModuleManage$', moduleManage.addModuleManage, name="admin_add_module_manage"),
    url(r'^myadmin/moduleManage/getModuleManageForId$', moduleManage.getModuleManageForId, name="admin_get_module_manage_for_id"),
    url(r'^myadmin/moduleManage/editModuleManage$', moduleManage.editModuleManage, name="admin_edit_moduleManage"),
    url(r'^myadmin/moduleManage/delModuleManage$', moduleManage.delModuleManage, name="admin_del_moduleManage"),
    url(r'^myadmin/moduleManage/resetModuleManage$', moduleManage.resetModuleManage, name="admin_del_moduleManage"),

    # source
    url(r'^myadmin/source/check$', source.sourceCheckPage, name="admin_source_check"),
    url(r'^myadmin/source/getSourceSubPage$', source.getSource, name="admin_get_source_sub_page"),
    url(r'^myadmin/source/addSource$', source.addSource, name="admin_add_source"),
    url(r'^myadmin/source/getSourceForId$', source.getSourceForId, name="admin_get_source_for_id"),
    url(r'^myadmin/source/editSource$', source.editSource, name="admin_edit_source"),
    url(r'^myadmin/source/delSource$', source.delSource, name="admin_del_source"),
    url(r'^myadmin/source/resetSource$', source.resetSource, name="admin_reset_source"),

    #changeLog
    url(r'^myadmin/changeLog/check$', changeLog.changeLogCheckPage, name="admin_changeLog_check"),
    url(r'^myadmin/changeLog/getChangeLogSubPage$', changeLog.getChangeLog, name="admin_get_changeLog_sub_page"),
    url(r'^myadmin/changeLog/getChangeLogDataForId$', changeLog.getChangeLogDataForId, name="admin_get_changeLogData_for_id"),

    #businessLineModule
    url(r'^myadmin/businessLineModule/check$', businessLineModule.businessLineModuleCheckPage, name="admin_businessLine_module_check"),
    url(r'^myadmin/businessLineModule/getBusinessLineModule$', businessLineModule.getBusinessLineModule, name="admin_get_businessLine_module"),
    url(r'^myadmin/businessLineModule/addBusinessLineModule$', businessLineModule.addBusinessLineModule, name="admin_add_businessLine_module"),
    url(r'^myadmin/businessLineModule/getAllBusinessLines$', businessLineModule.getAllBusinessLines, name="admin_get_all_businessLine"),
    url(r'^myadmin/businessLineModule/getAllModuleNames$', businessLineModule.getAllModuleNames, name="admin_get_all_moduleNames"),
    url(r'^myadmin/businessLineModule/getBusinessLineModuleForId$', businessLineModule.getBusinessLineModuleForId, name="admin_get_businessLineModule_for_id"),
    url(r'^myadmin/businessLineModule/delBusinessLineModule$', businessLineModule.delBusinessLineModule, name="admin_del_businessLineModule"),
    url(r'^myadmin/businessLineModule/editBusinessLineModule$', businessLineModule.editBusinessLineModule, name="admin_edit_businessLineModule"),
    url(r'^myadmin/businessLineModule/getBusinessLineId$', businessLineModule.getBusinessLineId, name="admin_get_businessLineId"),
    url(r'^myadmin/businessLineModule/getModuleId$', businessLineModule.getModuleId, name="admin_get_moduleId"),

    #configService
    url(r'^myadmin/configService/check$', configService.configServiceCheckPage, name="admin_configService_check"),
    url(r'^myadmin/configService/getConfigServiceSubPage$', configService.getConfigService, name="admin_get_configService_sub_page"),
    url(r'^myadmin/configService/addConfigService$', configService.addConfigService, name="admin_add_configService"),
    url(r'^myadmin/configService/getConfigServiceForId$', configService.getConfigServiceForId, name="admin_get_configService_for_id"),
    url(r'^myadmin/configService/editConfigService$', configService.editConfigService, name="admin_get_configService_for_id"),
    url(r'^myadmin/configService/delConfigService$', configService.delConfigService, name="admin_del_configService"),
    url(r'^myadmin/configService/resetConfigService$', configService.resetConfigService, name="admin_reset_configService"),

    # configUri
    url(r'^myadmin/configUri/check$', configUri.configUriCheckPage, name="admin_configURI_check"),
    url(r'^myadmin/configUri/getConfigUriSubPage$', configUri.getConfigUri, name="admin_get_configUri_sub_page"),
    url(r'^myadmin/configUri/addConfigUri$', configUri.addConfigUri, name="admin_add_configUri"),
    url(r'^myadmin/configUri/getConfigUriForId$', configUri.getConfigUriForId, name="admin_get_configUri_for_id"),
    url(r'^myadmin/configUri/editConfigUri$', configUri.editConfigUri, name="admin_edit_configUri"),
    url(r'^myadmin/configUri/delConfigUri$', configUri.delConfigUri, name="admin_del_configUri"),
    url(r'^myadmin/configUri/resetConfigUri$', configUri.resetConfigUri, name="admin_reset_configUri"),

    #jiraModule
    url(r'^myadmin/jiraModule/check$', jiraModule.jiraModuleCheckPage, name="admin_jiraModule_check"),
    url(r'^myadmin/jiraModule/getJiraModuleSubPage$', jiraModule.getJiraModule, name="admin_get_jiraModule_sub_page"),
    url(r'^myadmin/jiraModule/addJiraModule$', jiraModule.addJiraModule, name="admin_add_jiraModule"),
    url(r'^myadmin/jiraModule/getJiraModuleForId$', jiraModule.getJiraModuleForId, name="admin_get_jiraModule_for_id"),
    url(r'^myadmin/jiraModule/editJiraModule$', jiraModule.editJiraModule, name="admin_get_jiraModule_for_id"),
    url(r'^myadmin/jiraModule/delJiraModule$', jiraModule.delJiraModule, name="admin_del_jiraModule"),
    url(r'^myadmin/jiraModule/resetJiraModule$', jiraModule.resetJiraModule, name="admin_reset_jiraModule"),

    #modulePlatform
    url(r'^myadmin/modulePlatform/check$', modulePlatform.modulePlatformCheckPage, name="admin_modulePlatform_check"),
    url(r'^myadmin/modulePlatform/getModulePlatform$', modulePlatform.getModulePlatform, name="admin_get_modulePlatform_sub_page"),
    url(r'^myadmin/modulePlatform/getAllJiraModules$', modulePlatform.getAllJiraModules, name="admin_get_all_jiraModules"),
    url(r'^myadmin/modulePlatform/addModulePlatform$', modulePlatform.addModulePlatform, name="admin_add_modulePlatform"),
    url(r'^myadmin/modulePlatform/getModulePlatformForId$', modulePlatform.getModulePlatformForId, name="admin_get_modulePlatform_for_id"),
    url(r'^myadmin/modulePlatform/editModulePlatform$', modulePlatform.editModulePlatform, name="admin_edit_modulePlatform"),
    url(r'^myadmin/modulePlatform/deleteModulePlatform$', modulePlatform.deleteModulePlatform, name="admin_del_modulePlatform"),
    url(r'^myadmin/modulePlatform/getJiraModuleId$', modulePlatform.getJiraModuleId, name="admin_get_jiraModuleId"),
    url(r'^myadmin/modulePlatform/getModuleId$', modulePlatform.getModuleId, name="admin_get_moduleId"),

    #jiraBusinessLine
    url(r'^myadmin/jiraBusinessLine/check$', jiraBusinessLine.jiraBusinessLineCheckPage, name="admin_jiraBusinessLine_check"),
    url(r'^myadmin/jiraBusinessLine/getJiraBusinessLineSubPage$', jiraBusinessLine.getJiraBusinessLine, name="admin_get_jiraBusinessLine_sub_page"),
    url(r'^myadmin/jiraBusinessLine/addJiraBusinessLine$', jiraBusinessLine.addJiraBusinessLine, name="admin_add_jiraBusinessLine"),
    url(r'^myadmin/jiraBusinessLine/getJiraBusinessLineForId$', jiraBusinessLine.getJiraBusinessLineForId, name="admin_get_jiraBusinessLine_for_id"),
    url(r'^myadmin/jiraBusinessLine/editJiraBusinessLine$', jiraBusinessLine.editJiraBusinessLine, name="admin_edit_jiraBusinessLine_for_id"),
    url(r'^myadmin/jiraBusinessLine/delJiraBusinessLine$', jiraBusinessLine.delJiraBusinessLine, name="admin_del_jiraBusinessLine"),
    url(r'^myadmin/jiraBusinessLine/resetJiraBusinessLine$', jiraBusinessLine.resetJiraBusinessLine, name="admin_reset_jiraBusinessLine"),

    # jiraBusinessLinePlatform
    url(r'^myadmin/jiraBusinessLinePlatform/check$', jiraBusinessLinePlatform.jiraBusinessLinePlatformCheckPage, name="admin_jiraBusinessLinePlatform_check"),
    url(r'^myadmin/jiraBusinessLinePlatform/getJiraBusinessLinePlatform$', jiraBusinessLinePlatform.getJiraBusinessLinePlatform, name="admin_get_jiraBusinessLinePlatform_sub_page"),
    url(r'^myadmin/jiraBusinessLinePlatform/getAllPlatformBusinessLines$', jiraBusinessLinePlatform.getAllPlatformBusinessLines, name="admin_get_all_platformBusinessLines"),
    url(r'^myadmin/jiraBusinessLinePlatform/getAllJiraBusinessLines$',jiraBusinessLinePlatform.getAllJiraBusinessLines, name="admin_get_all_jiraBusinessLines"),
    url(r'^myadmin/jiraBusinessLinePlatform/addJiraBusinessLinePlatform$', jiraBusinessLinePlatform.addJiraBusinessLinePlatform, name="admin_add_jiraBusinessLinePlatform"),
    url(r'^myadmin/jiraBusinessLinePlatform/getJiraBusinessLinePlatformForId$', jiraBusinessLinePlatform.getJiraBusinessLinePlatformForId, name="admin_get_jiraBusinessLinePlatform_for_id"),
    url(r'^myadmin/jiraBusinessLinePlatform/editJiraBusinessLinePlatform$', jiraBusinessLinePlatform.editJiraBusinessLinePlatform, name="admin_edit_jiraBusinessLinePlatform"),
    url(r'^myadmin/jiraBusinessLinePlatform/deleteJiraBusinessLinePlatform$', jiraBusinessLinePlatform.deleteJiraBusinessLinePlatform, name="admin_del_jiraBusinessLinePlatform"),
    url(r'^myadmin/jiraBusinessLinePlatform/getJiraBusinessLineId$', jiraBusinessLinePlatform.getJiraBusinessLineId, name="admin_get_jiraBusinessLineId"),

    #configHttp
    url(r'^myadmin/configHttp/check$', configHttp.configHttpCheckPage, name="admin_configHttp_check"),
    url(r'^myadmin/configHttp/getConfigHttpSubPage$', configHttp.getConfigHttp, name="admin_get_configHttp_sub_page"),
    url(r'^myadmin/configHttp/getAllServiceConfKeys$', configHttp.getAllServiceConfKeys, name="admin_get_all_serviceConfKeys"),
    url(r'^myadmin/configHttp/addConfigHttp$', configHttp.addConfigHttp, name="admin_add_configHttp"),
    url(r'^myadmin/configHttp/getConfigHttpForId$', configHttp.getConfigHttpForId, name="admin_get_configHttp_for_id"),
    url(r'^myadmin/configHttp/editConfigHttp$', configHttp.editConfigHttp, name="admin_edit_configHttp"),
    url(r'^myadmin/configHttp/delConfigHttp$', configHttp.delConfigHttp, name="admin_del_configHttp"),
    url(r'^myadmin/configHttp/resetConfigHttp$', configHttp.resetConfigHttp, name="admin_reset_configHttp"),

    # httpInterfaceDebug
    url(r'^myadmin/httpInterfaceDebug/check$', httpInterfaceDebug.httpInterfaceDebugCheckPage, name="admin_httpInterfaceDebug_check"),
    url(r'^myadmin/httpInterfaceDebug/getHttpInterfaceDebugSubPage$', httpInterfaceDebug.getHttpInterfaceDebug, name="admin_get_httpInterfaceDebug_sub_page"),
    url(r'^myadmin/httpInterfaceDebug/getAllBusinessLines$', httpInterfaceDebug.getAllBusinessLines, name="admin_get_all_businessLines"),
    url(r'^myadmin/httpInterfaceDebug/getAllModuleNames$', httpInterfaceDebug.getAllModuleNames, name="admin_get_all_moduleNames"),
    url(r'^myadmin/httpInterfaceDebug/getAllSourceNames$', httpInterfaceDebug.getAllSourceNames, name="admin_get_all_sourceNames"),
    url(r'^myadmin/httpInterfaceDebug/getAllHttpConfKeys$', httpInterfaceDebug.getAllHttpConfKeys, name="admin_get_all_httpConfKeys"),
    url(r'^myadmin/httpInterfaceDebug/getAllUsers$', httpInterfaceDebug.getAllUsers, name="admin_get_all_users"),
    url(r'^myadmin/httpInterfaceDebug/addHttpInterfaceDebug$', httpInterfaceDebug.addHttpInterfaceDebug, name="admin_add_httpInterfaceDebug"),
    url(r'^myadmin/httpInterfaceDebug/getHttpInterfaceDebugForId$', httpInterfaceDebug.getHttpInterfaceDebugForId, name="admin_get_httpInterfaceDebug_for_id"),
    url(r'^myadmin/httpInterfaceDebug/editHttpInterfaceDebug$', httpInterfaceDebug.editHttpInterfaceDebug, name="admin_edit_httpInterfaceDebug"),
    url(r'^myadmin/httpInterfaceDebug/delHttpInterfaceDebug$', httpInterfaceDebug.delHttpInterfaceDebug, name="admin_del_httpInterfaceDebug"),
    url(r'^myadmin/httpInterfaceDebug/resetHttpInterfaceDebug$', httpInterfaceDebug.resetHttpInterfaceDebug, name="admin_reset_httpInterfaceDebug"),


    # httpTestcaseDebug
    url(r'^myadmin/httpTestcaseDebug/check$', httpTestcaseDebug.httpTestcaseDebugCheckPage, name="admin_httpTestcaseDebug_check"),
    url(r'^myadmin/httpTestcaseDebug/getHttpTestcaseDebugSubPage$', httpTestcaseDebug.getHttpTestcaseDebug, name="admin_get_httpTestcaseDebug_sub_page"),
    url(r'^myadmin/httpTestcaseDebug/getAllBusinessLines$', httpTestcaseDebug.getAllBusinessLines, name="admin_get_all_businessLines"),
    url(r'^myadmin/httpTestcaseDebug/getAllModuleNames$', httpTestcaseDebug.getAllModuleNames, name="admin_get_all_moduleNames"),
    url(r'^myadmin/httpTestcaseDebug/getAllSourceNames$', httpTestcaseDebug.getAllSourceNames, name="admin_get_all_sourceNames"),
    url(r'^myadmin/httpTestcaseDebug/getAllHttpConfKeys$', httpTestcaseDebug.getAllHttpConfKeys, name="admin_get_all_httpConfKeys"),
    url(r'^myadmin/httpTestcaseDebug/getAllUsers$', httpTestcaseDebug.getAllUsers, name="admin_get_all_users"),
    url(r'^myadmin/httpTestcaseDebug/addHttpTestcaseDebug$', httpTestcaseDebug.addHttpTestcaseDebug, name="admin_add_httpTestcaseDebug"),
    url(r'^myadmin/httpTestcaseDebug/getHttpTestcaseDebugForId$', httpTestcaseDebug.getHttpTestcaseDebugForId, name="admin_get_httpTestcaseDebug_for_id"),
    url(r'^myadmin/httpTestcaseDebug/editHttpTestcaseDebug$', httpTestcaseDebug.editHttpTestcaseDebug, name="admin_edit_httptestcaseDebug"),
    url(r'^myadmin/httpTestcaseDebug/delHttpTestcaseDebug$', httpTestcaseDebug.delHttpTestcaseDebug, name="admin_del_httptestcaseDebug"),
    url(r'^myadmin/httpTestcaseDebug/resetHttpTestcaseDebug$', httpTestcaseDebug.resetHttpTestcaseDebug, name="admin_reset_httptestcaseDebug"),

    # exePython
    url(r'^myadmin/exePython/check$', exePython.exePythonCheckPage, name="admin_exePython_check"),
    url(r'^myadmin/exePython/getExePythonSubPage$', exePython.getExePython,name="admin_get_exePython_sub_page"),
    url(r'^myadmin/exePython/addExePython$', exePython.addExePython, name="admin_add_exePython"),
    url(r'^myadmin/exePython/getExePythonForId$', exePython.getExePythonForId, name="admin_get_exePython_for_id"),
    url(r'^myadmin/exePython/editExePython$', exePython.editExePython, name="admin_edit_exePython"),
    url(r'^myadmin/exePython/delExePython$', exePython.delExePython, name="admin_del_exePythone"),
    url(r'^myadmin/exePython/delRedisKey$', exePython.delRedisKey, name="admin_del_redisKey"),
    url(r'^myadmin/exePython/resetExePython$', exePython.resetExePython, name="admin_reset_exePython"),

    # standardTask
    url(r'^myadmin/standardTask/check$', standardTask.standardTaskCheckPage, name="admin_standardTask_check"),
    url(r'^myadmin/standardTask/getStandardTaskSubPage$', standardTask.getStandardTask, name="admin_get_standardTask_sub_page"),
    url(r'^myadmin/standardTask/addStandardTask$', standardTask.addStandardTask, name="admin_add_standardTaskn"),
    url(r'^myadmin/standardTask/getStandardTaskForId$', standardTask.getStandardTaskForId, name="admin_get_standardTask_for_id"),
    url(r'^myadmin/standardTask/editStandardTask$', standardTask.editStandardTask, name="admin_edit_standardTask"),
    url(r'^myadmin/standardTask/delStandardTask$', standardTask.delStandardTask, name="admin_del_standardTask"),
    url(r'^myadmin/standardTask/resetStandardTask$', standardTask.resetStandardTask, name="admin_reset_standardTask"),
    url(r'^myadmin/standardTask/getAllVersions$', standardTask.getAllVersions, name="admin_get_all_versions"),
    url(r'^myadmin/standardTask/copyTaskToOtherVersion$', standardTask.copyTaskToOtherVersion, name="admin_copy_task"),


    # standardTask
    url(r'^myadmin/openApiBusinessLine/check$', openApiBusinessLine.openApiBusinessLineCheckPage, name="admin_openApiBusinessLine_check"),
    url(r'^myadmin/openApiBusinessLine/getOpenApiBusinessLineSubPage$', openApiBusinessLine.getOpenApiBusinessLine, name="admin_get_openApiBusinessLine_sub_page"),
    url(r'^myadmin/openApiBusinessLine/addOpenApiBusinessLine$', openApiBusinessLine.addOpenApiBusinessLine, name="admin_add_openApiBusinessLine"),
    url(r'^myadmin/openApiBusinessLine/getOpenApiBusinessLineForId$', openApiBusinessLine.getOpenApiBusinessLineForId, name="admin_get_openApiBusinessLine_for_id"),
    url(r'^myadmin/openApiBusinessLine/editOpenApiBusinessLine$', openApiBusinessLine.editOpenApiBusinessLine, name="admin_edit_openApiBusinessLine"),
    url(r'^myadmin/openApiBusinessLine/delOpenApiBusinessLine$', openApiBusinessLine.delOpenApiBusinessLine, name="admin_del_openApiBusinessLine"),
    url(r'^myadmin/openApiBusinessLine/resetOpenApiBusinessLine$', openApiBusinessLine.resetOpenApiBusinessLine, name="admin_reset_openApiBusinessLine"),

    # openApiUri
    url(r'^myadmin/openApiUri/check$', openApiUri.openApiUriCheckPage, name="admin_openApiUri_check"),
    url(r'^myadmin/openApiUri/getOpenApiUriSubPage$', openApiUri.getOpenApiUri, name="admin_get_openApiUri_sub_page"),
    url(r'^myadmin/openApiUri/addOpenApiUri$', openApiUri.addOpenApiUri, name="admin_add_openApiUri"),
    url(r'^myadmin/openApiUri/getOpenApiUriForId$', openApiUri.getOpenApiUriForId, name="admin_get_openApiUri_for_id"),
    url(r'^myadmin/openApiUri/editOpenApiUri$', openApiUri.editOpenApiUri, name="admin_edit_openApiUri"),
    url(r'^myadmin/openApiUri/deleteOpenApiUri$', openApiUri.deleteOpenApiUri, name="admin_del_openApiUri"),
    url(r'^myadmin/openApiUri/resetOpenApiUri$', openApiUri.resetOpenApiUri, name="admin_reset_openApiUri"),

    # unitTestService
    url(r'^myadmin/unitTestService/check$', unitTestService.unitTestServiceCheckPage, name="admin_unitTestService_check"),
    url(r'^myadmin/unitTestService/getUnitTestServiceSubPage$', unitTestService.getUnitTestService, name="admin_get_unitTestService_sub_page"),
    url(r'^myadmin/unitTestService/addUnitTestService$', unitTestService.addUnitTestService, name="admin_add_unitTestService"),
    url(r'^myadmin/unitTestService/getUnitTestServiceForId$', unitTestService.getUnitTestServiceForId, name="admin_get_unitTestService_for_id"),
    url(r'^myadmin/unitTestService/editUnitTestService$', unitTestService.editUnitTestService, name="admin_edit_unitTestService"),
    url(r'^myadmin/unitTestService/deleteUnitTestService$', unitTestService.deleteUnitTestService, name="admin_del_unitTestService"),
    url(r'^myadmin/unitTestService/resetUnitTestService$', unitTestService.resetUnitTestService, name="admin_reset_unitTestService"),

    # uiMobileServer
    url(r'^myadmin/uiMobileServer/check$', uiMobileServer.uiMobileServerCheckPage, name="admin_uiMobileServer_check"),
    url(r'^myadmin/uiMobileServer/getUiMobileServerSubPage$', uiMobileServer.getUiMobileServer, name="admin_get_uiMobileServer_sub_page"),
    url(r'^myadmin/uiMobileServer/addUiMobileServer$', uiMobileServer.addUiMobileServer, name="admin_add_uiMobileServer"),
    url(r'^myadmin/uiMobileServer/getUiMobileServerForId$', uiMobileServer.getUiMobileServerForId, name="admin_get_uuiMobileServer_for_id"),
    url(r'^myadmin/uiMobileServer/editUiMobileServer$', uiMobileServer.editUiMobileServer, name="admin_edit_uiMobileServer"),
    url(r'^myadmin/uiMobileServer/deleteUiMobileServer$', uiMobileServer.deleteUiMobileServer, name="admin_del_uiMobileServer"),
    url(r'^myadmin/uiMobileServer/resetUiMobileServer$', uiMobileServer.resetUiMobileServer, name="admin_reset_uiMobileServer"),

    # versionManage
    url(r'^myadmin/versionManage/check$', versionManage.versionManageCheckPage, name="admin_versionManage_check"),
    url(r'^myadmin/versionManage/getVersionManageSubPage$', versionManage.getVersionManage, name="admin_get_versionManage_sub_page"),
    url(r'^myadmin/versionManage/addVersionManage$', versionManage.addVersionManage, name="admin_add_versionManage"),
    url(r'^myadmin/versionManage/getVersionManageForId$', versionManage.getVersionManageForId, name="admin_get_versionManage_for_id"),
    url(r'^myadmin/versionManage/editVersionManage$', versionManage.editVersionManage, name="admin_edit_versionManage"),
    url(r'^myadmin/versionManage/deleteVersionManage$', versionManage.deleteVersionManage, name="admin_del_versionManage"),
    url(r'^myadmin/versionManage/resetVersionManage$', versionManage.resetVersionManage, name="admin_reset_versionManage"),

    # userLog
    url(r'^myadmin/userLog/check$', userLog.userLogCheckPage, name="admin_userLog_check"),
    url(r'^myadmin/userLog/getUserLogSubPage$', userLog.getUserLog, name="admin_get_userLog_sub_page"),
    url(r'^myadmin/userLog/addUserLog$', userLog.addUserLog, name="admin_add_userLog"),
    url(r'^myadmin/userLog/getUserLogForId$', userLog.getUserLogForId, name="admin_get_userLog_for_id"),
    url(r'^myadmin/userLog/editUserLog$', userLog.editUserLog, name="admin_edit_userLog"),
    url(r'^myadmin/userLog/deleteUserLog$', userLog.deleteUserLog, name="admin_del_userLog"),
    url(r'^myadmin/userLog/resetUserLog$', userLog.resetUserLog, name="admin_reset_userLog"),

    # standardEnv
    url(r'^myadmin/standardEnv/check$', standardEnv.standardEnvCheckPage, name="admin_standardEnv_check"),
    url(r'^myadmin/standardEnv/getStandardEnvSubPage$', standardEnv.getStandardEnv, name="admin_get_standardEnv_sub_page"),
    url(r'^myadmin/standardEnv/addStandardEnv$', standardEnv.addStandardEnv, name="admin_add_standardEnv"),
    url(r'^myadmin/standardEnv/getStandardEnvForId$', standardEnv.getStandardEnvForId, name="admin_get_standardEnv_for_id"),
    url(r'^myadmin/standardEnv/editStandardEnv$', standardEnv.editStandardEnv, name="admin_edit_standardEnv"),
    url(r'^myadmin/standardEnv/deleteStandardEnv$', standardEnv.deleteStandardEnv, name="admin_del_standardEnv"),
    url(r'^myadmin/standardEnv/resetStandardEnv$', standardEnv.resetStandardEnv, name="admin_reset_standardEnv"),

    # cacheManage
    url(r'^myadmin/cacheManage/check$', cacheManage.cacheManageCheckPage, name="admin_cacheManage_check"),
    url(r'^myadmin/cacheManage/getCacheManageSubPage$', cacheManage.getCacheManage, name="admin_get_cacheManage_sub_page"),
    url(r'^myadmin/cacheManage/deleteCacheData$', cacheManage.deleteCacheData, name="admin_delete_cacheData_sub_page"),
    url(r'^myadmin/cacheManage/flushAllDatas$', cacheManage.flushAllDatas, name="admin_flush_allDatas_sub_page"),
    url(r'^myadmin/cacheManage/addCacheData$', cacheManage.addCacheData, name="admin_add_cacheData"),
    url(r'^myadmin/cacheManage/getCacheValueForCacheKey$', cacheManage.getCacheValueForCacheKey, name="admin_getCacheValue_for_cacheKey"),
    url(r'^myadmin/cacheManage/editCacheData$', cacheManage.editCacheData, name="admin_edit_cacheData"),



    # dataStorage
    url(r'^myadmin/dataStorage/check$', dataStorage.dataStorageCheckPage, name="admin_dataStorage_check"),
    url(r'^myadmin/dataStorage/getCacheManageSubPage$', dataStorage.getdataStorage, name="admin_get_dataStorage_sub_page"),

    #serverConf
    url(r'^myadmin/serviceConf/check$', adminServiceConf.adminServiceConf, name="admin_service_conf_page"),
    url(r'^myadmin/serviceConf/getAdminServiceConfForId$', adminServiceConf.getAdminServiceConfForId, name="admin_get_service_conf_for_id"),
    url(r'^myadmin/serviceConf/getServiceConfSubPage', adminServiceConf.getAdminServiceConf, name="admin_service_conf_sub_page"),
    url(r'^myadmin/serviceConf/getServiceTaskConfSubPage', adminServiceConf.getAdminServiceTaskConf, name="admin_service_conf_sub_page"),
    url(r'^myadmin/serviceConf/saveEditServiceConf', adminServiceConf.editAdminServiceConf, name="admin_edit_service_conf"),
    url(r'^myadmin/serviceConf/queueDeleteTask', adminServiceConf.queueDeleteTask, name="admin_edit_service_conf"),

]