import logging
import traceback

from copy import deepcopy
import pickle,os
from apps.common.model.ExcelRead import ExcelProcesser
############################exec要用的库，打包用，不能删除############################################
import time

from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction

from appium import webdriver
from selenium import webdriver
####################################################################################################
class UITask(object):

    def __init__(self,confContext = {}):

        self.textDict = {}
        self.gvarDict = {}
        self.pageObjectDict = {}
        self.commonCaseDict = {}
        self.taskCaseList = []
        self.taskDistinctCaseIdList = []

    def generateTaskByFilenameAndSheetname(self,fileName,sheetName = "",execCaseId = ""):

        if os.path.exists(fileName):
            processer = ExcelProcesser(fileName)
            self.textDict = processer.getTEXTDict()
            self.gvarDict = processer.getGVARDict()
            allSheetNameList = processer.getAllSheetNameList()

            #生成通用方法，可以在sheet case中调用。
            for tmpSheetName in allSheetNameList:
                if "Common" in tmpSheetName:
                    tmpCommonCaseDict = processer.getCommonCaseDictBySheetName(tmpSheetName)
                    self.commonCaseDict[tmpSheetName] = tmpCommonCaseDict

            #生成pageObjectdict
            for tmpSheetName in allSheetNameList:
                if "PageObject" in tmpSheetName:
                    tmpPODict = processer.getPageObjectDictBySheetName(tmpSheetName)
                    self.pageObjectDict.update(tmpPODict)

            #生成要执行的caseList
            if sheetName.strip() == "":
                #如果sheetName为空，使用所有带Case的sheet
                for tmpCaseSheetName in allSheetNameList:
                    if "Case" in tmpCaseSheetName:
                        self.taskCaseList += processer.getCaseListBySheetName(tmpCaseSheetName,execCaseId)
            else:
                #不为空使用指定sheet的
                caseSheetList = sheetName.split(",")
                for tmpCaseSheetName in caseSheetList:
                    self.taskCaseList += processer.getCaseListBySheetName(tmpCaseSheetName,execCaseId)
            return True
