from django.shortcuts import render
from django.shortcuts import HttpResponse
from apps.common.helper.ApiReturn import ApiReturn
from all_models.models import *
from all_models_for_dubbo.models import *
from apps.common.func.CommonFunc import *
from apps.common.func.LanguageFunc import *
from django.forms.models import model_to_dict
from django.db.models import Q
import time,logging
from apps.common.func.WebFunc import *
from apps.common.model.RedisDBConfig import *

logger = logging.getLogger("invoke")

retMsg = ""
langDict = {}
addBy = ""
addByName = ""
addByObj = None
httpConfKey = ""
httpConfKeyAlias = ""
httpConfKeyObj = None
isSendEmail = 0
isSaveHistory = 0
execPlatform = 100
token = ""
timeout = 0
host = ""
version = "CurrentVersion"
token_for_trusted = "asdfasdkjbvljlkdafgjl1k23j4123lk4j1lkjlksdfgkljfklsajlkdfjalksjflkj134"
#invoke入口函数
def index(request):
    global retMsg,langDict,addBy,httpConfKey,isSendEmail,isSaveHistory,execPlatform,token,timeout,host,version,testLevel,addByName,addByObj,token_for_trusted
    logger.debug("TestLoggerINindex.")
    host = request.get_host()
    langDict = getLangTextDict(request)
    retMsg = eval(langDict['invoke']['retMsg'])
    paramDict = request.GET
    method = request.method
    opt = paramDict.get("opt","help")
    if opt == "help" or opt == "h":
        return HttpResponse(method+retMsg)

    #校验所包含参数合法性
    rightParamList = [KEY_LANGUAGE,"help","h","token","opt","httpConfKey","taskId","taskExecuteId","interfaceId","interfaceDebugId",
                      "caseId","testCaseDebugId","testCaseStepDebugId","isSendEmail","isSaveHistory","execPlatform","timeout",
                      "loginName","password","comments","emailList","version","packageId","testLevel",
                      "taskDetail","codeCoverage","startTime","taketime","type","testResult",
                      "taskSuiteExecuteId","taskSuiteId",
                      "retryCount","add_by"]

    for key in paramDict.keys():
        if key not in rightParamList:
            return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR,eval(langDict['invoke']['invalidRequestMethod']),body=retMsg).toJson())

    #校验参数opt中的值的合法性
    rightOptList  = ["runtask","runinterface","runtestcase","callbacktask","callbackinterface","callbacktestcase","canceltask","gettaskprogress","gettoken",
                     "runuitask","callbackuitask","canceluitask","rundubbotask","callbackdubbotask","canceldubbotask","getdubbotaskprogress",
                     "addStatis",
                     "runtasksuite","callbacktasksuite","canceltasksuite",
                     "rundubbotasksuite", "callbackdubbotasksuite", "canceldubbotasksuite"]
    if opt not in rightOptList:
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, """%s%s""" % (langDict['invoke']['paramNotValid'],rightOptList), body=retMsg).toJson())

    testLevelList = ["高","中","低"]
    #效验参数中testLevel的合法性
    testLevel = paramDict.get("testLevel",100)
    if testLevel not in testLevelList:
        testLevel = 100
    elif testLevel == "高":
        testLevel = 0
    elif testLevel == "中":
        testLevel = 5
    elif testLevel == "低":
        testLevel = 9


    # 校验isSendEmail合法性
    isSendEmail = paramDict.get("isSendEmail","0")
    if isInt(isSendEmail) and len(isSendEmail) <= 6:
        for iIsSendMailIndex in range(0,len(isSendEmail)):
            if isSendEmail[iIsSendMailIndex] != "0" and isSendEmail[iIsSendMailIndex] != "1":
                return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR,langDict['invoke']['isSendEmailInvalid'],body=retMsg).toJson())


    # 校验isSaveHistory合法性
    isSaveHistory = paramDict.get("isSaveHistory","0")
    if isSaveHistory != "0" and isSaveHistory != "1":
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR,langDict['invoke']['saveHistoryInvalid'],body=retMsg).toJson())


    #校验httpConfKey合法性
    if("run" in opt):
        #如果是runXXXXX则进行httpConfKey的校验，否则不校验
        httpConfKey = paramDict.get("httpConfKey","")
        if httpConfKey == "":
            return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['httpConfKeyCanNotNull'],body=retMsg).toJson())

        #DONE  必须验证是平台上有的httpConfKey
        httpConfList = httpConfKey.split(",")
        if len(httpConfList) > 1 and opt != "runtasksuite":
            return HttpResponse(
                ApiReturn(ApiReturn.CODE_PARAM_ERROR, "多环境只能执行任务集", body=retMsg).toJson())

        for httpConfIndex in httpConfList:
            httpConf = TbConfigHttp.objects.filter(httpConfKey=httpConfIndex)
            if httpConf:
                pass
            else:
                return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['httpConfKeyNotExist'], body=retMsg).toJson())


    # 校验version合法性
    version = paramDict.get("version", "")
    if version == "":
        version = "CurrentVersion"

    if version != "CurrentVersion":
        versionObjSets = TbVersion.objects.filter(type=1)
        findHistoryVersion = False  # 是否存在历史版本
        for tmpVersionObj in versionObjSets:
            if tmpVersionObj.versionName == version:
                findHistoryVersion = True
                break
        if not findHistoryVersion:
            currentVersionObj = TbVersion.objects.filter(type=2)
            if currentVersionObj and currentVersionObj[0].versionName == version:
                version = "CurrentVersion"
            else:
                return HttpResponse(
                    ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['notFoundHistoryVersion'],
                              body=retMsg).toJson())
    print("Version:%s" % version)

    # DONE 校验token合法性，并通过token获取user的loginname作为addBy
    if opt == "gettoken":
        # 处理gettoken opt
        loginName = paramDict.get("loginName")
        password = paramDict.get("password")
        if loginName == "":
            return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['loginnamecannotnull'] ,body=retMsg).toJson())
        if password == "":
            return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['passwordcannotnull'] ,body=retMsg).toJson())

        userData = TbUser.objects.filter(loginName=loginName,pwd=md5lower(password))
        if userData:
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK,langDict['invoke']['gettokensuccess'] , body={"token":userData[0].token}).toJson())
        else:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TOKEN_WRONG_PWD,langDict['invoke']['wrongloginnameandpwd'] , body={"loginName":loginName,"password":password}).toJson())
    else:
        #不是gottoken请求，那么必须有token
        token = paramDict.get("token","")
        if token == "":
            return HttpResponse(ApiReturn(ApiReturn.CODE_TOKEN_NULL, langDict['invoke']['tokencannotnull'],body=retMsg).toJson())

        if token == token_for_trusted:
            # 如果是信任token，则根据传入的add_by设置执行人。
            addBy = paramDict.get("add_by","")

            userbyaddby = TbUser.objects.filter(state=1, loginName=addBy).all()
            if userbyaddby:
                addByObj = userbyaddby[0]
                addBy = addByObj.loginName
                addByName = addByObj.userName
                if addBy == "" or addBy == None:
                    return HttpResponse(ApiReturn(ApiReturn.CODE_TOKEN_NULL, langDict['invoke']['tokencannotnull'],
                                                  body=retMsg).toJson())
            else:
                return HttpResponse(ApiReturn(ApiReturn.CODE_TOKEN_WRONG, langDict['invoke']['wrongtoken'], body=retMsg).toJson())

        else:
            # 如果是非信任token，走正常流程。
            userByToken = TbUser.objects.filter(state=1,token=token)
            if userByToken:
                addByObj = userByToken[0]
                addBy = addByObj.loginName
                addByName = addByObj.userName
                if addBy == "" or addBy == None:
                    return HttpResponse(ApiReturn(ApiReturn.CODE_TOKEN_NULL, langDict['invoke']['tokencannotnull'], body=retMsg).toJson())
            else:
                return HttpResponse(ApiReturn(ApiReturn.CODE_TOKEN_WRONG, langDict['invoke']['wrongtoken'], body=retMsg).toJson())

        #校验执行平台execPlatform合法性
        platformDict = {"1":"platform","2":"jenkins","100":"other"}
        execPlatform = paramDict.get("execPlatform","100")
        if execPlatform not in platformDict.keys() :
            return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, eval(langDict['invoke']['execplatformerror']), body=retMsg).toJson())

        #校验timeout合法性，必须是数字且大于等于0.
        timeout = paramDict.get("timeout",0)
        if isInt(timeout) == False or int(timeout) < 0 :
            return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['timeoutparamerror'] ,body=retMsg).toJson())
        else:
            timeout = int(timeout) > 10 and 10 or int(timeout)

        return eval("%s(request, paramDict)" % opt)

