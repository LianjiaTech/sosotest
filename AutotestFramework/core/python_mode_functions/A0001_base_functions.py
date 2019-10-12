from core.python_mode_functions import *

#平台互通引用
import core.processor.CP
import core.processor.KP
from core.tools.CommonFunc import getRespTextByResponse
from core.processor.Assert import Assert,MyAssertError
from core.keywords.ALL_FUNC import executeAndTransferContext,isLoop,processWhetherIGNORE
from core.tools.CommonFunc import isJson,get_sub_string

from core.model.CommonAttr import CommonAttr
context = CommonAttr()

#引入自定义关键字
def imports(codeKey):
    '''
    引入并执行自定义python代码
    :param codeKey: python代码的key
    :return: 无返回值
    '''
    # 判断是否超出最大引用次数
    if codeKey in context.varCallCountDict['imports'].keys():
        if context.varCallCountDict['imports'][codeKey] > core.processor.CP.CP.maxVarCallLoopCountForImports:
            resValue = "<ERROR:python引入%s在单接口中被引用次数超过最大值,请检查是否存在循环imports。>" % codeKey
            set_result("ERROR",resValue)
        else:
            context.varCallCountDict['imports'][codeKey] += 1
    else:
        context.varCallCountDict['imports'][codeKey] = 1

    context.globalDB.initGlobalDBConf()
    context.globalDB.setCursorDict(False)
    codeList = context.globalDB.execute_sql("SELECT keywordCode FROM tb4_data_keyword WHERE status = 3 AND state = 1 AND type='PYTHON_CODE' AND keywordKey='%s' " % codeKey)
    context.globalDB.release()
    if codeList:
        exec(codeList[0][0], context.varsPool)
    else:
        set_result("ERROR","<ERROR:不存在的codeKey[%s]>" % codeKey)

#日志输出函数，调用后可以将日志结果返回到对应的python执行区域
def log(logstr):
    '''
    python模式中打印日志，能够通过平台看到输出。
    :param logstr: 要打印的内容
    :return: 无返回值，直接输出。
    '''
    context.pythonModeExecuteLog += str(logstr) + "\n"
#日志输出函数，调用后可以将日志结果返回到对应的python执行区域

def prints(logstr):
    '''
    python模式中打印日志，能够通过平台看到输出。
    :param logstr: 要打印的内容
    :return: 无返回值，直接输出。
    '''
    context.pythonModeExecuteLog += str(logstr) + "\n"

#可以调用平台的数据关键字，例如call("TIMSTAMP(+0D)") 就是使用平台的数据关键字获取时间
def call(callStr):
    '''
    调用平台的关键字，例如call("LOGIN_CAS(100000000100010)")，可以执行登录关键字。
    :param callStr: 要调用的平台关键字
    :return: 返回平台关键字的返回字符串
    '''
    if "EXECUTE_INTERFACE(" in callStr or "EXECUTE_DUBBO_INTERFACE(" in callStr or "EXECUTE_TESTCASE(" in callStr:
        retCallStr = "<ERROR：python模式下执行其他接口请使用python模式内置函数 execute_interface(*args),execute_dubbo_interface(*args),execute_testcase(*args)>"
        set_result("ERROR", retCallStr)
        return retCallStr

    if "ASSERT(" in callStr :
        retCallStr = "<ERROR：python模式下请使用python模式内置函数 asserts(assertStr) >"
        set_result("ERROR",retCallStr)
        return retCallStr

    if "DB_SELECT(" in callStr :
        retCallStr = "<ERROR：python模式下请使用python模式内置函数 db_select(*args) >"
        set_result("ERROR",retCallStr)
        return retCallStr
    if "DB_UPDATE(" in callStr :
        retCallStr = "<ERROR：python模式下请使用python模式内置函数 db_update(*args) >"
        set_result("ERROR",retCallStr)
        return retCallStr
    if "DB_DELETE(" in callStr :
        retCallStr = "<ERROR：python模式下请使用python模式内置函数 db_delete(*args) >"
        set_result("ERROR",retCallStr)
        return retCallStr
    if "DB_INSERT(" in callStr :
        retCallStr = "<ERROR：python模式下请使用python模式内置函数 db_insert(*args) >"
        set_result("ERROR",retCallStr)
        return retCallStr

    if "REDIS_SET(" in callStr:
        retCallStr = """<ERROR：python模式下组合文本引用请使用python模式内置函数 redis_set(rediskey,value, timeout = None,db = 0, service="default") >"""
        set_result("ERROR", retCallStr)
        return retCallStr
    if "REDIS_GET(" in callStr:
        retCallStr = """<ERROR：python模式下组合文本引用请使用python模式内置函数 redis_get(rediskey,db = 0, service="default") >"""
        set_result("ERROR", retCallStr)
        return retCallStr
    if "REDIS_DEL(" in callStr:
        retCallStr = """<ERROR：python模式下组合文本引用请使用python模式内置函数 redis_del(rediskey,db = 0, service="default") >"""
        set_result("ERROR", retCallStr)
        return retCallStr

    return core.processor.KP.KP.getProcessedValue(callStr, context)

#一个参数时，从平台变量池取值，两个参数时设置变量到平台变量池,
def var(varkey, value = None):
    '''
    为平台变量池的变量赋值或者取值，只有参数varkey的时候是取值，有两个参数的时候是赋值。
    :param varkey: 平台变量池的变量key
    :param value: 要赋值的value
    :return: 变量值
    '''
    if value != None:
        context.setVar(varkey, value)
        context.updateCalledVarkeyList(varkey)
        return value
    else:
        return call("$VAR[" + varkey + "]")

