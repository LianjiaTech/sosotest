from core.decorator.normal_functions import *
from core.tools.CommonFunc import *
from core.processor.BP import BP
from core.keywords import kwKeyList  # 导入所有关键字,在 keywords.__init__.py中导入
import core.processor.KP
from core.processor.SelfKeywordProcesser import SelfKeywordProcesser
from core.tools.VerifyTool import VerifyTool


def processStrForPlatformVar(strbase):
    return strbase.replace("$VAR[","$VAR-[").replace("$GVAR[","$GVAR-[")\
        .replace("$TEXT[","$TEXT-[").replace("$RUNFUNC[","$RUNFUNC-[").replace("$IMPORT[","$IMPORT-[")\
        .replace("var(","var-[").replace("gvar(","gvar-[").replace("const(","const-[").replace("{{","{-{")

def processStrForPlatformKeyword(strbase):
    #系统关键字的处理
    for tmpKwKey in kwKeyList:
        strbase = strbase.replace("%s(" % tmpKwKey,"%s-(" % (tmpKwKey))
    #自定义关键字的处理
    selfKwList, selfKwDict = SelfKeywordProcesser.getSelfKeywordDict()
    for tmpKwKey in selfKwList:
        strbase = strbase.replace("%s(" % tmpKwKey,"%s-(" % (tmpKwKey))
    return strbase

def confuseAllStr(strBase):
    return processStrForPlatformVar(processStrForPlatformKeyword(strBase))

