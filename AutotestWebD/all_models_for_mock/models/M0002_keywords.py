from __future__ import unicode_literals
from django.db import models

class Tb4DataKeyword(models.Model):
    title = models.CharField(db_column='title', max_length=255, default="",  verbose_name="标题")
    descText = models.CharField(db_column='descText', max_length=2000, default="", verbose_name="描述")
    keywordKey = models.CharField(db_column='keywordKey', max_length=255, default="", unique=True, verbose_name="自定义关键字的key")
    keywordCode = models.TextField(db_column='keywordCode', default="", verbose_name="自定义关键字的代码")
    status_CHOICE = ((1, "新增"), (2, "审核中"), (3, "审核通过"), (4, "审核未通过"),)
    status = models.IntegerField(default=1, verbose_name="状态",choices=status_CHOICE)
    type = models.CharField(db_column='type', max_length=50, default="DATA_KEYWORD", verbose_name="类型：DATA_KEYWORD PYTHON_CODE")

    #通用基本信息
    state = models.IntegerField(default=1, verbose_name="状态 0删除 1有效")
    addBy = models.CharField(max_length=25,db_column='addBy',null = True, verbose_name="添加者登录名")
    modBy = models.CharField(max_length=25,db_column='modBy',null = True, verbose_name="修改者登录名")
    addTime = models.DateTimeField(db_column='addTime',auto_now_add=True, verbose_name="创建时间")
    modTime = models.DateTimeField(db_column='modTime',auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = 'tb4_data_keyword'
