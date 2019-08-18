import json,types,datetime
class ApiReturn(object):
    CODE_OK = 10000
    CODE_RELOAD = 11000
    CODE_WARNING = 10011
    CODE_ERROR = 10012
    CODE_EXCEPTION = 10013
    #common
    CODE_TIMEOUT = 10001
    #请求method相关的
    CODE_WRONE_REQUEST_METHOD = 11001
    #param错误相关的
    CODE_PARAM_ERROR = 12001
    #token错误相关的
    CODE_TOKEN_NULL = 13000
    CODE_TOKEN_WRONG_PWD = 13001
    CODE_TOKEN_WRONG = 13002
    #tcpSendRestCode
    CODE_TCP_RETURN_NOT_OK = 14001
    CODE_TCP_EXCEPTION = 14002
    #任务执行
    CODE_TASK_EXECUTE_EXCEPTION = 15001
    CODE_TASK_EXECUTE_CANCELLING = 15002
    CODE_TASK_EXECUTE_CANCELED = 15003

    CODE_NOT_FILE_EXCEPITON = 16005
    #接口调试
    CODE_INTERFACE_DEBUG_ADD_EXCEPITON = 16001 #liyc
    CODE_DEBUG_TIMEOUT = 16002 # liyc

    #method错误
    CODE_METHOD_ERROR = 17001 #liyc

    #接口
    CODE_INTERFACE_ERROR = 18001 #liyc

    #用例
    CODE_TESTCASE_ERROR = 19001
    #用例调试
    CODE_TESTCASE_DEBUG_EXCEPITON = 20001
    CODE_TESTCASE_DEBUG_TIMEOUT_EXCEPITON = 20002

    #任务
    CODE_TASK_EXCEPITON = 21001

    #全局变量
    CODE_GLOBAL_EXCEPITON = 22001

    #userHttpConf
    CODE_USER_HTTP_CONF_EXCEPTION = 23001

    CODE_USER_EXCEPTION = 24001

    CODE_NOT_FILE_EXCEPTION = 25001

    #接口覆盖
    CODE_INTERFACE_COVER_EXCEPTION = 26001
    CODE_INTERFACE_COVER_DIRISEXIST = 26002

    CODE_NOT_PERMISSION = 30000

    RQUEST_EXCEPTION_MSG = "发生错误，请联系管理员"

    def __init__(self,code=CODE_OK,message="ok",body={}):
        self.__code = code
        self.__message = message
        self.__body = body

    @property
    def code(self):
        return self.__code

    @code.setter
    def code(self, code):
        self.__code = code

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, message):
        self.__message = message

    @property
    def body(self):
        return self.__body

    @body.setter
    def body(self, body):
        if type(body) == type(b""):
            body = str(body,encoding = "utf-8")
        self.__body = body

    def toJson(self,isUnicode = False):
        retDict = {}
        retDict['code'] = self.code
        retDict['message'] = self.message
        if type(self.body) == type(b""):
            self.body = str(self.body,encoding = "utf-8")
        if type(self.body) != type({}) and type(self.body) != type([]) and type(self.body) != type(""):
            retDict['body'] = "不识别的body类型！body必须是dict，list或者str。"
        else:
            if type(self.body) == type({}):
                for k,v in self.body.items():
                    if type(v) == type(datetime.datetime(1984,1,2)):
                        #如果是datetime类型的，无法转换为json，要先转换为字符串
                        self.body[k] = str(v)

            retDict['body'] = self.body

        return json.dumps(retDict,ensure_ascii=isUnicode)

