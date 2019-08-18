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
import django.utils.timezone as timezone

class TbUiMobileServer(models.Model):
    # 基本信息
    serverName = models.CharField(db_column="serverName",unique=True,default="",max_length=30,verbose_name="appium服务的名称")
    serverDesc = models.CharField(db_column="serverDesc",default="",max_length=100,verbose_name="appium服务的描述")
    serverType = models.IntegerField(default=1,db_column="serverType", verbose_name="服务类型，1Android、2iphone")
    status = models.IntegerField(db_column="status",default=0,verbose_name="当前server有没有被使用")
    executeTaskId = models.CharField(db_column="executeTaskId",default="",null=True,blank=True,max_length=30,verbose_name="当前使用本服务的任务")
    serverIp = models.CharField(db_column="serverIp",default="",max_length=30,verbose_name="当前使用本服务ip地址")
    serverPort = models.CharField(db_column="serverPort",default="",max_length=30,verbose_name="当前使用本服务端口")
    udid = models.CharField(db_column="udid",default="",max_length=100,verbose_name="服务对应的设备udid")
    deviceName = models.CharField(db_column="deviceName",default="",max_length=100,verbose_name="服务对应的设备deviceName")
    wdaLocalPort = models.IntegerField(db_column="wdaLocalPort",default=8000,verbose_name="ios用到的webDriverAgen的端口，对应wdaLocalPort  参数")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True,  blank=True,verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_ui_mobile_server'
        verbose_name = 'ui移动端服务'
        verbose_name_plural = '40ui移动端服务表'

class TbUIMobileServerLog(models.Model):
    serviceName = models.CharField(db_column="serviceName",max_length=30,verbose_name="appium的服务名称")
    executeTaskId = models.CharField(db_column="executeTaskId",default="",max_length=30,verbose_name="当前使用本服务的任务")
    executeBy = models.CharField(max_length=25, db_column='executeBy', null=True, blank=True, verbose_name="执行者登录名")
    startTime = models.DateTimeField(default=timezone.now,db_column="startTime",verbose_name="任务使用服务的开始时间")
    endTime = models.DateTimeField(default=timezone.now,db_column="endTime",verbose_name="任务使用服务的结束时间")
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    class Meta:
        db_table = 'tb_ui_mobile_server_log'
        verbose_name = 'ui服务log'
        verbose_name_plural = '41ui移动端服务表Log'