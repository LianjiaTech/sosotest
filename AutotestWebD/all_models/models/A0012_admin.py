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

#后台小组
class TbAdminTeam(models.Model):
    teamName = models.CharField(max_length=100, db_column="teamName", verbose_name="小组名称")
    teamKey = models.CharField(max_length=100, db_column="teamKey", unique=True, verbose_name="小组key",default="")
    teamDesc = models.CharField(max_length=100, db_column="teamDesc", verbose_name="小组描述")
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True, blank=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = "tb_admin_team"

#后台用户
class TbAdminUser(models.Model):
    loginName = models.CharField(max_length=100, db_column="loginName", unique=True, verbose_name="登录名")
    passWord = models.CharField(max_length=100, db_column="passWord", verbose_name="密码")
    userName = models.CharField(max_length=100, db_column="userName", verbose_name="用户名")
    email = models.CharField(max_length=50, verbose_name="用户邮箱", default="")
    superManager = models.IntegerField(db_column="superManager",default=0,verbose_name="是否为超级管理员，0否，1是")
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True,blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True,blank=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")
    class Meta:
        db_table = 'tb_admin_user'

#后台角色
class TbAdminRole(models.Model):
    roleName = models.CharField(max_length=100, db_column="roleName", verbose_name="角色名")
    roleKey = models.CharField(max_length=100, db_column="roleKey", unique=True, verbose_name="角色key", default="")
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True, blank=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = "tb_admin_role"

# 权限
# class TbAdminPermission(models.Model):
#     permissionName = models.CharField(max_length=100, db_column="permissionName", verbose_name="权限名称")
#     permissionKey = models.CharField(max_length=100, db_column="permissionKey", unique=True, verbose_name="权限key", default="")
#     isDefaultPermission = models.IntegerField(default=0, verbose_name="状态 0不是默认的 1是默认的")
#     state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
#     addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
#     modBy = models.CharField(max_length=25, db_column='modBy', null=True, blank=True, verbose_name="修改者登录名")
#     addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
#     modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")
#
#     class Meta:
#         db_table = 'tb_admin_permissions'

#后台权限
class TbAdminManagePermission(models.Model):
    permissionName = models.CharField(max_length=100, db_column="permissionName", verbose_name="权限名称")
    permissionKey = models.CharField(max_length=100, db_column="permissionKey", unique=True, verbose_name="权限key", default="")
    permissionValue = models.CharField(max_length=200, db_column="permissionValue", verbose_name="权限值", default="")
    isDefaultPermission = models.IntegerField(default=0, verbose_name="状态 0不是默认的 1是默认的")
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True, blank=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_admin_manage_permission'

# 后台用户管理权限
class TbAdminManageUserPermissionRelation(models.Model):
    loginName = models.CharField(db_column='loginName', max_length=20, verbose_name="登录账号")
    permissionKey = models.CharField(max_length=100, db_column="permissionKey", verbose_name="权限key", default="")
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True, blank=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_admin_manage_user_permission_relation'


#后台小组权限
class TbAdminTeamPermissionRelation(models.Model):
    teamKey = models.CharField(max_length=100, db_column="teamKey", verbose_name="小组key", default="")
    permissionKey = models.CharField(max_length=100, db_column="permissionKey", verbose_name="权限key", default="")
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True, blank=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_admin_team_permission_relation'



#后台用户权限
class TbAdminUserPermissionRelation(models.Model):
    loginName = models.CharField(db_column='loginName', max_length=20, verbose_name="登录账号")
    permissionKey = models.CharField(max_length=100, db_column="permissionKey", verbose_name="权限key", default="")
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True, blank=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_admin_user_permission_relation'



#后台小组用户关联
class TbAdminUserTeamRelation(models.Model):
    loginName = models.CharField(max_length=100, db_column="loginName", verbose_name="登录名", default="")
    teamKey = models.CharField(max_length=100, db_column="teamKey", verbose_name="小组key", default="")
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True, blank=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_admin_user_team_relation'

#后台角色权限
class TbAdminRolePermissionRelation(models.Model):
    roleKey = models.CharField(max_length=100, db_column="roleKey", unique=True, verbose_name="角色key", default="")
    permissionKey = models.CharField(max_length=100, db_column="permissionKey", unique=True, verbose_name="权限key",default="")
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True, blank=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_admin_role_permission_relation'

#后台用户角色关联表
class TbAdminUserRoleRelation(models.Model):
    roleKey = models.CharField(max_length=100, db_column="roleKey",verbose_name="角色key", default="")
    loginName = models.CharField(max_length=100, db_column="loginName", verbose_name="登录名", default="")
    teamKey = models.CharField(max_length=100, db_column="teamKey", verbose_name="小组key", default="")
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True, blank=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_admin_user_role_relation'

# #后台接口和页面关联表
# class TbAdminInterfaceModuleRelation(models.Model):
#     url = models.CharField(max_length=255, db_column="url", verbose_name="url", default="")
#     moduleName = models.CharField(max_length=100, db_column="moduleName", verbose_name="接口所属页面", default="")
#     state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
#     addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
#     modBy = models.CharField(max_length=25, db_column='modBy', null=True, blank=True, verbose_name="修改者登录名")
#     addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
#     modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")
#
#     class Meta:
#         db_table = 'tb_admin_interface_module_relation'

#后台接口和权限关联表
class TbAdminInterfacePermissionRelation(models.Model):
    permissionName = models.CharField(max_length=255,db_column="permissionName",default="") #理论上这个也是惟一的
    permissionKey = models.CharField(max_length=100, db_column="permissionKey",unique=True, verbose_name="权限key", default="") # 供关联权限时使用
    url = models.CharField(max_length=255, db_column="url", verbose_name="url", default="")
    permission = models.CharField(max_length=100, db_column="permission", verbose_name="权限", default="") #供判断权限时使用 run delete check edit copy add
    isDefault = models.IntegerField(default=0, verbose_name="是否为默认权限 0否 1是")
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True, blank=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_admin_interface_permission_relation'

#后台权限
class TbAdminPlatformPermission(models.Model):
    permissionName = models.CharField(max_length=255, db_column="permissionName", verbose_name="权限Name", default="")
    permissionKey = models.CharField(max_length=100, db_column="permissionKey", unique=True, verbose_name="权限key", default="")
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True, blank=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_admin_platform_permission'

#后台用户权限
class TbAdminPlatformPermissionUserRelation(models.Model):
    loginName = models.CharField(max_length=100, db_column="loginName", verbose_name="登录名")
    permissionKey = models.CharField(max_length=100, db_column="permissionKey", verbose_name="权限key", default="")
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, blank=True, verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True, blank=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_admin_platform_permission_user_relation'