#从全局变量中取值
def gvar(gvarkey):
    '''
    取平台的全局变量
    :param gvarkey: 全局变量的key
    :return: 全局变量的值
    '''
    return call("$GVAR[" + gvarkey + "]")

#去平台常量 RESP_TEXT DUBBO_TEXT 之类的
def const(constkey):
    '''
    取平台的常量值
    :param constkey: 常量key
    :return:  常量value
    '''
    return call("$CONST[" + constkey + "]")

#处理组合文本，生成变量或者关键字执行等。
def text(textkey):
    '''
    加载平台的组合文本
    :param textkey: 组合文本key
    :return: 无返回结果，直接处理文本数据
    '''
    return call("$TEXT[" + textkey + "]")

#执行当前的context，为数据驱动服务
def execute_current():
    '''
    执行当前对象（接口用例，或者业务流的步骤）的执行信息，http的发送http请求，dubbo的发送dubbo请求
    :return: 返回执行后的对象，例如可以用returnObj.interfaceId获取执行的是哪个接口或者步骤信息，用returnObj.processedParams可以获取http的执行的参数等。
    '''
    context.processExecuteAttrAndRun(False)
    return context

#执行HTTP接口
def execute_interface(*args):
    '''
    执行HTTP接口列表，可以有多个接口。
    :param args: http接口列表，最后一个arg可以是IGNORE_ALL IGNORE_FAIL_ERROR等忽略信息
    :return: 执行后的接口对象或者接口对象列表
    '''
    interfaceIdList = args
    # 如果获取参数等导致错误，不继续执行登录返回错误原因。

    # 处理 interfaceIdList 判断是否结果影响后续执行
    # IGNORE_ALL IGNORE_FAIL_ERROR
    interfaceIdList, whetherSetResultWhenFAIL, whetherSetResultWhenERROR, whetherSetResultWhenEXCEPTION = processWhetherIGNORE(interfaceIdList)
    # 处理结束 interfaceIdList #########
    startInterfaceId = context.interfaceId
    interfaceTobeExecutedList = []
    for i in range(0, len(interfaceIdList)):
        endInterfaceId = interfaceIdList[i].strip()
        if endInterfaceId == "":
            continue
        if isLoop(context.calledInterfaceRecurDict, startInterfaceId, endInterfaceId):
            tobeReplacedError = "接口[%s]被循环调用形成死循环，请检查用例。" % endInterfaceId
            set_result("ERROR", tobeReplacedError)
            break
        else:
            if startInterfaceId not in context.calledInterfaceRecurDict.keys():
                context.calledInterfaceRecurDict[startInterfaceId] = []
            context.calledInterfaceRecurDict[startInterfaceId].append(endInterfaceId)

        import allmodels.HttpInterface
        interfaceTobeExecuted = allmodels.HttpInterface.HttpInterface()
        interfaceTobeExecuted.interfaceId = endInterfaceId
        interfaceTobeExecuted.version = context.version  # 加入版本属性。
        retBool = interfaceTobeExecuted.generateByInterfaceId()
        if retBool == False:
            tobeReplacedError = "接口[%s]没有找到，请确认是否存在或者已删除。" % endInterfaceId
            set_result("ERROR", tobeReplacedError)
            break

        executeAndTransferContext(interfaceTobeExecuted,context)
        interfaceTobeExecutedList.append(interfaceTobeExecuted)
        log("执行接口[%s],执行结果:%s" % (interfaceTobeExecuted.interfaceId, interfaceTobeExecuted.testResult))

        if interfaceTobeExecuted.testResult == "FAIL":
            if whetherSetResultWhenFAIL:
                set_result(interfaceTobeExecuted.testResult, "执行接口%s结果FAIL，断言结果：%s" % (interfaceTobeExecuted.interfaceId, interfaceTobeExecuted.assertResult))

        if interfaceTobeExecuted.testResult == "ERROR":
            if whetherSetResultWhenERROR:
                set_result(interfaceTobeExecuted.testResult, "执行接口%s出现错误，错误原因：%s" % (interfaceTobeExecuted.interfaceId, interfaceTobeExecuted.assertResult))

        if interfaceTobeExecuted.testResult == "EXCEPTION":
            if whetherSetResultWhenEXCEPTION:
                set_result(interfaceTobeExecuted.testResult,"执行接口%s出现异常，异常原因：%s" % (interfaceTobeExecuted.interfaceId,interfaceTobeExecuted.assertResult))

    return interfaceTobeExecutedList[0] if len(interfaceTobeExecutedList) == 1 else interfaceTobeExecutedList

