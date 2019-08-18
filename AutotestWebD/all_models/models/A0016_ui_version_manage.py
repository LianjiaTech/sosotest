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
from all_models.models.A0011_version_manage import TbVersion

class TbUiVersionGlobalText(models.Model):
    versionName = models.CharField(db_column='versionName', max_length=25,default='CurrentVersion',verbose_name="执行的版本")

    textDesc = models.CharField(db_column='textDesc', max_length=5000, default="", verbose_name="详情")
    textKey = models.CharField(db_column='textKey', max_length=100, verbose_name="文本key,中英文数字下划线组合")
    textValue = models.TextField(db_column='textValue',  verbose_name="文本value")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', verbose_name="修改时间")

    class Meta:
        db_table = 'tb_ui_version_global_text'
        unique_together = ('versionName', 'textKey',)

class TbUiVersionGlobalVars(models.Model):
    versionName = models.CharField(db_column='versionName', max_length=25,default='CurrentVersion',verbose_name="执行的版本")

    varDesc = models.CharField(db_column='varDesc', max_length=5000, verbose_name="详情")
    varKey = models.CharField(db_column='varKey', max_length=100, verbose_name="全局变量key,中英文数字下划线组合")
    varValue = models.TextField(db_column='varValue',  verbose_name="全局变量value")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', verbose_name="修改时间")

    class Meta:
        db_table = 'tb_ui_version_global_vars'
        unique_together = ('versionName', 'varKey',)

class TbUiVersionTask(models.Model):
    versionName = models.CharField(db_column='versionName', max_length=25,default='CurrentVersion',verbose_name="执行的版本")

    taskId = models.CharField(db_column='taskId', max_length=25,verbose_name="任务ID")
    title = models.CharField(max_length=100,verbose_name="任务标题")
    taskdesc = models.CharField(max_length=1000,verbose_name="任务描述")
    businessLineGroup = models.CharField(db_column='businessLineGroup', max_length=1000,verbose_name="任务包含的业务线名称，例如 SFA,服务云")
    modulesGroup = models.CharField(db_column='modulesGroup', max_length=1000, verbose_name="任务包含的模块名称，例如 合同,订单")
    sourceGroup = models.CharField(db_column='sourceGroup',default="['电脑Web']", max_length=1000, verbose_name="任务包含的来源名称，例如 IOS 安卓 Web端 所有")
    tasklevel = models.IntegerField(default=5,verbose_name="优先级，数字越小，优先级越高，从0-9。 0高 5中 9低")
    status = models.IntegerField(default=2,verbose_name="状态，1新建待审核 2审核通过 3审核未通过")
    caseCount = models.IntegerField(db_column='caseCount',verbose_name="任务中的用例数量统计")
    taskTestcases = models.TextField(db_column='taskTestcases',verbose_name="任务中的用例列表，多个接口用,间隔，例如 UI_TESTCASE_1,UI_TESTCASE_2")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_ui_version_task'
        unique_together = ('versionName', 'taskId',)

class TbUiVersionTestCase(models.Model):
    versionName = models.CharField(db_column='versionName', max_length=25,default='CurrentVersion',verbose_name="执行的版本")

    caseId = models.CharField(db_column='caseId', default="", max_length=25, verbose_name="用例ID")
    title = models.CharField(max_length=100, verbose_name="用例标题")
    casedesc = models.CharField(max_length=1000, verbose_name="任务描述")
    businessLineId = models.IntegerField(db_column='businessLineId', default=1, verbose_name="业务线Id")
    moduleId = models.IntegerField(db_column='moduleId', default=1, verbose_name="模块Id")
    sourceId = models.IntegerField(db_column='sourceId', default=1, verbose_name="来源Id")
    caseLevel = models.IntegerField(db_column='caseLevel',default=5, verbose_name="优先级，数字越小，优先级越高，从0-9。 0高 5中 9低")

    status = models.IntegerField(default=2, verbose_name="状态，1新建待审核 2审核通过 3审核未通过")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_ui_version_testcase'

class TbUiVersionTestCaseStep(models.Model):
    versionName = models.CharField(db_column='versionName', max_length=25,default='CurrentVersion',verbose_name="执行的版本")

    caseId = models.CharField(db_column='caseId', default="", max_length=25, verbose_name="用例ID")

    stepNum = models.IntegerField(db_column='stepNum',default=1, verbose_name="步骤编号，一个用例是从1开始递增")
    stepTitle = models.CharField(db_column='stepTitle',  default="", max_length=200, verbose_name="标题")
    stepDesc = models.CharField(db_column='stepDesc',  default="", max_length=2000, verbose_name="描述")
    specialTag = models.CharField(db_column='specialTag', default="", max_length=25, verbose_name="特殊标记")
    operate = models.CharField(db_column='operate', default="", max_length=100, verbose_name="操作关键字")
    params = models.TextField(db_column='params', default="", verbose_name="参数")

    status = models.IntegerField(default=2, verbose_name="状态，1新建待审核 2审核通过 3审核未通过")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_ui_version_testcase_step'


