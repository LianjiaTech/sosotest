import logging,traceback,os
rootpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).replace("\\","/")
print(rootpath)
from core.tools.DBTool import DBTool
from core.tools.CommonFunc import isInt
from core.tools.RedisTool import RedisTool

serviceRedis = RedisTool()

def getPythonThirdLib():
    importStr = ""
    if not serviceRedis.initRedisConf().existsKey("python_third_libs"):
        with DBTool() as db:
            db.initGlobalDBConf()
            db.setCursorDict(True)
            res = db.execute_sql("select execPythonValue from tb_exec_python_attrs where execPythonAttr = 'importString' ")
            if res:
                importStr = res[0]['execPythonValue']
        RedisTool().initRedisConf().set_data("python_third_libs", importStr)
        print("INIT KEY[python_third_libs] to redis!!!")
    return serviceRedis.initRedisConf().get_data("python_third_libs")

def getKeywordExecPythonTimeout(key = "timeoutString"):
    timeout = 10
    currentKey = "python_timeout_%s" % key
    if not serviceRedis.initRedisConf().existsKey(currentKey):
        with DBTool() as db:
            db.initGlobalDBConf()
            db.setCursorDict(True)
            res2 = db.execute_sql("select execPythonValue from tb_exec_python_attrs where execPythonAttr = '%s' " % key)
            if res2:
                timeoutStr = res2[0]['execPythonValue']
                if isInt(timeoutStr):
                    timeout = int(timeoutStr)
            RedisTool().initRedisConf().set_data(currentKey, timeout)
            print("INIT KEY[%s] to redis!!!" % currentKey)
    return int(serviceRedis.initRedisConf().get_data(currentKey))


def getPythonModeBuildInFromScriptFile():
    if not serviceRedis.initRedisConf().existsKey("python_mode_functions"):
        rootDir = rootpath
        initPythonCode = ""
        pythonFileList = ["A0001_base_functions.py"]
        for tmpFile in pythonFileList:
            with open("%s/core/python_mode_functions/%s" % (rootDir, tmpFile), encoding="utf8") as f:
                codeTobeExecute = f.read().replace("from core.model.CommonAttr import CommonAttr\ncontext = CommonAttr()","")\
                    .replace("from core.python_mode_functions import *", "").strip()
                initPythonCode += codeTobeExecute + "\n"
        RedisTool().initRedisConf().set_data("python_mode_functions", initPythonCode)
        print("INIT KEY[python_mode_functions] to redis!!!")
    return serviceRedis.initRedisConf().get_data("python_mode_functions")


