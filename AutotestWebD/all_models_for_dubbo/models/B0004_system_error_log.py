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

class Tb0ErrorLog(models.Model):
    title = models.CharField(max_length=100,default="UNTITLED",verbose_name="Log标题")
    errorLogText = models.TextField(db_column='errorLogText', default='', verbose_name="Log的文本")  # release2 新增
    logLevel = models.IntegerField(default=10, verbose_name="级别")

    STATE_CHOICE = ((1, "未解决"), (0, "已解决"))
    state = models.IntegerField(default=1, verbose_name="状态 0已解决 1未解决",choices=STATE_CHOICE)
    addBy = models.CharField(max_length=25,db_column='addBy',default=None,null = True, verbose_name="添加者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',default=None,null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb0_error_log'
        verbose_name = '00系统错误日志表'
        verbose_name_plural = '00系统错误日志表'
