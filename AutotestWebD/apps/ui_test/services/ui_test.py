

import apps.common.func.InitDjango
from all_models.models import TbHttpTestcaseDebug,TbUser
from django.db import connection
from django.forms.models import model_to_dict
from apps.common.func.CommonFunc import *
from all_models.models import *

class ui_test(object):
    @staticmethod
    def updateUiTestList():
        execTestList = dbModelListToListDict(TbUITestExecute.objects.filter(execStatus__in=[1, 2]))
        for testIndex in execTestList:
            reportLog = "%s/static/%s/%s/%s" % (BASE_DIR.replace("\\", "/"), "ui_test_reports",testIndex["reportDir"], "report.log")
            print(reportLog)
            if os.path.exists(reportLog):
                f = open(reportLog, 'r')
                fileContent = f.read()
                if "DONE:FINISHED" in fileContent:
                    print(fileContent)

                    resultList = re.findall(r"TestResultJsonString:(.+)TestResultJsonStringEnd",
                                            fileContent.replace("\n", "").strip())

                    resultJson = json.loads(resultList[0].strip())
                    tbModel = TbUITestExecute.objects.filter(id=testIndex["id"]).last()
                    tbModel.testResult = resultJson["testResult"]
                    tbModel.execTakeTime = "%.2f" % float(resultJson["totalTakeTime"])
                    tbModel.execStartTime = resultJson["startExecTime"]
                    tbModel.execEndTime = resultJson["endExecTime"]
                    print(resultJson)
                    tbModel.testResultMessage = json.dumps(resultJson)
                    tbModel.execStatus = 3
                    tbModel.save()
                else:
                    print(222222222)
            else:
                print(33333333333)

    @staticmethod
    def getUIExcelList():
        excelFilesDict = {}
        excelList = TbUITestExcel.objects.filter(state=1)
        for index in excelList:
            if index.addBy not in excelFilesDict.keys():
                userName = TbUser.objects.get(loginName=index.addBy).userName
                excelFilesDict[index.addBy] = {"userName":userName,"sheet":{}}
            excelFilesDict[index.addBy]["sheet"][index.fileName] = index.sheetNames.split("_,_")
        return excelFilesDict