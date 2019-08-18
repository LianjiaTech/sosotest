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
class TbUserDeploymentTool(models.Model):
    redisKey = models.CharField(max_length=1000, db_column="redisKey",verbose_name="redisKey",default="")
    opsList = models.CharField(max_length=1000, db_column="opsList",verbose_name="ops列表",default="")
    strongCheckSuccessList = models.CharField(max_length=1000, db_column="strongCheckSuccessList", verbose_name="强校验成功的ops列表", default="")
    weakCheckSuccessList = models.CharField(max_length=1000, db_column="weakCheckSuccessList", verbose_name="弱校验成功的ops列表", default="")
    strongCheckFailedList = models.CharField(max_length=1000, db_column="strongCheckFailedList", verbose_name="强校验失败的ops列表", default="")
    weakCheckFailedList = models.CharField(max_length=1000, db_column="weakCheckFailedList", verbose_name="弱校验失败的ops列表", default="")
    opsDeploySuccessList = models.CharField(max_length=1000, db_column="opsDeploySuccessList", verbose_name="部署成功的ops列表", default="")
    serviceDeployList = models.CharField(max_length=1000, db_column="serviceDeployList", verbose_name="service列表", default="")
    serviceDeploySuccessList = models.CharField(max_length=1000, db_column="serviceDeploySuccessList", verbose_name="部署成功的service列表", default="")
    serviceDeployFailedList = models.CharField(max_length=1000, db_column="serviceDeployFailedList", verbose_name="部署失败的service列表", default="")
    detail = models.TextField( db_column="detail", verbose_name="部署失败的service列表")
    remark = models.CharField(max_length=1000, db_column="remark", verbose_name="备注", default="")
    message = models.CharField(max_length=1000, db_column="message", verbose_name="返回的消息", default="")
    report = models.CharField(max_length=1000, db_column="report", verbose_name="报告路径", default="")
    status = models.IntegerField(default=1,db_column="status", verbose_name="状态 数据效验中 2部署中  3部署完成 4 部署发生异常")
    autoFlag = models.IntegerField(default=0,db_column="autoFlag", verbose_name="0,效验带部署 手动  1，效验 自动 2.部署 自动")
    execResult = models.CharField(max_length=100,default="",db_column="execResult", verbose_name="状态 PASS 成功 FAIL 失败")
    state = models.IntegerField(default=1,db_column="state", verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True, blank=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = "tb_user_deployment_tool"
