import django
import os
import sys
import traceback
import logging

rootpath = os.path.dirname(os.path.realpath(__file__)).replace("\\","/")
rootpath = rootpath.split("/apps")[0]
# print(rootpath)
syspath=sys.path
sys.path=[]
sys.path.append(rootpath) #指定搜索路径绝对目录
sys.path.extend([rootpath+i for i in os.listdir(rootpath) if i[0]!="."])#将工程目录下的一级目录添加到python搜索路径中
sys.path.extend(syspath)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutotestWebD.settings")# project_name 项目名称
django.setup()
from all_models.models import *
from AutotestWebD.settings import *
from apps.common.func.CommonFunc import *
from django.db import connection


class SrcFileAnalyzeService(object):

    @staticmethod
    def gitPullRecentCode():
        if isWindowsSystem():
            return True
        # return True
        for tmpFolder in srcFolders:
            retBool = False
            for i in range(0,3):
                tmpSrcRoot = "%s/%s" % (srcRootDir,tmpFolder)
                print("Start git pull srcroot: %s ." % tmpSrcRoot)
                output = os.popen('cd %s && git pull' % tmpSrcRoot)
                outStr = output.read()
                print("End git pull srcroot: %s ." % tmpSrcRoot)
                print("OUTPUTSTR:{[ %s ]}" % outStr)
                if "Already up-to-date"  in outStr:
                    #更新成功
                    retBool = True
                    print("git pull successful.")
                    break
                else:
                    print("git pull result:%s" % outStr)
                    print("git pull failed.")

            if retBool == False:
                return False
        return True

    @staticmethod
    def retryGitPullLatestCode():
        isPullLatestCodeSuccessful = False
        for i in range(0, 3):
            if SrcFileAnalyzeService.gitPullRecentCode():
                isPullLatestCodeSuccessful = True
        return isPullLatestCodeSuccessful

    @staticmethod
    def getNameSpace(text):
        nameSpaceStartTag = '@Namespace("'
        nameSpaceEndTag = '")'
        return get_sub_string(text,nameSpaceStartTag,nameSpaceEndTag)

    @staticmethod
    def getActionList(text):
        actionStartTag = '@Action('
        actionEndTag = ','
        splitList = text.split(actionStartTag)
        retActionList = []
        for i in range(1,len(splitList)):
            # if i > 0:
            #     if splitList[i-1].strip().endswith("//") or splitList[i-1].strip().endswith("*"):
            #         #如果是注释掉的，不进行解析
            #         continue
            tmpAction = get_sub_string(splitList[i],'"','"').strip()
            if tmpAction!= "":
                retActionList.append(tmpAction)
        return retActionList

    @staticmethod
    def getActionDictList(text):
        actionStartTag = '@Action('
        actionEndTag = ','
        splitList = text.split(actionStartTag)
        retActionList = []
        for i in range(1,len(splitList)):
            tmpAction = get_sub_string(splitList[i],'"','"').strip()
            tmpAllActionAttr = get_sub_string(splitList[i],'@apiStart','@apiEnd')
            tmpApiStatus = get_sub_string(tmpAllActionAttr,"@apiStatus:","\n").strip()
            tmpBusinessLine = get_sub_string(tmpAllActionAttr,"@businessLine:","\n").strip()
            tmpModules = get_sub_string(tmpAllActionAttr,"@module:","\n").strip()
            tmpmUrl = get_sub_string(tmpAllActionAttr,"@apiUrl:","\n").strip()

            if (tmpAction != "" or tmpmUrl !="") and tmpApiStatus == '1' and tmpBusinessLine != "" and tmpModules != "":
                tmpActionDict = {}
                tmpActionDict['url'] = tmpAction
                tmpActionDict['businessLine'] = tmpBusinessLine
                tmpActionDict['module'] = tmpModules
                tmpActionDict['apiUrl'] = tmpmUrl
                retActionList.append(tmpActionDict)
        return retActionList

    @staticmethod
    def getMappingBase(text):
        nameSpaceStartTag = '@RequestMapping("'
        nameSpaceEndTag = '")'
        return get_sub_string(text,nameSpaceStartTag,nameSpaceEndTag)

    @staticmethod
    def getMappingUrlList(text):
        actionStartTag = '@RequestMapping('
        splitList = text.split(actionStartTag)
        retActionList = []
        for i in range(2,len(splitList)):
            # if i > 0:
            #     if splitList[i-1].strip().endswith("//") or splitList[i-1].strip().endswith("*"):
            #         #如果是注释掉的，不进行解析
            #         continue
            tmpAction = get_sub_string(splitList[i],'"','"').strip()
            if tmpAction!= "":
                retActionList.append(tmpAction)
        return retActionList

    @staticmethod
    def getMappingUrlDictList(text):
        actionStartTag = '@RequestMapping('
        splitList = text.split(actionStartTag)
        retActionList = []
        for i in range(2,len(splitList)):
            tmpAction = get_sub_string(splitList[i],'"','"').strip()
            tmpAllActionAttr = get_sub_string(splitList[i], '@apiStart', '@apiEnd')
            tmpApiStatus = get_sub_string(tmpAllActionAttr, "@apiStatus:", "\n").strip()
            tmpBusinessLine = get_sub_string(tmpAllActionAttr, "@businessLine:", "\n").strip()
            tmpModules = get_sub_string(tmpAllActionAttr, "@module:", "\n").strip()
            tmpmUrl = get_sub_string(tmpAllActionAttr,"@apiUrl:","\n").strip()

            if (tmpAction != "" or tmpmUrl !="") and tmpApiStatus == '1' and tmpBusinessLine != "" and tmpModules != "":
                tmpActionDict = {}
                tmpActionDict['url'] = tmpAction
                tmpActionDict['businessLine'] = tmpBusinessLine
                tmpActionDict['module'] = tmpModules
                tmpActionDict['apiUrl'] = tmpmUrl
                retActionList.append(tmpActionDict)
        return retActionList

    @staticmethod
    def getApiCountsNumByApiRoll(text):
        retCount = 0
        for i in range(0,len(srcFoldersApiRoll)):
            actionStartTag = srcFoldersApiRoll[i]
            tmpCount = text.count(actionStartTag)
            if tmpCount > 0:
                tmpCount += srcFoldersApiRollNumControlFactor[i]
            retCount += tmpCount
        return retCount

    @staticmethod
    def getUrlDictListOnlyByAnno(text):
        reString = "@apiStart([\s\S]*?)@apiEnd"  # 取出所有的apidoc
        p = re.compile(r'%s' % reString)
        apiContentList = p.findall(text)
        retActionList = []
        for i in range(0,len(apiContentList)):
            tmpAllActionAttr = apiContentList[i]
            tmpApiStatus = get_sub_string(tmpAllActionAttr, "@apiStatus:", "\n").strip()
            tmpBusinessLine = get_sub_string(tmpAllActionAttr, "@businessLine:", "\n").strip()
            tmpModules = get_sub_string(tmpAllActionAttr, "@module:", "\n").strip()
            tmpmUrl = get_sub_string(tmpAllActionAttr,"@apiUrl:","\n").strip()
            # if tmpmUrl !="" and tmpApiStatus == '1' and tmpBusinessLine != "" and tmpModules != "":
            # 不做非法校验，在写数据库的时候，把错误的原因也写入db
            tmpActionDict = {}
            tmpActionDict['businessLine'] = tmpBusinessLine
            tmpActionDict['module'] = tmpModules
            tmpActionDict['url'] = tmpmUrl
            tmpActionDict['apiStatus'] = tmpApiStatus
            retActionList.append(tmpActionDict)
        return retActionList

    @staticmethod
    def analyzeFile(filePath):
        retUrlList = []
        retFileName = SrcFileAnalyzeService.getFileNameByFileRealPath(filePath)
        retFileText = ""
        prefix = ""
        isCorrectFolder = False
        for i in range(0,len(srcFolders)):
            tmpProjectFolder = srcFolders[i]
            if filePath.startswith("/%s/" % tmpProjectFolder):
                prefix = srcFoldersPrefix[i]
                isCorrectFolder = True
        if isCorrectFolder == False:
            return retUrlList,retFileName,retFileText
        fileObj = open("%s%s" % (srcRootDir, filePath),encoding="utf8")
        try:
            all_the_text = fileObj.read()
            retFileText = all_the_text
            #process @namespace @Action
            nameSpace = SrcFileAnalyzeService.getNameSpace(all_the_text)
            actionList = SrcFileAnalyzeService.getActionList(all_the_text)
            for tmpAction in actionList:
                tmpUrl = "%s%s/%s.action" % (prefix,nameSpace,tmpAction)
                retUrlList.append(tmpUrl)
            #process @RequestMapping
            mappingBase = SrcFileAnalyzeService.getMappingBase(all_the_text)
            mappingUrlList = SrcFileAnalyzeService.getMappingUrlList(all_the_text)
            for tmpMappingUrl in mappingUrlList:
                tmpUrl = "%s%s%s" % (prefix,mappingBase,tmpMappingUrl)
                retUrlList.append(tmpUrl)
            return retUrlList,retFileName,retFileText

        except Exception as e:
            print(traceback.format_exc())
            logging.error(traceback.format_exc())
            return retUrlList,retFileName,retFileText

        finally:
            fileObj.close()

    @staticmethod
    def getFileApisCountNum(filePath):
        isCorrectFolder = False
        apisCountNum = 0
        for i in range(0,len(srcFolders)):
            tmpProjectFolder = srcFolders[i]
            if filePath.startswith("/%s/" % tmpProjectFolder):
                isCorrectFolder = True
        if isCorrectFolder == False:
            return apisCountNum

        fileObj = open("%s%s" % (srcRootDir, filePath),encoding="utf8")
        try:
            apisCountNum = SrcFileAnalyzeService.getApiCountsNumByApiRoll(fileObj.read())
            return apisCountNum

        except Exception as e:
            print(traceback.format_exc())
            logging.error(traceback.format_exc())
            return apisCountNum

        finally:
            if fileObj:
                fileObj.close()

    @staticmethod
    def analyzeFileWithAnno(filePath):
        retUrlList = []
        isCorrectFolder = False
        for i in range(0,len(srcFolders)):
            tmpProjectFolder = srcFolders[i]
            if filePath.startswith("/%s/" % tmpProjectFolder):
                prefix = srcFoldersPrefix[i]
                isCorrectFolder = True
        if isCorrectFolder == False:
            return retUrlList
        fileObj = open("%s%s" % (srcRootDir, filePath),encoding="utf8")
        try:
            all_the_text = fileObj.read()
            retFileText = all_the_text
            retUrlList = SrcFileAnalyzeService.getUrlDictListOnlyByAnno(all_the_text) #根据text获取到urlDict
            return retUrlList

        except Exception as e:
            print(traceback.format_exc())
            logging.error(traceback.format_exc())
            return retUrlList

        finally:
            if fileObj:
                fileObj.close()

    @staticmethod
    def getFileRealPathType(filePath):
        rPath = "%s%s" % (srcRootDir, filePath)
        if os.path.isfile(rPath):
            return 1
        elif os.path.isdir(rPath):
            return 2
        else:
            return 0

    @staticmethod
    def getFileNameByFileRealPath(fileRealPath):
        return fileRealPath.split("/")[-1]

    @staticmethod
    def getFileListBySrcFolderConfig(folderPath):
        realPath = "%s%s" % (srcRootDir,folderPath)
        fileList = []
        for files in os.listdir(r"%s" % realPath):
            if files.endswith(".java"):
                fileList.append("%s/%s" % (folderPath,files))
        return fileList

    @staticmethod
    def updateSrcFileConfig(srcFileConfigObj,fileStatus,isAnalyzed):
        srcFileConfigObj.fileStatus = fileStatus
        srcFileConfigObj.isAnalyzed = isAnalyzed
        srcFileConfigObj.save(force_update=True)

    @staticmethod
    def truncateTbStandardInterface():
        cursor = connection.cursor()
        return cursor.execute("TRUNCATE TABLE `tb_standard_interface`")

    @staticmethod
    def createStandardInterfaceUseAnnoDictUrls(urDictListDict):
        retStr = ""
        businessLinesObjSets = TbBusinessLine.objects.all()
        businessDict = {}
        for tmpBusiObj in businessLinesObjSets:
            businessDict[tmpBusiObj.bussinessLineName] = tmpBusiObj

        modulesObjSets = TbModules.objects.all()
        moduleDict = {}
        for tmpModuleObj in modulesObjSets:
            moduleDict[tmpModuleObj.moduleName] = tmpModuleObj

        for tmpK,tmpV in urDictListDict.items():


            fileName = tmpK
            serviceName = fileName.split("/")[1]
            TbStandardInterface.objects.filter(fileName = fileName).delete() #先删除当前文件的已经写过的接口
            urlDictList = tmpV['urlDictList']
            if len(urlDictList) == 0:
                if retStr == "":
                    retStr = "WARNING:\n"
                retStr += "文件[%s]没有找到合法注释！\n" % (fileName)
                #如果url的长度是0，就是没有找到合法注释，加入错误条目
                tmpStandardInterface = TbStandardInterface()
                tmpStandardInterface.fileName = fileName
                tmpStandardInterface.serviceName = serviceName
                tmpStandardInterface.interfaceUrl = "文件[%s]没有找到合法注释！\n" % (fileName)
                tmpStandardInterface.businessLineId_id = 1
                tmpStandardInterface.moduleId_id = 1
                tmpStandardInterface.apiStatus = 3
                tmpStandardInterface.interfaceCreateTime = datetime.datetime.now()
                tmpStandardInterface.interfaceUpdateTime = datetime.datetime.now()
                tmpStandardInterface.addBy_id = "wangjl01"
                tmpStandardInterface.modBy = ""
                tmpStandardInterface.save()
                continue

            for i in range(0, len(urlDictList)): #从urlDictList中取出dict值
                tmpStandardInterface = TbStandardInterface()
                tmpStandardInterface.fileName = fileName
                tmpStandardInterface.serviceName = serviceName
                tmpStandardInterface.interfaceCreateTime = datetime.datetime.now()
                tmpStandardInterface.interfaceUpdateTime = datetime.datetime.now()
                tmpStandardInterface.addBy_id = "wangjl01"
                tmpStandardInterface.modBy = ""

                tmpUrlDict = urlDictList[i]
                tmpUrl = tmpUrlDict['url']
                tmpBusinessLine = tmpUrlDict['businessLine']
                tmpModule = tmpUrlDict['module']
                tmpApiStatus = tmpUrlDict['apiStatus']

                if tmpBusinessLine not in businessDict.keys():
                    if retStr == "":
                        retStr = "WARNING:\n"
                    retStr += "文件[%s]的第%d个注释不合法，不存在的业务线[%s]\n" % (fileName, (i + 1), tmpBusinessLine)

                    tmpStandardInterface.interfaceUrl = "文件[%s]的第%d个注释不合法，不存在的业务线[%s]\n" % (fileName, (i + 1), tmpBusinessLine)
                    tmpStandardInterface.businessLineId_id = 1
                    tmpStandardInterface.moduleId_id = 1
                    tmpStandardInterface.apiStatus = 4
                    tmpStandardInterface.save()
                    continue

                tmpStandardInterface.businessLineId = businessDict[tmpBusinessLine]

                if tmpModule not in moduleDict.keys():
                    if retStr == "":
                        retStr = "WARNING:\n"
                    retStr += "文件[%s]的第%d个注释不合法，不存在的模块[%s]\n" % (fileName, (i + 1), tmpModule)

                    tmpStandardInterface.interfaceUrl = "文件[%s]的第%d个注释不合法，不存在的模块[%s]\n" % (fileName, (i + 1), tmpModule)
                    tmpStandardInterface.moduleId_id = 1
                    tmpStandardInterface.apiStatus = 4
                    tmpStandardInterface.save()
                    continue

                tmpStandardInterface.moduleId = moduleDict[tmpModule]

                if tmpApiStatus != "0" and tmpApiStatus != "1":
                    if retStr == "":
                        retStr = "WARNING:\n"
                    retStr += "文件[%s]的第%d个注释不合法，存在不合法的的apiStatus[%s]\n" % (fileName, (i + 1), tmpApiStatus)

                    tmpStandardInterface.interfaceUrl = "文件[%s]的第%d个注释不合法，存在不合法的的apiStatus[%s]\n" % (fileName, (i + 1), tmpApiStatus)
                    tmpStandardInterface.apiStatus = 4
                    tmpStandardInterface.save()
                    continue

                if tmpUrl.startswith("/") == False :
                    if retStr == "":
                        retStr = "WARNING:\n"
                    retStr += "文件[%s]的第%d个注释不合法，url[%s]不是/开头！\n" % (fileName,(i+1),tmpUrl)

                    tmpStandardInterface.interfaceUrl = "文件[%s]的第%d个注释不合法，url[%s]不是/开头！\n" % (fileName,(i+1),tmpUrl)
                    tmpStandardInterface.apiStatus = 4
                    tmpStandardInterface.save()
                    continue

                #删除已经存在的
                # TbStandardInterface.objects.filter(businessLineId = businessDict[tmpBusinessLine],moduleId = moduleDict[tmpModule],interfaceUrl = tmpUrl).delete() #删除存在的同业务线通模块同url的内容,存在多线程问题
                #尝试用sql删除条目 也存在死锁
                # cursor = connection.cursor()
                # cursor.execute("DELETE FROM `tb_standard_interface` WHERE businessLineId = %d AND moduleId = %d AND interfaceUrl = '%s' " % (businessDict[tmpBusinessLine].id,moduleDict[tmpModule].id,tmpUrl))
                # 尝试先查询再处理更新。
                findRepeatObjSets = TbStandardInterface.objects.filter(businessLineId = businessDict[tmpBusinessLine],moduleId = moduleDict[tmpModule],interfaceUrl = tmpUrl)
                if findRepeatObjSets:
                    tmpStandardInterface = findRepeatObjSets[0]
                    tmpStandardInterface.apiStatus = tmpApiStatus
                    tmpStandardInterface.fileName = fileName
                    tmpStandardInterface.serviceName = serviceName
                    tmpStandardInterface.interfaceCreateTime = datetime.datetime.now()
                    tmpStandardInterface.interfaceUpdateTime = datetime.datetime.now()
                    tmpStandardInterface.addBy_id = "wangjl01"
                    tmpStandardInterface.modBy = ""
                    tmpStandardInterface.save(force_update = True)
                else:
                    tmpStandardInterface.interfaceUrl = tmpUrl
                    tmpStandardInterface.apiStatus = tmpApiStatus
                    tmpStandardInterface.save(force_insert= True)

                #############################################################################
                # 根据读出来的文件的URL 更新接口和步骤的业务线和代码 李亚超更新于 20180509
                tbInterfaceDataList = TbHttpInterface.objects.filter(url=tmpUrlDict['url'],state=1)

                for tmpInterfaceData in tbInterfaceDataList:
                    tmpInterfaceData.businessLineId = businessDict[tmpBusinessLine]
                    tmpInterfaceData.moduleId = moduleDict[tmpModule]
                    tmpInterfaceData.save()

                tbTestCaseStepDataList = TbHttpTestcaseStep.objects.filter(url=tmpUrlDict['url'],state=1)
                for tmpTestCaseData in tbTestCaseStepDataList:
                    tmpTestCaseData.businessLineId = businessDict[tmpBusinessLine]
                    tmpTestCaseData.moduleId = moduleDict[tmpModule]
                    tmpTestCaseData.save()

        return retStr