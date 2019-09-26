import apps.common.func.InitDjango
from all_models.models import *
from all_models.models.A0011_version_manage import TbVersionHttpInterface
from django.db import connection
from django.forms.models import model_to_dict
from apps.common.func.CommonFunc import *

class HTTP_interfaceService(object):

    @staticmethod
    def getInterface():
        return TbHttpInterface.objects.all()

    @staticmethod
    def getInterfaceList(execCheckSql,list):
        cursor = connection.cursor()
        cursor.execute(execCheckSql,list)
        return cursor.fetchall()

    # @staticmethod
    # def user_contacts():
    #     audit = 2
    #     sql = """SElECT * from tb_http_interface i LEFT JOIN tb_user u ON i.addBy = u.loginName WHERE 1=1 and i.state=1 and (i.addBy LIKE %s or u.userName LIKE %s)  LIMIT 0,%s """ % ("%s","%s",commonWebConfig.interFacePageNum)
    #     cursor = connection.cursor()
    #     cursor.execute(sql, ["l11111111111iyc","liyc"])
    #     rowData = cursor.fetchall()
    #
    #     col_names = [desc[0] for desc in cursor.description]
    #     result = []
    #     for row in rowData:
    #         objDict = {}
    #         # 把每一行的数据遍历出来放到Dict中
    #         for index, value in enumerate(row):
    #             # print(index, col_names[index], value)
    #             objDict[col_names[index]] = value
    #
    #         result.append(objDict)
    #
    #     return rowData

    @staticmethod
    def getInterfaceForId(id):
        return TbHttpInterface.objects.filter(id=id)[0]

    @staticmethod
    def getInterfaceByInterfaceId(interfaceId):
        return TbHttpInterface.objects.filter(interfaceId=interfaceId)[0]

    @staticmethod
    def getVersionInterfaceForId(id):
        return TbVersionHttpInterface.objects.filter(id=id)[0]

    @staticmethod
    def getInterfaceForIdToDict(id):
        return dbModelToDict(TbHttpInterface.objects.filter(id=id)[0])

    @staticmethod
    def getVersionInterfaceForIdToDict(id,versionName):
        return dbModelToDict(TbVersionHttpInterface.objects.filter(id=id,versionName_id=versionName)[0])

    @staticmethod
    def delInterfaceForId(request,id):
        interfaceObj = TbHttpInterface.objects.filter(id=id)
        if request.session.get("loginName") != interfaceObj[0].addBy.loginName:
            changeLog = TbUserChangeLog()
            changeLog.version = request.session.get("version")
            changeLog.loginName = request.session.get("loginName")
            changeLog.otherLoginName = interfaceObj[0].addBy.loginName
            changeLog.type = 0
            changeLog.beforeChangeData = dictToJson(dbModelToDict(interfaceObj[0]))
            changeLog.dataId = interfaceObj[0].interfaceId
            changeLog.changeDataId = interfaceObj[0].interfaceId
            changeLog.save()
        return interfaceObj.update(state=0)

    @staticmethod
    def delVersionInterfaceForId(request,id):
        interfaceObj = TbVersionHttpInterface.objects.filter(id=id)
        if request.session.get("loginName") != interfaceObj[0].addBy.loginName:
            changeLog = TbUserChangeLog()
            changeLog.version = request.session.get("version")
            changeLog.loginName = request.session.get("loginName")
            changeLog.otherLoginName = interfaceObj[0].addBy.loginName
            changeLog.type = 0
            changeLog.beforeChangeData = dictToJson(dbModelToDict(interfaceObj[0]))
            changeLog.dataId = interfaceObj[0].interfaceId
            changeLog.changeDataId = interfaceObj[0].interfaceId
            changeLog.save()
        return interfaceObj.update(state=0)

    @staticmethod
    def addInterface(data,addBy,preTitle = ""):
        try:
            newDataDict = {}
            for k, v in data.items():
                newDataDict[k] = data[k]
            newDataDict["addBy_id"] = addBy
            newDataDict["interfaceId"] = HTTP_interfaceService.getInterfaceId()
            if"title" not in newDataDict.keys():
                newDataDict["title"] = "%s:%s" % (preTitle,newDataDict["url"])
                newDataDict["casedesc"] = newDataDict["title"]
            saveInterface = TbHttpInterface.objects.create(**newDataDict)
            return saveInterface
        except Exception as e:
            return "%s" % e

    @staticmethod
    def addVersionInterface(data,addBy,versionName):
        newDataDict = {}
        for k, v in data.items():
            newDataDict[k] = data[k]
        newDataDict["addBy_id"] = addBy
        newDataDict["interfaceId"] = HTTP_interfaceService.getVersionInterfaceId(versionName)
        newDataDict["versionName_id"] = versionName
        newDataDict["addTime"] = datetime.datetime.now()
        newDataDict["modTime"] = datetime.datetime.now()
        saveInterface = TbVersionHttpInterface.objects.create(**newDataDict)
        return saveInterface

    @staticmethod
    def queryPeopleInterface(now_pageNum,pageNum , loginName):
        limit = ('%d,%d' % (now_pageNum * pageNum,pageNum))
        execSql = 'SELECT u.loginName , u.userName, c.count from tb_user u LEFT JOIN (SELECT addBy as loginName,COUNT(*) as count FROM tb_http_interface where state=1 GROUP BY addBy ) c on u.loginName = c.loginName WHERE u.state = 1 and c.count>0 and u.loginName != "%s" order by c.count desc LIMIT %s ;' % (loginName,limit)
        resultDict = executeSqlGetDict(execSql,[])
        return resultDict

    @staticmethod
    def getInterfaceId():
        try:
            interfaceMaxId = TbHttpInterface.objects.latest('id').interfaceId
        except Exception as e:
            interfaceId = 'HTTP_INTERFACE_1'
            return interfaceId
        splitData = interfaceMaxId.split('_')
        interfaceId = "%s_%s_%s" % (splitData[0],splitData[1],(int(splitData[2])+1))
        return interfaceId

    @staticmethod
    def getVersionInterfaceId(versionName):
        try:
            interfaceMaxId = TbVersionHttpInterface.objects.filter(versionName_id=versionName).latest('id').interfaceId
        except Exception as e:
            interfaceId = 'HTTP_INTERFACE_1'
            return interfaceId
        splitData = interfaceMaxId.split('_')
        interfaceId = "%s_%s_%s" % (splitData[0],splitData[1],(int(splitData[2])+1))
        return interfaceId

    @staticmethod
    def getInterfaceForInterfaceId(interfaceId):
        return TbHttpInterface.objects.filter(interfaceId=interfaceId, state=1)[0]

    @staticmethod
    def getVersionInterfaceForInterfaceId(interfaceId,versionName):
        return TbVersionHttpInterface.objects.filter(interfaceId=interfaceId,versionName_id=versionName)[0]

    @staticmethod
    def interfaceSaveEdit(request,interfaceData):
        interfaceObj = TbHttpInterface.objects.filter(id=interfaceData["id"])
        if interfaceObj[0].addBy.loginName != request.session.get("loginName"):
            changeLog = TbUserChangeLog()
            changeLog.version = request.session.get("version")
            changeLog.loginName = request.session.get("loginName")
            changeLog.otherLoginName = interfaceObj[0].addBy.loginName
            changeLog.type = 1
            changeLog.beforeChangeData = dictToJson(dbModelToDict(interfaceObj[0]))
            changeLog.afterChangeData = dictToJson(interfaceData)
            changeLog.dataId = interfaceObj[0].interfaceId
            changeLog.changeDataId = interfaceObj[0].interfaceId
            changeLog.save()
        interfaceSaveEditResule = interfaceObj.update(**interfaceData)
        return interfaceSaveEditResule

    @staticmethod
    def interfaceVersionSaveEdit(interfaceData):
        interfaceSaveEditResule = TbVersionHttpInterface.objects.filter(id=interfaceData["id"]).update(**interfaceData)
        return interfaceSaveEditResule

    @staticmethod
    def taskCheckInterfaceList(interfaceIdList):
        interfaceList = TbHttpInterface.objects.filter(interfaceId__in=interfaceIdList)
        return interfaceList

if __name__ == "__main__":
    print(HTTP_interfaceService.queryPeopleInterface(0,3,"liyc"))

    # print(UserService.getUserByLoginname(UserService.getUsers()[0].loginname))