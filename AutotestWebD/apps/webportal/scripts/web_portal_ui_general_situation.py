import django
import sys, os

rootpath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
rootpath = rootpath.split("/apps")[0]
# print(rootpath)
syspath = sys.path
sys.path = []
sys.path.append(rootpath)  # 指定搜索路径绝对目录
sys.path.extend([rootpath + i for i in os.listdir(rootpath) if i[0] != "."])  # 将工程目录下的一级目录添加到python搜索路径中
sys.path.extend(syspath)

from apps.common.func.WebFunc import *
from apps.webportal.services.webPortalService import WebPortalService
from all_models.models import *
from apps.task.services.HTTP_taskService import HTTP_taskService
import json, requests,copy


if __name__ == "__main__":

    loginUrl = 'http://jira.ingageapp.com/login.jsp'
    loginFormData = {"os_username":"liyc","os_password":"liyc"}
    lr = requests.post(url=loginUrl,data=loginFormData)
    JSESSIONID = lr.cookies.get("JSESSIONID")
    url = "http://jira.ingageapp.com/rest/gadget/1.0/twodimensionalfilterstats/generate?filterId=filter-13452&xstattype=customfield_11435&showTotals=true&sortDirection=desc&sortBy=total&ystattype=project&numberToShow=50&_=1523946330420"
    headers = {"cookie":"JSESSIONID=%s; atlassian.xsrf.token=%s; AWSELB=%s" % (lr.cookies.get("JSESSIONID"),lr.cookies.get("atlassian.xsrf.token"),lr.cookies.get("AWSELB"))}
    r = requests.get(url=url,headers=headers)
    rStr = r.text
    rJson = {"rows":[]}
    try:
        if isJson(rStr):
            rJson = json.loads(rStr)
        androidAutoMated = WebPortalService.reHtmlGetText(rJson["rows"][-1]["cells"][1]["markup"])
        androidAutoMatedNum = 0
        IOSAutoMated = WebPortalService.reHtmlGetText(rJson["rows"][-1]["cells"][3]["markup"])
        IOSAutoMatedNum = 0
        webAutoMated = WebPortalService.reHtmlGetText(rJson["rows"][-1]["cells"][2]["markup"])
        webAutoMatedNum = 0

        if len(androidAutoMated) > 0:
            androidAutoMatedNum = int(androidAutoMated[0])
        if len(IOSAutoMated) > 0:
            IOSAutoMatedNum = int(IOSAutoMated[0])
        if len(webAutoMated) > 0:
            webAutoMatedNum = int(webAutoMated[0])

        allAutoMetedNum = androidAutoMatedNum + IOSAutoMatedNum + webAutoMatedNum

        allTestCaseNum = int(rJson["rows"][-1]["cells"][5]["markup"])

        coverageRate = "%.2f" % (allAutoMetedNum / allTestCaseNum * 100)
    except Exception as e:
        allAutoMetedNum = 0
        allTestCaseNum = 0
        coverageRate = "%.2f" % 0
    tbModel = TbWebPortalUIGeneralSituation()
    tbModel.generalSituationDetail = json.dumps({"allAutoMetedNum":allAutoMetedNum,"allTestCaseNum":allTestCaseNum,"coverageRate":coverageRate})
    tbModel.statisticalTime = datetime.datetime.now()
    tbModel.save()

    print("done!")
