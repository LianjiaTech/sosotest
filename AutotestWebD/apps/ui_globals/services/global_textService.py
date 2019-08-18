import apps.common.func.InitDjango
from all_models_for_ui.models import Tb3UIGlobalText
from django.db import connection
from django.forms.models import model_to_dict
from apps.common.func.CommonFunc import *
from all_models.models.A0011_version_manage import TbVersionGlobalText

class global_textService(object):

    @staticmethod
    def delText(id):
        delResult = Tb3UIGlobalText.objects.get(id=id)
        delResult.state = 0
        delResult.save()

    @staticmethod
    def delVersionText(id):
        delResult = TbVersionGlobalText.objects.get(id=id)
        delResult.state = 0
        delResult.save()

    @staticmethod
    def getText(id):
        return Tb3UIGlobalText.objects.filter(id=id)[0]

    @staticmethod
    def getVersionText(id):
        return TbVersionGlobalText.objects.filter(id=id)[0]

    @staticmethod
    def addText(varData):
        return Tb3UIGlobalText.objects.create(**varData)

    @staticmethod
    def addVersionText(varData,versionName):
        varData['versionName_id'] = versionName
        varData['addTime'] = datetime.datetime.now()
        varData['modTime'] = datetime.datetime.now()
        return TbVersionGlobalText.objects.create(**varData)

    @staticmethod
    def editText(varData):
        varDBData = Tb3UIGlobalText.objects.get(id=varData["id"])
        varDBData.textDesc = varData["textDesc"]
        varDBData.textValue = varData["textValue"]
        varDBData.save()

    @staticmethod
    def editVersionText(varData,versionName):
        varDBData = TbVersionGlobalText.objects.get(id=varData["id"])
        varDBData.textDesc = varData["textDesc"]
        varDBData.textValue = varData["textValue"]
        varDBData.save()

if __name__ == "__main__":
    # print((HTTP_test_caseService.getTestCaseForIdToDict("23")))
    # print(UserService.getUserByLoginname(UserService.getUsers()[0].loginname))
    # HTTP_test_caseService.testCaseAdd("")
    pass

