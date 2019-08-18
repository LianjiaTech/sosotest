import xlrd
import os
import sys,random
import logging
from copy import deepcopy
rootpath = os.path.dirname(os.path.realpath(__file__)).replace("\\","/")
rootpath = rootpath.split("/apps")[0]
syspath=sys.path
sys.path=[]
sys.path.append(rootpath) #指定搜索路径绝对目录
sys.path.extend([rootpath+i for i in os.listdir( rootpath) if i[0]!="."])#将工程目录下的一级目录添加到python搜索路径中
sys.path.extend(syspath)
from apps.common.func.InitDjango import *
from all_models.models import TbUiTask,TbUiTaskExecute
from all_models.models import TbUiTestCase,TbUiTestCaseStep
from all_models.models import TbUiGlobalText,TbUiGlobalVars,TbUiPageObject,TbUiPageObjectElements,TbUiFunctions,TbUiFunctionsTestcase,TbUiFunctionsTestcaseStep
from all_models.models import TbBusinessLine,TbModules,TbSource,TbConfigHttp
from apps.common.func.CommonFunc import *

class ExcelProcesser(object):

    def __init__(self,excelFilePath):
        self.excelFilePath = excelFilePath
        self.businessLineDict = {} #key是name，value是id
        self.moduleDict = {} #key是name，value是id
        self.sourceDict = {} #key是name，value是id
        self.httpConfKeyList = []

        businessLineSets = TbBusinessLine.objects.filter(state=1).all()
        for tmpObj in businessLineSets:
            self.businessLineDict[tmpObj.bussinessLineName] = tmpObj.id

        moduleSets = TbModules.objects.filter(state=1).all()
        for tmpObj in moduleSets:
            self.moduleDict[tmpObj.moduleName] = tmpObj.id

        sourceSets = TbSource.objects.filter(state=1).all()
        for tmpObj in sourceSets:
            self.sourceDict[tmpObj.sourceName] = tmpObj.id

        configHttpSets = TbConfigHttp.objects.filter(state=1).all()
        for tmpObj in configHttpSets:
            self.httpConfKeyList.append(tmpObj.httpConfKey)

        self.specialTagList = ["#",#注释符号
                        ]

    def getAllDatas(self):
        textDict = {}
        gvarDict = {}
        pageObjectDict = {}
        commonCaseDict = {}
        caseList = []
        #step1 获取textDict
        retBl,retReason,textDict = self.getTEXTDict()
        if retBl == False:
            retReason = "获取全局文本失败，请检查。原因:%s" % retReason
            logging.error(retReason)
            return False,retReason,textDict,gvarDict,pageObjectDict,commonCaseDict,caseList

        #step2 获取gvarDict
        retBl, retReason,gvarDict = self.getGVARDict()
        if retBl == False:
            retReason = "获取全局变量失败，请检查。原因:%s" % retReason
            logging.error(retReason)
            return False,retReason,textDict,gvarDict,pageObjectDict,commonCaseDict,caseList

        allSheetNameList = self.getAllSheetNameList()

        #step3 获取pageObjectDict
        # 生成pageObjectdict
        pageObjectDict = {}
        for tmpSheetName in allSheetNameList:
            if tmpSheetName.startswith("PageObject_") :
                tmpPODict = self.getPageObjectDictBySheetName(tmpSheetName)
                pageObjectDict.update(tmpPODict)

        #step4 获取commonCaseDict
        commonCaseDict = {}
        # 生成通用方法，可以在sheet case中调用。
        for tmpSheetName in allSheetNameList:
            if tmpSheetName.startswith("Function_"):
                retBl,retReason,tmpCommonCaseDict = self.getCommonCaseDictBySheetName(tmpSheetName)
                if retBl:
                    commonCaseDict[tmpSheetName.split("Function_")[1]] = tmpCommonCaseDict
                else:
                    retReason = "生成Function用例时发生错误，原因：%s" % retReason
                    logging.error(retReason)
                    return False, retReason, textDict, gvarDict, pageObjectDict, commonCaseDict, caseList


        # step5 获取caseList
        # 生成要执行的caseList
        caseList = []
        # 如果sheetName为空，使用所有带Case的sheet
        for tmpCaseSheetName in allSheetNameList:
            if tmpCaseSheetName.startswith("Testcase_"):
                retBl,retReason,retTmpCaseList = self.getCaseListBySheetName(tmpCaseSheetName)
                if retBl:
                    caseList += retTmpCaseList
                else:
                    retReason = "生成用例时发生错误，原因：%s" % retReason
                    logging.error(retReason)
                    return False, retReason, textDict, gvarDict, pageObjectDict, commonCaseDict, caseList

        return True, "", textDict, gvarDict, pageObjectDict, commonCaseDict, caseList

    def getDataListBySheetName(self,sheetName):
        if ((os.path.exists(self.excelFilePath)) == False):
            logging.info("不存在文件[%s]，请检查！" % self.excelFilePath)
            return []
        else:
            data = xlrd.open_workbook(self.excelFilePath)
            if sheetName not in self.getAllSheetNameList():
                return []
            table = data.sheet_by_name(sheetName)
            maxRowsNum = table.nrows
            maxColsNum = table.ncols
            allDataList = []
            for rowIndex in range(0,maxRowsNum):
                tmpRowValueList = []
                for colIndex in range(0,maxColsNum):
                    # tmpRowValueList.append(table.cell(rowIndex,colIndex).value)
                    tmpRowValueList.append(str(table.cell(rowIndex,colIndex).value).strip())
                allDataList.append(tmpRowValueList)
            return allDataList

    def getTEXTDict(self,sheetName = "$TEXT"):
        commonEnvStartColNum = 2
        #return 结果bool，原因string，数据dict
        dataList = self.getDataListBySheetName(sheetName)
        print("----------------------------------")
        print(dataList)
        if len(dataList) == 0:
            return True,"",{}
        envDict = {}
        envList = dataList[0]
        for envIndex in range(commonEnvStartColNum,len(envList)):
            if (envList[envIndex] not in self.httpConfKeyList) and envList[envIndex] != "common":
                return False,"环境key[%s]不在系统中" %  envList[envIndex],{}
            else:
                envDict[str(envIndex)] = envList[envIndex]
        retTextDict = {}
        for i in range(1,len(dataList)):
            tmpTextStr = ""
            tmpEnvData = dataList[i]
            tmpTextObj = TbUiGlobalText()
            tmpTextObj.textDesc = tmpEnvData[0]
            tmpTextObj.textKey = tmpEnvData[1]
            for env2Index in range(commonEnvStartColNum,len(tmpEnvData)):
                tmpTextStr += "[CONF=%s]%s[ENDCONF]" % (envDict[str(env2Index)],tmpEnvData[env2Index])
            tmpTextObj.textValue = tmpTextStr
            retTextDict[tmpTextObj.textKey] = tmpTextObj
        return True,"",retTextDict

    def getGVARDict(self,sheetName = "$GVAR"):
        commonEnvStartColNum = 2
        # return 结果bool，原因string，数据dict
        dataList = self.getDataListBySheetName(sheetName)
        if len(dataList) == 0:
            return True, "", {}
        envDict = {}
        envList = dataList[0]
        for envIndex in range(commonEnvStartColNum, len(envList)):
            if (envList[envIndex] not in self.httpConfKeyList) and envList[envIndex] != "common":
                return False, "环境key[%s]不在系统中" % envList[envIndex], {}
            else:
                envDict[str(envIndex)] = envList[envIndex]
        retTextDict = {}
        for i in range(1, len(dataList)):
            tmpTextStr = ""
            tmpEnvData = dataList[i]
            tmpTextObj = TbUiGlobalVars()
            tmpTextObj.varDesc = tmpEnvData[0]
            tmpTextObj.varKey = tmpEnvData[1]
            for env2Index in range(commonEnvStartColNum, len(tmpEnvData)):
                tmpTextStr += "[CONF=%s]%s[ENDCONF]" % (envDict[str(env2Index)], tmpEnvData[env2Index])
            tmpTextObj.varValue = tmpTextStr
            retTextDict[tmpTextObj.varKey] = tmpTextObj
        return True, "", retTextDict

    def getCaseListBySheetName(self,sheetName,execCaseId = ""):
        if sheetName.startswith("Testcase_") == False:
            return False, "sheetName必须是Testcase_开头！", []  # 业务线错误，中止，返回空

        dataList = self.getDataListBySheetName(sheetName)
        caseList = []
        execCaseIdList = []
        if execCaseId.strip() != "":
            execCaseIdList = execCaseId.split(",")
        tmpUITestCaseDict = {}
        tmpUITestCaseDict['case'] = TbUiTestCase()
        tmpUITestCaseDict['caseSteps'] = []
        for i in range(1,len(dataList)):
            tmpRow = dataList[i]
            stepNumIndex = 0
            if tmpRow[2].strip()!="" and tmpRow[2] not in self.specialTagList:
                if tmpUITestCaseDict['case'].caseId != "":
                    if len(execCaseIdList) == 0 or (len(execCaseIdList) >0 and tmpUITestCaseDict['case'].caseId in execCaseIdList):
                        caseList.append(tmpUITestCaseDict) #添加上一个用例
                stepNumIndex = 0 #重置步骤编号
                #找到一个新用例

                tmpUITestCase = TbUiTestCase() #清空上一个用例信息
                businessLineName = tmpRow[0].strip()
                if businessLineName not in self.businessLineDict.keys():
                    retReason = "Case[%s]的业务线[%s]错误，请检查！" % (tmpRow[2],businessLineName)
                    logging.error(retReason)
                    return False,retReason,[] #业务线错误，中止，返回空

                tmpUITestCase.businessLineId = self.businessLineDict[businessLineName]
                moduleName = tmpRow[1].strip()
                if moduleName not in self.moduleDict.keys():
                    retReason = "Case[%s]的业务线[%s]错误，请检查！" % (tmpRow[2],moduleName)
                    logging.error(retReason)
                    return False,retReason,[] #模块错误，中止

                tmpUITestCase.moduleName = self.moduleDict[moduleName]

                tmpUITestCase.caseId = tmpRow[2]
                tmpUITestCase.title = tmpRow[3]
                tmpUITestCase.casedesc = tmpRow[4]
                tmpUITestCaseDict = {}
                tmpUITestCaseDict['case'] = tmpUITestCase
                tmpUITestCaseDict['caseSteps'] = []
            else:
                #找到的行不是用例，那肯定就是步骤
                tmpUITestcaseStep = TbUiTestCaseStep()
                stepNumIndex += 1
                tmpUITestcaseStep.caseId = tmpUITestCaseDict['case'].caseId
                tmpUITestcaseStep.stepNum = stepNumIndex
                tmpUITestcaseStep.specialTag = tmpRow[2]
                tmpUITestcaseStep.stepTitle = tmpRow[3]
                tmpUITestcaseStep.stepDesc = tmpRow[4]
                tmpUITestcaseStep.operate = tmpRow[5]
                tmpUITestcaseStep.params = tmpRow[6]
                if tmpUITestcaseStep.operate.strip() != "" and tmpUITestcaseStep.params.strip() != "":
                    #关键字和参数不能为空才是真的有效的。
                    tmpUITestCaseDict['caseSteps'].append(tmpUITestcaseStep)
            if i == len(dataList)-1 and tmpUITestCaseDict['case'].caseId != "":
                #执行完最后一步的时候，判断是否要把最后一个case加入到caseList
                if len(execCaseIdList) == 0 or (len(execCaseIdList) >0 and tmpUITestCaseDict['case'].caseId in execCaseIdList):
                    caseList.append(tmpUITestCaseDict) #把最后一个用例加进来
        return True,"",caseList

    def getCommonCaseDictBySheetName(self,sheetName):
        if sheetName.startswith("Function_") == False:
            return False, "sheetName必须是Function_开头！", []  # 业务线错误，中止，返回空

        dataList = self.getDataListBySheetName(sheetName)
        caseList = []
        commonFuncKey = sheetName.split("Function_")[1]

        tmpUITestCaseDict = {}
        tmpUITestCaseDict['function'] = TbUiFunctionsTestcase()
        tmpUITestCaseDict['functionSteps'] = []
        stepNumIndex = 0
        for i in range(1, len(dataList)):
            tmpRow = dataList[i]
            if tmpRow[2].strip()!="" and tmpRow[2] not in self.specialTagList:
                #找到一个新的用例：如果上一个的name不是空，那么就加入到case列表
                if tmpUITestCaseDict['function'].functionName != "":
                    caseList.append(tmpUITestCaseDict)  # 添加上一个用例

                stepNumIndex = 0  # 重置步骤编号
                # 找到一个新用例
                tmpUITestCase = TbUiFunctionsTestcase()  # 清空上一个用例信息
                businessLineName = tmpRow[0].strip()
                if businessLineName not in self.businessLineDict.keys():
                    retReason = "Function[%s]的业务线[%s]错误，请检查！" % (tmpRow[2], businessLineName)
                    logging.error(retReason)
                    return False, retReason, []  # 业务线错误，中止，返回空

                tmpUITestCase.businessLineId = self.businessLineDict[businessLineName]
                moduleName = tmpRow[1].strip()
                if moduleName not in self.moduleDict.keys():
                    retReason = "Function[%s]的业务线[%s]错误，请检查！" % (tmpRow[2], moduleName)
                    logging.error(retReason)
                    return False, retReason, []  # 模块错误，中止

                tmpUITestCase.moduleName = self.moduleDict[moduleName]
                tmpUITestCase.commonFuncKey = commonFuncKey
                tmpUITestCase.functionName = tmpRow[2]
                tmpUITestCase.title = tmpRow[3]
                tmpUITestCase.casedesc = tmpRow[4]
                tmpUITestCaseDict = {}
                tmpUITestCaseDict['function'] = tmpUITestCase
                tmpUITestCaseDict['functionSteps'] = []
            else:
                # 找到的行不是用例，那肯定就是步骤
                tmpUITestcaseStep = TbUiFunctionsTestcaseStep()
                stepNumIndex += 1
                tmpUITestcaseStep.commonFuncKey = commonFuncKey
                tmpUITestcaseStep.functionName = tmpUITestCaseDict['function'].functionName
                tmpUITestcaseStep.stepNum = stepNumIndex
                tmpUITestcaseStep.specialTag = tmpRow[2]
                tmpUITestcaseStep.stepTitle = tmpRow[3]
                tmpUITestcaseStep.stepDesc = tmpRow[4]
                tmpUITestcaseStep.operate = tmpRow[5]
                tmpUITestcaseStep.params = tmpRow[6]
                if tmpUITestcaseStep.operate.strip() != "" and tmpUITestcaseStep.params.strip() != "":
                    # 关键字和参数不能为空才是真的有效的。
                    tmpUITestCaseDict['functionSteps'].append(tmpUITestcaseStep)
            if i == len(dataList) - 1 and tmpUITestCaseDict['function'].functionName != "":
                # 执行完最后一步的时候，判断是否要把最后一个case加入到caseList
                caseList.append(tmpUITestCaseDict)  # 把最后一个用例加进来
        #跟获取用例一样
        caseDict = {}
        for tmpCase in caseList:
            caseDict[tmpCase['function'].functionName] = tmpCase
        return True,"",caseDict

    def getPageObjectDictBySheetName(self,sheetName = ""):
        dataList = self.getDataListBySheetName(sheetName)
        poDict = {}
        currentPageObjName = ""
        for i in range(1, len(dataList)):
            tmpRow = dataList[i]
            if tmpRow[0].strip() != "" :
                #这是一个新的pageObject,生成对应的对象 dict
                tmpPageObjectModel = TbUiPageObject()
                tmpPageObjectModel.poKey = tmpRow[0].strip()
                tmpPageObjectModel.poTitle = tmpRow[1].strip()
                tmpPageObjectModel.poDesc = tmpRow[2].strip()

                currentPageObjName = tmpRow[0].strip()
                if currentPageObjName not in poDict.keys():
                    poDict[currentPageObjName] = {}

                poDict[currentPageObjName]['po'] = tmpPageObjectModel
                poDict[currentPageObjName]['elements'] = []
            else:
                #如果是空，那么就是一个element选项
                tmpElementModel = TbUiPageObjectElements()
                tmpElementModel.poKey = poDict[currentPageObjName]['po'].poKey
                tmpElementModel.elementTitle = tmpRow[1]
                tmpElementModel.elementDesc = tmpRow[2]
                tmpElementModel.elementKey = tmpRow[3]
                tmpElementModel.elementType = tmpRow[4]
                tmpElementModel.elementValue = tmpRow[5]
                if currentPageObjName != "" and currentPageObjName in poDict.keys():
                    poDict[currentPageObjName]['elements'].append(tmpElementModel)

        return poDict

    def getAllSheetNameList(self):
        casefile = self.excelFilePath
        if ((os.path.exists(casefile)) == False):
            logging.info("不存在文件[%s]，请检查！" % casefile)
            return []
        else:
            data = xlrd.open_workbook(casefile)
            allSheetsObj = data.sheets()
            allName = []
            for tmpSheetObj in allSheetsObj:
                allName.append(tmpSheetObj.name)
        return allName

