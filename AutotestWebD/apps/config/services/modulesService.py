import apps.common.func.InitDjango
from apps.common.func.CommonFunc import *
from all_models.models import TbModules
class ModulesService(object):
    @staticmethod
    def getModules():
        return dbModelListToListDict(TbModules.objects.all())

    @staticmethod
    def getInterfaceListModulesId(interfeceListSql,protocol="HTTP"):
        if protocol == "HTTP":
            sql = "SELECT distinct moduleName from (SELECT moduleId from tb_http_interface WHERE %s) b  LEFT JOIN tb_modules bl  on bl.id = b.moduleId " % interfeceListSql
            result = executeSqlGetDict(sql,[])
            return result
        elif protocol=="DUBBO":
            sql = "SELECT distinct moduleName from (SELECT moduleId from tb2_dubbo_interface WHERE %s) b  LEFT JOIN tb_modules bl  on bl.id = b.moduleId " % interfeceListSql
            result = executeSqlGetDict(sql, [])
            return result

    @staticmethod
    def getVersionInterfaceListModulesId(interfeceListSql,versionName):
        sql = "SELECT distinct moduleName from (SELECT moduleId from tb_version_http_interface WHERE versionName='%s' and (%s)) b  LEFT JOIN tb_modules bl  on bl.id = b.moduleId " % (versionName,interfeceListSql)
        result = executeSqlGetDict(sql,[])
        return result

    @staticmethod
    def getTestCaseListModulesId(testCaseListSql,protocol="HTTP"):
        if protocol == "HTTP":
            sql = "SELECT distinct moduleName from (SELECT moduleId from tb_http_testcase WHERE %s) b  LEFT JOIN tb_modules bl  on bl.id = b.moduleId " % testCaseListSql
            result = executeSqlGetDict(sql, [])
            return result
        elif protocol=="DUBBO":
            sql = "SELECT distinct moduleName from (SELECT moduleId from tb2_dubbo_testcase WHERE %s) b  LEFT JOIN tb_modules bl  on bl.id = b.moduleId " % testCaseListSql
            result = executeSqlGetDict(sql, [])
            return result

    @staticmethod
    def getVersionTestCaseListModulesId(testCaseListSql,versionName):
        sql = "SELECT distinct moduleName from (SELECT moduleId from tb_version_http_testcase WHERE versionName='%s' and (%s) ) b  LEFT JOIN tb_modules bl  on bl.id = b.moduleId " % (versionName,testCaseListSql)
        result = executeSqlGetDict(sql, [])
        return result

    @staticmethod
    def getAllModules():
        return TbModules.objects.filter(state=1)

    @staticmethod
    def getModuleNameById(id):
        return TbModules.objects.filter(id=id)[0].moduleName

if __name__ == "__main__":
    # print((businessService.=)))
    # print(UserService.getUserByLoginname(UserService.getUsers()[0].loginname))
    print(dbModelListToListDict(ModulesService.getModules()))