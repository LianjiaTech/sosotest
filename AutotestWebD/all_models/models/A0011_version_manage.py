# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from all_models.models.A0001_user import *
from all_models.models.A0002_config import *
from all_models.models.A0003_attribute import *
from all_models.models.A0006_testcase import *
import django.utils.timezone
import datetime
class TbVersion(models.Model):
    versionName = models.CharField(db_column='versionName', unique=True, max_length=25, verbose_name="版本名称")
    versionDesc = models.TextField(db_column='versionDesc', verbose_name="版本描述")
    type_CHOICE = ((0, "废弃版本(封版数据已清理)"), (1, "历史版本(已封版)"), (2, "当前版本"), (3, "未启用版本(预留未启动)"),)
    type = models.IntegerField(default=3, verbose_name="类型", choices=type_CHOICE)
    closeTime = models.DateTimeField(db_column='closeTime', default=datetime.datetime(2018, 2, 23, 11, 24, 5, 219458),verbose_name="封板时间")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True,blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True,blank=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_version'
        verbose_name = '版本'
        verbose_name_plural = '50版本管理'

    def __str__(self):
        return self.versionName



class TbVersionGlobalText(models.Model):
    versionName = models.ForeignKey(to=TbVersion, to_field="versionName", related_name="TbVersionGlobalTextVersionName", on_delete=models.CASCADE, db_column='versionName', verbose_name="所属版本名称")

    textDesc = models.CharField(db_column='textDesc', max_length=5000, default="", verbose_name="详情")
    textKey = models.CharField(db_column='textKey', max_length=100, verbose_name="文本key,中英文数字下划线组合")
    textValue = models.TextField(db_column='textValue',  verbose_name="文本value")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.ForeignKey(to=TbUser, to_field="loginName", related_name="TbVersionGlobalTextAddBy", on_delete=models.CASCADE, db_column='addBy', verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', verbose_name="修改时间")

    class Meta:
        db_table = 'tb_version_global_text'
        unique_together = ('versionName', 'textKey',)

class TbVersionGlobalVars(models.Model):
    versionName = models.ForeignKey(to=TbVersion, to_field="versionName", related_name="TbVersionGlobalVarsVersionName", on_delete=models.CASCADE, db_column='versionName', verbose_name="所属版本名称")

    varDesc = models.CharField(db_column='varDesc', max_length=5000, verbose_name="详情")
    varKey = models.CharField(db_column='varKey', max_length=100, verbose_name="全局变量key,中英文数字下划线组合")
    varValue = models.TextField(db_column='varValue',  verbose_name="全局变量value")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.ForeignKey(to=TbUser, to_field="loginName", related_name="TbVersionGlobalVarsAddBy", on_delete=models.CASCADE, db_column='addBy', verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', verbose_name="修改时间")

    class Meta:
        db_table = 'tb_version_global_vars'
        unique_together = ('versionName', 'varKey',)


class TbVersionHttpInterface(models.Model):
    versionName = models.ForeignKey(to=TbVersion, to_field="versionName", related_name="TbVersionHttpInterfaceVersionName", on_delete=models.CASCADE, db_column='versionName', verbose_name="所属版本名称")

    interfaceId = models.CharField(db_column='interfaceId', max_length=25, verbose_name="接口ID，例如HTTP_INTERFACE_1")
    title = models.CharField(max_length=100, verbose_name="标题")
    casedesc = models.CharField(max_length=1000, verbose_name="描述")
    businessLineId = models.ForeignKey(to=TbBusinessLine, db_column='businessLineId', verbose_name="业务线ID")
    moduleId = models.ForeignKey(to=TbModules, db_column='moduleId', verbose_name="模块ID")
    sourceId = models.ForeignKey(to=TbSource, db_column='sourceId', verbose_name="来源ID", default=1)
    caselevel = models.IntegerField(default= 5, verbose_name="用例优先级，数字越小，优先级越高，从0-9。 0高 5中 9低")
    status = models.IntegerField(default=2, verbose_name="用例状态，1新建待审核 2审核通过 3审核未通过")
    caseType = models.IntegerField(default=2, verbose_name="用例类型，0测试用例，不计入统计，不进入任务，1 接口计入统计 2接口步骤均计入统计 3步骤计入统计")

    varsPre = models.TextField(db_column='varsPre', default="", verbose_name="前置变量")
    # dataInit = models.TextField(db_column='dataInit',default="", verbose_name="数据初始化信息")
    uri = models.CharField(max_length=50, verbose_name="HTTP请求的URI，http://domainORip,或者是 uri表中的key，比如apiUri等")
    method_CHOICE = (("POST", "POST"), ("GET", "GET"), ("PUT", "PUT"), ("PATCH", "PATCH"), ("DELETE", "DELETE"), ("HEAD", "HEAD"), ("OPTIONS", "OPTIONS"))
    method = models.CharField(max_length=20,default="POST" ,verbose_name="HTTP请求的method",choices=method_CHOICE)
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

    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效",choices=STATE_CHOICE)
    addBy = models.ForeignKey(to=TbUser, to_field="loginName", related_name="TbVersionHttpInterfaceAddBy", on_delete=models.CASCADE, db_column='addBy', verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', verbose_name="修改时间")


    class Meta:
        db_table = 'tb_version_http_interface'
        unique_together = ('versionName', 'interfaceId',)

class TbVersionHttpTestcase(models.Model):
    versionName = models.ForeignKey(to=TbVersion, to_field="versionName", related_name="TbVersionHttpTestcaseVersionName", on_delete=models.CASCADE, db_column='versionName', verbose_name="所属版本名称")

    caseId = models.CharField(db_column='caseId', max_length=25,verbose_name="caseId,可以理解为用例ID,格式HTTP_TESTCASE_1 - 99999999递增")
    title = models.CharField(max_length=100,verbose_name="用例标题")
    casedesc = models.CharField(max_length=1000,verbose_name="用例描述")
    businessLineId = models.ForeignKey(to=TbBusinessLine, db_column='businessLineId', verbose_name="业务线ID")
    moduleId = models.ForeignKey(to=TbModules, db_column='moduleId', verbose_name="模块ID")
    sourceId = models.ForeignKey(to=TbSource, db_column='sourceId', verbose_name="来源ID", default=1)
    caselevel = models.IntegerField(default=5, verbose_name="用例优先级，数字越小，优先级越高，从0-9。 0高 5中 9低")
    stepCount = models.IntegerField(db_column='stepCount',verbose_name="包含步骤数量")
    status = models.IntegerField(default=2, verbose_name="用例状态，1新建待审核 2审核通过 3审核未通过")
    caseType = models.IntegerField(default=2, verbose_name="用例类型，0测试用例，不计入统计，不进入任务，1 接口计入统计 2接口步骤均计入统计 3步骤计入统计")


    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.ForeignKey(to=TbUser, to_field="loginName", related_name="TbVersionHttpTestcaseAddBy", on_delete=models.CASCADE, db_column='addBy', verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', verbose_name="修改时间")

    class Meta:

        db_table = 'tb_version_http_testcase'
        unique_together = ('versionName', 'caseId',)

class TbVersionHttpTestcaseStep(models.Model):
    versionName = models.ForeignKey(to=TbVersion, to_field="versionName", related_name="TbVersionHttpTestcaseStepVersionName", on_delete=models.CASCADE, db_column='versionName', verbose_name="所属版本名称")

    caseId = models.CharField(db_column='caseId', default="",max_length=25,verbose_name="caseId,可以理解为用例ID,格式HTTP_TESTCASE_1 - 99999999递增")
    stepNum = models.IntegerField(db_column='stepNum', verbose_name="步骤编号，每个caseID中的有效编号是从1递增")

    title = models.CharField(max_length=100, verbose_name="步骤标题，默认 步骤1，步骤2 等等")
    stepDesc = models.CharField(db_column='stepDesc', max_length=1000, verbose_name="步骤描述")
    businessLineId = models.ForeignKey(to=TbBusinessLine, db_column='businessLineId', verbose_name="业务线ID")
    moduleId = models.ForeignKey(to=TbModules, db_column='moduleId', verbose_name="模块ID")
    sourceId = models.ForeignKey(to=TbSource, db_column='sourceId', verbose_name="来源ID", default=1)
    caseType = models.IntegerField(default=2, verbose_name="用例类型，0测试用例，不计入统计，不进入任务，1 接口计入统计 2接口步骤均计入统计 3步骤计入统计")

    fromInterfaceId = models.CharField(db_column="fromInterfaceId",default="",max_length=30,verbose_name="步骤引用的接口Id")
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

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.ForeignKey(to=TbUser, to_field="loginName", related_name="TbVersionHttpTestcaseStepAddBy", on_delete=models.CASCADE, db_column='addBy', verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', verbose_name="修改时间")

    class Meta:
        db_table = 'tb_version_http_testcase_step'
        unique_together = ('versionName', 'caseId','stepNum')

class TbVersionTask(models.Model):
    versionName = models.ForeignKey(to=TbVersion, to_field="versionName", related_name="TbVersionTaskVersionName", on_delete=models.CASCADE, db_column='versionName', verbose_name="所属版本名称")

    taskId = models.CharField(db_column='taskId', max_length=25,verbose_name="任务ID")
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
    addBy = models.ForeignKey(to=TbUser, to_field="loginName", related_name="TbVersionTaskAddBy", on_delete=models.CASCADE, db_column='addBy', verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', verbose_name="修改时间")

    class Meta:
        db_table = 'tb_version_task'
        unique_together = ('versionName', 'taskId',)

class TbVersionStandardInterface(models.Model):
    versionName = models.ForeignKey(to=TbVersion, to_field="versionName", related_name="TbVersionStandardInterfaceVersionName", on_delete=models.CASCADE, db_column='versionName', verbose_name="所属版本名称")

    #关联源文件
    businessLineId = models.ForeignKey(to=TbBusinessLine, db_column='businessLineId', verbose_name="业务线ID")
    moduleId = models.ForeignKey(to=TbModules, db_column='moduleId', verbose_name="模块ID")
    #解析结果
    fileName = models.CharField(db_column='fileName',max_length=3000,default="", verbose_name="文件名")
    # 解析出来的信息
    interfaceUrl = models.CharField(max_length=300,db_column='interfaceUrl',null = False,default="/", verbose_name="解析出的标准接口URL")
    interfaceCreateBy = models.CharField(max_length=100,db_column='interfaceCreateBy',null = False,default="暂时无法解析", verbose_name="创建者信息")
    interfaceCreateTime = models.DateTimeField(db_column='interfaceCreateTime',default="", verbose_name="创建时间")
    interfaceUpdateBy = models.CharField(max_length=100,db_column='interfaceUpdateBy',null = False,default="暂时无法解析", verbose_name="更新者信息")
    interfaceUpdateTime = models.DateTimeField(db_column='interfaceUpdateTime',default="", verbose_name="修改时间")
    authorEmail = models.CharField(max_length=200,db_column='authorEmail',default="暂时无法解析",verbose_name="作者邮箱（用于接收邮件）")
    apiStatus = models.IntegerField(default=1, verbose_name="状态 0废弃 1有效 3不存在接口 4apiStatus状态值错误")


    #通用信息
    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效",choices=STATE_CHOICE)
    addBy = models.ForeignKey(to=TbUser, to_field="loginName", related_name="TbVersionStandardInterfaceAddBy", on_delete=models.CASCADE, db_column='addBy', verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', verbose_name="修改时间")

    class Meta:
        db_table = 'tb_version_standard_interface'
        # unique_together = ('versionName', 'interfaceUrl',)



class TbVersionTaskSuite(models.Model):
    versionName = models.ForeignKey(to=TbVersion, to_field="versionName", related_name="TbVersionTaskSuiteVersionName", on_delete=models.CASCADE, db_column='versionName', verbose_name="所属版本名称")

    taskSuiteId = models.CharField(db_column='taskSuiteId', unique=True, max_length=25,verbose_name="任务ID")
    title = models.CharField(max_length=100,verbose_name="任务集标题",db_column="title")
    taskSuiteDesc = models.CharField(max_length=1000,verbose_name="任务集描述",db_column="taskSuiteDesc")
    protocol = models.CharField(max_length=20,verbose_name="任务集协议",db_column="protocol")
    emailList = models.CharField(db_column='emailList', max_length=2000,default='',verbose_name="发送邮件列表，除却执行人execBy以外的其他收件人")#release2 新增
    status = models.IntegerField(default=2,verbose_name="状态，1新建待审核 2审核通过 3审核未通过",db_column="status")
    taskCount = models.IntegerField(db_column='taskCount',verbose_name="任务集中的任务列表")
    taskList = models.TextField(db_column='taskList',verbose_name="任务集中的任务列表")
    isCI = models.IntegerField(db_column="isCI",verbose_name="是否加入到持续集成  0 不加人  1加入",default=0)

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效",db_column="state")
    addBy = models.CharField(max_length=25,db_column='addBy',null = True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_version_task_suite'
        verbose_name = '任务集'