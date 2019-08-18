import os
import sys
import threading
rootpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))).replace("\\","/")
syspath=sys.path
sys.path=[]
sys.path.append(rootpath) #指定搜索路径绝对目录
sys.path.extend([rootpath+i for i in os.listdir(rootpath) if i[0]!="."])#将工程目录下的一级目录添加到python搜索路径中
sys.path.extend(syspath)
from core.const.GlobalConst import ResultConst
from core.decorator.normal_functions import keyword,catch_exception
from core.keywords.ALL_FUNC import *

@keyword()
@catch_exception
def EXECUTE_INTERFACE(value, context,strTobeProcessed = ""):
    interfaceIdList = getParamList(strTobeProcessed,context)
    # 如果获取参数等导致错误，不继续执行登录返回错误原因。
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字EXECUTE_INTERFACE执行时解析参数列表返回错误。返回参数列表为%s" % str(interfaceIdList)
        context.assertResult = "%s\n%s" % (retMsg,context.assertResult)
        return retMsg

    #处理 interfaceIdList 判断是否结果影响后续执行
    #IGNORE_ALL IGNORE_FAIL_ERROR
    interfaceIdList, whetherSetResultWhenFAIL, whetherSetResultWhenERROR, whetherSetResultWhenEXCEPTION = processWhetherIGNORE(interfaceIdList)
    #处理结束 interfaceIdList #########

    tobeReplaced = ""
    startInterfaceId = context.interfaceId
    for i in range(0, len(interfaceIdList)):
        endInterfaceId = interfaceIdList[i].strip()
        if endInterfaceId== "":
            continue
        # if endInterfaceId in context.calledInterfaceList:
        #     tobeReplaced = "[接口被循环调用]"
        #     context.setERROR("接口[%s]被循环调用形成死循环，请检查用例。" % endInterfaceId)
        #     break
        # context.calledInterfaceList.append(endInterfaceId)
        if isLoop(context.calledInterfaceRecurDict,startInterfaceId,endInterfaceId):
            tobeReplaced = "<ERROR:接口[%s]被循环调用形成死循环，请检查EXECUTE_INTERFACE链路。>" % endInterfaceId
            tobeReplacedError = "接口[%s]被循环调用形成死循环，请检查用例。" % endInterfaceId
            context.setERROR(tobeReplacedError)
            break
        else:
            if startInterfaceId not in context.calledInterfaceRecurDict.keys():
                context.calledInterfaceRecurDict[startInterfaceId] = []
            context.calledInterfaceRecurDict[startInterfaceId].append(endInterfaceId)

        import allmodels.HttpInterface
        interfaceTobeExecuted = allmodels.HttpInterface.HttpInterface()
        interfaceTobeExecuted.interfaceId = endInterfaceId
        interfaceTobeExecuted.version = context.version #加入版本属性。
        retBool = interfaceTobeExecuted.generateByInterfaceId()
        if retBool == False:
            tobeReplaced = "<ERROR:接口[%s]没有找到，请确认是否存在或者已删除。>" % endInterfaceId
            tobeReplacedError = "接口[%s]没有找到，请确认是否存在或者已删除。" % endInterfaceId
            context.setERROR(tobeReplacedError)
            break

        executeAndTransferContext(interfaceTobeExecuted,context)
        tobeReplaced +=  getRespTextByResponse(interfaceTobeExecuted.interface_response) #替换为执行结果

        # 更新varsKeyList
        for j in range(0, len(interfaceTobeExecuted.varsKeyList)):
            tmpKey = interfaceTobeExecuted.varsKeyList[j]
            if tmpKey in context.varsKeyList:
                # 将tmpKey加入到最后
                context.varsKeyList.remove(tmpKey)
            context.varsKeyList.append(tmpKey)

        if interfaceTobeExecuted.testResult == ResultConst.FAIL:
            tobeReplaced = "%s\n%s" % ("执行接口%s结果FAIL" % interfaceTobeExecuted.interfaceId, tobeReplaced)
            if whetherSetResultWhenFAIL:
                context.setResult(interfaceTobeExecuted.testResult, "执行接口%s结果FAIL，断言结果：%s" % (interfaceTobeExecuted.interfaceId, interfaceTobeExecuted.assertResult))

        if interfaceTobeExecuted.testResult == ResultConst.ERROR:
            tobeReplaced = "%s\n%s" % ("执行接口%s出现错误" % interfaceTobeExecuted.interfaceId, tobeReplaced)
            if whetherSetResultWhenERROR:
                context.setResult(interfaceTobeExecuted.testResult, "执行接口%s出现错误，错误原因：%s" % (interfaceTobeExecuted.interfaceId, interfaceTobeExecuted.assertResult))

        if interfaceTobeExecuted.testResult == ResultConst.EXCEPTION:
            tobeReplaced = "%s\n%s" % ("执行接口%s出现异常" % interfaceTobeExecuted.interfaceId,tobeReplaced)
            if whetherSetResultWhenEXCEPTION:
                context.setResult(interfaceTobeExecuted.testResult,"执行接口%s出现异常，异常原因：%s" % (interfaceTobeExecuted.interfaceId,interfaceTobeExecuted.assertResult))

    return tobeReplaced


