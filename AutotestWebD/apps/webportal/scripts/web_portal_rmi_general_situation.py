import django
import sys,os
rootpath = os.path.dirname(os.path.realpath(__file__)).replace("\\","/")
rootpath = rootpath.split("/apps")[0]
syspath=sys.path
sys.path=[]
sys.path.append(rootpath) #指定搜索路径绝对目录
sys.path.extend([rootpath+i for i in os.listdir(rootpath) if i[0]!="."])#将工程目录下的一级目录添加到python搜索路径中
sys.path.extend(syspath)

from apps.common.func.WebFunc import *
from all_models.models import *
import requests,datetime,json


def getStandardEnv():
    TbWebPortalRmiStandardService.objects.all().delete()
    envName = "/test-devtest88"
    url = "http://0.0.0.0" + envName +"/service-coverage.json"
    # print(url)
    try:
        r = requests.get(url=url,timeout=5)

        rJson = json.loads(r.text)
    except Exception as e :
        rJson = []
    if rJson:
        rjsonLast = rJson[-1]
    else:
        rjsonLast = {}
    for index in rjsonLast["anlysisModel"]:
        dbModule = TbWebPortalRmiStandardService()
        dbModule.serviceName = index["category"]
        dbModule.save()

if __name__ == "__main__":
    getStandardEnv()
    envData = dbModelListToListDict(TbWebPortalStandardEnv.objects.filter(state=1))
    uri = "http://0.0.0.0"
    url = "/test-devtest88/summary.json"
    # print(uri + url)
    r = requests.get(uri + url)
    try:
        rJson = json.loads(r.text)
    except Exception as e:
        rJson = []

    if rJson:
        jsonLast = rJson[-1]
    else:
        jsonLast = {}
    dbModule = TbWebPortRMIGeneralSituation()
    dbModule.coverage = "coverage" in jsonLast.keys() and jsonLast["coverage"] or 0
    dbModule.methodTotal = "methodTotal" in jsonLast.keys() and jsonLast["methodTotal"] or 0
    dbModule.totalTest = "totalTest" in jsonLast.keys() and jsonLast["totalTest"] or 0
    dbModule.summaryAt = "summaryAt" in jsonLast.keys() and jsonLast["summaryAt"] or datetime.datetime.now()
    dbModule.failedNum = "failedNum" in jsonLast.keys() and jsonLast["failedNum"] or 0
    dbModule.passedNum = "passedNum" in jsonLast.keys() and jsonLast["passedNum"] or 0
    dbModule.skippedNum = "skippedNum" in jsonLast.keys() and jsonLast["skippedNum"] or 0
    dbModule.save()
    print("done!")
