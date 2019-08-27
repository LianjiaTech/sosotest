import html
import sys

from core.config.InitConfig import ServiceConf
from core.const.GlobalConst import ResultConst
from core.model.BaseReport import BaseReport
from core.tools.CommonFunc import *
from core.config.InitConfig import CommonConf

class DubboReport(BaseReport):
    """生成HTML测试报告
    param
    用例编号         名称    描述         系统     服务      方法      参数    预期结果          数据初始化       数据恢复        返回结果    断言结果    测试结果    (Excel列名)
    case_id      name    desc    system  service method  params  expect      data_init    data_recover  return_msg  assert_msg  test_result（dict的key）
    return：
    html文件
    """

    def __init__(self):
        super(DubboReport, self).__init__()

    def createHttpReportByTask(self, task , file_path='../reports/report.html'):
        interfaceList = task.taskInterfaceList
        testcaseList = task.taskTestcaseList
        htmlFile = open(file_path, 'w',encoding="utf8")
        # 写开始的标签

        htmlFile.write("""<!DOCTYPE html>
<html>%s<body>
<!--jquery弹出层时背景层DIV-->
<div id="fade" class="black_overlay"></div>
<div id="all" style="margin:10px;"> 
<h1>Dubbo测试报告</h1>""" % (self.report_html_head_content))

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
function toggleRetryTrs(baseLineId){
    $("tr[name='retryTr_"+baseLineId+"']").toggle();
}
function toggleRetryCaseTrs(baseLineId){
    $("tr[nameRetry='retryCaseTr_"+baseLineId+"']").toggle();
}
</script>""")

        htmlFile.write("""<p><button class="btn btn-primary" onclick="toggleSummaryAndDetail()">统计/详情</button></p>""")

        ##############任务摘要统计开始###############################################
        htmlFile.write("""<div id="summary_info" style="%s;display:block;">"""  % (task.testResult == ResultConst.PASS and self.success_color or self.danger_color))
        htmlFile.write("<br><h2>任务执行信息：</h2>")
        htmlFile.write("<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;系统信息：Framework[%s] (python[%s] on OS[%s])</p>" % ( ServiceConf.framework_version, sys.version, sys.platform))
        htmlFile.write("<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;任务ID：%s </p>" % task.taskId)
        htmlFile.write("<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;创建人：%s </p>" % task.addBy)
        htmlFile.write("<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;任务：%s </p>" % task.title)
        htmlFile.write("<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;任务详述：%s </p>" % task.taskDesc)
        htmlFile.write("<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;任务包含的%s：%s </p>" % (CommonConf.groupLevel1,task.businessLineGroup))
        htmlFile.write("<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;任务包含的%s：%s </p>" % (CommonConf.groupLevel2,task.modulesGroup))
        # htmlFile.write("<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;任务包含的请求来源：%s </p>" % task.sourceGroup)
        htmlFile.write("<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;任务执行环境：%s </p>" % task.confHttpLayer.alias)
        htmlFile.write("<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;任务执行数据环境：%s </p>" % task.confHttpLayer.confServiceLayer.alias)
        htmlFile.write("<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;任务执行人：%s </p>" % task.execBy)
        if task.execComments.strip() != "":
            htmlFile.write("<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;任务执行备注：%s </p>" % task.execComments)
        htmlFile.write("""<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;任务执行结果：<bdi id="summay_testresult">%s</bdi> </p>""" % task.testResult)
        htmlFile.write("<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;测试完成时间：%s </p>" % task.execFinishTime)
        htmlFile.write("<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;报告生成测试时间：%s</p>" % get_current_time())
        htmlFile.write("<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;测试执行占用时间：%d 秒 </p>" % task.taskExecTakeTime)
        if task.highPriorityVARSFinalStr != "":
            htmlFile.write("<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;任务优先变量： </p><pre>%s</pre>" % task.highPriorityVARSFinalStr)

        #提示用例错误输出######################
        if task.errorCount > 0:
            htmlFile.write("<H1>发现ERROR用例%d个，请检查是否有用例错误或者测试环境异常等因素。<br>%s</H1>" % (task.errorCount,task.errorIdList))
        # 提示用例错误输出######################

        htmlFile.write("<br><h2>结果统计信息：</h2>")
        #输出结果统计table
        htmlFile.write("""<table class="table table-bordered" style="word-break:break-all; word-wrap:break-all;width:50%">""")
        htmlFile.write("""  <thead>
<tr style="%s"> 
 <th width="5%%"></th>
 <th width="10%%">总计</th>
 <th width="10%%">通过</th>
 <th width="10%%">失败</th>
 <th width="10%%">通过率</th>
</tr>
</thead>
  <tbody>""" % self.warning_color)
        if task.actualTotalInterfaces != 0:
            htmlFile.write("""  <tr style="%s" id="interface_summary">""" % (task.actualTotalInterfaces == task.interfacePassCount and self.success_color or self.danger_color))
            htmlFile.write("""   <td>接口</td>
