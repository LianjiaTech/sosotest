
class ResultConst(object):
    #断言结果常量
    NO_ASSERT = "NO_ASSERT"
    PASS = "PASS"
    WARNING = "WARNING"
    FAIL = "FAIL"
    ERROR = "ERROR"
    NOTRUN = "NOTRUN"
    EXCEPTION = "EXCEPTION"
    NOTRUNLEVEL = "NOTRUNLEVEL"
    CANCELED = "CANCELED"

class PerformanceConst(object):
    NA = "N/A"
    PASS = "PASS"
    FAIL = "FAIL"

class CaseTypeConst(object):
    #用例类型常量
    GROUP = "GROUP"
    INTERFACE = "INTERFACE"

class CaseLevel(object):
    HIGN = 0
    MIDIUM = 5
    LOW = 9

class TestCaseStepSwitch(object):
    NOT_SWITCH = 0
    USE_SWITCH = 1

class CaseStatus(object):
    UN_AUDIT = 1 #未审核
    AUDIT_PASS = 2 #审核通过
    AUDIT_NOT_PASS = 3 #审核未通过

class MethodConst(object):
    POST = "POST"
    GET = "GET"

class DBConst(object):
    DEFAULT = "default"


class HttpKey(object):
    NO_KEY = "none"

class ServiceKey(object):
    NO_KEY = "none"

class ExecStatus(object):
    NOTRUN = 1
    RUNNING = 2
    DONE = 3
    EXCEPTION = 4
    CANCELING = 10
    CANCELED = 11

class ObjTypeConst(object):
    UNKNOWN = 0
    TASK = 1
    TESTCASE = 2
    TESTCASE_STEP = 3
    INTERFACE = 4

class testLevelConst(object):
    RUNALL = 100



