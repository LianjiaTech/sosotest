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

class TbHttpTestcase(models.Model):
    caseId = models.CharField(db_column='caseId', unique=True, max_length=25,verbose_name="caseId,可以理解为用例ID,格式HTTP_TESTCASE_1 - 99999999递增")
    title = models.CharField(max_length=100,verbose_name="用例标题")
    casedesc = models.TextField(default="",verbose_name="描述")
    businessLineId = models.ForeignKey(to=TbBusinessLine, db_column='businessLineId', verbose_name="业务线ID")
    moduleId = models.ForeignKey(to=TbModules, db_column='moduleId', verbose_name="模块ID")
    sourceId = models.ForeignKey(to=TbSource, db_column='sourceId', verbose_name="来源ID", default=1)
    caselevel = models.IntegerField(default=5, verbose_name="用例优先级，数字越小，优先级越高，从0-9。 0高 5中 9低")
    stepCount = models.IntegerField(db_column='stepCount',verbose_name="包含步骤数量")
    status = models.IntegerField(default=2, verbose_name="用例状态，1新建待审核 2审核通过 3审核未通过")
    caseType = models.IntegerField(default=2, verbose_name="用例类型，0测试用例，不计入统计，不进入任务，1 接口计入统计 2接口步骤均计入统计 3步骤计入统计")


    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.ForeignKey(to=TbUser, to_field="loginName", related_name="TbHttpTestcaseAddBy", on_delete=models.CASCADE, db_column='addBy', verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:

        db_table = 'tb_http_testcase'

class TbHttpTestcaseDebug(models.Model):
    caseId = models.CharField(db_column='caseId', max_length=25,verbose_name="caseId,可以理解为用例ID,格式HTTP_TESTCASE_1 - 99999999递增")
    title = models.CharField(max_length=100,verbose_name="用例标题")
    casedesc = models.TextField(default="",verbose_name="描述")
    businessLineId = models.ForeignKey(to=TbBusinessLine, db_column='businessLineId', verbose_name="业务线ID")
    moduleId = models.ForeignKey(to=TbModules, db_column='moduleId', verbose_name="模块ID")
    sourceId = models.ForeignKey(to=TbSource, db_column='sourceId', verbose_name="来源ID", default=1)
    caselevel = models.IntegerField(default=5, verbose_name="用例优先级，数字越小，优先级越高，从0-9。 0高 5中 9低")
    stepCount = models.IntegerField(db_column='stepCount',verbose_name="包含步骤数量")
    status = models.IntegerField(default=2, verbose_name="用例状态，1新建待审核 2审核通过 3审核未通过")
    caseType = models.IntegerField(default=2, verbose_name="用例类型，0测试用例，不计入统计，不进入任务，1 接口计入统计 2接口步骤均计入统计 3步骤计入统计")

    execStatus = models.IntegerField(db_column='execStatus',default=1,verbose_name="执行状态: NOTRUN = 1 RUNNING = 2 DONE = 3 EXCEPTION = 4")
    httpConfKey = models.ForeignKey(to=TbConfigHttp, to_field="httpConfKey", db_column='httpConfKey', max_length=20, verbose_name="执行环境的httpConfKey")
    assertResult = models.TextField(db_column='assertResult', blank=True, default="", verbose_name="断言结果")
    testResult = models.CharField(db_column='testResult', max_length=20, default='NOTRUN', verbose_name="执行结果")
    beforeExecuteTakeTime = models.IntegerField(db_column='beforeExecuteTakeTime', default=0, verbose_name="执行前耗时")
    afterExecuteTakeTime = models.IntegerField(db_column='afterExecuteTakeTime', default=0, verbose_name="执行后耗时")
    executeTakeTime = models.IntegerField(db_column='executeTakeTime', default=0, verbose_name="执行耗时")
    totalTakeTime = models.IntegerField(db_column='totalTakeTime', default=0, verbose_name="总耗时")

    version = models.CharField(db_column='version', max_length=25,default='CurrentVersion',verbose_name="执行的版本")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.ForeignKey(to=TbUser, to_field="loginName", related_name="TbHttpTestcaseDebugAddBy", on_delete=models.CASCADE, db_column='addBy', verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_http_testcase_debug'
        verbose_name = '用例调试'
        verbose_name_plural = '09用例调试'

class TbHttpTestcaseStep(models.Model):
    caseId = models.ForeignKey(to=TbHttpTestcase,to_field="caseId",db_column='caseId', max_length=25, verbose_name="TbHttpTestcase表中的caseID")
    stepNum = models.IntegerField(db_column='stepNum', verbose_name="步骤编号，每个caseID中的有效编号是从1递增")

    title = models.CharField(max_length=100, verbose_name="步骤标题，默认 步骤1，步骤2 等等")
    stepDesc = models.TextField(default="",verbose_name="描述")
    businessLineId = models.ForeignKey(to=TbBusinessLine, db_column='businessLineId', verbose_name="业务线ID")
    moduleId = models.ForeignKey(to=TbModules, db_column='moduleId', verbose_name="模块ID")
    sourceId = models.ForeignKey(to=TbSource, db_column='sourceId', verbose_name="来源ID", default=1)
    caseType = models.IntegerField(default=2, verbose_name="用例类型，0测试用例，不计入统计，不进入任务，1 接口计入统计 2接口步骤均计入统计 3步骤计入统计")

    fromInterfaceId = models.CharField(db_column="fromInterfaceId",default="",max_length=30,verbose_name="步骤引用的接口Id")
    isSync_CHOICE = ((0, "不同步"), (1, "同步"),)
    isSync = models.IntegerField(default=0, verbose_name="是否同步", choices=isSync_CHOICE)

    urlRedirect = models.IntegerField(db_column="urlRedirect",default=1,verbose_name="是否自动重定向")
    useCustomUri = models.IntegerField(db_column="useCustomUri",default=0,verbose_name="是否使用自定义请求地址")
    customUri = models.CharField(db_column="customUri",default="",max_length=200,verbose_name="自定义请求地址")
    stepSwitch = models.IntegerField(db_column="stepSwitch",default=1,verbose_name="此步骤是否勾选执行")
    varsPre = models.TextField(db_column='varsPre', verbose_name="前置变量")
    # dataInit = models.TextField(db_column='dataInit', verbose_name="数据初始化信息")
    uri = models.CharField(max_length=50, verbose_name="HTTP请求的URI，http://domainORip,或者是 uri表中的key，比如apiUri等")
    method = models.CharField(max_length=20, default="POST", verbose_name="HTTP请求的method")
    header = models.TextField(verbose_name="HTTP请求的头信息，json格式")
    url = models.CharField(max_length=250, verbose_name="HTTP请求的URL，也就是接口路径")
    params = models.TextField(verbose_name="HTTP请求的参数，urlencode格式或者json格式")
    bodyType_CHOICE = (("form-data", "表单提交"), ("x-www-form-urlencoded", "urlencode模式"), ("raw", "源提交，例如application/json等"), ("binary", "单文件上传"), ("", "GET、head时无请求体"))
    bodyType = models.CharField(db_column='bodyType', max_length=200, verbose_name="请求体类型",choices=bodyType_CHOICE,default="")
    bodyContent = models.TextField(db_column='bodyContent', verbose_name="请求体内容，字符串或者json",default="")
    timeout = models.IntegerField(default=20, verbose_name="超时时间，单位秒")
    varsPost = models.TextField(db_column='varsPost', verbose_name="后置变量")
    # expectResult = models.TextField(db_column='expectResult', verbose_name="预期结果")
    # dataRecover = models.TextField(db_column='dataRecover', verbose_name="数据恢复信息")
    performanceTime = models.FloatField(db_column="performanceTime", default=1, verbose_name="接口性能时间")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.ForeignKey(to=TbUser, to_field="loginName", related_name="TbHttpTestcaseStepAddBy", on_delete=models.CASCADE, db_column='addBy', verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_http_testcase_step'
        unique_together = (('caseId', 'stepNum'),)

class TbHttpTestcaseStepDebug(models.Model):
    caseId = models.CharField(db_column='caseId', max_length=25,verbose_name="caseId,可以理解为用例ID,格式HTTP_TESTCASE_1 - 99999999递增")
    stepNum = models.IntegerField(db_column='stepNum', verbose_name="步骤编号，每个caseID中的有效编号是从1递增")

    title = models.CharField(max_length=100, verbose_name="步骤标题，默认 步骤1，步骤2 等等")
    stepDesc = models.TextField(default="",verbose_name="描述")
    businessLineId = models.ForeignKey(to=TbBusinessLine, db_column='businessLineId', verbose_name="业务线ID")
    moduleId = models.ForeignKey(to=TbModules, db_column='moduleId', verbose_name="模块ID")
    sourceId = models.ForeignKey(to=TbSource, db_column='sourceId', verbose_name="来源ID", default=1)
    caseType = models.IntegerField(default=2, verbose_name="用例类型，0测试用例，不计入统计，不进入任务，1 接口计入统计 2接口步骤均计入统计 3步骤计入统计")

    fromInterfaceId = models.CharField(db_column="fromInterfaceId",default="", max_length=30, verbose_name="步骤引用的接口Id")
    isSync_CHOICE = ((0, "不同步"), (1, "同步"),)
    isSync = models.IntegerField(default=0, verbose_name="是否同步", choices=isSync_CHOICE)

    varsPre = models.TextField(db_column='varsPre', verbose_name="前置变量")
    # dataInit = models.TextField(db_column='dataInit', verbose_name="数据初始化信息")
    uri = models.CharField(max_length=50, verbose_name="HTTP请求的URI，http://domainORip,或者是 uri表中的key，比如apiUri等")
    method = models.CharField(max_length=20, default="POST", verbose_name="HTTP请求的method")
    header = models.TextField(verbose_name="HTTP请求的头信息，json格式")
    url = models.CharField(max_length=250, verbose_name="HTTP请求的URL，也就是接口路径")
    params = models.TextField(verbose_name="HTTP请求的参数，urlencode格式或者json格式")
    bodyType_CHOICE = (("form-data", "表单提交"), ("x-www-form-urlencoded", "urlencode模式"), ("raw", "源提交，例如application/json等"), ("binary", "单文件上传"), ("", "GET、head时无请求体"))
    bodyType = models.CharField(db_column='bodyType', max_length=200, verbose_name="请求体类型",choices=bodyType_CHOICE,default="")
    bodyContent = models.TextField(db_column='bodyContent', verbose_name="请求体内容，字符串或者json",default="")
    timeout = models.IntegerField(default=20, verbose_name="超时时间，单位秒")
    varsPost = models.TextField(db_column='varsPost', verbose_name="后置变量")
    # expectResult = models.TextField(db_column='expectResult', verbose_name="预期结果")
    # dataRecover = models.TextField(db_column='dataRecover', verbose_name="数据恢复信息")
    performanceTime = models.FloatField(db_column="performanceTime", default=1, verbose_name="接口性能时间")

    execStatus = models.IntegerField(db_column='execStatus',default=1,verbose_name="执行状态")
    httpConfKey = models.ForeignKey(to=TbConfigHttp,to_field="httpConfKey",db_column='httpConfKey', max_length=20,verbose_name="执行环境的httpConfKey")
    actualResult = models.TextField(db_column='actualResult', blank=True, default="",verbose_name="实际结果")
    assertResult = models.TextField(db_column='assertResult', blank=True, default="",verbose_name="断言结果")
    testResult = models.CharField(db_column='testResult', max_length=20,default='NOTRUN',verbose_name="执行结果")
    beforeExecuteTakeTime = models.IntegerField(db_column='beforeExecuteTakeTime',default=0,verbose_name="执行前耗时")
    afterExecuteTakeTime = models.IntegerField(db_column='afterExecuteTakeTime',default=0,verbose_name="执行后耗时")
    executeTakeTime = models.IntegerField(db_column='executeTakeTime',default=0,verbose_name="执行耗时")
    totalTakeTime = models.IntegerField(db_column='totalTakeTime',default=0,verbose_name="总耗时")

    version = models.CharField(db_column='version', max_length=25,default='CurrentVersion',verbose_name="执行的版本")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.ForeignKey(to=TbUser, to_field="loginName", related_name="TbHttpTestcaseStepDebugAddBy", on_delete=models.CASCADE, db_column='addBy', verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_http_testcase_step_debug'
        verbose_name = '用例步骤调试'
        verbose_name_plural = '10用例步骤调试'

class TbHttpTestcaseTag(models.Model):
    caseId = models.ForeignKey(to=TbHttpTestcase, to_field="caseId", db_column='caseId', max_length=25,verbose_name="TbHttpTestcase表中的caseID")
    tagId = models.ForeignKey(to=TbTag, db_column='tagId', max_length=25, verbose_name="tag表中的主键id")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.ForeignKey(to=TbUser, to_field="loginName", related_name="TbHttpTestcaseTagAddBy", on_delete=models.CASCADE, db_column='addBy', verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_http_testcase_tag'
        unique_together = (('caseId', 'tagId'),)