class TbUiVersionPageObject(models.Model):
    versionName = models.CharField(db_column='versionName', max_length=25,default='CurrentVersion',verbose_name="执行的版本")

    poKey = models.CharField(db_column='poKey', max_length=100, verbose_name="PageObjectKey,中英文数字下划线组合")
    poTitle = models.CharField(db_column='poTitle', max_length=200, verbose_name="标题")
    poDesc = models.CharField(db_column='poDesc', max_length=5000, verbose_name="详情")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_ui_version_page_object'
        unique_together = (('versionName', 'poKey'),)

class TbUiVersionPageObjectElements(models.Model):
    versionName = models.CharField(db_column='versionName', max_length=25,default='CurrentVersion',verbose_name="执行的版本")

    poKey = models.CharField(db_column='poKey', max_length=100, verbose_name="PageObjectKey,中英文数字下划线组合")

    elementTitle = models.CharField(db_column='poTitle', max_length=200, verbose_name="标题")
    elementDesc = models.CharField(db_column='poDesc', max_length=5000, verbose_name="详情")

    elementKey = models.CharField(db_column='elementKey', max_length=100, verbose_name="PageObjectKey,中英文数字下划线组合")
    elementType = models.CharField(db_column='elementType', max_length=50, verbose_name="PageObjectKey,中英文数字下划线组合")
    elementValue = models.CharField(db_column='elementValue', max_length=5000, verbose_name="PageObjectKey,中英文数字下划线组合")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_ui_version_page_object_elements'
        unique_together = (('versionName','poKey', 'elementKey'),)

class TbUiVersionFunctions(models.Model):
    versionName = models.CharField(db_column='versionName', max_length=25,default='CurrentVersion',verbose_name="执行的版本")

    commonFuncKey = models.CharField(db_column='commonFuncKey', max_length=100, verbose_name="commonFuncKey,中英文数字下划线组合")
    commonFuncTitle = models.CharField(db_column='commonFuncTitle', max_length=500, verbose_name="标题")
    commonFuncDesc = models.CharField(db_column='commonFuncDesc', max_length=5000, verbose_name="描述")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_ui_version_functions'
        unique_together = (('versionName','commonFuncKey'),)

class TbUiVersionFunctionsTestcase(models.Model):
    versionName = models.CharField(db_column='versionName', max_length=25,default='CurrentVersion',verbose_name="执行的版本")

    commonFuncKey = models.CharField(db_column='commonFuncKey', max_length=100, verbose_name="commonFuncKey,中英文数字下划线组合")
    functionName = models.CharField(db_column='functionName', default="", max_length=25, verbose_name="funcName")

    title = models.CharField(max_length=100, verbose_name="用例标题")
    casedesc = models.CharField(max_length=1000, verbose_name="任务描述")
    businessLineId = models.IntegerField(db_column='businessLineId', default=1, verbose_name="业务线Id")
    moduleId = models.IntegerField(db_column='moduleId', default=1, verbose_name="模块Id")
    sourceId = models.IntegerField(db_column='sourceId', default=1, verbose_name="来源Id")
    caseLevel = models.IntegerField(db_column='caseLevel', default=5, verbose_name="优先级，数字越小，优先级越高，从0-9。 0高 5中 9低")

    status = models.IntegerField(default=2, verbose_name="状态，1新建待审核 2审核通过 3审核未通过")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_ui_version_functions_testcase'
        unique_together = (('versionName','commonFuncKey','functionName'),)

class TbUiVersionFunctionsTestcaseStep(models.Model):
    versionName = models.CharField(db_column='versionName', max_length=25,default='CurrentVersion',verbose_name="执行的版本")

    commonFuncKey = models.CharField(db_column='commonFuncKey', max_length=100, verbose_name="commonFuncKey,中英文数字下划线组合")
    functionName = models.CharField(db_column='functionName', default="", max_length=25, verbose_name="funcName")

    stepNum = models.IntegerField(db_column='stepNum',default=1, verbose_name="步骤编号，一个用例是从1开始递增")
    stepTitle = models.CharField(db_column='stepTitle',  default="", max_length=200, verbose_name="标题")
    stepDesc = models.CharField(db_column='stepDesc',  default="", max_length=2000, verbose_name="描述")
    specialTag = models.CharField(db_column='specialTag', default="", max_length=25, verbose_name="特殊标记")
    operate = models.CharField(db_column='operate', default="", max_length=100, verbose_name="操作关键字")
    params = models.TextField(db_column='params', default="", verbose_name="参数")

    status = models.IntegerField(default=2, verbose_name="状态，1新建待审核 2审核通过 3审核未通过")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_ui_version_functions_testcase_step'