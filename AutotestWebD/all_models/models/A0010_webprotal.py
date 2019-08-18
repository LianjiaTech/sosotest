# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

import datetime
from django.db import models
from all_models.models.A0001_user import *
from all_models.models.A0003_attribute import *
import django.utils.timezone as timezone

#action概况
class TbWebPortalActionInterfaceGeneralSituation(models.Model):
    statisticalDetail = models.TextField(db_column="statisticalDetail",verbose_name="统计详情")
    # standardInterfaceNum = models.IntegerField(db_column='standardInterfaceNum',  verbose_name = "接口总数")
    # platformCoveredStandardNum = models.IntegerField(db_column='platformCoveredStandardNum', verbose_name = "已覆盖接口数")
    # platformCoverage = models.FloatField(db_column="platformCoverage",verbose_name="接口覆盖率")
    #
    # executeInterfaceNum = models.IntegerField(db_column='executeInterfaceNum', verbose_name = "已执行接口数")
    # executeInterfaceCoverage = models.FloatField(db_column="executeInterfaceCoverage",verbose_name="用例执行接口覆盖率")
    #
    # platformInterfaceNum = models.IntegerField(db_column="platformInterfaceNum",verbose_name="用例总数")
    # platformInterfaceAverageStandardInterface = models.FloatField(db_column="platformInterfaceAverageStandardInterface",verbose_name="用例平均数")
    #
    # executeInterfaceSum = models.IntegerField(db_column='executeInterfaceSum', verbose_name = "已执行接口总数")
    # executeInterfaceAverage = models.FloatField(db_column='executeInterfaceAverage', verbose_name = "执行用例平均数")
    #
    # testCaseNum = models.IntegerField(db_column='testCaseNum', verbose_name = "场景总数")
    # executeTestCaseNum = models.IntegerField(db_column='executeTestCaseNum', verbose_name = "已执行的场景数量")
    version = models.CharField(db_column="version",max_length=200,verbose_name="版本",default="v1801")

    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效",choices=STATE_CHOICE)
    #统计时间
    statisticalTime = models.DateTimeField(db_column="statisticalTime",default="2018-02-01 00:00:00",verbose_name="统计时间")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True,blank=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True,blank=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_webPortal_action_interface_general_situation'

class TbWebPortalActionInterfaceTest(models.Model):
    businessLine = models.CharField(db_column='businessLine',  max_length=200,verbose_name = "业务线")
    envTestDetail = models.TextField(db_column='envTestDetail',  verbose_name = "多环境测试结果")
    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效",choices=STATE_CHOICE)
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True,blank=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True,blank=True, verbose_name="修改时间")
    #统计时间
    statisticalTime = models.DateTimeField(db_column="statisticalTime",default="2018-02-01 00:00:00",verbose_name="统计时间")
    class Meta:
        db_table = 'tb_webPortal_action_interface_test'

class TbWebPortalPlatformInterfaceCovered(models.Model):
    businessLine = models.CharField(db_column="businessLine",max_length=200,verbose_name="业务线")
    standardInterfaceNum = models.IntegerField(db_column="standardInterfaceNum",verbose_name="标准接口数量")
    coveredInterfaceNum = models.IntegerField(db_column="coveredInterfaceNum",verbose_name="已覆盖接口数量")
    coverage = models.FloatField(db_column="coverage",verbose_name="覆盖率")
    executeInterfaceNum = models.IntegerField(db_column="executeInterfaceNum",verbose_name="已执行接口数")
    executeInterfaceCoverage = models.FloatField(db_column="executeInterfaceCoverage", verbose_name="用例执行接口覆盖率")
    interfaceNum = models.IntegerField(db_column="interfaceNum", verbose_name="用例总数")
    executeInterfaceSum = models.IntegerField(db_column="executeInterfaceSum", verbose_name="执行用例总数")
    testCaseSum = models.IntegerField(db_column="testCaseSum", verbose_name="场景总数")
    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效",choices=STATE_CHOICE)
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True,blank=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True,blank=True, verbose_name="修改时间")
    #统计时间
    statisticalTime = models.DateTimeField(db_column="statisticalTime",default="2018-02-01 00:00:00",verbose_name="统计时间")
    version = models.CharField(db_column="version", max_length=200, verbose_name="版本", default="v1801")
    class Meta:
        db_table = 'tb_webPortal_platform_interface_covered'

