import apps.common.func.InitDjango
from apps.common.func.CommonFunc import *
from all_models.models import TbSource
class SourceService(object):
    # @staticmethod
    # def getModules():
    #     return dbModelListToListDict(TbSource.objects.all())
    #
    @staticmethod
    def getInterfaceListSourcesId(interfeceListSql):
        sql = "SELECT distinct sourceName from (SELECT sourceId from tb_http_interface WHERE %s) b  LEFT JOIN tb_source bl  on bl.id = b.sourceId " % interfeceListSql
        result = executeSqlGetDict(sql,[])
        return result

    @staticmethod
    def getVersionInterfaceListSourcesId(interfeceListSql,versionName):
        sql = "SELECT distinct sourceName from (SELECT sourceId from tb_version_http_interface WHERE versionName='%s' and (%s)) b  LEFT JOIN tb_source bl  on bl.id = b.sourceId " % (versionName,interfeceListSql)
        result = executeSqlGetDict(sql,[])
        return result

    @staticmethod
    def getTestCaseListSourcesId(testCaseListSql):
        sql = "SELECT distinct sourceName from (SELECT sourceId from tb_http_testcase WHERE %s) b  LEFT JOIN tb_source bl  on bl.id = b.sourceId " % testCaseListSql
        print(sql)
        result = executeSqlGetDict(sql, [])
        return result

    @staticmethod
    def getVersionTestCaseListSourcesId(testCaseListSql,versionName):
        sql = "SELECT distinct sourceName from (SELECT sourceId from tb_version_http_testcase WHERE versionName='%s' and (%s) ) b  LEFT JOIN tb_source bl  on bl.id = b.sourceId " % (versionName,testCaseListSql)
        print(sql)
        result = executeSqlGetDict(sql, [])
        return result

    @staticmethod
    def getAllSource():
        return TbSource.objects.filter(state=1)

if __name__ == "__main__":
    # print((businessService.=)))
    # print(UserService.getUserByLoginname(UserService.getUsers()[0].loginname))
    print(dbModelListToListDict(SourceService.getAllSource()))