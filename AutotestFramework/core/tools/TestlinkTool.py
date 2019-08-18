import testlink

from core.decorator.normal_functions import *


class TestlinkTool(object):

    # @catch_exception
    def __init__(self,url = "http://192.168.0.102/testlink/lib/api/xmlrpc.php", key = "d65fcff4ad29e42c8e931a3ed0c314dd"):
        self.url = url
        self.key = key
        self.tlc = testlink.TestlinkAPIClient(url, key)

        self.manual = 1  # 手动
        self.automation = 2  # 自动

    @catch_exception
    def get_information_test_project(self):
        print("Number of Projects      in TestLink: %s " % self.tlc.countProjects())
        print("Number of Platforms  (in TestPlans): %s " % self.tlc.countPlatforms())
        print("Number of Builds                   : %s " % self.tlc.countBuilds())
        print("Number of TestPlans                : %s " % self.tlc.countTestPlans())
        print("Number of TestSuites               : %s " % self.tlc.countTestSuites())
        print("Number of TestCases (in TestSuites): %s " % self.tlc.countTestCasesTS())
        print("Number of TestCases (in TestPlans) : %s " % self.tlc.countTestCasesTP())
        self.tlc.listProjects()

    @catch_exception
    def get_test_suite(self):
        projects = self.tlc.getProjects()
        top_suites = self.tlc.getFirstLevelTestSuitesForTestProject(projects[0]["id"])
        for suite in top_suites:
            print (suite["id"], suite["name"])

    @catch_exception
    def create_test_suite(self, project_id, test_suite_name, test_suite_describe, father_id):
        if father_id == "":
            self.tlc.createTestSuite(project_id, test_suite_name, test_suite_describe)
        else:
            self.tlc.createTestSuite(project_id, test_suite_name, test_suite_describe, parentid=father_id)

    @catch_exception
    def create_test_case(self, father_id, data):
        self.tlc.initStep(data[0][2], data[0][3], self.automation)
        for i in range(1, len(data)):
            self.tlc.appendStep(data[i][2], data[i][3], self.automation)
        self.tlc.createTestCase(data[0][0], father_id, "1", "timen.xu", "", preconditions=data[0][1])

    @catch_exception
    def get_test_case(self, test_case_id):
        test_case = self.tlc.getTestCase(None, testcaseexternalid=test_case_id)
        for i in test_case:
            print("序列", "执行步骤", "预期结果")
            for m in i.get("steps"):
                print(m.get("step_number"), m.get("actions"), m.get("expected_results"))

    @catch_exception
    def report_test_result(self, test_plan_id, test_case_id, test_result):
        self.tlc.reportTCResult(None, test_plan_id, None, test_result, "", guess=True,testcaseexternalid=test_case_id, platformname="0")

