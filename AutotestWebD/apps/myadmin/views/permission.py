# Create your views here.
from apps.common.func.WebFunc import *
from apps.common.config import commonWebConfig
from urllib import parse



logger = logging.getLogger("django")

def permissionCheckPage(request):
    context = {}
    context["permission_check"] = "active"
    return render(request, "myadmin/permission/admin_permission_check.html", context)

def getPermission(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy", "")
    page = request.POST.get("page")

    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "单接口管理->查看用例->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT t.* from tb_admin_permissions t WHERE 1=1 "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and t.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql,attrList=checkList,page=page,pageNum=commonWebConfig.userPageNum)

    response = render(request, "myadmin/permission/subPages/permission_sub_page.html",context)
    return response


