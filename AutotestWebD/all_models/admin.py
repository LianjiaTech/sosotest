from django.contrib import admin
from all_models.models import *
from AutotestWebD.settings import *
admin.site.site_header = SITE_HEADER
admin.site.site_title = SITE_TITLE

@admin.register(TbUser)
class TbUserAdminT(admin.ModelAdmin):
    list_display = ('id', 'loginName', 'userName', 'email','addTime') #显示字段
    list_per_page = 50 #每页个数
    ordering = ('id',) #排序
    # list_editable 设置默认可编辑字段
    list_editable = ['userName', 'email']
    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('id', 'loginName')
    # 筛选器
    list_filter = ('loginName', 'userName', 'email', 'audit')  # 过滤器
    search_fields = ('loginName', 'userName', 'email')  # 搜索字段
    date_hierarchy = 'addTime'  # 详细时间分层筛选


@admin.register(TbBusinessLine)
class TbBusinessLineAdmin(admin.ModelAdmin):
    list_display = ('id', 'bussinessLineName', 'bussinessLineDesc') #显示字段
    list_per_page = 50 #每页个数
    ordering = ('id',) #排序

@admin.register(TbModules)
class TbModulesAdmin(admin.ModelAdmin):
    list_display = ('id', 'moduleName', 'moduleDesc') #显示字段
    list_per_page = 50 #每页个数
    ordering = ('id',) #排序

    list_filter = ('moduleName',)  # 过滤器
    search_fields = ('moduleName',)  # 搜索字段

@admin.register(TbBusinessLineModuleRelation)
class TbBusinessLineModuleRelationAdmin(admin.ModelAdmin):
    list_display = ('id', 'businessLineId', 'moduleId', 'level') #显示字段
    list_per_page = 50 #每页个数
    ordering = ('id',) #排序

    list_filter = ( 'businessLineId', 'moduleId')  # 过滤器
    search_fields = ( 'businessLineId__bussinessLineName', 'moduleId__moduleName')  # 搜索字段

    list_editable = [ 'level',]
    list_display_links = ('businessLineId', 'moduleId',)


@admin.register(TbSource)
class TbSourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'sourceName', 'sourceDesc') #显示字段
    list_per_page = 50 #每页个数
    ordering = ('id',) #排序

    list_filter = ('sourceName',)  # 过滤器
    search_fields = ('sourceName',)  # 搜索字段

@admin.register(TbConfigService)
class TbConfigServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'alias', 'serviceConfDesc') #显示字段
    list_per_page = 50 #每页个数
    ordering = ('id',) #排序

    list_filter = ('alias','serviceConfDesc',)  # 过滤器
    search_fields = ('alias','serviceConfDesc',)  # 搜索字段

@admin.register(TbConfigUri)
class TbConfigUriAdmin(admin.ModelAdmin):
    list_display = ('alias', 'uriKey','protocol','level') #显示字段

    list_per_page = 50 #每页个数
    ordering = ('level',) #排序
    list_editable = [ 'level']
    list_display_links = ('alias','uriKey',)

    list_filter = ('alias','uriKey',)  # 过滤器
    search_fields = ('alias','uriKey',)  # 搜索字段

@admin.register(TbConfigHttp)
class TbConfigHttpAdmin(admin.ModelAdmin):
    list_display = ('id', 'alias', 'httpConfKey','serviceConfKey') #显示字段
    list_per_page = 50 #每页个数
    ordering = ('id',) #排序

    list_filter = ('alias', 'httpConfKey',)  # 过滤器
    search_fields = ('alias', 'httpConfKey',)  # 搜索字段

@admin.register(TbHttpInterfaceDebug)
class TbHttpInterfaceDebugAdmin(admin.ModelAdmin):
    list_display = ('id', 'modTime','interfaceId', 'title','httpConfKey') #显示字段
    ordering = ('-modTime',)  # 排序
    search_fields = ('interfaceId', 'httpConfKey',)  # 搜索字段
    list_per_page = 10 #每页个数


@admin.register(TbHttpTestcaseDebug)
class TbHttpTestcaseDebugAdmin(admin.ModelAdmin):
    list_display = ('id','modTime', 'caseId', 'title','httpConfKey') #显示字段
    ordering = ('-modTime',)  # 排序
    search_fields = ('caseId', 'httpConfKey',)  # 搜索字段
    list_per_page = 10 #每页个数


@admin.register(TbHttpTestcaseStepDebug)
class TbHttpTestcaseStepDebugAdmin(admin.ModelAdmin):
    list_display = ('id', 'modTime', 'caseId', 'title','httpConfKey') #显示字段
    ordering = ('-modTime',)  # 排序
    search_fields = ('caseId', 'httpConfKey',)  # 搜索字段
    list_per_page = 10 #每页个数


