import django
import os
import sys
import traceback
import logging
from threading import Thread,Lock,RLock

rootpath = os.path.dirname(os.path.realpath(__file__)).replace("\\","/")
rootpath = rootpath.split("/apps")[0]
syspath=sys.path
sys.path=[]
sys.path.append(rootpath) #指定搜索路径绝对目录
sys.path.extend([rootpath+i for i in os.listdir(rootpath) if i[0]!="."])#将工程目录下的一级目录添加到python搜索路径中
sys.path.extend(syspath)

from apps.src_file_analyze.services.src_file_analyzeService import *

maxThread = 20
aliveThreadCount = 0
threadList = []
lock = RLock()
retStr = ""

def processFolder(myfolder):
    try:
        global retStr
        myFolderFilesHaveAnnoCount = 0
        for root, dirs, files in os.walk(myfolder):
            messageDict = {}
            #将第一个目录的所有file遍历一遍
            for tmpFile in files:
                isValidFileWithCorrectFileName = False
                for tmpLastRoleName in srcFoldersLastFileNameRole:
                    if tmpFile.endswith(tmpLastRoleName):
                        isValidFileWithCorrectFileName = True
                        break
                if isValidFileWithCorrectFileName:
                    realPath = (root + os.sep + tmpFile).replace("\\" ,"/")
                    fileRealPath = realPath.split(srcRootDir)[1].replace("\\" ,"/")
                    retUrlList = SrcFileAnalyzeService.analyzeFileWithAnno(fileRealPath)
                    messageDict[fileRealPath] = {}
                    messageDict[fileRealPath]['urlDictList'] = retUrlList
            #将第一个目录的所有url写进来
            if len(messageDict) > 0:
                myFolderFilesHaveAnnoCount += len(messageDict)
                retMessage = SrcFileAnalyzeService.createStandardInterfaceUseAnnoDictUrls(messageDict)  # 在写入所有
                if retMessage != "":
                    lock.acquire()
                    retStr += "\n%s" % retMessage
                    lock.release()

            messageDict.clear() #写完后清空messageDict
        lock.acquire()
        retStr += "\n======================================================================\nProcessed folder:%s\nHave %d files with correct anno.\nDONE:Update finished!" % (myfolder,myFolderFilesHaveAnnoCount)
        lock.release()
    except Exception as e:
        lock.acquire()
        retStr += "\nEXCEPTION:exception occurred:\n%s" % traceback.format_exc()
        lock.release()

if __name__ == "__main__":
    startTime = time.time()
    #第一步，先拉代码，没更新成功，退出。
    if SrcFileAnalyzeService.gitPullRecentCode() == False:
        retStr = "ERROR: Cannot git pull code!"
        print(retStr)
        sys.exit(0)
    time.sleep(2)
    #第二步，删除数据表中原有数据重新遍历
    SrcFileAnalyzeService.truncateTbStandardInterface()  # 先删除所有
    time.sleep(2)
    #第三步，多线程处理多个folder
    # processFolder(srcRootDir+"/apps-ingage-channel")
    for tmpFolder in srcFolders:
        tobeProcessedFolder = "%s/%s" % (srcRootDir,tmpFolder)
        t = Thread(target=processFolder, args=(tobeProcessedFolder,))  # 启动刚刚创建的线程
        t.start()
        threadList.append(t)
    for tmpThread in threadList:
        if tmpThread.is_alive():
            tmpThread.join()
    endTime = time.time()
    print("TakeTime: %s" % str(endTime - startTime))
    print("DONE: UPDATE FINISHED.")
    print(retStr)

