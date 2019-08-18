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
import json

def getServiceInterfaceCoverage():
    serviceNameList = srcFolders
    standardDataDict = {}
    for serviceName in serviceNameList:
        print("serviceName:", serviceName)
        execSql = "SELECT interfaceUrl,serviceName FROM tb_standard_interface WHERE state=1 AND apiStatus=1 AND serviceName='%s'" % serviceName
        standardData = executeSqlGetDict(execSql)
        print("standardData:", standardData)
        if not standardData:
            print("33333333333333")
            standardDataDict[serviceName] = {"dataList": [], "serviceInterfaceCount": 0, "serviceInterfaceIsCoveredCount": 0, "moduleDict": {}}
        else:
            # 生成标准dict
            for tmpInterfaceDict in standardData:
                tmpServiceName = tmpInterfaceDict['serviceName']
                if tmpServiceName not in standardDataDict.keys():
                    standardDataDict[tmpServiceName] = {"dataList": [], "serviceInterfaceCount": 0, "serviceInterfaceIsCoveredCount": 0, "moduleDict": {}}
                standardDataDict[tmpServiceName]['dataList'].append(tmpInterfaceDict)
                standardDataDict[tmpServiceName]['serviceInterfaceCount'] += 1
                httpInterface = TbHttpInterface.objects.filter(state=1, url=tmpInterfaceDict["interfaceUrl"])
                httpTestcaseStep = TbHttpTestcaseStep.objects.filter(state=1, url=tmpInterfaceDict["interfaceUrl"])
                if len(httpInterface) != 0 or len(httpTestcaseStep) != 0:
                    standardDataDict[tmpServiceName]['serviceInterfaceIsCoveredCount'] += 1
    print("standardDataDict:", standardDataDict)
    return standardDataDict


if __name__ == "__main__":
    now_time = datetime.datetime.now()
    yes_time = now_time + datetime.timedelta(-1)
    standardDataDict = getServiceInterfaceCoverage()
    for standardData in standardDataDict:
        coveredResult = TbWebPortalServiceInterfaceCovered.objects.filter(serviceName=standardData, state=1)
        if len(coveredResult) != 0:
            coveredResult.delete()
            serviceInterfaceCoverage = TbWebPortalServiceInterfaceCovered()
            serviceInterfaceCoverage.serviceName = standardData
            serviceInterfaceCoverage.standardInterfaceNum = standardDataDict[standardData]["serviceInterfaceCount"]
            serviceInterfaceCoverage.coveredInterfaceNum = standardDataDict[standardData][
                "serviceInterfaceIsCoveredCount"]
            serviceInterfaceCoverage.serviceTestDetail = json.dumps(standardDataDict[standardData]["dataList"])
            if standardDataDict[standardData]["serviceInterfaceCount"] == 0:
                serviceInterfaceCoverage.coverage = "%.2f" % 0
            else:
                serviceInterfaceCoverage.coverage = "%.2f" % ((standardDataDict[standardData][
                                                                   "serviceInterfaceIsCoveredCount"] /
                                                               standardDataDict[standardData][
                                                                   "serviceInterfaceCount"]) * 100)
            serviceInterfaceCoverage.state = 1
            serviceInterfaceCoverage.statisticalTime = yes_time
            serviceInterfaceCoverage.save()
        else:
            serviceInterfaceCoverage = TbWebPortalServiceInterfaceCovered()
            serviceInterfaceCoverage.serviceName = standardData
            serviceInterfaceCoverage.standardInterfaceNum = standardDataDict[standardData]["serviceInterfaceCount"]
            serviceInterfaceCoverage.coveredInterfaceNum = standardDataDict[standardData]["serviceInterfaceIsCoveredCount"]
            serviceInterfaceCoverage.serviceTestDetail = json.dumps(standardDataDict[standardData]["dataList"])
            if standardDataDict[standardData]["serviceInterfaceCount"] == 0:
                serviceInterfaceCoverage.coverage = "%.2f" % 0
            else:
                serviceInterfaceCoverage.coverage = "%.2f" % ((standardDataDict[standardData]["serviceInterfaceIsCoveredCount"] / standardDataDict[standardData]["serviceInterfaceCount"]) * 100)
            serviceInterfaceCoverage.state = 1
            serviceInterfaceCoverage.statisticalTime = yes_time
            serviceInterfaceCoverage.save()