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

if __name__ == "__main__":
    envData = dbModelListToListDict(TbWebPortalStandardEnv.objects.filter(state=1,rmiIsShow=1))
    uri = "http://0.0.0.0"
    result = {}
    for envIndex in envData:
        url = envIndex["rmiKey"]
        link = uri+ "/" + url +"/service-coverage.json"
        # print(link)
        try:
            r = requests.get(url=link,timeout=5)
        # print(r.text)

            rJson = json.loads(r.text)
        except Exception as e :
            rJson = []
        jsonLast = {"summaryAt":datetime.datetime.now().strftime('%Y-%m-%d 23:59:59'),"anlysisModel":[]}
        if rJson:
            jsonLast = rJson[-1]
            for jsonIndex in jsonLast["anlysisModel"]:
                jsonIndex["env"] = envIndex["rmiKey"]
                if "successNum" in jsonIndex.keys():
                    jsonIndex["testNum"] = jsonIndex["successNum"] + jsonIndex["skipNum"] + jsonIndex["failNum"]
                    jsonIndex["report"] = uri + "/" + jsonIndex["env"] + "/html/coverage-category_" + jsonIndex["category"] + ".html"
                    if jsonIndex["testNum"] != 0:
                        jsonIndex["passRate"] = "%.2f" % (jsonIndex["successNum"] / jsonIndex["testNum"] * 100)
                    else:
                        jsonIndex["passRate"] = "%.2f" % 0
            allService = dbModelListToListDict(TbWebPortalRmiStandardService.objects.all())
            for serviceIndex in allService:
                flag = 0
                for jsonIndex in jsonLast["anlysisModel"]:
                    if serviceIndex["serviceName"] == jsonIndex["category"]:
                        flag = 1
                if flag == 0:
                    jsonLast["anlysisModel"].append({"category":serviceIndex["serviceName"],"passRate":"%.2f" % 0,"successNum":0,"testNum":0,"report":"javascript:void(0)"})
        if envIndex["rmiKey"] not in result.keys():
            result[envIndex["rmiKey"]] = {}
        result[envIndex["rmiKey"]] = jsonLast

    dbModule = TbWebPortRMIInterfaceTest()
    dbModule.statisticalTime = datetime.datetime.now()
    dbModule.interfaceDetail = json.dumps(result)
    dbModule.save()

    for dataIndex in result["test-devtest88"]["anlysisModel"]:
        dbCoverageModule = TbWebPorRMIServiceTest()
        dbCoverageModule.classNum = "classNum" in dataIndex.keys() and dataIndex["classNum"] or 0
        dbCoverageModule.classCoverage = "classCoverage" in dataIndex.keys() and dataIndex["classCoverage"] or 0
        dbCoverageModule.methodNum = "methodNum" in dataIndex.keys() and dataIndex["methodNum"] or 0
        dbCoverageModule.methodCoverage = "methodCoverage" in dataIndex.keys() and dataIndex["methodCoverage"] or 0
        if "methodNum" in dataIndex.keys() and dataIndex["methodNum"] != 0:
            dbCoverageModule.coveredRate = "%.2f" % (dataIndex["methodCoverage"] / dataIndex["methodNum"] * 100)
        else:
            dbCoverageModule.coveredRate = "%.2f" % 0
        dbCoverageModule.testNum = "testNum" in dataIndex.keys() and dataIndex["testNum"] or 0
        dbCoverageModule.service = "category" in dataIndex.keys() and dataIndex["category"] or ""
        dbCoverageModule.save()
    print("done!")
