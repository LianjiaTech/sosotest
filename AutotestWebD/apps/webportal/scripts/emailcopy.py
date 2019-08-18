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
if __name__ == "__main__":
    versionTask = TbVersionTask.objects.filter(versionName="v1807")
    task = TbTask.objects.filter()
    for taskIndex in versionTask:
        taskIndex.emailList = task.filter(taskId=taskIndex.taskId)[0].emailList
        taskIndex.save()
    #     tmp = taskIndex.taskId
    #     print(te)