#标准任务表
class TbWebPortalTask(models.Model):
    businessLine = models.CharField(db_column="businessLine",max_length=200,verbose_name="业务线")
    team = models.CharField(db_column="team",max_length=200,verbose_name="小组")
    head = models.CharField(db_column="head",max_length=200,verbose_name="负责人")
    taskId = models.CharField(db_column="task",max_length=200,verbose_name="任务")

    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效", choices=STATE_CHOICE)
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, blank=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, blank=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_webPortal_task'
        verbose_name = '标准任务'
        verbose_name_plural = '20标准任务管理'

#通过率环境
class TbWebPortalPassingRateEnv(models.Model):
    httpConfKey = models.CharField(db_column='httpConfKey', unique=True, max_length=50,verbose_name="http服务的key，用例调试、任务执行时，会根据此key来获取对应的http的config信息")
    openApiKey = models.CharField(db_column='openApiKey', max_length=50,verbose_name="openApi服务的key，用例调试、任务执行时，会根据此key来获取对应的http的config信息")
    rmiKey = models.CharField(db_column='rmiKey', max_length=50,verbose_name="rmi服务的key，用例调试、任务执行时，会根据此key来获取对应的http的config信息")
    alias = models.CharField(db_column="alias",unique=True, max_length=200, verbose_name="别名")
    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效", choices=STATE_CHOICE)
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, blank=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, blank=True, verbose_name="修改时间")
    #统计时间
    statisticalTime = models.DateTimeField(db_column="statisticalTime",default=datetime.datetime(2018, 2, 23, 11, 24, 5, 219458),verbose_name="统计时间")
    class Meta:
        db_table = 'tb_webPortal_passingRate_Env'
        verbose_name = '通过率环境配置'
        verbose_name_plural = '21通过率环境配置管理'

class TbWebPortOpenApiGeneralSituation(models.Model):
    interfaceSum = models.IntegerField(db_column="interfaceSum",verbose_name="接口总数")
    covered = models.IntegerField(db_column="covered",verbose_name="覆盖的接口的总数")
    coveredRate = models.FloatField(db_column="coveredRate",verbose_name="接口覆盖率")
    total = models.IntegerField(db_column="total",verbose_name="测试用例总数")
    executedRate = models.IntegerField(db_column="executedRate",verbose_name="测试用例执行率，这里目前都是100%执行")
    profile = models.CharField(db_column="profile", max_length=200, verbose_name="测试环境")
    averageInterfaceNum = models.CharField(db_column="averageInterfaceNum",max_length=200,verbose_name="平均接口用例数")
    testBeginTime = models.DateTimeField(db_column="testBeginTime",verbose_name="测试开始时间")
    testEndTime = models.DateTimeField(db_column="testEnfTime",verbose_name="测试结束时间")
    statisticalTime = models.DateTimeField(db_column="statisticalTime", default="2018-02-01 00:00:00", verbose_name="统计时间")
    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效", choices=STATE_CHOICE)
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, blank=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, blank=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_webPortal_openApi_general_situation'

class TbWebPortOpenApiInterfaceTest(models.Model):
    businessLine = models.CharField(db_column="businessLine",max_length=200,verbose_name="业务线")
    interfaceDetail = models.TextField(db_column="interfaceDetail",verbose_name="多环境测试详情")
    statisticalTime = models.DateTimeField(db_column="statisticalTime", default="2018-02-01 00:00:00", verbose_name="统计时间")
    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效", choices=STATE_CHOICE)
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, blank=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, blank=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_webPortal_openApi_interface_test'


