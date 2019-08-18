from all_models.models import TbOpenApiUri

class OpenApiUriService(object):

    @staticmethod
    def updateOpenApi(permissionData):
        tbModel = TbOpenApiUri.objects.filter(id=permissionData["id"])
        tbModel.update(**permissionData)
