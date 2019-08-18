from apps.common.model.RedisDBConfig import *
from django.views.decorators.csrf import csrf_exempt
from apps.common.func.WebFunc import *
from apps.common.config import commonWebConfig
import datetime,requests,time
from urllib import parse
import datetime
import requests
import time
from urllib import parse

from django.views.decorators.csrf import csrf_exempt

from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from apps.common.model.RedisDBConfig import *

logger = logging.getLogger("django")
def deploymentPage(request):
    context = {}
    context["deploymentPage"] = "current-page"
    text = {}
    text["pageTitle"] = "一键部署工具"
    text["subPageTitle"] = "一键部署工具"
    context["text"] = text
    return render(request, "tools/deployment_tool/deploymentTool.html", context)

def initGetText(request):
    ret = {}
    cookies = request.COOKIES
    ret["jiraUserName"] = cookies.get("jiraUserName")
    ret["jiraPassword"] = cookies.get("jiraPassword")
    ret["gerritUserName"] = cookies.get("gerritUserName")
    ret["gerritPassword"] = cookies.get("gerritPassword")
    ret["releasemgrUserName"] = cookies.get("releasemgrUserName")
    ret["releasemgrPassword"] = cookies.get("releasemgrPassword")
    ret["filterId"] = cookies.get("filterId")
    ret["OPSType"] = cookies.get("OPSType")
    for index in ret:
        #如果一个为空 则不填写
        if not ret[index]:
            return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR).toJson())
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK,body=ret).toJson())

@csrf_exempt
def doDeployment(request):
    loginName = request.session.get("loginName")
    if not loginName:
        token = request.POST.get("token",None)
        if not token:
            return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR,message="token错误").toJson())
        try:
            loginName = TbUser.objects.get(token=request.POST.get("token")).loginName
        except:
            return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="token错误").toJson())

    redisKey = "deployment_%s_%s" % (loginName,int(time.time() * 1000))
    autoFlag = request.POST.get("autoFlag",0)
    reMark = request.POST.get("reMark","")
    table = TbUserDeploymentTool()
    table.redisKey = redisKey
    table.remark = reMark
    table.status = 1
    table.autoFlag = autoFlag
    table.addBy = loginName
    table.save()
    RedisCache().set_data(redisKey, """{"status":0}""", 60 * 60 * 12)
    ret = {}
    ret["jiraUserName"] = request.POST.get("jiraUserName")
    ret["jiraPassword"] = request.POST.get("jiraPassword")
    ret["gerritUserName"] = request.POST.get("gerritUserName")
    ret["gerritPassword"] = request.POST.get("gerritPassword")
    ret["releasemgrUserName"] = request.POST.get("releasemgrUserName")
    ret["releasemgrPassword"] = request.POST.get("releasemgrPassword")
    ret["filterId"] = request.POST.get("filterId")
    ret["OPSType"] = request.POST.get("OPSType")
    ret["redisKey"] = redisKey
    for index in ret:
        #如果一个为空 则不填写
        if not ret[index]:
            return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR).toJson())
    ret["autoFlag"] = autoFlag
    ret["initiator"] = request.POST.get("initiator","未知用户")

    # 发送HTTP
    req = requests.post(url="http://autotest.ingageapp.com:22222/autodeploy/doCheckAndDeploy", data=ret)
    try:
        logger.info("发送部署请求的返回值为：%s " % req.text)
        print(req.text)
        reqDict = json.loads(req.text)
    except:
        logger.info("发送部署请求的返回值解析异常：%s " % req.text)
        reqDict = {"status":"FAIL","statusCode":1001,"message":"结果解析失败，返回结果为%s" % req.text}
        RedisCache().del_data(redisKey)

    if reqDict["statusCode"] == 106 or reqDict["statusCode"] == 109:
        RedisCache().del_data(redisKey)

    now = (datetime.datetime.now() + datetime.timedelta(days=7 * 4 * 12))
    response = HttpResponse(ApiReturn(ApiReturn.CODE_OK,body=req.text).toJson())
    response.set_cookie("jiraUserName", ret["jiraUserName"], expires=now)
    response.set_cookie("jiraPassword", ret["jiraPassword"], expires=now)
    response.set_cookie("gerritUserName", ret["gerritUserName"], expires=now)
    response.set_cookie("gerritPassword", ret["gerritPassword"], expires=now)
    response.set_cookie("releasemgrUserName", ret["releasemgrUserName"], expires=now)
    response.set_cookie("releasemgrPassword", ret["releasemgrPassword"], expires=now)
    response.set_cookie("filterId", ret["filterId"], expires=now)
    response.set_cookie("OPSType", ret["OPSType"], expires=now)

    return response

