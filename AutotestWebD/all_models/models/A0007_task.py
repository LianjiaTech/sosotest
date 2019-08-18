# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from all_models.models.A0002_config import *
from all_models.models.A0003_attribute import *

class TbTask(models.Model):
    taskId = models.CharField(db_column='taskId', unique=True, max_length=25,verbose_name="任务ID")
    title = models.CharField(max_length=100,verbose_name="任务标题")
    taskdesc = models.CharField(max_length=1000,verbose_name="任务描述")
    protocol = models.CharField(max_length=20,verbose_name="任务协议")
    businessLineGroup = models.CharField(db_column='businessLineGroup', max_length=1000,verbose_name="任务包含的业务线名称，例如 SFA,服务云")
    modulesGroup = models.CharField(db_column='modulesGroup', max_length=1000, verbose_name="任务包含的模块名称，例如 合同,订单")
    sourceGroup = models.CharField(db_column='sourceGroup',default="['电脑Web']", max_length=1000, verbose_name="任务包含的来源名称，例如 IOS 安卓 Web端 所有")
    emailList = models.CharField(db_column='emailList', max_length=2000,default='',verbose_name="发送邮件列表，除却执行人execBy以外的其他收件人")#release2 新增
    taskLevel = models.IntegerField(default=5,verbose_name="优先级，数字越小，优先级越高，从0-9。 0高 5中 9低",db_column="taskLevel")
    highPriorityVARS = models.TextField(db_column='highPriorityVARS', default='', verbose_name="高优先级变量，执行时覆盖同名的变量和全局变量")  # release2 新增
    status = models.IntegerField(default=2,verbose_name="状态，1新建待审核 2审核通过 3审核未通过")
    interfaceCount = models.IntegerField(db_column='interfaceCount',verbose_name="任务中的接口数量统计")
    taskInterfaces = models.TextField(db_column='taskInterfaces',verbose_name="任务中的接口列表，多个接口用,间隔，例如 HTTP_INTERFACE_1,HTTP_INTERFACE_2")
    caseCount = models.IntegerField(db_column='caseCount',verbose_name="任务中的用例数量统计")
    taskTestcases = models.TextField(db_column='taskTestcases',verbose_name="任务中的用例列表，多个接口用,间隔，例如 HTTP_TESTCASE_1,HTTP_TESTCASE_2")
    interfaceNum = models.IntegerField(db_column='interfaceNum',verbose_name="任务总的接口数量，包含接口的和用例中的步骤数量")
    isCI = models.IntegerField(db_column="isCI",verbose_name="是否加入到持续集成  0 不加人  1加入",default=1)

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.ForeignKey(to=TbUser, to_field="loginName", related_name="TbTaskAddBy", on_delete=models.CASCADE, db_column='addBy', verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',default="", verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    addByName = models.CharField(max_length=25,db_column='addByName',default="", verbose_name="创建者姓名")
    modByName = models.CharField(max_length=25,db_column='modByName',default="", verbose_name="修改者姓名")


    class Meta:
        db_table = 'tb_task'
        verbose_name = '任务'
        verbose_name_plural = '11任务'

class TbTaskExecute(models.Model):
    taskId = models.CharField(db_column='taskId', max_length=100,verbose_name="要执行的任务ID")
    title = models.CharField(max_length=100,verbose_name="任务标题")
    taskdesc = models.CharField(max_length=1000,verbose_name="任务描述")
    protocol = models.CharField(max_length=20,verbose_name="任务协议")
    businessLineGroup = models.CharField(db_column='businessLineGroup', max_length=1000,verbose_name="任务包含的业务线名称，例如 SFA,服务云")
    modulesGroup = models.CharField(db_column='modulesGroup', max_length=1000,verbose_name="任务包含的模块名称，例如 合同,订单")
    sourceGroup = models.CharField(db_column='sourceGroup',default="['电脑Web']", max_length=1000, verbose_name="任务包含的来源名称，例如 IOS 安卓 Web端 所有")
    taskLevel = models.IntegerField(default=5,verbose_name="优先级，数字越小，优先级越高，从0-9。 0高 5中 9低",db_column="taskLevel")
    status = models.IntegerField(default=2,verbose_name="状态，1新建待审核 2审核通过 3审核未通过")
    highPriorityVARS = models.TextField(db_column='highPriorityVARS', default='', verbose_name="高优先级变量，执行时覆盖同名的变量和全局变量")  # release2 新增
    interfaceCount = models.IntegerField(db_column='interfaceCount',verbose_name="任务中的接口数量统计")
    taskInterfaces = models.TextField(db_column='taskInterfaces',verbose_name="任务中的接口列表，多个接口用,间隔，例如 HTTP_INTERFACE_1,HTTP_INTERFACE_2")
    caseCount = models.IntegerField(db_column='caseCount',verbose_name="任务中的用例数量统计")
    taskTestcases = models.TextField(db_column='taskTestcases',verbose_name="任务中的用例列表，多个接口用,间隔，例如 HTTP_TESTCASE_1,HTTP_TESTCASE_2")
    interfaceNum = models.IntegerField(db_column='interfaceNum',verbose_name="任务总的接口数量，包含接口的和用例中的步骤数量")
    isCI = models.IntegerField(db_column="isCI",verbose_name="是否加入到持续集成  0 不加人  1加入",default=1)

    caseLevel = models.IntegerField(db_column='caseLevel',default=100,verbose_name="执行时选择的执行优先级，如果选择了，那么只有同等优先级的case会执行，0高 5中 9低")
    httpConfKey = models.ForeignKey(to=TbConfigHttp, to_field="httpConfKey", db_column='httpConfKey', max_length=20,verbose_name="执行环境的httpConfKey")
    isSendEmail = models.IntegerField(db_column='isSendEmail',default=0,verbose_name="是否发送邮件[是否发送:是否带附件:PASS是否发送:FAIL是否发送:ERROR是否发送:EXCEPTION是否发送]0的时候不发送，1开头的时候依次往后判断即可后面没有的都是1，例如11标识发送带附件所有情况都发送10标识发送不带附件所有情况都发送100标识发送不带附件成功不发送其他情况发送")
    emailList = models.CharField(db_column='emailList', max_length=2000,default='',verbose_name="发送邮件列表，除却执行人execBy以外的其他收件人")#release2 新增
    isCodeRate = models.IntegerField(db_column='isCodeRate',default=0,verbose_name="是否生成代码覆盖率 1生成 0不生成")
    isSaveHistory = models.IntegerField(db_column='isSaveHistory',default=0,verbose_name="是否保存到历史记录 1保存 0不保存")
    execComments = models.CharField(db_column='execComments', max_length=400,verbose_name="执行备注信息")
    retryCount = models.IntegerField(db_column='retryCount', default=0,verbose_name="重试次数，默认0，不重试")
    execType = models.IntegerField(db_column='execType', blank=True, default=1,verbose_name="执行类型，1立即执行 2定时执行 3周期执行")
    execTime = models.DateTimeField(db_column='execTime',default="2000-01-01 00:00:01",verbose_name="执行开始时间，默认当前时间")
    execFinishTime = models.DateTimeField(db_column='execFinishTime',default="2000-01-01 00:00:01",verbose_name="执行结束时间")
    execTakeTime = models.IntegerField(db_column='execTakeTime',default=0,verbose_name="执行耗时")
    execBy = models.ForeignKey(to=TbUser, to_field="loginName", related_name="TbTaskExecuteExecBy",db_column='execBy', max_length=30, blank=True, default="", verbose_name="执行人登录用户名")
    execStatus = models.IntegerField(db_column='execStatus', default=1, verbose_name="执行状态: NOTRUN = 1 RUNNING = 2 DONE = 3 EXCEPTION = 4 CANCELING = 10 CANCELED = 11")
    execProgressData = models.CharField(db_column='execProgressData',default="0:0:0:0:0", max_length=30,verbose_name="执行进度数据，格式：ALL:PASS:FAIL:ERROR:NOTRUN，例如任务有10个用例，10:3:1:0:6,代表总共10个，通过3个，失败1个，错误0个，未执行6个。")
    execPlatform = models.IntegerField(db_column='execPlatform',default=1,verbose_name="调用接口的平台，1代表测试平台，2代表jenkins，100代表其他")
    execLevel = models.IntegerField(db_column='execLevel',default=5,verbose_name="优先级 5默认 数字越小优先级越高 范围1-10")
    testResult = models.CharField(db_column='testResult', max_length=20,default='NOTRUN',verbose_name="测试结果 根据断言结果生成的测试结果 PASS/FAIL/ERROR/EXCEPTION/CANCEL")
    testResultMsg = models.TextField(db_column='testResultMsg',verbose_name="任务执行的统计信息,详细统计，json字符串形式保存。")
    testReportUrl = models.CharField(db_column='testReportUrl', max_length=200,verbose_name="测试报告链接")
    performanceResult = models.CharField(db_column='performanceResult', max_length=20,default='N/A',verbose_name="性能测试结果 根据性能时间生成的测试结果 PASS/FAIL/  N/A")

    taskSuiteExecuteId = models.IntegerField(db_column='taskSuiteExecuteId', default='0',verbose_name="任务集执行Id")

    version = models.CharField(db_column='version', max_length=25,default='CurrentVersion',verbose_name="执行的版本")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.ForeignKey(to=TbUser, to_field="loginName", related_name="TbTaskExecuteAddBy", on_delete=models.CASCADE, db_column='addBy', verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',default="", verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    addByName = models.CharField(max_length=25, db_column='addByName', default="", verbose_name="创建者姓名")
    modByName = models.CharField(max_length=25, db_column='modByName', default="", verbose_name="修改者姓名")
    execByName = models.CharField(max_length=25, db_column='execByName', default="", verbose_name="执行者姓名")
    httpConfKeyAlias = models.CharField(max_length=200, db_column='httpConfKeyAlias',default="",  verbose_name="执行环境别名")

    class Meta:
        db_table = 'tb_task_execute'
        verbose_name = '任务执行'
        verbose_name_plural = '11任务执行'

class TbInterfaceExecuteHistory(models.Model):
    interfaceUrl = models.CharField(db_column='interfaceUrl', max_length=200, verbose_name="请求的接口URL")
    requestHost = models.CharField(db_column='requestHost', max_length=200, verbose_name="请求的主机地址，例如HTTP://test.domain.com")
    totalCount = models.IntegerField(db_column='totalCount', verbose_name="共执行次数统计")
    passCount = models.IntegerField(db_column='passCount', verbose_name="通过次数统计")
    failCount = models.IntegerField(db_column='failCount', verbose_name="失败次数统计")
    errorCount = models.IntegerField(db_column='errorCount', verbose_name="错误次数统计")
    exceptionCount = models.IntegerField(db_column='exceptionCount', verbose_name="异常次数统计")
    taskExecuteId = models.ForeignKey(to=TbTaskExecute,related_name="TbInterfaceExecuteHistoryTaskExecuteId",db_column='taskExecuteId', verbose_name="任务执行表的主键ID，关联哪次执行的任务")
    taskId = models.CharField(db_column='taskId', max_length=25, verbose_name="执行的任务ID")
    title = models.CharField(max_length=100, verbose_name="任务标题")
    taskdesc = models.CharField(max_length=1000, verbose_name="任务描述")
    protocol = models.CharField(max_length=20, verbose_name="任务协议")
    httpConfKey = models.ForeignKey(to=TbConfigHttp, to_field="httpConfKey", db_column='httpConfKey', max_length=20,verbose_name="执行环境的httpConfKey")
    # httpConfKey = models.CharField(db_column='httpConfKey', max_length=25, verbose_name="http服务的key，用例调试、任务执行时，会根据此key来获取对应的http的config信息")
    execBy = models.ForeignKey(to=TbUser,to_field="loginName",related_name="TbInterfaceExecuteHistoryExecBy",db_column='execBy', max_length=30, blank=True, default="", verbose_name="执行人登录用户名")
    testReportUrl = models.CharField(db_column='testReportUrl', max_length=200, verbose_name="报告路径")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.ForeignKey(to=TbUser, to_field="loginName", related_name="TbInterfaceExecuteHistoryAddBy", on_delete=models.CASCADE, db_column='addBy', verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_interface_execute_history'
        # unique_together = (('interfaceUrl', 'taskExecuteId'),)

class TbBatchTask(models.Model):
    businessLine = models.CharField(db_column="businessLine",verbose_name="业务线",max_length=200)
    httpConfKey = models.CharField(db_column='httpConfKey', max_length=20,verbose_name="执行环境的httpConfKey")
    taskLevel = models.IntegerField(db_column="taskLevel",default="9",verbose_name="任务优先级，0高，5中，9低")
    caseLevel = models.IntegerField(db_column="caseLevel",verbose_name="执行任务中case的优先级，0高，5中，9低")
    taskIdList = models.TextField(db_column="taskIdList",verbose_name="本次批量执行哪些任务")
    status = models.IntegerField(db_column="status",verbose_name="执行状态: NOTRUN = 1 RUNNING = 2 DONE = 3 EXCEPTION = 4 CANCELING = 10 CANCELED = 11")
    isSendEmail = models.IntegerField(db_column='isSendEmail', default=0,verbose_name="是否发送邮件[是否发送:是否带附件:PASS是否发送:FAIL是否发送:ERROR是否发送:EXCEPTION是否发送]0的时候不发送，1开头的时候依次往后判断即可后面没有的都是1，例如11标识发送带附件所有情况都发送10标识发送不带附件所有情况都发送100标识发送不带附件成功不发送其他情况发送")
    isCodeRate = models.IntegerField(db_column='isCodeRate', default=0, verbose_name="是否生成代码覆盖率 1生成 0不生成")
    isSaveHistory = models.IntegerField(db_column='isSaveHistory', default=0, verbose_name="是否保存到历史记录 1保存 0不保存")
    testResult = models.CharField(db_column='testResult', max_length=20,default='NOTRUN',verbose_name="测试结果 根据断言结果生成的测试结果 PASS/FAIL/ERROR/EXCEPTION/CANCEL")
    executeMsg = models.TextField(db_column='executeMsg',default='[]',verbose_name="测试过程中产生的信息")
    version = models.CharField(db_column='version', max_length=25,default='CurrentVersion',verbose_name="执行的版本")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25,db_column='addBy', verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")
    class Meta:
        db_table = 'tb_batch_execute_task'
        verbose_name = '任务批量执行'
        verbose_name_plural = '12任务批量执行'