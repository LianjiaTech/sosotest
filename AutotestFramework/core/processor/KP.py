from core.processor.CP import CP
from core.processor.BP import BP
from core.keywords import *  # 导入所有关键字,在 keywords.__init__.py中导入
from core.decorator.normal_functions import catch_exception
from core.processor.SelfKeywordProcesser import SelfKeywordProcesser
from core.tools.ExecFunc import *

class KP(object):
    @staticmethod
    @catch_exception
    def process_KEYWORDS(value,context,isTransSplitTag = False,splitTag = ","):
        """
        处理关键字
        Args:
            value: 要处理的字符串
            context: 上下文，HttpBase的self本身

        Returns: 处理了所有keyword后的value

        """
        #处理完所有变量引用，开始处理变量中的关键字
        valueKwStrList = value.split("(")
        importStr = """
%s
from core.const.GlobalConst import ResultConst
from core.decorator.normal_functions import keyword,time_limited,catch_exception
from core.keywords.ALL_FUNC import *
from core.tools.CommonFunc import *
from core.processor.HttpProcesserV2 import HttpProcesserV2
from core.processor.HttpProcesser import HttpProcesser
""" % getPythonThirdLib().strip()
        for kwStr in valueKwStrList:
            #在标准关键字中查找并处理
            isFindInStandard = False
            for i in range(0, len(kwKeyList)):
                tmpKwKey = kwKeyList[i]
                if kwStr.endswith(tmpKwKey) and tmpKwKey in value:
                    value = eval("%s(value,context)" % kwKeyList[i].strip())
                    isFindInStandard = True

            if isFindInStandard == False:
                selfKwList, selfKwDict = SelfKeywordProcesser.getSelfKeywordDict()
                #如果没有在标准关键字中发现，那么就在自定义关键字中查找并处理
                for selfKwIndex in range(0, len(selfKwList)):
                    tmpSelfKwKey = selfKwList[selfKwIndex]
                    if kwStr.endswith(tmpSelfKwKey) and tmpSelfKwKey in value:
                        #开始处理自定义关键字 tmpSelfKwKey
                        selfKwCodeStr = selfKwDict[tmpSelfKwKey]
                        processValueCodeStr = """value = %s(value,context)""" % tmpSelfKwKey
                        nameDict = {"context": context, "value":value}
                        exec(importStr, nameDict)
                        finalExecStr="%s\n%s" % (selfKwCodeStr,processValueCodeStr)
                        timeout = getKeywordExecPythonTimeout("timoutForSelfKeyword")
                        class TimeLimited(Thread):
                            def __init__(self):
                                Thread.__init__(self)

                            def run(self):
                                try:
                                    exec(finalExecStr, nameDict)
                                except Exception as eInner:
                                    nameDict["value"] = "<ERROR:自定义关键字执行发生异常：\n%s>" % (traceback.format_exc())
                                    context.setERROR( nameDict["value"])

                        t = TimeLimited()
                        t.start()
                        t.join(timeout=timeout)
                        if t.is_alive():
                            stop_thread(t)
                            value = '<ERROR:自定义关键字执行超时，超时时间%s秒。>' % timeout
                            context.setERROR( value)
                        else:
                            if nameDict["value"].startswith("★★★★★★★★★★平台异常，请联系管理员★★★★★★★★★★"):
                                value = "<ERROR:自定义关键字执行发生未知异常：\n%s>" % nameDict["value"]
                                context.setERROR( value)
                            else:
                                value = nameDict["value"]
        return value

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
        value = KP.process_KEYWORDS(value, context)
        value = CP.process_CONST(value, context)
        value = CP.process_GVAR(value, context)
        value = CP.process_VARS(value, context)
        value = CP.process_common_ALL_TYPE_VAR(value, context)
        value = CP.process_const(value, context)
        value = CP.process_gvar(value, context)
        value = CP.process_vars(value, context)
        return value
