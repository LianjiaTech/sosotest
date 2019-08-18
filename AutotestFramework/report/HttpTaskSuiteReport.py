import html
import sys

# from core.config.InitConfig import ServiceConf
from core.const.GlobalConst import ResultConst
# from core.const.GlobalConst import PerformanceConst
from core.model.BaseReport import BaseReport
from core.tools.CommonFunc import get_current_time
import json
# from core.config.InitConfig import CommonConf

class HttpTaskSuiteReport(BaseReport):
    """生成HTML测试报告
    param
    用例编号         名称    描述         系统     服务      方法      参数    预期结果          数据初始化       数据恢复        返回结果    断言结果    测试结果    (Excel列名)
    case_id      name    desc    system  service method  params  expect      data_init    data_recover  return_msg  assert_msg  test_result（dict的key）
    return：
    html文件
    """

    def __init__(self):
        super(HttpTaskSuiteReport, self).__init__()

    def divisionZero(self,min,max):
        if float(max) == 0.0:
            return 0.0
        else:
            return float(min/max)

    def createHttpReportByTask(self, taskSuiteDict , file_path='../reports/report.html'):
        testResultMsg = json.loads(taskSuiteDict["testResultMsg"])
        taskList = testResultMsg["taskList"]
        htmlFile = open(file_path, 'w',encoding="utf8")
        # 写开始的标签

        htmlFile.write("""<!DOCTYPE html>
<html>%s<body>
<!--jquery弹出层时背景层DIV-->
<div id="fade" class="black_overlay"></div>
<div id="all" style="margin:10px;"> 
<h1>%s测试报告</h1>""" % (self.report_html_head_content,taskSuiteDict["protocol"]))

        # js for toggle list and category
        htmlFile.write("""<script language='javascript'>
function toggleShowType(){
    $('#interface_show').toggle();
    $('#testcase_show').toggle();
}
function toggleSummaryAndDetail(){
    $('#summary_info').toggle();
    $('#detail_info').toggle();
}
</script>""")


        ##############任务摘要统计开始###############################################
        htmlFile.write("""<div id="summary_info" style="%s;display:block;">"""  % (taskSuiteDict["testResult"] == ResultConst.PASS and self.success_color or self.danger_color))
        htmlFile.write("<br><h2>任务集执行信息：</h2>")
        # htmlFile.write("<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;系统信息：Framework[%s] (python[%s] on OS[%s])</p>" % ( ServiceConf.framework_version, sys.version, sys.platform))
        htmlFile.write("<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;任务集ID：%s </p>" % taskSuiteDict["taskSuiteId"])
        htmlFile.write("<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;任务集名称：%s </p>" % taskSuiteDict["title"])
        htmlFile.write("<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;任务集详述：%s </p>" % taskSuiteDict["taskSuiteDesc"])
        htmlFile.write("<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;执行环境：%s </p>" % taskSuiteDict["httpConfKeyAliasList"])
        htmlFile.write("<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;执行人：%s </p>" % taskSuiteDict["execBy"])
        if taskSuiteDict["execComments"].strip() != "":
            htmlFile.write("<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;执行备注：%s </p>" % taskSuiteDict["execComments"])
        htmlFile.write("""<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;执行结果：<bdi id="summay_testresult">%s</bdi> </p>""" % taskSuiteDict["testResult"])
        htmlFile.write("<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;报告生成测试时间：%s</p>" % get_current_time())


        # 提示用例错误输出######################

        htmlFile.write("<br><h2>结果统计信息：</h2>")
        #输出结果统计table
        htmlFile.write("""<table class="table table-bordered" style="word-break:break-all; word-wrap:break-all;width:80%">""")
        htmlFile.write("""  <thead>
<tr style="%s"> 
 <th width="5%%"></th>
 <th width="10%%">总计</th>
 <th width="10%%">功能通过</th>
 <th width="10%%">功能失败</th>
 <th width="10%%">功能通过率</th>
 """ % self.warning_color)
        if taskSuiteDict["protocol"] == "HTTP":
            htmlFile.write("""
     <th width="10%%">性能通过</th>
     <th width="10%%">性能失败</th>
     <th width="10%%">性能通过率</th>""")

        htmlFile.write("""
 <th width="10%%">测试结果</th>
</tr>
</thead>
  <tbody>""")

        htmlFile.write("""<tr style="%s" id = "total_summay" >""" % (testResultMsg["caseTotal"] == testResultMsg["casePass"] and self.success_color or self.danger_color))
        htmlFile.write("""<td>所有</td>
<td><bdi id="summay_totalCount">%d</bdi></td>
<td><bdi id="summay_passCount">%d</bdi></td>
<td><bdi id="summay_failCount">%d</bdi></td>
<td><bdi id="summay_passPercent">%.2f%%</bdi></td>""" %  (
            testResultMsg["caseTotal"],
            testResultMsg["casePass"],
            testResultMsg["caseFail"],
            (self.divisionZero(float(testResultMsg["casePass"]),float(testResultMsg["caseTotal"])) * 100),


        ))
        if taskSuiteDict["protocol"] == "HTTP":
            htmlFile.write("""
<td><bdi>%d</bdi></td>
<td><bdi>%d</bdi></td>
<td><bdi>%.2f%%</bdi></td>""" % (testResultMsg["casePerformancePass"],
            testResultMsg["casePerformanceFail"],
            self.divisionZero(float(testResultMsg["casePerformancePass"]) , float(testResultMsg["caseTotal"])) * 100,))
        htmlFile.write("""
<td><bdi>%s</bdi></td>""" % taskSuiteDict["testResult"])
        htmlFile.write("""</tr>""")
        htmlFile.write("""</tbody></table>""")
        # 输出结果统计table结束
        htmlFile.write("<br><h2>任务执行情况统计：</h2>")
        htmlFile.write("<br><h3>任务执行统计：</h3>")

        htmlFile.write(
            """<table class="table table-bordered" style="word-break:break-all; word-wrap:break-all;width:90%">""")
        htmlFile.write("""<thead>
    <tr style="%s">
     <th width="5%%">任务执行ID</th>
     <th width="5%%">任务ID</th>
     <th width="5%%">任务名称</th>
     <th width="5%%">执行环境</th>
     <th width="5%%">功能通过</th>
     <th width="5%%">功能失败</th>
     <th width="6%%">功能通过率</th>""" % self.warning_color)
        if taskSuiteDict["protocol"] == "HTTP":
            htmlFile.write("""
     <th width="5%%">性能通过</th>
     <th width="5%%">性能失败</th>
     <th width="6%%">性能通过率</th>""")
        htmlFile.write("""
     <th width="6%%">测试结果</th>
     <th width="6%%">报告</th>
    </tr>
    </thead><tbody>""")
        for tmpIndex in taskList:
            if taskSuiteDict["protocol"] == "HTTP":
                htmlFile.write("""<tr style="%s" >""" % ((tmpIndex["executeSummary"]['total'] == tmpIndex["executeSummary"]['pass'] and tmpIndex["executeSummary"][
                    'total'] == tmpIndex["actualTotalPerformanceDict"]['pass']) and self.success_color or self.danger_color))
            else:
                htmlFile.write("""<tr style="%s" >""" % ((tmpIndex["executeSummary"]['total'] ==
                                                          tmpIndex["executeSummary"]['pass']) and self.success_color or self.danger_color))
            htmlFile.write("""<td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%d</td>
                <td>%d</td>
                <td>%.2f%%</td>""" % (tmpIndex["id"],tmpIndex["taskId"],tmpIndex["taskName"],
                       tmpIndex["httpConfKey"],
                       tmpIndex["executeSummary"]['pass'],
                       tmpIndex["executeSummary"]['fail'],
                       self.divisionZero(float(tmpIndex["executeSummary"]['pass']) , float(tmpIndex["executeSummary"]['total'])) * 100))
            if taskSuiteDict["protocol"] == "HTTP":
                htmlFile.write("""
                <td>%d</td>
                <td>%d</td>
                <td>%.2f%%</td>""" % (tmpIndex["actualTotalPerformanceDict"]['pass'],
                       tmpIndex["actualTotalPerformanceDict"]['fail'],
                       self.divisionZero(float(tmpIndex["actualTotalPerformanceDict"]['pass']) , float(tmpIndex["executeSummary"]['total'])) * 100))
            htmlFile.write("""
                <td>%s</td>
                <td><a href="%s" target="_blank">查看报告</a></td>
                """ % (

                       tmpIndex["testResult"],
                       tmpIndex["testReportUrl"]))

            htmlFile.write("""</tr>""")
        htmlFile.write("""</tbody></table>""")


            # =========================================================================

        ##########################################################################################################################################################

        htmlFile.write("""</div>""") #  <div id="detail_info" style="display:none;"> 结束
        htmlFile.write("""</div>""")  # <div id="all"> 结束标签
        htmlFile.write("""</body></html>""")
        # logging.debug("【测试报告】%s生成！任务集id[%s]任务名称[%s]" % (file_path,taskSuiteDict["taskSuiteId"],taskSuiteDict["title"]))
        htmlFile.close()
        return True

if __name__ == '__main__':

    pass