class ExcelDataUpdateDB(object):
    def __init__(self,sessionName,textDict = {},gvarDict = {},poDict = {},functionDict = {},caseList = [] ,upType = "add"):
        self.sessionName = sessionName
        self.textDict = textDict
        self.gvarDict = gvarDict
        self.poDict = poDict
        self.functionDict = functionDict
        self.caseList = caseList
        self.upType = upType
    def textUpdate(self):
        msg = ""
        result = True
        for k,v in self.textDict.items():
            dbV = TbUiGlobalText.objects.filter(textKey=k).all()
            # 查找这个text，找到后判断这个text是不是自己添加的，如果是自己添加的就更新，如果不是就记录下来 最后给提示
            if dbV:
                # print(dbModelToDict(v))
                if dbV[0].addBy != self.sessionName:
                    msg += "\n[%s]text不是当前用户添加，text未更新" % dbV[0].textKey
                    result = False
                    continue
                v.id = dbV[0].id
                v.addTime = dbV[0].addTime
                v.save(force_update=True)
                # print("#找到这个text")
            else:
                # print("#没有找到这个text")
                # print(v)
                v.addBy = self.sessionName
                v.save(force_insert=True)

        return result,msg

    def gvarUpdate(self):
        msg = ""
        result = True
        for k,v in self.gvarDict.items():

            dbV = TbUiGlobalVars.objects.filter(varKey = k).all()
            if dbV:
                if dbV[0].addBy != self.sessionName:
                    msg += "\n[%s]gvar不是当前用户添加，gvar未更新" % dbV[0].varKey
                    result = False
                    continue

                v.id = dbV[0].id
                v.addTime = dbV[0].addTime
                v.save(force_update=True)
            else:
                v.addBy = self.sessionName
                v.save(force_insert=True)
        return result, msg

    def poAndElementUpdate(self):
        poMsg = ""
        poResult= True
        elemetMsg = ""
        elementResult = True
        for k,v in self.poDict.items():
            poKey = k
            po = v['po']
            poFromDb = TbUiPageObject.objects.filter(poKey = poKey).all()
            if poFromDb:
                if poFromDb[0].addBy != self.sessionName:
                    poMsg += "\n[%s]object page不是当前用户添加，object page未更新" % poFromDb[0].poKey
                    poResult = False
                else:
                    po.id = poFromDb[0].id
                    po.addTime = poFromDb[0].addTime
                    po.save(force_update=True)
            else:
                po.addBy = self.sessionName
                po.save(force_insert=True)

            elementsList = v['elements']
            for tmpElement in elementsList:
                tmpEleFromDb = TbUiPageObjectElements.objects.filter(poKey=poKey,elementKey = tmpElement.elementKey).all()
                if tmpEleFromDb:
                    if tmpEleFromDb[0].addBy != self.sessionName:
                        elemetMsg += "\n[%s]element不是当前用户添加，element未更新" % tmpEleFromDb[0].elementKey
                        elementResult = False
                        continue
                    tmpElement.id = tmpEleFromDb[0].id
                    tmpElement.addTime = tmpEleFromDb[0].addTime
                    tmpElement.save(force_update=True)
                else:
                    tmpElement.addBy = self.sessionName
                    tmpElement.save(force_insert=True)
        return poResult,poMsg,elementResult,elemetMsg

    def funcUpdate(self):
        funcMsg = ""
        funcResult = True
        for k,v in self.functionDict.items():
            # ui functions #######################################################################################
            tmpUiFunction = TbUiFunctions.objects.filter(commonFuncKey = k).all()
            if tmpUiFunction:
                #有直接进行更新：

                tmpUiFunction = tmpUiFunction[0]
                tmpUiFunction.save(force_update=True)
            else:
                #没有对应的func，创建func
                tmpUiFunction = TbUiFunctions()
                tmpUiFunction.commonFuncKey = k
                tmpUiFunction.commonFuncTitle = "默认值，请修改"
                tmpUiFunction.commonFuncDesc = "默认值，请修改"
                tmpUiFunction.addBy = self.sessionName
                tmpUiFunction.save(force_insert=True)

            for k2,v2 in v.items():
                #对function testcase进行便利
                tmpUiFuncTestcase = TbUiFunctionsTestcase.objects.filter(commonFuncKey = k,functionName = k2).all()
                if tmpUiFuncTestcase:
                    #存在，那么就更新。
                    tmpFuntion = v2['function']
                    if tmpUiFuncTestcase[0].addBy != self.sessionName:
                        funcMsg += "\n[%s] 的创建人不是当前用户，function更新失败" % tmpFuntion.functionName
                        funcResult = False
                        continue
                    tmpFuntion.id = tmpUiFuncTestcase[0].id
                    tmpFuntion.addTime = tmpUiFuncTestcase[0].addTime
                    tmpFuntion.modBy = self.sessionName
                    tmpFuntion.save(force_update=True)
                else:
                    tmpFuntion = v2['function']
                    tmpFuntion.addBy = self.sessionName
                    tmpFuntion.save(force_insert=True)
                #开始保存步骤。
                funcSteps = v2['functionSteps']
                funcStepsInDb = TbUiFunctionsTestcaseStep.objects.filter(commonFuncKey = k,functionName = k2).all()
                if len(funcSteps) <= len(funcStepsInDb):
                    #如果实际的小于数据库中的,直接更新实际的到数据库中，多余的步骤为0
                    for dbFuncStepi in range(0,len(funcStepsInDb)):
                        #TODO pass根据步骤的长度决定是插入还是更新。
                        if dbFuncStepi < len(funcSteps):
                            #更新步骤到db中
                            funcSteps[dbFuncStepi].id = funcStepsInDb[dbFuncStepi].id
                            funcSteps[dbFuncStepi].state = 1
                            funcSteps[dbFuncStepi].addTime = funcStepsInDb[dbFuncStepi].addTime
                            funcSteps[dbFuncStepi].modBy = self.sessionName
                            funcSteps[dbFuncStepi].save(force_update=True)
                        else:
                            #更新数据库的步骤的state为0
                            funcStepsInDb[dbFuncStepi].state = 0
                            funcStepsInDb[dbFuncStepi].modBy = self.sessionName
                            funcStepsInDb[dbFuncStepi].save(force_update=True)
                else:
                    #如果实际的大于数据库中的
                    for realFuncStepi in range(0,len(funcSteps)):
                        if realFuncStepi < len(funcStepsInDb):
                            #更新到db中
                            funcSteps[realFuncStepi].id = funcStepsInDb[realFuncStepi].id
                            funcSteps[realFuncStepi].addTime = funcStepsInDb[realFuncStepi].addTime
                            funcSteps[realFuncStepi].state = 1
                            funcSteps[realFuncStepi].modBy = self.sessionName
                            funcSteps[realFuncStepi].save(force_update=True)
                        else:
                            #插入到db中
                            funcSteps[realFuncStepi].addBy = self.sessionName
                            funcSteps[realFuncStepi].save(force_insert=True)
        return funcResult,funcMsg

    def caseUpdate(self):
        caseMsg = ""
        caseResult = True
        for tmpCaseDict in self.caseList:
            tmpCase = tmpCaseDict['case']
            tmpCaseSteps = tmpCaseDict['caseSteps']
            if self.upType == "add":
                tmpCase.caseId = "TMPCASEID_%s" % random.randint(0,10000000)
                tmpCase.save(force_insert=True)
                tmpCase.caseId = "TC_UI_%d" % tmpCase.id
                tmpCase.addBy = self.sessionName
                tmpCase.save(force_update=True)
            else:
                tmpUiTestcase = TbUiTestCase.objects.filter(caseId = tmpCase.caseId).all()
                if tmpUiTestcase:
                    # 存在，那么就更新。
                    tmpCase.id = tmpUiTestcase[0].id
                    if tmpUiTestcase[0].addBy != self.sessionName:
                        print(tmpUiTestcase[0].addBy)
                        print("+++++++++++++++++++++++++++++++++")
                        caseMsg += "\n [%s]的创建人不是当前用户，跳过更新" % tmpUiTestcase[0].caseId
                        continue
                    else:
                        tmpCase.addBy = self.sessionName
                        tmpCase.addTime = tmpUiTestcase[0].addTime
                        tmpCase.save(force_update=True)
                else:
                    print("不存在%s" % tmpCase.caseId)
                    continue
            # 开始保存步骤。
            caseSteps = tmpCaseSteps
            caseStepsInDb = TbUiTestCaseStep.objects.filter(caseId = tmpCase.caseId).all()
            if len(caseSteps) <= len(caseStepsInDb):
                # 如果实际的小于数据库中的,直接更新实际的到数据库中，多余的步骤为0
                for dbFuncStepi in range(0, len(caseStepsInDb)):
                    # TODO pass根据步骤的长度决定是插入还是更新。
                    if dbFuncStepi < len(caseSteps):
                        # 更新步骤到db中
                        caseSteps[dbFuncStepi].id = caseStepsInDb[dbFuncStepi].id
                        caseSteps[dbFuncStepi].caseId = tmpCase.caseId
                        caseSteps[dbFuncStepi].state = 1
                        caseSteps[dbFuncStepi].addTime = caseStepsInDb[dbFuncStepi].addTime
                        caseSteps[dbFuncStepi].save(force_update=True)
                    else:
                        # 更新数据库的步骤的state为0
                        caseStepsInDb[dbFuncStepi].state = 0
                        caseStepsInDb[dbFuncStepi].caseId = tmpCase.caseId
                        caseStepsInDb[dbFuncStepi].save(force_update=True)
            else:
                # 如果实际的大于数据库中的
                for realFuncStepi in range(0, len(caseSteps)):
                    if realFuncStepi < len(caseStepsInDb):
                        # 更新到db中
                        caseSteps[realFuncStepi].id = caseStepsInDb[realFuncStepi].id
                        caseSteps[realFuncStepi].caseId = tmpCase.caseId
                        caseSteps[realFuncStepi].addTime = caseStepsInDb[realFuncStepi].addTime
                        caseSteps[realFuncStepi].state = 1
                        caseSteps[realFuncStepi].save(force_update=True)
                    else:
                        # 插入到db中
                        caseSteps[realFuncStepi].addBy = self.sessionName
                        caseSteps[realFuncStepi].caseId = tmpCase.caseId
                        caseSteps[realFuncStepi].save(force_insert=True)
        return caseResult,caseMsg
