import logging
from core.decorator.normal_functions import *
from core.tools.CommonFunc import *
from core.processor.CP import CP
from core.processor.KP import KP

class VP(object):

    @staticmethod
    @catch_exception
    def generateHighPriorityVARSDict(varsString,context):
        """
        在任务执行前用与生成任务的优先变量。
        """
        varsString = CP.processAllTextImportEtc(varsString, context)
        varsFinalStr = VP.getFinalVarsStringByHttpConfKey(varsString,context)
        varsKeyList,varsValueList = VP.getVarsKeyListByVarsString(varsFinalStr)
        retDict = {}
        for i in range(0, len(varsKeyList)):
            tmpKey = varsKeyList[i].strip()
            tmpValue = varsValueList[i].strip()
            tmpValue = CP.process_GVAR(tmpValue,context)
            #DONE 处理tmpValue，可以使用oldVarsDict中的任意变量，自己输入的;要带转义符
            if tmpKey != "":
                if tmpKey in retDict.keys():
                    retDict.pop(tmpKey)
                retDict[tmpKey] = tmpValue

        return retDict

    @staticmethod
    @catch_exception
    def getFinalVarsStringByHttpConfKey(vars,context):
        """
        得到最终的varsString,包括common的和对应的测试环境的。
        Args:
            vars: 要处理的整体vars的字符串，比如
                    [CONF=common]
                    [ENDCONF]
                    [CONF=test]
                    [ENDCONF]
        Returns:
            处理后的varsString，比如
            k1=v1;
            k2=v2;
        """
        startTag = "[CONF=common]"
        endTag = "[ENDCONF]"
        varsString1 = get_sub_string(vars, startTag, endTag).strip()
        if varsString1[-1:] != ";":
            varsString1 += ";"
        startTag = "[CONF=%s]" % context.confHttpLayer.confServiceLayer.key
        endTag = "[ENDCONF]"
        varsString2 = get_sub_string(vars,startTag,endTag).strip()
        return varsString1 + "\n" + varsString2

    @staticmethod
    @catch_exception
    def getVarsKeyListByVarsString(varsString):
        """
        得到通过varsString得到varkeyList
        Args:
            varsString: 比如
                    k1=v1;
                    k2=v2;
                    k3=v3;

        Returns:
            varskeyList，例如 ["k1","k2","k3"]
        """
        varsList = splitStringToListByTag(varsString,";")
        return VP.getVarsKeyListByVarsList(varsList)

    ####一些内部调用函数####
    ###变量 string json dict之间的转换函数
    @staticmethod
    @catch_exception
    def getVarsKeyListByVarsList(varsList):
        """
        通过varsList得到keylist
        Args:
            varsList: 处理过后的varslist，例如
                    ["k1=v1","k2=v2","k3=v3"]

        Returns:
            keyList,例如 ["k1","k2","k3"]
        """
        varsKeyList = []
        varsValueList = []
        for i in range(0,len(varsList)):
            tmpVarList = varsList[i].strip().split("=")
            if len(tmpVarList) >= 2 and varsList[i].strip()[0:1] != "#":
                #合法的key value并且不是#开头的注释语句，加入dict
                tmpkey = tmpVarList[0].strip()
                tmpValue = tmpVarList[1].strip()
                for j in range(2,len(tmpVarList)):
                    tmpValue = tmpValue + "=" + tmpVarList[j]
                #结束key 和 value赋值
                varsKeyList.append(tmpkey.strip())
                varsValueList.append(tmpValue.strip())
        return  varsKeyList,varsValueList
