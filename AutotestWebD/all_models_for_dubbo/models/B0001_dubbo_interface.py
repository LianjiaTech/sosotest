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

class Tb2DubboInterface(models.Model):
    interfaceId = models.CharField(db_column='interfaceId', unique=True, max_length=25, verbose_name="接口ID，例如DUBBO_INTERFACE_1")
    title = models.CharField(max_length=100, verbose_name="标题")
    casedesc = models.TextField(default="",verbose_name="描述")
    businessLineId = models.ForeignKey(to=TbBusinessLine, db_column='businessLineId', verbose_name="业务线ID")
    moduleId = models.ForeignKey(to=TbModules, db_column='moduleId', verbose_name="模块ID")
    caselevel = models.IntegerField(default= 5, verbose_name="用例优先级，数字越小，优先级越高，从0-9。 0高 5中 9低")
    status = models.IntegerField(default=2, verbose_name="用例状态，1新建待审核 2审核通过 3审核未通过")
    caseType = models.IntegerField(default=2, verbose_name="用例类型，0测试用例，不计入统计，不进入任务，1 接口计入统计 2接口步骤均计入统计 3步骤计入统计")

    varsPre = models.TextField(db_column='varsPre', default="", verbose_name="前置变量")
    # dataInit = models.TextField(db_column='dataInit',default="", verbose_name="数据初始化信息")
    useCustomUri = models.IntegerField(db_column="useCustomUri", default=0, verbose_name="是否使用自定义请求地址")
    customUri = models.CharField(db_column="customUri", default="", max_length=200, verbose_name="自定义请求地址")
    dubboSystem = models.CharField(max_length=100,db_column='dubboSystem', verbose_name="dubbo的project名称，比如testproject")
    dubboService = models.CharField(max_length=200,db_column='dubboService',  verbose_name="dubbo的service全路径，比如com.xxx.xxxx.XxxxxFacade")
    dubboMethod = models.CharField(max_length=100,db_column='dubboMethod',  verbose_name="dubbo的service中的具体method")
    dubboParams = models.TextField(verbose_name="Dubbo invoke时请求的参数,多个params中间用半角逗号间隔")
    encoding = models.CharField(max_length=10,db_column='encoding',default="gb18030",  verbose_name="dubbo的service中的编码方式")

    timeout = models.IntegerField(default=20, verbose_name="超时时间，单位秒")
    varsPost = models.TextField(db_column='varsPost', verbose_name="后置变量")
    # expectResult = models.TextField(db_column='expectResult', verbose_name="预期结果")
    # dataRecover = models.TextField(db_column='dataRecover', verbose_name="数据恢复信息")

    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效",choices=STATE_CHOICE)
    addBy = models.ForeignKey(to=TbUser, to_field="loginName", related_name="Tb2DubboInterfaceAddBy", on_delete=models.CASCADE, db_column='addBy', verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")


    class Meta:
        db_table = 'tb2_dubbo_interface'

class Tb2DubboInterfaceDebug(models.Model):
    interfaceId = models.CharField(db_column='interfaceId', max_length=25, verbose_name="接口ID，例如DUBBO_INTERFACE_1")
    title = models.CharField(max_length=100, verbose_name="标题")
    casedesc = models.TextField(default="",verbose_name="描述")
    businessLineId = models.ForeignKey(to=TbBusinessLine, db_column='businessLineId', verbose_name="业务线ID")
    moduleId = models.ForeignKey(to=TbModules, db_column='moduleId', verbose_name="模块ID")
    caselevel = models.IntegerField(default= 5, verbose_name="用例优先级，数字越小，优先级越高，从0-9。 0高 5中 9低")
    status = models.IntegerField(default=2, verbose_name="用例状态，1新建待审核 2审核通过 3审核未通过")
    caseType = models.IntegerField(default=2, verbose_name="用例类型，0测试用例，不计入统计，不进入任务，1 接口计入统计 2接口步骤均计入统计 3步骤计入统计")

    varsPre = models.TextField(db_column='varsPre', default="", verbose_name="前置变量")
    # dataInit = models.TextField(db_column='dataInit',default="", verbose_name="数据初始化信息")
    useCustomUri = models.IntegerField(db_column="useCustomUri", default=0, verbose_name="是否使用自定义请求地址")
    customUri = models.CharField(db_column="customUri", default="", max_length=200, verbose_name="自定义请求地址")
    dubboSystem = models.CharField(max_length=100,db_column='dubboSystem', verbose_name="dubbo的project名称，比如testproject")
    dubboService = models.CharField(max_length=200,db_column='dubboService',  verbose_name="dubbo的service全路径，比如com.xxx.xxxx.XxxxxFacade")
    dubboMethod = models.CharField(max_length=100,db_column='dubboMethod',  verbose_name="dubbo的service中的具体method")
    dubboParams = models.TextField(verbose_name="Dubbo invoke时请求的参数,多个params中间用半角逗号间隔")
    encoding = models.CharField(max_length=10,db_column='encoding',default="gb18030",  verbose_name="dubbo的service中的编码方式")

    timeout = models.IntegerField(default=20, verbose_name="超时时间，单位秒")
    varsPost = models.TextField(db_column='varsPost', verbose_name="后置变量")
    # expectResult = models.TextField(db_column='expectResult', verbose_name="预期结果")
    # dataRecover = models.TextField(db_column='dataRecover', verbose_name="数据恢复信息")

    execStatus = models.IntegerField(db_column='execStatus', default=1, verbose_name="执行状态")
    httpConfKey = models.ForeignKey(to=TbConfigHttp, to_field="httpConfKey", db_column='httpConfKey', max_length=20,verbose_name="执行环境的httpConfKey")
    actualResult = models.TextField(db_column='actualResult', blank=True, default="", verbose_name="实际结果")
    assertResult = models.TextField(db_column='assertResult', blank=True, default="", verbose_name="断言结果")
    testResult = models.CharField(db_column='testResult', max_length=20, default='NOTRUN', verbose_name="执行结果")
    beforeExecuteTakeTime = models.IntegerField(db_column='beforeExecuteTakeTime', default=0, verbose_name="执行前耗时")
    afterExecuteTakeTime = models.IntegerField(db_column='afterExecuteTakeTime', default=0, verbose_name="执行后耗时")
    executeTakeTime = models.IntegerField(db_column='executeTakeTime', default=0, verbose_name="执行耗时")
    totalTakeTime = models.IntegerField(db_column='totalTakeTime', default=0, verbose_name="总耗时")

    version = models.CharField(db_column='version', max_length=25, default='CurrentVersion', verbose_name="执行的版本")

    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效",choices=STATE_CHOICE)
    addBy = models.ForeignKey(to=TbUser, to_field="loginName", related_name="Tb2DubboInterfaceDebugAddBy", on_delete=models.CASCADE, db_column='addBy', verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")


    class Meta:
        db_table = 'tb2_dubbo_interface_debug'

class Tb2DubboQuickDebug(models.Model):
    requestAddr = models.CharField(max_length=200,db_column='requestAddr',  verbose_name="快速调试的请求地址")
    dubboService = models.CharField(max_length=200,db_column='dubboService',  verbose_name="dubbo的service全路径，比如com.xxx.xxxx.XxxxxFacade")
    dubboMethod = models.CharField(max_length=100,db_column='dubboMethod',  verbose_name="dubbo的service中的具体method")
    dubboParams = models.TextField(verbose_name="Dubbo invoke时请求的参数,多个params中间用半角逗号间隔")
    encoding = models.CharField(max_length=10,db_column='encoding',default="gb18030",  verbose_name="dubbo的service中的编码方式")

    actualResult = models.TextField(db_column='actualResult', blank=True, default="", verbose_name="实际结果")
    executeTakeTime = models.IntegerField(db_column='executeTakeTime', default=0, verbose_name="执行耗时")

    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效",choices=STATE_CHOICE)
    addBy = models.CharField(max_length=25,db_column='addBy',null = True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb2_dubbo_quick_debug'
