import django
import sys, os

rootpath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
rootpath = rootpath.split("/apps")[0]
# print(rootpath)
syspath = sys.path
sys.path = []
sys.path.append(rootpath)  # 指定搜索路径绝对目录
sys.path.extend([rootpath + i for i in os.listdir(rootpath) if i[0] != "."])  # 将工程目录下的一级目录添加到python搜索路径中
sys.path.extend(syspath)

from apps.common.func.WebFunc import *
from apps.webportal.services.webPortalService import WebPortalService
from all_models.models import *
from apps.task.services.HTTP_taskService import HTTP_taskService
import json, requests,copy


if __name__ == "__main__":
    tmpSrcRoot = "%s/AutotestWebD/apps/webportal/scripts" % (releaseDir)


    resultList = []
    for index in WebPortalService.scriptList:
        thisResule = {"code": 10000, "msg": "%s 执行成功!" % index}
        output = os.popen('cd %s && python3 %s' % (tmpSrcRoot, index))
        outStr = output.read()
        if "done!" not in outStr:
            thisResule = {"code": 10001, "msg": "%s  执行失败!" % index,
                          "body": 'cd %s && python3 %s' % (tmpSrcRoot, index)}
        resultList.append(thisResule)
    print("done!")
