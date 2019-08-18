import apps.common.func.InitDjango
from all_models.models import *
from all_models.models.A0011_version_manage import TbVersionHttpInterface
from django.db import connection
from django.forms.models import model_to_dict
from apps.common.func.CommonFunc import *
from apps.common.func.ValidataFunc import *
from all_models_for_mock.models import *
from apps.common.model.Config import Config

class MainService(object):

    @staticmethod
    def addData(data,addBy):
        newDataDict = {}
        for k, v in data.items():
            newDataDict[k] = data[k]

        if newDataDict["keywordKey"] == "":
            #数据关键字模式
            newDataDict["type"] = "DATA_KEYWORD"
            newDataDict["keywordKey"] = get_sub_string(data['keywordCode'], "def ", "(").strip()
            if not data['keywordCode'].startswith("@keyword()\n"):
                return 10001,"开头必须使用装饰器@keyword()"
            if '(value,context,strTobeProcessed = ""):' not in data['keywordCode']:
                return 10001,""""函数定义必须严格按照规范 def YOUR_KEYWORD_HER2E(value,context,strTobeProcessed = ""):"""
        else:
            newDataDict["type"] = "PYTHON_CODE"


        newDataDict["addBy"] = addBy
        newDataDict["status"] = 3 #默认设置为审核通过

        if newDataDict["keywordKey"] == "":
            return 10001,"key不能为空！"
        if newDataDict["keywordKey"] == "YOUR_KEYWORD_HERE":
            return 10001, "请不要使用默认函数名YOUR_KEYWORD_HERE"
        if MainService.getDataKeywordByKey(newDataDict["keywordKey"]):
            return 10002,"已经存在的KEY[%s]" % newDataDict["keywordKey"]

        print(data['keywordCode'])
        retVBl,retVMsg = verifyPythonMode(data['keywordCode'])
        print(retVBl)
        if retVBl == False:
            return 10003,retVMsg

        saveInterface = Tb4DataKeyword.objects.create(**newDataDict)
        return 10000,"添加成功！"

    @staticmethod
    def getDataKeywordByKey(dataKey):
        retdk = Tb4DataKeyword.objects.filter(keywordKey=dataKey).first()
        if retdk:
            return True
        else:
            return False

    @staticmethod
    def getDataById(id):
        return Tb4DataKeyword.objects.filter(id=id)[0]

    @staticmethod
    def getDataByKey(key):
        return Tb4DataKeyword.objects.filter(keywordKey=key)[0]

    @staticmethod
    def getDataByIdToDict(id):
        return dbModelToDict(Tb4DataKeyword.objects.filter(id=id)[0])

    @staticmethod
    def dataSaveEdit(request,postData):
        dataObj = Tb4DataKeyword.objects.filter(id=postData["id"])
        if dataObj:
            if dataObj[0].addBy == "" or dataObj[0].addBy == None:
                postData['addBy'] = postData['modBy']

        print(postData['keywordCode'])
        retVBl,retVMsg = verifyPythonMode(postData['keywordCode'])
        print(retVBl)
        if retVBl == False:
            return 10003,retVMsg

        if postData["keywordKey"] == "":
            #数据关键字模式
            postData["keywordKey"] = get_sub_string(postData['keywordCode'], "def ", "(").strip()
            if not postData['keywordCode'].startswith("@keyword()\n"):
                return 10001,"开头必须使用装饰器@keyword()"
            if '(value,context,strTobeProcessed = ""):' not in postData['keywordCode']:
                return 10001,""""函数定义必须严格按照规范 def YOUR_KEYWORD_HER2E(value,context,strTobeProcessed = ""):"""

        dataSaveRes = dataObj.update(**postData)
        return 10000,dataSaveRes

    @staticmethod
    def delDataById(request,id):
        dataObj = Tb4DataKeyword.objects.filter(id=id)
        return dataObj.update(state=0)

