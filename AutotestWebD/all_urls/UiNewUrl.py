from django.conf.urls import url
from apps.ui_globals.views import global_vars_conf, global_text_conf
from apps.config.views import http_conf
from apps.ui_main.views import page_object,ui_testcase,ui_function

urlpatterns = [
    url(r'^ui/GetVarsConf', global_vars_conf.getVarsConf, name="ui_getVarsConf"),
    url(r'^ui/GetTextConf', global_text_conf.getTextConf, name="ui_getTextConf"),
    # 全局变量
    url(r'^ui/uiGlobalVarsConf$', global_vars_conf.globalVarsCheck, name="ui_GlobalVarsConf"),
    url(r'^ui/uiGlobalVarsConfListPage$', global_vars_conf.queryVars, name="ui_GlobalVarsConfListPage"),
    url(r'^ui/uiGlobalVarsAdd$', global_vars_conf.varsConfAdd, name="ui_GlobalVarsAdd"),
    url(r'^ui/uiGlobalVarsDel$', global_vars_conf.varsConfDel, name="ui_GlobalVarsDel"),
    url(r'^ui/uiGlobalVarsEdit$', global_vars_conf.varsConfEdit, name="ui_GlobalVarsEdit"),
    # 组合文本
    url(r'^ui/uiGlobalTextConf$', global_text_conf.globalTextCheck, name="ui_GlobalTextConf"),
    url(r'^ui/uiGlobalTextConfListPage$', global_text_conf.queryText, name="ui_GlobalTextConfListPage"),
    url(r'^ui/uiGlobalTextAdd$', global_text_conf.textConfAdd, name="ui_GlobalTextAdd"),
    url(r'^ui/uiGlobalTextDel$', global_text_conf.textConfDel, name="ui_GlobalTextDel"),
    url(r'^ui/uiGlobalTextEdit$', global_text_conf.textConfEdit, name="ui_GlobalTextEdit"),
    ###获取UI的配置，也就是UI的httpConfiList
    url(r'^ui/getUIConf$', http_conf.getUiConf, name="ui_getUIConf"),
    #PageObject相关的
    url(r'^ui/pageObjectIndex$', page_object.showPOindex, name="ui_pageObjectIndex"),
    url(r'^ui/pageObjectList$', page_object.queryPageObjects, name="ui_pageObjectList"),
    url(r'^ui/uiPageObjectConfListPage$', page_object.queryText, name="ui_pageObejctConfListPage"),

    # url(r'^ui/pageObjectAddIndex$', page_object.addPOindex, name="ui_pageObjectAddIndex"),
    url(r'^ui/pageObjectAddIndex$', page_object.addPOindex, name="ui_pageObjectAddIndex"),
    # url(r'^ui/pageObjectAddList$', page_object.queryPageObjectsList, name="ui_pageObjectAddList"),

    url(r'^ui/pageObjectAddIndex$', page_object.addPOindex, name="ui_pageObjectAddIndex"),
]