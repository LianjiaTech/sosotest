from core.decorator.normal_functions import keyword,catch_exception
from core.tools.TypeTool import TypeTool
from core.keywords.ALL_FUNC import *
from core.const.GlobalConst import ResultConst
import re
from urllib import parse
from bs4 import BeautifulSoup
import hashlib
import jsonpath


################
#JSON处理函数
################
#jsonPath获取JOSN


@keyword()
@catch_exception
def JSON_PATH_GET_FIRST(value,context, strTobeProcessed = ""):
    paramList = getParamList(strTobeProcessed, context)
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字JSON_PATH_GET执行时解析参数列表返回错误。返回参数列表为%s" % str(paramList)
        context.assertResult = "%s\n%s" % (retMsg, context.assertResult)

        return retMsg

    jsonString = ""
    jsonPath = ""
    if len(paramList) == 2:
        jsonPath = paramList[1].strip().replace('"', "'")
        jsonString = paramList[0].strip()
        try:
            if isJson(jsonString):
                jsonDict = json.loads(jsonString)
            else:
                jsonDict = json.loads(processJsonString(jsonString))
            jsonValue = eval("""jsonpath.jsonpath(jsonDict,"%s")""" % jsonPath)

            if TypeTool.is_list(jsonValue) and len(jsonValue) > 0:
                jsonValue = jsonValue[0]

            if TypeTool.is_list(jsonValue) or TypeTool.is_dict(jsonValue):
                jsonValue = json.dumps(jsonValue, ensure_ascii=False)
            else:
                jsonValue = str(jsonValue)

        except Exception as e:
            logging.error(traceback.format_exc())
            logging.error("JSONSTRING:\n%s\nJSON_PATH: %s" % (jsonString,jsonPath))
            jsonValue = "<ERROR:JSON或者路径错误>"
            context.setResult("ERROR", jsonValue)

    else:
        jsonValue = "<ERROR:参数错误>"
        context.setResult("ERROR", jsonValue)

    return jsonValue

@keyword()
@catch_exception
def JSON_PATH_GET(value,context, strTobeProcessed = ""):
    paramList = getParamList(strTobeProcessed, context)
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字JSON_PATH_GET执行时解析参数列表返回错误。返回参数列表为%s" % str(paramList)
        context.assertResult = "%s\n%s" % (retMsg, context.assertResult)

        return retMsg

    jsonString = ""
    jsonPath = ""
    if len(paramList) == 2:
        jsonPath = paramList[1].strip().replace('"', "'")
        jsonString = paramList[0].strip()

        try:
            jsonDict = transferJsonToDict(jsonString)
            if jsonDict != False:
                jsonValue = eval("""jsonpath.jsonpath(jsonDict,"%s")""" % jsonPath)
            else:
                context.setERROR( "<ERROR:不是合法的JSON。> JSON_STRING:\n%s" % jsonString)
                return "<ERROR:不是合法的JSON。>"

            if isCanDump(jsonValue):
                jsonValue = json.dumps(jsonValue, ensure_ascii=False)
            else:
                jsonValue = str(jsonValue)

        except Exception as e:
            jsonValue = "<ERROR:JSON字符串不合法或者JSON路径错误:%s>" % str(e)
            context.setERROR( jsonValue)

    else:
        jsonValue = "<ERROR:参数错误>"
        context.setERROR( jsonValue)

    return jsonValue


@keyword()
@catch_exception
def JSON_GET(value,context, strTobeProcessed = ""):
    #开始处理paramsString jsonstring),( path
    paramList = getParamList(strTobeProcessed,context)

    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字JSON_GET执行时解析参数列表返回错误。返回参数列表为%s" % str(paramList)
        context.assertResult = "%s\n%s" % (retMsg,context.assertResult)
        return retMsg

    jsonString = ""
    jsonPath = ""
    if len(paramList) == 2:
        jsonPath = paramList[1].strip()
        jsonString = paramList[0].strip()
        try:
            jsonDict = transferJsonToDict(jsonString)
            if jsonDict != False:
                jsonValue = eval("jsonDict%s" % jsonPath)
            else:
                context.setERROR( "<ERROR:不是合法的JSON。> JSON_STRING:\n%s" % jsonString)
                return "<ERROR:不是合法的JSON。>"
            if isCanDump(jsonValue):
                jsonValue = json.dumps(jsonValue,ensure_ascii = False)
            else:
                jsonValue = str(jsonValue)
        except Exception as e:
            jsonValue = "<ERROR:JSON字符串不合法或者JSON路径错误:%s>" % str(e)
            context.setERROR( jsonValue)
    else:
        jsonValue = "<ERROR:参数错误>"
        context.setERROR( jsonValue)
    return jsonValue