<td><bdi id="summay_interfaceTotalCount">%d</bdi></td>
<td><bdi id="summay_interfacePassCount">%d</bdi></td>
<td><bdi id="summay_interfaceFailCount">%d</bdi></td>
<td><bdi id="summay_interfacePassPercent">%.2f%%</bdi></td>""" % (
                               task.actualTotalInterfaces,
                               task.interfacePassCount,
                               task.interfaceFailCount,
                               ((float(task.interfacePassCount) / float(task.actualTotalInterfaces)) * 100) ) )
            htmlFile.write("""</tr>""")

        if task.actualTotalTestcases != 0:
            htmlFile.write("""<tr style="%s" id="testcase_summary">""" % (task.actualTotalTestcases == task.testcasePassCount and self.success_color or self.danger_color))
            htmlFile.write("""<td>用例</td>
<td><bdi id="summay_testcaseTotalCount">%d</bdi></td>
<td><bdi id="summay_testcasePassCount">%d</bdi></td>
<td><bdi id="summay_testcaseFailCount">%d</bdi></td>
<td><bdi id="summay_testcasePassPercent">%.2f%%</bdi></td>""" % (
                               task.actualTotalTestcases,
                               task.testcasePassCount,
                               task.testcaseFailCount,
                               (float(task.testcasePassCount) / float(task.actualTotalTestcases)) * 100))
            htmlFile.write("""</tr>""")

        if task.actualTotalInterfaces != 0 and task.actualTotalTestcases != 0:
            htmlFile.write("""<tr style="%s" id = "total_summay" >""" % (task.actualTotal == task.passCount and self.success_color or self.danger_color))
            htmlFile.write("""<td>所有</td>
<td><bdi id="summay_totalCount">%d</bdi></td>
<td><bdi id="summay_passCount">%d</bdi></td>
<td><bdi id="summay_failCount">%d</bdi></td>
<td><bdi id="summay_passPercent">%.2f%%</bdi></td>""" % (
                               task.actualTotal,
                               task.passCount,
                               task.failCount,
                               (float(task.passCount) / float(task.actualTotal)) * 100) )
            htmlFile.write("""</tr>""")

        htmlFile.write("""</tbody></table>""")
        # 输出结果统计table结束

        #接口执行情况统计
        htmlFile.write("<br><h2>接口执行情况统计：</h2>")
        if len(task.interfaceCountDict) != 0:
            htmlFile.write("<br><h3>接口执行统计：</h3>")

            htmlFile.write("""<table class="table table-bordered" style="word-break:break-all; word-wrap:break-all;width:50%">""")
            htmlFile.write("""<thead>
<tr style="%s">
 <th width="25%%">接口</th>
 <th width="25%%">请求地址</th>
 <th width="10%%">总计</th>
 <th width="10%%">通过</th>
 <th width="10%%">失败</th>
 <th width="10%%">通过率</th>
</tr>
</thead><tbody>""" % self.warning_color)
            for tmpKey,tmpValue in task.interfaceCountDict.items():
                if tmpValue['total'] != 0:
                    htmlFile.write("""<tr style="%s" >""" % (tmpValue['total'] == tmpValue['pass'] and self.success_color or self.danger_color))
                    htmlFile.write("""<td>%s</td>
<td>%s</td>
<td>%d</td>
<td>%d</td>
<td>%d</td>
<td>%.2f%%</td>""" % (tmpValue['interfaceStr'],
                      tmpValue['requestHost'],
                       tmpValue['total'],
                       tmpValue['pass'],
                       tmpValue['fail'],
                       (float(tmpValue['pass']) / float(tmpValue['total'])) * 100) )
                    htmlFile.write("""</tr>""")
            htmlFile.write("""</tbody></table>""")

        if len(task.testcaseStepInterfaceCountDict) != 0:
            htmlFile.write("<br><h3>业务流执行接口统计：</h3>")

            htmlFile.write("""<table class="table table-bordered" style="word-break:break-all; word-wrap:break-all;width:50%">""")
            htmlFile.write(""" <thead>
<tr style="%s">
 <th width="25%%">接口</th>
 <th width="25%%">请求地址</th>
 <th width="10%%">总计</th>
 <th width="10%%">通过</th>
 <th width="10%%">失败</th>
 <th width="10%%">通过率</th>
</tr>
</thead>
<tbody>"""  % self.warning_color)
            for tmpKey,tmpValue in task.testcaseStepInterfaceCountDict.items():
                if tmpValue['total'] != 0 :
                    htmlFile.write("""<tr style="%s">""" % (tmpValue['total'] == tmpValue['pass'] and self.success_color or self.danger_color))
                    htmlFile.write("""<td>%s</td>
<td>%s</td>
 <td>%d</td>
 <td>%d</td>
 <td>%d</td>
 <td>%.2f%%</td>""" % (tmpValue['interfaceStr'],tmpValue['requestHost'],
                           tmpValue['total'],
                           tmpValue['pass'],
                           tmpValue['fail'],
                           (float(tmpValue['pass']) / float(tmpValue['total'])) * 100) )
                    htmlFile.write("""</tr>""")
            htmlFile.write("""</tbody></table>""")

        if len(task.totalInterfaceCountDict)!=0 :
            htmlFile.write("<br><h3>所有情况统计</h3>")
            htmlFile.write("""<table class="table table-bordered" style="word-break:break-all; word-wrap:break-all;width:50%">""")
            htmlFile.write("""<thead>
<tr style="%s">
 <th width="25%%">接口</th>
 <th width="25%%">请求地址</th>
 <th width="10%%">总计</th>
 <th width="10%%">通过</th>
 <th width="10%%">失败</th>
 <th width="10%%">通过率</th>
