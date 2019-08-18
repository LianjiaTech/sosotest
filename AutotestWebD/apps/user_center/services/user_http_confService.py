import apps.common.func.InitDjango
from all_models.models import TbUserHttpconf
class user_http_confService(object):

    @staticmethod
    def delUserHttpConf(id):
        delResult = TbUserHttpconf.objects.get(id=id)
        delResult.state = 0
        delResult.save()

    @staticmethod
    def delAllUserHttpConf(addBy):
        TbUserHttpconf.objects.filter(addBy=addBy).delete()

    @staticmethod
    def getUserHttpConf(id):
        return TbUserHttpconf.objects.filter(id=id)[0]

    @staticmethod
    def addUserHttpConf(loginName,httpConfKey,confLevel):
        addData = {}
        addData["loginName_id"] = loginName
        addData["httpConfKey_id"] = httpConfKey
        addData["conflevel"] = confLevel
        addData["addBy_id"] = loginName
        return TbUserHttpconf.objects.create(**addData)


    @staticmethod
    def editUserHttpConf(varData):
        varDBData = TbUserHttpconf.objects.get(id=varData["id"])
        varDBData.httpConfKey = varData["httpConfKey"]
        varDBData.loginName = varData["addBy"]
        varDBData.addBy_id = varData["addBy"]
        varDBData.conflevel = varData["conflevel"]
        varDBData.save()

    @staticmethod
    def queryUserHttpConfCount(loginName):
        return len(TbUserHttpconf.objects.filter(addBy_id=loginName))

    @staticmethod
    def queryUserHttpConfRepeat(loginName,httpConfKey):
        return TbUserHttpconf.objects.filter(httpConfKey_id=httpConfKey).filter(addBy_id=loginName).filter(state=1).order_by("conflevel")

    @staticmethod
    def queryUserHttpConf(loginName):
        return TbUserHttpconf.objects.filter(addBy_id=loginName).filter(state=1).order_by("conflevel")

    @staticmethod
    def updateLevel(addData):
        result = TbUserHttpconf.objects.filter(id=addData["id"]).update(**addData)
        return result

if __name__ == "__main__":
    # print((HTTP_test_caseService.getTestCaseForIdToDict("23")))
    # print(UserService.getUserByLoginname(UserService.getUsers()[0].loginname))
    # HTTP_test_caseService.testCaseAdd("")
    pass

