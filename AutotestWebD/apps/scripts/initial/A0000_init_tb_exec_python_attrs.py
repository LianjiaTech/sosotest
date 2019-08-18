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
    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE `tb_exec_python_attrs`")

    insSqlList = [
        """insert into tb_exec_python_attrs(execPythonAttr,execPythonDesc,execPythonValue,state,addTime,modTime) VALUES("importString","import的第三方库在所有的package中","#字符串处理相关的库
import json,re,jsonpath,hashlib,ast
from urllib import parse
from functools import reduce
from bs4 import BeautifulSoup
#时间处理相关的库
import datetime,time,calendar
#数学处理
import math,cmath,decimal
#造假数据
from faker import Faker
#web请求相关
import requests
#异常处理
import traceback
#数据库相关
import pymysql,redis
from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError",1,"%s","%s")""" % (get_current_time(),get_current_time()),
        """insert into tb_exec_python_attrs(execPythonAttr,execPythonDesc,execPythonValue,state,addTime,modTime) VALUES("timeoutString","timeout在关键字EXEC_PYTHON中","10",1,"%s","%s")""" % (get_current_time(),get_current_time()),
        """insert into tb_exec_python_attrs(execPythonAttr,execPythonDesc,execPythonValue,state,addTime,modTime) VALUES("timoutForPythonMode","timeout for python模式","300",1,"%s","%s")""" % (
        get_current_time(), get_current_time()),
        """insert into tb_exec_python_attrs(execPythonAttr,execPythonDesc,execPythonValue,state,addTime,modTime) VALUES("timoutForSelfKeyword","timeout for 自定义关键字","60",1,"%s","%s")""" % (
        get_current_time(), get_current_time()),
        """insert into tb_exec_python_attrs(execPythonAttr,execPythonDesc,execPythonValue,state,addTime,modTime) VALUES("timoutForMockAdvancedMode","timeout for mock的高级模式","30",1,"%s","%s")""" % (
        get_current_time(), get_current_time()),
    ]
    for tmpSql in insSqlList:
        try:
            cursor.execute(tmpSql)
        except:
            print("inserted!")