@keyword()
@catch_exception
def EXECUTE_TESTCASE(value, context,strTobeProcessed = ""):
    TestCaseIdList = getParamList(strTobeProcessed, context)
    # 如果获取参数等导致错误，不继续执行登录返回错误原因。
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字EXECUTE_INTERFACE执行时解析参数列表返回错误。返回参数列表为%s" % str(TestCaseIdList)
        context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
        return retMsg

    # 处理 TestCaseIdList 判断是否结果影响后续执行
    # IGNORE_ALL IGNORE_FAIL_ERROR
    TestCaseIdList, whetherSetResultWhenFAIL, whetherSetResultWhenERROR, whetherSetResultWhenEXCEPTION = processWhetherIGNORE(TestCaseIdList)

    # 处理结束 TestCaseIdList #########

    tobeReplaced = ""
    startTestCaseId = context.caseId
    for i in range(0, len(TestCaseIdList)):
        endTestCaseId = TestCaseIdList[i].strip()
        if endTestCaseId == "":
            continue
        if isLoop(context.calledInterfaceRecurDict, startTestCaseId, endTestCaseId):
            tobeReplaced += "<ERROR:用例[%s]被循环调用形成死循环，请检查EXECUTE_TESTCASE链路。>" % endTestCaseId
            tobeReplacedError = "用例[%s]被循环调用形成死循环，请检查用例。" % endTestCaseId
            context.setERROR(tobeReplacedError)
            break
        else:
            if startTestCaseId not in context.calledInterfaceRecurDict.keys():
                context.calledInterfaceRecurDict[startTestCaseId] = []
            context.calledInterfaceRecurDict[startTestCaseId].append(endTestCaseId)

        import allmodels.HttpTestcase
        testCaseTobeExecute = allmodels.HttpTestcase.HttpTestcase()
        testCaseTobeExecute.caseId = endTestCaseId
        testCaseTobeExecute.version = context.version
        testCaseTobeExecute.generateByCaseId()

        executeAndTransferContext(testCaseTobeExecute,context)

        tmpCaseLastStep = testCaseTobeExecute.stepTestcaseList[-1]
        tobeReplaced += getRespTextByResponse(tmpCaseLastStep.interface_response)  # 替换为执行结果

        # 更新varsKeyList
        for j in range(0, len(tmpCaseLastStep.varsKeyList)):
            tmpKey = tmpCaseLastStep.varsKeyList[j]
            if tmpKey in context.varsKeyList:
                # 将tmpKey加入到最后
                context.varsKeyList.remove(tmpKey)
            context.varsKeyList.append(tmpKey)

        if testCaseTobeExecute.testResult == ResultConst.FAIL:
            tobeReplaced = "%s\n%s" % ("执行业务流%s结果FAIL" % testCaseTobeExecute.caseId, tobeReplaced)
            if whetherSetResultWhenFAIL:
                context.setResult(testCaseTobeExecute.testResult, "执行业务流%s结果FAIL，断言结果：%s" % (testCaseTobeExecute.caseId, testCaseTobeExecute.assertResult))

        if testCaseTobeExecute.testResult == ResultConst.ERROR:
            tobeReplaced = "%s\n%s" % ("执行业务流%s出现错误" % testCaseTobeExecute.caseId, tobeReplaced)
            if whetherSetResultWhenERROR:
                context.setResult(testCaseTobeExecute.testResult, "执行业务流%s出现错误，错误原因：%s" % (testCaseTobeExecute.caseId, testCaseTobeExecute.assertResult))

        if testCaseTobeExecute.testResult == ResultConst.EXCEPTION:
            tobeReplaced = "%s\n%s" % ("执行业务流%s出现异常" % testCaseTobeExecute.caseId,tobeReplaced)
            if whetherSetResultWhenEXCEPTION:
                context.setResult(testCaseTobeExecute.testResult,"执行业务流%s出现异常，异常原因：%s" % (testCaseTobeExecute.caseId,testCaseTobeExecute.assertResult))

    return tobeReplaced