</tr>
</thead>
<tbody>""" % self.warning_color)

            totalDict = task.totalInterfaceCountDict
            for tmpKey, tmpValue in totalDict.items():
                if tmpValue['total'] != 0:
                    htmlFile.write("""<tr style="%s">""" % (
                    tmpValue['total'] == tmpValue['pass'] and self.success_color or self.danger_color))
                    htmlFile.write("""<td>%s</td><td>%s</td>
<td>%d</td>
<td>%d</td>
<td>%d</td>
<td>%.2f%%</td>""" % (  tmpValue['interfaceStr'],tmpValue['requestHost'],
                           tmpValue['total'],
                           tmpValue['pass'],
                           tmpValue['fail'],
                           (float(tmpValue['pass']) / float(tmpValue['total'])) * 100))
                    htmlFile.write("""</tr>""")
            htmlFile.write("""</tbody></table>""")
        htmlFile.write("""<br></div>""")  #任务摘要统计结束 <div id="summary_info" style="%s;display:block;">"
        ##############任务摘要统计结束。###############################################

        htmlFile.write(""" <div id="detail_info" style="display:none;">""")
        #######################################选择按钮部分############################
        htmlFile.write("""<div id="showDiffRadio" class="btn-group" data-toggle="buttons">
<label class="btn btn-primary">
   <input type="radio" name="options" id="optionAll" value="all" onChange="changeCaseStatus()" > ALL
</label>
<label class="btn btn-primary">
   <input type="radio" name="options" id="optionPass" value="pass" onChange="changeCaseStatus()" > PASS
</label>
<label class="btn btn-primary">
   <input type="radio" name="options" id="optionFail" value="fail" onChange="changeCaseStatus()" > FAIL
</label>
<label class="btn btn-primary" style="display:none;">
   <input type="radio" name="options" id="optionWarning" value="warning" onChange="changeCaseStatus()" > WARNING
</label>
<label class="btn btn-primary">
   <input type="radio" name="options" id="optionError" value="error" onChange="changeCaseStatus()" > ERROR
</label>
<label class="btn btn-primary">
   <input type="radio" name="options" id="optionException" value="exception" onChange="changeCaseStatus()" > EXCEPTION
</label>
<label class="btn btn-primary">
   <input type="radio" name="options" id="optionSelect" value="select" onChange="changeCaseStatus()" > SELECT
</label>""")
        if len(interfaceList) != 0 and len(testcaseList) != 0:
            htmlFile.write("""                   <button class="btn btn-primary" onclick="toggleShowType()">接口/业务流</button>""")
        htmlFile.write("""</div>""")
        #######################################选择按钮部分 结束 ############################

        ##########################################################################################################################################################
        interfaceDisplay = "block"
        testcaseDisplay = "none"
        if len(interfaceList) == 0:
            testcaseDisplay = "block"
        ##########################################################################################################################################################
        #输出接口层
        if len(interfaceList) > 0:
            #有接口用例，进行输出
            htmlFile.write("""<div id="interface_show" style="display:%s;"> <!--显示interface开始-->""" % interfaceDisplay)
            # ====================输出case列表=========================================
            htmlFile.write("""<table class="table table-bordered" style="word-break:break-all; word-wrap:break-all;">""")
            htmlFile.write("""<thead>
<tr>
   <th width="3%">序号</th>
   <th width="8%" >接口编号</th>
   <th width="10%">名称</th>
   <th width="15%">描述</th>
   <th width="22%">接口</th>
   <th width="5%">测试结果</th>
   <th width="5%">执行前耗时</th>
   <th width="5%">执行耗时</th>
   <th width="5%">执行后耗时</th>
   <th width="5%">总耗时</th>
   <th width="5%">创建人</th>
   <th width="5%">其他详情</th>

</tr>
</thead>
<tbody>""")

            for i in range(0,len(interfaceList)):
                # logging.debug("TMPTEST_name输出写入html钱：%s" % case_dict.get('name'))
                interface = interfaceList[i]
                # interface = HttpInterface() #TODO 编代码时提醒用，结束后注释掉。
                requestStr = ""
                requestStr = """系统：%s【 %s:%s 】 
dubbo请求： invoke %s.%s(
%s
)
""" % (interface.dubboSystem,interface.dubboTelnetHost,interface.dubboTelnetPort,interface.dubboService,interface.dubboMethod,interface.dubboParam)
                # if interface.interface_response.status_code == None:
                #     responseStr = interface.actualResult
                # else:
                responseStr = """%s""" % interface.actualResult

                # 获取className
                if interface.testResult == ResultConst.PASS:
                    className = "result_pass"
                if interface.testResult == ResultConst.PASS:
                    name1 = "result_pass"
                if interface.testResult == ResultConst.FAIL:
                    className = "result_fail"
                    name1 = "result_fail"
                if interface.testResult == ResultConst.WARNING:
                    className = "result_warning"
                    name1 = "result_warning"
                if interface.testResult == ResultConst.ERROR:
                    className = "result_error"
                    name1 = "result_error"
                if interface.testResult == ResultConst.EXCEPTION:
                    className = "result_exception"
                    name1 = "result_exception"
                if interface.testResult == ResultConst.NOTRUN:
                    className = "result_notrun"
                    name1 = "result_notrun"


                #切换重试的行的html
                toggleRetryTrsHtml = ""
                if len(interface.retryList) > 0:
                    toggleRetryTrsHtml = """<br><a href="javascript:void(0)" onclick="toggleRetryTrs(%d)">重试详情</a>""" % i

                htmlFile.write(""" <tr class="%s"  name="resultTr" name1="%s"  onclick="toggleTrBgClass($(this),'%s')">