class TbWebPortOpenApiBlTest(models.Model):
    interfaceSum = models.IntegerField(db_column="interfaceSum",verbose_name="接口总数")
    covered = models.IntegerField(db_column="covered",verbose_name="覆盖的接口的总数")
    coveredRate = models.FloatField(db_column="coveredRate",verbose_name="接口覆盖率")
    total = models.IntegerField(db_column="total",verbose_name="测试用例总数")
    executedRate = models.IntegerField(db_column="executedRate",verbose_name="测试用例执行率，这里目前都是100%执行")
    profile = models.CharField(db_column="profile",max_length=200,verbose_name="测试环境")
    businessLine = models.CharField(db_column="businessLine",max_length=200,verbose_name="openapi业务线")
    testBeginTime = models.DateTimeField(db_column="testBeginTime",verbose_name="测试开始时间")
    testEndTime = models.DateTimeField(db_column="testEnfTime",verbose_name="测试结束时间")
    statisticalTime = models.DateTimeField(db_column="statisticalTime", default="2018-02-01 00:00:00", verbose_name="统计时间")
    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效", choices=STATE_CHOICE)
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, blank=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, blank=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_webPortal_openApi_bl_test'


#标准任务表
class TbWebPortalStandardTask(models.Model):
    version = models.CharField(db_column="version", max_length=200, verbose_name="版本")
    businessLine = models.CharField(db_column="businessLine",max_length=200,verbose_name="业务线")
    team = models.CharField(db_column="team",max_length=200,verbose_name="小组")
    head = models.CharField(db_column="head",max_length=200,verbose_name="负责人")
    taskId = models.CharField(db_column="task",max_length=200,verbose_name="任务")


    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效", choices=STATE_CHOICE)
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, blank=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, blank=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_webPortal_standard_task'
        verbose_name = '标准任务版本管理'
        verbose_name_plural = '22标准任务版本管理'


#通过率环境
class TbWebPortalStandardEnv(models.Model):
    httpConfKey = models.CharField(db_column='httpConfKey', unique=True, max_length=50,verbose_name="http服务的key，用例调试、任务执行时，会根据此key来获取对应的http的config信息")
    openApiKey = models.CharField(db_column='openApiKey', max_length=50,verbose_name="openApi服务的key，用例调试、任务执行时，会根据此key来获取对应的http的config信息")
    rmiKey = models.CharField(db_column='rmiKey', max_length=50,verbose_name="rmi服务的key，用例调试、任务执行时，会根据此key来获取对应的http的config信息")
    version = models.CharField(db_column="version",max_length=200,verbose_name="版本")
    ISSHOW_CHOICE = ((1, "显示"), (0, "不显示"))
    actionIsShow = models.IntegerField(db_column="actionIsShow",verbose_name="action环境列是否显示,0不显示，1显示" ,choices=ISSHOW_CHOICE)
    rmiIsShow = models.IntegerField(db_column="rmiIsShow", verbose_name="rmi环境列是否显示,0不显示，1显示", choices=ISSHOW_CHOICE)
    openapiIsShow = models.IntegerField(db_column="openapiIsShow", verbose_name="openapi环境列是否显示,0不显示，1显示", choices=ISSHOW_CHOICE)
    uiIsShow = models.IntegerField(db_column="uiIsShow", verbose_name="ui环境列是否显示,0不显示，1显示",
                                        choices=ISSHOW_CHOICE)
    alias = models.CharField(db_column="alias",unique=True, max_length=200, verbose_name="别名")
    lineSort = models.IntegerField(db_column="lineSort",verbose_name="列的排-序，从小到大依次显示")
    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效", choices=STATE_CHOICE)
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, blank=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, blank=True, verbose_name="修改时间")
    #统计时间
    class Meta:
        db_table = 'tb_webPortal_standard_Env'
        verbose_name = '通过率环境版本配置'
        verbose_name_plural = '23通过率环境版本配置管理'

class TbOpenApiBusinessLine(models.Model):
    businessLineName = models.CharField(db_column="businessLineName",max_length=200,verbose_name="业务线")
    businessLineDesc = models.CharField(db_column="businessLineDesc",max_length=200,verbose_name="业务线描述")
    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效", choices=STATE_CHOICE)
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, blank=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, blank=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_webPortal_openApi_businessLine'
        verbose_name = 'openApi业务线'
        verbose_name_plural = '24openApi业务线'

