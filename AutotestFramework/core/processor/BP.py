from core.decorator.normal_functions import *
from core.tools.CommonFunc import *
import traceback
import core.processor.CP
import core.processor.KP
rootpath = os.path.dirname(os.path.abspath(__file__)).replace("\\","/")
from core.processor.Assert import Assert,MyAssertError
from core.tools.ExecFunc import *

class BP(object):

    @staticmethod
    @catch_exception
    def processConditionByKPCP(condition,context):
        condition = core.processor.KP.KP.process_KEYWORDS(condition, context)
        condition = core.processor.CP.CP.process_CONST(condition, context)
        condition = core.processor.CP.CP.process_GVAR(condition, context)
        condition = core.processor.CP.CP.process_VARS(condition, context)
        return condition

    @staticmethod
    @keyword(startTag="{%IF ",endTag="{%ENDIF%}")
    @catch_exception
    def process_branch_IF(value, context,strTobeProcessed = ""):
        """
        {%IF condition %}
          A
        {%ELIF condition %}
          B
        {%ELIF condition %}
          B2
        {%ELSE%}
          C
        {%ENDIF%}
        """
        ifBranchStr = strTobeProcessed.strip()
        conditionEndTag = "%}"
        elifStartTag = "{%ELIF "
        elseTag = "{%ELSE%}"
        ifEndPos = ifBranchStr.find(conditionEndTag)
        ifCondition = ifBranchStr[0:ifEndPos].strip()
        ifValueStartPos = ifEndPos+len(conditionEndTag)
        elifStartPos = ifBranchStr.find(elifStartTag,ifEndPos+1)
        elseStartPos = ifBranchStr.find(elseTag,ifEndPos+1)

        if elifStartPos == -1 and elseStartPos == -1:
            #没有elif 和 else 结束断言，直接判断if条件。
            ifValue = ifBranchStr[ifValueStartPos:].strip()
        elif elifStartPos == -1 :
            ifValue = ifBranchStr[ifValueStartPos:elseStartPos].strip()
        elif elseStartPos == -1 :
            ifValue = ifBranchStr[ifValueStartPos:elifStartPos].strip()
        elif elifStartPos < elseStartPos :
            ifValue = ifBranchStr[ifValueStartPos:elifStartPos].strip()
        else:
            ifValue = ifBranchStr[ifValueStartPos:elseStartPos].strip()

        ifCondition = BP.processConditionByKPCP(ifCondition,context)
        if ifCondition == "":
            retMsg = "<ERROR:IF缺少condition>"
            context.setERROR(retMsg)
            return retMsg
        try:
            retBool = eval(ifCondition)
            if TypeTool.is_bool(retBool):
                if retBool:
                    ifValue = BP.processConditionByKPCP(ifValue, context)
                    return ifValue
            else:
                retMsg = "<ERROR:IF判断条件[%s]返回的不是布尔类型>" % ifCondition
                context.setERROR(retMsg)
                return retMsg
        except Exception as e:
            retMsg = "<ERROR:IF判断条件[%s]异常>" % (ifCondition)
            context.setERROR(retMsg)
            return retMsg

        #执行到此说明IF的判断是False
        #开始执行elif判断
        if elifStartPos != -1:
            #执行elif判断
            elifConditionList = []
            elifValueList = []
            isStopFindElif = False
            while True:
                if isStopFindElif: break
                elifEndPos = ifBranchStr.find(conditionEndTag,elifStartPos+1)
                if elifEndPos == -1:
                    #没有找到结束标签，报错。
                    retMsg = "<ERROR:ELIF没有找到condition结束标签>"
                    context.setERROR(retMsg)
                    return retMsg
                else:
                    elifConditionList.append(ifBranchStr[elifStartPos+len(elifStartTag):elifEndPos])
                    elifStartPos = ifBranchStr.find(elifStartTag, elifEndPos + 1)
                    elseStartPos = ifBranchStr.find(elseTag, elifEndPos + 1)
                    elifValueStartPos = elifEndPos+len(conditionEndTag)
                    if elifStartPos == -1 and elseStartPos == -1:
                        # 没有elif 和 else 结束断言，直接判断if条件。
                        elifValue = ifBranchStr[elifValueStartPos:].strip()
                        isStopFindElif = True
                    elif elifStartPos == -1:
                        isStopFindElif = True
                        elifValue = ifBranchStr[elifValueStartPos:elseStartPos].strip()
                    elif elseStartPos == -1:
                        elifValue = ifBranchStr[elifValueStartPos:elifStartPos].strip()
                    elif elifStartPos < elseStartPos:
                        elifValue = ifBranchStr[elifValueStartPos:elifStartPos].strip()
                    else:
                        elifValue = ifBranchStr[elifValueStartPos:elseStartPos].strip()
                    elifValueList.append(elifValue)

            if len(elifConditionList) != len(elifValueList):
                retMsg = "<ERROR: ELIF语句出错>"
                context.setERROR(retMsg)
                return retMsg
            for i in range(0,len(elifConditionList)):
                tmpElifCondition = elifConditionList[i]
                tmpElifValue = elifValueList[i]
                tmpElifCondition = BP.processConditionByKPCP(tmpElifCondition, context)
                if tmpElifCondition == "":
                    retMsg = "<ERROR:第%d个ELIF缺少condition>" % (i+1)
                    context.setERROR(retMsg)
                    return retMsg
                try:
                    tmpRetBool = eval(tmpElifCondition)
                    if TypeTool.is_bool(tmpRetBool):
                        if tmpRetBool:
                            tmpElifValue = BP.processConditionByKPCP(tmpElifValue, context)
                            return tmpElifValue
                    else:
                        retMsg = "<ERROR:第%d个ELIF判断条件[%s]返回的不是布尔类型>" % ((i+1),tmpElifCondition)
                        context.setERROR(retMsg)
                        return retMsg
                except Exception as e:
                    retMsg = "<ERROR:第%d个ELIF判断条件[%s]异常>" % ((i+1),tmpElifCondition)
                    context.setERROR(retMsg)
                    return retMsg

        #k开始执行else
        if elseStartPos != -1:
            #执行else
            elseValue = ifBranchStr[elseStartPos+len(elseTag):].strip()
            elseValue = BP.processConditionByKPCP(elseValue, context)
            return elseValue
        else:
            return ""#没有else返回空

    @staticmethod
    @catch_exception
    def process_python_code(pythoncode, context):
        finalCode = ""
        try:
            # 预期引入的包
            timeout = getKeywordExecPythonTimeout("timoutForPythonMode")
            # 上下文如果没有引入过，要加入系统函数，初始化。
            #说明是没有执行过
            context.varsPool['IS_CONTINUE']= True
            context.varsPool['DEBUG_MODE'] = False
            context.varsPool['context'] = context

            # 不用纠结了，每次进来都要初始化一次基本配置。
            exec(context.get_python_mode_buildIn_functions(), context.varsPool)

            #####开始执行并超时退出
            retVBl,retVMsg = validatePythoCodeFromUser(pythoncode)
            if retVBl == False:
                raise Exception(retVMsg)

            finalCode = pythoncode.strip()
            class TimeLimited(Thread):
                def __init__(self):
                    Thread.__init__(self)

                def run(self):
                    try:
                        context.pythonModeExecuteLog += "[%s]开始执行...\n" % context.interfaceId
                        exec(finalCode, context.varsPool)
                    except Exception as eInner:
                        if isinstance(eInner,MyAssertError):
                            context.pythonModeExecuteLog += "终止执行，测试结果[%s]: %s\n" % (eInner.testResult,eInner.retMsg.strip())
                        elif str(eInner) == "BREAK":
                            context.pythonModeExecuteLog += "<ERROR:PYTHON MODE 下，用户BREAK代码执行！>"
                        else:
                            context.pythonModeExecuteLog += "<ERROR:PYTHON MODE 下执行python语句发生异常：\n%s>" % ( traceback.format_exc())
                            context.setERROR( context.pythonModeExecuteLog)

            t = TimeLimited()
            t.start()
            t.join(timeout=timeout)
            if t.is_alive():
                stop_thread(t)
                raise Exception('PYTHON MODE 执行超时，超时时间%s秒。' % timeout)

            context.pythonModeExecuteLog += "[%s]<DONE: PYTHON执行成功>" % context.interfaceId
            if context.varsPool["DEBUG_MODE"]:
                context.pythonModeExecuteLog +=  "\n############################################################\n" \
                                                 +context.interfaceId+"的Python脚本:\n" + finalCode + \
                                                 "\n############################################################\n" \
                                                 +context.interfaceId+"执行后的作用域值：\n" + str(context.varsPool)
        except Exception as e:
            logging.error(traceback.format_exc())
            if str(e) == "FUNC_TIMEOUT":
                context.pythonModeExecuteLog += "\n<ERROR:执行python语句发生[执行超时]异常，python代码：\n%s>" % (finalCode)
                context.setERROR( context.pythonModeExecuteLog)
            else:
                context.pythonModeExecuteLog += "\n<ERROR:发生异常：\n%s>" % (traceback.format_exc())
                context.setERROR( context.pythonModeExecuteLog)
        finally:
            context.updateVarWhichNoPath()
            return context.varsPool['IS_CONTINUE']

if __name__ == '__main__':
    pass








