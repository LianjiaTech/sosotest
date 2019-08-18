from django.shortcuts import render,HttpResponse
from all_models.models import *
from apps.common.func.WebFunc import *
from urllib import parse
from apps.version_manage.services.common_service import VersionService
from apps.common.config import commonWebConfig
from django.views.decorators.csrf import csrf_exempt
logger = logging.getLogger("django")

def appPackagePage(request):
    text = {}
    text["pageTitle"] = "app包添加"
    text["subPageTitle"] = "app包添加"
    context = {}
    context["option"] = "add"
    context["text"] = text
    context["uiAppPackagePage"] = "current-page"
    return render(request, "ui_test/ui_app_package/app_package.html", context)

def appPackageIsExist(request):
    fileName= request.POST.get("fileName","")
    if fileName == "":
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="未检测到文件").toJson())
    packageDir = "%s/static/ui_test/app_uploads/%s" % (BASE_DIR.replace("\\", "/"),request.session.get("loginName"))
    if os.path.isdir(packageDir):
        packageFile = "%s/%s" % (packageDir,fileName)
        if os.path.isfile(packageFile) or len(TbUiPackage.objects.filter(addBy=request.session.get("loginName"),appFileName=fileName,state=1)) > 0:
            return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="检测到已有同名数据添加，是否覆盖?").toJson())
        elif len(TbUiPackage.objects.filter(addBy=request.session.get("loginName"),state=1)) > 3:
            return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="检测到已添加3个app包文件，单人上传文件数量上限为3，请删除后重新上传").toJson())
        else:
            return HttpResponse(ApiReturn().toJson())
    else:
        os.makedirs(packageDir)
        return HttpResponse(ApiReturn().toJson())

def addPackage(request):

    fileDict = request.FILES
    logger.info("uiAppFile:%s" % fileDict)
    if fileDict == {}:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="未检测到文件").toJson())
    packageDir = "%s/static/ui_test/app_uploads/%s" % (BASE_DIR.replace("\\", "/"),request.session.get("loginName"))
    if not os.path.isdir(packageDir):
        os.makedirs(packageDir)
    if len(TbUiPackage.objects.filter(addBy=request.session.get("loginName"),state=1)) > 3:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="检测到已添加3个app包文件，单人上传文件数量上限为3，请删除后重新上传").toJson())
    packageFile = "%s/%s" % (packageDir, fileDict["file"])
    tbModule = TbUiPackage()
    tbModuleData = TbUiPackage.objects.filter(addBy=request.session.get("loginName"), appFileName=fileDict["file"],state=1)
    if os.path.isfile(packageFile):
        os.remove(packageFile)
    if len(tbModuleData) > 0:
        tbModule = tbModuleData[0]
    tbModule.title = request.POST.get("title")
    tbModule.packageDesc = request.POST.get("packageDesc")
    tbModule.packageType = int(request.POST.get("packageType"))
    tbModule.appFileName = fileDict["file"]
    if tbModule.packageType == 1:
        tbModule.appPackage = request.POST.get("appPackage")
        tbModule.appActivity = request.POST.get("appActivity")
    else:
        tbModule.bundleId = request.POST.get("bundleId")
    tbModule.state = 1
    tbModule.addBy = request.session.get("loginName")
    tbModule.save()
    tbModule.packageId = "UI_PACKAGE_%s" % tbModule.id
    tbModule.save()
    destination = open(os.path.join(packageFile), "wb+")
    for chunk in fileDict["file"].chunks():
        destination.write(chunk)
    destination.close()

    return HttpResponse(ApiReturn().toJson())

def appPackageCheckPage(request):
    context = {}
    if not isRelease:
        context["env"] = "test"
    context["uiAppPackageCheckPage"] = "current-page"
    context["userName"] = request.session.get("userName")
    #文本
    text = {}
    text["pageTitle"] = "app包查看"
    context["text"] = text
    context["page"] = 1
    addUserLog(request,"app包管理->查看列表->页面展示->成功","PASS")
    return render(request,"ui_test/ui_app_package/app_package_check.html",context)


