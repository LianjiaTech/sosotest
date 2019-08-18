import apps.common.func.InitDjango
from all_models.models import *

class AdminLoginService(object):

    @staticmethod
    def getUserLoginType(loginName,passWord):
        return TbAdminUser.objects.filter(loginName=loginName, passWord=passWord, state=1)