@csrf_exempt
def deploymentCallBack(request):
    result = request.POST.get("result")
    try:
        resultDict = json.loads(result)
    except Exception as e:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR,message="返回result解析失败").toJson())
    redisKey = resultDict["task"]["redisKey"]
    file = request.FILES.get("files")
    if file :
        filedir = "%s/static/tools" % (BASE_DIR.replace("\\", "/") )
        if not os.path.exists(filedir):
            os.makedirs(filedir)
        realPath = "%s/%s" % (filedir, file)
        if os.path.exists(realPath):
            os.remove(realPath)
        destination = open(os.path.join(realPath), "wb+")
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
    else:
        file = ""
    try:
        tableObj = TbUserDeploymentTool.objects.get(redisKey=redisKey)
        tableObj.opsList = len(resultDict["opsList"]) == 0 and "-" or ",".join(resultDict["opsList"])
        tableObj.strongCheckSuccessList = len(resultDict["strongCheckSuccessList"]) == 0 and "-" or ",".join(resultDict["strongCheckSuccessList"])
        tableObj.weakCheckSuccessList = len(resultDict["weakCheckSuccessList"]) == 0 and "-" or ",".join(resultDict["weakCheckSuccessList"])
        tableObj.strongCheckFailedList = len(resultDict["strongCheckFailedList"]) == 0 and "-" or ",".join(resultDict["strongCheckFailedList"])
        tableObj.weakCheckFailedList = len(resultDict["weakCheckFailedList"]) == 0 and "-" or ",".join(resultDict["weakCheckFailedList"])
        tableObj.opsDeploySuccessList = len(resultDict["opsDeploySuccessList"]) == 0 and "-" or ",".join(resultDict["opsDeploySuccessList"])
        tableObj.serviceDeployList = len(resultDict["serviceDeployList"]) == 0 and "-" or ",".join(resultDict["serviceDeployList"])
        tableObj.serviceDeploySuccessList = len(resultDict["serviceDeploySuccessList"]) == 0 and "-" or ",".join(resultDict["serviceDeploySuccessList"])
        tableObj.serviceDeployFailedList = len(resultDict["serviceDeployFailedList"]) == 0 and "-" or ",".join(resultDict["serviceDeployFailedList"])
        tableObj.detail = result
        tableObj.status = resultDict["runningState"]
        tableObj.execResult = resultDict["status"]
        tableObj.message = resultDict["message"] == None and "-" or resultDict["message"]
        tableObj.report = "/static/tools/%s" % file
        if resultDict["runningState"] == 3 or resultDict["runningState"] == 4:
            RedisCache().del_data(redisKey)
            if file:
                # 上传aws
                if isRelease:
                    if http_report_to_AWS == "1":
                        try:
                            os.system("aws s3 cp %s s3://test-team/deploy_report/" % realPath)
                            tableObj.report = "https://test.domain.com/deploy_report/%s" % file
                            os.remove(realPath)
                        except:
                            logging.error("scp到AWS发生异常%s" % traceback.format_exc())
                            tableObj.report = "/static/tools/%s" % file
                pass
        else:
            tableObj.report = ""
        tableObj.save()

    except Exception as e:
        print(traceback.format_exc())
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR,message="数据库中未找到对应的数据  %s " % traceback.format_exc()).toJson())

    return HttpResponse(ApiReturn().toJson())


def deploymentCheck(request):
    context = {}
    if not isRelease:
        context["env"] = "test"
    context["deploymentPageCheck"] = "current-page"
    # 文本
    text = {}
    text["pageTitle"] = "部署查看"
    context["text"] = text
    context["page"] = 1
    return render(request, "tools/deployment_tool/deploymentCheck.html", context)

def deploymentListCheck(request):

    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy")
    if isSqlInjectable(orderBy):
        addUserLog(request, "单接口管理->查看用例->获取数据->SQL注入检测时发现查询条件非法", "FAIL")
        return HttpResponse("<script>alert('查询条件非法');</script>")


    execSql = "SELECT ud.*,u.userName from tb_user_deployment_tool ud LEFT JOIN tb_user u ON ud.addBy = u.loginName WHERE 1=1 and ud.state=1 and (ud.autoFlag = 0 OR ((ud.autoFlag = 1 or ud.autoFlag = 2) and ud.execResult = 'FAIL')) "
    # execSql = "SELECT ud.*,u.userName from tb_user_deployment_tool ud LEFT JOIN tb_user u ON ud.addBy = u.loginName WHERE 1=1 and ud.state=1 and(ud.execResult = 'FAIL' or ud.execResult = 'PASS') and (ud.autoFlag = 0 OR ((ud.autoFlag = 1 or ud.autoFlag = 2) and ud.execResult = 'FAIL')) "
    # execSql = "SELECT ud.*,u.userName from tb_user_deployment_tool ud LEFT JOIN tb_user u ON ud.addBy = u.loginName WHERE 1=1 and ud.state=1   "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        elif key == "caseFounder":
            checkList.append("%%%s%%" % checkArr[key])
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and (ud.addBy LIKE %s or u.userName LIKE %s) """
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and ud.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.interFacePageNum)

    response = render(request, "tools/deployment_tool/subPages/deployment_list_check_page.html", context)
    addUserLog(request, "单接口管理->查看用例->获取数据->成功", "PASS")
    return response

