import django
import os
import sys
import traceback
import logging
from AutotestWebD.settings import *
from apps.common.func.CommonFunc import *
from collections import *

now_time = datetime.datetime.now()
yes_time = now_time + datetime.timedelta(days=-1)
yes_time_bofore = yes_time.strftime('%Y-%m-%d 00:00:00')
yes_time_after = yes_time.strftime('%Y-%m-%d 23:59:59')
class WebPortalService(object):
    scriptList = ["web_portal_version_action_interface_test.py", "web_portal_platform_coverage.py",
                  "web_portal_action_interface_general_situation.py",
                  "web_portal_openApi_general_situation.py", "web_portal_openApi_interface_test.py",
                  "web_portal_rmi_general_situation.py", "web_portal_rmi_interface_test.py",
                  "web_portal_unit_test.py", "web_portal_ui_test.py", "web_portal_ui_general_situation.py","web_portal_ui_coverage.py"]

    @staticmethod
    def reHtmlGetText(htmlText):
       return re.findall(r">(.+?)<", htmlText)

    #根据版本拿到标准接口的数据
    @staticmethod
    def getVersionStandardData(version):
        versionTb = dbModelToDict(TbVersion.objects.filter(versionName=version)[0])
        if versionTb["type"] == 2:
            versionStandardData = dbModelListToListDict(TbStandardInterface.objects.filter(state=1))
        else:
            versionStandardData = dbModelListToListDict(TbVersionStandardInterface.objects.filter(versionName=version,state=1))
        return versionStandardData
    @staticmethod
    def getYesterdayAddInterfaceNum():
        # now_time = datetime.datetime.now()
        # yes_time = now_time + datetime.timedelta(days=-1)
        # yes_time_bofore = yes_time.strftime('%Y-%m-%d 00:00:00')
        # yes_time_after = yes_time.strftime('%Y-%m-%d 23:59:59').
        yesterdayData = TbStandardInterface.objects.filter(addTime__gt=yes_time_bofore).filter(addTime__lt=yes_time_after).filter(state=1)
        return yesterdayData

    @staticmethod
    def getStandardCount():
        return TbStandardInterface.objects.filter(state=1)

    @staticmethod
    def getHttpTestGeneralSituation():
        # now_time = datetime.datetime.now()
        # yes_time = now_time + datetime.timedelta(days=-1)
        # yes_time_bofore = yes_time.strftime('%Y-%m-%d 00:00:00')
        # yes_time_after = yes_time.strftime('%Y-%m-%d 23:59:59')
        resultData = TbWebPortalActionInterfaceGeneralSituation.objects.filter(state=1)
        return resultData

    @staticmethod
    def getInterfaceTest():
        # now_time = datetime.datetime.now()
        # yes_time = now_time + datetime.timedelta(days=-1)
        # yes_time_bofore = yes_time.strftime('%Y-%m-%d 00:00:00')
        # yes_time_after = yes_time.strftime('%Y-%m-%d 23:59:59')
        allBlDict = dbModelListToListDict(TbBusinessLine.objects.filter(state=1))
        resultDict = {}
        for blIndex in allBlDict:
            print(blIndex)
            data = dbModelListToListDict(TbWebPortalActionInterfaceTest.objects.filter(businessLine=blIndex["bussinessLineName"]).filter(state=1))[-1]
            # data = dbModelListToListDict(TbWebPortalActionInterfaceTest.objects.filter(businessLine=blIndex["bussinessLineName"]).filter(state=1))[-1]

            data["envTestDetail"] = json.loads(data["envTestDetail"])
            resultDict[blIndex["bussinessLineName"]] = data
        return resultDict

    @staticmethod
    def getCoverageRate():
        # now_time = datetime.datetime.now()
        # yes_time = now_time + datetime.timedelta(days=-1)
        # yes_time_bofore = yes_time.strftime('%Y-%m-%d 00:00:00')
        # yes_time_after = yes_time.strftime('%Y-%m-%d 23:59:59')
        allBlDict = dbModelListToListDict(TbBusinessLine.objects.filter(state=1))
        resultDict = OrderedDict()
        notSortDict = {}
        sortDict = {}
        for blIndex in allBlDict:
            data = dbModelListToListDict(TbWebPortalPlatformInterfaceCovered.objects.filter(businessLine=blIndex["bussinessLineName"]).filter(state=1))[-1]
            if data:
                sortDict[blIndex["bussinessLineName"]] = data["coverage"]
                notSortDict[blIndex["bussinessLineName"]] = data
                # resultDict[blIndex["bussinessLineName"]] = data
            else:
                sortDict[blIndex["bussinessLineName"]] = 0
                notSortDict[blIndex["bussinessLineName"]] = data
                # resultDict[blIndex["bussinessLineName"]] = {}

        atlist = OrderedDict(sorted(sortDict.items(), key=lambda x: x[1], reverse=True))
        for item in atlist:
            resultDict[item] = notSortDict[item]

        return resultDict

    @staticmethod
    def getOpenApiIntrefaceTest():
        allBlDict = dbModelListToListDict(TbOpenApiBusinessLine.objects.filter(state=1))
        resultDict = {}
        for blIndex in allBlDict:
            data = TbWebPortOpenApiInterfaceTest.objects.filter(state=1,businessLine=blIndex["businessLineName"]).last()
            if data:
                dataDict = dbModelToDict(data)
                dataDict["interfaceDetail"] = json.loads(dataDict["interfaceDetail"])
                resultDict[blIndex["businessLineName"]] = dataDict
            else:
                resultDict[blIndex["businessLineName"]] = {}
                
        return resultDict
    
    @staticmethod
    def getOpenApiBlTest():
        allBlDict = dbModelListToListDict(TbOpenApiBusinessLine.objects.filter(state=1))
        resultDict = {}
        for blIndex in allBlDict:
            data = TbWebPortOpenApiBlTest.objects.filter(state=1, businessLine=blIndex["businessLineName"]).last()
            if data:
                dataDict = dbModelToDict(data)
                resultDict[blIndex["businessLineName"]] = dataDict
            else:
                resultDict[blIndex["businessLineName"]] = {}
        
        return resultDict
    
    @staticmethod
    def getRencentDays():
        dateList = []
        numList = [-7, -6, -5, -4, -3, -2, -1]

        for num in numList:
            date = (datetime.date.today() + datetime.timedelta(days=num)).strftime("%Y-%m-%d")
            dateList.append(date)
        return dateList
    
    @staticmethod
    def getAllHttpConf():
        allEnvlist = TbWebPortalStandardEnv.objects.filter(state=1, actionIsShow=1).order_by("lineSort")
        httpConfKeysList = []
        for env in allEnvlist:
            if env.alias not in httpConfKeysList:
                httpConfKeysList.append(env.httpConfKey)
        return httpConfKeysList

    @staticmethod
    def getEnvVersion(httpConfKey):
        version = TbWebPortalStandardEnv.objects.get(httpConfKey=httpConfKey, state=1).version
        return version


    @staticmethod
    def getAllEnvAlias():
        allEnvlist = TbWebPortalStandardEnv.objects.filter(state=1, actionIsShow=1).order_by("lineSort")
        envAliasDict = {}
        for env in allEnvlist:
            envAliasDict[env.httpConfKey] = env.alias + "(" + env.version + ")"
        return envAliasDict
    



if __name__ == "__main__":
    # print(dbModelListToListDict(WebPortalService.getYesterdayAddInterfaceNum()))
    pass
