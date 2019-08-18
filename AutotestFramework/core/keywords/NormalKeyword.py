from core.decorator.normal_functions import keyword,time_limited,catch_exception
import traceback,json,ast
from core.keywords.ALL_FUNC import *
from core.const.GlobalConst import ResultConst
from threading import Thread
from core.processor.Assert import Assert
from core.tools.CommonFunc import validatePythoCodeFromUser
from core.tools.ExecFunc import *
from core.processor.Assert import Assert,MyAssertError

@keyword()
@catch_exception
def EVAL(value,context,strTobeProcessed = ""):
    try:
        retStr = ""
        strTobeProcessed = core.processor.KP.KP.process_KEYWORDS(strTobeProcessed, context)
        if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
            retMsg = "CASE_ERROR:关键字EVAL执行时解析参数列表返回错误。返回参数列表为%s" % strTobeProcessed
            context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
            return retMsg
        evalstring = core.processor.CP.CP.getProcessedValue(strTobeProcessed, context)
        invalidStrList = ["import","system","read"]
        for tmpInvalidStr in invalidStrList:
            if tmpInvalidStr in evalstring:
                retStr = "<ERROR:不合法的请求，不能包含字符串%s>" % tmpInvalidStr
                context.setERROR( retStr)
                return retStr
        retStr =  str(eval(evalstring))
    except Exception as e:
        retStr = "<ERROR:执行python语句发生异常：python代码：\n%s\n发生异常：\n%s>" % (evalstring,traceback.format_exc())
        context.setERROR( retStr)

    finally:
        return retStr


