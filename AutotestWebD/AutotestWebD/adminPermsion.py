from AutotestWebD.settings import *
from apps.common.func.WebFunc import *
from all_models.models import *
from apps.webportal.services.webPortalService import WebPortalService


def adminPermsion(request):
    context = {}
    currentUser = request.session.get("adminLoginName")

    if request.path.startswith('/myadmin'):
        adminUserList = dbModelListToListDict(TbAdminUser.objects.filter(loginName=currentUser, superManager=1, state=1))
        if len(adminUserList) == 0:
            context["isTeamLeader"] = 1
        else:
            context["isTeamLeader"] = 0

    isSuperManager = ""
    userPermissions = TbAdminManageUserPermissionRelation.objects.filter(loginName=currentUser, state=1)
    permissions = TbAdminManagePermission.objects.filter(state=1)
    permissionKeys = []

    if "adminAudit" in request.session and request.session["adminAudit"] == 1:
        user = TbAdminUser.objects.get(loginName=currentUser, state=1)
        isSuperManager = user.superManager
        '''判断是否是超级管理员，是超级管理员，获得所有的权限列表；不是，获得授权的权限列表'''
        if isSuperManager == 1:
            if len(permissions) != 0:
                for permission in permissions:
                    permissionKeys.append(permission.permissionKey)
        else:
            if len(userPermissions) != 0:
                for userpermission in userPermissions:
                    permissionKeys.append(userpermission.permissionKey)
    context["permissionKeys"] = permissionKeys
 

    if "adminAudit" in request.session and request.session["adminAudit"] == 1:
        user = TbAdminUser.objects.get(loginName=currentUser, state=1)
        isSuperManager = user.superManager
    context["isSuperManager"] = isSuperManager


    generalSituation = dbModelListToListDict(WebPortalService.getHttpTestGeneralSituation())
    if generalSituation:
        generalSituation[-1]["statisticalDetail"] = json.loads(generalSituation[-1]["statisticalDetail"])
        context["generalSituation"] = generalSituation[-1]

    else:
        context["generalSituation"] = []
    try:
        platformUser = TbAdminUser.objects.get(loginName=request.session.get("loginName",""), state=1)
        context["userIsSuperManager"] = platformUser.superManager
    except:
        context["userIsSuperManager"] = 0
    return context