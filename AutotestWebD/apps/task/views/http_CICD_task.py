from apps.common.func.LanguageFunc import *
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from apps.common.model.RedisDBConfig import *
from apps.common.func.CommonFunc import *

def http_task_CICD_check(request):
    context = {}
    return render(request, "InterfaceTest/HTTPTask/HTTP_taskCICDCheck.html", context)


def http_task_get_CICD_sub_page(request):
    try:
        redisCache = RedisCache()
        redisData = redisCache.get_data("CICD_TASK_LIST")
    except ValueError:
        redisData = None
    if redisData and isJson(redisData):
        redisDict = json.loads(redisData)
        if "envList" not in redisDict.keys():
            return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR,message="envList Key 不存在").toJson())
        if "taskList" not in redisDict.keys():
            return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="taskList Key 不存在").toJson())

        pageDatas = []
        for envIndex in redisDict["envList"]:
            for taskIndex in redisDict["taskList"]:
                try:
                    pageDatas.append(dbModelToDict(TbTaskExecute.objects.filter(httpConfKey_id=envIndex,taskId=taskIndex,addBy="ci").filter(~Q(execStatus__in=[1,2,10,11])).last()))
                except:
                    pass
        for dataIndex in pageDatas:
            if dataIndex["version"] == "CurrentVersion":
                dataIndex["versionText"] = TbVersion.objects.get(type=2).versionName
            else:
                dataIndex["versionText"] = TbVersion.objects.get(versionName=dataIndex["version"]).versionName
            dataIndex["taskId"] = dataIndex["taskId"]
            dataIndex["userName"] = TbUser.objects.get(loginName=dataIndex["addBy_id"]).userName

            if dataIndex["testResult"] == "PASS":
                # print(dataIndex["testResultMsg"])
                stopLoop = False
                testResultMsg = json.loads(dataIndex["testResultMsg"])
                for caseIndex in testResultMsg["taskContrastDict"].keys():
                    # print("caseIndex",caseIndex)
                    for caseResultIndex in testResultMsg["taskContrastDict"][caseIndex]["result"]:
                        if caseResultIndex["performanceResult"] != "PASS":
                            dataIndex["testResult"] = "orangePASS"
                            stopLoop = True
                            break
                    if stopLoop:
                        break

    else:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="请检查redis key  CICD_TASK_LIST").toJson())

    return render(request,"InterfaceTest/HTTPTask/SubPages/CICD_task_result_list_page.html",{"pageDatas":pageDatas})

@csrf_exempt
def test(request):
    return render(request,"mock_server/http/test.html",{})