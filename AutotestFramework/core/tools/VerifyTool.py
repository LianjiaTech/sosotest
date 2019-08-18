import types
import re

"""
验证所有表单提交的数据
"""

class VerifyTool(object):

    # 判断是否为整数 15
    @staticmethod
    def IsNumber(varObj):
        return type(varObj) is types.IntType


    # 判断是否为字符串 string
    @staticmethod
    def IsString(varObj):
        return type(varObj) is types.StringType


    # 判断是否为浮点数 1.324
    @staticmethod
    def IsFloat(varObj):
        return type(varObj) is types.FloatType


    # 判断是否为字典 {'a1':'1','a2':'2'}
    @staticmethod
    def IsDict(varObj):
        return type(varObj) is types.DictType


    # 判断是否为tuple [1,2,3]
    @staticmethod
    def IsTuple(varObj):
        return type(varObj) is types.TupleType


    # 判断是否为List [1,3,4]
    @staticmethod
    def IsList(varObj):
        return type(varObj) is types.ListType


    # 判断是否为布尔值 True
    @staticmethod
    def IsBoolean(varObj):
        return type(varObj) is types.BooleanType


    # # 判断是否为货币型 1.32
    # @staticmethod
    # def IsCurrency(varObj):
    #     # 数字是否为整数或浮点数
    #     if IsFloat(varObj) and IsNumber(varObj):
    #         # 数字不能为负数
    #         if varObj > 0:
    #             return isNumber(currencyObj)
    #             return False
    #     return True


    # 判断某个变量是否为空 x
    @staticmethod
    def IsEmpty(varObj):
        if len(varObj) == 0:
            return True
        return False


    # 判断变量是否为None None
    @staticmethod
    def IsNone(varObj):
        return type(varObj) is types.NoneType  # == "None" or varObj == "none":


    # 判断是否为日期格式,并且是否符合日历规则 2010-01-31
    @staticmethod
    def IsDate(varObj):
        if len(varObj) == 10:
            rule = '(([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))|((([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00))-02-29)$/'
            match = re.match(rule, varObj)
            if match:
                return True
            return False
        return False


    # 判断是否为邮件地址
    @staticmethod
    def IsEmail(varObj):
        rule = '[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$'
        match = re.match(rule, varObj)

        if match:
            return True
        return False


    # 判断是否为中文字符串
    @staticmethod
    def IsChineseCharString(varObj):
        for x in varObj:
            if (x >= u"\u4e00" and x <= u"\u9fa5") or (x >= u'\u0041' and x <= u'\u005a') or (
                    x >= u'\u0061' and x <= u'\u007a'):
                continue
            else:
                return False
        return True


    # 判断是否为中文字符
    @staticmethod
    def IsChineseChar(varObj):
        if varObj[0] > chr(127):
            return True
        return False


    # 判断帐号是否合法 字母开头，允许4-16字节，允许字母数字下划线
    @staticmethod
    def IsLegalAccounts(varObj):
        rule = '[a-zA-Z][a-zA-Z0-9_]{3,15}$'
        match = re.match(rule, varObj)

        if match:
            return True
        return False


    # 匹配IP地址
    @staticmethod
    def IsIpAddr(varObj):
        rule = '\d+\.\d+\.\d+\.\d+'
        match = re.match(rule, varObj)

        if match:
            return True
        return False

    @staticmethod
    def IsVarMatch(varObj):
        if re.match('^[a-zA-Z][a-zA-Z0-9_-]*$', varObj):
            if varObj.startswith("PaTh-_-"):
                return False
            else:
                return True
        else:
            return False

    @staticmethod
    def IsValidVarValue(valueObj):
        if isinstance(valueObj,str) or isinstance(valueObj,dict) or isinstance(valueObj,list) or isinstance(valueObj,int) or isinstance(valueObj,float):
            return True
        else:
            return False

if __name__ == "__main__":
    tmpkey = "a_-abc"
    if not re.match('^[a-zA-Z][a-zA-Z0-9_-]*$', tmpkey):
        print("not match")
    else:
        print("match")