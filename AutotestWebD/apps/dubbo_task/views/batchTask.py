import threading
from django.shortcuts import HttpResponse,render
from apps.common.func.CommonFunc import *
from all_models.models import *
from apps.common.model.RedisDBConfig import *
class batchTaskThread(threading.Thread):
    def __init__(self,tbModule):
        super(batchTaskThread, self).__init__()
        self.tbModule = tbModule

    def run(self):
        print(self.tbModule.id)
        self.tbModule.status = 2
        taskList = self.tbModule.taskIdList.split(',')
        runMsg = []
        for taskIndex in taskList:
            print(taskIndex)
            thisTask = dbModelToDict(TbTask.objects.filter(taskId=taskIndex).last())
            thisTaskId = thisTask["taskId"]
            thisTaskMsg = {}
            thisTaskMsg[thisTaskId] = {"insertDB": "未执行", "sendTCP": "未执行","exception":""}
            try:
                thisTask["taskId"] = thisTask["taskId"]
                thisTask["protocol"] = "DUBBO"
                thisTask["addBy_id"] = self.tbModule.addBy
                thisTask["isSaveHistory"] = self.tbModule.isSaveHistory
                thisTask["isSendEmail"] = self.tbModule.isSendEmail
                thisTask["execBy_id"] = self.tbModule.addBy
                thisTask["version"] = self.tbModule.version
                thisTask["httpConfKey_id"] = self.tbModule.httpConfKey
                thisTask["caseLevel"] = self.tbModule.caseLevel
                del thisTask["id"]
                del thisTask["taskId"]
                taskExecute = dbModelToDict(TbTaskExecute.objects.create(**thisTask))
                thisTaskMsg[thisTaskId]["insertDB"] = "已执行"
                RedisCache().set_data("%s_taskExecute_%s" % ("DUBBO", taskExecute["id"]), "0:0:0:0:0")
                RedisCache().set_data("%s_taskExecuteStatus_%s" % ("DUBBO", taskExecute["id"]), "1")
                tcpin = '{"do":3,"TaskExecuteId":%s,"TaskId":"%s","TaskExecuteEnv":"%s","protocol":"DUBBO"}' % (taskExecute["id"],taskExecute["taskId"],self.tbModule.httpConfKey,)
                retApiResult = send_tcp_request(tcpin)
                if retApiResult.code != ApiReturn.CODE_OK:
                    thisTaskMsg[thisTaskId]["exception"] = "任务执行添加成功，但是执行服务出现异常，请联系管理员"
                else:
                    thisTaskMsg[thisTaskId]["sendTCP"] = "已发送"
            except Exception as e:
                print("Exception %s " % e)
                traceback.format_exc(e)
                thisTaskMsg[thisTaskId]["exception"] = "发生异常，异常信息为 %s" % e
                self.tbModule.status = 4
                self.tbModule.testResult = "EXCEPTION"
                continue
            runMsg.append(thisTaskMsg)
        self.tbModule.executeMsg = json.dumps(runMsg)
        if self.tbModule.status == 2:
            self.tbModule.status = 3
            self.tbModule.testResult = "DONE"
        self.tbModule.save()


#参数是业务线，任务优先级，用例优先级，环境，是否发送邮箱，是否记录到历史信息，还有taskIdlist
def batchTask(request):
    return render(request,"InterfaceTest/HTTPTask/batchTask.html")


