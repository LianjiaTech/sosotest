import django
import os,time,sys
from threading import Thread,Lock

rootpath = os.path.dirname(os.path.realpath(__file__)).replace("\\","/")
rootpath = rootpath.split("/apps")[0]
# print(rootpath)
syspath=sys.path
sys.path=[]
sys.path.append(rootpath) #指定搜索路径绝对目录
sys.path.extend([rootpath+i for i in os.listdir(rootpath) if i[0]!="."])#将工程目录下的一级目录添加到python搜索路径中
sys.path.extend(syspath)

from apps.version_manage.services.get_data_service import GetData

if __name__ == "__main__":
    t0 = time.time()

    #获取当前版本
    currentVersionObj = GetData.getCurrentVersion()#获取当前版本
    if currentVersionObj == False:
        print("没有找到当前版本，封板终止。")
        sys.exit(0)

    #获取未启用版本
    unuseVersionObj = GetData.getUnuseVersion()#获取未启用版本
    if unuseVersionObj == False:
        print("没有找到可启用版本，封板终止。")
        sys.exit(0)

    print("版本%s开始进行封板处理..." % currentVersionObj.versionName)
    #TbVersionGlobalText
    t1 = time.time()
    GetData.saveAllGlobalTextToVersionTable(GetData.getAllGlobalText(),currentVersionObj) #组合文本
    t2 = time.time()
    print("GlobalText:%s" % (t2-t1))
    GetData.saveAllGlobalVarsToVersionTable(GetData.getAllGlobalVars(),currentVersionObj) #全局变量
    t3 = time.time()
    print("GlobalVars:%s" % (t3-t2))
    GetData.saveAllHttpInterfaceToVersionTable(GetData.getAllHttpIntrface(),currentVersionObj) #接口用例
    t4 = time.time()
    print("HttpInterface:%s" % (t4-t3))
    GetData.saveAllHttpTestcaseToVersionTable(GetData.getAllHttpTestcase(), currentVersionObj) #业务场景用例
    t5 = time.time()
    print("HttpTestcase:%s" % (t5 - t4))
    GetData.saveAllHttpTestcaseStepToVersionTable(GetData.getAllHttpTestcaseStep(), currentVersionObj) #场景用例步骤
    t6 = time.time()
    print("HttpTestcaseStep:%s" % (t6 - t5))
    GetData.saveAllTaskToVersionTable(GetData.getAllTask(), currentVersionObj)                          #任务
    t7 = time.time()
    print("HttpTask:%s" % (t7 - t6))
    GetData.saveAllStandardInterfaceToVersionTable(GetData.getAllStandardInterface(), currentVersionObj) #标准接口
    t8 = time.time()
    print("HttpStandardInterface:%s" % (t8 - t7))
    GetData.saveAllTaskSuiteToVersionTable(GetData.getAllTaskSuite(),currentVersionObj)

    #将任务执行表中的CurrentVersion全部换成currentVersionObj.versionName
    GetData.changeTaskExecuteCurrentVersionToVersionName(currentVersionObj)
    print("DONE:任务执行将执行版本修改为上一版本。")

    GetData.changeTaskSuiteExecuteCurrentVersionToVersionName(currentVersionObj)
    print("DONE:任务集合执行将执行版本修改为上一版本。")
    GetData.changeVersionToHistoyVersion(currentVersionObj)                                         #设置为历史版本
    print("DONE：版本%s封板完成！" % currentVersionObj.versionName)

    GetData.changeVersionToUsingVersion(unuseVersionObj)                                            #设置为当前版本
    print("DONE：版本%s启用成功！" % unuseVersionObj.versionName)
    t9 = time.time()
    print("本次封板%s供占用时间:%s秒" % (currentVersionObj.versionName,(t9 - t0)))
    a = "!"
