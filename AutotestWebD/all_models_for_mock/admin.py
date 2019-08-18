from django.contrib import admin
from all_models_for_mock.models import *

@admin.register(Tb4DataKeyword)
class Tb4DataKeywordAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'keywordKey','status', 'addTime') #显示字段
    list_per_page = 50 #每页个数
    ordering = ('-id',) #排序
    # list_editable 设置默认可编辑字段
    # list_editable = ['userName', 'email']
    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('id', 'title', 'keywordKey','status', 'addTime') #显示字段
    # 筛选器
    list_filter = ( 'title', 'keywordKey','status', )
    search_fields = ( 'title', 'keywordKey','status', )
    # date_hierarchy = 'addTime'  # 详细时间分层筛选
