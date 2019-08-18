import django
import os,time,sys
from threading import Thread,Lock

rootpath = os.path.dirname(os.path.realpath(__file__)).replace("\\","/")
rootpath = rootpath.split("/apps")[0]
# print(rootpath)
syspath=sys.path
sys.path=[]
sys.path.append(rootpath) #指定搜索路径绝对目录
sys.path.extend([rootpath+i for i in os.listdir(rootpath) if i[0]!="."])#将工程目录下的一级目录添加到python搜索路径中
sys.path.extend(syspath)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutotestWebD.settings")# project_name 项目名称
django.setup()

from all_models.models import TbUserLog
from apps.common.func.CommonFunc import *
from django.db import connection
import datetime

if __name__ == "__main__":
    try:
        daysAgo = sys.argv[1]
        if isInt(daysAgo):
            daysAgo = int(daysAgo)*-1
            date2daysago = datetime.datetime.now() + datetime.timedelta(days=daysAgo)
            formatTime = date2daysago.strftime('%Y%m%d')
            execSql = "DELETE FROM `tb_user_log` where addTime <= %s235959" % formatTime
            print("Exec sql: %s" % execSql)
            cursor = connection.cursor()
            cursor.execute(execSql)
            print("DONE:delete log successful!")
        else:
            print("Param must be an integer.")
            sys.exit(0)
    except Exception as e:
        print("Need an int parms.")
        sys.exit(0)

