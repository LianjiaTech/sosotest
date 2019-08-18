from core.const.AssertConst import AssertConst
from core.const.GlobalConst import ResultConst
from core.tools.TypeTool import TypeTool
from core.tools.CommonFunc import *


def setAssertResult(result, msg):
    return [result, "%s: %s" % (result, msg)]

class MyAssertError(AssertionError):
    def __init__(self,testResult,retMsg):
        super(MyAssertError, self).__init__()
        self.testResult = testResult
        self.retMsg = retMsg
        
class Assert(object):
    """
    断言类

    Attributes:
        无
    """

    @staticmethod
    def assertExpectText(value,return_msg):
        """
        要断言的值和实际返回结果
        Args:
            value: 要断言的内容
            return_msg: 实际返回的内容

        Returns: 数组，第一个元素是断言结果PASS/FAIL等，第二个元素是断言内容。

        """
        orList = value.split(AssertConst.TAG_OR)
        retList = [ResultConst.NOTRUN,""]

        if len(orList) == 1:
            return Assert.assertExpectSingleTextV2(orList[0],return_msg)

        for tmpText in orList:
            tmpRetList = Assert.assertExpectSingleTextV2(tmpText,return_msg)
            if tmpRetList[0] == ResultConst.PASS:
                retList[0] = ResultConst.PASS
                retList[1] = retList[1] + tmpRetList[1] + "条件满足，{OR}断言结束。"
                retList[1] = "PASS：{OR}断言通过。\n" + retList[1]
                return retList
            else:
                retList[0] = tmpRetList[0]
                retList[1] = retList[1] + tmpRetList[1]

        retList[1] = retList[0] + "：{OR}断言失败，所有条件均不满足。\n" + retList[1]
        return retList

    @staticmethod
    def assertExpectSingleText(value,return_msg):
        """
        要断言的值和实际返回结果
        Args:
            value: 要断言的内容
            return_msg: 实际返回的内容

        Returns: 数组，第一个元素是断言结果PASS/FAIL等，第二个元素是断言内容。

        """

        # 首先要判断预期结果是否是JSON，还是字符串，如果是字符串，就测试返回结果是否保存字符串内容，异常返回是带字符串的
        likeList = value.split(AssertConst.TAG_LIKE) # [LIKE]  #现阶段不开放，后期做成正则匹配的形式。
        inList = value.split(AssertConst.TAG_IN)  # [LIKE]
        notInList = value.split(AssertConst.TAG_NOT_IN)  # [LIKE]
        equalList = value.split(AssertConst.TAG_EQUAL) #[==]
        gtList = value.split(AssertConst.TAG_GT) # [>]
        ltList = value.split(AssertConst.TAG_LT) # [<]
        getList = value.split(AssertConst.TAG_GT_EQUAL) #[>=]
        letList = value.split(AssertConst.TAG_LT_EQUAL) #[<=]
        neList = value.split(AssertConst.TAG_NOT_EQUAL) # [!=]

        ret_list = [ResultConst.NOTRUN, ""]

        if len(inList) == 2:
            #进行 [IN] 断言 a in b 表示 a是字符串b的子串
            db_values = str(inList[0]).strip()
            expectValue = str(inList[1]).strip()
            if db_values in expectValue:
                ret_list[1] += "%s: 断言通过，预期值[ %s ]包含于实际值[ %s ]。\n" % (ResultConst.PASS, db_values, expectValue)
                ret_list[1] = "PASS：断言成功！\n%s" % ret_list[1]
                ret_list[0] = ResultConst.PASS
                return ret_list
            else:
                ret_list[1] += "FAIL: 断言失败，预期值[ %s ]不包含于实际值[ %s ]。\n" % (db_values, expectValue)
                ret_list[1] = "FAIL：断言失败！\n%s" % ret_list[1]
                ret_list[0] = ResultConst.FAIL
                return ret_list
        elif len(notInList) == 2:
            # 进行 [IN] 断言 a in b 表示 a是字符串b的子串
            db_values = str(notInList[0]).strip()
            expectValue = str(notInList[1]).strip()
            if db_values not in expectValue:
                ret_list[1] += "%s: 断言通过，预期值[ %s ]不包含于实际值[ %s ]。\n" % (ResultConst.PASS, db_values, expectValue)
                ret_list[1] = "PASS：断言成功！\n%s" % ret_list[1]
                ret_list[0] = ResultConst.PASS
                return ret_list
            else:
                ret_list[1] += "FAIL: 断言失败，预期值[ %s ]包含于实际值[ %s ]。\n" % (db_values, expectValue)
                ret_list[1] = "FAIL：断言失败！\n%s" % ret_list[1]
                ret_list[0] = ResultConst.FAIL
                return ret_list

        elif len(likeList) == 2:
            #进行like断言
            db_values = likeList[0].split(",")
            len_db_values = len(db_values)
            e_list = likeList[1].split(",")
            if len(e_list) != len_db_values:
                ret_list[1] = "ERROR: " + ret_list[1] + "断言失败，左右侧长度不一致，无法断言。\n"
                ret_list[0] = ResultConst.ERROR
                return ret_list
            for i in range(0, len_db_values):
                if str(db_values[i]).strip() not in str(e_list[i]):
                    ret_list[1] += "FAIL: 第%d个元素断言失败，预期值[ %s ]不包含于实际值[ %s ]。\n" % ((i+1),str(db_values[i]).strip(),str(e_list[i]).strip())
                    ret_list[1] = "FAIL：断言失败！\n%s" % ret_list[1]
                    ret_list[0] = ResultConst.FAIL
                    return ret_list
                else:
                    ret_list[1] += "%s: 第%d个元素断言通过，预期值[ %s ]包含于实际值[ %s ]。\n" % ( ResultConst.PASS,(i + 1), str(db_values[i]).strip(), str(e_list[i]).strip())

            ret_list[1] = "PASS：断言成功！\n%s" % ret_list[1]
            ret_list[0] = ResultConst.PASS
            return ret_list
        elif len(equalList) == 2:
            #进行==断言
            db_values = equalList[0].split(",")
            len_db_values = len(db_values)
            e_list = equalList[1].split(",")
            if len(e_list) != len_db_values:
                ret_list[1] = "ERROR: " + ret_list[1] + "断言失败，左右侧长度不一致，无法断言。\n"
                ret_list[0] = ResultConst.ERROR
                return ret_list
            for i in range(0, len_db_values):
                if str(db_values[i]).strip() != str(e_list[i]).strip():
                    ret_list[1] += "FAIL: 第%d个元素断言失败,预期[%s == %s]，实际不成立。\n" % ((i+1),str(db_values[i]).strip(),str(e_list[i]).strip())
                    ret_list[1] = "FAIL：断言失败！\n%s" % ret_list[1]
                    ret_list[0] = ResultConst.FAIL
                    return ret_list
                else:
                    ret_list[1] += "%s: 第%d个元素断言通过,预期[%s == %s]，实际成立。\n" % (ResultConst.PASS,(i + 1), str(db_values[i]).strip(), str(e_list[i]).strip())

            ret_list[1] = "PASS：断言成功！\n%s" % ret_list[1]
            ret_list[0] = ResultConst.PASS
            return ret_list
        elif len(neList) == 2:
            # 进行==断言
            db_values = neList[0].split(",")
            len_db_values = len(db_values)
            e_list = neList[1].split(",")
            if len(e_list) != len_db_values:
                ret_list[1] = "ERROR: " + ret_list[1] + "断言失败，左右侧长度不一致，无法断言。\n"
                ret_list[0] = ResultConst.ERROR
                return ret_list
            for i in range(0, len_db_values):
                if str(db_values[i]).strip() == str(e_list[i]).strip():
                    ret_list[1] += "FAIL: 第%d个元素断言失败,预期[%s != %s]，实际不成立。\n" % (
                    (i + 1), str(db_values[i]).strip(), str(e_list[i]).strip())
                    ret_list[1] = "FAIL：断言失败！\n%s" % ret_list[1]
                    ret_list[0] = ResultConst.FAIL
                    return ret_list
                else:
                    ret_list[1] += "%s: 第%d个元素断言通过,预期[%s != %s]，实际成立。\n" % (
                    ResultConst.PASS, (i + 1), str(db_values[i]).strip(), str(e_list[i]).strip())

            ret_list[1] = "PASS：断言成功！\n%s" % ret_list[1]
            ret_list[0] = ResultConst.PASS
            return ret_list
        elif len(gtList) == 2:
            #进行>断言
            db_values = gtList[0].split(",")
            len_db_values = len(db_values)
            e_list = gtList[1].split(",")
            if len(e_list) != len_db_values:
                ret_list[1] = "ERROR: " + ret_list[1] + "断言失败，左右侧长度不一致，无法断言。\n"
                ret_list[0] = ResultConst.ERROR
                return ret_list
            for i in range(0, len_db_values):
                if isInt(db_values[i]) == False or isInt(e_list[i]) == False:
                    ret_list[1] += "ERROR: 第%d个元素断言错误，预期和实际结果应该是数字,预期[%s]，实际[%s]。\n" % ((i + 1), str(db_values[i]).strip(), str(e_list[i]).strip())
                    ret_list[0] = ResultConst.ERROR
                    return ret_list
                if int(db_values[i]) <= int(e_list[i]):
                    ret_list[1] += "FAIL: 第%d个元素断言失败,预期[%s > %s]，实际不成立。\n" % ((i+1),str(db_values[i]).strip(),str(e_list[i]).strip())
                    ret_list[1] = "FAIL：断言失败！\n%s" % ret_list[1]
                    ret_list[0] = ResultConst.FAIL
                    return ret_list
                else:
                    ret_list[1] += "%s: 第%d个元素断言通过,预期[%s > %s]，实际成立。\n" % (ResultConst.PASS,(i + 1), str(db_values[i]).strip(), str(e_list[i]).strip())

            ret_list[1] = "PASS：断言成功！\n%s" % ret_list[1]
            ret_list[0] = ResultConst.PASS
            return ret_list
        elif len(ltList) == 2:
            #进行<小于断言
            db_values = ltList[0].split(",")
            len_db_values = len(db_values)
            e_list = ltList[1].split(",")
            if len(e_list) != len_db_values:
                ret_list[1] = "ERROR: " + ret_list[1] + "断言失败，左右侧长度不一致，无法断言。\n"
                ret_list[0] = ResultConst.ERROR
                return ret_list
            for i in range(0, len_db_values):
                if isInt(db_values[i]) == False or isInt(e_list[i]) == False:
                    ret_list[1] += "ERROR: 第%d个元素断言错误，预期和实际结果应该是数字,预期[%s]，实际[%s]。\n" % ((i + 1), str(db_values[i]).strip(), str(e_list[i]).strip())
                    ret_list[0] = ResultConst.ERROR
                    return ret_list
                if int(db_values[i]) >= int(e_list[i]):
                    ret_list[1] += "FAIL: 第%d个元素断言失败,预期[%s < %s]，实际不成立。\n" % ((i+1),str(db_values[i]).strip(),str(e_list[i]).strip())
                    ret_list[1] = "FAIL：断言失败！\n%s" % ret_list[1]
                    ret_list[0] = ResultConst.FAIL
                    return ret_list
                else:
                    ret_list[1] += "%s: 第%d个元素断言通过,预期[%s < %s]，实际成立。\n" % (ResultConst.PASS,(i + 1), str(db_values[i]).strip(), str(e_list[i]).strip())

            ret_list[1] = "PASS：断言成功！\n%s" % ret_list[1]
            ret_list[0] = ResultConst.PASS
            return ret_list
        elif len(getList) == 2:
            #进行==断言
            db_values = getList[0].split(",")
            len_db_values = len(db_values)
            e_list = getList[1].split(",")
            if len(e_list) != len_db_values:
                ret_list[1] = "ERROR: " + ret_list[1] + "断言失败，左右侧长度不一致，无法断言。\n"
                ret_list[0] = ResultConst.ERROR
                return ret_list
            for i in range(0, len_db_values):
                if isInt(db_values[i]) == False or isInt(e_list[i]) == False:
                    ret_list[1] += "ERROR: 第%d个元素断言错误，预期和实际结果应该是数字,预期[%s]，实际[%s]。\n" % ((i + 1), str(db_values[i]).strip(), str(e_list[i]).strip())
                    ret_list[0] = ResultConst.ERROR
                    return ret_list
                if int(db_values[i]) < int(e_list[i]):
                    ret_list[1] += "FAIL: 第%d个元素断言失败,预期[%s >= %s]，实际不成立。\n" % ((i+1),str(db_values[i]).strip(),str(e_list[i]).strip())
                    ret_list[1] = "FAIL：断言失败！\n%s" % ret_list[1]
                    ret_list[0] = ResultConst.FAIL
                    return ret_list
                else:
                    ret_list[1] += "%s: 第%d个元素断言通过,预期[%s >= %s]，实际成立。\n" % (ResultConst.PASS,(i + 1), str(db_values[i]).strip(), str(e_list[i]).strip())

            ret_list[1] = "PASS：断言成功！\n%s" % ret_list[1]
            ret_list[0] = ResultConst.PASS
            return ret_list
        elif len(letList) == 2:
            #进行==断言
            db_values = letList[0].split(",")
            len_db_values = len(db_values)
            e_list = letList[1].split(",")
            if len(e_list) != len_db_values:
                ret_list[1] = "ERROR: " + ret_list[1] + "断言失败，左右侧长度不一致，无法断言。\n"
                ret_list[0] = ResultConst.ERROR
                return ret_list
            for i in range(0, len_db_values):
                if isInt(db_values[i]) == False or isInt(e_list[i]) == False:
                    ret_list[1] += "ERROR: 第%d个元素断言错误，预期和实际结果应该是数字,预期[%s]，实际[%s]。\n" % ((i + 1), str(db_values[i]).strip(), str(e_list[i]).strip())
                    ret_list[0] = ResultConst.ERROR
                    return ret_list
                if int(db_values[i]) > int(e_list[i]):
                    ret_list[1] += "FAIL: 第%d个元素断言失败,预期[%s <= %s]，实际不成立。\n" % ((i+1),str(db_values[i]).strip(),str(e_list[i]).strip())
                    ret_list[1] = "FAIL：断言失败！\n%s" % ret_list[1]
                    ret_list[0] = ResultConst.FAIL
                    return ret_list
                else:
                    ret_list[1] += "%s: 第%d个元素断言通过,预期[%s <= %s]，实际成立。\n" % (ResultConst.PASS,(i + 1), str(db_values[i]).strip(), str(e_list[i]).strip())

            ret_list[1] = "PASS：断言成功！\n%s" % ret_list[1]
            ret_list[0] = ResultConst.PASS
            return ret_list
        else:
            #进行正常Assert断言
            return Assert.assertText(value,return_msg)

    @staticmethod
    def assertExpectSingleTextV2(value,return_msg):
        """
        要断言的值和实际返回结果
        Args:
            value: 要断言的内容
            return_msg: 实际返回的内容

        Returns: 数组，第一个元素是断言结果PASS/FAIL等，第二个元素是断言内容。

        """
        ret_list = [ResultConst.NOTRUN, ""]

        assertInfoDict = {}
        ###判断 left in right
        assertInfoDict["IN"] = {}
        assertInfoDict["IN"]["assertConditionString"] = "leftValue in rightValue"
        assertInfoDict["IN"]["passOutputTemplate"] = """ "%s\\nPASS: 断言通过，%s IN %s\\n" % ( value,leftValue, rightValue) """
        assertInfoDict["IN"]["failOutputTemplate"] = """ "%s\\nFAIL: 断言失败，%s 不包含于 %s\\n" % (value,leftValue, rightValue) """
        ###判断 left not in right
        assertInfoDict["NOT_IN"] = {}
        assertInfoDict["NOT_IN"]["assertConditionString"] = "leftValue not in rightValue"
        assertInfoDict["NOT_IN"]["passOutputTemplate"] = """ "%s\\nPASS: 断言通过，%s NOT IN %s\\n" % (value,leftValue, rightValue) """
        assertInfoDict["NOT_IN"]["failOutputTemplate"] = """ "%s\\nFAIL: 断言失败，%s 包含于 %s\\n" % (value,leftValue, rightValue) """
        ###判断 字符串或者数字 的等于
        assertInfoDict["=="] = {}
        assertInfoDict["=="]["assertConditionString"] = "leftValue == rightValue"
        assertInfoDict["=="]["passOutputTemplate"] = """ "%s\\nPASS: 断言通过，%s == %s\\n" % (value,leftValue, rightValue) """
        assertInfoDict["=="]["failOutputTemplate"] = """ "%s\\nFAIL: 断言失败，%s 不等于 %s\\n" % (value,leftValue, rightValue) """
        ###判断 字符串或者数字 不等于
        assertInfoDict["!="] = {}
        assertInfoDict["!="]["assertConditionString"] = "leftValue != rightValue"
        assertInfoDict["!="]["passOutputTemplate"] = """ "%s\\nPASS: 断言通过，%s != %s\\n" % (value,leftValue, rightValue) """
        assertInfoDict["!="]["failOutputTemplate"] = """ "%s\\nFAIL: 断言失败，%s 等于 %s\\n" % (value,leftValue, rightValue) """
        ###判断 数字的大于 >
        assertInfoDict[">"] = {}
        assertInfoDict[">"]["assertConditionString"] = "float(leftValue) > float(rightValue)"
        assertInfoDict[">"]["passOutputTemplate"] = """ "%s\\nPASS: 断言通过，%s > %s\\n" % (value,leftValue, rightValue) """
        assertInfoDict[">"]["failOutputTemplate"] = """ "%s\\nFAIL: 断言失败，%s 不大于 %s\\n" % (value,leftValue, rightValue) """
        ###判断 数字的小于 <
        assertInfoDict["<"] = {}
        assertInfoDict["<"]["assertConditionString"] = "float(leftValue) < float(rightValue)"
        assertInfoDict["<"]["passOutputTemplate"] = """ "%s\\nPASS: 断言通过，%s < %s\\n" % (value,leftValue, rightValue) """
        assertInfoDict["<"]["failOutputTemplate"] = """ "%s\\nFAIL: 断言失败，%s 不小于 %s\\n" % (value,leftValue, rightValue) """
        ###判断 数字的大于等于 >=
        assertInfoDict[">="] = {}
        assertInfoDict[">="]["assertConditionString"] = "float(leftValue) >= float(rightValue)"
        assertInfoDict[">="]["passOutputTemplate"] = """ "%s\\nPASS: 断言通过，%s >= %s\\n" % (value,leftValue, rightValue) """
        assertInfoDict[">="]["failOutputTemplate"] = """ "%s\\nFAIL: 断言失败，%s 小于 %s\\n" % (value,leftValue, rightValue) """
        ###判断 数字的小于等于 <=
        assertInfoDict["<="] = {}
        assertInfoDict["<="]["assertConditionString"] = "float(leftValue) <= float(rightValue)"
        assertInfoDict["<="]["passOutputTemplate"] = """ "%s\\nPASS: 断言通过，%s <= %s\\n" % (value,leftValue, rightValue) """
        assertInfoDict["<="]["failOutputTemplate"] = """ "%s\\nFAIL: 断言失败，%s 大于 %s\\n" % (value,leftValue, rightValue) """
        ###判断 re.match
        assertInfoDict["RE_MATCH"] = {}
        assertInfoDict["RE_MATCH"]["assertConditionString"] = "re.match(re.compile(r'%s' % rightValue),leftValue )"
        assertInfoDict["RE_MATCH"]["passOutputTemplate"] = """ "%s\\nPASS: 断言通过，%s 正则匹配 %s\\n" % (value,leftValue, rightValue) """
        assertInfoDict["RE_MATCH"]["failOutputTemplate"] = """ "%s\\nFAIL: 断言失败，%s 正则不匹配 %s\\n" % (value,leftValue, rightValue) """
        ###判断 re.match
        assertInfoDict["RE_SEARCH"] = {}
        assertInfoDict["RE_SEARCH"]["assertConditionString"] = "re.search(re.compile(r'%s' % rightValue),leftValue )"
        assertInfoDict["RE_SEARCH"]["passOutputTemplate"] = """ "%s\\nPASS: 断言通过，%s 正则匹配 %s\\n" % (value,leftValue, rightValue) """
        assertInfoDict["RE_SEARCH"]["failOutputTemplate"] = """ "%s\\nFAIL: 断言失败，%s 正则不匹配 %s\\n" % (value,leftValue, rightValue) """

        for tmpTag,tmpTagDict in assertInfoDict.items():
            assertList = value.split("[%s]" % tmpTag)  # [LIKE]
            if len(assertList) == 2:
                #发现对应的断言请求，进行断言
                leftValue = str(assertList[0]).strip()
                rightValue = str(assertList[1]).strip()
                try:
                    # print(tmpTagDict['assertConditionString'])
                    if eval(tmpTagDict['assertConditionString']):
                        ret_list[1] = "开始断言： " + eval(tmpTagDict['passOutputTemplate'])
                        ret_list[0] = ResultConst.PASS
                        return ret_list
                    else:
                        ret_list[1] = "开始断言： " + eval(tmpTagDict['failOutputTemplate'])
                        ret_list[0] = ResultConst.FAIL
                        return ret_list
                except:
                    ret_list[1] = "开始断言： " + traceback.format_exc()
                    ret_list[0] = ResultConst.ERROR
                    return ret_list
        return Assert.assertText(value,return_msg)

    @staticmethod
    def assertText(expect, return_msg):
        """
        完成json或者string预期结果，跟实际结果的断言。

        Args:
            one: 预期结果
            two: 实际结果

        Return:返回一个数组，第一个元素是测试结果 PASS/FAIL/ERROR等，第二个元素是返回的断言内容。

        Raises: 无
        """
        # 首先要判断预期结果是否是JSON，还是字符串，如果是字符串，就测试返回结果是否保存字符串内容，异常返回是带字符串的


        expect = str(expect).strip()
        return_msg = str(return_msg).strip()
        logging.debug("预期结果：%s" % expect)
        logging.debug("实际结果：%s" % return_msg)
        #定义一个变量，用来存储多个断言值不对的情况
        if expect == "":
            return setAssertResult(ResultConst.ERROR,"预期结果为空，请检查预期结果。")

        try:
            ################################################################################################################
            #STEP1： 当预期结果或者实际结果有一个不是json的时候进行字符串断言
            ######判断returnmsg是否是断言过切结果ERROR的#####################
            # error_return_msg = return_msg.split(":")  #如果实际结果return_msg前面有 ERROR，证明用例错误，无需继续断言
            # if  ResultConst.ERROR in error_return_msg[0] :
            #     return [return_msg,ResultConst.ERROR]

            ###########判断不不是ERROR，断言继续########################
            #expect不是null，如果是null会json load成功
            if isDictJson(expect) and isDictJson(return_msg):
                expectResultDict = json.loads(expect)
                actualResultDict = json.loads(return_msg)
                logging.debug("预期结果和实际结果loads成功。")
            else:
                logging.debug("预期结果不是json，进行字符包含断言。")
                if expect in return_msg:
                    return setAssertResult(ResultConst.PASS, "预期结果断言成功。\n预期结果[ %s ]包含于\n实际结果:%s\n" % (expect,return_msg))
                else:
                    return setAssertResult(ResultConst.FAIL, "预期结果断言失败！\n预期结果[ %s ]不包含于\n实际结果:%s\n" % (expect, return_msg))

        except Exception as e:
            #不可知异常，进行包含断言。
            logging.error("未知异常:%s" % (traceback.format_exc()))
            if expect in return_msg:
                return setAssertResult(ResultConst.PASS, "预期结果断言成功。\n预期结果[ %s ]包含于\n实际结果:%s\n" % (expect, return_msg))
            else:
                return setAssertResult(ResultConst.FAIL, "预期结果断言失败！\n预期结果[ %s ]不包含于\n实际结果:%s\n" % (expect, return_msg))

        ################################################################################################################
        # STEP2： 都是json，进行json递归断言
        #变量当前数组中的所有键值 判断是否相等
        #预期结果、实际结果都是json。下面开始key value的断言。
        # 遍历字典，比对结果
        failPointCount = [0]
        fail = ['']  # 失败字符串拼接
        global_key = ['']

        def asssert_value(expectValue, actualValue):
            if type(expectValue) == type(actualValue):
                if expectValue == actualValue:
                    fail[0] = fail[0] + "PASS: 断言通过！预期结果Key(%s)的值与实际结果一致。\r\n" % (global_key[0])
                else:
                    failPointCount[0] += 1
                    fail[0] = fail[0] + "FAIL: 断言失败！预期结果Key(%s)的值与实际不一致，预期%s，实际%s。\r\n" % (global_key[0], expectValue,actualValue)
            else:
                failPointCount[0] += 1
                fail[0] = fail[0] + "FAIL: 断言失败！预期结果Key(%s)的类型与实际结构不一致，预期%s，实际%s。\r\n" % (
                global_key[0], get_sub_string(str(type(expectValue)), "'", "'"),
                get_sub_string(str(type(actualValue)), "'", "'"))

        def pathAdd(keyStr):
            global_key[0] = "%s[%s]" % (global_key[0], keyStr)

        def pathRemove():
            allKeyList = global_key[0].split("[")
            global_key[0] = ''
            for allKeyIndex in range(1, len(allKeyList) - 1):
                global_key[0] = "%s[%s" % (global_key[0], allKeyList[allKeyIndex])

        def recur_data(expect, actual):
            if TypeTool.is_list(expect):
                # 如果预期和实际的任何一个为空，则断言通过，
                # 如果都不为空，判定第一个值
                if TypeTool.is_list(actual):
                    # 如果实际结果也是list，进行逐个断言
                    if len(expect) > len(actual):
                        # 长度超过了实际长度，断言石板
                        failPointCount[0] += 1
                        fail[0] = fail[0] + "FAIL: 断言失败！预期结果Key(%s)的长度%d超过了实际长度%d。\r\n" % (global_key[0], len(expect), len(actual))
                    else:
                        #长度符合实际长度，进行预期结果的断言
                        for tmpListIndex in range(0,len(expect)):
                            pathAdd(tmpListIndex)
                            if TypeTool.is_list(expect[tmpListIndex]) or TypeTool.is_dict(expect[tmpListIndex]):
                                recur_data(expect[tmpListIndex],actual[tmpListIndex])
                            else:
                                #进行实际断言
                                asssert_value(expect[tmpListIndex],actual[tmpListIndex])
                            pathRemove()
                else:
                    #如果实际结果不是list，那么就失败了
                    failPointCount[0] += 1
                    fail[0] = fail[0] + "FAIL: 断言失败！预期结果Key(%s)的值与实际结果类型不一致，预期list，实际%s。\r\n" % (global_key[0], type(actual))

            elif TypeTool.is_dict(expect):
                # 如果预期的是dict，先判断长度一致，再进行递归断言
                if TypeTool.is_dict(actual):
                    # 实际结果也是dict
                    # 进行判断每个key的类型
                    for innerKey, innerValue in expect.items():
                        if innerKey in actual.keys():
                            #实际结果有这个值
                            pathAdd(innerKey)
                            if TypeTool.is_list(innerValue) or TypeTool.is_dict(innerValue):
                                # 如果值是list或者dict，递归判断
                                recur_data(expect[innerKey], actual[innerKey])
                            else:
                                # 否则判断类型
                                asssert_value(expect[innerKey], actual[innerKey])
                            pathRemove()
                        else:
                            #实际结果不存在这个值
                            failPointCount[0] += 1
                            fail[0] = fail[0] + "FAIL: 断言失败！预期结果Key(%s)在实际结果中不存在。\r\n" % (global_key[0])
                else:
                    # 实际结果不是dict
                    failPointCount[0] += 1
                    fail[0] = fail[0] + "FAIL: 断言失败！预期结果Key(%s)的值与实际结果类型不一致，预期dict，实际%s。\r\n" % (global_key[0], type(actual))
            else:
                # 不是list不是字典，进行类型判断
                asssert_value(expect, actual)
                pathRemove()

        recur_data(expectResultDict, actualResultDict)

        if failPointCount[0] == 0:
            logging.debug("PASS: 预期返回结果断言成功！")
            return setAssertResult(ResultConst.PASS, "返回内容全部断言通过。\n%s" % fail[0])
        else:
            logging.debug("FAIL: 测试失败，断言失败点有%d个，请查看详情。" % failPointCount[0])
            return setAssertResult(ResultConst.FAIL, "返回内容最终断言失败。\n%s" % fail[0])

    @staticmethod
    def assertStruct(expectStruct,actualStruct):
        expectResultDict = json.loads(expectStruct)
        actualResultDict = json.loads(actualStruct)
        failPointCount = [0]
        fail = ['']  # 失败字符串拼接
        global_key = ['']

        def asssert_type(expectValue,actualValue):
            if expectValue == None or actualValue == None:
                fail[0] = fail[0] + "PASS: 断言通过！预期结构Key(%s)的类型与实际结构有一方为None。\r\n" % (global_key[0])
                return
            if type(expectValue) == type(actualValue):
                fail[0] = fail[0] + "PASS: 断言通过！预期结构Key(%s)的类型与实际结构一致为%s。\r\n" % (global_key[0], get_sub_string(str(type(expectValue)),"'","'"))
            else:
                failPointCount[0] += 1
                fail[0] = fail[0] + "FAIL: 断言失败！预期结构Key(%s)的类型与实际结构不一致，预期%s，实际%s。\r\n" % (global_key[0], get_sub_string(str(type(expectValue)),"'","'"), get_sub_string(str(type(actualValue)),"'","'"))

        def pathAdd(keyStr):
            global_key[0] = "%s[%s]" % (global_key[0],keyStr)

        def pathRemove():
            allKeyList = global_key[0].split("[")
            global_key[0] = ''
            for allKeyIndex in range(1,len(allKeyList)-1):
                global_key[0] = "%s[%s" % (global_key[0],allKeyList[allKeyIndex])

        def recur_data(expect,actual):
            if TypeTool.is_list(expect):
                # 如果预期和实际的任何一个为空，则断言通过，
                # 如果都不为空，判定第一个值
                if TypeTool.is_list(actual):
                    if len(expect) == 0 or len(actual) == 0:
                        #如果任何一个长度为0，则不断言，直接通过。
                        fail[0] = fail[0] + "PASS: 断言通过！预期结构Key(%s)或者实际结构的Key长度为0，不进行比对。\r\n" % (global_key[0])
                    else:
                        #否则，把第一个结构进行断言
                        if TypeTool.is_list(expect[0]) or TypeTool.is_dict(expect[0]):
                            # 如果值是list或者dict，递归判断
                            pathAdd(0)
                            recur_data(expect[0], actual[0])
                            pathRemove()
                        else:
                            # 否则判断类型
                            pathAdd(0)
                            asssert_type(expect[0], actual[0])
                            pathRemove()
                else:
                    failPointCount[0] += 1
                    fail[0] = fail[0] + "FAIL: 断言失败！预期结构Key(%s)的值与实际结构类型不一致，预期list，实际%s。\r\n" % (
                    global_key[0], type(actual))

            elif TypeTool.is_dict(expect):
                #如果预期的是dict，先判断长度一致，再进行递归断言
                if TypeTool.is_dict(actual):
                    #实际结果也是dict
                    if len(expect) == len(actual):
                        # 进行判断每个key的类型
                        for innerKey, innerValue in expect.items():
                            if innerKey in actual.keys():
                                if TypeTool.is_list(innerValue) or TypeTool.is_dict(innerValue):
                                    #如果值是list或者dict，递归判断
                                    pathAdd(innerKey)
                                    recur_data(expect[innerKey],actual[innerKey])
                                    pathRemove()
                                else:
                                    #否则判断类型
                                    pathAdd(innerKey)
                                    asssert_type(expect[innerKey], actual[innerKey])
                                    pathRemove()

                    else:
                        # 结构一致，长度不一致
                        failPointCount[0] += 1
                        fail[0] = fail[0] + "FAIL: 断言失败！预期结构Key(%s)的值与实际结构的长度不一致，预期长度%s，实际长度%s。\r\n" % (
                        global_key[0], len(expect), len(actual))
                else:
                    #实际结果不是dict
                    failPointCount[0] += 1
                    fail[0] = fail[0] + "FAIL: 断言失败！预期结构Key(%s)的值与实际结构类型不一致，预期dict，实际%s。\r\n" % (global_key[0],  type(actual))
            else:
                #不是list不是字典，进行类型判断
                asssert_type(expect,actual)
                pathRemove()

        recur_data(expectResultDict,actualResultDict)

        if failPointCount[0] == 0:
            logging.debug( "PASS: 预期返回结果断言成功！")
            return setAssertResult(ResultConst.PASS,"返回内容全部断言通过。\n%s" % fail[0])
        else:
            logging.debug("FAIL: 测试失败，断言失败点有%d个，请查看详情。" % failPointCount[0])
            return setAssertResult(ResultConst.FAIL,"返回内容最终断言失败。\n%s" % fail[0])



if __name__ == "__main__":
    expect = {"id":1,"data":[{"name":["llj"],"name2":"wang","name3":{"id":1}}],"msg":"ok"}
    acutal = {"id":2,"data":[{"name":[123,"llllj"],"name2":"wang","name3":{"id":1,"name":"innert"}}],"msg":"ok"}
    retList = Assert.assertStruct(json.dumps(expect),json.dumps(acutal))
    print(retList)