#任务执行
def runtask(request,paramDict):
    taskId = paramDict.get("taskId","")
    # 校验comments合法性
    comments = paramDict.get("comments","")
    emailList = paramDict.get("emailList","")
    retryCount = paramDict.get("retryCount",0)
    if taskId == "":
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR,langDict['invoke']['taskidcannotnull'],retMsg).toJson())

    if version == "CurrentVersion":
        taskData = TbTask.objects.filter(taskId=taskId,state=1)
    else:
        taskData = TbVersionTask.objects.filter(taskId=taskId,versionName_id=version)
    if taskData:
        taskData = taskData[0]
    else:
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['cannotfindtaskinvalidtaskid'], retMsg).toJson())

    if "1" in isSendEmail and emailList == "" and taskData.emailList == "":
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, "没有获取到邮件列表", retMsg).toJson())

    taskExecuteData = TbTaskExecute()

    taskExecuteData.taskId = taskData.taskId
    taskExecuteData.title = taskData.title
    taskExecuteData.taskdesc = taskData.taskdesc
    taskExecuteData.protocol = taskData.protocol
    taskExecuteData.businessLineGroup = taskData.businessLineGroup
    taskExecuteData.modulesGroup = taskData.modulesGroup
    taskExecuteData.taskLevel = taskData.taskLevel
    taskExecuteData.status = taskData.status
    taskExecuteData.interfaceCount = taskData.interfaceCount
    taskExecuteData.taskInterfaces = taskData.taskInterfaces
    taskExecuteData.caseCount = taskData.caseCount
    taskExecuteData.taskTestcases = taskData.taskTestcases
    taskExecuteData.interfaceNum = taskData.interfaceNum
    addByUser = addByObj
    taskExecuteData.addBy = addByUser
    taskExecuteData.addByName = addByUser.userName
    taskExecuteData.modBy = addBy
    taskExecuteData.modByName = addByUser.userName
    taskExecuteData.testLevel = testLevel
    httpConfKeyObj = TbConfigHttp.objects.get(httpConfKey=httpConfKey)
    taskExecuteData.httpConfKey = httpConfKeyObj
    taskExecuteData.httpConfKeyAlias = httpConfKeyObj.alias
    taskExecuteData.isCodeRate = 0
    taskExecuteData.isSendEmail = isSendEmail
    taskExecuteData.emailList = emailList == "" and taskData.emailList or emailList
    taskExecuteData.isSaveHistory = isSaveHistory
    taskExecuteData.execComments = comments
    taskExecuteData.retryCount = retryCount
    taskExecuteData.execType = 1
    taskExecuteData.execLevel = 5
    taskExecuteData.execTakeTime = 0
    taskExecuteData.execBy = addByUser
    taskExecuteData.execByName = addByUser.userName

    taskExecuteData.execStatus = 1
    taskExecuteData.execProgressData = "0:0:0:0:0"
    taskExecuteData.execPlatform = execPlatform
    taskExecuteData.testResult = "NOTRUN"
    taskExecuteData.testResultMsg = ""
    taskExecuteData.testReportUrl = ""
    taskExecuteData.state = 1
    taskExecuteData.execTime = datetime.datetime.utcnow()
    taskExecuteData.execFinishTime = "2000-01-01 00:00:01"
    taskExecuteData.version = version  #增加版本
    taskExecuteData.save(force_insert = True)


    taskExecuteId = taskExecuteData.id
    if taskExecuteId > 0:
        pass
    else:
        addUserLog(request, "invoke->runtask->任务执行添加失败！", "FAIL")
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['createtaskexecutefailure'], retMsg).toJson())
    RedisCache().set_data("%s_taskExecute_%s" % ("HTTP",taskExecuteId), "0:0:0:0:0")
    RedisCache().set_data("%s_taskExecuteStatus_%s" % ("HTTP",taskExecuteId), "1")
    tcpStr = '{"do":3,"TaskExecuteId":%s,"TaskExecuteEnv":"%s","TaskId":"%s","protocol":"%s"}' % (taskExecuteId,httpConfKey,taskData.taskId,taskData.protocol)

    retApiReturn = send_tcp_request(tcpStr)
    if retApiReturn.code != ApiReturn.CODE_OK :
        taskExecuteData.testResult = "EXCEPTION"
        taskExecuteData.execStatus = 4
        taskExecuteData.testResultMsg = retApiReturn.message
        taskExecuteData.save()
        addUserLog(request, "invoke->runtask->任务执行发送请求到tcpserver失败！", "FAIL")
        return HttpResponse(retApiReturn.toJson())
    else:
        addUserLog(request, "invoke->runtask->任务执行发送请求到tcpserver成功，开始执行！", "PASS")
        return getTaskResult(token,taskExecuteId,timeout)

def callbacktask(request, paramDict):
    taskExecuteId = paramDict.get("taskExecuteId")
    if isInt(taskExecuteId) == False or int(taskExecuteId) < 0 :
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['taskexecidmustbelagerthan0'], retMsg).toJson())
    else:
        taskExecuteId = int(taskExecuteId)

    return getTaskResult(token,taskExecuteId,timeout)

def canceltask(request, paramDict):
    taskExecuteId = paramDict.get("taskExecuteId")
    if isInt(taskExecuteId) == False or int(taskExecuteId) < 0 :
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['taskexecidmustbelagerthan0'], retMsg).toJson())
    else:
        taskExecuteId = int(taskExecuteId)

    runRes = TbTaskExecute.objects.filter(id=taskExecuteId)
    if runRes:
        runRes = runRes[0]
        if runRes.execBy_id != addBy :
            return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['cannotcancelotherusertask'],retMsg).toJson())
        if runRes.execStatus != 1 and runRes.execStatus != 2:
            return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['cannotcancelfinishedtask'], retMsg).toJson())

        try:
            runRes.execStatus = 10
            runRes.save(force_update=True)
            retApiResult = send_tcp_request('{"do":4,"TaskExecuteId":%s}' % taskExecuteId)
            if retApiResult.code != 10000:
                return HttpResponse(retApiResult.toJson())
            else:
                return HttpResponse(ApiReturn(ApiReturn.CODE_OK,langDict['invoke']['taskcancelsuccess']).toJson())
        except Exception as e:
            return HttpResponse( ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['taskcancelfailure'], retMsg).toJson())
    else:
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['tasktobecancelnotfound'], retMsg).toJson())

def gettaskprogress(request, paramDict):
    taskExecuteId = paramDict.get("taskExecuteId")
    if isInt(taskExecuteId) == False or int(taskExecuteId) < 0 :
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['taskexecidmustbelagerthan0'], retMsg).toJson())
    else:
        taskExecuteId = int(taskExecuteId)

    runRes = TbTaskExecute.objects.filter(id=taskExecuteId)
    if runRes:
        runRes = runRes[0]
        return HttpResponse(ApiReturn(ApiReturn.CODE_OK, langDict['invoke']['taskprogresspromptmsg']+runRes.execProgressData, retMsg).toJson())
    else :
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['executetasknotfound'], retMsg).toJson())

def getTaskResult(token,taskExecuteId,timeout):
    if isInt(taskExecuteId) == False or int(taskExecuteId) < 0 :
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['taskexecidmustbelagerthan0'], retMsg).toJson())

    startTimer = 0
    while True:
        runRes = TbTaskExecute.objects.filter(id=taskExecuteId)
        if runRes:
            runRes = runRes[0]
            if isJson(runRes.testResultMsg):
                runRes.testResultMsg = json.loads(runRes.testResultMsg)
            if not runRes.testReportUrl.startswith("http"):
                runRes.testReportUrl = "HTTP://%s%s" % (host,runRes.testReportUrl)
        else:
            return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['taskexecidmustbelagerthan0'], retMsg).toJson())

        resDict = dbModelToDict(runRes)
        if runRes.execStatus == 3:
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK, langDict['invoke']['taskexecutefinished'], resDict).toJson())
        elif runRes.execStatus == 4:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXECUTE_EXCEPTION, langDict['invoke']['taskexecuteexception'], resDict).toJson())
        elif runRes.execStatus == 10:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXECUTE_CANCELLING, langDict['invoke']['taskexecutecanceling'],resDict).toJson())
        elif runRes.execStatus == 11:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXECUTE_CANCELED, langDict['invoke']['taskexecutecanceled'],resDict).toJson())

        if startTimer > timeout :
            return_msg = {}
            return_msg['callbacktaskUrl'] = "HTTP://%s/invoke?opt=callbacktask&token=%s&taskExecuteId=%s&add_by=%s" % (host,token,taskExecuteId,addBy)
            return_msg['canceltaskUrl'] = "HTTP://%s/invoke?opt=canceltask&token=%s&taskExecuteId=%s&add_by=%s" % (host,token,taskExecuteId,addBy)
            return_msg['gettaskprogressUrl'] = "HTTP://%s/invoke?opt=gettaskprogress&token=%s&taskExecuteId=%s&add_by=%s" % (host,token,taskExecuteId,addBy)
            return HttpResponse(ApiReturn(ApiReturn.CODE_TIMEOUT, langDict['invoke']['taskexecutetimeout'],return_msg).toJson())

        time.sleep(1)
        startTimer += 1