class TbOpenApiUri(models.Model):
    summaryUri = models.CharField(db_column="summaryUri",max_length=200,verbose_name="获取概况数据的URI")
    summaryUrl = models.CharField(db_column="summaryUrl",default="" ,max_length=200,verbose_name="获取概况数据的URL")
    interfaceTestUri = models.CharField(db_column="interfaceTestUri",max_length=200,verbose_name="获取接口测试数据的URI")
    interfaceTestUrl = models.CharField(db_column="interfaceTestUrl",default="", max_length=200, verbose_name="获取接口测试数据的URL")
    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效", choices=STATE_CHOICE)
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, blank=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, blank=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_webPortal_openApi_uri'
        verbose_name = 'openApi_uri'
        verbose_name_plural = '25openApi_uri'


class TbWebPortRMIGeneralSituation(models.Model):
    coverage = models.IntegerField(db_column="coverage",verbose_name="覆盖的数量")
    methodTotal = models.IntegerField(db_column="methodTotal",verbose_name="方法总数")
    totalTest = models.IntegerField(db_column="totalTest",verbose_name="测试用例总数")
    failedNum = models.IntegerField(db_column="failedNum",verbose_name="测试失败总数")
    passedNum = models.IntegerField(db_column="passedNum",  verbose_name="测试通过总数")
    skippedNum = models.IntegerField(db_column="skippedNum",verbose_name="测试跳过总数")
    summaryAt = models.DateTimeField(db_column="summaryAt", default="2018-02-01 00:00:00", verbose_name="测试时间")
    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效", choices=STATE_CHOICE)
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, blank=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, blank=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_webPortal_RMI_general_situation'

class TbWebPortRMIInterfaceTest(models.Model):
    interfaceDetail = models.TextField(db_column="interfaceDetail",verbose_name="多环境测试详情")
    statisticalTime = models.DateTimeField(db_column="statisticalTime", default="2018-02-01 00:00:00", verbose_name="统计时间")
    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效", choices=STATE_CHOICE)
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, blank=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, blank=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_webPortal_RMI_interface_test'


class TbWebPorRMIServiceTest(models.Model):
    classNum = models.IntegerField(db_column="classNum", verbose_name="类总数")
    classCoverage = models.IntegerField(db_column="classCoverage", verbose_name="类覆盖数量")
    methodNum = models.IntegerField(db_column="methodNum",verbose_name="方法总数")
    methodCoverage = models.IntegerField(db_column="methodCoverage",verbose_name="方法覆盖数")
    coveredRate = models.FloatField(db_column="coveredRate",verbose_name="方法覆盖率")
    testNum = models.IntegerField(db_column="testNum",verbose_name="测试用例总数")
    service = models.CharField(db_column="service",max_length=200,verbose_name="测试的服务")
    statisticalTime = models.DateTimeField(db_column="statisticalTime", default="2018-02-01 00:00:00", verbose_name="统计时间")
    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效", choices=STATE_CHOICE)
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, blank=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, blank=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_webPortal_RMI_service_test'

class TbWebPortalAllPassRate(models.Model):
    testResultMsg = models.TextField(db_column='testResultMsg',verbose_name="任务执行的统计信息,详细统计，json字符串形式保存。")
    execTakeTime = models.IntegerField(db_column='execTakeTime', default=0, verbose_name="执行耗时")
    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效", choices=STATE_CHOICE)
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, blank=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, blank=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_webPortal_all_passRate'


class TbWebPortalBusinessLineActionPassRate(models.Model):
    testResultMsg = models.TextField(db_column='testResultMsg', verbose_name="任务执行的统计信息,详细统计，json字符串形式保存。")
    execTakeTime = models.IntegerField(db_column='execTakeTime', default=0, verbose_name="执行耗时")
    businessLine = models.CharField(db_column='businessLine', max_length=25, verbose_name="businessLine名字")
    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效", choices=STATE_CHOICE)
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, blank=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, blank=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_webPortal_business_line_action_passrate'


