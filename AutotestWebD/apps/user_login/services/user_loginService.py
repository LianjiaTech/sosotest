import apps.common.func.InitDjango
from all_models.models import TbUser
class UserLoginService(object):

    @staticmethod
    def getUsers():
        return TbUser.objects.all()

    @staticmethod
    def getUserByLoginname(loginName):
        return TbUser.objects.filter(loginName=loginName)

    @staticmethod
    def getUserLoginMsg(loginName,pwd):
        return TbUser.objects.filter(loginName=loginName,pwd=pwd)

    @staticmethod
    def updateMd5(loginName,token):
        user = TbUser.objects.get(loginName=loginName)
        user.token = token
        user.save()

    @staticmethod
    def updatePwd(loginName,newPwd):
        user = TbUser.objects.get(loginName=loginName)
        user.pwd = newPwd
        user.save()

if __name__ == "__main__":

    # for user in TbUser.objects.all():
    #     print(user.loginname)
    # print(TbUser.objects.all())
    # print(UserService.getUsers()[0].loginname)
    # print(UserService.getUserByLoginname(UserService.getUsers()[0].loginname))
    if(UserLoginService.getUserLoginMsg("liycd","e10adc3949ba59abbe56e057f20f883e")):

        print(UserLoginService.getUserLoginMsg("liycd","e10adc3949ba59abbe56e057f20f883e"))
    else:
        print("fail")