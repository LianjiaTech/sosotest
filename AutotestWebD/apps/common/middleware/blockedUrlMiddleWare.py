from django.utils.deprecation import MiddlewareMixin
import logging

from apps.common.func.CommonFunc import TbAdminUser,NO_AUTH_URLS,TbAdminManageUserPermissionRelation,TbAdminManagePermission,render


logger = logging.getLogger("django")
class blockedUrlMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        requestUrl = request.path
        if requestUrl.startswith("/myadmin") and requestUrl.endswith("/check"):
            currentUser = request.session.get("adminLoginName")
            urlsList = []
            if "adminAudit" in request.session and request.session["adminAudit"] == 1:
                adminUser = TbAdminUser.objects.get(loginName=currentUser, state=1)
                if adminUser.superManager == 1:
                    return

            if requestUrl in NO_AUTH_URLS:
                return

            '''当前用户的权限'''
            userPermissions = TbAdminManageUserPermissionRelation.objects.filter(loginName=currentUser, state=1)
            if len(userPermissions) != 0:
                for userPermission in userPermissions:
                    try:
                        url = TbAdminManagePermission.objects.get(permissionKey=userPermission.permissionKey).permissionValue
                        urlsList.append(url)
                    except:
                        return render(request, "myadmin/returnHome.html", {})
            urlsList.append("/myadmin/changeLog/check")
            urlsList.append("/myadmin/userLog/check")
            urlsList.append("/myadmin/dataStorage/check")
            urlsStr = ",".join(urlsList)
            logger.info("urlsStr: %s" % urlsStr)
            if urlsStr.lower().find(requestUrl.lower()) < 0:
                return render(request, "myadmin/returnHome.html", {})