def runinterface(request,paramDict):
    testDebugId = "interfaceDebug_%s_%s" % (request.session.get("loginName"),int(time.time() * 1000))
    interfaceId = paramDict.get("interfaceId","")
    if interfaceId == "":
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['interfaceIdcannotnull'], retMsg).toJson())

    # DONE   必须验证$interfaceId合法且存在
    if version == "CurrentVersion":
        interfaceData = TbHttpInterface.objects.filter(interfaceId=interfaceId)
    else:
        interfaceData = TbVersionHttpInterface.objects.filter(interfaceId=interfaceId,versionName_id=version)

    if interfaceData:
        interfaceData = dbModelToDict(interfaceData[0])
    else:
        return HttpResponse(
            ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['interfacenotfound'], retMsg).toJson())
    interfaceData['actualResult'] = ''
    interfaceData['assertResult'] = ''
    interfaceData['testResult'] = "NOTRUN"
    interfaceData['execStatus'] = 1
    interfaceData['beforeExecuteTakeTime'] = 0
    interfaceData['executeTakeTime'] = 0
    interfaceData['afterExecuteTakeTime'] = 0
    interfaceData['totalTakeTime'] = 0
    interfaceData['businessLineId'] = interfaceData["businessLineId_id"]
    interfaceData['moduleId'] = interfaceData["moduleId_id"]
    interfaceData['httpConfKey'] = httpConfKey
    interfaceData['version'] = version

    try:
        RedisCache().set_data(testDebugId,json.dumps(interfaceData))
        #初始设置接口debug的时间是1小时
        RedisCache().expire_data(testDebugId,60*60)
        tcpStr = '{"do":1,"InterfaceDebugId":"%s","protocol":"HTTP"}' % testDebugId
        retApiReturn = send_tcp_request(tcpStr)
        if retApiReturn.code != ApiReturn.CODE_OK:
            return HttpResponse(retApiReturn.toJson())
        else:
            return getInterfaceResult(token, testDebugId, timeout)
        # else:
        #     return HttpResponse( ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['interfacedebugidinvalid'], retMsg).toJson())
    except Exception as e:
        logging.error(traceback.format_exc())
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['exceptionoccurredwhendebuginterface'], retMsg).toJson())

def callbackinterface(request, paramDict):
    interfaceDebugId = paramDict.get("interfaceDebugId","")
    if interfaceDebugId == False and interfaceDebugId == None:
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['interfacedebugidnotexist'],retMsg).toJson())
    return getInterfaceResult(token,interfaceDebugId,timeout)

def getInterfaceResult(token,interfaceDebugId,execTimeout):
    if isInt(execTimeout) == False or execTimeout < 0 :
        return HttpResponse(
            ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['timeoutparamerror'], retMsg).toJson())
    if interfaceDebugId == False or interfaceDebugId == None:
        return HttpResponse(
            ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['interfacedebugidinvalid'], retMsg).toJson())
    startTimer = 0
    while True:
        # runRes = json.loads(RedisCache().get_data(interfaceDebugId))
        try:
            runRes = json.loads(RedisCache().get_data(interfaceDebugId))
        except Exception as e:
            print(traceback.format_exc())
            return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['nointerfacedebugfound']).toJson())
        # if runRes:
        #     runRes = runRes[0]
        # else:
        #     return HttpResponse(
        #         ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['nointerfacedebugfound'], retMsg).toJson())
        # resDict = dbModelToDict(runRes)
        if runRes["execStatus"] == 3:
            print(3)
            return HttpResponse(
                ApiReturn(ApiReturn.CODE_OK, langDict['invoke']['interfacedebugfinished'], runRes).toJson())
        if runRes["execStatus"] == 4:
            print(4)
            return HttpResponse(
                ApiReturn(ApiReturn.CODE_OK, langDict['invoke']['interfacedebugexception'], runRes).toJson())
        if startTimer > execTimeout :
            return_msg = {}
            return_msg['callbackinterfaceUrl'] = "HTTP://%s/invoke?opt=callbackinterface&token=%s&interfaceDebugId=%s&add_by=%s" % (host,token,interfaceDebugId,addBy)
            return HttpResponse(ApiReturn(ApiReturn.CODE_TIMEOUT, langDict['invoke']['interfacedebugtimeout'], return_msg).toJson())

        time.sleep(1)
        startTimer+=1

def runtestcase(request,paramDict):
    testCaseDebugId = "testCaseDebug_%s_%s" % (request.session.get("loginName"), int(time.time() * 1000))
    testCaseStepDebugId = "testCaseStepDebug_%s_%s" % (request.session.get("loginName"), int(time.time() * 1000))
    caseId = paramDict.get("caseId","")
    if caseId == "":
        #没有发现caseId，参数错误
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['paramerrornocaseId']).toJson())

    if version == "CurrentVersion":
        caseData = TbHttpTestcase.objects.filter(caseId=caseId, state=1)
        if caseData:
            caseData = caseData[0]
        else:
            # 未找到对应的testcase
            return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['nocasefoundindb']).toJson())

        caseStepData = TbHttpTestcaseStep.objects.filter(caseId=caseId, state=1).order_by("stepNum")
        if caseStepData:
            caseStepData = dbModelListToListDict(caseStepData)
        else:
            # 没有步骤数据
            return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['nocasestepfoundindb']).toJson())

    else:
        caseData = TbVersionHttpTestcase.objects.filter(caseId=caseId, state=1,versionName_id=version)
        if caseData:
            caseData = caseData[0]
        else:
            # 未找到对应的testcase
            return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['nocasefoundindb']).toJson())

        caseStepData = TbVersionHttpTestcaseStep.objects.filter(caseId=caseId, state=1,versionName_id=version).order_by("stepNum")
        if caseStepData:
            caseStepData = dbModelListToListDict(caseStepData)
        else:
            # 没有步骤数据
            return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['nocasestepfoundindb']).toJson())

    caseDebugData = dbModelToDict(caseData)
    caseDebugData["httpConfKey"] = httpConfKey
    caseDebugData['execStatus'] = 1
    caseDebugData['version'] = version
    testCaseStepList = []

    for stepIndex in caseStepData:
        print(stepIndex)
        stepIndex["httpConfKey"] = httpConfKey
        stepIndex["execStatus"] = 1
        stepIndex["businessLineId"] = stepIndex["businessLineId_id"]
        stepIndex["moduleId"] = stepIndex["moduleId_id"]
        stepIndex["sourceId"] = stepIndex["sourceId_id"]
        stepIndex['version'] = version
        testCaseStepList.append(stepIndex)
    RedisCache().set_data(testCaseDebugId, json.dumps(caseDebugData))
    RedisCache().set_data(testCaseStepDebugId, json.dumps(testCaseStepList))
    RedisCache().expire_data(testCaseDebugId, 60 * 60)
    RedisCache().expire_data(testCaseStepDebugId, 60 * 60)
    tcpStr = '{"do":2,"CaseDebugId":"%s","CaseStepDebugIdList":"%s","protocol":"HTTP"}' % (testCaseDebugId,testCaseStepDebugId)
    retApiReturn = send_tcp_request(tcpStr)
    if retApiReturn.code != ApiReturn.CODE_OK:
        return HttpResponse(retApiReturn.toJson())
    else:
        #执行成功，获取结果
        return getCaseResult(token, testCaseDebugId,testCaseStepDebugId, timeout)

def callbacktestcase(request, paramDict):
    caseDebugId = paramDict.get("testCaseDebugId")
    testCaseStepDebugId = paramDict.get("testCaseStepDebugId")
    if caseDebugId == None:
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['casedebugidmustlargerthan0']).toJson())
    return getCaseResult(token, caseDebugId,testCaseStepDebugId, timeout)

def getCaseResult(token,testCaseDebugId,testCaseStepDebugId,execTimeout):
    if isInt(execTimeout) == False or int(execTimeout) < 0 :
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['timeoutparamerror']).toJson())


    startTimer = 0
    while True:
        # caseDebugData = TbHttpTestcaseDebug.objects.filter(id=caseDebugId)
        resDict = json.loads(RedisCache().get_data(testCaseDebugId))
        if resDict == None:
            return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['nocasedebuginfofound']).toJson())
        if resDict["execStatus"] == 3:
            # caseStepDebugData = TbHttpTestcaseStepDebug.objects.filter(caseId=caseDebugData.caseId,state=1,addBy=addBy).order_by("stepNum")
            # stepList = []
            # for i in range(0,len(caseStepDebugData)):
            #     tmpStepDebugDict = dbModelToDict(caseStepDebugData[i])
            #     stepList.append(tmpStepDebugDict)
            resDict['stepList'] = json.loads(RedisCache().get_data(testCaseStepDebugId))
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK, langDict['invoke']['interfacedebugfinished'], resDict).toJson())
        if resDict["execStatus"] == 4:
            # caseStepDebugData = TbHttpTestcaseStepDebug.objects.filter(caseId=caseDebugData.caseId,state=1,addBy=addBy).order_by("stepNum")
            # stepList = []
            # for i in range(0,len(caseStepDebugData)):
            #     tmpStepDebugDict = dbModelToDict(caseStepDebugData[i])
            #     stepList.append(tmpStepDebugDict)
            resDict['stepList'] = json.loads(RedisCache().get_data(testCaseStepDebugId))
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK, langDict['invoke']['interfacedebugexception'], resDict).toJson())
        if startTimer > execTimeout:
            return_msg = {}
            return_msg['callbackTestcaseUrl'] = "HTTP://%s/invoke?opt=callbacktestcase&token=%s&testCaseDebugId=%s&testCaseStepDebugId=%s&add_by=%s" % (host, token, testCaseDebugId,testCaseStepDebugId,addBy)
            return HttpResponse(ApiReturn(ApiReturn.CODE_TIMEOUT, langDict['invoke']['casedebugtimeout'], return_msg).toJson())

        time.sleep(1)
        startTimer += 1

