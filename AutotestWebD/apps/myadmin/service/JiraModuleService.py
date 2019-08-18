from all_models.models import TbjiraModule


class JiraModuleService(object):

    @staticmethod
    def updateJiraModule(jiraModuleData):
        tbModel = TbjiraModule.objects.filter(id=jiraModuleData["id"])
        tbModel.update(**jiraModuleData)