#执行DUBBO接口
def execute_dubbo_interface(*args):
    '''
       执行DUBBO接口列表，可以有多个接口。
       :param args: dubbo接口列表，最后一个arg可以是IGNORE_ALL IGNORE_FAIL_ERROR等忽略信息
       :return: 执行后的接口对象或者接口对象列表
       '''
    interfaceIdList = args
    # 如果获取参数等导致错误，不继续执行登录返回错误原因。

    # 处理 interfaceIdList 判断是否结果影响后续执行
    # IGNORE_ALL IGNORE_FAIL_ERROR
    interfaceIdList, whetherSetResultWhenFAIL, whetherSetResultWhenERROR, whetherSetResultWhenEXCEPTION = processWhetherIGNORE(interfaceIdList)
    # 处理结束 interfaceIdList #########

    startInterfaceId = context.interfaceId
    interfaceTobeExecutedList = []
    for i in range(0, len(interfaceIdList)):
        endInterfaceId = interfaceIdList[i].strip()
        if endInterfaceId == "":
            continue
        if isLoop(context.calledInterfaceRecurDict, startInterfaceId, endInterfaceId):
            tobeReplacedError = "接口[%s]被循环调用形成死循环，请检查用例。" % endInterfaceId
            set_result("ERROR", tobeReplacedError)
            break
        else:
            if startInterfaceId not in context.calledInterfaceRecurDict.keys():
                context.calledInterfaceRecurDict[startInterfaceId] = []
            context.calledInterfaceRecurDict[startInterfaceId].append(endInterfaceId)

        import allmodels.DubboInterface
        interfaceTobeExecuted = allmodels.DubboInterface.DubboInterface()
        interfaceTobeExecuted.interfaceId = endInterfaceId
        interfaceTobeExecuted.version = context.version  # 加入版本属性。
        retBool = interfaceTobeExecuted.generateByInterfaceId()
        if retBool == False:
            tobeReplacedError = "接口[%s]没有找到，请确认是否存在或者已删除。" % endInterfaceId
            set_result("ERROR", tobeReplacedError)
            break

        executeAndTransferContext(interfaceTobeExecuted, context)
        interfaceTobeExecutedList.append(interfaceTobeExecuted)
        log("执行接口[%s],执行结果:%s" % (interfaceTobeExecuted.interfaceId, interfaceTobeExecuted.testResult))

        if interfaceTobeExecuted.testResult == "FAIL":
            if whetherSetResultWhenFAIL:
                set_result(interfaceTobeExecuted.testResult, "执行接口%s结果FAIL，断言结果：%s" % (interfaceTobeExecuted.interfaceId, interfaceTobeExecuted.assertResult))

        if interfaceTobeExecuted.testResult == "ERROR":
            if whetherSetResultWhenERROR:
                set_result(interfaceTobeExecuted.testResult, "执行接口%s出现错误，错误原因：%s" % (interfaceTobeExecuted.interfaceId, interfaceTobeExecuted.assertResult))

        if interfaceTobeExecuted.testResult == "EXCEPTION":
            if whetherSetResultWhenEXCEPTION:
                set_result(interfaceTobeExecuted.testResult,"执行接口%s出现异常，异常原因：%s" % (interfaceTobeExecuted.interfaceId,interfaceTobeExecuted.assertResult))

    return interfaceTobeExecutedList[0] if len(interfaceTobeExecutedList) == 1 else interfaceTobeExecutedList

#执行HTTP业务流用例
def execute_testcase(*args):
    '''
       执行HTTP业务流列表，可以有多个业务流。
       :param args: http业务流列表，最后一个arg可以是IGNORE_ALL IGNORE_FAIL_ERROR等忽略信息
       :return: 执行后的业务流对象或者业务流对象列表
       '''
    TestCaseIdList = args

    # 处理 TestCaseIdList 判断是否结果影响后续执行
    # IGNORE_ALL IGNORE_FAIL_ERROR
    TestCaseIdList, whetherSetResultWhenFAIL, whetherSetResultWhenERROR, whetherSetResultWhenEXCEPTION = processWhetherIGNORE(TestCaseIdList)

    # 处理结束 TestCaseIdList #########

    startTestCaseId = context.caseId
    testCaseTobeExecuteList = []
    for i in range(0, len(TestCaseIdList)):
        endTestCaseId = TestCaseIdList[i].strip()
        if endTestCaseId == "":
            continue
        if isLoop(context.calledInterfaceRecurDict, startTestCaseId, endTestCaseId):
            tobeReplacedError = "用例[%s]被循环调用形成死循环，请检查用例。" % endTestCaseId
            set_result("ERROR", tobeReplacedError)
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
        log("执行业务流[%s],执行结果:%s" % (testCaseTobeExecute.caseId, testCaseTobeExecute.testResult))
        testCaseTobeExecuteList.append(testCaseTobeExecute)

        if testCaseTobeExecute.testResult == "FAIL":
            if whetherSetResultWhenFAIL:
                set_result(testCaseTobeExecute.testResult, "执行业务流%s结果FAIL，断言结果：%s" % (testCaseTobeExecute.caseId, testCaseTobeExecute.assertResult))

        if testCaseTobeExecute.testResult == "ERROR":
            if whetherSetResultWhenERROR:
                set_result(testCaseTobeExecute.testResult, "执行业务流%s出现错误，错误原因：%s" % (testCaseTobeExecute.caseId, testCaseTobeExecute.assertResult))

        if testCaseTobeExecute.testResult == "EXCEPTION":
            if whetherSetResultWhenEXCEPTION:
                set_result(testCaseTobeExecute.testResult,"执行业务流%s出现异常，异常原因：%s" % (testCaseTobeExecute.caseId,testCaseTobeExecute.assertResult))

    return testCaseTobeExecuteList[0] if len(testCaseTobeExecuteList) == 1 else testCaseTobeExecuteList