@keyword()
@catch_exception
def EXEC_PYTHON(value,context,strTobeProcessed = ""):
    retStr = ""
    try:
        #正则取出所有的EXECUTE_KEYWORD
        reString = "INVOKE\{([\s\S]*?)\}END"  # 取出所有的KEYWORD[ ]END
        p = re.compile(r'%s' % reString)
        kwListInEval = p.findall(strTobeProcessed)
        logging.debug(kwListInEval)
        for tmpKw in kwListInEval:
            tmpRplacedString = ""
            # 开始混淆关键字前面的小括号
            hxTag = "("
            kwListSplitByKh = tmpKw.split(hxTag)
            specialSplitTag = "<-+->"
            for  tmpIndex in range(0,len(kwListSplitByKh)):
                tmpSubSplitStr = kwListSplitByKh[tmpIndex]
                if tmpIndex < len(kwListSplitByKh) - 1:
                    tmpRplacedString += "%s%s" % ((tmpSubSplitStr!="" and tmpSubSplitStr[0:-1]+specialSplitTag+tmpSubSplitStr[-1:] or specialSplitTag),hxTag)
                else:
                    tmpRplacedString += tmpSubSplitStr
            #开始处理混淆变量等[
            hxTag = "["
            kwListSplitByKh = tmpRplacedString.split(hxTag)
            specialSplitTag = "<-+->"
            tmpRplacedString = ""
            for tmpIndex in range(0,len(kwListSplitByKh)):
                tmpSubSplitStr = kwListSplitByKh[tmpIndex]
                if tmpIndex < len(kwListSplitByKh) - 1:
                    tmpRplacedString += "%s%s" % ((tmpSubSplitStr!="" and tmpSubSplitStr[0:-1]+specialSplitTag+tmpSubSplitStr[-1:] or specialSplitTag),hxTag)
                else:
                    tmpRplacedString += tmpSubSplitStr
            strTobeProcessed = strTobeProcessed.replace("INVOKE{%s}END" % tmpKw,"INVOKE(\"\"\"%s\"\"\",context)" % tmpRplacedString)

        logging.debug(strTobeProcessed)

        evalstring = core.processor.KP.KP.getProcessedValue(strTobeProcessed, context)
        if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
            retMsg = "CASE_ERROR:关键字EXEC_PYTHON执行时解析参数列表返回错误。返回参数列表为%s" % evalstring
            context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
            return retMsg

        logging.debug(evalstring)

        importStr = getPythonThirdLib().strip()
        timeout = getKeywordExecPythonTimeout("timeoutString")
        retBl,retmsg = validatePythoCodeFromUser(evalstring)
        if retBl == False:
            raise Exception(retmsg)

        evalstring = "from core.keywords.ALL_FUNC import INVOKE\n%s" % (evalstring.strip())
        logging.debug(evalstring)
        nameDict = {"VAR": context.varsPool,"ASSERT_MODE": False,"retStr":retStr}
        #线程类执行python代码，超时退出
        #加载pythonmode的东西
        context.varsPool['IS_CONTINUE'] = True
        context.varsPool['DEBUG_MODE'] = False
        context.varsPool['context'] = context
        exec(context.get_python_mode_buildIn_functions(), context.varsPool)
        context.varsPool.update(nameDict)
        class TimeLimited(Thread):
            def __init__(self):
                Thread.__init__(self)
            def run(self):
                try:
                    exec(evalstring, context.varsPool)
                except AssertionError as assertError:
                    logging.debug(context.varsPool['ASSERT_MODE'])
                    if isinstance(assertError, MyAssertError):
                        retStr = "终止执行，测试结果[%s]: %s\n" % (assertError.testResult, assertError.retMsg.strip())
                    elif str(assertError) == "BREAK":
                        retStr = "<用户BREAK代码执行！>"
                    elif context.varsPool['ASSERT_MODE']:
                        retStr = "FAIL：断言失败！"  # 断言失败，不返回任何值影响断言。
                        context.testResult = ResultConst.FAIL
                        context.assertResult += "FAIL: 使用EXEC_PYTHON断言失败！\n\n"
                    else:
                        retStr = "<ERROR:执行python语句发生异常：python代码：\n%s\n发生异常：\n%s>" % (evalstring, traceback.format_exc())
                        context.setERROR( retStr)

                    context.varsPool['retStr'] = retStr
                except Exception or TypeError as e:
                    retStr = "<ERROR:执行python语句发生异常：python代码：\n%s\n发生异常：\n%s>" % (evalstring, traceback.format_exc())
                    context.setERROR( retStr)
                    context.varsPool['retStr'] = retStr
                    if context.varsPool['ASSERT_MODE']:
                        context.testResult = ResultConst.ERROR
                        context.assertResult += "ERROR: 执行python语句发生异常：python代码：\n%s\n发生异常：\n%s>\n\n" % (evalstring, traceback.format_exc())

        t = TimeLimited()
        t.start()
        t.join(timeout=timeout)
        if t.is_alive():
            stop_thread(t)
            raise Exception('FUNC_TIMEOUT')
        retStr = context.varsPool['retStr'] #将线程中的retStr带出来
        ###########开始处理生成的字典并加入到变量中
        if "VAR" in context.varsPool.keys():
            context.varsPool.pop("VAR")
        context.updateVarWhichNoPath()
        ###########结束处理生成的字典并加入到变量中

        if context.varsPool['ASSERT_MODE'] :
            if context.testResult != ResultConst.FAIL and context.testResult != ResultConst.ERROR:
                retStr = "PASS：断言通过！" # 断言通过，不返回任何值影响断言。
                context.testResult = ResultConst.PASS
                context.assertResult += "PASS: 使用EXEC_PYTHON断言通过！\n\n"
        else:
            if retStr == "":
                retStr = "<DONE: PYTHON执行成功>"

        if context.varsPool["DEBUG_MODE"]:
            retStr = retStr + "\nPython脚本:\n" + evalstring +"\n变量池：\n" + str(context.varsPool)

    except Exception as e:
        logging.error(traceback.format_exc())
        if str(e) == "FUNC_TIMEOUT":
            retStr = "<ERROR:执行python语句发生异常：python代码：\n%s\n发生异常：\n执行超时。>" % (evalstring)
            context.setERROR( retStr)

        elif str(e) == "IMPORT_DENIED":
            retStr = "<ERROR:执行python语句发生异常：python代码：\n%s\n发生异常：\n禁止使用import引入包，如果引入包需求，请联系管理员。>" % (evalstring)
            context.setERROR( retStr)

        else:
            retStr = "<ERROR:发生异常：\n%s>" % ( traceback.format_exc())
            context.setERROR( retStr)

        if context.varsPool['ASSERT_MODE']:
            context.testResult = ResultConst.ERROR
            context.assertResult += "ERROR: 发生异常：\n%s>\n\n" % (traceback.format_exc())
    finally:
        return retStr

