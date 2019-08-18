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

class TbUiPackage(models.Model):
    packageId = models.CharField(db_column='packageId', unique=True, default="", max_length=25, verbose_name="包ID")
    title = models.CharField(db_column='title',max_length=100, verbose_name="标题")
    packageDesc = models.CharField(db_column='packageDesc',max_length=1000, verbose_name="描述")

    # 基本信息
    packageType = models.IntegerField(default=1,db_column="packageType", verbose_name="包类型，1-安卓 2-iPhone 3-iPad ")
    appFileName = models.CharField(max_length=300, db_column="appFileName", verbose_name="包文件名(android/ios)")
    appPackage = models.CharField(max_length=300, db_column='appPackage', default="", verbose_name="appPackage(Android)")
    appActivity = models.CharField(max_length=300, db_column='appActivity', default="", verbose_name="appActivity(Android)")
    bundleId = models.CharField(max_length=300, db_column='bundleId', default="", verbose_name="bundleId(iOS)")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_ui_package'

class TbUiAutoUploadPackage(models.Model):
    appType = models.CharField(max_length=300, db_column='appType', default="", verbose_name="appType Android or ios")
    uploadResult = models.IntegerField( db_column='uploadResult', default=1, verbose_name="上传成功1 失败2")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_ui_auto_upload_package'