@keyword()
@catch_exception
def JSON_PATH_EXIST(value,context, strTobeProcessed = ""):
    #开始处理paramsString jsonstring),( path
    paramList = getParamList(strTobeProcessed,context)

    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字JSON_PATH_EXIST执行时解析参数列表返回错误。返回参数列表为%s" % str(paramList)
        context.assertResult = "%s\n%s" % (retMsg,context.assertResult)
        return retMsg

    jsonValue = ""
    jsonString = ""
    jsonPath = ""
    if len(paramList) == 2:
        jsonPath = paramList[1].strip()
        jsonString = paramList[0].strip()
        try:
            jsonDict = transferJsonToDict(jsonString)
            jsonValue = str(eval("jsonDict%s" % jsonPath))
            jsonValue = "True"
        except Exception as e:
            jsonValue = "False"
    else:
        jsonValue = "<ERROR:参数错误>"
        context.setERROR( jsonValue)

    return jsonValue


@keyword()
@catch_exception
def JSON_LIST_LEN(value, context, strTobeProcessed=""):
    # 开始处理paramsString jsonstring),( path
    paramList = getParamList(strTobeProcessed,context)

    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字JSON_LIST_LEN执行时解析参数列表返回错误。返回参数列表为%s" % str(paramList)
        context.assertResult = "%s\n%s" % (retMsg,context.assertResult)
        return retMsg

    jsonValue = ""
    lenRes = "0"
    jsonString = ""
    jsonPath = ""
    if len(paramList) == 1:
        paramList.append("")

    if len(paramList) == 2:
        jsonPath = paramList[1].strip()
        jsonString = paramList[0].strip()
        try:
            jsonDict = transferJsonToDict(jsonString)
            if jsonPath.strip() == "":
                jsonValue = jsonDict
            else:
                jsonValue = eval("jsonDict%s" % jsonPath)
            if TypeTool.is_list(jsonValue):
                lenRes = str(len(jsonValue))
            else:
                lenRes = "<ERROR:不是列表不进行长度判断>"
                context.setERROR( lenRes)

        except Exception as e:
            lenRes = "<ERROR:JSON格式错误>"
            context.setERROR( lenRes)

    else:
        lenRes = "<ERROR:参数长度[%d]错误>" % len(paramList)
        context.setERROR( lenRes)

    return lenRes


@keyword()
@catch_exception
def GET_JSON_KEYS_LIST(value, context, strTobeProcessed=""):
    # GET_JSON_KEYS_LIST(jsonStr) 返回keysList
    paramList = getParamList(strTobeProcessed,context)

    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字GET_JSON_KEYS_LIST执行时解析参数列表返回错误。返回参数列表为%s" % str(paramList)
        context.assertResult = "%s\n%s" % (retMsg,context.assertResult)
        return retMsg

    if len(paramList) == 1:
        jsonString = paramList[0].strip()
        try:
            if isDictJson(jsonString):
                jsonDict = json.loads(jsonString)
            else:
                retKey = "<ERROR:非法的JSON参数>"
                context.setERROR(retKey)
                return retKey

            jsonKeys = list(jsonDict.keys())
            retKey = json.dumps(jsonKeys,ensure_ascii = False)
        except Exception as e:
            logging.error(traceback.format_exc())
            retKey = "<ERROR:未知错误>"
            context.setERROR( retKey)
    else:
        retKey = "<ERROR:参数长度%d错误>" % len(paramList)
        context.setERROR( retKey)

    return retKey


