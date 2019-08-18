from apps.common.func.CommonFunc import executeSqlGetDict, isInt
from apps.common.model.RedisDBConfig import RedisCache

serviceRedis = RedisCache()

def getPythonThirdLib():
    importStr = ""
    if not serviceRedis.existsKey("python_third_libs"):
        res = executeSqlGetDict("select execPythonValue from tb_exec_python_attrs where execPythonAttr = 'importString' ")
        if res:
            importStr = res[0]['execPythonValue']
        serviceRedis.set_data("python_third_libs", importStr)
        print("INIT KEY[python_third_libs] to redis!!!")
    return serviceRedis.get_data("python_third_libs")

def getKeywordExecPythonTimeout(key = "timeoutString"):
    timeout = 10
    currentKey = "python_timeout_%s" % key
    if not serviceRedis.existsKey(currentKey):
        res2 = executeSqlGetDict("select execPythonValue from tb_exec_python_attrs where execPythonAttr = '%s' " % key)
        if res2:
            timeoutStr = res2[0]['execPythonValue']
            if isInt(timeoutStr):
                timeout = int(timeoutStr)
            serviceRedis.set_data(currentKey, timeout)
            print("INIT KEY[%s] to redis!!!" % currentKey)
    return int(serviceRedis.get_data(currentKey))
