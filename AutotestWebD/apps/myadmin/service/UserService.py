import apps.common.func.InitDjango
from all_models.models import TbUser, TbAdminUserPermissionRelation
from apps.common.func.WebFunc import *



class UserService(object):

    @staticmethod
    def getUsers():
        return TbUser.objects.all()

    @staticmethod
    def getUserByLoginname(loginname):
        return TbUser.objects.filter(loginName=loginname)

    @staticmethod
    def updateUser(userData):
        tbModel = TbUser.objects.filter(id=userData["id"])
        tbModel.update(**userData)


if __name__ == "__main__":
     # print(UserService.getUsers()[0])
    #permissionDict = UserPermission.getUserPermissions("liyc", "/interfaceTest/HTTP_InterfaceListCheck")
    #print(permissionDict)
    # print("permissionDict:", permissionDict)
    #print("interfaceDict:", interfaceDict)
     permissionsList = UserPermission.getOthersPermissions("liyc", ['lining02', 'gaozhe', 'qinjp', 'yongwy', 'pengjie', 'tanglu', 'hongln'], "/interfaceTest/HTTP_GlobalTextConfListPage")
     # print("permissionsList:", permissionsList)
  #  print(UserService.getUserByLoginname(UserService.getUsers()[0].loginName))
