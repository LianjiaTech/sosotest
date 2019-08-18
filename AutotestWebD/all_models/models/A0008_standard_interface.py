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
from all_models.models.A0003_attribute import *

class TbStandardInterface(models.Model):
    #关联源文件
    businessLineId = models.ForeignKey(to=TbBusinessLine, db_column='businessLineId', verbose_name="业务线ID")
    moduleId = models.ForeignKey(to=TbModules, db_column='moduleId', verbose_name="模块ID")
    #解析结果
    fileName = models.CharField(db_column='fileName',max_length=3000,default="", verbose_name="文件名")
    # 解析出来的信息
    interfaceUrl = models.CharField(max_length=9999,db_column='interfaceUrl',null = False,default="/", verbose_name="解析出的标准接口URL")
    interfaceCreateBy = models.CharField(max_length=100,db_column='interfaceCreateBy',null = False,default="暂时无法解析", verbose_name="创建者信息")
    interfaceCreateTime = models.DateTimeField(db_column='interfaceCreateTime',default="", verbose_name="创建时间")
    interfaceUpdateBy = models.CharField(max_length=100,db_column='interfaceUpdateBy',null = False,default="暂时无法解析", verbose_name="更新者信息")
    interfaceUpdateTime = models.DateTimeField(db_column='interfaceUpdateTime',default="", verbose_name="修改时间")
    authorEmail = models.CharField(max_length=200,db_column='authorEmail',default="暂时无法解析",verbose_name="作者邮箱（用于接收邮件）")
    apiStatus = models.IntegerField(default=1, verbose_name="状态 0废弃 1有效 3不存在接口 4apiStatus状态值错误")
    serviceName = models.CharField(max_length=100, db_column='serviceName', default="", verbose_name="接口所属service")

    #通用信息
    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效",choices=STATE_CHOICE)
    addBy = models.ForeignKey(to=TbUser, to_field="loginName", related_name="TbStandardInterfaceAddBy", on_delete=models.CASCADE, db_column='addBy', verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_standard_interface'


