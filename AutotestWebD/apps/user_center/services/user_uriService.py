import apps.common.func.InitDjango
from all_models.models import TbUserUri
class user_uriService(object):

 
    @staticmethod
    def queryUserUriCount(loginName):
        return len(TbUserUri.objects.filter(addBy=loginName))


    @staticmethod
    def addUserUrl(loginName,uriKey,confLevel):
        addData = TbUserUri()
        addData.loginName_id = loginName
        addData.uriKey_id = uriKey
        addData.conflevel = confLevel
        addData.addBy = loginName
        addData.save()

    @staticmethod
    def queryUserUriRepeat(loginName,uriKey):
        return TbUserUri.objects.filter(uriKey_id=uriKey).filter(addBy=loginName).filter(state=1).order_by("conflevel")
    
    
    @staticmethod
    def queryUserUri(loginName):
        return TbUserUri.objects.filter(addBy=loginName).filter(state=1).order_by("conflevel")

    @staticmethod
    def updateLevel(addData):
        result = TbUserUri.objects.filter(id=addData["id"]).update(**addData)
        return result