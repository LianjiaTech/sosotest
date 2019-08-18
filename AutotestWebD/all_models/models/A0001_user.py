# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

class TbUser(models.Model):
    loginName = models.CharField(db_column='loginName', unique=True, max_length=20, verbose_name = "登录账号")
    email = models.CharField(max_length=50, verbose_name="用户邮箱")
    userName = models.CharField(db_column='userName', max_length=10, verbose_name="用户姓名")
    pwd = models.CharField(max_length=100,default= "e10adc3949ba59abbe56e057f20f883e", verbose_name = "登录密码")
    token = models.CharField(max_length=200, null=True,default="",blank=True, verbose_name = "用户生成的token信息")
    type_CHOICE = ((0, "未选择"), (1, "开发人员"),(2, "测试人员"),)
    type = models.IntegerField(default=1, verbose_name = "用户类型 0未选择 1开发人员 2测试人员",choices=type_CHOICE) # 0未选择 1开发人员 2测试人员
    audit_CHOICE = ((0, "0未审核"), (1, "1审核中"), (2, "2通过"), (3, "3未通过"),)
    audit = models.IntegerField(default=2, verbose_name = "审核状态 0未审核 1审核中 2通过 3未通过",choices=audit_CHOICE) # 0未审核 1审核中 2通过 3未通过
    defaultPermission = models.IntegerField(default=1, verbose_name="是否具有默认权限 1 有 2 无") # 0未审核 1审核中 2通过 3未通过
    language_CHOICE = (("cn", "中文简体"), ("en", "英语"),)
    language = models.CharField(max_length=10,default="cn", verbose_name = "用户显示语言cn或者en",choices=language_CHOICE)
    state_CHOICE = ((0,"已删除"),(1,"有效"),)
    state = models.IntegerField(default=1, verbose_name = "状态 0删除 1有效",choices=state_CHOICE)
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True,verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True,verbose_name="修改时间")

    class Meta:
        db_table = 'tb_user'
        verbose_name = '用户'
        verbose_name_plural = '01用户管理'

    def __str__(self):
        return "[%d]%s(%s)" % (self.id,self.userName,self.email)



class TbUserLog(models.Model):
    loginName = models.CharField(db_column='loginName', max_length=20, verbose_name = "登录账号")
    userName = models.CharField(db_column='userName', max_length=10, verbose_name = "用户姓名")
    operationUrl = models.CharField(db_column="operationUrl",max_length=500, default="",verbose_name = "操作地址")
    operationDesc = models.TextField(db_column="operationDesc", default="",verbose_name = "操作详情")
    operationResult = models.CharField(db_column="operationResult", max_length=1000,default="",verbose_name = "操作结果")
    fromHostIp = models.CharField(db_column="fromHostIp",max_length=500, default="",verbose_name = "请求来源IP")
    state = models.IntegerField(default=1, verbose_name = "状态 0删除 1有效")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True,verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True,verbose_name="修改时间")

    class Meta:
        db_table = 'tb_user_log'
        verbose_name = '用户操作日志'
        verbose_name_plural = '51用户操作日志'

class TbUserChangeLog(models.Model):
    loginName = models.CharField(db_column='loginName', max_length=20, verbose_name = "登录账号")
    otherLoginName = models.CharField(db_column='otherLoginName', max_length=20, verbose_name = "被修改人的登录账号")
    beforeChangeData = models.TextField(db_column="beforeChangeData",verbose_name = "修改前的数据")
    afterChangeData = models.TextField(db_column="afterChangeData", verbose_name = "修改后的数据")
    dataId = models.CharField(db_column="dataId",max_length=500, default="",verbose_name = "选择修改的数据的Id  interfaceId caseId taskId")
    changeDataId = models.CharField(db_column="changeDataId",max_length=500, default="",verbose_name = "使用哪个Id的数据进行修改")
    testStepId = models.CharField(db_column="testStepId",max_length=500, default="",verbose_name = "testStepId")
    type = models.IntegerField(db_column="type",verbose_name = "0 删除 ，1 编辑")
    version = models.CharField(db_column="version",max_length=500, default="",verbose_name = "数据版本")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True,verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True,verbose_name="修改时间")

    class Meta:
        db_table = 'tb_user_change_log'

class TbTeam(models.Model):
    teamName = models.CharField(max_length=100,db_column="teamName",unique=True,verbose_name="小组名称")
    teamDesc = models.CharField(max_length=100,db_column="teamDesc",verbose_name="小组描述")
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True, blank=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = "tb_team"

# 权限
class TbPermission(models.Model):
    permissionName = models.CharField(max_length=100,db_column="permissionName",verbose_name="权限名称",unique=True)
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True, blank=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_permissions'


#后台小组权限
class TbTeamPermissionRelation(models.Model):
    teamName = models.CharField(max_length=100,db_column="teamName",verbose_name="小组名称")
    permissionName = models.CharField(max_length=100,db_column="permissionName",verbose_name="权限名称")
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True, blank=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_team_permission_relation'

#后台用户权限
class TbUserPermissionRelation(models.Model):
    loginName = models.CharField(max_length=100,db_column="loginName",default="",verbose_name="用户名称")
    permissionKey = models.CharField(max_length=100,db_column="permissionKey",default="",verbose_name="权限名称")
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True, blank=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_user_permission_relation'

#后台小组用户关联
class TbUserTeamRelation(models.Model):
    userName = models.CharField(max_length=100,db_column="userName",verbose_name="用户名称")
    teamName = models.CharField(max_length=100, db_column="teamName", verbose_name="小组名称")
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True, blank=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_user_team_relation'