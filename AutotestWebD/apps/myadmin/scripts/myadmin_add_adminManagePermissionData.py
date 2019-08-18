
import django
import sys,os
rootpath = os.path.dirname(os.path.realpath(__file__)).replace("\\","/")
rootpath = rootpath.split("/apps")[0]
# print(rootpath)
syspath=sys.path
sys.path=[]
sys.path.append(rootpath) #指定搜索路径绝对目录
sys.path.extend([rootpath+i for i in os.listdir(rootpath) if i[0]!="."])#将工程目录下的一级目录添加到python搜索路径中
sys.path.extend(syspath)


from datetime import datetime
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *





if __name__ == "__main__":
    addTime = datetime.datetime.now()
    adminManagePermissionList = []
    adminManagePermissionList.append({"permissionName": " 用户管理", "permissionKey": "AdminUser", "state": 1, "addBy": "", "modBy": "", "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue":"/myadmin/user/check"})
    adminManagePermissionList.append({"permissionName": " 小组管理", "permissionKey": "AdminTeam", "state": 1, "addBy": "", "modBy": "", "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue":"/myadmin/team/check"})
    adminManagePermissionList.append({"permissionName": " 角色管理", "permissionKey": "AdminRole", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue":"/myadmin/role/check"})
    adminManagePermissionList.append(
        {"permissionName": " 权限管理", "permissionKey": "AdminPermission", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue":"/myadmin/permission/check"})
    adminManagePermissionList.append(
        {"permissionName": " 接口页面管理", "permissionKey": "AdminInterfaceModule", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue":"/myadmin/interfaceModule/check"})
    adminManagePermissionList.append(
        {"permissionName": " 接口权限管理", "permissionKey": "AdminInterfacePermission", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue":"/myadmin/interfacePermission/check"})
    adminManagePermissionList.append(
        {"permissionName": " 后台权限管理", "permissionKey": "AdminManagePermission", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue":"/myadmin/adminManagePermission/check"})
    adminManagePermissionList.append(
        {"permissionName": " 管理员管理", "permissionKey": "AdminManager", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue":"/myadmin/admin/check"})
    adminManagePermissionList.append(
        {"permissionName": " 业务线管理", "permissionKey": "AdminBusinessLine", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue":"/myadmin/businessLine/check"})
    adminManagePermissionList.append(
        {"permissionName": " 模块管理", "permissionKey": "AdminModuleManage", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue":"/myadmin/moduleManage/check"})
    adminManagePermissionList.append(
        {"permissionName": " 业务线模块管理", "permissionKey": "AdminBusinessLineModule", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue":"/myadmin/businessLineModule/check"})
    adminManagePermissionList.append(
        {"permissionName": " 来源管理", "permissionKey": "AdminSource", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue":"/myadmin/source/check"})
    adminManagePermissionList.append(
        {"permissionName": " 数据服务器管理", "permissionKey": "AdminConfigService", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue":"/myadmin/configService/check"})
    adminManagePermissionList.append(
        {"permissionName": " URI管理", "permissionKey": "AdminConfigURI", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue":"/myadmin/configUri/check"})
    adminManagePermissionList.append(
        {"permissionName": " jira模块管理", "permissionKey": "AdminJiraModule", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue":"/myadmin/jiraModule/check"})
    adminManagePermissionList.append(
        {"permissionName": " jira模块和平台关联管理", "permissionKey": "AdminModulePlatform", "state": 1, "addBy": "",
         "modBy": "", "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue":"/myadmin/modulePlatform/check"})
    adminManagePermissionList.append(
        {"permissionName": " jira业务线管理", "permissionKey": "AdminJiraBusinessLine", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue":"/myadmin/jiraBusinessLine/check"})
    adminManagePermissionList.append(
        {"permissionName": " jira业务线和平台关联管理", "permissionKey": "AdminJiraBusinessLinePlatform", "state": 1, "addBy": "",
         "modBy": "", "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue":"/myadmin/jiraBusinessLinePlatform/check"})
    adminManagePermissionList.append(
        {"permissionName": " 环境配置管理", "permissionKey": "AdminConfigHttp", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue":"/myadmin/configHttp/check"})
    # adminManagePermissionList.append({"permissionName": " 接口调试管理", "permissionKey": "AdminHttpInterfaceDebug", "state": 1, "addBy": "", "modBy": "", "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0})
    # adminManagePermissionList.append({"permissionName": " 接口用例调试管理", "permissionKey": "AdminHttpTestcaseDebug", "state": 1, "addBy": "", "modBy": "", "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0})
    adminManagePermissionList.append(
        {"permissionName": " 执行python代码管理", "permissionKey": "AdminExePython", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue":"/myadmin/exePython/check"})
    adminManagePermissionList.append(
        {"permissionName": " 标准任务版本管理", "permissionKey": "AdminStandardTask", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue":"/myadmin/standardTask/check"})
    adminManagePermissionList.append(
        {"permissionName": " openApi业务线管理", "permissionKey": "AdminOpenApiBusinessLine", "state": 1, "addBy": "",
         "modBy": "", "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue":"/myadmin/openApiBusinessLine/check"})
    adminManagePermissionList.append(
        {"permissionName": " openApi_Uri管理", "permissionKey": "AdminOpenApiUri", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue":"/myadmin/openApiUri/check"})
    adminManagePermissionList.append(
        {"permissionName": " unitTestService管理", "permissionKey": "AdminUnitTestService", "state": 1, "addBy": "",
         "modBy": "", "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue":"/myadmin/unitTestService/check"})
    adminManagePermissionList.append(
        {"permissionName": " ui移动端服务管理", "permissionKey": "AdminUiMobileServer", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue":"/myadmin/uiMobileServer/check"})
    adminManagePermissionList.append(
        {"permissionName": " 版本管理", "permissionKey": "AdminVersionManage", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue":"/myadmin/versionManage/check"})
    adminManagePermissionList.append(
        {"permissionName": " 操作记录管理", "permissionKey": "AdminChangeLog", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 1, "permissionValue":"/myadmin/changeLog/check"})
    adminManagePermissionList.append(
        {"permissionName": " 用户操作日志管理", "permissionKey": "AdminUserLog", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 1, "permissionValue":"/myadmin/userLog/check"})
    adminManagePermissionList.append(
        {"permissionName": " 通过率环境版本配置管理", "permissionKey": "AdminStandardEnv", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue": "/myadmin/standardEnv/check"})
    adminManagePermissionList.append(
        {"permissionName": " webportal业务线管理", "permissionKey": "AdminWebportalBusinessLine", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue": "/myadmin/webportalBusinessLine/check"})
    adminManagePermissionList.append(
        {"permissionName": " 缓存管理", "permissionKey": "AdminCacheManage", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue": "/myadmin/cacheManage/check"})
    adminManagePermissionList.append(
        {"permissionName": " 前台数据管理", "permissionKey": "AdminDataStorage", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 1,
         "permissionValue": "/myadmin/dataStorage/check"})

    TbAdminManagePermission.objects.all().delete()
    for permissionIndex in adminManagePermissionList:
        permission = TbAdminManagePermission()
        permission.permissionName = permissionIndex["permissionName"]
        permission.permissionKey = permissionIndex["permissionKey"]
        permission.state = permissionIndex["state"]
        permission.addBy = permissionIndex["addBy"]
        permission.modBy = permissionIndex["modBy"]
        permission.addTime = permissionIndex["addTime"]
        permission.modTime = permissionIndex["modTime"]
        permission.isDefaultPermission = permissionIndex["isDefaultPermission"]
        permission.permissionValue = permissionIndex["permissionValue"]
        permission.save()