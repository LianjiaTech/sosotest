import apps.common.func.InitDjango
from all_models.models import TbUser
class UserService(object):

    @staticmethod
    def getUsers():
        return TbUser.objects.all()

    @staticmethod
    def getUserByLoginname(loginname):
        return TbUser.objects.filter(loginname=loginname)

    @staticmethod
    def updateUser(userData):
        tbModel = TbUser.objects.filter(id=userData["id"])
        tbModel.update(**userData)

if __name__ == "__main__":
    print(UserService.getUsers()[0].loginname)
    print(UserService.getUserByLoginname(UserService.getUsers()[0].loginname))