###########UI相关的###########################
def runuitask(request, paramDict):
    taskId = paramDict.get("taskId", "")
    # 校验comments合法性
    comments = paramDict.get("comments", "")
    emailList = paramDict.get("emailList", "")
    packageId = paramDict.get("packageId", "")
    if packageId != "":
        pacInDb = TbUiPackage.objects.filter(packageId=packageId).all()
        if pacInDb:
            pass
        else:
            return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['packageNotExist'], retMsg).toJson())

    if taskId == "":
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['taskidcannotnull'], retMsg).toJson())

    if version == "CurrentVersion":
        taskData = TbUiTaskSimple.objects.filter(taskId=taskId, state=1)
    else:
        #历史版本的UI任务还未实现，暂时仅支持当前版本的。
        taskData = TbUiTaskSimple.objects.filter(taskId=taskId, state=1)
        # taskData = TbVersionTask.objects.filter(taskId=taskId, versionName_id=version)
    print(taskData)
    if taskData:
        taskData = taskData[0]
    else:
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['cannotfindtaskinvalidtaskid'], retMsg).toJson())

    taskExecuteData = TbUITestExecute()

    taskExecuteData.taskId = taskData.taskId
    taskExecuteData.title = taskData.title
    taskExecuteData.taskdesc = taskData.taskdesc
    taskExecuteData.businessLineId = taskData.businessLineId
    taskExecuteData.moduleId = taskData.moduleId
    taskExecuteData.sourceGroup = taskData.sourceGroup
    taskExecuteData.tasklevel = taskData.tasklevel

    taskExecuteData.fileAddBy = taskData.fileAddBy
    taskExecuteData.fileName = taskData.fileName
    taskExecuteData.sheetName = taskData.sheetName
    taskExecuteData.httpConfKey = httpConfKey
    taskExecuteData.reportDir = ""
    taskExecuteData.packageId = packageId


    taskExecuteData.addBy = addBy
    taskExecuteData.modBy = addBy
    taskExecuteData.isSendEmail = isSendEmail
    taskExecuteData.emailList = (emailList == "" and taskData.emailList or emailList)
    taskExecuteData.execComments = comments

    taskExecuteData.execStatus = 1
    taskExecuteData.execProgressString = ""
    taskExecuteData.execPlatform = execPlatform
    taskExecuteData.testResult = "NOTRUN"
    taskExecuteData.testResultMessage = ""
    taskExecuteData.state = 1
    taskExecuteData.save(force_insert=True)

    taskExecuteId = taskExecuteData.id
    if taskExecuteId > 0:
        pass
    else:
        addUserLog(request, "invoke->runuitask->UI任务执行添加失败！", "FAIL")
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['createtaskexecutefailure'], retMsg).toJson())

    tcpStr = '{"do":31,"UITaskExecuteId":%s}' % taskExecuteId

    retApiReturn = send_tcp_request_to_uiport(tcpStr);
    if retApiReturn.code != ApiReturn.CODE_OK:
        taskExecuteData.testResult = "EXCEPTION"
        taskExecuteData.execStatus = 4
        taskExecuteData.testResultMessage = retApiReturn.message
        taskExecuteData.save()
        addUserLog(request, "invoke->runuitask->UI任务执行[%s]发送请求到tcpserver失败！" % taskExecuteId, "FAIL")
        return HttpResponse(retApiReturn.toJson())
    else:
        addUserLog(request, "invoke->runuitask->UI任务执行[%s]发送请求到tcpserver成功，开始执行！" % taskExecuteId, "PASS")
        return getuiTaskResult(token, taskExecuteId, timeout)

def callbackuitask(request, paramDict):
    taskExecuteId = paramDict.get("taskExecuteId")
    if isInt(taskExecuteId) == False or int(taskExecuteId) < 0:
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['taskexecidmustbelagerthan0'], retMsg).toJson())
    else:
        taskExecuteId = int(taskExecuteId)

    return getuiTaskResult(token, taskExecuteId, timeout)

def canceluitask(request, paramDict):
    taskExecuteId = paramDict.get("taskExecuteId")
    if isInt(taskExecuteId) == False or int(taskExecuteId) < 0:
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['taskexecidmustbelagerthan0'], retMsg).toJson())
    else:
        taskExecuteId = int(taskExecuteId)

    runRes = TbUITestExecute.objects.filter(id=taskExecuteId)
    if runRes:
        runRes = runRes[0]
        if runRes.addBy != addBy:
            return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['cannotcancelotherusertask'], retMsg).toJson())
        if runRes.execStatus != 1 and runRes.execStatus != 2:
            return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['cannotcancelfinishedtask'], retMsg).toJson())

        try:
            if isJson(runRes.execProgressString):
                tmpDict = json.loads(runRes.execProgressString)
                if tmpDict['whetherCanCancelTask'] == "0":
                    return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['cannotCancelTaskWhenDriverInitialing'], retMsg).toJson())

            runRes.execStatus = 10
            runRes.save(force_update=True)
            retApiResult = send_tcp_request_to_uiport('{"do":6,"UITaskExecuteId":%s}' % taskExecuteId)
            if retApiResult.code != 10000:
                return HttpResponse(retApiResult.toJson())
            else:
                return HttpResponse(ApiReturn(ApiReturn.CODE_OK, langDict['invoke']['taskcancelsuccess']).toJson())
        except Exception as e:
            return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['taskcancelfailure'], retMsg).toJson())
    else:
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['tasktobecancelnotfound'], retMsg).toJson())

def getuiTaskResult(token,taskExecuteId,timeout):
    if isInt(taskExecuteId) == False or int(taskExecuteId) < 0 :
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['taskexecidmustbelagerthan0'], retMsg).toJson())

    startTimer = 0
    while True:
        runRes = TbUITestExecute.objects.filter(id=taskExecuteId)
        if runRes:
            runRes = runRes[0]
            if isJson(runRes.testResultMessage):
                runRes.testResultMessage = json.loads(runRes.testResultMessage)
            runRes.testReportUrl = "HTTP://%s/static/ui_test_reports/%s/report.html" % (host,runRes.reportDir)
        else:
            return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['taskexecidmustbelagerthan0'], retMsg).toJson())

        resDict = dbModelToDict(runRes)
        if runRes.execStatus == 3:
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK, langDict['invoke']['taskexecutefinished'], resDict).toJson())
        elif runRes.execStatus == 4:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXECUTE_EXCEPTION, langDict['invoke']['taskexecuteexception'], resDict).toJson())
        elif runRes.execStatus == 10:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXECUTE_CANCELLING, langDict['invoke']['taskexecutecanceling'],resDict).toJson())
        elif runRes.execStatus == 11:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXECUTE_CANCELED, langDict['invoke']['taskexecutecanceled'],resDict).toJson())

        if startTimer > timeout :
            return_msg = {}
            return_msg['callbacktaskUrl'] = "HTTP://%s/invoke?opt=callbackuitask&token=%s&taskExecuteId=%s&add_by=%s" % (host,token,taskExecuteId,addBy)
            return_msg['canceltaskUrl'] = "HTTP://%s/invoke?opt=canceluitask&token=%s&taskExecuteId=%s&add_by=%s" % (host,token,taskExecuteId,addBy)
            return HttpResponse(ApiReturn(ApiReturn.CODE_TIMEOUT, langDict['invoke']['taskexecutetimeout'],return_msg).toJson())

        time.sleep(1)
        startTimer += 1

