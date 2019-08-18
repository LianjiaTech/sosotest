
import django
import sys,os
rootpath = os.path.dirname(os.path.realpath(__file__)).replace("\\","/")
rootpath = rootpath.split("/apps")[0]
# print(rootpath)
syspath=sys.path
sys.path=[]
sys.path.append(rootpath) #指定搜索路径绝对目录
sys.path.extend([rootpath+i for i in os.listdir(rootpath) if i[0]!="."])#将工程目录下的一级目录添加到python搜索路径中
sys.path.extend(syspath)
import apps.common.func.InitDjango
from apps.common.config.permissionConst import *
from all_models.models import *
from apps.common.model.RedisDBConfig import *

if __name__ == "__main__":
    interfaceData = TbAdminInterfacePermissionRelation.objects.all()
    for index in interfaceData:
        try:
            RedisCache().del_data("%s_%s" % (PermissionConst.urlDefaultPermission,index.url))
            RedisCache().del_data("%s_%s" % (PermissionConst.urlAllPermission,index.url))
        except:
            pass



        teamData = TbAdminTeam.objects.all()
        for teamIndex in teamData:
            try:
                RedisCache().del_data("%s_%s_%s" % (PermissionConst.team_url_permission,teamIndex.teamName,index.url))
                print("%s_%s_%s" % (PermissionConst.team_url_permission,teamIndex.teamName,index.url))
            except:
                pass


    userData = TbUser.objects.all()
    for userIndex in userData:
        try:
            RedisCache().del_data("%s_%s" % (PermissionConst.user_permission, userIndex.loginName))
        except:
            pass