def appPackageCheckSunPage(request):
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "app包管理->查看列表->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))

    orderBy = request.POST.get("orderBy")
    if isSqlInjectable(orderBy):
        addUserLog(request, "app包管理->查看列表->获取数据->SQL注入检测时发现查询条件非法", "FAIL")
        return HttpResponse("<script>alert('查询条件非法');</script>")

    #根据版本判断应该从哪个表里取数据 王吉亮添加于20180224
    # if VersionService.isCurrentVersion(request):
    #     tbName = "tb_http_interface"
    #     versionCondition = ""
    # else:
    #     tbName = "tb_version_http_interface"
    #     versionCondition = "and versionName='%s'" % request.session.get("version")

    execSql = "SELECT p.*,u.userName from tb_ui_package p LEFT JOIN tb_user u ON u.loginName = p.addBy WHERE 1=1 and p.state=1 "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        elif key == "caseFounder" :
            checkList.append("%%%s%%" % checkArr[key])
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and (p.addBy LIKE %s or u.userName LIKE %s) """
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and i.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql,attrList=checkList,page=page,pageNum=commonWebConfig.interFacePageNum)
    for index in context["pageDatas"]:
        if index["packageType"] == 1:
            index["typeText"] = "android"
        else:
            index["typeText"] = "ios"

        if index["appPackage"] == "":
            index["appPackage"] = "-"
        if index["appActivity"] == "":
            index["appActivity"] = "-"
        if index["bundleId"] == "":
            index["bundleId"] = "-"
    response = render(request, "ui_test/ui_app_package/subPages/app_package_sub_page.html",context)
    addUserLog(request, "app包管理->查看列表->获取数据->成功", "PASS")
    return response

def delAppPackage(request):

    dataId = request.GET.get("id")
    try:
        tbModule = TbUiPackage.objects.get(id=dataId)
        if tbModule.addBy != request.session.get("loginName"):
            return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="只可以删除自己的文件").toJson())
        tbModule.state = 0
        tbModule.save()
        packageDir = "%s/static/ui_test/app_uploads/%s/%s" % (BASE_DIR.replace("\\", "/"), request.session.get("loginName"),tbModule.appFileName)
        os.remove(packageDir)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR,message="查询数据出现异常，请联系管理员").toJson())

    return HttpResponse(ApiReturn().toJson())

def editAppPackagePage(request):
    text = {}
    text["pageTitle"] = "app包添加"
    text["subPageTitle"] = "app包添加"
    context = {}
    context["option"] = "edit"
    context["text"] = text
    context["uiAppPackagePage"] = "current-page"
    context["dataId"] = request.GET.get("id")
    return render(request, "ui_test/ui_app_package/app_package.html", context)

def saveEditAppPackage(request):


    try:
        tbModule = TbUiPackage.objects.get(id=request.POST.get("dataId"))

        fileDict = request.FILES
        logger.info("uiAppFile:%s" % fileDict)
        if fileDict != {}:
            packageDir = "%s/static/ui_test/app_uploads/%s" % (BASE_DIR.replace("\\", "/"), request.session.get("loginName"))
            packageFile = "%s/%s" % (packageDir, fileDict["file"])
            if os.path.isfile(packageFile):
                os.remove(packageFile)
            destination = open(os.path.join(packageFile), "wb+")
            for chunk in fileDict["file"].chunks():
                destination.write(chunk)
            destination.close()
        tbModule.title = request.POST.get("title")
        tbModule.packageDesc = request.POST.get("packageDesc")
        tbModule.packageType = int(request.POST.get("packageType"))
        tbModule.appFileName = request.POST.get("fileName")
        if tbModule.packageType == 1:
            tbModule.appPackage = request.POST.get("appPackage")
            tbModule.appActivity = request.POST.get("appActivity")
        else:
            tbModule.bundleId = request.POST.get("bundleId")
        tbModule.state = 1
        tbModule.addBy = request.session.get("loginName")
        tbModule.save()
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR,message="请检查提交数据的正确性").toJson())

    return HttpResponse(ApiReturn().toJson())

def getAppPackage(request):

    dataId = request.POST.get("dataId")
    try:
        tbModule = TbUiPackage.objects.get(id=dataId,state=1)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR,message="未查询到数据").toJson())
    return HttpResponse(ApiReturn(body=dbModelToDict(tbModule)).toJson())

@csrf_exempt
def uploadAPK(request):
    tbModule = TbUiAutoUploadPackage()
    try:
        tbModule.appType = "android"
        packageDir = "%s/static/ui_test/app_android/" %  BASE_DIR.replace("\\", "/")

        fileDict = request.FILES
        fileName = str(fileDict["file"])
        if fileName.endswith(".apk"):
            if fileDict != {}:
                packageFile = "%s/%s" % (packageDir, fileDict["file"])
                if os.path.isfile(packageFile):
                    os.rename(packageFile, "%s%s.%s".replace(" ","_") % (packageDir,fileName, datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")))
                destination = open(os.path.join(packageFile), "wb+")
                for chunk in fileDict["file"].chunks():
                    destination.write(chunk)
                destination.close()
            tbModule.uploadResult = 1
            tbModule.save()
            return HttpResponse(ApiReturn().toJson())
        else:
            tbModule.uploadResult = 0
            tbModule.save()
            return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="必须以.apk结尾").toJson())
    except Exception as e:
        print(traceback.format_exc())
        tbModule.uploadResult = 0
        tbModule.save()
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR).toJson())


#为ios文件上传提供的接口，ios端要提供的是zip包
@csrf_exempt
def uploadAPP(request):
    tbModule = TbUiAutoUploadPackage()
    try:
        tbModule.appType = "ios"
        packageDir = "%s/static/ui_test/app_ios/" %  BASE_DIR.replace("\\", "/")

        fileDict = request.FILES
        fileName = str(fileDict["file"])
        if fileName.endswith(".zip"):
            if fileDict != {}:
                packageFile = "%s/%s" % (packageDir, fileName)
                if os.path.isfile(packageFile):
                    os.rename(packageFile, "%s%s.%s" % (packageDir,fileName, datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")))
                destination = open(os.path.join(packageFile), "wb+")
                for chunk in fileDict["file"].chunks():
                    destination.write(chunk)
                destination.close()
            tbModule.uploadResult = 1
            tbModule.save()
            return HttpResponse(ApiReturn().toJson())
        else:
            tbModule.uploadResult = 0
            tbModule.save()
            return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="必须以.zip结尾").toJson())
    except Exception as e:
        logger.error(e)
        print(traceback.format_exc())
        tbModule.uploadResult = 0
        tbModule.save()
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR).toJson())