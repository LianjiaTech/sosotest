from apps.common.model.RedisDBConfig import logger
from all_models.models import TbAdminUserTeamRelation

class TeamUserRelationService(object):

    @staticmethod
    def updateTeamUser(teamUserData):
        tbModel = TbAdminUserTeamRelation.objects.filter(id=teamUserData["id"])
        tbModel.update(**teamUserData)

