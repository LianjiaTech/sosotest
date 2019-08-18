import django
import sys,os
rootpath = os.path.dirname(os.path.realpath(__file__)).replace("\\","/")
rootpath = rootpath.split("/apps")[0]
syspath=sys.path
sys.path=[]
sys.path.append(rootpath) #指定搜索路径绝对目录
sys.path.extend([rootpath+i for i in os.listdir(rootpath) if i[0]!="."])#将工程目录下的一级目录添加到python搜索路径中
sys.path.extend(syspath)

from apps.common.func.WebFunc import *
from all_models.models import *
import requests,datetime,json


if __name__ == "__main__":
    env = "product"

    now_time = datetime.datetime.now()

    nt = now_time.strftime('%Y-%m-%d')
    linkData = dbModelToDict(TbOpenApiUri.objects.filter(state=1)[0])
    url = linkData["summaryUri"] + linkData["summaryUrl"] + "/" + nt + "/" + env
    # print(url)
    try:
        r = requests.get(url=url,timeout=3)
        dataDict = json.loads(r.text)

    except Exception as e :
        dataDict = {}
    # print(dataDict)
    #判断请求结果是否成功
    flag = 1
    if "sum" in dataDict.keys():
        dbModule = TbWebPortOpenApiGeneralSituation()
        dbModule.interfaceSum = dataDict["sum"]
        dbModule.covered = dataDict["covered"]
        dbModule.coveredRate = dataDict["coveredRate"]
        dbModule.total = dataDict["total"]
        dbModule.executedRate = 100
        dbModule.profile = dataDict["profile"]
        dbModule.averageInterfaceNum = dataDict["average"]
        dbModule.statisticalTime = datetime.datetime.now()
        dbModule.testBeginTime = dataDict["begin"]
        dbModule.testEndTime = dataDict["end"]
        dbModule.save()
    else:
        flag = 0
    #############################获取各个业务线接口覆盖度
    openApiBusinessLine = dbModelListToListDict(TbOpenApiBusinessLine.objects.filter(state=1))
    for blIndex in openApiBusinessLine:
        blUrl = linkData["summaryUri"] + linkData["summaryUrl"] + "/" + nt + "/" + env + "/" + blIndex["businessLineName"]
        blr = requests.get(url=blUrl)
        # print(blUrl)
        # print(blr.text)
        blDataDict = json.loads(blr.text)
        if not blDataDict:
            blDataDict = {"begin":datetime.datetime.now(),"end":datetime.datetime.now(),"total":0,"covered":0,"coveredRate":0,"scenario":0,
                          "sum":0,"executed":0,"executedRate":0,"profile":" ","host":"https://api-devhttps.xiaoshouyi.com","type": blIndex["businessLineName"]}
        blDbModule = TbWebPortOpenApiBlTest()
        blDbModule.interfaceSum = blDataDict["sum"]
        blDbModule.covered = blDataDict["covered"]
        blDbModule.coveredRate = blDataDict["coveredRate"]
        blDbModule.total = blDataDict["total"]
        blDbModule.executedRate = blDataDict["executedRate"]
        blDbModule.profile = blDataDict["profile"]
        blDbModule.businessLine = blDataDict["type"]
        blDbModule.testBeginTime = blDataDict["begin"]
        blDbModule.testEndTime = blDataDict["end"]
        blDbModule.statisticalTime = datetime.datetime.now()
        blDbModule.save()
    if flag == 1:
        print("done!")