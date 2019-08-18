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

class Tb3UIGlobalText(models.Model):
    textDesc = models.CharField(db_column='textDesc', max_length=5000, default="", verbose_name="详情")
    textKey = models.CharField(db_column='textKey', unique=True, max_length=100, verbose_name="文本key,中英文数字下划线组合")
    textValue = models.TextField(db_column='textValue',  verbose_name="文本value")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25,db_column='addBy',null = True, verbose_name="添加者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb3_ui_global_text'

class Tb3UIGlobalVars(models.Model):
    varDesc = models.CharField(db_column='varDesc', max_length=5000, verbose_name="详情")
    varKey = models.CharField(db_column='varKey', unique=True, max_length=100, verbose_name="全局变量key,中英文数字下划线组合")
    varValue = models.TextField(db_column='varValue',  verbose_name="全局变量value")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25,db_column='addBy',null = True, verbose_name="添加者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb3_ui_global_vars'

