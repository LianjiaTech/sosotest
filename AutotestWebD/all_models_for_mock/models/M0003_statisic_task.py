from __future__ import unicode_literals
from django.db import models

class Tb4StatisticTask(models.Model):
    businessLineId = models.IntegerField(db_column='businessLineId',default=0, verbose_name="业务线id")
    moduleId = models.IntegerField(db_column='moduleId',default=0, verbose_name="模块id")
    title = models.CharField(db_column='title', max_length=255, default="",  verbose_name="统计任务标题")
    descText = models.CharField(db_column='descText', max_length=2000, default="", verbose_name="统计任务描述")

    #通用基本信息
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25,db_column='addBy',null = True, verbose_name="添加者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb4_statistic_task'

class Tb4StatisticTaskExecuteInfo(models.Model):
    statisticTaskId = models.IntegerField(db_column='statisticTaskId',default=0, verbose_name="统计任务Id")
    businessLineId = models.IntegerField(db_column='businessLineId',default=0, verbose_name="业务线id")
    moduleId = models.IntegerField(db_column='moduleId',default=0, verbose_name="模块id")
    title = models.CharField(db_column='title', max_length=255, default="",  verbose_name="统计任务标题")
    descText = models.CharField(db_column='descText', max_length=2000, default="", verbose_name="统计任务描述")

    #执行信息
    executeDetailText = models.TextField(db_column='executeDetailText', default="", verbose_name="统计任务执行详情")
    testResult = models.CharField(db_column='testResult', max_length=10, default="",  verbose_name="PASS/FAIL/EXCEPTION/ERROR")
    codeCoverage = models.FloatField(db_column='codeCoverage',default=0.0, verbose_name="代码覆盖率")
    executeStartTime = models.DateTimeField(db_column='executeStartTime', verbose_name="执行开始时间")
    executeTaketime = models.IntegerField(db_column='executeTaketime',default=0, verbose_name="执行耗时单位秒")
    httpConfKey = models.CharField(db_column='httpConfKey', max_length=50, default="",  verbose_name="执行环境key")
    executeType = models.CharField(db_column='executeType', max_length=20, default="",  verbose_name="执行类型pipeline/daily/manual")
    executeBy = models.CharField(db_column='executeBy', max_length=30, default="",  verbose_name="执行人的loginName")
    comments = models.CharField(db_column='comments', max_length=4000, default="",  verbose_name="备注")
    reason = models.CharField(db_column='reason', max_length=4000, default="",  verbose_name="执行失败的原因等")

    #通用基本信息
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25,db_column='addBy',null = True, verbose_name="添加者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb4_statistic_task_execute_info'