from apps.common.func.WebFunc import *
class PageObjectService(object):
    @staticmethod
    def updatePageObject(pageObjectData):
        tbModel = TbUiPageObject.objects.filter(id=pageObjectData["id"])
        tbModel.update(**pageObjectData)