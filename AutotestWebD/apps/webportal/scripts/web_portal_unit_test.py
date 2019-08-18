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
import json,requests
if __name__ == "__main__":
    serviceList = dbModelListToListDict(TbWebPortalUnitTestService.objects.filter(state=1,isShow=1).order_by("level"))

    result = {"serviceList":[]}
    allCode = 0
    coverage = 0
    coverageRate = 0
    for serviceIndex in serviceList:
        serviceDict = {"serviceName":serviceIndex["serviceName"],"status":"NOTRUN","codeNum":0,"coverage":0,"coverageRate":0.0,"uncoverage":0,"reportUrl":"javascript:void(0)"}
        # url = "http://sonarqube.ingageapp.com/api/measures/component_tree?ps=100&s=qualifier%2Cname&baseComponentKey=com.rkhd.ienterprise%3A"+ serviceIndex["serviceName"] +"&metricKeys=ncloc%2Ccode_smells%2Cbugs%2Cvulnerabilities%2Ccoverage%2Cduplicated_lines_density%2Calert_status%2Clines_to_cover&strategy=children"
        url = "http://sonarqube.ingageapp.com/api/measures/component?additionalFields=periods&componentKey=com.rkhd.ienterprise%3A" + serviceIndex["serviceName"] +"&metricKeys=lines_to_cover%2Cuncovered_lines%2Cline_coverage"
        print(url)
        r = requests.get(url)
        try:
            rJson = json.loads(r.text)
            rResult = rJson["component"]["measures"]
            for rIndex in rResult:
                if rIndex["metric"] == "lines_to_cover":
                    serviceDict["codeNum"] = int(rIndex["value"])
                    allCode += int(rIndex["value"])
                    serviceDict["status"] = "RUN"
                    serviceDict["reportUrl"] = "http://sonarqube.ingageapp.com/component_measures/domain/Coverage?id=com.rkhd.ienterprise%3A" + serviceIndex["serviceName"]
                elif rIndex["metric"] == "line_coverage":
                    serviceDict["coverageRate"] = float(rIndex["value"])
                    serviceDict["status"] = "RUN"
                elif rIndex["metric"] == "uncovered_lines":
                    serviceDict["uncoverage"] = int(rIndex["value"])
                    serviceDict["status"] = "RUN"

        except Exception as e:
            print(e)
            serviceDict["codeNum"] = 0
        result["serviceList"].append(serviceDict)
    # print(result)
    for resultIndex in result["serviceList"]:
        if resultIndex["codeNum"] != 0:
            # print(resultIndex)
            resultIndex["coverage"] = resultIndex["codeNum"] - resultIndex["uncoverage"]
            coverage += resultIndex["coverage"]
    # print(result)
    dbModule = TbWebPortalUnitTestGeneralSituation()
    dbModule.codeNum = allCode
    dbModule.coverage = coverage
    if allCode == 0:
        dbModule.coverageRate = "%.2f" % 0
    else:
        dbModule.coverageRate = "%.2f" % (coverage / allCode * 100)
    dbModule.unitTestDetail = json.dumps(result)
    dbModule.statisticalTime = datetime.datetime.now()
    dbModule.save()
    print("done!")
