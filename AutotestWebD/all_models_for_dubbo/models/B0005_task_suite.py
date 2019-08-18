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

class Tb2DUBBOTaskSuite(models.Model):
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
        db_table = 'tb2_dubbo_task_suite'
        verbose_name = '任务集'

class Tb2DUBBOTaskSuiteExecute(models.Model):
    taskSuiteId = models.CharField(db_column='taskSuiteId' , max_length=25,verbose_name="任务ID")
    title = models.CharField(max_length=100,verbose_name="任务标题",db_column="title")
    taskSuiteDesc = models.CharField(max_length=1000,verbose_name="任务描述",db_column="taskSuiteDesc")
    protocol = models.CharField(max_length=20,verbose_name="任务协议",db_column="protocol")
    status = models.IntegerField(default=2,verbose_name="状态，1新建待审核 2审核通过 3审核未通过")
    taskCount = models.IntegerField(db_column='taskCount',verbose_name="任务集中的任务列表")
    taskList = models.CharField(db_column='taskList',verbose_name="任务集中的任务列表",max_length=300)
    isCI = models.IntegerField(db_column="isCI",verbose_name="是否加入到持续集成  0 不加人  1加入",default=0)

    httpConfKeyList = models.CharField(db_column="httpConfKeyList",max_length=300,verbose_name="任务集包含的执行环境")
    httpConfKeyAliasList = models.CharField(db_column="httpConfKeyAliasList",max_length=300,verbose_name="任务集包含的执行环境名称")
    caseLevel = models.IntegerField(db_column='caseLevel',default=100,verbose_name="执行时选择的执行优先级，如果选择了，那么只有同等优先级的case会执行，0高 5中 9低")
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
    execBy = models.CharField(db_column='execBy', max_length=30, default="", verbose_name="执行人登录用户名")
    execStatus = models.IntegerField(db_column='execStatus', default=1, verbose_name="执行状态: NOTRUN = 1 RUNNING = 2 DONE = 3 EXCEPTION = 4 CANCELING = 10 CANCELED = 11")
    execProgressData = models.CharField(db_column='execProgressData',default="0:0:0:0:0", max_length=30,verbose_name="执行进度数据，格式：ALL:PASS:FAIL:ERROR:NOTRUN，例如任务有10个用例，10:3:1:0:6,代表总共10个，通过3个，失败1个，错误0个，未执行6个。  ")
    execPlatform = models.IntegerField(db_column='execPlatform',default=1,verbose_name="调用接口的平台，1代表测试平台，2代表jenkins，100代表其他")
    execLevel = models.IntegerField(db_column='execLevel',default=5,verbose_name="优先级 5默认 数字越小优先级越高 范围1-10")
    testResult = models.CharField(db_column='testResult', max_length=20,default='NOTRUN',verbose_name="测试结果 根据断言结果生成的测试结果 PASS/FAIL/ERROR/EXCEPTION/CANCEL")
    testResultMsg = models.TextField(db_column='testResultMsg',verbose_name="任务执行的统计信息,详细统计，json字符串形式保存。")
    testReportUrl = models.CharField(db_column='testReportUrl', max_length=200,verbose_name="测试报告链接")

    taskExecuteIdList = models.CharField(db_column="taskExecuteIdList",max_length=200,verbose_name="本次任务执行包含的任务执行Id",default="")
    version = models.CharField(db_column='version', max_length=25,default='CurrentVersion',verbose_name="执行的版本")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(db_column='addBy', verbose_name="创建者登录名",max_length=25)
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb2_dubbo_task_suite_execute'