#使用平台方式进行断言
def asserts(assertStr,actual = None):
    '''
    断言函数
    :param assertStr:可以是一个非json，进行包含断言，可以是json，进行递归断言，可以是bool类型的，直接断言。也可以调用平台的[==]等进行断言
    :return: 一些输入，断言结果会直接写入context的testResult属性
    '''
    try:
        retStr = ""
        #如果是bool类型的，直接返回通过失败。
        if isinstance(assertStr,bool):
            if assertStr:
                context.testResult = "PASS"
                retStr = "断言结果是True，断言通过！"
                context.assertResult += retStr+"\n"
                return retStr
            else:
                context.testResult = "FAIL"
                retStr = "断言结果是False，断言失败！"
                context.assertResult += retStr + "\n"
                return retStr

        #如果是字符串类型的，开始常规断言
        if not isinstance(assertStr,str) and not isinstance(assertStr,int) and not isinstance(assertStr,float):
            context.testResult = "ERROR"
            retStr = "<ERROR: %s 必须是str/int/float/bool类型！>" % str(assertStr)
            context.assertResult += retStr + "\n"
            return retStr

        #开始处理断言语热天句
        tmpAssertString = str(assertStr).strip()
        if tmpAssertString == "":
            context.testResult = "ERROR"
            retStr = "<ERROR: 断言的string不能是空字符串！>"
            context.assertResult += retStr + "\n"
            return retStr
        else:
            tmpAssertString = core.processor.KP.KP.getProcessedValue(tmpAssertString, context)
            if actual is None:
                if context.protocol == "HTTP":
                    #如果不是dubbo就是http的
                    assertText = getRespTextByResponse(context.interface_response)
                elif context.protocol=="DUBBO":
                    #如果是dubbo，就用dubbo的actualResult
                    assertText = context.actualResult
                else:
                    context.testResult = "ERROR"
                    retStr = "错误的协议类型：%s" % context.protocol
                    context.assertResult += retStr + "\n"
                    return retStr
            else:
                assertText = actual

            retList = Assert.assertExpectText(tmpAssertString, assertText)
            retStr = retList[1].strip() + "\n\n"
            context.testResult = retList[0]
            context.assertResult += retStr
            return retStr
    except:
        log(traceback.format_exc())
        retStr = traceback.format_exc()
        context.testResult = "ERROR"
        context.assertResult += retStr
    finally:
        retResList = retStr.strip().split("\n")
        log("断言结束，断言结果：%s" % retResList[0] if len(retResList) == 1 else retResList[0]+"...(超出部分详见断言结果)")
        if context.testResult in context.exitExecStatusList:
            raise MyAssertError(context.testResult,retStr)
        return retStr

def assert_struct(expectJson,actual = None):
    '''
    断言数据结构
    :param expectJson: 预期结构，必填
    :param actual: 实际结构，选填，如果不写默认使用常量的返回值
    :return:
    '''
    try:
        #开始处理断言语句
        retStr = ""
        standardJson = expectJson.strip()
        if actual:
            actualJson = actual
        else:
            if context.protocol == "HTTP":
                #如果不是dubbo就是http的
                actualJson = getRespTextByResponse(context.interface_response)
            elif context.protocol=="DUBBO":
                #如果是dubbo，就用dubbo的actualResult
                actualJson = context.actualResult
            else:
                context.testResult = "ERROR"
                retStr = "错误的协议类型：%s" % context.protocol
                context.assertResult += retStr + "\n"
                return retStr

        if isJson(standardJson) == False:
            context.testResult = "ERROR"
            retStr =  "<ERROR:assert_struct执行时预期结构不是json>"
            context.assertResult += retStr + "\n"
            return retStr
        if isJson(actualJson) == False:
            context.testResult = "FAIL"
            retStr = "FAIL: assert_struct执行时返回的内容不是JSON。"
            context.assertResult += retStr + "\n"
            return retStr

        # 开始进行结构断言
        retList = Assert.assertStruct(standardJson, actualJson)
        retStr = retList[1].strip() + "\n\n"
        context.testResult = retList[0]
        context.assertResult += retStr
        return retStr

    except:
        log(traceback.format_exc())
        retStr = traceback.format_exc()
        context.testResult = "ERROR"
        context.assertResult += retStr
    finally:
        retResList = retStr.strip().split("\n")
        log("断言结束，断言结果：%s" % retResList[0] if len(retResList) == 1 else retResList[0]+"...(超出部分详见断言结果)")
        if context.testResult in context.exitExecStatusList:
            raise MyAssertError(context.testResult,retStr)
        return retStr

#使用平台方式进行断言
def set_result(testResult,assertMsg):
    '''
    设置测试结果，如果不是PASS将结束执行。
    :param testResult: 测试结果
    :param assertMsg: 断言信息
    :return: 无返回
    '''
    #testResult必须是PASS FAIL ERROR
    resList = ["PASS","FAIL","ERROR"]
    if testResult not in resList:
        context.setERROR( "set_result的第一个参必须是%s中的一个" % resList)
        raise MyAssertError("ERROR", "set_result的第一个参必须是%s中的一个" % resList)
    else:
        context.setResult(testResult,assertMsg)
        if testResult == "FAIL" or testResult == "ERROR":
            raise MyAssertError(testResult,assertMsg)

