from urllib import parse

from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *

logger = logging.getLogger("django")

def dataStorageCheckPage(request):
    context = {}
    context["dataStorage_check"] = "active"
    return render(request, "myadmin/dataStorage/admin_dataStorage_check.html", context)

def getdataStorage(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy", "")
    page = request.POST.get("page")

    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "单接口管理->查看用例->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT t.* from tb_admin_manage_permission t WHERE 1=1 "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and t.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql,attrList=checkList,page=page,pageNum=commonWebConfig.userPageNum)

    response = render(request, "myadmin/dataStorage/subPages/dataStorage_sub_page.html", context)
    return response


def getPermissionForId(request):
    permissionId = request.POST.get("permissionId")
    try:
        permissionData = TbAdminManagePermission.objects.get(id=permissionId)
    except Exception as e:
        message = "权限查询出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())
    return HttpResponse(ApiReturn(body=dbModelToDict(permissionData)).toJson())

