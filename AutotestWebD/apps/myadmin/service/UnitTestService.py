from all_models.models import TbWebPortalUnitTestService

class UnitTestService(object):

    @staticmethod
    def updataUnitTestService(permissionData):
        tbModel = TbWebPortalUnitTestService.objects.filter(id=permissionData["id"])
        tbModel.update(**permissionData)