@keyword()
@catch_exception
def ASSERT(value,context,strTobeProcessed = ""):
    try:
        retStr = ""
        strTobeProcessed = core.processor.KP.KP.process_KEYWORDS(strTobeProcessed, context)
        if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
            retMsg = "CASE_ERROR:关键字ASSERT执行时解析参数列表返回错误。返回参数列表为%s" % strTobeProcessed
            context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
            return retMsg
        #开始处理断言语句
        tmpAssertString = strTobeProcessed.strip()
        if tmpAssertString == "":
            return "<断言结果为空，不进行断言。>"
        else:
            # 执行db断言和正常断言
            tmpAssertString = core.processor.KP.KP.getProcessedValue(tmpAssertString, context)
            if context.protocol == "HTTP":
                #如果不是dubbo就是http的
                assertText = getRespTextByResponse(context.interface_response)
            elif context.protocol=="DUBBO":
                #如果是dubbo，就用dubbo的actualResult
                assertText = context.actualResult
            else:
                assertText = "错误的协议类型：%s" % context.protocol

            retList = Assert.assertExpectText(tmpAssertString, assertText)
            retStr = retList[1].strip() + "\n\n"
            context.testResult = retList[0]
            context.assertResult += retStr
            return retStr
    except:
        logging.error(traceback.format_exc())
        retStr = traceback.format_exc()
        context.testResult = "ERROR"
        context.assertResult += retStr
        return retStr

@keyword()
@catch_exception
def ASSERT_STRUCT(value,context,strTobeProcessed = ""):
    try:
        paramList = getParamList(strTobeProcessed, context)
        if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
            retMsg = "CASE_ERROR:关键字ASSERT_STRUCT执行时解析参数列表返回错误。返回参数列表为%s" % strTobeProcessed
            context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
            return retMsg
        #开始处理断言语句
        standardJson = ""
        actualJson = ""

        if len(paramList) == 2 and '"' not in strTobeProcessed:
            standardJson = paramList[0].strip()
            actualJson = paramList[1].strip()
        else:
            standardJson = strTobeProcessed.strip()
            if context.protocol == "HTTP":
                # 如果不是dubbo就是http的
                actualJson = getRespTextByResponse(context.interface_response)
            elif context.protocol == "DUBBO":
                # 如果是dubbo，就用dubbo的actualResult
                actualJson = context.actualResult
            else:
                actualJson = "错误的协议类型：%s" % context.protocol
                context.setERROR( actualJson)
                return actualJson
        print(standardJson)
        if isJson(standardJson) == False:
            retMsg = "<ERROR:ASSERT_STRUCT执行时预期结构不是json>"
            context.setERROR( retMsg)
            return retMsg
        if isJson(actualJson) == False:
            retMsg = "<ERROR:ASSERT_STRUCT执行时实际结构不是json>"
            context.setERROR( retMsg)
            return retMsg

        # 开始进行结构断言
        retList = Assert.assertStruct(standardJson, actualJson)
        retStr = retList[1].strip() + "\n\n"
        context.testResult = retList[0]
        context.assertResult += retStr
        return retStr

    except:
        logging.error(traceback.format_exc())
        retStr = traceback.format_exc()
        context.testResult = "ERROR"
        context.assertResult += retStr
        return retStr