#############dubbo相关的#########################
def rundubbotask(request,paramDict):
    taskId = paramDict.get("taskId","")
    # 校验comments合法性
    comments = paramDict.get("comments","")
    emailList = paramDict.get("emailList","")
    retryCount = paramDict.get("retryCount",0)
    if taskId == "":
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR,langDict['invoke']['taskidcannotnull'],retMsg).toJson())

    if version == "CurrentVersion":
        taskData = Tb2DubboTask.objects.filter(taskId=taskId,state=1)
    else:
        taskData = TbVersionTask.objects.filter(taskId=taskId,versionName_id=version)

    if taskData:
        taskData = taskData[0]
    else:
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['cannotfindtaskinvalidtaskid'], retMsg).toJson())

    taskExecuteData = Tb2DubboTaskExecute()

    taskExecuteData.taskId = taskData.taskId
    taskExecuteData.title = taskData.title
    taskExecuteData.taskdesc = taskData.taskdesc
    taskExecuteData.protocol = taskData.protocol
    taskExecuteData.businessLineGroup = taskData.businessLineGroup
    taskExecuteData.modulesGroup = taskData.modulesGroup
    taskExecuteData.taskLevel = taskData.taskLevel
    taskExecuteData.status = taskData.status
    taskExecuteData.interfaceCount = taskData.interfaceCount
    taskExecuteData.taskInterfaces = taskData.taskInterfaces
    taskExecuteData.caseCount = taskData.caseCount
    taskExecuteData.taskTestcases = taskData.taskTestcases
    taskExecuteData.interfaceNum = taskData.interfaceNum
    taskExecuteData.addBy = TbUser.objects.get(loginName=addBy)
    taskExecuteData.modBy = addBy
    taskExecuteData.testLevel = testLevel
    taskExecuteData.httpConfKey = TbConfigHttp.objects.get(httpConfKey=httpConfKey)
    taskExecuteData.isCodeRate = 0
    taskExecuteData.isSendEmail = isSendEmail
    taskExecuteData.emailList = emailList == "" and taskData.emailList or emailList
    taskExecuteData.isSaveHistory = isSaveHistory
    taskExecuteData.execComments = comments
    taskExecuteData.retryCount = retryCount
    taskExecuteData.execType = 1
    taskExecuteData.execLevel = 5
    taskExecuteData.execTakeTime = 0
    taskExecuteData.execBy = TbUser.objects.get(loginName=addBy)
    taskExecuteData.execStatus = 1
    taskExecuteData.execProgressData = "0:0:0:0:0"
    taskExecuteData.execPlatform = execPlatform
    taskExecuteData.testResult = "NOTRUN"
    taskExecuteData.testResultMsg = ""
    taskExecuteData.testReportUrl = ""
    taskExecuteData.state = 1
    taskExecuteData.execTime = datetime.datetime.utcnow()
    taskExecuteData.execFinishTime = "2000-01-01 00:00:01"
    taskExecuteData.version = version  #增加版本
    taskExecuteData.save(force_insert = True)

    taskExecuteId = taskExecuteData.id
    if taskExecuteId > 0:
        pass
    else:
        addUserLog(request, "invoke->rundubbotask->任务执行添加失败！", "FAIL")
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['createtaskexecutefailure'], retMsg).toJson())

    tcpStr = '{"do":3,"TaskExecuteId":%s,"TaskExecuteEnv":"%s","TaskId":"%s","protocol":"%s"}' % (taskExecuteId,httpConfKey,taskData.taskId,taskData.protocol)

    retApiReturn = send_tcp_request(tcpStr)
    if retApiReturn.code != ApiReturn.CODE_OK :
        taskExecuteData.testResult = "EXCEPTION"
        taskExecuteData.execStatus = 4
        taskExecuteData.testResultMsg = retApiReturn.message
        taskExecuteData.save()
        addUserLog(request, "invoke->rundubbotask->任务执行发送请求到tcpserver失败！", "FAIL")
        return HttpResponse(retApiReturn.toJson())
    else:
        addUserLog(request, "invoke->rundubbotask->任务执行发送请求到tcpserver成功，开始执行！", "PASS")
        return getdubboTaskResult(token,taskExecuteId,timeout)

def callbackdubbotask(request, paramDict):
    taskExecuteId = paramDict.get("taskExecuteId")
    if isInt(taskExecuteId) == False or int(taskExecuteId) < 0 :
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['taskexecidmustbelagerthan0'], retMsg).toJson())
    else:
        taskExecuteId = int(taskExecuteId)

    return getdubboTaskResult(token,taskExecuteId,timeout)

def canceldubbotask(request, paramDict):
    taskExecuteId = paramDict.get("taskExecuteId")
    if isInt(taskExecuteId) == False or int(taskExecuteId) < 0 :
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['taskexecidmustbelagerthan0'], retMsg).toJson())
    else:
        taskExecuteId = int(taskExecuteId)

    runRes = Tb2DubboTaskExecute.objects.filter(id=taskExecuteId)
    if runRes:
        runRes = runRes[0]
        if runRes.execBy_id != addBy :
            return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['cannotcancelotherusertask'],retMsg).toJson())
        if runRes.execStatus != 1 and runRes.execStatus != 2:
            return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['cannotcancelfinishedtask'], retMsg).toJson())

        try:
            runRes.execStatus = 10
            runRes.save(force_update=True)
            retApiResult = send_tcp_request('{"do":4,"TaskExecuteId":%s,"protocol":"DUBBO"}' % taskExecuteId)
            if retApiResult.code != 10000:
                return HttpResponse(retApiResult.toJson())
            else:
                return HttpResponse(ApiReturn(ApiReturn.CODE_OK,langDict['invoke']['taskcancelsuccess']).toJson())
        except Exception as e:
            return HttpResponse( ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['taskcancelfailure'], retMsg).toJson())
    else:
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['tasktobecancelnotfound'], retMsg).toJson())

def getdubbotaskprogress(request, paramDict):
    taskExecuteId = paramDict.get("taskExecuteId")
    if isInt(taskExecuteId) == False or int(taskExecuteId) < 0 :
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['taskexecidmustbelagerthan0'], retMsg).toJson())
    else:
        taskExecuteId = int(taskExecuteId)

    runRes = Tb2DubboTaskExecute.objects.filter(id=taskExecuteId)
    if runRes:
        runRes = runRes[0]
        return HttpResponse(ApiReturn(ApiReturn.CODE_OK, langDict['invoke']['taskprogresspromptmsg']+runRes.execProgressData, retMsg).toJson())
    else :
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['executetasknotfound'], retMsg).toJson())

def getdubboTaskResult(token,taskExecuteId,timeout):
    if isInt(taskExecuteId) == False or int(taskExecuteId) < 0 :
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['taskexecidmustbelagerthan0'], retMsg).toJson())

    startTimer = 0
    while True:
        runRes = Tb2DubboTaskExecute.objects.filter(id=taskExecuteId)
        if runRes:
            runRes = runRes[0]
            if isJson(runRes.testResultMsg):
                runRes.testResultMsg = json.loads(runRes.testResultMsg)
            # runRes.testReportUrl = "HTTP://%s%s" % (host,runRes.testReportUrl)
            try:
                if http_report_to_AWS != "1":
                    runRes.testReportUrl = "HTTP://%s%s" % (host,runRes.testReportUrl)
            except:
                runRes.testReportUrl = "HTTP://%s%s" % (host, runRes.testReportUrl)
        else:
            return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['taskexecidmustbelagerthan0'], retMsg).toJson())

        resDict = dbModelToDict(runRes)
        if runRes.execStatus == 3:
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK, langDict['invoke']['taskexecutefinished'], resDict).toJson())
        elif runRes.execStatus == 4:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXECUTE_EXCEPTION, langDict['invoke']['taskexecuteexception'], resDict).toJson())
        elif runRes.execStatus == 10:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXECUTE_CANCELLING, langDict['invoke']['taskexecutecanceling'],resDict).toJson())
        elif runRes.execStatus == 11:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXECUTE_CANCELED, langDict['invoke']['taskexecutecanceled'],resDict).toJson())

        if startTimer > timeout :
            return_msg = {}
            return_msg['callbacktaskUrl'] = "HTTP://%s/invoke?opt=callbackdubbotask&token=%s&taskExecuteId=%s&add_by=%s" % (host,token,taskExecuteId,addBy)
            return_msg['canceltaskUrl'] = "HTTP://%s/invoke?opt=canceldubbotask&token=%s&taskExecuteId=%s&add_by=%s" % (host,token,taskExecuteId,addBy)
            return_msg['gettaskprogressUrl'] = "HTTP://%s/invoke?opt=getdubbotaskprogress&token=%s&taskExecuteId=%s&add_by=%s" % (host,token,taskExecuteId,addBy)
            return HttpResponse(ApiReturn(ApiReturn.CODE_TIMEOUT, langDict['invoke']['taskexecutetimeout'],return_msg).toJson())

        time.sleep(1)
        startTimer += 1



from all_models_for_mock.models import Tb4StatisticTaskExecuteInfo,Tb4StatisticTask
def addStatis(request, paramDict):
    # invoke?opt=addStatis&taskId=1&taskDetail={"total":100,"pass":10,"fail":100,"error":1}&testResult=PASS&codeCoverage=56.8&startTime=2018-01-02 11:11:11&taketime=230&httpConfKey=test1&type=pipeline&comments=哈哈哈
    statisticTaskId = paramDict.get("taskId","")
    if "StatisticTask" not in showMenuConfig.keys() or showMenuConfig["StatisticTask"] != 1:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, "未打开统计任务功能！").toJson())

    if statisticTaskId:
        taskInfo = Tb4StatisticTask.objects.filter(id=statisticTaskId)
        if taskInfo:
            taskInfo = taskInfo[0]
        else:
            return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, "没有发现这个统计任务[%s]" % statisticTaskId).toJson())
        try:
            newStatisTaskExecInfo = Tb4StatisticTaskExecuteInfo()
            newStatisTaskExecInfo.statisticTaskId = statisticTaskId
            newStatisTaskExecInfo.businessLineId = taskInfo.businessLineId
            newStatisTaskExecInfo.moduleId = taskInfo.moduleId
            newStatisTaskExecInfo.title = taskInfo.title
            newStatisTaskExecInfo.descText = taskInfo.descText
            taskDetail = paramDict.get("taskDetail","")
            if taskDetail=="" or isJson(taskDetail) == False:
                return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, "参数taskDetail不合法必须是合法的json!").toJson())
            else:
                taskDetailDict = json.loads(taskDetail)
                if "total" not in taskDetailDict.keys():
                    return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, "参数taskDetail不合法必须有total!").toJson())
                if "pass" not in taskDetailDict.keys():
                    return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, "参数taskDetail不合法必须有pass!").toJson())
                if "fail" not in taskDetailDict.keys():
                    return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, "参数taskDetail不合法必须有fail!").toJson())
                if "error" not in taskDetailDict.keys():
                    return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, "参数taskDetail不合法必须有error!").toJson())
            newStatisTaskExecInfo.executeDetailText = paramDict.get("taskDetail","")
            newStatisTaskExecInfo.codeCoverage = paramDict.get("codeCoverage","0.0")

            newStatisTaskExecInfo.testResult = paramDict.get("testResult","")
            if newStatisTaskExecInfo.testResult not in ["PASS","FAIL","ERROR"]:
                return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, "参数testResult不合法必须PASS/FAIL/ERROR").toJson())


            newStatisTaskExecInfo.executeStartTime = paramDict.get("startTime","")
            if newStatisTaskExecInfo.executeStartTime == "":
                return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, "参数startTime必传，必须为合法的日期时间格式，请使用 YYYY-MM-DD HH:MM:SS").toJson())

            newStatisTaskExecInfo.executeTaketime = paramDict.get("taketime","")
            if newStatisTaskExecInfo.executeTaketime == "":
                return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, "参数taketime必传，必须是数字！").toJson())

            newStatisTaskExecInfo.httpConfKey = paramDict.get("httpConfKey","")
            newStatisTaskExecInfo.executeType = paramDict.get("type","")
            newStatisTaskExecInfo.executeBy = addBy
            newStatisTaskExecInfo.addBy = addBy
            newStatisTaskExecInfo.modBy = addBy
            newStatisTaskExecInfo.comments = paramDict.get("comments","")
            newStatisTaskExecInfo.save(force_insert=True)

            return HttpResponse(ApiReturn(ApiReturn.CODE_OK, "上报统计任务执行信息成功！",{"id":newStatisTaskExecInfo.id}).toJson())
        except:
            print(traceback.format_exc())
            return HttpResponse(ApiReturn(ApiReturn.CODE_EXCEPTION, "上报统计任务执行信息异常！<br>%s" % traceback.format_exc()).toJson())

    else:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, "上报统计任务taskId是必传参数！").toJson())



