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
from all_models.models import *
from datetime import datetime, timedelta

def cpReportToAws():
    d = datetime.now() - timedelta(days=8)
    # print(len(TbTaskExecute.objects.filter(state=1)))
    allTaskExecuteData = TbTaskExecute.objects.filter( state=1,testReportUrl__istartswith="/report").exclude(testReportUrl="")
    for executeIndex in allTaskExecuteData:
        reportFile = "%s/AutotestWebD%s" % (rootDir, executeIndex.testReportUrl)
        if os.path.exists(reportFile):
            reportFileName = reportFile.split("/")[-1]
            try:
                os.system("aws s3 cp %s s3://test-team/http_interface_report/" % reportFile)
            except:
                print(traceback.format_exc())
            executeIndex.testReportUrl = "https://test.domain.com/http_interface_report/%s" % reportFileName
            executeIndex.save()
            # os.remove(reportFile)
            reportDirName = reportFile.split("/")[:-1]
            # if not os.listdir(reportDirName):
            #     print(reportDirName)
                # os.remove(reportDirName)


if __name__ == "__main__":
    cpReportToAws()