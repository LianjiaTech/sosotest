from core.model.DubboBase import DubboBase
from core.decorator.normal_functions import *
from core.tools.CommonFunc import *
from core.tools.DBTool import DBTool

from core.const.GlobalConst import CaseLevel
from core.const.GlobalConst import CaseStatus
from core.const.GlobalConst import ObjTypeConst

class DubboTestcaseStep(DubboBase):
    """
    用例步骤类
    """
    def __init__(self):
        super(DubboTestcaseStep, self).__init__()
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

    @take_time
    def executeStep(self):
        """
        执行步骤
        Returns:
            无
        """
        logging.debug("****************************************步骤[%d]开始执行****************************************" % (self.stepNum))
        super(DubboTestcaseStep,self).execute()
        logging.debug( "****************************************步骤[%d]结束执行****************************************" % (self.stepNum))

    @catch_exception
    def generateByCaseStepDebugId(self):
        """
        根据步骤debug表的id获取步骤
        Returns:
            无
        """
        sqlCaseStepDebug = "select * from tb2_dubbo_testcase_step_debug where id=%d" % int(self.caseStepDebugId)
        self.globalDB.initGlobalDBConf()
        resCaseStepDebug = self.globalDB.execute_sql(sqlCaseStepDebug)
        self.globalDB.release()
        if resCaseStepDebug:
            caseStepDebugInfo = resCaseStepDebug[0]
            self.id = caseStepDebugInfo['id']
            self.caseId = caseStepDebugInfo['caseId']
            self.stepNum = caseStepDebugInfo['stepNum']
            self.interfaceId = "%s-%s" % (self.caseId, self.stepNum)

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

            self.stepSwitch = caseStepDebugInfo['stepSwitch']

            self.customUri = caseStepDebugInfo['customUri']
            self.useCustomUri = caseStepDebugInfo['useCustomUri']
            self.dubboSystem = caseStepDebugInfo['dubboSystem']
            self.dubboService = caseStepDebugInfo['dubboService']  # 接口 interface
            self.dubboMethod = caseStepDebugInfo['dubboMethod']
            self.dubboParam = caseStepDebugInfo['dubboParams']
            self.encoding = caseStepDebugInfo['encoding']

            self.varsPost = caseStepDebugInfo['varsPost']  # 后置变量
            self.httprequestTimeout = caseStepDebugInfo['timeout']

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

    def generateByStepDict(self,stepDict = {}):
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

        self.title = stepDict['title']
        self.desc = stepDict['stepDesc']
        self.businessLine = stepDict['businessLineId']
        self.modules = stepDict['moduleId']

        self.varsPre = stepDict['varsPre']  # 前置变量
        self.dubboSystem = stepDict['dubboSystem']
        self.dubboService = stepDict['dubboService']  # 接口 interface
        self.dubboMethod = stepDict['dubboMethod']
        self.dubboParam = stepDict['dubboParams']

        self.varsPost = stepDict['varsPost']  # 后置变量
        self.httprequestTimeout = stepDict['timeout']

        self.state = stepDict['state']
        self.addBy = stepDict['addBy']
        self.modBy = stepDict['modBy']
        self.addTime = stepDict['addTime']
        self.modTime = stepDict['modTime']


    def generateByStepDebugDict(self,stepDict = {}):
        """
        根据步骤的字典生成步骤
        Args:
            stepDict: 步骤dict

        Returns:
            无
        """
        self.stepNum = stepDict['stepNum']

        self.title = stepDict['title']
        self.desc = stepDict['stepDesc']
        self.businessLine = stepDict['businessLineId']
        self.modules = stepDict['moduleId']

        self.varsPre = stepDict['varsPre']  # 前置变量
        self.dubboSystem = stepDict['dubboSystem']
        self.dubboService = stepDict['dubboService']  # 接口 interface
        self.dubboMethod = stepDict['dubboMethod']
        self.dubboParam = stepDict['dubboParams']

        self.varsPost = stepDict['varsPost']  # 后置变量

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
        self.dubboSystem = str(self.dubboSystem) + "(" + str(self.dubboTelnetHost) + ":" + str(self.dubboTelnetPort) + ")"

        self.caseStepDebugData["testResult"] = self.testResult
        self.caseStepDebugData["actualResult"] = self.actualResult
        self.caseStepDebugData["assertResult"] = self.assertResult
        self.caseStepDebugData["execStatus"] = self.execStatus
        self.caseStepDebugData["beforeExecuteTakeTime"] = self.beforeExecuteTakeTime
        self.caseStepDebugData["afterExecuteTakeTime"] = self.afterExecuteTakeTime
        self.caseStepDebugData["executeTakeTime"] = self.executeTakeTime
        self.caseStepDebugData["totalTakeTime"] = self.totalTakeTime
        self.caseStepDebugData["dubboSystem"] = self.dubboSystem
        self.caseStepDebugData["dubboParams"] = self.dubboParam
        self.caseStepDebugData["dubboMethod"] = self.dubboMethod
        if self.testResult == ResultConst.NOTRUN:
            self.caseStepDebugData["varsPre"] = ""
            self.caseStepDebugData["varsPost"] = ""
        else:
            self.caseStepDebugData["varsPre"] = self.varsPre
            self.caseStepDebugData["varsPost"] = self.varsPost
        # sql = """ UPDATE tb2_dubbo_testcase_step_debug SET dubboSystem='%s',dubboParams='%s',testResult='%s',actualResult='%s',assertResult='%s',
        #         beforeExecuteTakeTime=%d,afterExecuteTakeTime=%d, executeTakeTime=%d, totalTakeTime=%d, execStatus = 3,varsPre='%s',varsPost='%s',modTime='%s' WHERE id=%d""" \
        #             % (self.dubboSystem,self.dubboParam,self.testResult,self.actualResult,self.assertResult,
        #                int(self.beforeExecuteTakeTime),int(self.afterExecuteTakeTime),int(self.executeTakeTime),int(self.totalTakeTime),self.varsPre,self.varsPost,get_current_time(),self.caseStepDebugId)
        # logging.debug("############################################updateByStepDebugId:%s" % sql)
        standardLen = 1000
        # try:
        #     self.globalDB.initGlobalDBConf()
        #     res = self.globalDB.execute_sql(sql)
        #     if res == False:
        #         sql = """ UPDATE tb2_dubbo_testcase_step_debug SET testResult='%s',actualResult='%s',assertResult='%s',
        #                                     beforeExecuteTakeTime=%d,afterExecuteTakeTime=%d, executeTakeTime=%d, totalTakeTime=%d, execStatus = 3,varsPre='%s',varsPost='%s' WHERE id=%d""" \
        #               % (
        #                  "EXCEPTION",
        #                  "EXCEPTION:平台更新测试结果时发生异常，请联系管理员检查原因。",
        #                  "EXCEPTION:平台更新测试结果时发生异常，请联系管理员检查原因。",
        #                  int(self.beforeExecuteTakeTime),
        #                  int(self.afterExecuteTakeTime),
        #                  int(self.executeTakeTime),
        #                  int(self.totalTakeTime),
        #                  "EXCEPTION:平台更新测试结果时发生异常，请联系管理员检查原因。",
        #                  "EXCEPTION:平台更新测试结果时发生异常，请联系管理员检查原因。",
        #                  self.caseStepDebugId)
        #         res = self.globalDB.execute_sql(sql)
        # except Exception as e:
        #     logging.error(traceback.format_exc())
        # finally:
        #     self.globalDB.release()


if __name__ == "__main__":
    t = DubboTestcaseStep()