def runtasksuite(request,paramDict):
    taskSuiteId = paramDict.get("taskSuiteId", "")
    # 校验comments合法性
    comments = paramDict.get("comments", "")
    emailList = paramDict.get("emailList", "")
    retryCount = paramDict.get("retryCount", 0)
    if taskSuiteId == "":
        return HttpResponse(
            ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['tasksuiteidcannotnull'], retMsg).toJson())

    if version == "CurrentVersion":
        taskSuiteData = TbTaskSuite.objects.filter(taskSuiteId=taskSuiteId)
    else:
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, "任务集暂不支持历史版本", retMsg).toJson())

    if taskSuiteData:
        taskSuiteData = taskSuiteData[0]
    else:
        return HttpResponse(
            ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['cannotfindtaskinvalidtaskid'], retMsg).toJson())
        # 先写taskSuite
    taskSuiteExecuteModel = TbTaskSuiteExecute()
    taskSuiteExecuteModel.taskSuiteId = taskSuiteData.taskSuiteId
    taskSuiteExecuteModel.title = taskSuiteData.title
    taskSuiteExecuteModel.taskSuiteDesc = taskSuiteData.taskSuiteDesc
    taskSuiteExecuteModel.protocol = taskSuiteData.protocol
    taskSuiteExecuteModel.status = taskSuiteData.status
    taskSuiteExecuteModel.taskCount = taskSuiteData.taskCount
    taskSuiteExecuteModel.taskList = taskSuiteData.taskList
    taskSuiteExecuteModel.isSendEmail = isSendEmail
    taskSuiteExecuteModel.emailList = emailList == "" and taskSuiteData.emailList or emailList
    taskSuiteExecuteModel.isSaveHistory = isSaveHistory
    taskSuiteExecuteModel.execComments = comments
    taskSuiteExecuteModel.retryCount = retryCount
    taskSuiteExecuteModel.execBy = addBy
    taskSuiteExecuteModel.execTime = datetime.datetime.now()
    taskSuiteExecuteModel.httpConfKeyList = httpConfKey
    taskSuiteExecuteModel.execStatus = 2
    httpConfList = httpConfKey.split(",")
    httpConfKeyAliasList = ""
    for httpConfIndex in httpConfList:
        if httpConfKeyAliasList == "":
            httpConfKeyAliasList = TbConfigHttp.objects.get(httpConfKey=httpConfIndex).alias
        else:
            httpConfKeyAliasList = "%s,%s" % (
            httpConfKeyAliasList, TbConfigHttp.objects.get(httpConfKey=httpConfIndex).alias)
    taskSuiteExecuteModel.httpConfKeyAliasList = httpConfKeyAliasList

    taskSuiteExecuteModel.addBy = addBy
    taskSuiteExecuteModel.save()

    taskList = taskSuiteData.taskList.split(",")

    # 获取taskExecuteId list
    taskExecuteIdList = []
    taskExecuteTcpList = []
    for taskIndex in taskList:
        taskData = TbTask.objects.get(taskId=taskIndex)
        for httpConfIndex in range(0, len(httpConfList)):
            taskExecuteData = TbTaskExecute()
            taskExecuteData.taskId = taskData.taskId
            if taskSuiteData.emailList != "":
                taskExecuteData.emailList = taskSuiteData.emailList
            else:
                taskExecuteData.emailList = taskData.emailList
            taskExecuteData.title = taskData.title
            taskExecuteData.taskdesc = taskData.taskdesc
            taskExecuteData.protocol = taskData.protocol
            taskExecuteData.businessLineGroup = taskData.businessLineGroup
            taskExecuteData.modulesGroup = taskData.modulesGroup
            taskExecuteData.interfaceCount = taskData.interfaceCount
            taskExecuteData.taskInterfaces = taskData.taskInterfaces
            taskExecuteData.caseCount = taskData.caseCount
            taskExecuteData.taskTestcases = taskData.taskTestcases
            taskExecuteData.interfaceNum = taskData.interfaceNum
            taskExecuteData.emailList = emailList == "" and taskSuiteData.emailList or emailList
            taskExecuteData.addBy_id = addBy
            taskExecuteData.addByName = addByName
            taskExecuteData.modBy = addBy
            taskExecuteData.modByName = addByName

            taskExecuteData.isSaveHistory = isSaveHistory
            # taskExecuteData.isSendEmail = 0

            taskExecuteData.isSendEmail = 0
            taskExecuteData.execBy_id = addBy
            taskExecuteData.execByName = addByName
            taskExecuteData.version = version
            taskExecuteData.execComments = comments
            taskExecuteData.retryCount = retryCount

            httpConfKeyObj = TbConfigHttp.objects.get(httpConfKey=httpConfList[httpConfIndex])
            taskExecuteData.httpConfKey_id = httpConfList[httpConfIndex]
            taskExecuteData.httpConfKeyAlias = httpConfKeyObj.alias

            taskExecuteData.taskSuiteExecuteId = taskSuiteExecuteModel.id
            taskExecuteData.save(force_insert=True)
            taskExecuteIdList.append(taskExecuteData.id)
            RedisCache().set_data("%s_taskExecute_%s" % ("HTTP",taskExecuteData.id), "0:0:0:0:0", 60 * 60 * 12)
            RedisCache().set_data("%s_taskExecuteStatus_%s" % ("HTTP",taskExecuteData.id), "1", 60 * 60 * 12)
            RedisCache().set_data("%s_taskSuite_%s_task_%s" % ("HTTP",taskSuiteExecuteModel.id, taskExecuteData.id),
                                  json.dumps({"progress": 0, "testResult": "", "execStatus": 0}), 60 * 60 * 12)
            tcpin = '{"do":3,"TaskExecuteId":%s,"TaskExecuteEnv":"%s","TaskId":"%s","protocol":"HTTP","TaskSuiteExecuteId":"%s"}' % (
                taskExecuteData.id, taskExecuteData.httpConfKey_id, taskExecuteData.taskId, taskSuiteExecuteModel.id)
            taskExecuteTcpList.append(tcpin)

    taskSuiteExecuteModel.taskExecuteIdList = ",".join('%s' % id for id in taskExecuteIdList)
    taskSuiteExecuteModel.save(force_update=True)
    taskSuiteRedisDict = {"taskExecuteIdList": taskExecuteIdList, "execStatus": 1, "progress": 0,"protocol":taskSuiteData.protocol}
    RedisCache().set_data("%s_taskSuiteExecuteId_%s" % ("HTTP",taskSuiteExecuteModel.id), json.dumps(taskSuiteRedisDict),60 * 60 * 12)
    for index in taskExecuteTcpList:
        retApiResult = send_tcp_request(index)
        if retApiResult.code != ApiReturn.CODE_OK:
            RedisCache().del_data("%s_taskSuiteExecuteId_%s" % ("HTTP",taskSuiteExecuteModel.id))
            for taskIndex in taskExecuteTcpList:
                RedisCache().del_data("%s_taskExecute_%s" % ("HTTP",json.loads(taskIndex)['TaskExecuteId']))
                taskExecuteDataDel = TbTaskExecute.objects.get(id=json.loads(taskIndex)['TaskExecuteId'])
                taskExecuteDataDel.testResult = "ERROR"
                taskExecuteDataDel.save()
            taskSuiteExecuteModel.testResult = "ERROR"
            taskSuiteExecuteModel.save()
            addUserLog(request, "invoke->runtasksuite->任务执行发送请求到tcpserver失败！", "FAIL")
            return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, "任务执行添加成功，但是执行服务出现异常，请联系管理员").toJson())

    addUserLog(request, "invoke->runtasksuite->成功", "PASS")
    return getTaskSuiteResult(token, taskSuiteExecuteModel.id, timeout)

