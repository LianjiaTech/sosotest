import django
import sys,os
rootpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))).replace("\\","/")
# print(rootpath)
syspath=sys.path
sys.path=[]
sys.path.append(rootpath) #指定搜索路径绝对目录
sys.path.extend([rootpath+i for i in os.listdir(rootpath) if i[0]!="."])#将工程目录下的一级目录添加到python搜索路径中
sys.path.extend(syspath)


from datetime import datetime
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from apps.common.func.CommonFunc import *

if __name__ == "__main__":
    try:
        TbSource(sourceName="WEB",sourceDesc="WEB").save()
    except:
        pass

    try:
        TbSource(sourceName="APP",sourceDesc="APP").save()
    except:
        pass

    try:
        TbSource(sourceName="Android",sourceDesc="Android").save()
    except:
        pass

    try:
        TbSource(sourceName="iOS",sourceDesc="iOS").save()
    except:
        pass

    try:
        TbSource(sourceName="所有",sourceDesc="所有").save()
    except:
        pass

    try:
        TbSource(sourceName="API",sourceDesc="API").save()
    except:
        pass
    