@keyword()
@catch_exception
def GET_JSON_KEY_BY_INDEX(value, context, strTobeProcessed=""):
    # 开始处理GET_JSON_KEY_BY_INDEX(jsonStr,index)
    paramList = getParamList(strTobeProcessed,context)
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字GET_JSON_KEY_BY_INDEX执行时解析参数列表返回错误。返回参数列表为%s" % str(paramList)
        context.assertResult = "%s\n%s" % (retMsg,context.assertResult)
        return retMsg
    retKey = ""
    if len(paramList) == 2:
        jsonString = paramList[0].strip()
        jsonIndex = paramList[1].strip()
        if isInt(jsonIndex) == False:
            retKey = "<ERROR:位置索引必须是大于0的整数>"
            context.setERROR( retKey)
            return retKey
        try:
            jsonIndex = int(jsonIndex)
            if isDictJson(jsonString):
                jsonDict = json.loads(jsonString)
            else:
                retKey = "<ERROR:非法的JSON参数>"
                context.setERROR( retKey)
                return retKey
            jsonKeys = list(jsonDict.keys())
            if len(jsonKeys) >= jsonIndex:
                retKey = jsonKeys[jsonIndex-1]
            else:
                retKey = "<ERROR:位置索引%d超过总长度%d>" % (jsonIndex,len(jsonKeys))
                context.setERROR( retKey)

        except Exception as e:
            logging.error(traceback.format_exc())
            retKey = "<ERROR:未知错误>"
            context.setERROR( retKey)

    else:
        retKey = "<ERROR:参数长度%d错误>" % len(paramList)
        context.setERROR( retKey)

    return retKey


@keyword()
@catch_exception
def GET_JSON_FROM_LIST_BY_KEYVALUE(value, context, strTobeProcessed=""):
    # 开始处理GET_JSON_FROM_LIST_BY_KEYVALUE(listStr,keyPath,keyValue,index)
    paramList = getParamList(strTobeProcessed,context)
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字GET_JSON_FROM_LIST_BY_KEYVALUE执行时解析参数列表返回错误。返回参数列表为%s" % str(paramList)
        context.assertResult = "%s\n%s" % (retMsg,context.assertResult)
        return retMsg
    lenRes = ""
    if len(paramList) != 3 and len(paramList) != 4:
        lenRes = "<ERROR:参数错误>"
        context.setERROR( lenRes)
        return lenRes

    listStr = paramList[0]
    keyPath = paramList[1]
    keyValue = str(paramList[2])
    index = 1
    if len(paramList) == 4 :
        if isInt(paramList[3]):
            index = int(paramList[3])
        else:
            lenRes = "<ERROR:第四个参数索引必须是数字>"
            context.setERROR( lenRes)
            return lenRes

    listObj = []
    if isListJson(listStr):
        listObj = json.loads(listStr)
    else:
        lenRes = "<ERROR:第一个参数必须是LIST>"
        context.setERROR( lenRes)
        return lenRes

    countCurrentIndex = 0
    for i in range(0,len(listObj)):
        tmpDict = listObj[i]
        if TypeTool.is_str(tmpDict) and isDictJson(tmpDict):
            tmpDict = json.loads(tmpDict)

        if TypeTool.is_dict(tmpDict):
            #是dict
            try:
                tmpKeyValue = str(eval("tmpDict%s" % keyPath))
                if tmpKeyValue == keyValue:
                    #找到当前dict
                    countCurrentIndex += 1
                    if countCurrentIndex == index:
                        lenRes = json.dumps(tmpDict,ensure_ascii = False)
                        return lenRes
                    else:
                        continue
                else:
                    #未找到dict
                    continue

            except Exception as e:
                #异常，没有对应的key，继续下一个
                continue
        else:
            #不是dict,继续遍历下一个元素
            continue
    lenRes = "<ERROR:未找到对应的元素>"
    context.setERROR( lenRes)
    return lenRes