<td>%d</td><td>%s</td>
<td><div style="OVERFLOW: auto;HEIGHT: 40px">%s</div></td>
<td><div style="OVERFLOW: auto;HEIGHT: 40px">%s</div></td>
<td><div style="OVERFLOW: auto;HEIGHT: 40px">%s</div></td>

<td>%s</td>
<td>%s ms</td>
<td>%s ms</td>
<td>%s ms</td>
<td>%s ms</td>
<td>%s</td>
<td>
<a href="javascript:void(0)" onclick="ShowDiv('listshow_interface_%d','fade')">查看详情</a>%s
<div id="listshow_interface_%d" class="white_content">
<label style="text-align: left; background-color: #ac2925; font-size: 80px; position:fixed;" onclick="CloseDiv('listshow_interface_%d','fade')">&nbsp;×&nbsp;</label>
<table class="table table-bordered" >
<caption>%s[%s]&nbsp;&nbsp;请求：[%s]&nbsp;%s%s</caption>
   
   <tr class="result_pop"><td>准备</td><td>%s</td></tr>
   
   <tr class="result_pop"><td>DUBBO请求</td><td>%s</td></tr>
   <tr class="result_pop"><td>DUBBO响应</td><td>%s</td></tr>
   
   <tr class="result_pop"><td>断言恢复</td><td>%s</td></tr>
   
   <tr class="result_pop"><td>断言结果</td><td>%s</td></tr>
   <tr class="result_pop"><td>耗时统计</td>
   <td>执行前耗时：%s ms &nbsp;&nbsp;&nbsp;&nbsp;
       执行耗时：%s ms &nbsp;&nbsp;&nbsp;&nbsp;
       执行后耗时：%s ms &nbsp;&nbsp;&nbsp;&nbsp;
       <br>总耗时：%s ms &nbsp;&nbsp;&nbsp;&nbsp;</td></tr>
