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
from apps.webportal.services.webPortalService import WebPortalService
from all_models.models import *
from apps.task.services.HTTP_taskService import HTTP_taskService
import xlrd,openpyxl

def loadAllExcelToDb():
    userDir = "%s/%s/" % (BASE_DIR.replace("\\", "/"), "ui_file_uploads")
    excelFilesDict = {}

    allUserDir = []
    # 有用户的文件夹
    for filename in os.listdir(userDir):
        if os.path.isdir("%s%s" % (userDir,filename)):
            excelFilesDict[filename] = {"userName":TbUser.objects.get(loginName=filename).userName,"sheet":{}}
            userFileList = []
            for excelName in os.listdir("%s%s" % (userDir, filename)):
                # print("%s%s/%s" % (userDir, filename, excelName))
                if os.path.isfile("%s%s/%s" % (userDir, filename, excelName)):
                    userFileList.append(excelName)
                    # print(excelName)
                    for index in userFileList:
                        excelFilesDict[filename]["sheet"][index] = []
                        fileDir = "%s%s/%s" % (userDir, filename, index)
                        # print(fileDir)
                        # print(index)
                        fileType = index.split(".")
                        if fileType[-1] == "xls":
                            workbook = xlrd.open_workbook(fileDir)
                            sheets = workbook.sheet_names()
                            for i in range(len(sheets)):
                                if "case" in sheets[i].lower():
                                    excelFilesDict[filename]["sheet"][index].append(sheets[i])
                        # else:
                        #     # print("##########")
                        #     # print(fileDir)
                        #     wb = openpyxl.load_workbook(fileDir)
                        #     sheets = wb.get_sheet_names()
                        #     for i in range(len(sheets)):
                        #         sheet = wb.get_sheet_by_name(sheets[i])
                        #         excelFilesDict[filename]["sheet"][index].append(sheet.title)
    for index in excelFilesDict:
        for excelIndex in excelFilesDict[index]["sheet"]:
            excelObj = TbUITestExcel()
            excelObj.addBy = index
            excelObj.fileName = excelIndex
            excelObj.sheetNames = "_,_".join(excelFilesDict[index]["sheet"][excelIndex])
            excelObj.save()

if __name__ == "__main__":
    loadAllExcelToDb()