#使用DB查询
def db_select(*args):
    '''
    数据库查询
    :param args:参数可以是1个或者2个，1个的话就是sql语句，调用默认服务，2个的话第一个参数是数据服务key，第2个是sql语句。
    :return: sql查询的dict
    '''
    dbKey = "default"
    sqlstring = ""
    if len(args) == 1:
        sqlstring = args[0]
    elif len(args) == 2:
        dbKey = args[0]
        sqlstring = args[1]
    else:
        set_result("ERROR","执行db_select()时参数个数错误。")
        return "<ERROR:参数个数错误>"

    # 如果是更新或者删除或者插入操作，提示错误
    if sqlstring.strip().lower().startswith("update ") or sqlstring.strip().lower().startswith(
            "delete ") or sqlstring.strip().lower().startswith("insert "):
        set_result("ERROR","执行db_select()时只能使用SELECT语句。")
        return "<ERROR:只能使用SELECT语句>"

    if "delete " in sqlstring.strip().lower() or "update " in sqlstring.strip().lower() or "insert " in sqlstring.strip().lower():
        set_result("ERROR","执行db_select()时不能包含UPDATE/DELETE/INSERT操作！")
        return "<ERROR:不能包含UPDATE/DELETE/INSERT操作！>"

    if "where " not in sqlstring.strip().lower():
        set_result("ERROR","执行db_select()时必须包含where子句！")
        return "<ERROR:必须包含where子句！>"

    # 兼容旧的
    if not sqlstring.strip().lower().startswith("select "):
        set_result("ERROR","执行db_select()时开头必须是select！")
        return "<ERROR:使用db_select时，开头必须是select。>"

    if dbKey in context.serviceDBDict.keys():
        db = context.serviceDBDict[dbKey]
    else:
        set_result("ERROR","<ERROR:没有找到数据库%s的配置>" % dbKey)
        return "<ERROR:没有找到数据库%s的配置>" % dbKey

    # paramList = splitStringToListByTag(strTobeProcessed, splitTag)
    sqlstring = core.processor.CP.CP.getProcessedValue(sqlstring, context)
    if db.connect() == False:
        set_result("ERROR","<ERROR:service[%s]数据库连接异常>" % dbKey)
        return "<ERROR:service[%s]数据库连接异常>" % dbKey
    db.setCursorDict(True)

    # 判断影响行数
    if db.get_effected_rows_count(sqlstring.strip()) > 100:
        db.release()
        set_result("ERROR","<ERROR:DB_SELECT查询数据不得超过100行，请检查where子句。>")
        return "<ERROR:DB_SELECT查询数据不得超过100行，请检查where子句。>"

    res = db.execute_sql(sqlstring.strip())
    db.release()
    retList = []
    if isinstance(res,bool) and res == False:
        # check是否加了dbname.tablename
        fromTable = get_sub_string(sqlstring.strip().lower(), "from ", " where").strip()
        if fromTable and "." not in fromTable:
            set_result("ERROR","<ERROR:sql语句中的表名%s格式必须是database.table>" % fromTable)
            return "<ERROR:sql语句中的表名%s格式必须是database.table>" % fromTable
        else:
            set_result("ERROR","<ERROR:执行sql发生异常，请检查sql语句:%s>" % sqlstring.strip())
            return "<ERROR:执行sql发生异常，请检查sql语句:%s>" % sqlstring.strip()

    for tmpObj in res:
        tmpDict = {}
        for tmpK, tmpV in tmpObj.items():
            if isinstance(tmpV, datetime.datetime) or isinstance(tmpV, datetime.date):
                # 如果是datetime类型的，无法转换为json，要先转换为字符串
                tmpDict[tmpK] = str(tmpV)
            elif isinstance(tmpV, decimal.Decimal):
                tmpDict[tmpK] = str(decimal.Decimal(tmpV))
            else:
                tmpDict[tmpK] = tmpV
        retList.append(tmpDict)
    return json.dumps(retList)

#使用DB更新
def db_update(*args):
    '''
    数据库更新
    :param args:参数可以是1个或者2个，1个的话就是sql语句，调用默认服务，2个的话第一个参数是数据服务key，第2个是sql语句。
    :return: 更新结果
    '''
    dbKey = "default"
    sqlstring = ""
    if len(args) == 1:
        sqlstring = args[0]
    elif len(args) == 2:
        dbKey = args[0]
        sqlstring = args[1]
    else:
        set_result("ERROR", "执行db_select()时参数个数错误。")
        return "<ERROR:参数个数错误>"
    # 如果是更新或者删除或者插入操作，提示错误
    if sqlstring.strip().lower().startswith("select ") or sqlstring.strip().lower().startswith(
            "delete ") or sqlstring.strip().lower().startswith("insert "):

        set_result("ERROR","<ERROR:只能使用UPDATE语句>")
        return "<ERROR:只能使用UPDATE语句>"

    if "delete " in sqlstring.strip().lower() or "insert " in sqlstring.strip().lower():
        set_result("ERROR","<ERROR:不能包含DELETE/INSERT操作！>")
        return "<ERROR:不能包含DELETE/INSERT操作！>"

    if "where " not in sqlstring.strip().lower():
        set_result("ERROR","<ERROR:必须包含where子句！>")
        return "<ERROR:必须包含where子句！>"


    if dbKey in context.serviceDBDict.keys():
        db = context.serviceDBDict[dbKey]
    else:
        set_result("ERROR","<ERROR:没有找到数据库%s的配置,请联系管理员！>" % dbKey)
        return "<ERROR:没有找到数据库%s的配置>" % dbKey

    if db.connect() == False:
        set_result("ERROR", "service数据库连接异常！请联系管理员检查配置！")
        return "<ERROR:service[%s]数据库连接异常>" % dbKey
    db.setCursorDict(True)

    # 判断影响行数
    if db.get_effected_rows_count(sqlstring.strip()) > 100:
        db.release()
        set_result("ERROR", "<ERROR:DB_UPDATE一次更新数据不得超过100行，请检查where子句。>")
        return "<ERROR:DB_UPDATE一次更新数据不得超过100行，请检查where子句。>"

    res = db.execute_update_sql(sqlstring.strip())
    db.release()
    if isinstance(res,bool) and res == False:
        # check是否加了dbname.tablename
        fromTable =  get_sub_string(sqlstring.strip().lower(),"update "," set").strip()
        if fromTable and "." not in fromTable:
            set_result("ERROR","<ERROR:sql语句中的表名%s格式必须是database.table>" % fromTable)
            return "<ERROR:sql语句中的表名%s格式必须是database.table>" % fromTable
        else:
            set_result("ERROR","<ERROR:执行sql发生异常，请检查sql语句:%s>" % sqlstring.strip())
            return "<ERROR:执行sql发生异常，请检查sql语句:%s>" % sqlstring.strip()
    else:
        return str(res)

