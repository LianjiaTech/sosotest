import apps.common.func.InitDjango
from apps.common.func.CommonFunc import *
from all_models.models import TbBusinessLine

class BusinessService(object):
    @staticmethod
    def getBusiness():
        return dbModelListToListDict(TbBusinessLine.objects.all())

    @staticmethod
    def getInterfaceListBusinessId(interfaceListSql,protocol="HTTP"):
        if protocol == "HTTP":
            sql = 'SELECT distinct bussinessLineName from (SELECT businessLineId from tb_http_interface WHERE %s) b LEFT JOIN tb_business_line bl on bl.id = b.businessLineId ' % interfaceListSql
            result = executeSqlGetDict(sql,[])
            return result
        elif protocol == "DUBBO":
            sql = 'SELECT distinct bussinessLineName from (SELECT businessLineId from tb2_dubbo_interface WHERE %s) b LEFT JOIN tb_business_line bl on bl.id = b.businessLineId ' % interfaceListSql
            result = executeSqlGetDict(sql, [])
            return result

    @staticmethod
    def getVersionInterfaceListBusinessId(interfaceListSql,versionName):
        sql = 'SELECT distinct bussinessLineName from (SELECT businessLineId from tb_version_http_interface WHERE versionName="%s" and ( %s)) b LEFT JOIN tb_business_line bl on bl.id = b.businessLineId ' % (versionName,interfaceListSql)
        result = executeSqlGetDict(sql,[])
        return result

    @staticmethod
    def getTestCaseListBusinessId(testCaseListSql,protocol="HTTP"):
        if protocol=="HTTP":
            sql = "SELECT distinct bussinessLineName from  (SELECT businessLineId from tb_http_testcase WHERE %s) b LEFT JOIN tb_business_line bl on bl.id = b.businessLineId " % testCaseListSql
            result = executeSqlGetDict(sql,[])
            return result
        elif protocol=="DUBBO":
            sql = "SELECT distinct bussinessLineName from  (SELECT businessLineId from tb2_dubbo_testcase WHERE %s) b LEFT JOIN tb_business_line bl on bl.id = b.businessLineId " % testCaseListSql
            result = executeSqlGetDict(sql, [])
            return result

    @staticmethod
    def getVersionTestCaseListBusinessId(testCaseListSql,versionName):
        sql = "SELECT distinct bussinessLineName from  (SELECT businessLineId from tb_version_http_testcase WHERE versionName='%s' and (%s) ) b LEFT JOIN tb_business_line bl on bl.id = b.businessLineId " % (versionName,testCaseListSql)
        result = executeSqlGetDict(sql,[])
        return result

    @staticmethod
    def getAllBusinessLine():
        return TbBusinessLine.objects.filter(state=1)

    @staticmethod
    def getBusinessLineNameById(id):
        return TbBusinessLine.objects.filter(id=id)[0].bussinessLineName

if __name__ == "__main__":
    # print((businessService.=)))
    # print(UserService.getUserByLoginname(UserService.getUsers()[0].loginname))
    print(dbModelListToListDict(BusinessService.getBusiness()))