class CP(object):
    maxVarCallLoopCountForGvar = 10
    maxVarCallLoopCountForText = 2
    maxVarCallLoopCountForImports = 2
    maxVarCallLoopCountForVar = 300

    @staticmethod
    @catch_exception
    def process_TEXT_subStr(context,strTobeProcessed):
        """
                处理组合文本
                Args:
                    value: 要处理的字符串
                    context: 上下文，HttpBase的self本身
                    strTobeProcessed: 为装饰器keyword准备，装饰器会获取相应的要处理的文本后传入。

                Returns: 处理了所有$TEXT[]后的value。

                """
        if strTobeProcessed.strip() in context.highPriorityVARSDict.keys():
            return context.highPriorityVARSDict[strTobeProcessed.strip()]

        varKey = strTobeProcessed.strip()
        # 判断是否超出最大引用次数
        if varKey in context.varCallCountDict['TEXT'].keys():
            if context.varCallCountDict['TEXT'][varKey] > CP.maxVarCallLoopCountForText:
                resValue = "<ERROR:组合文本%s在单接口中被引用次数超过最大值,请检查是否存在循环引用。>" % varKey
                context.setERROR(resValue)
                return resValue
            else:
                context.varCallCountDict['TEXT'][varKey] += 1
        else:
            context.varCallCountDict['TEXT'][varKey] = 1

        db = context.globalDB
        db.setCursorDict(False)
        if db.connect() == False:
            context.setEXCEPTION("global数据库连接异常！请联系管理员检查配置！")
            return "<EXCEPTION:平台数据库连接异常，请联系管理员。>"
        if context.version == "CurrentVersion":
            res = db.execute_sql("SELECT textValue FROM tb_global_text WHERE textKey='%s' and state=1 " % strTobeProcessed.strip())
        else:
            res = db.execute_sql("SELECT textValue FROM tb_version_global_text WHERE textKey='%s' and versionName='%s' and state=1 " % (strTobeProcessed.strip(),context.version))

        resValue = ""
        textValue = ""
        if res:
            resValue = res[0][0].strip()
            endTag = "[ENDCONF]"
            if endTag in resValue:
                # 根据环境取值 如果当前环境有值用当前环境的值，如果没有用common中的
                startTag = "[CONF=common]"
                commonValue = get_sub_string(resValue, startTag, endTag).strip()
                startTag = "[CONF=%s]" % context.confHttpLayer.confServiceLayer.key  # 获取环境的key
                serviceValue = get_sub_string(resValue, startTag, endTag).strip()
                if commonValue == "" and serviceValue == "":
                    resValue = "<ERROR:当前环境未配置此组合文本%s>" % strTobeProcessed.strip()
                    context.setERROR(resValue)  #当没有获取到组合文本时，执行ERROR退出。
                else:
                    textValue = commonValue + "\n" + serviceValue
                    resValue = "<PASS: 成功处理组合文本%s>" % strTobeProcessed.strip()

        else:
            resValue = "<ERROR:不合法的组合文本%s>" % strTobeProcessed.strip()
            context.setERROR(resValue)  # 当没有获取到组合文本时，执行ERROR退出。

        db.setCursorDict(True)
        #对于获取到的文本进行一次处理。
        context.generateVarsKeyListAndVarsPool("%s" % textValue)
        return resValue

    """
    一些通用处理的类，针对核心执行的类HttpBase.py
    """
    @staticmethod
    @keyword(startTag="$TEXT[",endTag="]")
    @catch_exception
    def process_TEXT(value, context,strTobeProcessed = ""):
        return CP.process_TEXT_subStr(context,strTobeProcessed)

    @staticmethod
    @keyword(startTag="$INCLUDE[",endTag="]")
    @catch_exception
    def process_INCLUDE(value, context,strTobeProcessed = ""):
        return CP.process_TEXT_subStr(context,strTobeProcessed)

    @staticmethod
    @keyword(startTag="$IMPORT[",endTag="]")
    @catch_exception
    def process_IMPORT(value, context,strTobeProcessed = ""):
        return CP.process_TEXT_subStr(context,strTobeProcessed)

    @staticmethod
    @keyword(startTag="$RUNFUNC[",endTag="]")
    @catch_exception
    def process_RUNFUNC(value, context,strTobeProcessed = ""):
        return CP.process_TEXT_subStr(context,strTobeProcessed)

    @staticmethod
    @catch_exception
    def processAllTextImportEtc(value,context):
        value = CP.process_TEXT(value, context)
        value = CP.process_IMPORT(value, context)
        # value = CP.process_INCLUDE(value, context)
        value = CP.process_RUNFUNC(value, context)
        return value

    @staticmethod
    @keyword(startTag="$GVAR[", endTag="]")
    @catch_exception
    def process_GVAR(value, context, strTobeProcessed = ""):
        """
        处理全局变量
        Args:
            value: 要处理的字符串
            context: 上下文，HttpBase的self本身

        Returns: 处理了所有$GVAR[]后的value。

        """
        varKey = strTobeProcessed.strip()
        #判断是否超出最大引用次数
        if varKey in context.varCallCountDict['GVAR'].keys():
            if context.varCallCountDict['GVAR'][varKey] > CP.maxVarCallLoopCountForGvar:
                resValue = "<ERROR:全局变量%s在单接口中被引用次数超过最大值,请检查是否存在循环引用。>" % varKey
                context.setERROR(resValue)
                return resValue
            else:
                context.varCallCountDict['GVAR'][varKey] += 1
        else:
            context.varCallCountDict['GVAR'][varKey] = 1

        if varKey in context.highPriorityVARSDict.keys():
            resValue = context.highPriorityVARSDict[varKey]
        else:
            db = context.globalDB
            db.setCursorDict(False)
            if db.connect() == False:
                context.setEXCEPTION("global数据库连接异常！请联系管理员检查配置！")
                resValue = "<EXCEPTION:平台数据库连接异常，请联系管理员。>"
            else:
                if context.version == "CurrentVersion":
                    res = db.execute_sql("SELECT varValue FROM tb_global_vars WHERE varKey='%s' and state=1 " % varKey)
                else:
                    res = db.execute_sql("SELECT varValue FROM tb_version_global_vars WHERE varKey='%s'and versionName='%s'  and state=1 " % (varKey,context.version))

                if res:
                    resValue = res[0][0]
                    endTag = "[ENDCONF]"
                    if endTag in resValue:
                        # 根据环境取值 如果当前环境有值用当前环境的值，如果没有用common中的
                        startTag = "[CONF=common]"
                        commonValue = get_sub_string(resValue, startTag, endTag).strip()
                        startTag = "[CONF=%s]" % context.confHttpLayer.confServiceLayer.key #获取环境的key
                        serviceValue = get_sub_string(resValue, startTag, endTag).strip()
                        if serviceValue == "":
                            #没有指定环境的全局变量，使用common中的
                            if commonValue == "":
                                #没有通用环境的全局变量，返回异常。
                                resValue = "<ERROR:环境[%s]未配置此全局变量%s>" % (context.confHttpLayer.confServiceLayer.key,varKey)
                                context.setERROR(resValue)

                            else:
                                resValue = commonValue
                        else:
                            resValue = serviceValue
                else:
                    resValue = "<ERROR:不合法的全局变量%s>" % varKey
                    context.setERROR(resValue)

            db.setCursorDict(True)

        return core.processor.KP.KP.getProcessedValue(resValue,context)

    @staticmethod
    @keyword(startTag="gvar(", endTag=")")
    @catch_exception
    def process_gvar(value, context, strTobeProcessed=""):
        """
        处理全局变量
        Args:
            value: 要处理的字符串
            context: 上下文，HttpBase的self本身

        Returns: 处理了所有$GVAR[]后的value。

        """
        varKey = strTobeProcessed.strip()
        # 判断是否超出最大引用次数
        if varKey in context.varCallCountDict['GVAR'].keys():
            if context.varCallCountDict['GVAR'][varKey] > CP.maxVarCallLoopCountForGvar:
                resValue = "<ERROR:全局变量%s在单接口中被引用次数超过最大值,请检查是否存在循环引用。>" % varKey
                context.setERROR(resValue)
                return resValue
            else:
                context.varCallCountDict['GVAR'][varKey] += 1
        else:
            context.varCallCountDict['GVAR'][varKey] = 1

        if varKey in context.highPriorityVARSDict.keys():
            resValue = context.highPriorityVARSDict[varKey]
        else:
            db = context.globalDB
            db.setCursorDict(False)
            if db.connect() == False:
                context.setEXCEPTION("global数据库连接异常！请联系管理员检查配置！")
                resValue = "<EXCEPTION:平台数据库连接异常，请联系管理员。>"
            else:
                if context.version == "CurrentVersion":
                    res = db.execute_sql("SELECT varValue FROM tb_global_vars WHERE varKey='%s' and state=1 " % varKey)
                else:
                    res = db.execute_sql(
                        "SELECT varValue FROM tb_version_global_vars WHERE varKey='%s'and versionName='%s'  and state=1 " % (
                        varKey, context.version))

                if res:
                    resValue = res[0][0]
                    endTag = "[ENDCONF]"
                    if endTag in resValue:
                        # 根据环境取值 如果当前环境有值用当前环境的值，如果没有用common中的
                        startTag = "[CONF=common]"
                        commonValue = get_sub_string(resValue, startTag, endTag).strip()
                        startTag = "[CONF=%s]" % context.confHttpLayer.confServiceLayer.key  # 获取环境的key
                        serviceValue = get_sub_string(resValue, startTag, endTag).strip()
                        if serviceValue == "":
                            # 没有指定环境的全局变量，使用common中的
                            if commonValue == "":
                                # 没有通用环境的全局变量，返回异常。
                                resValue = "<ERROR:当前环境未配置此全局变量%s>" % varKey
                                context.setERROR(resValue)

                            else:
                                resValue = commonValue
                        else:
                            resValue = serviceValue
                else:
                    resValue = "<ERROR:不合法的全局变量%s>" % varKey
                    context.setERROR(resValue)

            db.setCursorDict(True)

        return core.processor.KP.KP.getProcessedValue(resValue,context)

    @staticmethod
    @keyword(startTag="$VAR[", endTag="]")
    @catch_exception
    def process_VARS(value,context, strTobeProcessed = ""):
        """
        处理变量
        Args:
            value: 要处理的字符串
            context: 上下文，HttpBase的self本身

        Returns: 处理了所有$VAR[]后的value。

        """

        #varsPool必须是
        # 先参数自替换
        varKeyStrip = strTobeProcessed.strip()
        # 判断是否超出最大引用次数
        varKey = varKeyStrip
        if not VerifyTool.IsVarMatch(varKey):
            resValue = "<ERROR:引用变量key[%s]不合法>" % varKey
            context.setERROR(resValue)
            return resValue

        if varKey in context.varCallCountDict['VAR'].keys():
            if context.varCallCountDict['VAR'][varKey] > CP.maxVarCallLoopCountForVar:
                resValue = "<ERROR:变量%s在单接口中被引用次数超过最大值,请检查是否存在循环引用。>" % varKey
                context.setERROR(resValue)
                return resValue
            else:
                context.varCallCountDict['VAR'][varKey] += 1
        else:
            context.varCallCountDict['VAR'][varKey] = 1

        if varKeyStrip == "":
            varValue = "<ERROR:变量名不能为空>"
            context.setERROR(varValue)
            return varValue

        if varKeyStrip in context.highPriorityVARSDict.keys():
            varValue = context.highPriorityVARSDict[varKeyStrip]
        else:
            if varKeyStrip not in context.varsPool.keys():
                varValue = "<ERROR:不合法的变量%s>" % varKeyStrip
                context.setERROR(varValue)
            else:
                varValue = context.varsPool[varKeyStrip]
                context.updateCalledVarkeyList(varKeyStrip)
        return processJsonalbeValue(varValue)

    @staticmethod
    @keyword(startTag="var(", endTag=")")
    @catch_exception
    def process_vars(value, context, strTobeProcessed=""):
        """
        处理变量
        Args:
            value: 要处理的字符串
            context: 上下文，HttpBase的self本身

        Returns: 处理了所有$VAR[]后的value。

        """

        # varsPool必须是
        # 先参数自替换
        varKeyStrip = strTobeProcessed.strip()
        # 判断是否超出最大引用次数
        varKey = varKeyStrip
        if not VerifyTool.IsVarMatch(varKey):
            resValue = "<ERROR:引用变量key[%s]不合法>" % varKey
            context.setERROR(resValue)
            return resValue

        if varKey in context.varCallCountDict['VAR'].keys():
            if context.varCallCountDict['VAR'][varKey] > CP.maxVarCallLoopCountForVar:
                resValue = "<ERROR:变量%s在单接口中被引用次数超过最大值,请检查是否存在循环引用。>" % varKey
                context.setERROR(resValue)
                return resValue
            else:
                context.varCallCountDict['VAR'][varKey] += 1
        else:
            context.varCallCountDict['VAR'][varKey] = 1

        if varKeyStrip == "":
            varValue = "<ERROR:变量名不能为空>"
            context.setERROR(varValue)
            return varValue

        if varKeyStrip in context.highPriorityVARSDict.keys():
            varValue = context.highPriorityVARSDict[varKeyStrip]
        else:
            if varKeyStrip not in context.varsPool.keys():
                varValue = "<ERROR:不合法的变量%s>" % varKeyStrip
                context.setERROR(varValue)
            else:
                varValue = context.varsPool[varKeyStrip]
                context.updateCalledVarkeyList(varKeyStrip)

        return processJsonalbeValue(varValue)

    @staticmethod
    @keyword(startTag="{{", endTag="}}")
    @catch_exception
    def process_common_ALL_TYPE_VAR(value,context, strTobeProcessed = ""):
        """
        处理变量
        Args:
            value: 要处理的字符串
            context: 上下文，HttpBase的self本身

        Returns: 处理了所有$VAR[]后的value。

        """

        #varsPool必须是
        # 先参数自替换
        varKeyStrip = strTobeProcessed.strip()
        varKey = varKeyStrip
        if varKeyStrip == "":
            varValue = "<ERROR:变量名不能为空>"
            context.setERROR(varValue)
            return varValue

        if varKeyStrip in context.highPriorityVARSDict.keys():
            # 判断是否超出最大引用次数
            if varKey in context.varCallCountDict['VAR'].keys():
                if context.varCallCountDict['VAR'][varKey] > CP.maxVarCallLoopCountForVar:
                    resValue = "<ERROR:变量%s在单接口中被引用次数超过最大值,请检查是否存在循环引用。>" % varKey
                    context.setERROR(resValue)
                    return resValue
                else:
                    context.varCallCountDict['VAR'][varKey] += 1
            else:
                context.varCallCountDict['VAR'][varKey] = 1

            varValue = context.highPriorityVARSDict[varKeyStrip]
        else:
            if varKeyStrip not in context.varsPool.keys():
                #进入全局变量匹配模式
                db = context.globalDB
                db.setCursorDict(False)
                if db.connect() == False:
                    context.setEXCEPTION("global数据库连接异常！请联系管理员检查配置！")
                    resValue = "<EXCEPTION:平台数据库连接异常，请联系管理员。>"
                else:
                    if context.version == "CurrentVersion":
                        res = db.execute_sql(
                            "SELECT varValue FROM tb_global_vars WHERE varKey='%s' and state=1 " % varKey)
                    else:
                        res = db.execute_sql(
                            "SELECT varValue FROM tb_version_global_vars WHERE varKey='%s'and versionName='%s'  and state=1 " % (
                            varKey, context.version))

                    if res:
                        # 判断是否超出最大引用次数
                        if varKey in context.varCallCountDict['GVAR'].keys():
                            if context.varCallCountDict['GVAR'][varKey] > CP.maxVarCallLoopCountForGvar:
                                resValue = "<ERROR:全局变量%s在单接口中被引用次数超过最大值,请检查是否存在循环引用。>" % varKey
                                context.setERROR(resValue)
                                return resValue
                            else:
                                context.varCallCountDict['GVAR'][varKey] += 1
                        else:
                            context.varCallCountDict['GVAR'][varKey] = 1
                        resValue = res[0][0]
                        endTag = "[ENDCONF]"
                        if endTag in resValue:
                            # 根据环境取值 如果当前环境有值用当前环境的值，如果没有用common中的
                            startTag = "[CONF=common]"
                            commonValue = get_sub_string(resValue, startTag, endTag).strip()
                            startTag = "[CONF=%s]" % context.confHttpLayer.confServiceLayer.key  # 获取环境的key
                            serviceValue = get_sub_string(resValue, startTag, endTag).strip()
                            if serviceValue == "":
                                # 没有指定环境的全局变量，使用common中的
                                if commonValue == "":
                                    # 没有通用环境的全局变量，返回异常。
                                    resValue = "<ERROR:环境[%s]未配置此全局变量%s>" % (context.confHttpLayer.confServiceLayer.key,varKey)
                                    context.setERROR(resValue)
                                else:
                                    resValue = commonValue
                                    resValue = core.processor.KP.KP.getProcessedValue(resValue, context)

                            else:
                                resValue = serviceValue
                                resValue = core.processor.KP.KP.getProcessedValue(resValue, context)

                    else:
                        resValue = "<ERROR:优先变量、变量和全局变量中没有匹配到%s。>" % varKey
                        context.setERROR(resValue)

                    varValue = resValue
            else:
                #进去局部变量匹配
                if not VerifyTool.IsVarMatch(varKeyStrip):
                    resValue = "<ERROR:引用变量key[%s]不合法>" % varKeyStrip
                    context.setERROR(resValue)
                    return resValue
                # 判断是否超出最大引用次数
                if varKey in context.varCallCountDict['VAR'].keys():
                    if context.varCallCountDict['VAR'][varKey] > CP.maxVarCallLoopCountForVar:
                        resValue = "<ERROR:变量%s在单接口中被引用次数超过最大值,请检查是否存在循环引用。>" % varKey
                        context.setERROR(resValue)
                        return resValue
                    else:
                        context.varCallCountDict['VAR'][varKey] += 1
                else:
                    context.varCallCountDict['VAR'][varKey] = 1
                #匹配到局部变量池的中的变量，直接返回。
                varValue = context.varsPool[varKeyStrip]
                context.updateCalledVarkeyList(varKeyStrip)

        return processJsonalbeValue(varValue)


    @staticmethod
    @keyword(startTag="$CONST[", endTag="]")
    @catch_exception
    def process_CONST(value, context, strTobeProcessed = ""):
        """
        处理全局常量
        Args:
            value: 要处理的字符串
            context: 上下文，HttpBase的self本身

        Returns: 处理了所有$CONST[]后的value。

        """

        constKeyList = ["RESP_STATUS","RESP_HEADER","RESP_TEXT","RESP_BODY","RESP_CONTENT",
                        "INTERFACE_RESP_STATUS","INTERFACE_RESP_HEADER","INTERFACE_RESP_TEXT","INTERFACE_RESP_BODY","INTERFACE_RESP_CONTENT",
                        "DUBBO_TEXT"]
        varKeyStrip = strTobeProcessed.strip()
        if varKeyStrip not in constKeyList:
            varValue = "<ERROR:不合法的常量%s，支持常量%s>" % (varKeyStrip, constKeyList)
            context.setERROR(varValue)
        else:
            try:
                if varKeyStrip == constKeyList[0]:
                    varValue = getRespCodeByResponse(context.response)
                elif varKeyStrip == constKeyList[1]:
                    varValue = confuseAllStr(getRespHeaderJsonByResponse(context.response))
                elif varKeyStrip == constKeyList[2] or varKeyStrip == constKeyList[3] or varKeyStrip == constKeyList[4]:
                    varValue = confuseAllStr(getRespTextByResponse(context.response))
                elif varKeyStrip == constKeyList[5]:
                    varValue = getRespCodeByResponse(context.interface_response)
                elif varKeyStrip == constKeyList[6]:
                    varValue = confuseAllStr(getRespHeaderJsonByResponse(context.interface_response))
                elif varKeyStrip == constKeyList[7] or varKeyStrip == constKeyList[8] or varKeyStrip == constKeyList[9]:
                    varValue = confuseAllStr(getRespTextByResponse(context.interface_response))
                elif varKeyStrip == constKeyList[10]:
                    varValue = confuseAllStr(context.dubboResponseString)
                else:
                    varValue = "<ERROR:未知的常量类型%s>" % varKeyStrip
            except Exception as e:
                varValue = "<EXCEPTION:不可知异常，请联系管理员解决>"
                context.setEXCEPTION(varValue)
        return varValue

    @staticmethod
    @keyword(startTag="const(", endTag=")")
    @catch_exception
    def process_const(value, context, strTobeProcessed = ""):
        """
        处理全局常量
        Args:
            value: 要处理的字符串
            context: 上下文，HttpBase的self本身

        Returns: 处理了所有$CONST[]后的value。

        """

        constKeyList = ["RESP_STATUS","RESP_HEADER","RESP_TEXT","RESP_BODY","RESP_CONTENT",
                        "INTERFACE_RESP_STATUS","INTERFACE_RESP_HEADER","INTERFACE_RESP_TEXT","INTERFACE_RESP_BODY","INTERFACE_RESP_CONTENT",
                        "DUBBO_TEXT"]
        varKeyStrip = strTobeProcessed.strip()
        if varKeyStrip not in constKeyList:
            varValue = "<ERROR:不合法的常量%s，支持常量%s>" % (varKeyStrip, constKeyList)
            context.setERROR(varValue)
        else:
            try:
                if varKeyStrip == constKeyList[0]:
                    varValue = getRespCodeByResponse(context.response)
                elif varKeyStrip == constKeyList[1]:
                    varValue = confuseAllStr(getRespHeaderJsonByResponse(context.response))
                elif varKeyStrip == constKeyList[2] or varKeyStrip == constKeyList[3] or varKeyStrip == constKeyList[4]:
                    varValue = confuseAllStr(getRespTextByResponse(context.response))
                elif varKeyStrip == constKeyList[5]:
                    varValue = getRespCodeByResponse(context.interface_response)
                elif varKeyStrip == constKeyList[6]:
                    varValue = confuseAllStr(getRespHeaderJsonByResponse(context.interface_response))
                elif varKeyStrip == constKeyList[7] or varKeyStrip == constKeyList[8] or varKeyStrip == constKeyList[9]:
                    varValue = confuseAllStr(getRespTextByResponse(context.interface_response))
                elif varKeyStrip == constKeyList[10]:
                    varValue = confuseAllStr(context.dubboResponseString)
                else:
                    varValue = "<ERROR:未知的常量类型%s>" % varKeyStrip
            except Exception as e:
                varValue = "<EXCEPTION:不可知异常，请联系管理员解决>"
                context.setEXCEPTION(varValue)
        return varValue


    @staticmethod
    @catch_exception
    def getProcessedValue(value,context):
        """
        处理value，所有都处理一遍。
        Args:
            value: 要处理的字符串
            context: 上下文，HttpBase的self本身
            isProcessKeyword: 是否处理关键字

        Returns: 处理了所有属性后的value

        """
        value = CP.processAllTextImportEtc(value, context)
        value = BP.process_branch_IF(value,context)
        value = CP.process_CONST(value, context)
        value = CP.process_GVAR(value, context)
        value = CP.process_VARS(value, context)
        value = CP.process_common_ALL_TYPE_VAR(value, context)
        value = CP.process_const(value, context)
        value = CP.process_gvar(value, context)
        value = CP.process_vars(value, context)
        return value


if __name__ == '__main__':
    value = "NOW_FORMAT(%Y)"
    value = eval("NOW_FORMAT(value)")
    print (value)


