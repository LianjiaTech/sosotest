
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


from datetime import datetime
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from apps.common.model.Config import Config
from all_models.models.A0002_config import TbConfigHttp,TbEnvUriConf

if __name__ == "__main__":
    tbConfHttp = TbConfigHttp.objects.filter(state = 1)
    print(len(tbConfHttp))
    for tmpConf in tbConfHttp:
        env = tmpConf.httpConfKey
        confDict = Config.getConfDictByString(tmpConf.httpConf)
        for protocal,uriDict in confDict.items():
            for uri,domain in uriDict.items():
                envUri = TbEnvUriConf()
                envUri.httpConfKey = env
                envUri.uriKey = uri
                envUri.requestAddr = domain
                envUri.addBy = tmpConf.addBy
                envUri.save(force_insert=True)