def getTaskSuiteResult(token,taskSuiteExecuteId,timeout):
    if isInt(taskSuiteExecuteId) == False or int(taskSuiteExecuteId) < 0 :
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['tasksuiteexecidmustbelagerthan0'], retMsg).toJson())

    startTimer = 0
    while True:
        runRes = TbTaskSuiteExecute.objects.filter(id=taskSuiteExecuteId)
        if runRes:
            runRes = runRes[0]
            if isJson(runRes.testResultMsg):
                runRes.testResultMsg = json.loads(runRes.testResultMsg)
            if not runRes.testReportUrl.startswith("http"):
                runRes.testReportUrl = "HTTP://%s%s" % (host,runRes.testReportUrl)
        else:
            return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['taskexecidmustbelagerthan0'], retMsg).toJson())

        resDict = dbModelToDict(runRes)
        if runRes.execStatus == 3:
            resDict['testResultMsgForShell'] = "%s|%s|%s|%s|%s" \
                % (resDict['testResultMsg']['testResult'],resDict['testResultMsg']['caseTotal'],resDict['testResultMsg']['casePass']
                   ,resDict['testResultMsg']['caseFail'],resDict['testResultMsg']['caseError'])
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK, langDict['invoke']['taskexecutefinished'], resDict).toJson())
        elif runRes.execStatus == 4:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXECUTE_EXCEPTION, langDict['invoke']['taskexecuteexception'], resDict).toJson())
        elif runRes.execStatus == 10:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXECUTE_CANCELLING, langDict['invoke']['taskexecutecanceling'],resDict).toJson())
        elif runRes.execStatus == 11:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXECUTE_CANCELED, langDict['invoke']['taskexecutecanceled'],resDict).toJson())

        if startTimer > timeout :
            return_msg = {}
            return_msg['callbacktaskUrl'] = "HTTP://%s/invoke?opt=callbacktasksuite&token=%s&taskSuiteExecuteId=%s&add_by=%s" % (host,token,taskSuiteExecuteId,addBy)
            # return_msg['canceltaskUrl'] = "HTTP://%s/invoke?opt=canceldubbotask&token=%s&taskExecuteId=%s" % (host,token,taskSuiteExecuteId)
            # return_msg['gettaskprogressUrl'] = "HTTP://%s/invoke?opt=getdubbotaskprogress&token=%s&taskExecuteId=%s" % (host,token,taskSuiteExecuteId)
            return HttpResponse(ApiReturn(ApiReturn.CODE_TIMEOUT, langDict['invoke']['taskexecutetimeout'],return_msg).toJson())

        time.sleep(1)
        startTimer += 1

def callbacktasksuite(request, paramDict):
    taskSuiteExecuteId = paramDict.get("taskSuiteExecuteId")
    if isInt(taskSuiteExecuteId) == False or int(taskSuiteExecuteId) < 0 :
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['tasksuiteexecidmustbelagerthan0'], retMsg).toJson())
    else:
        taskSuiteExecuteId = int(taskSuiteExecuteId)

    return getTaskSuiteResult(token,taskSuiteExecuteId,timeout)

def canceltasksuite(request, paramDict):
    taskSuiteExecuteId = paramDict.get("taskSuiteExecuteId")
    if isInt(taskSuiteExecuteId) == False or int(taskSuiteExecuteId) < 0:
        return HttpResponse(
            ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['taskexecidmustbelagerthan0'], retMsg).toJson())
    else:
        taskSuiteExecuteId = int(taskSuiteExecuteId)

    runRes = TbTaskSuiteExecute.objects.filter(id=taskSuiteExecuteId)
    if runRes:
        runRes = runRes[0]
        if runRes.execBy != addBy:
            return HttpResponse(
                ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['cannotcancelotherusertask'], retMsg).toJson())
        # if runRes.execStatus != 1 and runRes.execStatus != 2:
        #     return HttpResponse(
        #         ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['cannotcancelfinishedtask'], retMsg).toJson())

        try:
            # runRes.execStatus = 10
            # runRes.save(force_update=True)

            taskList = runRes.taskExecuteIdList.split(",")
            for taskIndex in taskList:
                status = TbTaskExecute.objects.get(id=taskIndex).execStatus
                if status == 1 or status == 2:
                    runRes.execStatus = 11
                    runRes.save()
                    RedisCache().del_data("%s_taskSuiteExecuteId_%s" % ("HTTP", taskSuiteExecuteId))

                    RedisCache().del_data("%s_taskExecute_%s" % ("HTTP", taskIndex))
                    RedisCache().del_data("%s_taskExecuteStatus_%s" % ("HTTP", taskIndex))
                    RedisCache().del_data("%s_taskSuite_%s_task_%s" % ("HTTP", taskSuiteExecuteId, taskIndex))

                    tcpin = '{"do":4,"TaskExecuteId":%s,"protocol":"HTTP","TaskSuiteExecuteId":%s}' % (
                    taskIndex, taskSuiteExecuteId)
                    retApiResult = send_tcp_request(tcpin)
                    if retApiResult.code != ApiReturn.CODE_OK:
                        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['taskcancelfailure'], retMsg).toJson())

            return HttpResponse(ApiReturn(ApiReturn.CODE_OK, langDict['invoke']['taskcancelsuccess']).toJson())

        except Exception as e:
            return HttpResponse(
                ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['taskcancelfailure'], retMsg).toJson())
    else:
        return HttpResponse(
            ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['tasktobecancelnotfound'], retMsg).toJson())




#dubbo
def rundubbotasksuite(request,paramDict):
    taskSuiteId = paramDict.get("taskSuiteId", "")
    # 校验comments合法性
    comments = paramDict.get("comments", "")
    emailList = paramDict.get("emailList", "")
    retryCount = paramDict.get("retryCount", 0)
    if taskSuiteId == "":
        return HttpResponse(
            ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['tasksuiteidcannotnull'], retMsg).toJson())

    if version == "CurrentVersion":
        taskSuiteData = Tb2DUBBOTaskSuite.objects.filter(taskSuiteId=taskSuiteId)
    else:
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, "任务集暂不支持历史版本", retMsg).toJson())

    if taskSuiteData:
        taskSuiteData = taskSuiteData[0]
    else:
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['cannotfindtaskinvalidtaskid'], retMsg).toJson())
        # 先写taskSuite
    taskSuiteExecuteModel = Tb2DUBBOTaskSuiteExecute()
    taskSuiteExecuteModel.taskSuiteId = taskSuiteData.taskSuiteId
    taskSuiteExecuteModel.title = taskSuiteData.title
    taskSuiteExecuteModel.taskSuiteDesc = taskSuiteData.taskSuiteDesc
    taskSuiteExecuteModel.protocol = taskSuiteData.protocol
    taskSuiteExecuteModel.status = taskSuiteData.status
    taskSuiteExecuteModel.taskCount = taskSuiteData.taskCount
    taskSuiteExecuteModel.taskList = taskSuiteData.taskList
    taskSuiteExecuteModel.isSendEmail = isSendEmail
    taskSuiteExecuteModel.emailList = emailList == "" and taskSuiteData.emailList or emailList
    taskSuiteExecuteModel.isSaveHistory = isSaveHistory
    taskSuiteExecuteModel.execComments = comments
    taskSuiteExecuteModel.retryCount = retryCount
    taskSuiteExecuteModel.execBy = addBy
    taskSuiteExecuteModel.execTime = datetime.datetime.now()
    taskSuiteExecuteModel.httpConfKeyList = httpConfKey
    taskSuiteExecuteModel.execStatus = 2
    httpConfList = httpConfKey.split(",")
    httpConfKeyAliasList = ""
    for httpConfIndex in httpConfList:
        if httpConfKeyAliasList == "":
            httpConfKeyAliasList = TbConfigHttp.objects.get(httpConfKey=httpConfIndex).alias
        else:
            httpConfKeyAliasList = "%s,%s" % (
            httpConfKeyAliasList, TbConfigHttp.objects.get(httpConfKey=httpConfIndex).alias)
    taskSuiteExecuteModel.httpConfKeyAliasList = httpConfKeyAliasList

    taskSuiteExecuteModel.addBy = addBy
    taskSuiteExecuteModel.save()

    taskList = taskSuiteData.taskList.split(",")

    # 获取taskExecuteId list
    taskExecuteIdList = []
    taskExecuteTcpList = []
    for taskIndex in taskList:
        taskData = Tb2DubboTask.objects.get(taskId=taskIndex)
        for httpConfIndex in range(0, len(httpConfList)):
            taskExecuteData = Tb2DubboTaskExecute()
            taskExecuteData.taskId = taskData.taskId
            if taskSuiteData.emailList != "":
                taskExecuteData.emailList = taskSuiteData.emailList
            else:
                taskExecuteData.emailList = taskData.emailList
            taskExecuteData.title = taskData.title
            taskExecuteData.taskdesc = taskData.taskdesc
            taskExecuteData.protocol = taskData.protocol
            taskExecuteData.businessLineGroup = taskData.businessLineGroup
            taskExecuteData.modulesGroup = taskData.modulesGroup
            taskExecuteData.interfaceCount = taskData.interfaceCount
            taskExecuteData.taskInterfaces = taskData.taskInterfaces
            taskExecuteData.caseCount = taskData.caseCount
            taskExecuteData.taskTestcases = taskData.taskTestcases
            taskExecuteData.interfaceNum = taskData.interfaceNum
            taskExecuteData.emailList = emailList == "" and taskSuiteData.emailList or emailList
            taskExecuteData.addBy_id = addBy
            taskExecuteData.isSaveHistory = isSaveHistory
            # taskExecuteData.isSendEmail = 0

            taskExecuteData.isSendEmail = 0
            taskExecuteData.execBy_id = addBy
            taskExecuteData.version = version
            taskExecuteData.execComments = comments
            taskExecuteData.retryCount = retryCount
            taskExecuteData.httpConfKey_id = httpConfList[httpConfIndex]
            taskExecuteData.taskSuiteExecuteId = taskSuiteExecuteModel.id

            taskExecuteData.save(force_insert=True)
            taskExecuteIdList.append(taskExecuteData.id)
            RedisCache().set_data("%s_taskExecute_%s" % ("DUBBO",taskExecuteData.id), "0:0:0:0:0", 60 * 60 * 12)
            RedisCache().set_data("%s_taskExecuteStatus_%s" % ("DUBBO",taskExecuteData.id), "1", 60 * 60 * 12)
            RedisCache().set_data("%s_taskSuite_%s_task_%s" % ("DUBBO",taskSuiteExecuteModel.id, taskExecuteData.id),
                                  json.dumps({"progress": 0, "testResult": "", "execStatus": 0}), 60 * 60 * 12)
            tcpin = '{"do":3,"TaskExecuteId":%s,"TaskExecuteEnv":"%s","TaskId":"%s","protocol":"DUBBO","TaskSuiteExecuteId":"%s"}' % (
                taskExecuteData.id, taskExecuteData.httpConfKey_id, taskExecuteData.taskId, taskSuiteExecuteModel.id)
            taskExecuteTcpList.append(tcpin)

    taskSuiteExecuteModel.taskExecuteIdList = ",".join('%s' % id for id in taskExecuteIdList)
    taskSuiteExecuteModel.save(force_update=True)
    taskSuiteRedisDict = {"taskExecuteIdList": taskExecuteIdList, "execStatus": 1, "progress": 0,"protocol":taskSuiteData.protocol}
    RedisCache().set_data("%s_taskSuiteExecuteId_%s" % ("DUBBO",taskSuiteExecuteModel.id), json.dumps(taskSuiteRedisDict),60 * 60 * 12)
    for index in taskExecuteTcpList:
        retApiResult = send_tcp_request(index)
        if retApiResult.code != ApiReturn.CODE_OK:
            RedisCache().del_data("%s_taskSuiteExecuteId_%s" % ("DUBBO",taskSuiteExecuteModel.id))
            for taskIndex in taskExecuteTcpList:
                RedisCache().del_data("%s_taskExecute_%s" % ("DUBBO",json.loads(taskIndex)['TaskExecuteId']))
                taskExecuteDataDel = TbTaskExecute.objects.get(id=json.loads(taskIndex)['TaskExecuteId'])
                taskExecuteDataDel.testResult = "ERROR"
                taskExecuteDataDel.save()
            taskSuiteExecuteModel.testResult = "ERROR"
            taskSuiteExecuteModel.save()
            addUserLog(request, "invoke->runtasksuite->任务执行发送请求到tcpserver失败！", "FAIL")
            return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, "任务执行添加成功，但是执行服务出现异常，请联系管理员").toJson())

    addUserLog(request, "invoke->runtasksuite->成功", "PASS")
    return getDubboTaskSuiteResult(token, taskSuiteExecuteModel.id, timeout)

