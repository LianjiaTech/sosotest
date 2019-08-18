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

from apps.common.func.WebFunc import *
from apps.webportal.services.webPortalService import WebPortalService
from all_models.models import *
from apps.task.services.HTTP_taskService import HTTP_taskService
import json

def getAllPassrate(argv):
    if len(argv) == 1:
        num = 1
    else:
        num = int(argv[-1])
    httpConfKeysList = WebPortalService.getAllHttpConf()
    execStatus = [3, 4]
    numList = []
    startExeTime = datetime.datetime.now()
    i = 1
    while (i <= num):
        numList.append(-i)
        i = i + 1
    numList.reverse()
    for num in numList:

        date = datetime.datetime.today() + datetime.timedelta(days=num)
        zeroToday = date - datetime.timedelta(hours=date.hour, minutes=date.minute,
                                              seconds=date.second,
                                              microseconds=date.microsecond)
        # 获取23:59:59
        lastToday = zeroToday + datetime.timedelta(hours=23, minutes=59, seconds=59)

        envPassRateList = []
        for httpConf in httpConfKeysList:

            totalNum = 0
            passNum = 0
            version = WebPortalService.getEnvVersion(httpConf)
            type = TbVersion.objects.get(versionName=version, state=1).type
            taskList = TbWebPortalStandardTask.objects.filter(version=version, state=1)

            for task in taskList:
                if type == 2:
                    taskExecuteResult = TbTaskExecute.objects.filter(version="CurrentVersion",
                                                                     taskId=task.taskId,
                                                                     httpConfKey=httpConf,
                                                                     execTime__range=(zeroToday, lastToday),
                                                                     execStatus__in=execStatus, state=1)
                else:
                    taskExecuteResult = TbTaskExecute.objects.filter(version=version, taskId=task.taskId,
                                                                     httpConfKey=httpConf,
                                                                     execTime__range=(zeroToday, lastToday),
                                                                     execStatus__in=execStatus, state=1)

                for taskExecute in taskExecuteResult:
                    testResultMsg = taskExecute.testResultMsg

                    if not isJson(testResultMsg) or "totalExecuteSummary" not in json.loads(testResultMsg).keys():
                        continue
                    num = (json.loads(testResultMsg))["totalExecuteSummary"]
                    totalNum += num["total"]
                    passNum += num["pass"]

            if totalNum == 0:
                # passRate = '%.2f%%' % (0)
                passRate = 0
            else:
                # passRate = '%.2f%%' % ((passNum / totalNum) * 100)
                passRate = (passNum / totalNum) * 100
            alias = TbWebPortalStandardEnv.objects.get(state=1, httpConfKey=httpConf).alias
            version = TbWebPortalStandardEnv.objects.get(state=1, httpConfKey=httpConf).version
            envPassRateList.append({"env": httpConf, "passRate": passRate, "date": date.strftime("%Y-%m-%d"),
                                    "alias": alias + "(" + version + ")", "passNum": passNum, "totalNum": totalNum})

        endExeTime = datetime.datetime.now()

        passRate = TbWebPortalAllPassRate()

        passRate.testResultMsg = json.dumps(envPassRateList)
        passRate.state = 1
        passRate.execTakeTime = (endExeTime - startExeTime).seconds
        passRate.save()

if __name__ == "__main__":
    getAllPassrate(sys.argv)
