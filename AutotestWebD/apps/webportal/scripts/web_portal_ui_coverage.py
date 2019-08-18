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



    #
    dataDict = {}

    jiraBlList = dbModelListToListDict(TbJiraBusinessLine.objects.filter(state=1))
    # print(jiraBlList)
    jiraModuleList = dbModelListToListDict(TbjiraModule.objects.filter(state=1))

    for jiraBlIndex in jiraBlList:
        # print(jiraBlIndex)
        #查出平台有没有jira的这个业务线
        jiraBlData = TbJiraBusinessLinePlatFormRelation.objects.filter(jiraBusinessLineId_id=jiraBlIndex["id"]).last()
        if jiraBlData:
            blData = jiraBlData.platformBusinessLineId
            dataDict[blData.bussinessLineName] = {"moduleDict":{},"jiraBLName":jiraBlIndex["businessLineName"]}
            bl_module_relation_list = TbBusinessLineModuleRelation.objects.filter(businessLineId=blData)

            #查出业务线关联的模块
            for jiraModuleIndex in jiraModuleList:
                jiraModuleData = TbJiraModulePlatFormRelation.objects.filter(jiraModuleId_id=jiraModuleIndex["id"]).last()
                if jiraModuleData:
                    for PLMdIndex in bl_module_relation_list:
                        if jiraModuleData.platformModuleId == PLMdIndex.moduleId :
                            if jiraModuleData.platformModuleId.moduleName not in dataDict[blData.bussinessLineName]["moduleDict"].keys():
                                dataDict[blData.bussinessLineName]["moduleDict"][jiraModuleData.platformModuleId.moduleName] = {"jiraModuleName" : [jiraModuleData.jiraModuleId.moduleName]}
                            else:
                                dataDict[blData.bussinessLineName]["moduleDict"][
                                    jiraModuleData.platformModuleId.moduleName]["jiraModuleName"].append(jiraModuleData.jiraModuleId.moduleName)
    #标准字典生成完毕-------------------------------------------


    loginUrl = 'http://jira.ingageapp.com/login.jsp'
    loginFormData = {"os_username": "liyc", "os_password": "liyc"}
    lr = requests.post(url=loginUrl, data=loginFormData)
    JSESSIONID = lr.cookies.get("JSESSIONID")
    url = "http://jira.ingageapp.com/rest/gadget/1.0/twodimensionalfilterstats/generate?filterId=filter-13452&xstattype=customfield_11435&showTotals=true&sortDirection=desc&sortBy=total&ystattype=components&numberToShow=200&_=1524233147860"
    headers = {"cookie": "JSESSIONID=%s; atlassian.xsrf.token=%s; AWSELB=%s" % (
    lr.cookies.get("JSESSIONID"), lr.cookies.get("atlassian.xsrf.token"), lr.cookies.get("AWSELB"))}
    r = requests.get(url=url, headers=headers)
    requestJson = json.loads(r.text)
    # print( r.text)
    # print(requestJson)
    for blIndexKey,blIndexValue in dataDict.items():
        blIndexValue["coverDetail"] = {"allTestCaseNum": 0, "allAutoMetedNum": 0, "coverageRate": float("%.2f" % 0)}
        blIndexValue["terminal"] = {}
        blIndexValue["terminal"]["IOS"] = {"allTestCaseNum":0, "allAutoMetedNum":0,"coverageRate": float("%.2f" % 0)}
        blIndexValue["terminal"]["Android"] = {"allTestCaseNum":0, "allAutoMetedNum":0,"coverageRate": float("%.2f" % 0)}
        blIndexValue["terminal"]["Web"] = {"allTestCaseNum":0, "allAutoMetedNum":0,"coverageRate": float("%.2f" % 0)}
        for mdIndexKey,mdIndexValue in blIndexValue["moduleDict"].items():

            mdIndexValue["terminal"] = {}
            mdIndexValue["terminal"]["IOS"] = {"allTestCaseNum": 0, "allAutoMetedNum": 0, "coverageRate": float("%.2f" % 0)}
            mdIndexValue["terminal"]["Android"] = {"allTestCaseNum": 0, "allAutoMetedNum": 0,"coverageRate": float("%.2f" % 0)}
            mdIndexValue["terminal"]["Web"] = {"allTestCaseNum": 0, "allAutoMetedNum": 0, "coverageRate": float("%.2f" % 0)}
            mdIndexValue["coverDetail"] = {"allTestCaseNum":0,"allAutoMetedNum":0,"coverageRate":float("%.2f" % 0)}
            for requestIndex in requestJson["rows"]:
                requestModuleName = WebPortalService.reHtmlGetText(requestIndex["cells"][0]["markup"])
                if len(requestModuleName) > 0 and requestModuleName[0] in mdIndexValue["jiraModuleName"]:
                    allTestCaseNum = int(WebPortalService.reHtmlGetText(requestIndex["cells"][5]["markup"])[0])
                    #计算IOS
                    iosAutoMetedNum = int(WebPortalService.reHtmlGetText(requestIndex["cells"][3]["markup"])[0])
                    mdIndexValue["terminal"]["IOS"]["allTestCaseNum"] += allTestCaseNum
                    mdIndexValue["terminal"]["IOS"]["allAutoMetedNum"] += iosAutoMetedNum
                    mdIndexValue["terminal"]["IOS"]["coverageRate"] = float("%.2f" % 0)


                    mdIndexValue["coverDetail"]["allTestCaseNum"] += allTestCaseNum
                    mdIndexValue["coverDetail"]["allAutoMetedNum"] += iosAutoMetedNum
                    blIndexValue["coverDetail"]["allTestCaseNum"] += allTestCaseNum
                    blIndexValue["coverDetail"]["allAutoMetedNum"] += iosAutoMetedNum
                    blIndexValue["terminal"]["IOS"]["allTestCaseNum"] += allTestCaseNum
                    blIndexValue["terminal"]["IOS"]["allAutoMetedNum"] += iosAutoMetedNum

                    #计算Android
                    androidAutoMetedNum = int(WebPortalService.reHtmlGetText(requestIndex["cells"][1]["markup"])[0])
                    mdIndexValue["terminal"]["Android"]["allTestCaseNum"] += allTestCaseNum
                    mdIndexValue["terminal"]["Android"]["allAutoMetedNum"] += androidAutoMetedNum
                    mdIndexValue["terminal"]["Android"]["coverageRate"] = float("%.2f" % 0)
                    # mdIndexValue["terminal"]["Android"] = {"allTestCaseNum": allTestCaseNum,"allAutoMetedNum": androidAutoMetedNum, "coverageRate": float("%.2f" % 0)}

                    mdIndexValue["coverDetail"]["allTestCaseNum"] += allTestCaseNum
                    mdIndexValue["coverDetail"]["allAutoMetedNum"] += androidAutoMetedNum
                    blIndexValue["coverDetail"]["allTestCaseNum"] += allTestCaseNum
                    blIndexValue["coverDetail"]["allAutoMetedNum"] += androidAutoMetedNum
                    blIndexValue["terminal"]["Android"]["allTestCaseNum"] += allTestCaseNum
                    blIndexValue["terminal"]["Android"]["allAutoMetedNum"] += androidAutoMetedNum

                    #计算web
                    webAutoMetedNum = int(WebPortalService.reHtmlGetText(requestIndex["cells"][2]["markup"])[0])
                    mdIndexValue["terminal"]["Web"]["allTestCaseNum"] += allTestCaseNum
                    mdIndexValue["terminal"]["Web"]["allAutoMetedNum"] += webAutoMetedNum
                    mdIndexValue["terminal"]["Web"]["coverageRate"] = float("%.2f" % 0)
                    # if mdIndexKey == "销售机会":
                    #     print(mdIndexKey)
                    #     print(requestModuleName[0])
                    #     print(allTestCaseNum)
                    #     print(requestIndex)
                    # mdIndexValue["terminal"]["Web"] = {"allTestCaseNum": allTestCaseNum,"allAutoMetedNum": webAutoMetedNum,"coverageRate": float("%.2f" % 0)}

                    mdIndexValue["coverDetail"]["allTestCaseNum"] += allTestCaseNum
                    mdIndexValue["coverDetail"]["allAutoMetedNum"] += webAutoMetedNum
                    blIndexValue["coverDetail"]["allTestCaseNum"] += allTestCaseNum
                    blIndexValue["coverDetail"]["allAutoMetedNum"] += webAutoMetedNum
                    blIndexValue["terminal"]["Web"]["allTestCaseNum"] += allTestCaseNum
                    blIndexValue["terminal"]["Web"]["allAutoMetedNum"] += webAutoMetedNum

                    if allTestCaseNum > 0 :
                        mdIndexValue["terminal"]["IOS"]["coverageRate"] = float("%.2f" % (mdIndexValue["terminal"]["IOS"]["allAutoMetedNum"] / mdIndexValue["terminal"]["IOS"]["allTestCaseNum"] * 100))
                        mdIndexValue["terminal"]["Android"]["coverageRate"] = float("%.2f" % (mdIndexValue["terminal"]["Android"]["allAutoMetedNum"] / mdIndexValue["terminal"]["Android"]["allTestCaseNum"] * 100))
                        mdIndexValue["terminal"]["Web"]["coverageRate"] = float("%.2f" % (mdIndexValue["terminal"]["Web"]["allAutoMetedNum"] / mdIndexValue["terminal"]["Web"]["allTestCaseNum"] * 100))
            mdCoverDetail = mdIndexValue["coverDetail"]
            if mdCoverDetail["allTestCaseNum"] > 0:
                mdCoverDetail["coverageRate"] = float("%.2f" % (mdCoverDetail["allAutoMetedNum"] / mdCoverDetail["allTestCaseNum"] * 100))

        blCoverDetail = blIndexValue["coverDetail"]
        if blCoverDetail["allTestCaseNum"] > 0:
            blCoverDetail["coverageRate"] = float("%.2f" % (blCoverDetail["allAutoMetedNum"] / blCoverDetail["allTestCaseNum"] * 100))
        if blIndexValue["terminal"]["IOS"]["allTestCaseNum"] > 0:
            blIndexValue["terminal"]["IOS"]["coverageRate"] = float("%.2f" % (blIndexValue["terminal"]["IOS"]["allAutoMetedNum"] /
                                                                        blIndexValue["terminal"]["IOS"]["allTestCaseNum"] * 100))
        if blIndexValue["terminal"]["Android"]["allTestCaseNum"] > 0:
            blIndexValue["terminal"]["Android"]["coverageRate"] = float("%.2f" % (blIndexValue["terminal"]["Android"]["allAutoMetedNum"] /
            blIndexValue["terminal"]["Android"]["allTestCaseNum"] * 100))
        if blIndexValue["terminal"]["Web"]["allTestCaseNum"] > 0:
            blIndexValue["terminal"]["Web"]["coverageRate"] = float("%.2f" % (blIndexValue["terminal"]["Web"]["allAutoMetedNum"] /
            blIndexValue["terminal"]["Web"]["allTestCaseNum"] * 100))
    # print(dataDict)
    tbModule = TbWebPortalUiCovered()
    tbModule.statisticalTime = datetime.datetime.now()
    tbModule.coverDetail = json.dumps(dataDict)
    tbModule.save()

    print("done!")