if __name__ == '__main__':

    excelFilePath = "D:/autotest/AutotestPlatform/RobotUiTest/testData/StandardTemplate.xls"
    sheetName = "Testcase_OnlyWeb"
    excelObj = ExcelProcesser(excelFilePath)
    retBl,retReason,textDict,gvarDict,poDict,functionDict,caseList = excelObj.getAllDatas()
    # print(retBl)
    # print(retReason)
    # print(textDict)
    # print(gvarDict)
    # print(poDict)
    print("----------------------------------------------------")
    print(functionDict)
    # print(caseList)

    updateDb = ExcelDataUpdateDB(sessionName="1",textDict=textDict,gvarDict=gvarDict,poDict=poDict,functionDict=functionDict,caseList=caseList,upType="update")
    #saveText
    textResult,textMsg = updateDb.textUpdate()
    gvarResult,gvarMsg = updateDb.gvarUpdate()
    #poDict
    poResult,poMsg,elementResult,elementMsg = updateDb.poAndElementUpdate()
    funcResult,funcMsg = updateDb.funcUpdate()
    caseResult,caseMsg = updateDb.caseUpdate()
    print(caseResult)
    print(caseMsg)
    if textResult:
        textMsg = "text更新成功"
        textMsg = "textMsg:%s" % textMsg



    #testSaveText
    # for k,v in textDict.items():
    #     dbV = TbUiGlobalText.objects.filter(textKey = k).all()
    #     #查找这个text，找到后判断这个text是不是自己添加的，如果是自己添加的就更新，如果不是就记录下来 最后给提示
    #     if dbV:
    #         v.id = dbV[0].id
    #         v.addTime = dbV[0].addTime
    #         v.save(force_update=True)
    #         print("#找到这个text")
    #         from apps.common.func.CommonFunc import *
    #         print(dbModelToDict(v))
    #     else:
    #         print("#没有找到这个text")
    #         print(v)
    #         v.save(force_insert=True)
    #
    # #testSaveGvar
    # for k,v in gvarDict.items():
    #     dbV = TbUiGlobalVars.objects.filter(varKey = k).all()
    #     if dbV:
    #         v.id = dbV[0].id
    #         v.addTime = dbV[0].addTime
    #         v.save(force_update=True)
    #     else:
    #         v.save(force_insert=True)
    #
    # #testSavePageObjectandElemnts#######################################################################################
    # for k,v in poDict.items():
    #     poKey = k
    #     po = v['po']
    #     poFromDb = TbUiPageObject.objects.filter(poKey = poKey).all()
    #     if poFromDb:
    #         po.id = poFromDb[0].id
    #         po.addTime = poFromDb[0].addTime
    #         po.save(force_update=True)
    #     else:
    #         po.save(force_insert=True)
    #
    #     elementsList = v['elements']
    #     for tmpElement in elementsList:
    #         tmpEleFromDb = TbUiPageObjectElements.objects.filter(poKey=poKey,elementKey = tmpElement.elementKey).all()
    #         if tmpEleFromDb:
    #             tmpElement.id = tmpEleFromDb[0].id
    #             tmpElement.addTime = tmpEleFromDb[0].addTime
    #             tmpElement.save(force_update=True)
    #         else:
    #             tmpElement.save(force_insert=True)
    #
    # for k,v in functionDict.items():
    #     # ui functions #######################################################################################
    #     tmpUiFunction = TbUiFunctions.objects.filter(commonFuncKey = k).all()
    #     if tmpUiFunction:
    #         #有直接进行更新：
    #         tmpUiFunction = tmpUiFunction[0]
    #     else:
    #         #没有对应的func，创建func
    #         tmpUiFunction = TbUiFunctions()
    #         tmpUiFunction.commonFuncKey = k
    #         tmpUiFunction.commonFuncTitle = "默认值，请修改"
    #         tmpUiFunction.commonFuncDesc = "默认值，请修改"
    #         tmpUiFunction.save(force_insert=True)
    #
    #     for k2,v2 in v.items():
    #         #对function testcase进行便利
    #         tmpUiFuncTestcase = TbUiFunctionsTestcase.objects.filter(commonFuncKey = k,functionName = k2).all()
    #         if tmpUiFuncTestcase:
    #             #存在，那么就更新。
    #             tmpFuntion = v2['function']
    #             tmpFuntion.id = tmpUiFuncTestcase[0].id
    #             tmpFuntion.addTime = tmpUiFuncTestcase[0].addTime
    #             tmpFuntion.save(force_update=True)
    #         else:
    #             tmpFuntion = v2['function']
    #             tmpFuntion.save(force_insert=True)
    #         #开始保存步骤。
    #         funcSteps = v2['functionSteps']
    #         funcStepsInDb = TbUiFunctionsTestcaseStep.objects.filter(commonFuncKey = k,functionName = k2).all()
    #         if len(funcSteps) <= len(funcStepsInDb):
    #             #如果实际的小于数据库中的,直接更新实际的到数据库中，多余的步骤为0
    #             for dbFuncStepi in range(0,len(funcStepsInDb)):
    #                 #TODO pass根据步骤的长度决定是插入还是更新。
    #                 if dbFuncStepi < len(funcSteps):
    #                     #更新步骤到db中
    #                     funcSteps[dbFuncStepi].id = funcStepsInDb[dbFuncStepi].id
    #                     funcSteps[dbFuncStepi].state = 1
    #                     funcSteps[dbFuncStepi].addTime = funcStepsInDb[dbFuncStepi].addTime
    #                     funcSteps[dbFuncStepi].save(force_update=True)
    #                 else:
    #                     #更新数据库的步骤的state为0
    #                     funcStepsInDb[dbFuncStepi].state = 0
    #                     funcStepsInDb[dbFuncStepi].save(force_update=True)
    #         else:
    #             #如果实际的大于数据库中的
    #             for realFuncStepi in range(0,len(funcSteps)):
    #                 if realFuncStepi < len(funcStepsInDb):
    #                     #更新到db中
    #                     funcSteps[realFuncStepi].id = funcStepsInDb[realFuncStepi].id
    #                     funcSteps[realFuncStepi].addTime = funcStepsInDb[realFuncStepi].addTime
    #                     funcSteps[realFuncStepi].state = 1
    #                     funcSteps[realFuncStepi].save(force_update=True)
    #                 else:
    #                     #插入到db中
    #                     funcSteps[realFuncStepi].save(force_insert=True)
    #
    # # ui functions #######################################################################################
    #
    # #testcases #######################################################################################
    # upType = "update"  # update
    # for tmpCaseDict in caseList:
    #     tmpCase = tmpCaseDict['case']
    #     tmpCaseSteps = tmpCaseDict['caseSteps']
    #     if upType == "add":
    #         tmpCase.caseId = "TMPCASEID_%s" % random.randint(0,10000000)
    #         tmpCase.save(force_insert=True)
    #         tmpCase.caseId = "TC_UI_%d" % tmpCase.id
    #         tmpCase.save(force_update=True)
    #     else:
    #         tmpUiTestcase = TbUiTestCase.objects.filter(caseId = tmpCase.caseId).all()
    #         if tmpUiTestcase:
    #             # 存在，那么就更新。
    #             tmpCase.id = tmpUiTestcase[0].id
    #             tmpCase.addTime = tmpUiTestcase[0].addTime
    #             tmpCase.save(force_update=True)
    #         else:
    #             print("不存在%s" % tmpCase.caseId)
    #             continue
    #     # 开始保存步骤。
    #     caseSteps = tmpCaseSteps
    #     caseStepsInDb = TbUiTestCaseStep.objects.filter(caseId = tmpCase.caseId).all()
    #     if len(caseSteps) <= len(caseStepsInDb):
    #         # 如果实际的小于数据库中的,直接更新实际的到数据库中，多余的步骤为0
    #         for dbFuncStepi in range(0, len(caseStepsInDb)):
    #             # TODO pass根据步骤的长度决定是插入还是更新。
    #             if dbFuncStepi < len(caseSteps):
    #                 # 更新步骤到db中
    #                 caseSteps[dbFuncStepi].id = caseStepsInDb[dbFuncStepi].id
    #                 caseSteps[dbFuncStepi].caseId = tmpCase.caseId
    #                 caseSteps[dbFuncStepi].state = 1
    #                 caseSteps[dbFuncStepi].addTime = caseStepsInDb[dbFuncStepi].addTime
    #                 caseSteps[dbFuncStepi].save(force_update=True)
    #             else:
    #                 # 更新数据库的步骤的state为0
    #                 caseStepsInDb[dbFuncStepi].state = 0
    #                 caseStepsInDb[dbFuncStepi].caseId = tmpCase.caseId
    #                 caseStepsInDb[dbFuncStepi].save(force_update=True)
    #     else:
    #         # 如果实际的大于数据库中的
    #         for realFuncStepi in range(0, len(caseSteps)):
    #             if realFuncStepi < len(caseStepsInDb):
    #                 # 更新到db中
    #                 caseSteps[realFuncStepi].id = caseStepsInDb[realFuncStepi].id
    #                 caseSteps[realFuncStepi].caseId = tmpCase.caseId
    #                 caseSteps[realFuncStepi].addTime = caseStepsInDb[realFuncStepi].addTime
    #                 caseSteps[realFuncStepi].state = 1
    #                 caseSteps[realFuncStepi].save(force_update=True)
    #             else:
    #                 # 插入到db中
    #                 caseSteps[realFuncStepi].caseId = tmpCase.caseId
    #                 caseSteps[realFuncStepi].save(force_insert=True)




    #testcases #######################################################################################