</table>
</div>
</td>
</tr>""" % (   # 第一行参数
                className,name1,
                className,
                i+1,
                #第二行
                html.escape(interface.interfaceId),
                html.escape(interface.title),
                html.escape(interface.desc).replace("\n", "<br>"),
                "[%s]%s.%s" % (interface.dubboSystem, interface.dubboService, interface.dubboMethod),
                html.escape(interface.testResult),
                interface.beforeExecuteTakeTime,
                interface.executeTakeTime,
                interface.afterExecuteTakeTime,
                interface.totalTakeTime,
                interface.addBy,
                #第4-6行
                i,toggleRetryTrsHtml,i,i,
                #第八行 <caption>开始
                html.escape(interface.interfaceId),
                html.escape(interface.title),
                interface.dubboSystem,
                html.escape(interface.dubboSystem),
                html.escape(interface.dubboService),
                html.escape(interface.varsPre).replace("\n", "<br>"), #从这里开始处理
                html.escape(requestStr).replace("\n", "<br>"),
                html.escape(responseStr).replace("\n", "<br>"),
                html.escape(interface.varsPost).replace("\n", "<br>"),#到这里结束
                html.escape(interface.assertResult).replace("\n", "<br>"),
                interface.beforeExecuteTakeTime,
                interface.executeTakeTime,
                interface.afterExecuteTakeTime,
                interface.totalTakeTime

                ))
                if len(interface.retryList) > 0:
                    #写retry的行和查看详情
                    for retryIndex in range(0,len(interface.retryList)):
                        interfaceRetry = interface.retryList[retryIndex]
                        requestStr = """系统：%s【 %s:%s 】 
                        dubbo请求： invoke %s.%s(
                        %s
                        )
                        """ % (interfaceRetry.dubboSystem, interfaceRetry.dubboTelnetHost, interfaceRetry.dubboTelnetPort,
                               interfaceRetry.dubboService, interfaceRetry.dubboMethod, interfaceRetry.dubboParam)
                        responseStr = """%s""" % interfaceRetry.actualResult

                        # 获取className
                        if interfaceRetry.testResult == ResultConst.PASS:
                            className = "result_pass"
                        if interfaceRetry.testResult == ResultConst.PASS:
                            name1 = "result_pass"
                        if interfaceRetry.testResult == ResultConst.FAIL:
                            className = "result_fail"
                            name1 = "result_fail"
                        if interfaceRetry.testResult == ResultConst.WARNING:
                            className = "result_warning"
                            name1 = "result_warning"
                        if interfaceRetry.testResult == ResultConst.ERROR:
                            className = "result_error"
                            name1 = "result_error"
                        if interfaceRetry.testResult == ResultConst.EXCEPTION:
                            className = "result_exception"
                            name1 = "result_exception"
                        if interfaceRetry.testResult == ResultConst.NOTRUN:
                            className = "result_notrun"
                            name1 = "result_notrun"

                        htmlFile.write(""" <tr class="%s" style="display:none" name="retryTr_%d"  nameRetryTr="1" onclick="toggleTrBgClass($(this),'%s')">
                        <td colspan="4" style="text-align:right;">%s</td>
                        <td><div style="OVERFLOW: auto;HEIGHT: 40px">%s</div></td>

                        <td>%s</td>
                        <td>%s ms</td>
                        <td>%s ms</td>
                        <td>%s ms</td>
                        <td>%s ms</td>
                        <td>%s</td>
                        <td>
                        <a href="javascript:void(0)" onclick="ShowDiv('listshow_interface_%d_%d','fade')">查看详情</a>
                        <div id="listshow_interface_%d_%d" class="white_content">
                        <label style="text-align: left; background-color: #ac2925; font-size: 80px; position:fixed;" onclick="CloseDiv('listshow_interface_%d_%d','fade')">&nbsp;×&nbsp;</label>
                        <table class="table table-bordered" >
                        <caption>%s[%s]&nbsp;&nbsp;请求：[%s]&nbsp;%s%s</caption>

                           <tr class="result_pop"><td>准备</td><td>%s</td></tr>

                           <tr class="result_pop"><td>DUBBO请求</td><td>%s</td></tr>
                           <tr class="result_pop"><td>DUBBO响应</td><td>%s</td></tr>

                           <tr class="result_pop"><td>断言恢复</td><td>%s</td></tr>

                           <tr class="result_pop"><td>断言结果</td><td>%s</td></tr>
                           <tr class="result_pop"><td>耗时统计</td>
                           <td>执行前耗时：%s ms &nbsp;&nbsp;&nbsp;&nbsp;
                               执行耗时：%s ms &nbsp;&nbsp;&nbsp;&nbsp;
                               执行后耗时：%s ms &nbsp;&nbsp;&nbsp;&nbsp;
                               <br>总耗时：%s ms &nbsp;&nbsp;&nbsp;&nbsp;</td></tr>
                        </table>
                        </div>
                        </td>
                        </tr>""" % (  # 第一行参数
                            className,i,
                            className,
                            # 第二行
                            "Retry-" + str(retryIndex + 1),
                            "[%s]%s.%s" % (interfaceRetry.dubboSystem,interfaceRetry.dubboService,interfaceRetry.dubboMethod),
                            html.escape(interfaceRetry.testResult),
                            interfaceRetry.beforeExecuteTakeTime,
                            interfaceRetry.executeTakeTime,
                            interfaceRetry.afterExecuteTakeTime,
                            interfaceRetry.totalTakeTime,
                            interfaceRetry.addBy,
                            # 第4-6行
                            i,retryIndex, i,retryIndex, i, retryIndex,
                            # 第八行 <caption>开始
                            html.escape(interfaceRetry.interfaceId),
                            html.escape(interfaceRetry.title),
                            interfaceRetry.dubboSystem,
                            html.escape(interfaceRetry.dubboSystem),
                            html.escape(interfaceRetry.dubboService),
                            html.escape(interfaceRetry.varsPre).replace("\n", "<br>"),  # 从这里开始处理
                            html.escape(requestStr).replace("\n", "<br>"),
                            html.escape(responseStr).replace("\n", "<br>"),
                            html.escape(interfaceRetry.varsPost).replace("\n", "<br>"),  # 到这里结束
                            html.escape(interfaceRetry.assertResult).replace("\n", "<br>"),
                            interfaceRetry.beforeExecuteTakeTime,
                            interfaceRetry.executeTakeTime,
                            interfaceRetry.afterExecuteTakeTime,
                            interfaceRetry.totalTakeTime

                        ))
            htmlFile.write("""</tbody></table>""")
            # =========================================================================
            htmlFile.write("""</div><!--显示interface结束-->""")

        ##########################################################################################################################################################
        #输出用例层
        if len(testcaseList) > 0:
            # 有测试用例带步骤的，进行输出
            htmlFile.write("""<div id="testcase_show" style="display:%s;"> <!--显示case开始-->""" % testcaseDisplay)
            # ====================输出case列表=========================================
            htmlFile.write("""<table class="table table-bordered" style="word-break:break-all; word-wrap:break-all;">""")
            htmlFile.write("""<thead>
<tr>
    <th width="3%">序号</th>
    <th width="7%">用例编号</th>
    <th width="12%">名称</th>
    <th width="18%">描述</th>
    <th width="5%">步骤数量</th>
    <th width="20%">断言结果</th>
    <th width="5%">测试结果</th>
    <th width="5%">执行前耗时</th>
    <th width="5%">执行耗时</th>
    <th width="5%">执行后耗时</th>
    <th width="5%">总耗时</th>
    <th width="5%">创建人</th>
    <th width="10%">查看</th>
