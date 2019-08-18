
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
    #标准的，但是暂时不开放的功能，开发中的...
    adminManagePermissionList.append({"permissionName": " 角色管理", "permissionKey": "AdminRole", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue":"/myadmin/role/check"})

    adminManagePermissionList.append(
        {"permissionName": " ui移动端服务管理", "permissionKey": "AdminUiMobileServer", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0,
         "permissionValue": "/myadmin/uiMobileServer/check"})
    adminManagePermissionList.append(
        {"permissionName": " 版本管理", "permissionKey": "AdminVersionManage", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0,
         "permissionValue": "/myadmin/versionManage/check"})

    #非标准的，定制的
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
        {"permissionName": " openApi业务线管理", "permissionKey": "AdminOpenApiBusinessLine", "state": 1, "addBy": "",
         "modBy": "", "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue":"/myadmin/openApiBusinessLine/check"})
    adminManagePermissionList.append(
        {"permissionName": " openApi_Uri管理", "permissionKey": "AdminOpenApiUri", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue":"/myadmin/openApiUri/check"})
    adminManagePermissionList.append(
        {"permissionName": " unitTestService管理", "permissionKey": "AdminUnitTestService", "state": 1, "addBy": "",
         "modBy": "", "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0, "permissionValue":"/myadmin/unitTestService/check"})
    adminManagePermissionList.append(
        {"permissionName": " 标准任务版本管理", "permissionKey": "AdminStandardTask", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0,
         "permissionValue": "/myadmin/standardTask/check"})
    adminManagePermissionList.append(
        {"permissionName": " 通过率环境版本配置管理", "permissionKey": "AdminStandardEnv", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0,
         "permissionValue": "/myadmin/standardEnv/check"})
    adminManagePermissionList.append(
        {"permissionName": " webportal业务线管理", "permissionKey": "AdminWebportalBusinessLine", "state": 1, "addBy": "",
         "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0,
         "permissionValue": "/myadmin/webportalBusinessLine/check"})

    adminManagePermissionList.append(
        {"permissionName": " 缓存管理", "permissionKey": "AdminCacheManage", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 0,
         "permissionValue": "/myadmin/cacheManage/check"})

    adminManagePermissionList.append(
        {"permissionName": " 前台数据管理", "permissionKey": "AdminDataStorage", "state": 1, "addBy": "", "modBy": "",
         "addTime": addTime, "modTime": addTime, "isDefaultPermission": 1,
         "permissionValue": "/myadmin/dataStorage/check"})

    # TbAdminManagePermission.objects.all().delete()
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