@keyword()
@catch_exception
def GET_LIST_KEY_VALUE_TO_STRING_WITH_SPLIT_TAG(value, context, strTobeProcessed=""):
    #GET_LIST_KEY_VALUE_TO_STRING_WITH_SPLIT_TAG(listStr,path,splitTag)
    """
    [
        {
          "id": "1002",
          "datacell": [
            "1002",
            "oHrET0mak8nXtfFuJiC6Ge9AdjVI",
            "蓝翔坦克",
            "",
            "",
            0,
            "wxafc354d761cdcfad"
          ]
        },
        {
          "id": "1003",
          "datacell": [
            "1003",
            "oHrET0sldwXTwQQch4dQYZoyzkag",
            "静",
            "",
            "",
            0,
            "wxafc354d761cdcfad"
          ]
        },
        {
          "id": "1402",
          "datacell": [
            "1402",
            "oHrET0t8a3j5LMhEtL7ZgNpQgamg",
            "史超",
            "史超",
            "15010452531",
            1,
            "wxafc354d761cdcfad"
          ]
        },
        {
          "id": "1101",
          "datacell": [
            "1101",
            "oHrET0qvKFd-5tLUkUBek3JeqLEI",
            "fanger",
            "",
            "",
            0,
            "wxafc354d761cdcfad"
          ]
        }
      ]

    """
    paramList = getParamList(strTobeProcessed,context)
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字GET_LIST_KEY_VALUE_TO_STRING_WITH_SPLIT_TAG执行时解析参数列表返回错误。返回参数列表为%s" % str(paramList)
        context.assertResult = "%s\n%s" % (retMsg,context.assertResult)
        return retMsg
    lenRes = ""
    if len(paramList) != 3 and len(paramList) != 2:
        lenRes = "<ERROR:参数错误>"
        context.setERROR( lenRes)
        return lenRes

    listStr = paramList[0]
    keyPath = paramList[1]
    if len(paramList) == 3:
        splitTag = str(paramList[2])
    elif len(paramList) == 2:
        splitTag = ","

    listObj = []
    if isListJson(listStr):
        listObj = json.loads(listStr)
    else:
        lenRes = "<ERROR:第一个参数必须是LIST>"
        context.setERROR( lenRes)
        return lenRes

    countCurrentIndex = 0
    retListStr = ""
    for i in range(0, len(listObj)):
        tmpDict = listObj[i]
        if TypeTool.is_str(tmpDict) and isDictJson(tmpDict):
            tmpDict = json.loads(tmpDict)

        if TypeTool.is_dict(tmpDict):
            # 是dict
            try:
                tmpKeyValue = str(eval("tmpDict%s" % keyPath))
                if i == 0:
                    tSplitTag = ""
                else:
                    tSplitTag = splitTag
                retListStr = "%s%s%s" % (retListStr,tSplitTag,tmpKeyValue)
            except Exception as e:
                # 异常，没有对应的key，继续下一个
                continue
        else:
            # 不是dict,继续遍历下一个元素
            continue
    return retListStr

################
# String处理函数
################

@keyword()
@catch_exception
def SUB_STR(value,context,strTobeProcessed = ""):
    paramList = getParamList(strTobeProcessed,context)
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字SUB_STR执行时解析参数列表返回错误。返回参数列表为%s" % str(paramList)
        context.assertResult = "%s\n%s" % (retMsg,context.assertResult)
        return retMsg
    if len(paramList) == 3:
        #正确解析
        subedString = paramList[0].strip()
        startTag = paramList[1].strip()
        endTag = paramList[2].strip()
        subValue = get_sub_string(subedString,startTag,endTag)
    else:
        subValue = "<ERROR:参数错误>"
        context.setERROR( subValue)

    return subValue

################
# 正则表达式取值
################

@keyword()
@catch_exception
def RE_FINDALL(value,context,strTobeProcessed = ""):
    #RE_FINDALL(baseString,reMatchStr)
    #返回 JSON LIST
    paramList = getParamList(strTobeProcessed,context)
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字RE_FINDALL执行时解析参数列表返回错误。返回参数列表为%s" % str(paramList)
        context.assertResult = "%s\n%s" % (retMsg,context.assertResult)
        return retMsg
    if len(paramList) == 2:
        #正确解析
        baseString = paramList[0].strip()
        reString = paramList[1].strip()
        try:
            p = re.compile(r'%s' % reString)
        except Exception as e:
            subValue = "<ERROR:正则表达式错误>"
            context.setERROR( subValue)
            return subValue
        subValue = json.dumps(p.findall(baseString),ensure_ascii = False)
    else:
        subValue = "<ERROR:参数错误>"
        context.setERROR( subValue)

    return subValue

################
# BeautifulSOAP 查找
################

