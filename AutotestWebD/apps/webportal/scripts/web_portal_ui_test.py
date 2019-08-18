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
    allBLDict = dbModelListToListDict(TbBusinessLine.objects.filter(state=1))
    dataDict = {"envDetail": {}, "blDetail": {}}
    standardBlDict = {}
    allEnv = dbModelListToListDict(TbWebPortalStandardEnv.objects.filter(state=1, uiIsShow=1).order_by("lineSort"))

    for blIndex in allBLDict:
        blExecuteLen = len(TbUITestExecute.objects.filter(state=1, businessLineId=blIndex["id"]))
        if blExecuteLen > 0:
            standardBlDict[blIndex["bussinessLineName"]] = {}
            # 获取执行过的业务线下的模块
            moduleList = dbModelListToListDict(
                TbBusinessLineModuleRelation.objects.filter(businessLineId=blIndex["id"]))
            # 获取执行过的业务线下执行过的模块
            for moduleIndex in moduleList:
                module = TbModules.objects.get(id=moduleIndex["moduleId_id"])
                mdExecuteLen = len(TbUITestExecute.objects.filter(state=1, moduleId=module.id))
                if mdExecuteLen > 0:
                    standardBlDict[blIndex["bussinessLineName"]][module.moduleName] = {}

    # blDetailDict = copy.deepcopy(standardBlDict)
    #
    # #生成确定值
    # for blIndexKey,blIndexValue in blDetailDict.items():
    #     for mdIndexKey,mdIndexValue in blIndexValue.items():
    #         for envIndex in allEnv:
    #             mdIndexValue[envIndex["httpConfKey"]] = {}
    #             execDetail = TbUITestExecute.objects.filter(state=1,businessLineName=blIndexKey,moduleName=mdIndexKey,httpConfKey=envIndex["httpConfKey"]).last()
    #             if execDetail:
    #                 mdIndexValue[envIndex["httpConfKey"]] = dbModelToDict(execDetail)
    #                 if mdIndexValue[envIndex["httpConfKey"]]["testResultMessage"] == "" or not isJson(mdIndexValue[envIndex["httpConfKey"]]["testResultMessage"]):
    #                     mdIndexValue[envIndex["httpConfKey"]]["testResultMessage"] = {"testResult": "NOTRUN", "testResultMessage": "", "casePassCount": 0,
    #                                                                                   "caseFailCount": 0, "caseWarningCount": 0,"caseNotrunCount": 0, "caseStepPassCount": 0,
    #                                                                                   "caseStepFailCount": 0, "caseStepWarningCount": 0, "caseStepNotrunCount": 0,
    #                                                                                   "totalTakeTime": 0}
    #                 else:
    #                     mdIndexValue[envIndex["httpConfKey"]]["testResultMessage"] = json.loads(mdIndexValue[envIndex["httpConfKey"]]["testResultMessage"])

    blEnvDetail = {}
    for blIndexKey, blIndexValue in standardBlDict.items():
        blEnvDetail[blIndexKey] = {"mdTestDetail":{},"testMessage":{},"testResultList" : []}

        for envIndex in allEnv:
            blEnvDetail[blIndexKey]["testMessage"][envIndex["httpConfKey"]] = {
                "caseStepPassCount": 0, "caseStepFailCount": 0, "caseStepWarningCount": 0, "caseStepNotrunCount": 0,
                "caseStepTotalCount": 0}

        for mdIndexKey, mdIndexValue in blIndexValue.items():
            blEnvDetail[blIndexKey]["mdTestDetail"][mdIndexKey] = {"envTest":{}}
            for envIndex in allEnv:
                mdEnvTest = blEnvDetail[blIndexKey]["mdTestDetail"][mdIndexKey]["envTest"][envIndex["httpConfKey"]] = {}
                bsId = TbBusinessLine.objects.get(bussinessLineName=blIndexKey).id
                mdId = TbModules.objects.get(moduleName=mdIndexKey).id
                execDetail = TbUITestExecute.objects.filter(state=1, businessLineId=bsId, moduleId=mdId, httpConfKey=envIndex["httpConfKey"]).last()
                testResult = {"testResult": "NOTRUN", "testResultMessage": "", "caseStepPassCount": 0,
                              "caseStepFailCount": 0, "caseStepWarningCount": 0,
                              "caseStepNotrunCount": 0, "caseStepTotalCount": 0,"passRate" : "%.2f" % 0,"report":"javascript:void(0)"}

                if execDetail:
                    execDetailDict = dbModelToDict(execDetail)
                    if execDetailDict["testResultMessage"] != "" and isJson(execDetailDict["testResultMessage"]):
                        testResult = json.loads(execDetailDict["testResultMessage"])
                        testResult["caseStepTotalCount"] = testResult["caseStepPassCount"] + testResult["caseStepFailCount"] + testResult["caseStepWarningCount"] + testResult["caseStepNotrunCount"]
                        if testResult["caseStepTotalCount"] == 0:
                            testResult["passRate"] = "%.2f" % 0
                        else:
                            testResult["passRate"] = "%.2f" % (testResult["caseStepPassCount"] / testResult["caseStepTotalCount"] *100)
                    if execDetailDict["reportDir"] != "":
                        testResult["report"] = "/static/ui_test/reports/%s/report.html" % execDetailDict["reportDir"]

                if testResult["passRate"] > "90.00" or testResult["passRate"] == "100.00":
                    testResult["color"] = "green"
                elif  testResult["passRate"] < "90.00" and testResult["passRate"] > "80.00":
                    testResult["color"] = "orange"
                else:
                    testResult["color"] = "red"

                mdEnvTest["testMessage"] = testResult
                blEnvTestMessage = blEnvDetail[blIndexKey]["testMessage"][envIndex["httpConfKey"]]
                blEnvTestMessage["caseStepPassCount"] += testResult["caseStepPassCount"]
                blEnvTestMessage["caseStepFailCount"] += testResult["caseStepFailCount"]
                blEnvTestMessage["caseStepWarningCount"] += testResult["caseStepWarningCount"]
                blEnvTestMessage["caseStepNotrunCount"] += testResult["caseStepNotrunCount"]
                blEnvTestMessage["caseStepTotalCount"] += testResult["caseStepTotalCount"]
                blEnvDetail[blIndexKey]["testResultList"].append(testResult["testResult"])

    for blIndexKey,blIndexValue in blEnvDetail.items():

        if "EXCEPTION" in blIndexValue["testResultList"]:
            blIndexValue["testResult"] = "EXCEPITON"
        elif "ERROR" in blIndexValue["testResultList"]:
            blIndexValue["testResult"] = "ERROR"
        elif "FAIL" in blIndexValue["testResultList"]:
            blIndexValue["testResult"] = "FAIL"
        elif "PASS" in blIndexValue["testResultList"]:
            blIndexValue["testResult"] = "PASS"
        elif "NOTRUN" in blIndexValue["testResultList"]:
            blIndexValue["testResult"] = "NOTRUN"

        for envIndexKey,envIndexValue in blIndexValue["testMessage"].items():
            if envIndexValue["caseStepTotalCount"] == 0:
                envIndexValue["passRate"] = "%.2f" % 0
            else:
                envIndexValue["passRate"] = "%.2f" % (envIndexValue["caseStepPassCount"] / envIndexValue["caseStepTotalCount"] * 100)
            if envIndexValue["passRate"] > "90.00" or envIndexValue["passRate"] == "100.00":
                envIndexValue["color"] = "green"
            elif envIndexValue["passRate"] < "90.00" and envIndexValue["passRate"] > "80.00":
                envIndexValue["color"] = "orange"
            else:
                envIndexValue["color"] = "red"
    # print(json.dumps(blDetailDict))
    # print(json.dumps(blEnvDetail))
    resultDict = {"blEnvDetail":blEnvDetail}

    tbModel = TbWebPortalUITest()
    tbModel.testDetail = json.dumps(resultDict)
    tbModel.statisticalTime = datetime.datetime.now()
    tbModel.save()
    print("done!")
