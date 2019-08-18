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

class TbBusinessLine(models.Model):
    bussinessLineName = models.CharField(db_column='bussinessLineName', unique=True, max_length=25, verbose_name="businessLine名字")
    bussinessLineDesc = models.CharField(db_column='bussinessLineDesc', default= "", max_length=2000, verbose_name="businessLine描述")

    state = models.IntegerField(default=1,verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25,db_column='addBy', null=True,verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True,verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True,verbose_name="修改时间")

    class Meta:
        db_table = 'tb_business_line'
        verbose_name = '03业务线'
        verbose_name_plural = '03业务线管理'

    def __str__(self):
        return self.bussinessLineName

class TbModules(models.Model):
    moduleName = models.CharField(db_column='moduleName', unique=True, max_length=25, verbose_name="模块名称")
    moduleDesc = models.CharField(db_column='moduleDesc', max_length=2000, verbose_name="模块描述")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_modules'
        verbose_name = '04模块'
        verbose_name_plural = '04模块管理'

    def __str__(self):
        return self.moduleName

class TbSource(models.Model):
    sourceName = models.CharField(db_column='sourceName', unique=True, max_length=25, verbose_name="来源名称")
    sourceDesc = models.CharField(db_column='sourceDesc', max_length=2000, verbose_name="来源描述")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_source'
        verbose_name = '来源'
        verbose_name_plural = '05来源管理'

    def __str__(self):
        return self.sourceName

class TbTag(models.Model):
    tag = models.CharField(unique=True, max_length=30, verbose_name="tag名称")
    usecount = models.IntegerField(default=0,verbose_name="tag数量统计")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.ForeignKey(to=TbUser, to_field="loginName", related_name="TbTagAddBy", on_delete=models.CASCADE, db_column='addBy', verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_tag'


class TbBusinessLineModuleRelation(models.Model):
    businessLineId = models.ForeignKey(to=TbBusinessLine, db_column='businessLineId', verbose_name="业务线ID")
    moduleId = models.ForeignKey(to=TbModules, db_column='moduleId', verbose_name="模块ID")
    level = models.IntegerField(default=10, verbose_name="显示优先级，数字越小越优先")

    class Meta:
        db_table = 'tb_businessLine_module_relation'
        unique_together = (('businessLineId', 'moduleId'),)
        verbose_name = '业务线模块关系表'
        verbose_name_plural = '041业务线模块关系表'