@admin.register(TbTaskExecute)
class TbTaskExecuteAdmin(admin.ModelAdmin):
    list_display = ('id', 'modTime','taskId', 'title', 'httpConfKey')  # 显示字段
    ordering = ('-modTime',)  # 排序
    search_fields = ('taskId', 'httpConfKey',)  # 搜索字段
    list_per_page = 10 #每页个数

@admin.register(TbExecPythonAttrs)
class TbExecPythonAttrsAdmin(admin.ModelAdmin):
    list_display = ('id', 'execPythonAttr','execPythonDesc','execPythonValue')  # 显示字段
    ordering = ('id',)  # 排序
    list_per_page = 10 #每页个数

@admin.register(TbWebPortalStandardTask)
class TbWebPortalStandardTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'version','businessLine','team','head','taskId','state')  # 显示字段
    ordering = ('-id',)  # 排序
    list_per_page = 10 #每页个数

@admin.register(TbWebPortalStandardEnv)
class TbWebPortalStandardEnvAdmin(admin.ModelAdmin):
    list_display = ('id', 'httpConfKey','openApiKey','rmiKey','version','actionIsShow','rmiIsShow','openapiIsShow','uiIsShow','alias','lineSort')  # 显示字段
    ordering = ('-id',)  # 排序
    list_per_page = 10 #每页个数

@admin.register(TbVersion)
class TbVersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'versionName','type','closeTime')  # 显示字段
    ordering = ('-id',)  # 排序
    list_per_page = 10 #每页个数

@admin.register(TbUserLog)
class TbUserLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'loginName','userName','operationUrl','operationDesc','operationResult','fromHostIp','addTime')  # 显示字段
    ordering = ('-id',)  # 排序
    list_per_page = 50 #每页个数

    list_filter = ( 'operationResult','operationUrl', )  # 过滤器
    search_fields = ('loginName','userName','operationUrl', 'operationResult','operationDesc')  # 搜索字段


@admin.register(TbOpenApiBusinessLine)
class TbOpenApiBusinessLineAdmin(admin.ModelAdmin):
    list_display = ('id', "businessLineName","businessLineDesc",'addTime')  # 显示字段
    ordering = ('-id',)  # 排序
    list_per_page = 20 #每页个数

@admin.register(TbOpenApiUri)
class TbOpenApiUriAdmin(admin.ModelAdmin):
    list_display = ('id', 'summaryUri','summaryUrl','interfaceTestUri','interfaceTestUrl','addTime')  # 显示字段
    ordering = ('-id',)  # 排序
    list_per_page = 20 #每页个数

@admin.register(TbWebPortalUnitTestService)
class TbUnitTestServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'serviceName','serviceDesc','isShow','level','addTime')  # 显示字段
    ordering = ('-id',)  # 排序
    list_per_page = 20 #每页个数


@admin.register(TbJiraBusinessLine)
class TbJiraBusinessLineAdmin(admin.ModelAdmin):
    list_display = ('id', 'businessLineName','businessLineDesc','state')  # 显示字段
    ordering = ('-id',)  # 排序
    list_per_page = 20 #每页个数

@admin.register(TbJiraBusinessLinePlatFormRelation)
class TbJiraBusinessLinePlatFormRelationAdmin(admin.ModelAdmin):
    list_display = ('id', 'jiraBusinessLineId', 'platformBusinessLineId') #显示字段
    list_per_page = 50 #每页个数
    ordering = ('-id',) #排序
    list_filter = ('jiraBusinessLineId', 'platformBusinessLineId')

    search_fields = ('jiraBusinessLineId', 'platformBusinessLineId')  # 搜索字段

    list_display_links = ('jiraBusinessLineId', 'platformBusinessLineId',)

@admin.register(TbjiraModule)
class TbjiraModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'moduleName','moduleDesc','state')  # 显示字段
    ordering = ('-id',)  # 排序
    list_per_page = 20 #每页个数

@admin.register(TbJiraModulePlatFormRelation)
class TbJiraModulePlatFormRelationAdmin(admin.ModelAdmin):
    list_display = ('id', 'jiraModuleId','platformModuleId')  # 显示字段
    ordering = ('-id',)  # 排序
    list_per_page = 20 #每页个数d

@admin.register(TbUiMobileServer)
class TbUIMobileServerAdmin(admin.ModelAdmin):
    list_display = ('id','serverName','serverDesc','serverType','serverIp','serverPort','status','addBy')
    ordering = ('-id',)
    list_per_page = 20  # 每页个数

#增加任务编辑功能，添加收件人列表之类的
@admin.register(TbTask)
class TbTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'taskId', 'title','businessLineGroup','modulesGroup','addBy') #显示字段
    list_per_page = 50 #每页个数
    ordering = ('id',) #排序

    list_filter = ('title',)  # 过滤器
    search_fields = ('title',)  # 搜索字段