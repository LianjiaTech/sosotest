from django.shortcuts import render,HttpResponse
from apps.common.func.WebFunc import *
from django.http import StreamingHttpResponse
from all_models.models import TbUITestExecute


def uiShowPorgressIndex(request):
    taskExecId = request.GET.get("id","0")
    uiTaskExcuted = TbUITestExecute.objects.filter(id=taskExecId)
    if uiTaskExcuted:
        uiTaskExcuted = uiTaskExcuted[0]
    else:
        return HttpResponse("No task execute found！")
    pageTitle = "%s:%s" % (uiTaskExcuted.taskId, uiTaskExcuted.title)
    context = {}
    context['pageTitle'] = pageTitle
    context['id'] = taskExecId
    return render(request,"ui_test/ui_task/progressShow.html",context = context)

def uiGetTaskProgressData(request):
    taskExecId = request.GET.get("id","0")
    uiTaskExcuted = TbUITestExecute.objects.filter(id=taskExecId)
    if uiTaskExcuted:
        uiTaskExcuted = uiTaskExcuted[0]
        retDict = {}
        if isJson(uiTaskExcuted.execProgressString):
            progressDict = json.loads(uiTaskExcuted.execProgressString)

            currentScreenShot = "/static/ui_test/reports/%s/screenshot/%s" % (uiTaskExcuted.reportDir,progressDict['currentCaseStepScreenShot'])
            currentCaseId = progressDict['currentCaseId'] +": " + progressDict['currentCaseTitle']
            currentStepId = progressDict['currentCaseStepId'] + ": " + progressDict['currentCaseStepTitle']
            currentRealNotRun = int(progressDict['realNotrunTestcaseStepCount'])
            totalStepCount = int(progressDict['totalTestcaseStepCount'])
        else:
            currentScreenShot = ""
            currentCaseId = ""
            currentStepId = ""
            currentRealNotRun = 0
            totalStepCount = 0

        realLogPath = "%s/static/ui_test/reports/%s/report.log" % (BASE_DIR.replace("\\", "/"), uiTaskExcuted.reportDir)
        with open(realLogPath, 'r') as f:
            currentLogStr = f.read()

        retDict['currentScreenShot'] = currentScreenShot
        retDict['currentCaseId'] = currentCaseId.replace("\n","<br>")
        retDict['currentStepId'] = currentStepId.replace("\n","<br>")
        retDict['currentRealNotRun'] = currentRealNotRun
        retDict['totalStepCount'] = totalStepCount
        retDict['currentLogStr'] = currentLogStr.replace("\n","<br>")

        retDict['execStatus'] = uiTaskExcuted.execStatus
        return HttpResponse(json.dumps(retDict))
    else:
        return HttpResponse("No task execute found！")

def uiShowProgressing(request):
    taskExecId = request.GET.get("id","0")
    context = {}
    resp = StreamingHttpResponse(stream_response_generator(taskExecId,))
    return resp

def stream_response_generator(taskExecId):

    isFirstRet = True
    lastScreenShot = ""
    lastCaseId = ""
    lastStepId = ""
    lastLogStr = ""
    lastRealNotRun = 0
    while True:
        uiTaskExcuted = TbUITestExecute.objects.filter(id=taskExecId)

        if uiTaskExcuted:
            uiTaskExcuted = uiTaskExcuted[0]
        else:
            yield "No task execute found！"
            break

        if isFirstRet:
            baseHtml = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta charset="utf-8">
    <!-- Title and other stuffs -->
    <title>%s: %s</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="author" content="">

    <link rel="stylesheet" href="/static/style/publicKey.css">

     <!-- Bootstrap -->
    <link href="/static/new_template/vendors/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="/static/new_template/vendors/font-awesome/css/font-awesome.min.css" rel="stylesheet">
    <!-- NProgress -->
    <link href="/static/new_template/vendors/nprogress/nprogress.css" rel="stylesheet">
    <!-- iCheck -->
    <link href="/static/new_template/vendors/iCheck/skins/flat/green.css" rel="stylesheet">
    <!-- bootstrap-progressbar -->
    <link href="/static/new_template/vendors/bootstrap-progressbar/css/bootstrap-progressbar-3.3.4.min.css" rel="stylesheet">
    <!-- JQVMap -->
    <link href="/static/new_template/vendors/jqvmap/dist/jqvmap.min.css" rel="stylesheet"/>
    <!-- bootstrap-daterangepicker -->
    <link href="/static/new_template/vendors/bootstrap-daterangepicker/daterangepicker.css" rel="stylesheet">

    <!-- Custom Theme Style -->
    <link href="/static/new_template/build/css/custom.min.css" rel="stylesheet">
    <link href="/static/new_template/style/commonStyle.css" rel="stylesheet">
    <link href="/static/style/publicKey.css" rel="stylesheet">

    <!--loading-->
    <link href="/static/style/loading.css" rel="stylesheet">

    <!-- HTML5 Support for IE -->
    <!--[if lt IE 9]>
    <script src="/static/js/html5shim.js"></script>
    <![endif]-->
    <!-- Favicon -->

    <script src="/static/new_template/vendors/jquery/dist/jquery.min.js"></script>
    <script src="/static/js/jquery-cookie/jquery.cookie.js"></script>
    <link rel="stylesheet" href="/static/datetime-picker/bootstrap-datetimepicker.min.css">
    <!--<script type="text/javascript" src="/s/js/bootstrap.js"></script>-->
    <script type="text/javascript" src="/static/datetime-picker/bootstrap-datetimepicker.min.js"></script>
    <script type="text/javascript" src="/static/datetime-picker/bootstrap-datetimepicker.zh-CN.js"></script>
    <script type="text/javascript" src="/static/datetime-picker/moment-with-local.js"></script>

     <!--这个是jquery发送post的js文件-->
    <script type="text/javascript" src="/static/frame_work/jQueryPOST.js"></script>

    <!-- Bootstrap -->
    <script src="/static/new_template/vendors/bootstrap/dist/js/bootstrap.min.js"></script>