class TbWebPortalBusinessLine(models.Model):
    bussinessLine = models.CharField(db_column='bussinessLine', unique=True, max_length=25, verbose_name="businessLine名字")
    bussinessLineDesc = models.CharField(db_column='bussinessLineDesc', default="", max_length=2000, verbose_name="businessLine描述")
    ISSHOW_CHOICE = ((1, "显示"), (0, "隐藏"))
    isShow = models.IntegerField(db_column="isShow", verbose_name="是否显示", choices=ISSHOW_CHOICE)
    level = models.IntegerField(db_column="level", verbose_name="webpotal页面显示排序，从小到大排序")
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_webPortal_business_line'




class TbWebPortalRmiStandardService(models.Model):
    serviceName = models.CharField(db_column="serviceName",max_length=200)
    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效", choices=STATE_CHOICE)
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, blank=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, blank=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_webPortal_RMI_standard_service'

class TbWebPortalUnitTestService(models.Model):
    serviceName = models.CharField(db_column="serviceName",max_length=200,verbose_name="service名称")
    serviceDesc = models.CharField(db_column="serviceDesc",max_length=200,verbose_name="service描述")
    ISSHOW_CHOICE = ((1,"显示"),(0,"隐藏"))
    isShow = models.IntegerField(db_column="isShow",verbose_name="是否显示",choices=ISSHOW_CHOICE)
    level = models.IntegerField(db_column="level",verbose_name="service显示排序，从小到大排序")
    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效", choices=STATE_CHOICE)
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, blank=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, blank=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_webPortal_unit_test_service'
        verbose_name = '单元测试service'
        verbose_name_plural = '26单元测试service'


class TbWebPortalUnitTestGeneralSituation(models.Model):
    codeNum = models.IntegerField(db_column="codeNum",verbose_name="代码总行数")
    coverage = models.IntegerField(db_column="coverage",verbose_name="代码覆盖行数")
    coverageRate = models.FloatField(db_column="coverageRate",verbose_name="覆盖率")
    unitTestDetail = models.TextField(db_column="unitTestDetail", verbose_name="单元覆盖详情")
    statisticalTime = models.DateTimeField(db_column="statisticalTime", default="2018-02-01 00:00:00",)
    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效", choices=STATE_CHOICE)
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, blank=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, blank=True, verbose_name="修改时间")

    class Meta:
        db_table = "tb_webPortal_unit_test_general_situation"

class TbWebPortalUITestGeneralSituation(models.Model):
    testCaseNum = models.IntegerField(db_column="testCaseNum",verbose_name="功能测试用例数量")
    autoTestCoveredNum = models.IntegerField(db_column="autoTestCoveredNum",verbose_name="自动化覆盖数量")
    autoTestRate = models.FloatField(db_column="autoTestRate",verbose_name="自动化率")
    coveredDetail = models.TextField(db_column="coveredDetail",verbose_name="ui覆盖度")
    statisticalTime = models.DateTimeField(db_column="statisticalTime", default="2018-02-01 00:00:00",)
    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效", choices=STATE_CHOICE)
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, blank=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, blank=True, verbose_name="修改时间")

    class Meta:
        db_table = "tb_webPortal_ui_test_general_situation"

class TbWebPortalUITest(models.Model):
    testDetail = models.TextField(db_column='testDetail', verbose_name="多环境测试结果")
    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效", choices=STATE_CHOICE)
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, blank=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, blank=True, verbose_name="修改时间")
    # 统计时间
    statisticalTime = models.DateTimeField(db_column="statisticalTime", default="2018-02-01 00:00:00", verbose_name="统计时间")

    class Meta:
        db_table = 'tb_webPortal_ui_test'