@keyword()
@catch_exception
def BS_FIND(value,context,strTobeProcessed = ""):
    #BS_FIND(htmlString,attrJson,textNameOrAll,index)
    #返回 字符串
    try:
        paramList = getParamList(strTobeProcessed,context)
        if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
            retMsg = "CASE_ERROR:关键字BS_FIND执行时解析参数列表返回错误。返回参数列表为%s" % str(paramList)
            context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
            return retMsg
        if len(paramList) >= 2:
            #正确解析
            htmlString = paramList[0].strip()
            attrJson = paramList[1].strip()
            if isDictJson(attrJson) :
                attrDict = json.loads(attrJson)
            else:
                retValue = "<ERROR:attrJson必须是合法的json字符串，有逗号用反斜杠转义。>"
                context.setERROR( retValue)
                return retValue
            attrStr = "text"
            if len(paramList) >=3:
                attrStr = paramList[2].strip()
            index = 0
            if len(paramList) >= 4:
                index = paramList[3].strip()
                if isInt(index):
                    index = int(index)
                    if index < 0:
                        subValue = "<ERROR:INDEX参数必须是大于等于0的数字>"
                        context.setERROR( subValue)

                else:
                    subValue = "<ERROR:INDEX参数必须是数字>"
                    context.setERROR( subValue)

            bsobj = BeautifulSoup(htmlString)
            idValue = bsobj.find_all(attrs=attrDict)[index]
            if attrStr == "all":
                subValue = str(idValue).strip()
            else:
                subValue = eval("idValue."+attrStr).strip()

        else:
            subValue = "<ERROR:参数错误>"
            context.setERROR( subValue)

        return subValue
    except Exception as e:
        subValue = "<ERROR:发生异常,参数1必须是html格式的文本或者其他错误>"
        context.setERROR( subValue)
        return subValue

################
# 随机字符串函数
################

@keyword()
@catch_exception
def RANDOM_INT(value,context,strTobeProcessed=""):
    ranList = getParamList(strTobeProcessed,context)
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字RANDOM_INT执行时解析参数列表返回错误。返回参数列表为%s" % str(ranList)
        context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
        return retMsg

    randNum = ""
    if len(ranList) != 2:
        randNum = "<ERROR:参数个数错误>"
        context.setERROR( randNum)

    else:
        minNum = ranList[0].strip()
        maxNum = ranList[1].strip()
        if isInt(minNum) and isInt(maxNum):
            randNum = str(random.randint(int(minNum), int(maxNum)))
        else:
            randNum = "<ERROR:参数必须是数字>"
            context.setERROR( randNum)

    logging.debug(u"RANDOM_INT()：得到：%s" % randNum)
    return str(randNum)


@keyword()
@catch_exception
def RANDOM_EN(value,context,strTobeProcessed=""):
    # RANDOM_EN() 无前缀随机一个10位的英文字符串
    # RANDOM_EN(name) 随机一个前缀是name，后面10个英文随机字符串
    # RANDOM_EN(name,8) 随机一个前缀是name，后满跟着8个随机英文字母，比如 nameABCDEFGH
    ranList = getParamList(strTobeProcessed,context)
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字RANDOM_EN执行时解析参数列表返回错误。返回参数列表为%s" % str(ranList)
        context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
        return retMsg
    retEn = ""
    if len(ranList) > 2:
        retEn = "<ERROR:参数个数错误>"
        context.setERROR( retEn)

    elif len(ranList) == 1:
        preEn = ranList[0]
        #随机个10为英文字符串
        randomEn = genereateAnEnStr(10)
        retEn = preEn + randomEn
    elif len(ranList) == 2:
        preEn = ranList[0]
        randonLen = isInt(ranList[1]) and int(ranList[1]) or 10
        #随机一个randomLen的英文字符串
        randomEn = genereateAnEnStr(randonLen)
        retEn = preEn + randomEn
    else:
        retEn = "<ERROR:参数个数错误>"
        context.setERROR( retEn)

    logging.debug(u"RANDOM_EN()：得到：%s" % retEn)
    return str(retEn)


@keyword()
@catch_exception
def RANDOM_CN(value,context,strTobeProcessed=""):
    # RANDOM_EN() 无前缀随机一个10位的英文字符串
    # RANDOM_EN(name) 随机一个前缀是name，后面10个英文随机字符串
    # RANDOM_EN(name,8) 随机一个前缀是name，后满跟着8个随机英文字母，比如 nameABCDEFGH
    ranList = getParamList(strTobeProcessed,context)
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字RANDOM_CN执行时解析参数列表返回错误。返回参数列表为%s" % str(ranList)
        context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
        return retMsg

    retEn = ""
    if len(ranList) > 2:
        retEn = "<ERROR:参数个数错误>"
        context.setERROR( retEn)

    elif len(ranList) == 1:
        preEn = ranList[0]
        #随机个10为英文字符串
        randomEn = generateAnCnStr(10)
        retEn = preEn + randomEn
    elif len(ranList) == 2:
        preEn = ranList[0]
        randonLen = isInt(ranList[1]) and int(ranList[1]) or 10
        #随机一个randomLen的英文字符串
        randomEn = generateAnCnStr(randonLen)
        retEn = preEn + randomEn
    else:
        retEn = "<ERROR:参数个数错误>"
        context.setERROR( retEn)


    logging.debug(u"RANDOM_CN()：得到：%s" % retEn)
    return str(retEn)

