# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
from django.db import models

class Tb4MockTag(models.Model):

    tagKey = models.CharField(db_column='tagKey', max_length=50, default="", unique=True, verbose_name="mock的tag的key")
    tagAlias = models.CharField(db_column='tagAlias', max_length=200, default="", unique=True, verbose_name="mock的tag的描述")

    #通用基本信息
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25,db_column='addBy',null = True, verbose_name="添加者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb4_mock_tag'

class Tb4MockHttp(models.Model):

    mockId = models.CharField(db_column='mockId', max_length=50, default="",unique=True, verbose_name="mock的ID")
    title = models.CharField(db_column='title', max_length=500, default="", verbose_name="标题")
    describe = models.TextField(db_column='describe', default="", verbose_name="详细描述")
    businessLineId = models.IntegerField(db_column='businessLineId',default=1, verbose_name="业务线id")
    moduleId = models.IntegerField(db_column='moduleId',default=1, verbose_name="模块id")

    #service 和 tag 可以确定要调用哪个url
    uriKey = models.CharField(db_column='uriKey', max_length=50, default="", verbose_name="mock的服务")
    tagKey = models.CharField(db_column='tagKey', max_length=50, default="common", verbose_name="mock的tag的key")
    # mock 请求信息
    reqMethod = models.CharField(db_column='reqMethod', max_length=20, default="GET", verbose_name="请求Method")
    reqUrl = models.CharField(db_column='reqUrl', max_length=255, default="/", verbose_name="请求Url")
    reqParam = models.CharField(db_column='reqParam', max_length=255, default="", verbose_name="请求行参数")
    reqHeader = models.CharField(db_column='reqHeader', max_length=3000, default="", verbose_name="请求头dict")
    reqBody = models.TextField(db_column='reqBody', default="", verbose_name="请求体")

    #mock 响应信息
    respStatusCode = models.CharField(db_column='respStatusCode', max_length=5, default="",  verbose_name="状态码")
    respStatusReason =  models.CharField(db_column='respStatusReason', max_length=50, default="",  verbose_name="状态文本")
    respContentType =  models.CharField(db_column='respContentType', max_length=100, default="",  verbose_name="响应类型-html json等")
    respBody = models.TextField(db_column='respBody', default="", verbose_name="响应体")
    respCookie = models.CharField(db_column='respCookie', max_length=2048, default="", verbose_name="设置cookie到请求端，json")
    respHeader = models.CharField(db_column='respHeader', max_length=2048, default="", verbose_name="设置header到请求端，json")
    respCharset = models.CharField(db_column='respCharset', max_length=20, default="", verbose_name="响应编码")

    mockMode = models.IntegerField(db_column='mockMode', default=0, verbose_name="mock模式 0 普通mormal模式 1 高级advanced模式")
    #高级信息
    advancedPythonCode = models.TextField(db_column='advancedPythonCode', default="", verbose_name="高级模式的code")

    #mock信息关联的interfaceId列表
    interfaceIds = models.TextField(db_column='interfaceIds', default="", verbose_name="接口ID列表，例如HTTP_INTERFACE_1,HTTP_INTERFACE_2,")

    #通用基本信息
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25,db_column='addBy',null = True, verbose_name="添加者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb4_mock_http'


