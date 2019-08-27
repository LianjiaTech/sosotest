import apps.common.func.InitDjango
from all_models.models import *
from all_models.models.A0011_version_manage import TbVersionHttpInterface
from django.db import connection
from django.forms.models import model_to_dict
from apps.common.func.CommonFunc import *
from all_models_for_mock.models import *
from apps.common.model.Config import Config
from apps.common.func.send_mail import send_mail

class MockHttpService(object):

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
        return Tb4MockHttp.objects.filter(id=id)[0]

    @staticmethod
    def getInterfaceByMockId(mockId):
        try:
            return Tb4MockHttp.objects.filter(mockId=mockId)[0]
        except:
            return False

    @staticmethod
    def getVersionInterfaceForId(id):
        return TbVersionHttpInterface.objects.filter(id=id)[0]

    @staticmethod
    def getInterfaceForIdToDict(id):
        return dbModelToDict(Tb4MockHttp.objects.filter(id=id)[0])

    @staticmethod
    def getVersionInterfaceForIdToDict(id,versionName):
        return dbModelToDict(TbVersionHttpInterface.objects.filter(id=id,versionName_id=versionName)[0])

    @staticmethod
    def delInterfaceForId(request,id):
        interfaceObj = Tb4MockHttp.objects.filter(id=id)
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
    def addHttpMockInfo(data,addBy):
        newDataDict = {}
        for k, v in data.items():
            newDataDict[k] = data[k]
        newDataDict["addBy"] = addBy
        newDataDict["mockId"] = MockHttpService.getMockId()
        saveInterface = Tb4MockHttp.objects.create(**newDataDict)
        return saveInterface

    @staticmethod
    def addVersionInterface(data,addBy,versionName):
        newDataDict = {}
        for k, v in data.items():
            newDataDict[k] = data[k]
        newDataDict["addBy_id"] = addBy
        newDataDict["interfaceId"] = MockHttpService.getVersionInterfaceId(versionName)
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
    def getMockId():
        try:
            interfaceMaxId = Tb4MockHttp.objects.latest('id').mockId
        except Exception as e:
            interfaceId = 'MOCK_HTTP_1'
            return interfaceId
        splitData = interfaceMaxId.split('_')
        interfaceId = "MOCK_HTTP_%s" % str(int(splitData[-1])+1)
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
        return TbHttpInterface.objects.filter(interfaceId=interfaceId)[0]

    @staticmethod
    def getVersionInterfaceForInterfaceId(interfaceId,versionName):
        return TbVersionHttpInterface.objects.filter(interfaceId=interfaceId,versionName_id=versionName)[0]

    @staticmethod
    def interfaceSaveEdit(request,interfaceData):
        interfaceObj = Tb4MockHttp.objects.filter(mockId=interfaceData["mockId"])
        if interfaceObj:
            if interfaceObj[0].addBy == "" or interfaceObj[0].addBy == None:
                interfaceData['addBy'] = interfaceData['modBy']
        whether_change = False
        for tmpk in interfaceData:
            dstValue = interfaceData[tmpk]
            srcValue = getattr(interfaceObj[0], tmpk)
            if str(dstValue) != str(srcValue):
                whether_change = True
        if whether_change:
            interfaceData["modTime"] = datetime.datetime.now()
            interfaceData["modBy"] = request.session.get("loginName")
            interfaceObj.update(**interfaceData)
            # 发邮件给相关人员
            follower_email = ""
            sql = "select user.email from tb4_mock_follower follower LEFT JOIN tb_user user on follower.follower=user.loginName where follower.mockId='%s'" % interfaceData["mockId"]
            res= executeSqlGetDict(sql)
            for tmpemail in res:
                follower_email += "%s;" % tmpemail["email"]
            follower_email = follower_email.strip(";")
            if follower_email != "":
                subject = "【%s】【%s】已更新，请关注！" % (interfaceData["mockId"], interfaceData["reqUrl"])
                emailhtml = render(None, "mock_server/email.html", interfaceData).content.decode("utf8")
                send_mail(follower_email, subject, emailhtml, sub_type="html")
            return "更新成功"
        else:
            return "没有变更"

    @staticmethod
    def interfaceVersionSaveEdit(interfaceData):
        interfaceSaveEditResule = TbVersionHttpInterface.objects.filter(id=interfaceData["id"]).update(**interfaceData)
        return interfaceSaveEditResule

    @staticmethod
    def taskCheckInterfaceList(interfaceIdList):
        interfaceList = TbHttpInterface.objects.filter(interfaceId__in=interfaceIdList)
        return interfaceList

    @staticmethod
    def getUri(httpConfKey, uriKey,protocol = "HTTP"):
        confObj = TbEnvUriConf.objects.filter(httpConfKey = httpConfKey,state = 1,uriKey = uriKey)
        if confObj:
            reqHost = confObj[0].requestAddr
            return reqHost
        else:
            return ""

    @staticmethod
    def follow(mockid, operate, follower):
        if operate == "follow":
            followinfo = Tb4MockFollower.objects.filter(mockId=mockid,follower=follower).all()
            if followinfo:
                followinfo = followinfo[0]
            else:
                followinfo = Tb4MockFollower(mockId=mockid, follower=follower)
            followinfo.state = 1
            followinfo.save()
            return 10000, "关注成功！"
        elif operate == "cancel":
            followinfo = Tb4MockFollower.objects.filter(mockId=mockid,follower=follower).all()
            if followinfo:
                followinfo = followinfo[0]
            else:
                return False, "施主，未曾关注，何必取消？"
            followinfo.state = 0
            followinfo.save(force_update=True)
            return 10000, "取消关注成功！"
        else:
            return 10012, "错误的操作！"