from all_models.models import TbOpenApiBusinessLine

class OpenApiBusinessLineService(object):

    @staticmethod
    def updatePermission(permissionData):
        tbModel = TbOpenApiBusinessLine.objects.filter(id=permissionData["id"])
        tbModel.update(**permissionData)
