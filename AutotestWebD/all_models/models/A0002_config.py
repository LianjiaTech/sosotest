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

class TbConfigService(models.Model):
    serviceConfKey = models.CharField(db_column='serviceConfKey', unique=True, max_length=50, verbose_name="service服务的key，TbConfigHttp会根据此key关联对应的使用的service，用户新增TbConfigHttp可选择service")
    alias = models.CharField(unique=True, max_length=200, verbose_name="别名，显示给用户，用户选择时看到的描述")
    serviceConfDesc = models.CharField(db_column='serviceConfDesc',default="", max_length=5000, verbose_name="详细描述")
    serviceConf = models.TextField(db_column='serviceConf', verbose_name="""配置文件，configparser通用的配置文件格式""")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25,db_column='addBy', null=True,verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_config_service'
        verbose_name = '数据服务器'
        verbose_name_plural = '06数据服务器管理'

    def __str__(self):
        return "%s(%s)" % (self.alias,self.serviceConfKey)

class TbConfigHttp(models.Model):
    httpConfKey = models.CharField(db_column='httpConfKey', unique=True, max_length=50, verbose_name="http服务的key，用例调试、任务执行时，会根据此key来获取对应的http的config信息")
    serviceConfKey = models.ForeignKey(to=TbConfigService,to_field = "serviceConfKey",on_delete=models.CASCADE,db_column='serviceConfKey', max_length=25, verbose_name="TbConfigService的serviceConfKey，根据此信息把http_conf调用的底层service配置获取加载")
    alias = models.CharField(unique=True, max_length=200, verbose_name="别名")
    httpConfDesc = models.CharField(db_column='httpConfDesc', default="" ,max_length=5000, verbose_name="详细描述")

    UI_STATE_CHOICE = ((1, "显示"), (0, "不显示"))
    apiRunState = models.IntegerField(default=1,db_column='apiRunState', verbose_name="是否在API执行时显示 0不显示 1显示" , choices=UI_STATE_CHOICE)
    uiRunState = models.IntegerField(default=0,db_column='uiRunState', verbose_name="是否在UI执行时显示 0不显示 1显示" , choices=UI_STATE_CHOICE)
    dubboRunState = models.IntegerField(default=0,db_column='dubboRunState', verbose_name="是否在dubbo执行时显示 0不显示 1显示" , choices=UI_STATE_CHOICE)
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25,db_column='addBy', null=True,verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_config_http'
        verbose_name = '环境配置'
        verbose_name_plural = '08环境配置管理'

    def __str__(self):
        return "%s(%s)" % (self.alias,self.httpConfKey)

class TbUserHttpconf(models.Model):
    loginName = models.ForeignKey(to=TbUser,to_field="loginName",related_name="TbUserHttpconfLoginname",db_column='loginName', max_length=30, blank=True, default="", verbose_name="执行人登录用户名")
    httpConfKey = models.ForeignKey(to=TbConfigHttp, to_field="httpConfKey", db_column='httpConfKey', max_length=20,verbose_name="执行环境的httpConfKey")
    conflevel = models.IntegerField(verbose_name="配置优先级")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.ForeignKey(to=TbUser, to_field="loginName", related_name="TbUserHttpconfAddBy", on_delete=models.CASCADE, db_column='addBy', verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_user_httpconf'
        unique_together = (('loginName', 'httpConfKey'),)

class TbConfigUri(models.Model):
    uriKey = models.CharField(db_column='uriKey', primary_key=True, max_length=100)
    id = models.IntegerField(db_column='id', verbose_name="id非主键 无自增",auto_created=True)
    alias = models.CharField(max_length=200,unique=True)
    uriDesc = models.CharField(db_column='uriDesc', max_length=5000, default="")
    level = models.IntegerField(default=5, verbose_name="优先级，数字越小越优先显示")
    protocol_CHOICE = (("HTTP", "HTTP"), ("DUBBO", "DUBBO"),)
    protocol = models.CharField(db_column='protocol', max_length=300, default="HTTP",choices=protocol_CHOICE)

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25,db_column='addBy', null=True,verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_config_uri'
        verbose_name = 'URI管理'
        verbose_name_plural = '07URI管理'

    def __str__(self):
        return "%s(%s)" % (self.alias,self.uriKey)

class TbUserUri(models.Model):
    loginName = models.ForeignKey(to=TbUser,to_field="loginName",related_name="TbUserUriLoginname",db_column='loginName', max_length=30, blank=True, default="", verbose_name="执行人登录用户名")
    uriKey = models.ForeignKey(to=TbConfigUri, to_field="uriKey", db_column='uriKey', max_length=20,verbose_name="执行环境的httpConfKey")
    conflevel = models.IntegerField(verbose_name="配置优先级")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25,db_column='addBy', null=True,verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_user_uri'
        unique_together = (('loginName', 'uriKey'),)

class TbRunServerConf(models.Model):
    serviceName = models.CharField(db_column="serviceName",max_length=30,verbose_name="执行机名称",default="")
    serviceIp = models.CharField(db_column="serviceIp",max_length=30,verbose_name="执行机服务器的IP",default="")
    servicePort = models.IntegerField(db_column="servicePort",verbose_name="执行机服务器的端口")
    maxTaskProgressNum = models.IntegerField(default=10,db_column="maxTaskProgressNum",verbose_name="当前服务器最大任务进程数")
    maxCaseProgressNum = models.IntegerField(default=10,db_column="maxCaseProgressNum",verbose_name="当前服务器最大调试进程数")
    status = models.IntegerField(db_column="status",verbose_name="当前执行机的状态")   # 0:离线 1:在线 不可更改

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25,db_column='addBy', null=True,verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_run_server_conf'

class TbEnvUriConf(models.Model):
    httpConfKey = models.CharField(db_column='httpConfKey',  max_length=50, verbose_name="http服务的key，用例调试、任务执行时，会根据此key来获取对应的http的config信息")
    uriKey = models.CharField(db_column='uriKey',  max_length=100)
    requestAddr = models.TextField(db_column='requestAddr', verbose_name="请求地址")

    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25,db_column='addBy', null=True,verbose_name="创建者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb_env_uri_conf'
        verbose_name = '环境服务配置'
        verbose_name_plural = '08环境服务配置管理'
        unique_together = (('httpConfKey', 'uriKey'),)

    def __str__(self):
        return "%s->%s" % (self.httpConfKey,self.uriKey)
