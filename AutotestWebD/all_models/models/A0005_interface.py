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

class TbHttpInterface(models.Model):
    interfaceId = models.CharField(db_column='interfaceId', unique=True, max_length=25, verbose_name="接口ID，例如HTTP_INTERFACE_1")
    title = models.CharField(max_length=100, verbose_name="标题")
    casedesc = models.TextField(default="",verbose_name="描述")
    businessLineId = models.ForeignKey(to=TbBusinessLine, db_column='businessLineId', verbose_name="业务线ID")
    moduleId = models.ForeignKey(to=TbModules, db_column='moduleId', verbose_name="模块ID")
    sourceId = models.ForeignKey(to=TbSource, db_column='sourceId', verbose_name="来源ID", default=1)
    caselevel = models.IntegerField(default= 5, verbose_name="用例优先级，数字越小，优先级越高，从0-9。 0高 5中 9低")
    status = models.IntegerField(default=2, verbose_name="用例状态，1新建待审核 2审核通过 3审核未通过")
    caseType = models.IntegerField(default=2, verbose_name="用例类型，0测试用例，不计入统计，不进入任务，1 接口计入统计 2接口步骤均计入统计 3步骤计入统计")

    urlRedirect = models.IntegerField(db_column="urlRedirect",default=1,verbose_name="是否自动重定向")
    useCustomUri = models.IntegerField(db_column="useCustomUri",default=0,verbose_name="是否使用自定义请求地址")
    customUri = models.CharField(db_column="customUri",default="",max_length=200,verbose_name="自定义请求地址")
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
    performanceTime = models.FloatField(db_column="performanceTime",default=1,verbose_name="接口性能时间")

    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效",choices=STATE_CHOICE)
    addBy = models.ForeignKey(to=TbUser, to_field="loginName", related_name="TbHttpInterfaceAddBy", on_delete=models.CASCADE, db_column='addBy', verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")


    class Meta:
        db_table = 'tb_http_interface'

class TbHttpInterfaceDebug(models.Model):
    interfaceId = models.CharField(db_column='interfaceId', max_length=25, verbose_name="接口ID，例如HTTP_INTERFACE_1")

    title = models.CharField(max_length=100, verbose_name="标题")
    casedesc = models.TextField(default="",verbose_name="描述")
    businessLineId = models.ForeignKey(to=TbBusinessLine, db_column='businessLineId', verbose_name="业务线ID")
    moduleId = models.ForeignKey(to=TbModules, db_column='moduleId', verbose_name="模块ID")
    sourceId = models.ForeignKey(to=TbSource, db_column='sourceId', verbose_name="来源ID", default=1)
    caselevel = models.IntegerField(default= 5, verbose_name="用例优先级，数字越小，优先级越高，从0-9。 0高 5中 9低")
    status = models.IntegerField(default=2, verbose_name="用例状态，1新建待审核 2审核通过 3审核未通过")
    caseType = models.IntegerField(default=2, verbose_name="用例类型，0测试用例，不计入统计，不进入任务，1 接口计入统计 2接口步骤均计入统计 3步骤计入统计")

    varsPre = models.TextField(db_column='varsPre', default="", verbose_name="前置变量")
    # dataInit = models.TextField(db_column='dataInit',default="", verbose_name="数据初始化信息")
    uri = models.CharField(max_length=50, verbose_name="HTTP请求的URI，http://domainORip,或者是 uri表中的key，比如apiUri等")
    method = models.CharField(max_length=20,default="POST" ,verbose_name="HTTP请求的method")
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
    addBy = models.ForeignKey(to=TbUser, to_field="loginName", related_name="TbHttpInterfaceDebugAddBy", on_delete=models.CASCADE, db_column='addBy', verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_http_interface_debug'
        verbose_name = '接口调试'
        verbose_name_plural = '09接口调试'

class TbHttpInterfaceTag(models.Model):
    interfaceId = models.ForeignKey(to=TbHttpInterface,to_field="interfaceId",db_column='interfaceId', max_length=25, verbose_name="接口ID")
    tagId = models.ForeignKey(to=TbTag,db_column='tagId', max_length=25, verbose_name="tag表中的主键id")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.ForeignKey(to=TbUser, to_field="loginName", related_name="TbHttpInterfaceTagAddBy", on_delete=models.CASCADE, db_column='addBy', verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_http_interface_tag'
        unique_together = (('interfaceId', 'tagId'),)
