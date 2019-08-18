from all_models.models import TbJiraBusinessLine


class JiraBusinessLineService(object):

    @staticmethod
    def updateJiraBusinessLine(jiraBusinessLineData):
        tbModel = TbJiraBusinessLine.objects.filter(id=jiraBusinessLineData["id"])
        tbModel.update(**jiraBusinessLineData)