#使用DB删除
def db_delete(*args):
    '''
    数据库删除
    :param args:参数可以是1个或者2个，1个的话就是sql语句，调用默认服务，2个的话第一个参数是数据服务key，第2个是sql语句。
    :return: 删除结果
    '''
    dbKey = "default"
    sqlstring = ""
    if len(args) == 1:
        sqlstring = args[0]
    elif len(args) == 2:
        dbKey = args[0]
        sqlstring = args[1]
    else:
        set_result("ERROR", "执行db_select()时参数个数错误。")
        return "<ERROR:参数个数错误>"


    # 如果是更新或者删除或者插入操作，提示错误
    if sqlstring.strip().lower().startswith("select ") or sqlstring.strip().lower().startswith(
            "update ") or sqlstring.strip().lower().startswith("insert "):
        set_result("ERROR",  "<ERROR:只能使用DELETE语句>")
        return "<ERROR:只能使用DELETE语句>"

    if "update " in sqlstring.strip().lower() or "insert " in sqlstring.strip().lower():
        set_result("ERROR",  "<ERROR:不能包含UPDATE/INSERT操作！>")
        return "<ERROR:不能包含UPDATE/INSERT操作！>"

    if " where " not in sqlstring.strip().lower():
        set_result("ERROR",  "<ERROR:必须包含where子句！>")
        return "<ERROR:必须包含where子句！>"


    if dbKey in context.serviceDBDict.keys():
        db = context.serviceDBDict[dbKey]
    else:
        set_result("ERROR",   "<ERROR:没有找到数据库%s的配置,请联系管理员添加！>" % dbKey)
        return "<ERROR:没有找到数据库%s的配置>" % dbKey

    # paramList = splitStringToListByTag(strTobeProcessed, splitTag)

    if db.connect() == False:
        set_result("ERROR",   "<ERROR:service[%s]数据库连接异常>" % dbKey)
        return "<ERROR:service[%s]数据库连接异常>" % dbKey
    db.setCursorDict(True)

    # 判断影响行数
    if db.get_effected_rows_count(sqlstring.strip()) > 100:
        db.release()
        set_result("ERROR",  "<ERROR:DB_DELETE一次删除数据不得超过100行，请检查where子句。>")
        return "<ERROR:DB_DELETE一次删除数据不得超过100行，请检查where子句。>"

    res = db.execute_update_sql(sqlstring.strip())
    db.release()
    if isinstance(res,bool) and res == False:
        # check是否加了dbname.tablename
        fromTable = get_sub_string(sqlstring.strip().lower(), "from ", " where").strip()
        if fromTable and "." not in fromTable:
            set_result("ERROR","<ERROR:sql语句中的表名%s格式必须是database.table>" % fromTable)
            return "<ERROR:sql语句中的表名%s格式必须是database.table>" % fromTable
        else:
            set_result("ERROR","<ERROR:执行sql发生异常，请检查sql语句:%s>" % sqlstring.strip())
            return "<ERROR:执行sql发生异常，请检查sql语句:%s>" % sqlstring.strip()
    else:
        return str(res)

#使用DB插入
def db_insert(*args):
    '''
    数据库插入
    :param args:参数可以是1个或者2个，1个的话就是sql语句，调用默认服务，2个的话第一个参数是数据服务key，第2个是sql语句。
    :return: 插入结果
    '''
    dbKey = "default"
    sqlstring = ""
    if len(args) == 1:
        sqlstring = args[0].strip()
    elif len(args) == 2:
        dbKey = args[0].strip()
        sqlstring = args[1].strip()
    else:
        set_result("ERROR", "执行db_select()时参数个数错误。")
        return "<ERROR:参数个数错误>"


    # 如果是更新或者删除或者插入操作，提示错误
    if sqlstring.strip().lower().startswith("select ") or sqlstring.strip().lower().startswith(
            "update ") or sqlstring.strip().lower().startswith("delete "):
        set_result("ERROR", "<ERROR:只能使用INSERT语句>")
        return "<ERROR:只能使用INSERT语句>"

    if "update " in sqlstring.strip().lower() or "delete " in sqlstring.strip().lower():
        set_result("ERROR", "<ERROR:不能包含UPDATE/DELETE操作！>")
        return "<ERROR:不能包含UPDATE/DELETE操作！>"


    if dbKey in context.serviceDBDict.keys():
        db = context.serviceDBDict[dbKey]
    else:
        set_result("ERROR", "<ERROR:没有找到数据库%s的配置>" % dbKey)
        return "<ERROR:没有找到数据库%s的配置>" % dbKey

    # paramList = splitStringToListByTag(strTobeProcessed, splitTag)
    if db.connect() == False:
        set_result("ERROR",  "<ERROR:service[%s]数据库连接异常>" % dbKey)
        return "<ERROR:service[%s]数据库连接异常>" % dbKey
    db.setCursorDict(True)
    res = db.execute_update_sql(sqlstring.strip())
    db.release()
    if isinstance(res,bool) and res == False:
        # check是否加了dbname.tablename
        fromTable = get_sub_string(sqlstring.strip().lower(), "insert into ", "(").strip()
        if fromTable and "." not in fromTable:
            set_result("ERROR", "<ERROR:sql语句中的表名%s格式必须是database.table>" % fromTable)
            return "<ERROR:sql语句中的表名%s格式必须是database.table>" % fromTable
        else:
            set_result("ERROR", "<ERROR:执行sql发生异常，请检查sql语句:%s>" % sqlstring.strip())
            return "<ERROR:执行sql发生异常，请检查sql语句:%s>" % sqlstring.strip()
    else:
        return str(res)

