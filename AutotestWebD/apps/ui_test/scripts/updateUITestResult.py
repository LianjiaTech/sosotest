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
import re

if __name__ == "__main__":
    execTestList = dbModelListToListDict(TbUITestExecute.objects.filter(execStatus__in=[1,2]))
    for testIndex in execTestList:
        reportLog = "%s/static/%s%s%s" % (
        BASE_DIR.replace("\\", "/"), "ui_test_reports", testIndex["reportDir"], "report.log")

        if os.path.exists(reportLog):
            f = open(reportLog, 'r')
            fileContent = f.read()
            if "DONE:FINISHED" in fileContent:
                print(fileContent)
                resultList = re.findall(r"TestResultJsonString:(.+)TestResultJsonStringEnd",fileContent.replace("\n", "").strip())

                resultJson = json.loads(resultList[0].strip())
                tbModel = TbUITestExecute.objects.filter(id=testIndex["id"]).last()
                tbModel.resultDetail = json.dumps(resultJson)
                tbModel.execStatus = 3
                tbModel.save()
            else:
                print("字符串不存在")
        else:
            print(reportLog)
            print("不是文件")