</tr>
</thead>
<tbody>""")

            for i in range(0,len(testcaseList)):
                httpTestcase = testcaseList[i]
                # httpTestcase = HttpTestcase()
                if httpTestcase.testResult == ResultConst.PASS:
                    className = "result_pass"
                if httpTestcase.testResult == ResultConst.PASS:
                    name1 = "result_pass"
                if httpTestcase.testResult == ResultConst.FAIL:
                    className = "result_fail"
                    name1 = "result_fail"
                if httpTestcase.testResult == ResultConst.WARNING:
                    className = "result_warning"
                    name1 = "result_warning"
                if httpTestcase.testResult == ResultConst.ERROR:
                    className = "result_error"
                    name1 = "result_error"
                if httpTestcase.testResult == ResultConst.EXCEPTION:
                    className = "result_exception"
                    name1 = "result_exception"
                if httpTestcase.testResult == ResultConst.NOTRUN:
                    className = "result_notrun"
                    name1 = "result_notrun"

                # 切换重试的行的html
                toggleRetryTrsHtml = ""
                if len(httpTestcase.retryList) > 0:
                    toggleRetryTrsHtml = """<br><a href="javascript:void(0)" onclick="toggleRetryCaseTrs(%d)">重试详情</a>""" % i

                htmlFile.write("""<tr class="%s" name="resultTr" name1="%s" onclick="toggleTrBgClass($(this),'%s')">
<td>%d</td>    
<td>%s</td>
<td><div style="OVERFLOW: auto;HEIGHT: 40px">%s</div></td>
<td><div style="OVERFLOW: auto;HEIGHT: 40px">%s</div></td>
<td>%s</td>
<td><div style="OVERFLOW: auto;HEIGHT: 40px">%s</div></td>
<td>%s</td>
<td>%s ms</td>
<td>%s ms</td>
<td>%s ms</td>
<td>%s ms</td>
<td>%s</td>
<td>""" % (#第一行
                className,name1,
                className,
                i + 1,
                #第二行
                httpTestcase.caseId,
                httpTestcase.title,
                html.escape(httpTestcase.desc).replace("\n","<br>"),
                httpTestcase.stepCount,
                html.escape(httpTestcase.assertResult).replace("\n","<br>"),
                httpTestcase.testResult,
                httpTestcase.beforeExecuteTakeTime,
                httpTestcase.executeTakeTime,
                httpTestcase.afterExecuteTakeTime,
                httpTestcase.totalTakeTime,
                httpTestcase.addBy
                ))  # 截止到tgcDesc，下面是循环展开步骤
                # 步骤显示部分
                htmlFile.write("""<a href="javascript:void(0)" onclick="toggleDivById('steplistshow_%d')">查看步骤</a>%s
</td></tr>
<tr class="stepDivs" id="steplistshow_%d" style="display:none;"><td colspan="13">
<div>
<table class="table table-bordered" style="word-break:break-all; word-wrap:break-all;">
<thead>
<tr>
<th width="3%%">步骤</th>
<th width="27%%">描述</th>
<th width="15%%">请求地址（服务）</th>
<th width="25%%">请求类/方法</th>
<th width="5%%">测试结果</th>
<th width="5%%">执行前耗时</th>
<th width="5%%">执行耗时</th>
<th width="5%%">执行后耗时</th>
<th width="5%%">总耗时</th>
<th width="5%%">查看</th>
</tr>
</thead>
<tbody>""" % (i,toggleRetryTrsHtml,i))
                # 循环输出各个步骤
                for stepi in range(0,len(httpTestcase.stepTestcaseList)):

                    tmpStep = httpTestcase.stepTestcaseList[stepi]
                    # tmpStep = HttpTestcaseStep()
                    requestStr = """系统：%s【 %s:%s 】 
                    dubbo请求： invoke %s.%s(
                    %s
                    )
                    """ % (tmpStep.dubboSystem, tmpStep.dubboTelnetHost, tmpStep.dubboTelnetPort, tmpStep.dubboService,
                        tmpStep.dubboMethod, tmpStep.dubboParam)
                    # if interface.interface_response.status_code == None:
                    #     responseStr = interface.actualResult
                    # else:
                    responseStr = """%s""" % tmpStep.actualResult
                    htmlFile.write("""<tr class="%s">
<td >%s</td>
<td><div style="OVERFLOW: auto;HEIGHT: 40px">%s</div></td>
<td>%s</td>
<td>%s</td>
<td>%s</td>
<td>%s ms</td>
<td>%s ms</td>
<td>%s ms</td>
<td>%s ms</td>
<td><a href="javascript:void(0)" onclick="ShowStepDiv('steplistshow_%d_%d_desc','fade')">查看详情</a>

<div id="steplistshow_%d_%d_desc" class="white_content">
<label style="text-align: left; background-color: #ac2925; font-size: 80px; position:fixed;"
onclick="CloseDiv('steplistshow_%d_%d_desc','fade')">&nbsp;×&nbsp;</label>
<table class="table table-bordered" >
<caption>%s[%s]&nbsp;&nbsp;请求：[%s]&nbsp;%s%s</caption>
<tr class="result_pop"><td>准备</td><td>%s</td></tr>

<tr class="result_pop"><td>DUBBO请求</td><td>%s</td></tr>
<tr class="result_pop"><td>DUBBO响应</td><td>%s</td></tr>