@keyword()
@catch_exception
def RANDOM_VALUE_IN_LIST(value,context,strTobeProcessed=""):
    strTobeProcessed = core.processor.KP.KP.getProcessedValue(strTobeProcessed, context)
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字RANDOM_VALUE_IN_LIST执行时解析参数列表返回错误。"
        context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
        return retMsg
    if isListJson(strTobeProcessed) == False:
        retMsg = "<ERROR:参数必须是list。>"
        context.setERROR( retMsg)
        return retMsg

    listRandomValue = json.loads(strTobeProcessed)
    if len(listRandomValue) < 1:
        retMsg = "<ERROR:列表不能为空。>"
        context.setERROR( retMsg)
        return retMsg

    randindex = random.randint(0,len(listRandomValue)-1)
    return str(listRandomValue[randindex])

#对字符串进行urlencode编码

@keyword()
@catch_exception
def URL_ENCODE(value,context,strTobeProcessed=""):
    strTobeProcessed = core.processor.KP.KP.process_KEYWORDS(strTobeProcessed, context)
    strTobeProcessed = core.processor.CP.CP.getProcessedValue(strTobeProcessed, context)
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字URL_ENCODE执行时解析参数返回错误。返回参数为%s" % strTobeProcessed
        context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
        return retMsg
    retEn = parse.quote_plus(strTobeProcessed)
    return str(retEn)

# 对字符串进行md5编码

@keyword()
@catch_exception
def MD5(value, context, strTobeProcessed=""):
    #只有一个参数，不需要getParamList
    #ranList = getParamList(strTobeProcessed, context)
    strTobeProcessed = core.processor.KP.KP.process_KEYWORDS(strTobeProcessed, context)
    strTobeProcessed = core.processor.CP.CP.getProcessedValue(strTobeProcessed, context)
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字MD5执行时解析参数列表返回错误。返回参数列表为%s" % strTobeProcessed
        context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
        return retMsg

    # 创建md5对象
    hl = hashlib.md5()
    # Tips
    # 此处必须声明encode
    # 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
    hl.update(strTobeProcessed.encode(encoding='utf-8'))
    retMd5String=hl.hexdigest()

    logging.debug(u"MD5()：得到：%s" % retMd5String)
    return str(retMd5String)

# 对字符串进行md5编码

@keyword()
@catch_exception
def STR_TO_LOWER(value, context, strTobeProcessed=""):
    #只有一个参数，不需要getParamList
    #ranList = getParamList(strTobeProcessed, context)
    strTobeProcessed = core.processor.KP.KP.process_KEYWORDS(strTobeProcessed, context)
    strTobeProcessed = core.processor.CP.CP.getProcessedValue(strTobeProcessed, context)
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字STR_TO_LOWER执行时解析参数列表返回错误。返回参数列表为%s" % strTobeProcessed
        context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
        return retMsg

    # 创建md5对象
    retString = strTobeProcessed.lower()

    logging.debug(u"STR_TO_LOWER：得到：%s" % retString)
    return str(retString)

# 对字符串进行md5编码

@keyword()
@catch_exception
def STR_TO_UPPER(value, context, strTobeProcessed=""):
    #只有一个参数，不需要getParamList
    #ranList = getParamList(strTobeProcessed, context)
    strTobeProcessed = core.processor.KP.KP.process_KEYWORDS(strTobeProcessed, context)
    strTobeProcessed = core.processor.CP.CP.getProcessedValue(strTobeProcessed, context)
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字STR_TO_UPPER执行时解析参数列表返回错误。返回参数列表为%s" % strTobeProcessed
        context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
        return retMsg

    # 创建md5对象
    retString = strTobeProcessed.upper()

    logging.debug(u"STR_TO_UPPER：得到：%s" % retString)
    return str(retString)
