import django
import sys,os
rootpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))).replace("\\","/")
# print(rootpath)
syspath=sys.path
sys.path=[]
sys.path.append(rootpath) #指定搜索路径绝对目录
sys.path.extend([rootpath+i for i in os.listdir(rootpath) if i[0]!="."])#将工程目录下的一级目录添加到python搜索路径中
sys.path.extend(syspath)

from datetime import datetime
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *





if __name__ == "__main__":
    TbAdminInterfacePermissionRelation.objects.all().delete()

    permissionsList = []
    #TODO:HTTP单接口
    permission = {}
    permission["permissionName"] = "HTTP单接口_可进入[查看]页面"
    permission["permissionKey"] = "HTTP_INTERFACE_CHECK"
    permission["url"] = "/interfaceTest/HTTP_operationInterface"
    permission["permission"] = "check"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP单接口_可进入[拷贝]页面"
    permission["permissionKey"] = "HTTP_INTERFACE_COPY"
    permission["url"] = "/interfaceTest/HTTP_operationInterface"
    permission["permission"] = "copy"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP单接口_可进入[编辑]页面"
    permission["permissionKey"] = "HTTP_INTERFACE_EDIT"
    permission["url"] = "/interfaceTest/HTTP_operationInterface"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP单接口_可进入[添加]页面"
    permission["permissionKey"] = "HTTP_INTERFACE_ADD"
    permission["url"] = "/interfaceTest/HTTP_InterfaceAddPage"
    permission["permission"] = "add"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP单接口_列表页显示[查看]按钮"
    permission["permissionKey"] = "HTTP_INTERFACE_LIST_CHECK"
    permission["url"] = "/interfaceTest/HTTP_InterfaceListCheck"
    permission["permission"] = "check"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP单接口_列表页显示[拷贝]按钮"
    permission["permissionKey"] = "HTTP_INTERFACE_LIST_COPY"
    permission["url"] = "/interfaceTest/HTTP_InterfaceListCheck"
    permission["permission"] = "copy"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP单接口_列表页显示[编辑]按钮"
    permission["permissionKey"] = "HTTP_INTERFACE_LIST_EDIT"
    permission["url"] = "/interfaceTest/HTTP_InterfaceListCheck"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP单接口_列表页显示[删除]按钮"
    permission["permissionKey"] = "HTTP_INTERFACE_LIST_DELETE"
    permission["url"] = "/interfaceTest/HTTP_InterfaceListCheck"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP单接口_数据[添加]权限"
    permission["permissionKey"] = "HTTP_INTERFACE_DATA_ADD"
    permission["url"] = "/interfaceTest/HTTP_InterfaceAdd"
    permission["permission"] = "add"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP单接口_数据[编辑]权限"
    permission["permissionKey"] = "HTTP_INTERFACE_DATA_EDIT"
    permission["url"] = "/interfaceTest/HTTP_InterfaceSaveEdit"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP单接口_数据[删除]权限"
    permission["permissionKey"] = "HTTP_INTERFACE_DATA_DELETE"
    permission["url"] = "/interfaceTest/HTTP_InterfaceDel"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)


    #TODO:HTTP业务流
    permission = {}
    permission["permissionName"] = "HTTP业务流_可进入[查看]页面"
    permission["permissionKey"] = "HTTP_TESTCASE_CHECK"
    permission["url"] = "/interfaceTest/HTTP_operationTestCase"
    permission["permission"] = "check"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP业务流_可进入[拷贝]页面"
    permission["permissionKey"] = "HTTP_TESTCASE_COPY"
    permission["url"] = "/interfaceTest/HTTP_operationTestCase"
    permission["permission"] = "copy"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP业务流_可进入[编辑]页面"
    permission["permissionKey"] = "HTTP_TESTCASE_EDIT"
    permission["url"] = "/interfaceTest/HTTP_operationTestCase"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP业务流_可进入[添加]页面"
    permission["permissionKey"] = "HTTP_TESTCASE_ADD"
    permission["url"] = "/interfaceTest/HTTP_TestCaseAddPage"
    permission["permission"] = "add"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP业务流_列表页显示[查看]按钮"
    permission["permissionKey"] = "HTTP_TESTCASE_LIST_CHECK"
    permission["url"] = "/interfaceTest/HTTP_TestCaseListCheck"
    permission["permission"] = "check"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP业务流_列表页显示[拷贝]按钮"
    permission["permissionKey"] = "HTTP_TESTCASE_LIST_COPY"
    permission["url"] = "/interfaceTest/HTTP_TestCaseListCheck"
    permission["permission"] = "copy"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP业务流_列表页显示[编辑]按钮"
    permission["permissionKey"] = "HTTP_TESTCASE_LIST_EDIT"
    permission["url"] = "/interfaceTest/HTTP_TestCaseListCheck"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP业务流_列表页显示[删除]按钮"
    permission["permissionKey"] = "HTTP_TESTCASE_LIST_DELETE"
    permission["url"] = "/interfaceTest/HTTP_TestCaseListCheck"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP业务流_数据[添加]权限"
    permission["permissionKey"] = "HTTP_TESTCASE_DATA_ADD"
    permission["url"] = "/interfaceTest/HTTP_TestCaseAdd"
    permission["permission"] = "add"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP业务流_数据[编辑]权限"
    permission["permissionKey"] = "HTTP_TESTCASE_DATA_EDIT"
    permission["url"] = "/interfaceTest/HTTP_TestCaseSaveEdit"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP业务流_数据[删除]权限"
    permission["permissionKey"] = "HTTP_TESTCASE_DATA_DELETE"
    permission["url"] = "/interfaceTest/HTTP_TestCaseDel"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    #TODO:业务流步骤
    permission = {}
    permission["permissionName"] = "HTTP业务流步骤_列表页显示[查看]按钮"
    permission["permissionKey"] = "HTTP_INTERFACE_STEP_LIST_CHECK"
    permission["url"] = "/interfaceTest/HTTP_TestCaseStepListCheck"
    permission["permission"] = "check"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP业务流步骤_列表页显示[拷贝]按钮"
    permission["permissionKey"] = "HTTP_INTERFACE_STEP_LIST_COPY"
    permission["url"] = "/interfaceTest/HTTP_TestCaseStepListCheck"
    permission["permission"] = "copy"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP业务流步骤_列表页显示[编辑]按钮"
    permission["permissionKey"] = "HTTP_INTERFACE_STEP_LIST_EDIT"
    permission["url"] = "/interfaceTest/HTTP_TestCaseStepListCheck"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP业务流步骤_列表页显示[删除]按钮"
    permission["permissionKey"] = "HTTP_INTERFACE_STEP_LIST_DELETE"
    permission["url"] = "/interfaceTest/HTTP_TestCaseStepListCheck"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    #TODO:task
    permission = {}
    permission["permissionName"] = "HTTP任务_可进入[查看]页面"
    permission["permissionKey"] = "HTTP_TASK_CHECK"
    permission["url"] = "/interfaceTest/HTTP_operationTask"
    permission["permission"] = "check"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP任务_可进入[拷贝]页面"
    permission["permissionKey"] = "HTTP_TASK_COPY"
    permission["url"] = "/interfaceTest/HTTP_operationTask"
    permission["permission"] = "copy"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP任务_可进入[编辑]页面"
    permission["permissionKey"] = "HTTP_TASK_EDIT"
    permission["url"] = "/interfaceTest/HTTP_operationTask"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP任务_可进入[添加]页面"
    permission["permissionKey"] = "HTTP_TASK_ADD"
    permission["url"] = "/interfaceTest/HTTP_TaskAddPage"
    permission["permission"] = "add"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP任务_列表页显示[查看]按钮"
    permission["permissionKey"] = "HTTP_TASK_LIST_CHECK"
    permission["url"] = "/interfaceTest/HTTP_TaskListCheck"
    permission["permission"] = "check"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP任务_列表页显示[拷贝]按钮"
    permission["permissionKey"] = "HTTP_TASK_LIST_COPY"
    permission["url"] = "/interfaceTest/HTTP_TaskListCheck"
    permission["permission"] = "copy"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP任务_列表页显示[编辑]按钮"
    permission["permissionKey"] = "HTTP_TASK_LIST_EDIT"
    permission["url"] = "/interfaceTest/HTTP_TaskListCheck"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP任务_列表页显示[删除]按钮"
    permission["permissionKey"] = "HTTP_TASK_LIST_DELETE"
    permission["url"] = "/interfaceTest/HTTP_TaskListCheck"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP任务_列表页显示[执行]按钮"
    permission["permissionKey"] = "HTTP_TASK_LIST_RUN"
    permission["url"] = "/interfaceTest/HTTP_TaskListCheck"
    permission["permission"] = "run"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP任务_列表页显示[去重]按钮"
    permission["permissionKey"] = "HTTP_TASK_LIST_DISTINCT"
    permission["url"] = "/interfaceTest/HTTP_TaskListCheck"
    permission["permission"] = "distinct"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP任务_数据[添加]权限"
    permission["permissionKey"] = "HTTP_TASK_DATA_ADD"
    permission["url"] = "/interfaceTest/HTTP_TaskAddData"
    permission["permission"] = "add"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP任务_数据[编辑]权限"
    permission["permissionKey"] = "HTTP_TASK_DATA_EDIT"
    permission["url"] = "/interfaceTest/HTTP_TaskSaveEdit"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)


    permission = {}
    permission["permissionName"] = "HTTP任务_数据[删除]权限"
    permission["permissionKey"] = "HTTP_TASK_DATA_DELETE"
    permission["url"] = "/interfaceTest/HTTP_TaskDel"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    #TODO:HTTP任务集
    permission = {}
    permission["permissionName"] = "HTTP任务集_可进入[查看]页面"
    permission["permissionKey"] = "HTTP_TASK_SUITE_CHECK"
    permission["url"] = "/interfaceTest/HTTP_operationTaskSuite"
    permission["permission"] = "check"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP任务集_可进入[拷贝]页面"
    permission["permissionKey"] = "HTTP_TASK_SUITE_COPY"
    permission["url"] = "/interfaceTest/HTTP_operationTaskSuite"
    permission["permission"] = "copy"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP任务集_可进入[编辑]页面"
    permission["permissionKey"] = "HTTP_TASK_SUITE_EDIT"
    permission["url"] = "/interfaceTest/HTTP_operationTaskSuite"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP任务集_可进入[添加]页面"
    permission["permissionKey"] = "HTTP_TASK_SUITE_ADD"
    permission["url"] = "/interfaceTest/HTTP_TaskSuiteAddPage"
    permission["permission"] = "add"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP任务集_列表页显示[查看]按钮"
    permission["permissionKey"] = "HTTP_TASK_SUITE_LIST_CHECK"
    permission["url"] = "/interfaceTest/HTTP_TaskSuiteListCheck"
    permission["permission"] = "check"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP任务集_列表页显示[拷贝]按钮"
    permission["permissionKey"] = "HTTP_TASK_SUITE_LIST_COPY"
    permission["url"] = "/interfaceTest/HTTP_TaskSuiteListCheck"
    permission["permission"] = "copy"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP任务集_列表页显示[编辑]按钮"
    permission["permissionKey"] = "HTTP_TASK_SUITE_LIST_EDIT"
    permission["url"] = "/interfaceTest/HTTP_TaskSuiteListCheck"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP任务集_列表页显示[删除]按钮"
    permission["permissionKey"] = "HTTP_TASK_SUITE_LIST_DELETE"
    permission["url"] = "/interfaceTest/HTTP_TaskSuiteListCheck"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP任务集_列表页显示[执行]按钮"
    permission["permissionKey"] = "HTTP_TASK_SUITE_LIST_RUN"
    permission["url"] = "/interfaceTest/HTTP_TaskSuiteListCheck"
    permission["permission"] = "run"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP任务集_数据[添加]权限"
    permission["permissionKey"] = "HTTP_TASK_SUITE_DATA_ADD"
    permission["url"] = "/interfaceTest/HTTP_TaskSuiteAddData"
    permission["permission"] = "add"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP任务集_数据[编辑]权限"
    permission["permissionKey"] = "HTTP_TASK_SUITE_DATA_EDIT"
    permission["url"] = "/interfaceTest/HTTP_TaskSuiteSaveEdit"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "HTTP任务集_数据[删除]权限"
    permission["permissionKey"] = "HTTP_TASK_SUITE_DATA_DELETE"
    permission["url"] = "/interfaceTest/HTTP_TaskSuiteDel"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    #TODO:DUBBO单接口
    permission = {}
    permission["permissionName"] = "DUBBO单接口_可进入[查看]页面"
    permission["permissionKey"] = "DUBBO_INTERFACE_CHECK"
    permission["url"] = "/dubbo/operationInterface"
    permission["permission"] = "check"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO单接口_可进入[拷贝]页面"
    permission["permissionKey"] = "DUBBO_INTERFACE_COPY"
    permission["url"] = "/dubbo/operationInterface"
    permission["permission"] = "copy"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO单接口_可进入[编辑]页面"
    permission["permissionKey"] = "DUBBO_INTERFACE_EDIT"
    permission["url"] = "/dubbo/operationInterface"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO单接口_可进入[添加]页面"
    permission["permissionKey"] = "DUBBO_INTERFACE_ADD"
    permission["url"] = "/dubbo/interfaceAddPage"
    permission["permission"] = "add"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO单接口_列表页显示[查看]按钮"
    permission["permissionKey"] = "DUBBO_INTERFACE_LIST_CHECK"
    permission["url"] = "/dubbo/interfaceListDesc"
    permission["permission"] = "check"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO单接口_列表页显示[拷贝]按钮"
    permission["permissionKey"] = "DUBBO_INTERFACE_LIST_COPY"
    permission["url"] = "/dubbo/interfaceListDesc"
    permission["permission"] = "copy"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO单接口_列表页显示[编辑]按钮"
    permission["permissionKey"] = "DUBBO_INTERFACE_LIST_EDIT"
    permission["url"] = "/dubbo/interfaceListDesc"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO单接口_列表页显示[删除]按钮"
    permission["permissionKey"] = "DUBBO_INTERFACE_LIST_DELETE"
    permission["url"] = "/dubbo/interfaceListDesc"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO单接口_数据[添加]权限"
    permission["permissionKey"] = "DUBBO_INTERFACE_DATA_ADD"
    permission["url"] = "/dubbo/interfaceAdd"
    permission["permission"] = "add"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO单接口_数据[编辑]权限"
    permission["permissionKey"] = "DUBBO_INTERFACE_DATA_EDIT"
    permission["url"] = "/dubbo/interfaceSaveEdit"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO单接口_数据[删除]权限"
    permission["permissionKey"] = "DUBBO_INTERFACE_DATA_DELETE"
    permission["url"] = "/dubbo/interfaceDel"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    # TODO:DUBBO业务流
    permission = {}
    permission["permissionName"] = "DUBBO业务流_可进入[查看]页面"
    permission["permissionKey"] = "DUBBO_TESTCASE_CHECK"
    permission["url"] = "/dubbo/operationTestCase"
    permission["permission"] = "check"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO业务流_可进入[拷贝]页面"
    permission["permissionKey"] = "DUBBO_TESTCASE_COPY"
    permission["url"] = "/dubbo/operationTestCase"
    permission["permission"] = "copy"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO业务流_可进入[编辑]页面"
    permission["permissionKey"] = "DUBBO_TESTCASE_EDIT"
    permission["url"] = "/dubbo/operationTestCase"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO业务流_可进入[添加]页面"
    permission["permissionKey"] = "DUBBO_TESTCASE_ADD"
    permission["url"] = "/dubbo/testCaseAddPage"
    permission["permission"] = "add"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO业务流_列表页显示[查看]按钮"
    permission["permissionKey"] = "DUBBO_TESTCASE_LIST_CHECK"
    permission["url"] = "/dubbo/TestcaseListCheck"
    permission["permission"] = "check"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO业务流_列表页显示[拷贝]按钮"
    permission["permissionKey"] = "DUBBO_TESTCASE_LIST_COPY"
    permission["url"] = "/dubbo/TestcaseListCheck"
    permission["permission"] = "copy"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO业务流_列表页显示[编辑]按钮"
    permission["permissionKey"] = "DUBBO_TESTCASE_LIST_EDIT"
    permission["url"] = "/dubbo/TestcaseListCheck"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO业务流_列表页显示[删除]按钮"
    permission["permissionKey"] = "DUBBO_TESTCASE_LIST_DELETE"
    permission["url"] = "/dubbo/TestcaseListCheck"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO业务流_数据[添加]权限"
    permission["permissionKey"] = "DUBBO_TESTCASE_DATA_ADD"
    permission["url"] = "/dubbo/TestCaseAdd"
    permission["permission"] = "add"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO业务流_数据[编辑]权限"
    permission["permissionKey"] = "DUBBO_TESTCASE_DATA_EDIT"
    permission["url"] = "/dubbo/TestCaseSaveEdit"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO业务流_数据[删除]权限"
    permission["permissionKey"] = "DUBBO_TESTCASE_DATA_DELETE"
    permission["url"] = "/dubbo/TestCaseDel"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    # TODO:DUBBO任务
    permission = {}
    permission["permissionName"] = "DUBBO任务_可进入[查看]页面"
    permission["permissionKey"] = "DUBBO_TASK_CHECK"
    permission["url"] = "/dubbo/operationTask"
    permission["permission"] = "check"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO任务_可进入[拷贝]页面"
    permission["permissionKey"] = "DUBBO_TASK_COPY"
    permission["url"] = "/dubbo/operationTask"
    permission["permission"] = "copy"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO任务_可进入[编辑]页面"
    permission["permissionKey"] = "DUBBO_TASK_EDIT"
    permission["url"] = "/dubbo/operationTask"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO任务_可进入[添加]页面"
    permission["permissionKey"] = "DUBBO_TASK_ADD"
    permission["url"] = "/dubbo/TaskAddPage"
    permission["permission"] = "add"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO任务_列表页显示[查看]按钮"
    permission["permissionKey"] = "DUBBO_TASK_LIST_CHECK"
    permission["url"] = "/dubbo/TaskListCheck"
    permission["permission"] = "check"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO任务_列表页显示[拷贝]按钮"
    permission["permissionKey"] = "DUBBO_TASK_LIST_COPY"
    permission["url"] = "/dubbo/TaskListCheck"
    permission["permission"] = "copy"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO任务_列表页显示[编辑]按钮"
    permission["permissionKey"] = "DUBBO_TASK_LIST_EDIT"
    permission["url"] = "/dubbo/TaskListCheck"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO任务_列表页显示[删除]按钮"
    permission["permissionKey"] = "DUBBO_TASK_LIST_DELETE"
    permission["url"] = "/dubbo/TaskListCheck"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO任务_列表页显示[执行]按钮"
    permission["permissionKey"] = "DUBBO_TASK_LIST_RUN"
    permission["url"] = "/dubbo/TaskListCheck"
    permission["permission"] = "run"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO任务_列表页显示[去重]按钮"
    permission["permissionKey"] = "DUBBO_TASK_LIST_DISTINCT"
    permission["url"] = "/dubbo/TaskListCheck"
    permission["permission"] = "distinct"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO任务_数据[添加]权限"
    permission["permissionKey"] = "DUBBO_TASK_DATA_ADD"
    permission["url"] = "/dubbo/TaskAddData"
    permission["permission"] = "add"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO任务_数据[编辑]权限"
    permission["permissionKey"] = "DUBBO_TASK_DATA_EDIT"
    permission["url"] = "/dubbo/TaskSaveEdit"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO任务_数据[删除]权限"
    permission["permissionKey"] = "DUBBO_TASK_DATA_DELETE"
    permission["url"] = "/dubbo/TaskDel"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    # TODO:DUBBO任务集
    permission = {}
    permission["permissionName"] = "DUBBO任务集_可进入[查看]页面"
    permission["permissionKey"] = "DUBBO_TASK_SUITE_CHECK"
    permission["url"] = "/dubbo/operationTaskSuite"
    permission["permission"] = "check"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO任务集_可进入[拷贝]页面"
    permission["permissionKey"] = "DUBBO_TASK_SUITE_COPY"
    permission["url"] = "/dubbo/operationTaskSuite"
    permission["permission"] = "copy"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO任务集_可进入[编辑]页面"
    permission["permissionKey"] = "DUBBO_TASK_SUITE_EDIT"
    permission["url"] = "/dubbo/operationTaskSuite"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO任务集_可进入[添加]页面"
    permission["permissionKey"] = "DUBBO_TASK_SUITE_ADD"
    permission["url"] = "/dubbo/TaskSuiteAddPage"
    permission["permission"] = "add"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO任务集_列表页显示[查看]按钮"
    permission["permissionKey"] = "DUBBO_TASK_SUITE_LIST_CHECK"
    permission["url"] = "/dubbo/TaskSuiteListCheck"
    permission["permission"] = "check"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO任务集_列表页显示[拷贝]按钮"
    permission["permissionKey"] = "DUBBO_TASK_SUITE_LIST_COPY"
    permission["url"] = "/dubbo/TaskSuiteListCheck"
    permission["permission"] = "copy"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO任务集_列表页显示[编辑]按钮"
    permission["permissionKey"] = "DUBBO_TASK_SUITE_LIST_EDIT"
    permission["url"] = "/dubbo/TaskSuiteListCheck"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO任务集_列表页显示[删除]按钮"
    permission["permissionKey"] = "DUBBO_TASK_SUITE_LIST_DELETE"
    permission["url"] = "/dubbo/TaskSuiteListCheck"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO任务集_列表页显示[执行]按钮"
    permission["permissionKey"] = "DUBBO_TASK_SUITE_LIST_RUN"
    permission["url"] = "/dubbo/TaskSuiteListCheck"
    permission["permission"] = "run"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO任务集_数据[添加]权限"
    permission["permissionKey"] = "DUBBO_TASK_SUITE_DATA_ADD"
    permission["url"] = "/dubbo/TaskSuiteAddData"
    permission["permission"] = "add"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO任务集_数据[编辑]权限"
    permission["permissionKey"] = "DUBBO_TASK_SUITE_DATA_EDIT"
    permission["url"] = "/dubbo/TaskSuiteSaveEdit"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "DUBBO任务集_数据[删除]权限"
    permission["permissionKey"] = "DUBBO_TASK_SUITE_DATA_DELETE"
    permission["url"] = "/dubbo/TaskSuiteDel"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    # TODO:全局变量
    permission = {}
    permission["permissionName"] = "全局变量_列表页显示[查看]按钮"
    permission["permissionKey"] = "GLOBAL_VALS_LIST_CHECK"
    permission["url"] = "/interfaceTest/HTTP_GlobalVarsConfListPage"
    permission["permission"] = "check"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "全局变量_列表页显示[编辑]按钮"
    permission["permissionKey"] = "GLOBAL_VALS_LIST_EDIT"
    permission["url"] = "/interfaceTest/HTTP_GlobalVarsConfListPage"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "全局变量_列表页显示[删除]按钮"
    permission["permissionKey"] = "GLOBAL_VALS_LIST_DELETE"
    permission["url"] = "/interfaceTest/HTTP_GlobalVarsConfListPage"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "全局变量_数据[添加]权限"
    permission["permissionKey"] = "GLOBAL_VALS_DATA_ADD"
    permission["url"] = "/interfaceTest/HTTP_GlobalVarsAdd"
    permission["permission"] = "add"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "全局变量_数据[编辑]权限"
    permission["permissionKey"] = "GLOBAL_VALS_DATA_EDIT"
    permission["url"] = "/interfaceTest/HTTP_GlobalVarsEdit"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "全局变量_数据[删除]权限"
    permission["permissionKey"] = "GLOBAL_VALS_DATA_DELETE"
    permission["url"] = "/interfaceTest/HTTP_GlobalVarsDel"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    # TODO:组合文本
    permission = {}
    permission["permissionName"] = "组合文本_列表页显示[查看]按钮"
    permission["permissionKey"] = "GLOBAL_TEXT_LIST_CHECK"
    permission["url"] = "/interfaceTest/HTTP_GlobalTextConfListPage"
    permission["permission"] = "check"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "组合文本_列表页显示[编辑]按钮"
    permission["permissionKey"] = "GLOBAL_TEXT_LIST_EDIT"
    permission["url"] = "/interfaceTest/HTTP_GlobalTextConfListPage"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "组合文本_列表页显示[删除]按钮"
    permission["permissionKey"] = "GLOBAL_TEXT_LIST_DELETE"
    permission["url"] = "/interfaceTest/HTTP_GlobalTextConfListPage"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "组合文本_数据[添加]权限"
    permission["permissionKey"] = "GLOBAL_TEXT_DATA_ADD"
    permission["url"] = "/interfaceTest/HTTP_GlobalTextAdd"
    permission["permission"] = "add"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "组合文本_数据[编辑]权限"
    permission["permissionKey"] = "GLOBAL_TEXT_DATA_EDIT"
    permission["url"] = "/interfaceTest/HTTP_GlobalTextEdit"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "组合文本_数据[删除]权限"
    permission["permissionKey"] = "GLOBAL_TEXT_DATA_DELETE"
    permission["url"] = "/interfaceTest/HTTP_GlobalTextDel"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    #TODO:请求地址
    permission = {}
    permission["permissionName"] = "请求地址_列表页显示[编辑]按钮"
    permission["permissionKey"] = "ENVURICONF_LIST_EDIT"
    permission["url"] = "/interfaceTest/HTTP_UserEnvUriConfListCheck"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "请求地址_列表页显示[删除]按钮"
    permission["permissionKey"] = "ENVURICONF_LIST_DELETE"
    permission["url"] = "/interfaceTest/HTTP_UserEnvUriConfListCheck"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "请求地址_数据[添加]权限"
    permission["permissionKey"] = "ENVURICONF_DATA_ADD"
    permission["url"] = "/interfaceTest/HTTP_saveEnvUri"
    permission["permission"] = "add"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "请求地址_数据[编辑]权限"
    permission["permissionKey"] = "ENVURICONF_DATA_EDIT"
    permission["url"] = "/interfaceTest/HTTP_SaveEditEnvUri"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "请求地址_数据[删除]权限"
    permission["permissionKey"] = "ENVURICONF_DATA_DELETE"
    permission["url"] = "/interfaceTest/HTTP_DelEnvUri"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    #TODO:环境配置
    permission = {}
    permission["permissionName"] = "环境配置_列表页显示[编辑]按钮"
    permission["permissionKey"] = "HTTP_CONF_LIST_EDIT"
    permission["url"] = "/interfaceTest/HTTP_UserHttpConfListCheck"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "环境配置_列表页显示[删除]按钮"
    permission["permissionKey"] = "HTTP_CONF_LIST_DELETE"
    permission["url"] = "/interfaceTest/HTTP_UserHttpConfListCheck"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "环境配置_数据[添加]权限"
    permission["permissionKey"] = "HTTP_CONF_DATA_ADD"
    permission["url"] = "/interfaceTest/HTTP_HttpConfAdd"
    permission["permission"] = "add"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "环境配置_数据[编辑]权限"
    permission["permissionKey"] = "HTTP_CONF_DATA_EDIT"
    permission["url"] = "/interfaceTest/HTTP_HttpConfEdit"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "环境配置_数据[删除]权限"
    permission["permissionKey"] = "HTTP_CONF_DATA_DELETE"
    permission["url"] = "/interfaceTest/HTTP_HttpConfDel"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    # TODO:服务配置
    permission = {}
    permission["permissionName"] = "服务配置_列表页显示[编辑]按钮"
    permission["permissionKey"] = "HTTP_URI_CONF_LIST_EDIT"
    permission["url"] = "/interfaceTest/HTTP_UserUriConfListCheck"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "服务配置_列表页显示[编辑]按钮"
    permission["permissionKey"] = "HTTP_URI_CONF_LIST_DELETE"
    permission["url"] = "/interfaceTest/HTTP_UserUriConfListCheck"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "服务配置_数据[添加]权限"
    permission["permissionKey"] = "HTTP_URI_CONF_DATA_ADD"
    permission["url"] = "/interfaceTest/HTTP_HttpUriAddApply"
    permission["permission"] = "add"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "服务配置_数据[编辑]权限"
    permission["permissionKey"] = "HTTP_URI_CONF_DATA_EDIT"
    permission["url"] = "/interfaceTest/HTTP_UriConfEdit"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "服务配置_数据[删除]权限"
    permission["permissionKey"] = "HTTP_URI_CONF_DATA_DELETE"
    permission["url"] = "/interfaceTest/HTTP_UriConfDel"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    #TODO:mockServer
    permission = {}
    permission["permissionName"] = "mockServer_列表页显示[查看]按钮"
    permission["permissionKey"] = "HTTP_MOCK_SERVER_LIST_CHECK"
    permission["url"] = "/mockserver/HTTP_InterfaceListCheck"
    permission["permission"] = "check"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "mockServer_列表页显示[拷贝]按钮"
    permission["permissionKey"] = "HTTP_MOCK_SERVER_LIST_COPY"
    permission["url"] = "/mockserver/HTTP_InterfaceListCheck"
    permission["permission"] = "copy"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "mockServer_列表页显示[编辑]按钮"
    permission["permissionKey"] = "HTTP_MOCK_SERVER_LIST_EDIT"
    permission["url"] = "/mockserver/HTTP_InterfaceListCheck"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "mockServer_列表页显示[删除]按钮"
    permission["permissionKey"] = "HTTP_MOCK_SERVER_LIST_DELETE"
    permission["url"] = "/mockserver/HTTP_InterfaceListCheck"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "mockServer_列表页显示[录制]按钮"
    permission["permissionKey"] = "HTTP_MOCK_SERVER_LIST_RECORD"
    permission["url"] = "/mockserver/HTTP_InterfaceListCheck"
    permission["permission"] = "record"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "mockServer_数据[添加]权限"
    permission["permissionKey"] = "HTTP_MOCK_DATA_ADD"
    permission["url"] = "/mockserver/HTTP_InterfaceAdd"
    permission["permission"] = "add"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "mockServer_数据[编辑]权限"
    permission["permissionKey"] = "HTTP_MOCK_DATA_EDIT"
    permission["url"] = "/mockserver/HTTP_InterfaceSaveEdit"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "mockServer_数据[删除]权限"
    permission["permissionKey"] = "HTTP_MOCK_DATA_DELETE"
    permission["url"] = "/mockserver/HTTP_InterfaceDel"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "mockServer_可进入[查看]页面"
    permission["permissionKey"] = "HTTP_MOCK_CHECK"
    permission["url"] = "/mockserver/HTTP_operationInterface"
    permission["permission"] = "check"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "mockServer_可进入[拷贝]页面"
    permission["permissionKey"] = "HTTP_MOCK_COPY"
    permission["url"] = "/mockserver/HTTP_operationInterface"
    permission["permission"] = "copy"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "mockServer_可进入[编辑]页面"
    permission["permissionKey"] = "HTTP_MOCK_EDIT"
    permission["url"] = "/mockserver/HTTP_operationInterface"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "mockServer_可进入[添加]页面"
    permission["permissionKey"] = "HTTP_MOCK_ADD"
    permission["url"] = "/mockserver/HTTP_InterfaceAddPage"
    permission["permission"] = "add"
    permission["isDefault"] = 1
    permissionsList.append(permission)


    #TODO:关键字
    permission = {}
    permission["permissionName"] = "自定义关键字_可进入[查看]页面"
    permission["permissionKey"] = "DATA_KEYWORD_CHECK"
    permission["url"] = "/datakeyword/operationCheck"
    permission["permission"] = "check"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "自定义关键字_可进入[拷贝]页面"
    permission["permissionKey"] = "DATA_KEYWORD_COPY"
    permission["url"] = "/datakeyword/operationCheck"
    permission["permission"] = "copy"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "自定义关键字_可进入[编辑]页面"
    permission["permissionKey"] = "DATA_KEYWORD_EDIT"
    permission["url"] = "/datakeyword/operationCheck"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "自定义关键字_可进入[添加]页面"
    permission["permissionKey"] = "DATA_KEYWORD_ADD"
    permission["url"] = "/datakeyword/addPage"
    permission["permission"] = "add"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "自定义关键字_列表页显示[查看]按钮"
    permission["permissionKey"] = "DATA_KEYWORD_LIST_CHECK"
    permission["url"] = "/datakeyword/listData"
    permission["permission"] = "check"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "自定义关键字_列表页显示[拷贝]按钮"
    permission["permissionKey"] = "DATA_KEYWORD_LIST_COPY"
    permission["url"] = "/datakeyword/listData"
    permission["permission"] = "copy"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "自定义关键字_列表页显示[编辑]按钮"
    permission["permissionKey"] = "DATA_KEYWORD_LIST_EDIT"
    permission["url"] = "/datakeyword/listData"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "自定义关键字_列表页显示[删除]按钮"
    permission["permissionKey"] = "DATA_KEYWORD_LIST_DELETE"
    permission["url"] = "/datakeyword/listData"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "自定义关键字_数据[添加]权限"
    permission["permissionKey"] = "DATA_KEYWORD_DATA_ADD"
    permission["url"] = "/datakeyword/addData"
    permission["permission"] = "add"
    permission["isDefault"] = 1
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "自定义关键字_数据[编辑]权限"
    permission["permissionKey"] = "DATA_KEYWORD_DATA_EDIT"
    permission["url"] = "/datakeyword/saveEditData"
    permission["permission"] = "edit"
    permission["isDefault"] = 0
    permissionsList.append(permission)

    permission = {}
    permission["permissionName"] = "自定义关键字_数据[删除]权限"
    permission["permissionKey"] = "DATA_KEYWORD_DATA_DELETE"
    permission["url"] = "/datakeyword/delData"
    permission["permission"] = "delete"
    permission["isDefault"] = 0
    permissionsList.append(permission)


    for index in permissionsList:
       tbModel = TbAdminInterfacePermissionRelation()
       tbModel.permissionName = index["permissionName"]
       tbModel.permissionKey = index["permissionKey"]
       tbModel.permission = index["permission"]
       tbModel.url = index["url"]
       tbModel.isDefault = index["isDefault"]
       tbModel.save()

    TbAdminTeamPermissionRelation.objects.all().delete()

    allTeam = TbAdminTeam.objects.filter(state=1)
    for teamIndex in allTeam:
        for permissionIndex in permissionsList:
            tb_admin_team_relation = TbAdminTeamPermissionRelation()
            tb_admin_team_relation.teamKey = teamIndex.teamKey
            tb_admin_team_relation.permissionKey = permissionIndex["permissionKey"]
            tb_admin_team_relation.save()
