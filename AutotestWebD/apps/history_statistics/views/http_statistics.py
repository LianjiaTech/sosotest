from apps.common.func.CommonFunc import *
from apps.common.func.LanguageFunc import *
from apps.common.config import commonWebConfig
from django.shortcuts import *
from urllib import parse
def http_statisticsCheck(request):
    langDict = getLangTextDict(request)
    context = {}
    if not isRelease:
        context["env"] = "test"
    context["history_statistics"] = "current-page"
    context["userName"] = request.session.get("userName")
    #文本
    text = {}
    text["pageTitle"] = langDict["web"]["httpInterfacePageHeadings_check"]
    context["text"] = text

    context["page"] = 1
    return render(request,"InterfaceTest/history_statistics/HTTP_statistics.html",context)

def queryStatistics(request):
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        return HttpResponse("<script>alert('请验证页数参数');</script>")

    checkArr = json.loads(parse.unquote(request.POST.get("queryArr")))
    orderBy = request.POST.get("orderBy")
    if isSqlInjectable(orderBy):
        return HttpResponse("<script>alert('查询条件非法');</script>")

    # "SElECT s.*,u.userName,tch.alias from tb_interface_execute_history s LEFT JOIN tb_user u ON s.addBy = u.loginName LEFT JOIN tb_config_http tch ON s.httpConfKey = tch.httpConfKey WHERE 1=1 and s.state=1"

    execSql =  """SELECT s.id id,s.interfaceUrl,s.requestHost,sum(s.totalCount) countTotal,sum(s.passCount) countPass,sum(s.failCount) countFail,sum(s.errorCount) countError,sum(s.exceptionCount) countException,s.taskExecuteId,s.taskId,s.title,s.taskdesc,s.httpConfKey,s.execBy,s.testReportUrl,s.addBy,tch.alias alias,u.userName FROM tb_interface_execute_history s LEFT JOIN tb_user u ON s.addBy = u.loginName LEFT JOIN tb_config_http tch ON s.httpConfKey = tch.httpConfKey WHERE 1=1 and s.state=1"""

    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        elif key == "execBy":
            checkList.append("%%%s%%" % checkArr[key])
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and (s.addBy LIKE %s or u.userName LIKE %s) """
            continue
        elif key == 'httpConfKey':
            checkList.append("%%%s%%" % checkArr[key])
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and (s.httpConfKey LIKE %s or tch.alias LIKE %s)"""
            continue
        elif key == "taskId" or key == "execTaskId":
            execSql += """ and s.%s = "%s" """ % (key,checkArr[key])
            continue
        elif key == "startTime":
            execSql += """ and s.addTime >= "%s" """ % checkArr[key]
            continue
        elif key == "endTime":
            execSql += """ and s.modTime <= "%s" """ % checkArr[key]
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and s.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """GROUP BY s.interfaceUrl ORDER BY %s """ % orderBy
    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.historypageNum)
    response = render(request, "InterfaceTest/history_statistics/SubPages/HTTP_statistics_list.html", context)
    return response