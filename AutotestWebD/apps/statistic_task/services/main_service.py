import apps.common.func.InitDjango
from all_models.models import *
from all_models.models.A0011_version_manage import TbVersionHttpInterface
from django.db import connection
from django.forms.models import model_to_dict
from apps.common.func.CommonFunc import *
from all_models_for_mock.models import *
from apps.common.model.Config import Config

class MainService(object):

    @staticmethod
    def addData(data,addBy):
        newDataDict = {}
        for k, v in data.items():
            newDataDict[k] = data[k]
        newDataDict["addBy"] = addBy
        saveInterface = Tb4StatisticTask.objects.create(**newDataDict)
        return 10000,"新增统计任务成功！"

    @staticmethod
    def getDataById(id):
        return Tb4StatisticTask.objects.filter(id=id)[0]

    @staticmethod
    def getDataByIdToDict(id):
        return dbModelToDict(Tb4StatisticTask.objects.filter(id=id)[0])

    @staticmethod
    def dataSaveEdit(request,postData):
        dataObj = Tb4StatisticTask.objects.filter(id=postData["id"])
        if dataObj:
            if dataObj[0].addBy == "" or dataObj[0].addBy == None:
                postData['addBy'] = postData['modBy']

        dataSaveRes = dataObj.update(**postData)
        return 10000,dataSaveRes

    @staticmethod
    def delDataById(request,id):
        dataObj = Tb4StatisticTask.objects.filter(id=id)
        return dataObj.update(state=0)

    @staticmethod
    def getExecDataById(id):
        return Tb4StatisticTaskExecuteInfo.objects.filter(id=id)[0]

    @staticmethod
    def dataSaveEditSetReason(id,reason):
        dataObj = Tb4StatisticTaskExecuteInfo.objects.filter(id=id)
        if dataObj:
            postData = {"reason":reason,"modTime":get_current_time()}
            dataSaveRes = dataObj.update(**postData)
            return 10000,dataSaveRes
        else:
            return 10001,"没有找到任务执行！"