</head>
<body class="nav-md">
    <div id="screenShot"></div>
    <h2 id="progressBar"></h2>
    <h2 id="status"></h2>
    <h1 id="currentExecuteInfo"></h1>
    <div id="log"></div>
</body>
</html>
""" % (uiTaskExcuted.taskId,uiTaskExcuted.title)
            isFirstRet = False
            yield baseHtml

        """
            {
              "totalTestcaseStepCount": 8,
              "passTestcaseStepCount": 8,
              "failTestcaseStepCount": 0,
              "warningTestcaseStepCount": 0,
              "skipNotrunTestcaseStepCount": 0,
              "realNotrunTestcaseStepCount": 0,
              "currentCaseId": "TC_WEBUI_0001",
              "currentCaseTitle": "测试修改数字配置",
              "currentCaseStepId": "CaseStep5->Common->LOGINTOLJ->CStep4",
              "currentCaseStepTitle": "点击登录",
              "currentCaseStepScreenShot": "driver_TC_WEBUI_0001_7_20180709121517.png",
              "whetherCanCancelTask": "1"
            }
        """
        try:
            progressDict = json.loads(uiTaskExcuted.execProgressString)

            currentScreenShot = progressDict['currentCaseStepScreenShot']
            currentCaseId = progressDict['currentCaseId']
            currentStepId = progressDict['currentCaseStepId']
            currentRealNotRun = progressDict['realNotrunTestcaseStepCount']
            totalStepCount = progressDict['totalTestcaseStepCount']
            if currentScreenShot != lastScreenShot:
                #更新当前截图截图
                yield """<script type="text/javascript">$("#screenShot").html("<img src='/static/ui_test/reports/%s/screenshot/%s' />");</script>""" % (uiTaskExcuted.reportDir,currentScreenShot)

            if (currentCaseId == lastCaseId and currentStepId == lastStepId) == False:
                #更新currentExecuteInfo
                yield """<script type="text/javascript">$("#currentExecuteInfo").html("%s:%s<br>--------%s: %s");</script>""" % (
                    currentCaseId.replace('\\','\\\\"').replace('"','\\"').replace("\n","<br>"),
                    progressDict['currentCaseTitle'].replace('\\','\\\\"').replace('"','\\"').replace("\n","<br>"),
                    currentStepId.replace('\\','\\\\"').replace('"','\\"').replace("\n","<br>"),
                    progressDict['currentCaseStepTitle'].replace('\\','\\\\"').replace('"','\\"').replace("\n","<br>"))


            # if currentRealNotRun != lastRealNotRun:
            #     # 更新进度
            #     yield """<script type="text/javascript">$("#progressBar").html("任务执行进度：%.2f%%");</script>""" % float((float(totalStepCount) - float(currentRealNotRun))/float(totalStepCount))
            # elif currentRealNotRun == 0:
            #     yield """<script type="text/javascript">$("#progressBar").html("任务执行进度：100%");</script>"""
            # elif lastRealNotRun== 0:
            #     yield """<script type="text/javascript">$("#progressBar").html("任务执行进度：0%");</script>"""

            realLogPath = "%s/static/ui_test/reports/%s/report.log" % (BASE_DIR.replace("\\","/"),uiTaskExcuted.reportDir)
            with open(realLogPath,'r') as f:
                currentLogStr = f.read()

            if lastLogStr == "":
                lastLogStr = currentLogStr
                yield """<script type="text/javascript">$("#log").html("<h2>执行LOG如下：</h2>%s");</script>""" % currentLogStr.replace('\\','\\\\"').replace('"','\\"').replace("\n","<br>")
            elif currentLogStr != lastLogStr:
                #更新log
                appendLogStr = currentLogStr.replace(lastLogStr,"")
                lastLogStr = currentLogStr
                yield """<script type="text/javascript">$("#log").append("%s");</script>""" % appendLogStr.replace('\\','\\\\"').replace('"','\\"').replace("\n","<br>")

            if uiTaskExcuted.execStatus == 3:
                yield """<script type="text/javascript">$("#status").html("任务执行状态：已经执行结束");</script>"""
                break
            elif uiTaskExcuted.execStatus == 4:
                yield """<script type="text/javascript">$("#status").html("任务执行状态：执行异常");</script>"""
                break
            elif uiTaskExcuted.execStatus == 11:
                yield """<script type="text/javascript">$("#status").html("任务执行状态：已取消");</script>"""
                break
            elif uiTaskExcuted.execStatus == 1:
                yield """<script type="text/javascript">$("#status").html("任务执行状态：排队中......");</script>"""
            elif uiTaskExcuted.execStatus == 2:
                yield """<script type="text/javascript">$("#status").html("任务执行状态：执行中......");</script>"""

        except :
            logging.debug(uiTaskExcuted.execProgressString)


        time.sleep(0.3)