def executeBatchTask(request):

    #token 必填参数
    token = request.GET.get("token","")
    if not token:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="token不能为空").toJson())
    if not TbUser.objects.filter(token=token).last():
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="token找不到正确用户").toJson())


    #httpConf  这个得必填
    httpConfKey = request.GET.get("httpConfKey", "")
    if httpConfKey == "":
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="httpConfKey不能为空").toJson())

    if not TbConfigHttp.objects.filter(httpConfKey=httpConfKey).last() :
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="httpConfKey找不到对应的key").toJson())

    businessLine = request.GET.get("businessLine", "")
    if businessLine and not TbBusinessLine.objects.filter(bussinessLineName=businessLine).last():
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="businessLine找不到对应的业务线").toJson())

    levelDict = {"高":0,"中":5,"低":9}

    #用例优先级 可选
    caseLevel = request.GET.get("caseLevel", "")
    if caseLevel == "":
        caseLevel = "低"

    if caseLevel not in levelDict.keys():
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="caseLevel只能为【高，中，低】").toJson())

    #任务集合 可选 用逗号分隔
    taskList = request.GET.get("taskList","")


    #任务优先级 可选
    taskLevel = request.GET.get("taskLevel", "")
    if taskLevel == "":
        taskLevel = "低"

    #是否发送邮件 可选
    isSendEmail = request.GET.get("isSendEmail",0)
    #是否保存到历史记录 可选
    isSaveHistory = request.GET.get("isSaveHistory",0)

    version = request.GET.get("version", "")
    dataList = TbTask.objects
    if version == "":
        try:
            version = TbWebPortalStandardEnv.objects.get(httpConfKey=httpConfKey).version
        except:
            return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="version参数没有查到相关数据").toJson())
    if version != "CurrentVersion":
        versionModule = TbVersion.objects.filter(versionName=version).last()
        if versionModule:
            if versionModule.type == 2:
                version = "CurrentVersion"
            else:
                version = versionModule.versionName
                dataList = TbVersionTask.objects.filter(versionName=version)
        else:
            return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="version参数没有查到相关数据").toJson())



    tbModule = TbBatchTask()
    tbModule.caseLevel = levelDict[caseLevel]
    tbModule.httpConfKey = httpConfKey
    tbModule.taskLevel = levelDict[taskLevel]
    tbModule.addBy = TbUser.objects.get(token=token).loginName
    tbModule.isSendEmail = isSendEmail
    tbModule.isSaveHistory = isSaveHistory
    tbModule.version = version

    #如果没有任务集合 就必须有tasklevel 业务线 和是是否加入持续集成的筛选
    if not taskList:
        if taskLevel not in levelDict.keys():
            return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="taskLevel只能为【高，中，低】").toJson())

        dataList = dataList.filter(state=1).filter(isCI=1,taskLevel__lte=levelDict[taskLevel])
        if businessLine:
            dataList = dataList.filter(businessLineGroup__in=[businessLine,"['"+businessLine+"']"])
        tbModule.businessLine = businessLine
        tbModule.taskLevel = levelDict[taskLevel]
        taskIdList = []
        for index in dbModelListToListDict(dataList):
            taskIdList.append(index["taskId"])

        tbModule.taskIdList = ",".join(taskIdList)

    else:
        for index in list(set(taskList.split(","))):
            if not TbTask.objects.filter(taskId=index,state=1).last():
                return HttpResponse("%s 未查到相关任务" % index)
        tbModule.taskIdList = ",".join(list(set(taskList.split(","))))
    tbModule.status = 1
    tbModule.save()

    batchTaskThread(tbModule=tbModule).start()
    url = "%s/batchTaskCallBack?batchId=%s" % (confDict['WEB']['uri'], tbModule.id)
    return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="请求发送中，请稍后回调 <a href='%s'>%s</a> " % (url, url)).toJson())


def batchTaskCallBack(request):
    batchId = request.GET.get("batchId","")
    if not batchId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR,message="batchId 参数不能为空").toJson())
    thisData = TbBatchTask.objects.filter(id=batchId).last()
    if not thisData:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR,message="batchId 结果查询失败，没有匹配的数据").toJson())
    url = "%s/batchTaskCallBack?batchId=%s" % (confDict['WEB']['uri'],batchId)
    if thisData.status == 1:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="请求未发送，请稍后回调 <a href='%s'>%s</a> " % (url,url)).toJson())
    elif thisData.status == 2:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="请求发送中，请稍后回调 <a href='%s'>%s</a> " % (url,url)).toJson())
    elif thisData.status == 3:
        return HttpResponse(ApiReturn(ApiReturn.CODE_OK,message="请求发送完成").toJson())
    else:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="请求发送异常，请联系管理员").toJson())