#redis 设置数据
def redis_set(rediskey,value, timeout = None,db = 0, service="default"):
    '''
    设置redis的值
    :param rediskey: 要设置的key
    :param value:  要设置的value
    :param timeout: 超时时间
    :param db: 数据库 大于等于0
    :param service: 哪个服务key
    :return:
    '''
    key,value,db,dbKey,timeout = rediskey,value,db,service,timeout

    try:
        if timeout != None and int(timeout) > 0 :
            timeout = int(timeout)
        elif timeout == None:
            pass
        else:
            raise ValueError("不合法的timeout")
    except:
        retMsg = "CASE_ERROR:关redis_set调用时参数3[timeout]必须是大于0的整数或者是None。"
        set_result("ERROR", retMsg)
        return retMsg

    try:
        if int(db) >= 0 :
            db = int(db)
        else:
            raise ValueError("不合法的db")
    except:
        retMsg = "CASE_ERROR:redis_set调用时参数4[db]必须是大于等于0的整数。"
        set_result("ERROR", retMsg)
        return retMsg

    if dbKey in context.serviceRedisDict.keys():
        redisHand = context.serviceRedisDict[dbKey]
        redisHand.db = db
        try:
            redisHand.connect()
            setres = redisHand.set_data(key, value, timeout)
            if setres == True:
                return "REDIS设置成功！[%s]" % setres
            else:
                retMsg = "CASE_ERROR:关键字REDIS_SET设置失败。原因[%s]" % str(setres)
                context.setERROR(retMsg)
                return retMsg
        except:
            retMsg = "CASE_ERROR:redis_set调用时Redis数据库%s连接失败>" % dbKey
            set_result("ERROR", retMsg)
            return retMsg
    else:
        retMsg = "CASE_ERROR:redis_set调用时没有找到Redis数据库%s的配置>" % dbKey
        set_result("ERROR", retMsg)
        return retMsg

def redis_get(rediskey, db = 0, service="default"):
    '''
    从redis取值
    :param rediskey: 要取值的key
    :param db: 哪个数据库
    :param service: 服务key
    :return:
    '''

    key,db,dbKey = rediskey,db,service
    try:
        if int(db) >= 0 :
            db = int(db)
        else:
            raise ValueError("不合法的db")
    except:
        retMsg = "CASE_ERROR:redis_get调用时参数2[db]必须是大于等于0的整数。"
        set_result("ERROR", retMsg)
        return retMsg

    if dbKey in context.serviceRedisDict.keys():
        redisHand = context.serviceRedisDict[dbKey]
        redisHand.db = db
        try:
            redisHand.connect()
            try:
                retV = redisHand.get_data_for_data_keyword(key)
                return retV
            except:
                retMsg = "CASE_ERROR:redis_get没有找到这个key[%s]>" % key
                set_result("ERROR", retMsg)
                return retMsg
        except:
            retMsg = "CASE_ERROR:redis_get调用时Redis数据库%s连接失败>" % dbKey
            set_result("ERROR", retMsg)
            return retMsg
    else:
        retMsg = "CASE_ERROR:redis_get调用时没有找到Redis数据库%s的配置>" % dbKey
        set_result("ERROR", retMsg)
        return retMsg

def redis_del(rediskey, db = 0, service="default"):
    '''
    删除redis的值
    :param rediskey: 要删除的key
    :param db: 哪个数据库
    :param service: 服务key
    :return:
    '''

    key,db,dbKey = rediskey,db,service

    try:
        if int(db) >= 0 :
            db = int(db)
        else:
            raise ValueError("不合法的db")
    except:
        retMsg = "CASE_ERROR:redis_del调用时参数2[db]必须是大于等于0的整数。"
        set_result("ERROR", retMsg)
        return retMsg


    if dbKey in context.serviceRedisDict.keys():
        redisHand = context.serviceRedisDict[dbKey]
        redisHand.db = db
        try:
            redisHand.connect()
            try:
                retV = redisHand.del_data(key)
                return retV
            except:
                retMsg = "CASE_ERROR:redis_del没有找到这个key[%s]>" % key
                set_result("ERROR", retMsg)
                return retMsg
        except:
            retMsg = "CASE_ERROR:redis_del调用时Redis数据库%s连接失败>" % dbKey
            set_result("ERROR", retMsg)
            return retMsg
    else:
        retMsg = "CASE_ERROR:redis_del调用时没有找到Redis数据库%s的配置>" % dbKey
        set_result("ERROR", retMsg)
        return retMsg

def redis_flushall(db = 0, service="default"):
    '''
    删除redis的值
    :param rediskey: 要删除的key
    :param db: 哪个数据库
    :param service: 服务key
    :return:
    '''

    db,dbKey = db,service

    try:
        if int(db) >= 0 :
            db = int(db)
        else:
            raise ValueError("不合法的db")
    except:
        retMsg = "CASE_ERROR:redis_flushall调用时参数2[db]必须是大于等于0的整数。"
        set_result("ERROR", retMsg)
        return retMsg

    if dbKey in context.serviceRedisDict.keys():
        redisHand = context.serviceRedisDict[dbKey]
        redisHand.db = db
        try:
            redisHand.connect()
            try:
                retV = redisHand.flushall()
                return retV
            except:
                retMsg = "CASE_ERROR:redis_flushall执行异常>"
                set_result("ERROR", retMsg)
                return retMsg
        except:
            retMsg = "CASE_ERROR:redis_flushall调用时Redis数据库%s连接失败>" % dbKey
            set_result("ERROR", retMsg)
            return retMsg
    else:
        retMsg = "CASE_ERROR:redis_flushall调用时没有找到Redis数据库%s的配置>" % dbKey
        set_result("ERROR", retMsg)
        return retMsg

