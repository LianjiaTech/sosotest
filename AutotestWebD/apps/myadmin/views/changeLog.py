from urllib import parse

# Create your views here.
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *

logger = logging.getLogger("django")

def changeLogCheckPage(request):
    context = {}
    context["adminUserChangeLog_check"] = "active"
    return render(request,"myadmin/changeLog/admin_changeLog_check.html",context)

def getChangeLog(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy","")
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "单接口管理->查看用例->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT u.* from tb_user_change_log u WHERE 1=1 "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and u.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql,attrList=checkList,page=page,pageNum=commonWebConfig.userPageNum)
    response = render(request, "myadmin/changeLog/subPages/changeLog_sub_page.html", context)

    return response

def getChangeLogDataForId(request):
    changeLogId = request.POST.get("changeLogId")
    changeLogObject = TbUserChangeLog.objects.get(id=changeLogId)
    detailsDict = {}
    detailsDict["beforeData"] = changeLogObject.beforeChangeData
    detailsDict["afterData"] = changeLogObject.afterChangeData
    return HttpResponse(ApiReturn(body=detailsDict).toJson())

