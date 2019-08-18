import django
import sys,os
rootpath = os.path.dirname(os.path.realpath(__file__)).replace("\\","/")
rootpath = rootpath.split("/apps")[0]
# print(rootpath)
syspath=sys.path
sys.path=[]
sys.path.append(rootpath) #指定搜索路径绝对目录
sys.path.extend([rootpath+i for i in os.listdir(rootpath) if i[0]!="."])#将工程目录下的一级目录添加到python搜索路径中
sys.path.extend(syspath)

from apps.common.func.WebFunc import *
from all_models.models import *
import requests,datetime,json

def getInterfaceTest(businessLine):
    now_time = datetime.datetime.now()
    yes_time = now_time + datetime.timedelta(days=-1)
    yes_time_bofore = yes_time.strftime('%Y-%m-%d')
    nt = now_time.strftime('%Y-%m-%d-')
    linkData = dbModelToDict(TbOpenApiUri.objects.filter(state=1)[0])
    #URLDATA
    url = linkData["interfaceTestUri"] + "/" + businessLine + "/" + nt
    # print(url)
    try:
        r = requests.get(url=url,timeout=3)
    except Exception as e :
        return "[]"
    return r.text

if __name__ == "__main__":
    businessLineList = dbModelListToListDict(TbOpenApiBusinessLine.objects.filter(state=1))
    result = {}
    allEnvData = dbModelListToListDict(TbWebPortalStandardEnv.objects.filter(state=1,openapiIsShow=1))
    for blIndex in businessLineList:
        if blIndex["businessLineName"] not in result.keys():
            result[blIndex["businessLineName"]] = {}
        result[blIndex["businessLineName"]] = json.loads(getInterfaceTest(blIndex["businessLineName"]))
        for envIndex in allEnvData:
            flag = 0
            for dataIndex in result[blIndex["businessLineName"]]:
                # print(dataIndex)
                if "profile" in dataIndex.keys() and envIndex["openApiKey"] == dataIndex["profile"]:
                    flag = 1
            if flag == 0:
                result[blIndex["businessLineName"]].append({"profile":envIndex["openApiKey"],"success":0,"total":0,"successRate":0,"status":"NOTRUN"})

        dbModule = TbWebPortOpenApiInterfaceTest()
        dbModule.businessLine = blIndex["businessLineName"]
        if json.dumps(result[blIndex["businessLineName"]]):
            dbModule.interfaceDetail = json.dumps(result[blIndex["businessLineName"]])
        else:
            dbModule.interfaceDetail = {"successRate" : 0,"success":0,"total":0,"status" : "NOTRUN"}
        dbModule.statisticalTime = datetime.datetime.now()
        dbModule.save()
    print("done!")
    # dbModule.save()
