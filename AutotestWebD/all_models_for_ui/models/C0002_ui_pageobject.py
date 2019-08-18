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

class Tb3UIPageObject(models.Model):
    poKey = models.CharField(db_column='poKey', unique=True, max_length=100, verbose_name="文本key,中英文数字下划线组合")
    poTitle = models.CharField(db_column='poTitle', max_length=500, default="", verbose_name="详情")
    poDesc = models.CharField(db_column='poDesc', max_length=2000, default="", verbose_name="详情")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25,db_column='addBy',null = True, verbose_name="添加者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb3_ui_page_object'

class Tb3UIPageElement(models.Model):
    poKey = models.CharField(db_column='poKey', max_length=100, verbose_name="PageObject的key,中英文数字下划线组合")
    elementTitle = models.CharField(db_column='elementTitle', max_length=200, default="", verbose_name="标题")
    elementDesc = models.CharField(db_column='elementDesc', max_length=2000, default="", verbose_name="详情")
    elementKey = models.CharField(db_column='elementKey', max_length=100, default="", verbose_name="elementKey")
    elementType = models.CharField(db_column='elementType', max_length=20, default="", verbose_name="element类型，name id 等等")
    elementValue = models.CharField(db_column='elementValue', max_length=1000, default="", verbose_name="element 值")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25,db_column='addBy',null = True, verbose_name="添加者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb3_ui_page_element'
        unique_together = (('poKey', 'elementKey'),)
