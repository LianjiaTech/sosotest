import django
import sys,os,hashlib
rootpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))).replace("\\","/")
rootpath = rootpath.split("/apps")[0]
print(rootpath)
syspath=sys.path
sys.path=[]
sys.path.append(rootpath) #指定搜索路径绝对目录
sys.path.extend([rootpath+i for i in os.listdir(rootpath) if i[0]!="."])#将工程目录下的一级目录添加到python搜索路径中
sys.path.extend(syspath)
from apps.common.func import InitDjango
from all_models.models import *

if __name__ == "__main__":
    tbModel = TbAdminUser()
    tbModel.loginName = "admin"
    pwdMd5 = hashlib.md5()
    pwdMd5.update("admin".encode("utf-8"))
    tbModel.passWord = pwdMd5.hexdigest()
    tbModel.userName = "系统管理员"
    tbModel.superManager = 1
    tbModel.save()