class Tb4MockHttpInvokeHistory(models.Model):

    mockId = models.CharField(db_column='mockId', max_length=50, default="", verbose_name="mock的ID")
    title = models.CharField(db_column='title', max_length=500, default="", verbose_name="标题")
    businessLineId = models.IntegerField(db_column='businessLineId',default=1, verbose_name="业务线id")
    moduleId = models.IntegerField(db_column='moduleId',default=1, verbose_name="模块id")

    uriKey = models.CharField(db_column='uriKey', max_length=50, default="", verbose_name="mock的服务")
    tagKey = models.CharField(db_column='tagKey', max_length=50, default="common", verbose_name="mock的tag的key")
    # mock 请求信息
    reqMethod = models.CharField(db_column='reqMethod', max_length=20, default="GET", verbose_name="请求Method")
    reqUrl = models.CharField(db_column='reqUrl', max_length=255, default="/", verbose_name="请求Url")
    reqParam = models.CharField(db_column='reqParam', max_length=255, default="", verbose_name="请求行参数")
    reqHeader = models.CharField(db_column='reqHeader', max_length=3000, default="", verbose_name="请求头dict")
    reqBody = models.TextField(db_column='reqBody', default="", verbose_name="请求体")

    #mock 响应信息
    respStatusCode = models.CharField(db_column='respStatusCode', max_length=5, default="200",  verbose_name="状态码")
    respStatusReason =  models.CharField(db_column='respStatusReason', max_length=50, default="OK",  verbose_name="状态文本")
    respContentType =  models.CharField(db_column='respContentType', max_length=100, default="",  verbose_name="响应类型-html json等")
    respBody = models.TextField(db_column='respBody', default="", verbose_name="响应体")
    respCookie = models.CharField(db_column='respCookie', max_length=2048, default="", verbose_name="设置cookie到请求端，json")
    respHeader = models.CharField(db_column='respHeader', max_length=2048, default="", verbose_name="设置header到请求端，json")
    respCharset = models.CharField(db_column='respCharset', max_length=20, default="utf8", verbose_name="响应编码")

    mockMode = models.IntegerField(db_column='mockMode', default=0, verbose_name="mock模式 0 普通mormal模式 1 高级advanced模式")
    #高级信息
    advancedPythonCode = models.TextField(db_column='advancedPythonCode', default="", verbose_name="高级模式的code")

    #请求来源
    fromHostIp = models.CharField(db_column="fromHostIp",max_length=16, default="",verbose_name = "请求来源IP")
    httpConfKey = models.CharField(db_column="httpConfKey",max_length=16, default="",verbose_name = "录制来源环境的key")


    #实际信息
    # mock 请求信息
    actualReqUrl = models.CharField(db_column='actualReqUrl', max_length=255, default="/", verbose_name="实际请求Url")
    actualReqParam = models.CharField(db_column='actualReqParam', max_length=255, default="", verbose_name="实际请求行参数")
    actualReqHeader = models.CharField(db_column='actualReqHeader', max_length=3000, default="", verbose_name="实际请求头dict")
    actualReqBody = models.TextField(db_column='actualReqBody', default="", verbose_name="实际请求体")

    #mock 响应信息
    actualRespStatusCode = models.CharField(db_column='actualRespStatusCode', max_length=5, default="200",  verbose_name="实际状态码")
    actualRespStatusReason =  models.CharField(db_column='actualRespStatusReason', max_length=50, default="OK",  verbose_name="实际状态文本")
    actualRespContentType =  models.CharField(db_column='actualRespContentType', max_length=100, default="",  verbose_name="实际响应类型-html json等")
    actualRespBody = models.TextField(db_column='actualRespBody', default="", verbose_name="实际响应体")
    actualRespCookie = models.CharField(db_column='actualRespCookie', max_length=2048, default="", verbose_name="实际设置cookie到请求端")
    actualRespCharset = models.CharField(db_column='actualRespCharset', max_length=20, default="", verbose_name="实际响应编码")

    # 通用基本信息
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, verbose_name="添加者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb4_mock_http_invoke_history'


class Tb4MockFollower(models.Model):
    mockId = models.CharField(db_column='mockId', max_length=50, default="", verbose_name="mock的ID")
    follower = models.CharField(max_length=25,db_column='follower',null = True, verbose_name="关注者邮箱前缀")
    followTime = models.DateTimeField(db_column='followTime', null=True, verbose_name="关注时间")

    # 通用基本信息
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25, db_column='addBy', null=True, verbose_name="添加者登录名")
    modBy = models.CharField(max_length=25, db_column='modBy', null=True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime', auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime', auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb4_mock_follower'