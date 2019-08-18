from django.contrib import admin
from all_models_for_dubbo.models import *
from AutotestWebD.settings import *
admin.site.site_header = SITE_HEADER
admin.site.site_title = SITE_TITLE

@admin.register(Tb0ErrorLog)
class Tb0ErrorLogT(admin.ModelAdmin):
    list_display = ('id', 'title', 'errorLogText', 'addTime','state') #显示字段
    list_per_page = 50 #每页个数
    ordering = ('-id',) #排序
    # list_editable 设置默认可编辑字段
    # list_editable = ['userName', 'email']
    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('id', 'title', 'errorLogText', 'addTime')
    # 筛选器
    list_filter = ( 'title', 'errorLogText',)
    search_fields = ( 'title', 'errorLogText',)
    # date_hierarchy = 'addTime'  # 详细时间分层筛选