def getDubboTaskSuiteResult(token,taskSuiteExecuteId,timeout):
    if isInt(taskSuiteExecuteId) == False or int(taskSuiteExecuteId) < 0 :
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['tasksuiteexecidmustbelagerthan0'], retMsg).toJson())

    startTimer = 0
    while True:
        runRes = Tb2DUBBOTaskSuiteExecute.objects.filter(id=taskSuiteExecuteId)
        if runRes:
            runRes = runRes[0]
            if isJson(runRes.testResultMsg):
                runRes.testResultMsg = json.loads(runRes.testResultMsg)
            runRes.testReportUrl = "HTTP://%s%s" % (host,runRes.testReportUrl)
        else:
            return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['taskexecidmustbelagerthan0'], retMsg).toJson())

        resDict = dbModelToDict(runRes)
        if runRes.execStatus == 3:
            resDict['testResultMsgForShell'] = "%s|%s|%s|%s|%s" \
                                               % (resDict['testResultMsg']['testResult'],
                                                  resDict['testResultMsg']['caseTotal'],
                                                  resDict['testResultMsg']['casePass'],
                                                  resDict['testResultMsg']['caseFail'],
                                                  resDict['testResultMsg']['caseError'])
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK, langDict['invoke']['taskexecutefinished'], resDict).toJson())
        elif runRes.execStatus == 4:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXECUTE_EXCEPTION, langDict['invoke']['taskexecuteexception'], resDict).toJson())
        elif runRes.execStatus == 10:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXECUTE_CANCELLING, langDict['invoke']['taskexecutecanceling'],resDict).toJson())
        elif runRes.execStatus == 11:
            return HttpResponse(ApiReturn(ApiReturn.CODE_TASK_EXECUTE_CANCELED, langDict['invoke']['taskexecutecanceled'],resDict).toJson())

        if startTimer > timeout :
            return_msg = {}
            return_msg['callbacktaskUrl'] = "HTTP://%s/invoke?opt=callbackdubbotasksuite&token=%s&taskSuiteExecuteId=%s&add_by=%s" % (host,token,taskSuiteExecuteId,addBy)
            # return_msg['canceltaskUrl'] = "HTTP://%s/invoke?opt=canceldubbotask&token=%s&taskExecuteId=%s" % (host,token,taskSuiteExecuteId)
            # return_msg['gettaskprogressUrl'] = "HTTP://%s/invoke?opt=getdubbotaskprogress&token=%s&taskExecuteId=%s" % (host,token,taskSuiteExecuteId)
            return HttpResponse(ApiReturn(ApiReturn.CODE_TIMEOUT, langDict['invoke']['taskexecutetimeout'],return_msg).toJson())

        time.sleep(1)
        startTimer += 1

def callbackdubbotasksuite(request, paramDict):
    taskSuiteExecuteId = paramDict.get("taskSuiteExecuteId")
    if isInt(taskSuiteExecuteId) == False or int(taskSuiteExecuteId) < 0 :
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['tasksuiteexecidmustbelagerthan0'], retMsg).toJson())
    else:
        taskSuiteExecuteId = int(taskSuiteExecuteId)

    return getDubboTaskSuiteResult(token,taskSuiteExecuteId,timeout)

def canceldubbotasksuite(request, paramDict):
    taskSuiteExecuteId = paramDict.get("taskSuiteExecuteId")
    if isInt(taskSuiteExecuteId) == False or int(taskSuiteExecuteId) < 0:
        return HttpResponse(
            ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['taskexecidmustbelagerthan0'], retMsg).toJson())
    else:
        taskSuiteExecuteId = int(taskSuiteExecuteId)

    runRes = Tb2DUBBOTaskSuiteExecute.objects.filter(id=taskSuiteExecuteId)
    if runRes:
        runRes = runRes[0]
        if runRes.execBy != addBy:
            return HttpResponse(
                ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['cannotcancelotherusertask'], retMsg).toJson())
        # if runRes.execStatus != 1 and runRes.execStatus != 2:
        #     return HttpResponse(
        #         ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['cannotcancelfinishedtask'], retMsg).toJson())

        try:
            # runRes.execStatus = 10
            # runRes.save(force_update=True)
            taskList = runRes.taskExecuteIdList.split(",")
            for taskIndex in taskList:
                status = Tb2DubboTaskExecute.objects.get(id=taskIndex).execStatus
                if status == 1 or status == 2:
                    runRes.execStatus = 11
                    runRes.save()
                    RedisCache().del_data("%s_taskSuiteExecuteId_%s" % ("DUBBO", taskSuiteExecuteId))

                    RedisCache().del_data("%s_taskExecute_%s" % ("DUBBO", taskIndex))
                    RedisCache().del_data("%s_taskExecuteStatus_%s" % ("DUBBO", taskIndex))
                    RedisCache().del_data("%s_taskSuite_%s_task_%s" % ("DUBBO", taskSuiteExecuteId, taskIndex))

                    tcpin = '{"do":4,"TaskExecuteId":%s,"protocol":"DUBBO","TaskSuiteExecuteId":%s}' % (
                        taskIndex, taskSuiteExecuteId)
                    retApiResult = send_tcp_request(tcpin)
                    if retApiResult.code != ApiReturn.CODE_OK:
                        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['taskcancelfailure'], retMsg).toJson())

            return HttpResponse(ApiReturn(ApiReturn.CODE_OK, langDict['invoke']['taskcancelsuccess']).toJson())

        except Exception as e:
            return HttpResponse(
                ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['taskcancelfailure'], retMsg).toJson())
    else:
        return HttpResponse(
            ApiReturn(ApiReturn.CODE_PARAM_ERROR, langDict['invoke']['tasktobecancelnotfound'], retMsg).toJson())