@keyword()
@catch_exception
def EXECUTE_DUBBO_INTERFACE(value, context,strTobeProcessed = ""):
    interfaceIdList = getParamList(strTobeProcessed,context)
    # 如果获取参数等导致错误，不继续执行登录返回错误原因。
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字EXECUTE_DUBBO_INTERFACE执行时解析参数列表返回错误。返回参数列表为%s" % str(interfaceIdList)
        context.assertResult = "%s\n%s" % (retMsg,context.assertResult)
        return retMsg

    #处理 interfaceIdList 判断是否结果影响后续执行
    #IGNORE_ALL IGNORE_FAIL_ERROR
    interfaceIdList, whetherSetResultWhenFAIL, whetherSetResultWhenERROR, whetherSetResultWhenEXCEPTION = processWhetherIGNORE(interfaceIdList)
    #处理结束 interfaceIdList #########

    tobeReplaced = ""
    startInterfaceId = context.interfaceId
    for i in range(0, len(interfaceIdList)):
        endInterfaceId = interfaceIdList[i].strip()
        if endInterfaceId== "":
            continue
        if isLoop(context.calledInterfaceRecurDict,startInterfaceId,endInterfaceId):
            tobeReplaced = "<ERROR:接口[%s]被循环调用形成死循环，请检查EXECUTE_INTERFACE链路。>" % endInterfaceId
            tobeReplacedError = "接口[%s]被循环调用形成死循环，请检查用例。" % endInterfaceId
            context.setERROR(tobeReplacedError)
            break
        else:
            if startInterfaceId not in context.calledInterfaceRecurDict.keys():
                context.calledInterfaceRecurDict[startInterfaceId] = []
            context.calledInterfaceRecurDict[startInterfaceId].append(endInterfaceId)

        import allmodels.DubboInterface
        interfaceTobeExecuted =  allmodels.DubboInterface.DubboInterface()
        interfaceTobeExecuted.interfaceId = endInterfaceId
        interfaceTobeExecuted.version = context.version #加入版本属性。
        retBool = interfaceTobeExecuted.generateByInterfaceId()
        if retBool == False:
            tobeReplaced = "<ERROR:接口[%s]没有找到，请确认是否存在或者已删除。>" % endInterfaceId
            tobeReplacedError = "接口[%s]没有找到，请确认是否存在或者已删除。" % endInterfaceId
            context.setERROR(tobeReplacedError)
            break

        executeAndTransferContext(interfaceTobeExecuted,context)

        tobeReplaced += interfaceTobeExecuted.actualResult

        # 更新varsKeyList
        for j in range(0, len(interfaceTobeExecuted.varsKeyList)):
            tmpKey = interfaceTobeExecuted.varsKeyList[j]
            if tmpKey in context.varsKeyList:
                # 将tmpKey加入到最后
                context.varsKeyList.remove(tmpKey)
            context.varsKeyList.append(tmpKey)

        if interfaceTobeExecuted.testResult == ResultConst.FAIL:
            tobeReplaced = "%s\n%s" % ("执行接口%s结果FAIL" % interfaceTobeExecuted.interfaceId, tobeReplaced)
            if whetherSetResultWhenFAIL:
                context.setResult(interfaceTobeExecuted.testResult, "执行接口%s结果FAIL，断言结果：%s" % (interfaceTobeExecuted.interfaceId, interfaceTobeExecuted.assertResult))

        if interfaceTobeExecuted.testResult == ResultConst.ERROR:
            tobeReplaced = "%s\n%s" % ("执行接口%s出现错误" % interfaceTobeExecuted.interfaceId, tobeReplaced)
            if whetherSetResultWhenERROR:
                context.setResult(interfaceTobeExecuted.testResult, "执行接口%s出现错误，错误原因：%s" % (interfaceTobeExecuted.interfaceId, interfaceTobeExecuted.assertResult))

        if interfaceTobeExecuted.testResult == ResultConst.EXCEPTION:
            tobeReplaced = "%s\n%s" % ("执行接口%s出现异常" % interfaceTobeExecuted.interfaceId,tobeReplaced)
            if whetherSetResultWhenEXCEPTION:
                context.setResult(interfaceTobeExecuted.testResult,"执行接口%s出现异常，异常原因：%s" % (interfaceTobeExecuted.interfaceId,interfaceTobeExecuted.assertResult))

    return tobeReplaced



if __name__ == '__main__':
    pass