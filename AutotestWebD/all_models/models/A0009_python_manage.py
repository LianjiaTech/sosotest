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

class TbExecPythonAttrs(models.Model):
    #用户添加信息
    execPythonAttr = models.CharField(db_column='execPythonAttr',  max_length=200, unique=True, verbose_name = "属性key，例如importStr,timeoutTime")
    execPythonDesc = models.CharField(db_column='execPythonDesc',  max_length=1000, verbose_name = "描述")
    execPythonValue = models.TextField(db_column='execPythonValue',  verbose_name = "属性值，例如import json 或者0 等")
    #通用信息
    STATE_CHOICE = ((1, "有效"), (0, "无效"))
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效",choices=STATE_CHOICE)
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True,blank=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True,blank=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_exec_python_attrs'
        verbose_name = '执行python代码管理'
        verbose_name_plural = '12执行python代码管理py'