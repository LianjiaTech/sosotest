import apps.common.func.InitDjango
from all_models_for_ui.models import Tb3UIGlobalText
from django.db import connection
from django.forms.models import model_to_dict
from apps.common.func.CommonFunc import *
from all_models.models.A0011_version_manage import TbVersionGlobalText

class UITestcaseService(object):

    @staticmethod
    def delText(id):
        delResult = Tb3UIGlobalText.objects.get(id=id)
        delResult.state = 0
        delResult.save()


if __name__ == "__main__":
    # print((HTTP_test_caseService.getTestCaseForIdToDict("23")))
    # print(UserService.getUserByLoginname(UserService.getUsers()[0].loginname))
    # HTTP_test_caseService.testCaseAdd("")
    pass

