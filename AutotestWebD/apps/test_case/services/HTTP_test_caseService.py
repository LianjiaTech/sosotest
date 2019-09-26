import apps.common.func.InitDjango
from all_models.models import *
from all_models.models.A0011_version_manage import TbVersionHttpTestcase
from django.db import connection
from django.forms.models import model_to_dict
from apps.common.func.CommonFunc import *

class HTTP_test_caseService(object):

    @staticmethod
    def getTestCase():
        return TbHttpTestcase.objects.all()

    @staticmethod
    def getTestCaseForId(id):
        return TbHttpTestcase.objects.filter(id=id)[0]

    @staticmethod
    def getVersionTestCaseForId(id):
        return TbVersionHttpTestcase.objects.filter(id=id)[0]

    @staticmethod
    def getInterfaceList(execCheckSql,list):
        cursor = connection.cursor()
        cursor.execute(execCheckSql,list)
        return cursor.fetchall()

    @staticmethod
    def delTestCaseForId(request,id):
        testCaseObj = TbHttpTestcase.objects.filter(id=id)
        if testCaseObj[0].addBy.loginName != request.session.get("loginName"):
            userChangeLogTestCaseDel(request,dbModelToDict(testCaseObj[0]))
        delData = testCaseObj.update(state=0)
        return delData

    @staticmethod
    def delVersionTestCaseForId(request,id):
        testCaseObj = TbVersionHttpTestcase.objects.filter(id=id)
        if testCaseObj[0].addBy.loginName != request.session.get("loginName"):
            userChangeLogTestCaseDel(request, dbModelToDict(testCaseObj[0]))
        delData = testCaseObj.update(state=0)
        return delData

    @staticmethod
    def user_contacts():
        audit = 2
        sql = """SElECT * from tb_http_interface i LEFT JOIN tb_user u ON i.addBy = u.loginName WHERE 1=1 and i.state=1 and (i.addBy LIKE %s or u.userName LIKE %s)  LIMIT 0,20 """
        import pymysql
        cursor = connection.cursor()
        cursor.execute(sql, ["l11111111111iyc","liyc"])
        rowData = cursor.fetchall()

        col_names = [desc[0] for desc in cursor.description]
        result = []
        for row in rowData:
            objDict = {}
            # 把每一行的数据遍历出来放到Dict中
            for index, value in enumerate(row):
                # print(index, col_names[index], value)
                objDict[col_names[index]] = value

            result.append(objDict)

        return rowData


    @staticmethod
    def queryPeopleTestCase(now_pageNum,pageNum , loginName):
        limit = ('%d,%d' % (now_pageNum * pageNum ,pageNum))
        execSql = 'SELECT u.loginName , u.userName, c.count from tb_user u LEFT JOIN (SELECT addBy as loginName,COUNT(*) as count FROM tb_http_testcase where state=1 GROUP BY addBy ) c on u.loginName = c.loginName WHERE u.state = 1 and c.count>0 and u.loginName != "%s" order by c.count desc LIMIT %s ;' % (loginName,limit)
        resultDict = executeSqlGetDict(execSql,[])
        return resultDict

    @staticmethod
    def queryVersionPeopleTestCase(now_pageNum,pageNum , loginName,versionName):
        limit = ('%d,%d' % (now_pageNum * pageNum ,pageNum))
        execSql = 'SELECT u.loginName , u.userName, c.count from tb_user u LEFT JOIN (SELECT addBy as loginName,COUNT(*) as count FROM tb_version_http_testcase where state=1 and versionName="%s" GROUP BY addBy ) c on u.loginName = c.loginName WHERE u.state = 1 and c.count>0 and u.loginName != "%s" order by c.count desc LIMIT %s ;' % (versionName,loginName,limit)
        resultDict = executeSqlGetDict(execSql,[])
        return resultDict

    @staticmethod
    def getTestCaseForIdToDict(id):
        return dbModelToDict(TbHttpTestcase.objects.filter(id=id)[0])

    @staticmethod
    def getVersionTestCaseForIdToDict(id):
        return dbModelToDict(TbVersionHttpTestcase.objects.filter(id=id)[0])

    @staticmethod
    def testCaseAdd(testCaseData):
        testCaseData["caseId"] = HTTP_test_caseService.getTestCaseId()
        try:
            saveTestCase = TbHttpTestcase.objects.create(**testCaseData)
        except Exception as e:
            print(e)
        return saveTestCase

    @staticmethod
    def testVersionCaseAdd(testCaseData,versionName):
        testCaseData["versionName_id"] = versionName
        testCaseData["addTime"] = datetime.datetime.now()
        testCaseData["modTime"] = datetime.datetime.now()
        testCaseData["caseId"] = HTTP_test_caseService.getVersionTestCaseId(versionName)
        try:
            saveTestCase = TbVersionHttpTestcase.objects.create(**testCaseData)
        except Exception as e:
            print(e)
        return saveTestCase

    @staticmethod
    def getTestCaseId():
        try:
            testCaseMaxId = TbHttpTestcase.objects.latest('id').caseId
        except Exception as e:
            caseId = 'HTTP_TESTCASE_1'
            return caseId
        splitData = testCaseMaxId.split('_')
        caseId = "%s_%s_%s" % (splitData[0], splitData[1], (int(splitData[2]) + 1))
        return caseId

    @staticmethod
    def getVersionTestCaseId(versionName):
        try:
            testCaseMaxId = TbVersionHttpTestcase.objects.filter(versionName_id=versionName).latest('id').caseId
        except Exception as e:
            caseId = 'HTTP_TESTCASE_1'
            return caseId
        splitData = testCaseMaxId.split('_')
        caseId = "%s_%s_%s" % (splitData[0], splitData[1], (int(splitData[2]) + 1))
        return caseId

    @staticmethod
    def saveEdit(request,testCaseData):
        try:
            testCaseObj = TbHttpTestcase.objects.filter(id=testCaseData["id"])
            if testCaseObj[0].addBy.loginName != request.session.get("loginName"):
                userChangeLogTestCaseToTestCaseChange(request,dbModelToDict(testCaseObj[0]),testCaseData)
            saveEditResult = testCaseObj.update(**testCaseData)
            return saveEditResult
        except Exception as e:
            print(traceback.format_exc())
            return False
    @staticmethod
    def saveVersionEdit(request,testCaseData):
        testCaseObj = TbVersionHttpTestcase.objects.filter(id=testCaseData["id"])
        if testCaseObj[0].addBy.loginName != request.session.get("loginName"):
            userChangeLogTestCaseToTestCaseChange(request, dbModelToDict(testCaseObj[0]), testCaseData)
        saveEditResult = testCaseObj.update(**testCaseData)
        return saveEditResult

    @staticmethod
    def taskCheckTestCaseList(testCaseIdList):
        testCaseList = TbHttpTestcase.objects.filter(caseId__in=testCaseIdList)
        return testCaseList

    @staticmethod
    def getTestCaseForTestCaseId(testCaseId):
        return TbHttpTestcase.objects.filter(caseId=testCaseId, state=1)[0]

    @staticmethod
    def getVersionTestCaseForTestCaseId(testCaseId,versionName):
        return TbVersionHttpTestcase.objects.filter(caseId=testCaseId,versionName_id=versionName)[0]

if __name__ == "__main__":
    # print((HTTP_test_caseService.getTestCaseForIdToDict("23")))
    # print(UserService.getUserByLoginname(UserService.getUsers()[0].loginname))
    # HTTP_test_caseService.testCaseAdd("")
    pass

