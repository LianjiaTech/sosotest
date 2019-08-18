import core.processor.KP
import core.processor.CP 
from core.tools.CommonFunc import *
from core.tools.DBTool import DBTool

def getParamList(strTobeProcessed,context):
    #为什么不将关键字处理放入到循环中
    strTobeProcessed = core.processor.KP.KP.process_KEYWORDS(strTobeProcessed, context)
    paramList = splitStringToListByTag(strTobeProcessed, ",")
    for jj in range(0, len(paramList)):
        paramList[jj] = core.processor.CP.CP.getProcessedValue(paramList[jj], context)
    return paramList

def getParamListAndKWParam(strTobeProcessed,context):
    #为什么不将关键字处理放入到循环中
    strTobeProcessed = core.processor.KP.KP.process_KEYWORDS(strTobeProcessed, context)
    paramList = splitStringToListByTag(strTobeProcessed, ",")
    retParamList = []
    retParamDict = {}
    for jj in range(0, len(paramList)):
        sigParamList = splitStringToListByTag(paramList[jj], "=")
        if len(sigParamList) == 2:
            retParamDict[sigParamList[0].strip()] = core.processor.CP.CP.getProcessedValue(sigParamList[1].strip(), context)
        else:
            retParamList.append(core.processor.CP.CP.getProcessedValue(paramList[jj], context))
    return retParamList,retParamDict

def INVOKE(strTobeProcessed,context):
    strTobeProcessed = core.processor.KP.KP.getProcessedValue(strTobeProcessed.replace("<-+->",""), context)
    return strTobeProcessed

def isLoop(recurDict={}, startInerfaceId="", endInterfaceId=""):
    if startInerfaceId == endInterfaceId:  # 如果开始和结束是同一个，直接就死循环了
        return True
    if endInterfaceId not in recurDict.keys():  # 是否执行过，没有就没有死循环
        return False

    # end曾经执行过，取出执行过的值，看看执行过的值有没有startInterfaceId，以及下面的父极的父极有没有。
    endInterfaceKeyList = recurDict[endInterfaceId]  # 去除end key下面所有执行过的接口，如果end执行过父极，或者end的子集执行过父极都是死循环。
    for tmpExucutedInterface in endInterfaceKeyList:
        # 去除值判断
        if tmpExucutedInterface == startInerfaceId:
            # 如果调用过父极，死循环返回True
            return True
        else:
            # 如果没有，递归判断他的子集有没有调用过父极。
            if isLoop(recurDict, startInerfaceId, tmpExucutedInterface):
                return True
    return False

def executeAndTransferContext(interfaceTobeExecuted,context):
    #接口、步骤级别的执行时需要传递，不包括任务级别的
    #主需要从context传递到被执行接口即可
    interfaceTobeExecuted.confHttpLayer = context.confHttpLayer

    #需要回传的对象
    context.transferAttrsFrom1Pto2P(context,interfaceTobeExecuted,isTrans_calledInterfaceRecurDict = True)
    ##需要特殊处理 pythonmode相关的############################################################################
    bak_IS_CONTINUE = ""
    bak_DEBUG_MODE = ""
    bak_context = ""
    if "IS_CONTINUE" in interfaceTobeExecuted.varsPool.keys():
        bak_IS_CONTINUE = interfaceTobeExecuted.varsPool["IS_CONTINUE"]
        del interfaceTobeExecuted.varsPool["IS_CONTINUE"]

    if "DEBUG_MODE" in interfaceTobeExecuted.varsPool.keys():
        bak_DEBUG_MODE = interfaceTobeExecuted.varsPool["DEBUG_MODE"]
        del interfaceTobeExecuted.varsPool["DEBUG_MODE"]

    if "context" in interfaceTobeExecuted.varsPool.keys():
        bak_context = interfaceTobeExecuted.varsPool["context"]
        del interfaceTobeExecuted.varsPool["context"]
    #############################################################################################
    if "allmodels.HttpTestcase.HttpTestcase" in str(type(interfaceTobeExecuted)):
        interfaceTobeExecuted.execute()
    else:
        interfaceTobeExecuted.executeInterface()

    context.transferAttrsFrom1Pto2P(interfaceTobeExecuted,context,isTrans_calledInterfaceRecurDict = True)

    if bak_IS_CONTINUE != "" and bak_context != "":
        #context是pythonmode，需要回传。
        #如果我是pythonmode，如果对方是pythommode进来的，我肯定也要走这一段
        interfaceTobeExecuted.varsPool["IS_CONTINUE"] = bak_IS_CONTINUE
        interfaceTobeExecuted.varsPool["DEBUG_MODE"] = bak_DEBUG_MODE
        interfaceTobeExecuted.varsPool["context"] = bak_context
        exec(context.get_python_mode_buildIn_functions(), context.varsPool)  # 执行完重新处理一次

def processWhetherIGNORE(interfaceIdList):
    whetherSetResultWhenFAIL = True
    whetherSetResultWhenERROR = True
    whetherSetResultWhenEXCEPTION = True
    if len(interfaceIdList) > 1:
        lastParam = interfaceIdList[-1].strip()
        if "IGNORE_" in lastParam:
            interfaceIdList = interfaceIdList[:-1]  # 接口列表去掉最后一个元素
            if "_ALL" in lastParam:
                whetherSetResultWhenFAIL = False
                whetherSetResultWhenERROR = False
                whetherSetResultWhenEXCEPTION = False
            else:
                if "_FAIL" in lastParam:
                    whetherSetResultWhenFAIL = False
                if "_ERROR" in lastParam:
                    whetherSetResultWhenERROR = False
                if "_EXCEPTION" in lastParam:
                    whetherSetResultWhenEXCEPTION = False
    return interfaceIdList,whetherSetResultWhenFAIL,whetherSetResultWhenERROR,whetherSetResultWhenEXCEPTION