class TbWebPortalUIGeneralSituation(models.Model):
    generalSituationDetail = models.CharField(max_length=2000,db_column="generalSituationDetail",verbose_name="统计详情")
    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效", choices=STATE_CHOICE)
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, blank=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, blank=True, verbose_name="修改时间")
    # 统计时间
    statisticalTime = models.DateTimeField(db_column="statisticalTime", default="2018-02-01 00:00:00", verbose_name="统计时间")

    class Meta:
        db_table = 'tb_webPortal_ui_general_situation'


class TbJiraBusinessLine(models.Model):
    businessLineName = models.CharField(db_column='businessLineName', unique=True, max_length=25,verbose_name="businessLine名字")
    businessLineDesc = models.CharField(db_column='businessLineDesc', default="", max_length=2000,verbose_name="businessLine描述")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_webPortal_jira_business_line'
        verbose_name = 'jira业务线'
        verbose_name_plural = '27jira业务线管理'

    def __str__(self):
        return self.businessLineName

class TbJiraBusinessLinePlatFormRelation(models.Model):
    jiraBusinessLineId = models.ForeignKey(to=TbJiraBusinessLine,db_column="jiraBusinessLineId",verbose_name="jira上的业务线Id")
    platformBusinessLineId = models.ForeignKey(to=TbBusinessLine,db_column="platformBusinessLineId",verbose_name="平台上的业务线Id")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, blank=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, blank=True, verbose_name="修改时间")

    class Meta:
        db_table = "tb_webPortal_jira_business_line_platform_relation"
        verbose_name = 'jira业务线与平台对应关系表'
        verbose_name_plural = '28jira业务线与平台对应关系表'
        unique_together = (('jiraBusinessLineId', 'platformBusinessLineId'),)

class TbjiraModule(models.Model):
    moduleName = models.CharField(db_column='moduleName', unique=True, max_length=25,verbose_name="module名字")
    moduleDesc = models.CharField(db_column='moduleDesc', default="", max_length=2000,verbose_name="module描述")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_webPortal_jira_module'
        verbose_name = 'jira模块'
        verbose_name_plural = '29jira模块'

    def __str__(self):
        return self.moduleName

class TbJiraModulePlatFormRelation(models.Model):
    jiraModuleId = models.ForeignKey(to=TbjiraModule, db_column='jiraModuleId', verbose_name="业务线ID")
    platformModuleId = models.ForeignKey(to=TbModules,db_column="platformModuleId",verbose_name="平台上的模块Id")

    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, blank=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, blank=True, verbose_name="修改时间")

    class Meta:
        db_table = "tb_webPortal_jira_module_platform_relation"
        verbose_name = 'jira模块与平台对应关系表'
        verbose_name_plural = '30jira模块与平台对应关系表'
        unique_together = (('jiraModuleId', 'platformModuleId'),)

class TbWebPortalUiCovered(models.Model):
    coverDetail = models.TextField(db_column='coverDetail',  verbose_name = "多环境测试结果")
    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效",choices=STATE_CHOICE)
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True,blank=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True,blank=True, verbose_name="修改时间")
    #统计时间
    statisticalTime = models.DateTimeField(db_column="statisticalTime",default="2018-02-01 00:00:00",verbose_name="统计时间")
    class Meta:
        db_table = 'tb_webPortal_ui_covered'


class TbWebPortalServiceInterfaceCovered(models.Model):
    serviceName = models.CharField(db_column="serviceName",max_length=100, unique=True, verbose_name="service名称")
    standardInterfaceNum = models.IntegerField(db_column="standardInterfaceNum",verbose_name="标准接口数量")
    coveredInterfaceNum = models.IntegerField(db_column="coveredInterfaceNum",verbose_name="已覆盖接口数量")
    coverage = models.FloatField(db_column="coverage",verbose_name="覆盖率")
    serviceTestDetail = models.TextField(db_column="serviceTestDetail", verbose_name="service覆盖详情", default="")
    #统计时间
    statisticalTime = models.DateTimeField(db_column="statisticalTime",default="2018-02-01 00:00:00",verbose_name="统计时间")

    state = models.IntegerField(default=1, db_column="state", verbose_name="状态 0删除 1有效")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True,blank=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True,blank=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_webPortal_service_interface_covered'