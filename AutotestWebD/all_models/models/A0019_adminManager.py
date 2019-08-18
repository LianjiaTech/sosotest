# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
import django.utils.timezone
import datetime

#后台管理员
class TbAdminManager(models.Model):
    loginName = models.CharField(max_length=100, db_column="loginName", unique=True, verbose_name="登录名称")
    password = models.CharField(max_length=100, db_column="password", verbose_name="密码", default="")
    userName = models.CharField(max_length=100, db_column="userName", verbose_name="用户名")
    email = models.CharField(max_length=50, verbose_name="用户邮箱", default="")
    superManager = models.IntegerField(default=0, verbose_name="状态 0不是 1是")
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True, blank=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = "tb_admin_manager"