<tr class="result_pop"><td>断言恢复</td><td>%s</td></tr>
<tr class="result_pop"><td>断言结果</td><td>%s</td></tr>
<tr class="result_pop"><td>耗时统计</td>
<td>执行前耗时：%s ms &nbsp;&nbsp;&nbsp;&nbsp;
执行耗时：%s ms &nbsp;&nbsp;&nbsp;&nbsp;
执行后耗时：%s ms &nbsp;&nbsp;&nbsp;&nbsp;
<br>总耗时：%s ms &nbsp;&nbsp;&nbsp;&nbsp;</td></tr>
</table>
</div></td>""" % (  "result_casestep",
                      tmpStep.stepNum,
                      tmpStep.desc,
                      "%s:%s(%s)" % (tmpStep.dubboTelnetHost,tmpStep.dubboTelnetPort,tmpStep.dubboSystem) ,#请求地址（服务）
                      "%s.%s" % (tmpStep.dubboService,tmpStep.dubboMethod) ,#请求地址（服务）
                      tmpStep.testResult,
                      tmpStep.beforeExecuteTakeTime,
                      tmpStep.executeTakeTime,
                      tmpStep.afterExecuteTakeTime,
                      tmpStep.totalTakeTime,
                      #开始：<td><a href="#" onclick="ShowStepDiv('steplistshow_%d_desc','fade')">查看详情</a>
                      i, tmpStep.stepNum, i, tmpStep.stepNum, i, tmpStep.stepNum,
                      #开始：<caption>%s[%s]<br>请求地址:%s:%s
                      tmpStep.stepNum,
                      tmpStep.title,
                      tmpStep.dubboSystem,
                      tmpStep.dubboService,
                      tmpStep.dubboMethod,
                      html.escape(tmpStep.varsPre).replace("\n", "<br>"),  # 从这里开始处理
                      html.escape(requestStr).replace("\n", "<br>"),
                      html.escape(responseStr).replace("\n", "<br>"),
                      html.escape(tmpStep.varsPost).replace("\n", "<br>"),  # 到这里结束
                      html.escape(tmpStep.assertResult).replace("\n","<br>"),
                      tmpStep.beforeExecuteTakeTime,
                      tmpStep.executeTakeTime,
                      tmpStep.afterExecuteTakeTime,
                      tmpStep.totalTakeTime
                      ))
                htmlFile.write("""</tbody></table></div>""")

                if len(httpTestcase.retryList) > 0:
                    # 写retry的行和查看详情
                    for retryIndex in range(0, len(httpTestcase.retryList)):
                        httpTestcaseRetry = httpTestcase.retryList[retryIndex]
                        # 获取className
                        # 获取className
                        if httpTestcaseRetry.testResult == ResultConst.PASS:
                            className = "result_pass"
                        if httpTestcaseRetry.testResult == ResultConst.PASS:
                            name1 = "result_pass"
                        if httpTestcaseRetry.testResult == ResultConst.FAIL:
                            className = "result_fail"
                            name1 = "result_fail"
                        if httpTestcaseRetry.testResult == ResultConst.WARNING:
                            className = "result_warning"
                            name1 = "result_warning"
                        if httpTestcaseRetry.testResult == ResultConst.ERROR:
                            className = "result_error"
                            name1 = "result_error"
                        if httpTestcaseRetry.testResult == ResultConst.EXCEPTION:
                            className = "result_exception"
                            name1 = "result_exception"
                        if httpTestcaseRetry.testResult == ResultConst.NOTRUN:
                            className = "result_notrun"
                            name1 = "result_notrun"

                        htmlFile.write("""<tr class="%s" style="display:none" nameRetry="retryCaseTr_%d" name="resultTr" nameRetryTr="1" onclick="toggleTrBgClass($(this),'%s')">
                        <td colspan="5" style="text-align:right;">%s</td>    
            
                        <td><div style="OVERFLOW: auto;HEIGHT: 40px">%s</div></td>
                        <td>%s</td>
                        <td>%s ms</td>
                        <td>%s ms</td>
                        <td>%s ms</td>
                        <td>%s ms</td>
                        <td>%s</td>
                        <td>""" % (  # 第一行
                            className,i,
                            className,
                            "Retry-%s" % (str(retryIndex + 1)),
                            html.escape(httpTestcaseRetry.assertResult).replace("\n", "<br>"),
                            httpTestcaseRetry.testResult,
                            httpTestcaseRetry.beforeExecuteTakeTime,
                            httpTestcaseRetry.executeTakeTime,
                            httpTestcaseRetry.afterExecuteTakeTime,
                            httpTestcaseRetry.totalTakeTime,
                            httpTestcaseRetry.addBy
                        ))  # 截止到tgcDesc，下面是循环展开步骤
                        # 步骤显示部分
                        htmlFile.write("""<a href="javascript:void(0)" onclick="toggleDivById('steplistshow_%d_%d')">查看步骤</a>
                        </td></tr>
                        <tr class="stepDivs" id="steplistshow_%d_%d" style="display:none;"><td colspan="13">
                        <div>
                        <table class="table table-bordered" style="word-break:break-all; word-wrap:break-all;">
                        <thead>
                        <tr>
                        <th width="3%%">步骤</th>
                        <th width="27%%">描述</th>
                        <th width="15%%">请求地址（服务）</th>
                        <th width="25%%">请求类/方法</th>
                        <th width="5%%">测试结果</th>
                        <th width="5%%">执行前耗时</th>
                        <th width="5%%">执行耗时</th>
                        <th width="5%%">执行后耗时</th>
                        <th width="5%%">总耗时</th>
                        <th width="5%%">查看</th>
                        </tr>
                        </thead>
                        <tbody>""" % (i,retryIndex, i, retryIndex))
                        # 循环输出各个步骤
                        for stepi in range(0, len(httpTestcaseRetry.stepTestcaseList)):
                            tmpStep = httpTestcaseRetry.stepTestcaseList[stepi]
                            # tmpStep = HttpTestcaseStep()
                            requestStr = """系统：%s【 %s:%s 】 
                                            dubbo请求： invoke %s.%s(
                                            %s
                                            )
                                            """ % (
                            tmpStep.dubboSystem, tmpStep.dubboTelnetHost, tmpStep.dubboTelnetPort, tmpStep.dubboService,
                            tmpStep.dubboMethod, tmpStep.dubboParam)
                            # if interface.interface_response.status_code == None:
                            #     responseStr = interface.actualResult
                            # else:
                            responseStr = """%s""" % tmpStep.actualResult
                            htmlFile.write("""<tr class="%s">
                        <td >%s</td>
                        <td><div style="OVERFLOW: auto;HEIGHT: 40px">%s</div></td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s ms</td>
                        <td>%s ms</td>
                        <td>%s ms</td>
                        <td>%s ms</td>
                        <td><a href="javascript:void(0)" onclick="ShowStepDiv('steplistshow_%d_%d_%d_desc','fade')">查看详情</a>

                        <div id="steplistshow_%d_%d_%d_desc" class="white_content">
                        <label style="text-align: left; background-color: #ac2925; font-size: 80px; position:fixed;"
                        onclick="CloseDiv('steplistshow_%d_%d_%d_desc','fade')">&nbsp;×&nbsp;</label>
                        <table class="table table-bordered" >
                        <caption>%s[%s]&nbsp;&nbsp;请求：[%s]&nbsp;%s%s</caption>
                        <tr class="result_pop"><td>准备</td><td>%s</td></tr>

                        <tr class="result_pop"><td>DUBBO请求</td><td>%s</td></tr>
                        <tr class="result_pop"><td>DUBBO响应</td><td>%s</td></tr>

                        <tr class="result_pop"><td>断言恢复</td><td>%s</td></tr>
                        <tr class="result_pop"><td>断言结果</td><td>%s</td></tr>
                        <tr class="result_pop"><td>耗时统计</td>
                        <td>执行前耗时：%s ms &nbsp;&nbsp;&nbsp;&nbsp;
                        执行耗时：%s ms &nbsp;&nbsp;&nbsp;&nbsp;
                        执行后耗时：%s ms &nbsp;&nbsp;&nbsp;&nbsp;
                        <br>总耗时：%s ms &nbsp;&nbsp;&nbsp;&nbsp;</td></tr>
                        </table>
                        </div></td>""" % ("result_casestep",
                                          tmpStep.stepNum,
                                          tmpStep.desc,
                                          "%s:%s(%s)" % (tmpStep.dubboTelnetHost, tmpStep.dubboTelnetPort,
                                                         tmpStep.dubboSystem),  # 请求地址（服务）
                                          "%s.%s" % (tmpStep.dubboService, tmpStep.dubboMethod),  # 请求地址（服务）
                                          tmpStep.testResult,
                                          tmpStep.beforeExecuteTakeTime,
                                          tmpStep.executeTakeTime,
                                          tmpStep.afterExecuteTakeTime,
                                          tmpStep.totalTakeTime,
                                          # 开始：<td><a href="#" onclick="ShowStepDiv('steplistshow_%d_desc','fade')">查看详情</a>
                                          i, tmpStep.stepNum,retryIndex, i, tmpStep.stepNum,retryIndex, i, tmpStep.stepNum,retryIndex,
                                          # 开始：<caption>%s[%s]<br>请求地址:%s:%s
                                          tmpStep.stepNum,
                                          tmpStep.title,
                                          tmpStep.dubboSystem,
                                          tmpStep.dubboService,
                                          tmpStep.dubboMethod,
                                          html.escape(tmpStep.varsPre).replace("\n", "<br>"),  # 从这里开始处理
                                          html.escape(requestStr).replace("\n", "<br>"),
                                          html.escape(responseStr).replace("\n", "<br>"),
                                          html.escape(tmpStep.varsPost).replace("\n", "<br>"),  # 到这里结束
                                          html.escape(tmpStep.assertResult).replace("\n", "<br>"),
                                          tmpStep.beforeExecuteTakeTime,
                                          tmpStep.executeTakeTime,
                                          tmpStep.afterExecuteTakeTime,
                                          tmpStep.totalTakeTime
                                          ))

                        htmlFile.write("""</tbody></table></div>""")

            htmlFile.write("""</td></tr></tbody></table>""")
            # =========================================================================
            htmlFile.write("""</div><!--显示case结束-->""")

        ##########################################################################################################################################################

        htmlFile.write("""</div>""") #  <div id="detail_info" style="display:none;"> 结束
        htmlFile.write("""</div>""")  # <div id="all"> 结束标签
        htmlFile.write("""</body></html>""")
        logging.debug("【测试报告】%s生成！任务id[%s]任务名称[%s]" % (file_path,task.taskId,task.title))
        htmlFile.close()
        return True

if __name__ == '__main__':
    htmlStr = "<div>abc</div>"
    print(htmlStr)
    print( html.escape(htmlStr))