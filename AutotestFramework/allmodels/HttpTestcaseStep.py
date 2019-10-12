from core.model.HttpBase import HttpBase
from core.decorator.normal_functions import *
from core.tools.CommonFunc import *
from core.tools.DBTool import DBTool

from core.const.GlobalConst import CaseLevel
from core.const.GlobalConst import PerformanceConst
from core.const.GlobalConst import CaseStatus
from core.const.GlobalConst import ObjTypeConst

class HttpTestcaseStep(HttpBase):
    """
    用例步骤类
    """
    def __init__(self):
        super(HttpTestcaseStep, self).__init__()
        self.objType = ObjTypeConst.TESTCASE_STEP

        self.id = 0
        self.caseId = ""
        self.caseStepDebugId = 0
        self.caseStepDebugData = {}
        self.stepNum = 1
        self.interfaceId = "%s-%s" % (self.caseId,self.stepNum)

        #基本信息
        self.title = ""
        self.desc = ""
        self.businessLine = ""
        self.modules = ""
        self.level = CaseLevel.MIDIUM  #优先级
        self.status = CaseStatus.UN_AUDIT #用例状态 未审核 审核通过 审核未通过  任务添加只能添加审核通过的用例

        self.testcaseStepPerformanceResult = PerformanceConst.NA

    @take_time
    def executeStep(self):
        """
        执行步骤
        Returns:
            无
        """
        logging.debug("****************************************步骤[%d]开始执行****************************************" % (self.stepNum))
        super(HttpTestcaseStep,self).execute()
        logging.debug( "****************************************步骤[%d]结束执行****************************************" % (self.stepNum))

    @catch_exception
    def generateByCaseStepDebugId(self):
        """
        根据步骤debug表的id获取步骤
        Returns:
            无
        """
        sqlCaseStepDebug = "select * from tb_http_testcase_step_debug where id=%d" %  int(self.caseStepDebugId)
        self.globalDB.initGlobalDBConf()
        resCaseStepDebug = self.globalDB.execute_sql(sqlCaseStepDebug)
        self.globalDB.release()
        if resCaseStepDebug:
            caseStepDebugInfo = resCaseStepDebug[0]
            self.id = caseStepDebugInfo['id']
            self.caseId = caseStepDebugInfo['caseId']
            self.stepNum = caseStepDebugInfo['stepNum']
            self.interfaceId = "%s-%s" % (self.caseId, self.stepNum)
            self.traceId = md5("%s-%s" % (self.interfaceId, get_current_time()))
            self.execStatus = caseStepDebugInfo['execStatus']

            self.title = caseStepDebugInfo['title']
            self.businessLine = caseStepDebugInfo['businessLineId']
            self.modules = caseStepDebugInfo['moduleId']

            self.desc = caseStepDebugInfo['stepDesc']
            self.state = caseStepDebugInfo['state']
            self.addBy = caseStepDebugInfo['addBy']
            self.modBy = caseStepDebugInfo['modBy']
            self.addTime = caseStepDebugInfo['addTime']
            self.modTime = caseStepDebugInfo['modTime']

            self.varsPre = caseStepDebugInfo['varsPre']  # 前置变量
            if int(caseStepDebugInfo['useCustomUri']) == 1:
                self.uri = caseStepDebugInfo['customUri']
            else:
                self.uri = caseStepDebugInfo['uri']
            # self.uri = caseStepDebugInfo['uri']
            self.url = caseStepDebugInfo['url']  # 接口 interface
            if int(caseStepDebugInfo['urlRedirect']) == 0:
                self.urlRedirectStatus = False
            self.method = caseStepDebugInfo['method']
            self.header = caseStepDebugInfo['header']
            self.params = caseStepDebugInfo['params']  # key1=value1&key2=value2
            self.bodyType = caseStepDebugInfo['bodyType']  # key1=value1&key2=value2
            self.bodyContent = caseStepDebugInfo['bodyContent'].strip()  # key1=value1&key2=value2
            self.varsPost = caseStepDebugInfo['varsPost']  # 后置变量
            self.httprequestTimeout = caseStepDebugInfo['timeout']
            self.performanceTime = float(caseStepDebugInfo['performanceTime']) * 1000

            self.version = caseStepDebugInfo['version'].strip()

            self.actualResult = caseStepDebugInfo['actualResult']  # 实际结果
            self.assertResult = caseStepDebugInfo['assertResult']  # 断言结果
            self.testResult = caseStepDebugInfo['testResult']  # 测试结果

            self.beforeExecuteTakeTime = caseStepDebugInfo['beforeExecuteTakeTime']
            self.afterExecuteTakeTime = caseStepDebugInfo['afterExecuteTakeTime']
            self.executeTakeTime = caseStepDebugInfo['executeTakeTime']
            self.totalTakeTime = caseStepDebugInfo['totalTakeTime']

            self.varsStr = ""  # 变量string
            self.varsPool = {}  # 变量dict 变量池，包括varsPre的和varsPost的
            self.headerDict = {}  # header json字符串转换成的dict

    @catch_exception
    def generateByCaseStepDebugData(self):
        """
        根据步骤debug表的id获取步骤
        Returns:
            无
        """
        if self.caseStepDebugData["execStatus"] == 1:
            caseStepDebugInfo = self.caseStepDebugData
            # self.id = caseStepDebugInfo['id']
            self.stepNum = caseStepDebugInfo['stepNum']
            self.interfaceId = "%s-%s" % (self.caseId, self.stepNum)
            self.traceId = md5("%s-%s" % (self.interfaceId, get_current_time()))

            self.execStatus = caseStepDebugInfo['execStatus']

            self.title = caseStepDebugInfo['title']
            self.businessLine = caseStepDebugInfo['businessLineId']
            self.modules = caseStepDebugInfo['moduleId']

            self.desc = caseStepDebugInfo['stepDesc']

            self.varsPre = caseStepDebugInfo['varsPre']  # 前置变量
            if int(caseStepDebugInfo['useCustomUri']) == 1:
                self.uri = caseStepDebugInfo['customUri']
            else:
                self.uri = caseStepDebugInfo['uri']
            # self.uri = caseStepDebugInfo['uri']
            self.url = caseStepDebugInfo['url']  # 接口 interface
            self.urlRedirect = caseStepDebugInfo['urlRedirect']
            if int(caseStepDebugInfo['urlRedirect']) == 0:
                self.urlRedirectStatus = False
            self.method = caseStepDebugInfo['method']
            self.header = caseStepDebugInfo['header']
            self.params = caseStepDebugInfo['params']  # key1=value1&key2=value2
            self.bodyType = caseStepDebugInfo['bodyType']  # key1=value1&key2=value2
            self.bodyContent = caseStepDebugInfo['bodyContent'].strip()  # key1=value1&key2=value2
            self.varsPost = caseStepDebugInfo['varsPost']  # 后置变量
            self.httprequestTimeout = caseStepDebugInfo['timeout']
            self.performanceTime = float(caseStepDebugInfo['performanceTime']) * 1000

            self.version = caseStepDebugInfo['version'].strip()

            self.actualResult = caseStepDebugInfo['actualResult']  # 实际结果
            self.assertResult = caseStepDebugInfo['assertResult']  # 断言结果
            self.testResult = caseStepDebugInfo['testResult']  # 测试结果

            self.beforeExecuteTakeTime = caseStepDebugInfo['beforeExecuteTakeTime']
            self.afterExecuteTakeTime = caseStepDebugInfo['afterExecuteTakeTime']
            self.executeTakeTime = caseStepDebugInfo['executeTakeTime']
            self.totalTakeTime = caseStepDebugInfo['totalTakeTime']

            self.varsStr = ""  # 变量string
            self.varsPool = {}  # 变量dict 变量池，包括varsPre的和varsPost的
            self.headerDict = {}  # header json字符串转换成的dict

    def generateByStepDict(self,stepDict):
        """
        根据步骤的字典生成步骤
        Args:
            stepDict: 步骤dict

        Returns:
            无
        """
        self.id = stepDict['id']
        self.caseId = stepDict['caseId']
        self.stepNum = stepDict['stepNum']
        self.interfaceId = "%s-%s" % (self.caseId, self.stepNum)
        self.traceId = md5("%s-%s" % (self.interfaceId, get_current_time()))

        self.title = stepDict['title']
        self.desc = stepDict['stepDesc']
        self.businessLine = stepDict['businessLineId']
        self.modules = stepDict['moduleId']

        self.varsPre = stepDict['varsPre']  # 前置变量

        if int(stepDict['useCustomUri']) == 1:
            self.uri = stepDict['customUri']
        else:
            self.uri = stepDict['uri']
        # self.uri = stepDict['uri']
        self.url = stepDict['url']   # 接口 interface
        self.urlRedirect = stepDict['urlRedirect']
        if int(stepDict['urlRedirect']) == 0:
            self.urlRedirectStatus = False
        self.method = stepDict['method']
        self.header = stepDict['header']
        self.params = stepDict['params']  # key1=value1&key2=value2
        self.bodyType = stepDict['bodyType'].strip()  # key1=value1&key2=value2
        self.bodyContent = stepDict['bodyContent'].strip()  # key1=value1&key2=value2

        self.varsPost = stepDict['varsPost']  # 后置变量
        self.httprequestTimeout = stepDict['timeout']
        self.performanceTime = float(stepDict['performanceTime']) * 1000

        self.state = stepDict['state']
        self.addBy = stepDict['addBy']
        self.modBy = stepDict['modBy']
        self.addTime = stepDict['addTime']
        self.modTime = stepDict['modTime']

    def updateByStepDebugId(self):
        """
        根据步骤调试id更新执行结果
        Returns:
            无
        """
        # colstr = "id, httpConfKey, serviceConfKey, alias, httpConfDesc, httpConf, state, addBy, modBy, addTime, modTime"
        self.testResult = self.testResult == None and "没有生成测试结果" or self.testResult
        self.actualResult = self.actualResult == None and "没有实际返回结果" or self.actualResult
        self.assertResult = self.assertResult == None and "没有断言结果" or self.assertResult
        self.varsPre = self.varsPre == None and "未发现前置变量" or self.varsPre
        self.varsPost = self.varsPost == None and "未发现后置变量" or self.varsPost
        self.params = self.params == None and "没有参数" or self.params
        self.header = self.header == None and "没有头信息" or self.header
        self.uri = self.host

        self.caseStepDebugData["urlRedirect"] = self.urlRedirect
        self.caseStepDebugData["testResult"] = self.testResult
        self.caseStepDebugData["actualResult"] = self.actualResult
        self.caseStepDebugData["assertResult"] = self.assertResult
        self.caseStepDebugData["params"] = self.params
        self.caseStepDebugData["header"] = self.header
        self.caseStepDebugData["uri"] = self.uri
        self.caseStepDebugData["execStatus"] = self.execStatus
        self.caseStepDebugData["bodyContent"] = self.bodyContentFinalStr
        self.caseStepDebugData["beforeExecuteTakeTime"] = self.beforeExecuteTakeTime
        self.caseStepDebugData["afterExecuteTakeTime"] = self.afterExecuteTakeTime
        self.caseStepDebugData["executeTakeTime"] = self.executeTakeTime
        self.caseStepDebugData["totalTakeTime"] = self.totalTakeTime

        if self.testResult == ResultConst.NOTRUN:
            self.caseStepDebugData["varsPre"] = ""
            self.caseStepDebugData["varsPost"] = ""
        else:
            self.caseStepDebugData["varsPre"] = self.varsPre
            self.caseStepDebugData["varsPost"] = self.varsPost


if __name__ == "__main__":
    t = HttpTestcaseStep()
