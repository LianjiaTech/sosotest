import os
import sys

rootpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))).replace("\\","/")
print(rootpath)
syspath=sys.path
sys.path=[]
sys.path.append(rootpath) #指定搜索路径绝对目录
sys.path.extend([rootpath+i for i in os.listdir(rootpath) if i[0]!="."])#将工程目录下的一级目录添加到python搜索路径中
sys.path.extend(syspath)

from apps.common.model.RedisDBConfig import RedisCache

if __name__ == "__main__":
    #清除python引用的所有缓存，下次加载重新刷新
    RedisCache().del_data("python_mode_functions")
    RedisCache().del_data("python_third_libs")
    RedisCache().del_data("python_timeout_timeoutString")
    RedisCache().del_data("python_timeout_timoutForMockAdvancedMode")
    RedisCache().del_data("python_timeout_timoutForSelfKeyword")
    RedisCache().del_data("python_timeout_timoutForPythonMode")