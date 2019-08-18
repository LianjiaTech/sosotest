from all_models.models import TbAdminTeamPermissionRelation

class TeamPermissionRelationService(object):

    @staticmethod
    def updateTeamPermission(teamPermissionData):
        tbModel = TbAdminTeamPermissionRelation.objects.filter(id=teamPermissionData["id"])
        tbModel.update(**teamPermissionData)
