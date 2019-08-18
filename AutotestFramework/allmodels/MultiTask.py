import os,requests
from allmodels.HttpInterface import HttpInterface
from allmodels.HttpTestcase import HttpTestcase
from core.decorator.normal_functions import *
from core.model.TaskBase import TaskBase
from core.tools.CommonFunc import *
from core.tools.DBTool import DBTool
from core.tools.UsualTool import UsualTool
from report.HttpReport import HttpReport
from core.config.InitConfig import EnvConfig
from core.const.GlobalConst import ExecStatus

class MultiTask(TaskBase):

    def __init__(self):
        super(MultiTask, self).__init__()

        self.id = 0  # tb_task_execute的主键id
        self.taskExecuteId = 0  # tb_task_execute的主键id
        self.taskId = ""

        self.title = ""
        self.taskDesc = ""
        self.protocol = "HTTP"
        self.businessLineGroup = ""
        self.modulesGroup = ""
        self.sourceGroup = ""
        self.tasklevel = ""
        self.status = ""
        self.httpConfKeyList = [] #环境列表
        self.confHttpLayerList = [] #配置列表