def mongo_insert(*args):
    """
    REDIS_FLUSH_ALL(db=0,service=mls-biz-support)
    :param key: 必须的
    :param db: 可选的，0-15 默认是0
    :param system: 可选的，默认是Default
    :return:
    """
    paramList = args
    if len(paramList) != 4 and len(paramList) != 3:
        retMsg = "CASE_ERROR:内置函数mongo_insert调用时参数必须是3个或者4个（调用默认库时不需要穿servicekey）。"
        set_result("ERROR",retMsg)
        return retMsg

    if len(paramList) == 3:
        mongoServiceKey, dbname, setname, insertDictOrList = "default",paramList[0],paramList[1],paramList[2]
    else:
        mongoServiceKey, dbname, setname, insertDictOrList = paramList[0],paramList[1],paramList[2],paramList[3]


    if not isinstance(insertDictOrList,dict) and not isinstance(insertDictOrList, list):
        retMsg = "CASE_ERROR:内置函数mongo_insert调用时插入的值必须是dict或者list！"
        set_result("ERROR", retMsg)
        return retMsg

    try:
        insertRes = context.serviceMongoDBDict[mongoServiceKey].refresh_collect(dbname,setname).insert(insertDictOrList)
        return str(insertRes)
    except:
        retMsg = "CASE_ERROR:内置函数mongo_insert执行时出现异常！\n参数列表%s\n异常原因：%s" % (paramList, traceback.format_exc())
        set_result("ERROR", retMsg)
        return retMsg

def mongo_find(*args):
    """
    REDIS_FLUSH_ALL(db=0,service=mls-biz-support)
    :param key: 必须的
    :param db: 可选的，0-15 默认是0
    :param system: 可选的，默认是Default
    :return:
    """
    paramList = args
    if len(paramList) != 4 and len(paramList) != 3:
        retMsg = "CASE_ERROR:内置函数mongo_find调用时参数必须是3个或者4个（调用默认库时不需要穿servicekey）。"
        set_result("ERROR",retMsg)
        return retMsg

    if len(paramList) == 3:
        mongoServiceKey, dbname, setname, insertDictOrList = "default",paramList[0],paramList[1],paramList[2]
    else:
        mongoServiceKey, dbname, setname, insertDictOrList = paramList[0],paramList[1],paramList[2],paramList[3]


    if not isinstance(insertDictOrList,dict):
        retMsg = "CASE_ERROR:内置函数mongo_find调用时最后一个参数必须是dict！"
        set_result("ERROR", retMsg)
        return retMsg

    try:
        insertRes = context.serviceMongoDBDict[mongoServiceKey].refresh_collect(dbname,setname).find_to_list(insertDictOrList)
        return json.dumps(insertRes)
    except:
        retMsg = "CASE_ERROR:内置函数mongo_find执行时出现异常！\n参数列表%s\n异常原因：%s" % (paramList, traceback.format_exc())
        set_result("ERROR", retMsg)
        return retMsg

def mongo_remove(*args):
    """
    REDIS_FLUSH_ALL(db=0,service=mls-biz-support)
    :param key: 必须的
    :param db: 可选的，0-15 默认是0
    :param system: 可选的，默认是Default
    :return:
    """
    paramList = args
    if len(paramList) != 4 and len(paramList) != 3:
        retMsg = "CASE_ERROR:内置函数mongo_remove调用时参数必须是3个或者4个（调用默认库时不需要穿servicekey）。"
        set_result("ERROR",retMsg)
        return retMsg

    if len(paramList) == 3:
        mongoServiceKey, dbname, setname, insertDictOrList = "default",paramList[0],paramList[1],paramList[2]
    else:
        mongoServiceKey, dbname, setname, insertDictOrList = paramList[0],paramList[1],paramList[2],paramList[3]


    if not isinstance(insertDictOrList,dict) and not isinstance(insertDictOrList, list):
        retMsg = "CASE_ERROR:内置函数mongo_remove调用时插入的值必须是dict或者list！"
        set_result("ERROR", retMsg)
        return retMsg

    try:
        insertRes = context.serviceMongoDBDict[mongoServiceKey].refresh_collect(dbname,setname).remove(insertDictOrList)
        return json.dumps(insertRes)
    except:
        retMsg = "CASE_ERROR:内置函数mongo_remove执行时出现异常！\n参数列表%s\n异常原因：%s" % (paramList, traceback.format_exc())
        set_result("ERROR", retMsg)
        return retMsg

def mongo_update(*args):
    """
    REDIS_FLUSH_ALL(db=0,service=mls-biz-support)
    :param key: 必须的
    :param db: 可选的，0-15 默认是0
    :param system: 可选的，默认是Default
    :return:
    """
    paramList = args
    if len(paramList) != 4 and len(paramList) != 5:
        retMsg = "CASE_ERROR:内置函数mongo_update调用时参数必须是4个或者5个（调用默认库时不需要穿servicekey）。"
        set_result("ERROR",retMsg)
        return retMsg

    if len(paramList) == 4:
        mongoServiceKey, dbname, setname, insertDictOrList,updateDict = "default",paramList[0],paramList[1],paramList[2],paramList[3]
    else:
        mongoServiceKey, dbname, setname, insertDictOrList,updateDict = paramList[0],paramList[1],paramList[2],paramList[3],paramList[4]


    if not isinstance(insertDictOrList,dict) or not isinstance(updateDict, dict):
        retMsg = "CASE_ERROR:内置函数mongo_update调用时条件和修改的值必须是dict！"
        set_result("ERROR", retMsg)
        return retMsg

    try:
        insertRes = context.serviceMongoDBDict[mongoServiceKey].refresh_collect(dbname,setname).update(insertDictOrList,updateDict)
        return json.dumps(insertRes)
    except:
        retMsg = "CASE_ERROR:内置函数mongo_update执行时出现异常！\n参数列表%s\n异常原因：%s" % (paramList, traceback.format_exc())
        set_result("ERROR", retMsg)
        return retMsg