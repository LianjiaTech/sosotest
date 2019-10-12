import logging
import os
from core.processor.Config import Config

rootDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))).replace("\\","/")
print("rootDir: %s" % rootDir)
confDict = Config().getConfDictByFile("%s/config.ini" % rootDir)
print("config.ini CONFDICT: %s" % confDict)
releaseRootDir = confDict['DIR']['releaseRoot']  # release环境的rootDir
print("releaseRootDir: %s" % releaseRootDir)

if os.path.isfile("%s/RobotUiTest/DriverConfig.conf" % rootDir):
    driverConfDict = Config.getConfDictByFile("%s/RobotUiTest/DriverConfig.conf" % rootDir)
    print("DriverConfig.conf : %s" % driverConfDict)
else:
    #UI 功能没有开启
    driverConfDict = {}


dbKey = "DB-%s" % confDict['DIR']['useTag']
tcpKey = "TCP-%s" % confDict['DIR']['useTag']
runTcpKey = "RUNTCP-%s" % confDict['DIR']['useTag']
webKey = "WEB-%s" % confDict['DIR']['useTag']
emailKey = "EMAIL-%s" % confDict['DIR']['useTag']
redisKey = "REDIS-%s" % confDict['DIR']['useTag']
clusterKey = "CLUSTER-%s" % confDict['DIR']['useTag']
webTypeKey = "电脑Web"
androidTypeKey = "安卓App"
iosTypeKey = "苹果App"
dirfileKey = "DIRFILE-%s" % confDict['DIR']['useTag']


isReleaseEnv = False
if releaseRootDir == rootDir:
    isReleaseEnv = True
    dbKey = "DB"
    tcpKey = "TCP"
    runTcpKey = "RUNTCP"
    webKey = "WEB"
    emailKey = "EMAIL"
    redisKey = "REDIS"
    clusterKey = "CLUSTER"
    dirfileKey = "DIRFILE"

print("isRelase[%s], TEST_ENV [%s]" % ((isReleaseEnv),confDict['DIR']['useTag']))
print("CONF_KEYS:dbKey[%s] tcpKey[%s] webKey[%s] emailKey[%s]" % (dbKey,tcpKey,webKey,emailKey))

class DBConf(object):
    dbHost = confDict[dbKey]['host']
    dbPort = int(confDict[dbKey]['port'])
    dbUsername = confDict[dbKey]['username']
    dbPassword = confDict[dbKey]['password']
    dbName = confDict[dbKey]['dbname']

print("DBConf: dbHost[%s] dbPort[%s] dbUsername[%s] dbPassword[%s] dbName[%s]" % (DBConf.dbHost,DBConf.dbPort,DBConf.dbUsername,DBConf.dbPassword,DBConf.dbName))

class RedisConf(object):
    redisHost = confDict[redisKey]['host']
    redisPort = confDict[redisKey]['port']
    redisPWD = confDict[redisKey]['password']
print("RedisConf: host[%s] port[%s] password[%s]" % (RedisConf.redisHost,RedisConf.redisPort,RedisConf.redisPWD))

class TcpServerConf(object):
    ip = confDict[tcpKey]['host']
    port = int(confDict[tcpKey]['port'])
    uiport = int(confDict[tcpKey]['uiport'])
    ftpport = int(confDict[tcpKey]['ftpport'])
    maxRequestCount = 20
    recvLength = 1024

class RunTcpServerConf(object):
    ip = ""
    port = 0
    uiport = 0
    maxRequestCount = 20
    recvLength = 1024
print("TcpServerConf: ip[%s] port[%s] uiport[%s] maxRequestCount[%s] recvLength[%s]" % (TcpServerConf.ip,TcpServerConf.port,TcpServerConf.uiport,TcpServerConf.maxRequestCount,TcpServerConf.recvLength))

class LogConfig(object):
    dirfilePath = confDict[dirfileKey]['filepath']
    dirfileLog = confDict[dirfileKey]['log']
    dirfileUploads = confDict[dirfileKey]['uploads']
    dirfileReports = confDict[dirfileKey]['reports']

    logRoot = dirfileLog if "/" in dirfileLog or "\\" in dirfileLog else "%s/%s" % (dirfilePath, dirfileLog)
    uploadsRoot = dirfileUploads if "/" in dirfileUploads or "\\" in dirfileUploads else "%s/%s" % (dirfilePath, dirfileUploads)
    reportsRoot = dirfileReports if "/" in dirfileReports or "\\" in dirfileReports else "%s/%s" % (dirfilePath, dirfileReports)

    if isReleaseEnv:
        LEVEL = logging.INFO #release环境a
        FILE = "%s/AutotestFrameworkRelease.log" % logRoot#release环境
        MainFILE = "%s/AutotestFrameworkMainRelease.log" % logRoot#release环境
        FILE_UILOG = "%s/UIAutotestFrameworkRelease.log" % logRoot#release环境
        FILE_DUBBOLOG = "%s/DubboAutotestFrameworkRelease.log" % logRoot#release环境
    else:
        LEVEL = logging.DEBUG #测试环境
        FILE = "%s/AutotestFramework%s.log" % (logRoot,confDict['DIR']['useTag'])  # 测试环境
        MainFILE = "%s/AutotestFrameworkMain%s.log" % (logRoot,confDict['DIR']['useTag'])  # 测试环境
        FILE_UILOG = "%s/UIAutotestFramework%s.log" % (logRoot,confDict['DIR']['useTag'])  # 测试环境
        FILE_DUBBOLOG = "%s/DubboAutotestFramework%s.log" % (logRoot,confDict['DIR']['useTag'])  # 测试环境


print("LogConfig: logRoot[%s] LEVEL[%s] FILE[%s] UIFILE[%s]\n"
      "reportsRoot: %s\n"
      "uploadsRoot: %s" %
      (LogConfig.logRoot,LogConfig.LEVEL,LogConfig.FILE,LogConfig.FILE_UILOG,LogConfig.reportsRoot,LogConfig.uploadsRoot))

class EnvConfig(object):
    # DONE
    # 初始化好就行了，没必要从db获取
    PLATFORM_ROOT = rootDir
    PYTHON_ROOT = rootDir+"/"+confDict['DIR']['framework']
    WEB_ROOT = rootDir+"/"+confDict['DIR']['web']
    UI_FRAMEWORK_ROOT = rootDir+"/"+confDict['DIR']['uiFramework']
    WEB_URI = confDict[webKey]['uri']

print("EnvConfig: PLATFORM_ROOT[%s] PYTHON_ROOT[%s] WEB_ROOT[%s] WEB_URI[%s] UI_FRAMEWORK_ROOT[%s] " % (EnvConfig.PLATFORM_ROOT,EnvConfig.PYTHON_ROOT,EnvConfig.WEB_ROOT,EnvConfig.WEB_URI,EnvConfig.UI_FRAMEWORK_ROOT))

class EmailConfig(object):
    sender =  confDict[emailKey]['sender']
    smtpserver = confDict[emailKey]['smtpserver']
    username = confDict[emailKey]['username']
    password = confDict[emailKey]['password']

print("EmailConfig: sender[%s] smtpserver[%s] username[%s] password[%s]" % (EmailConfig.sender,EmailConfig.smtpserver,EmailConfig.username,EmailConfig.password))


class ServiceConf(object):
    sql_effect_lines = 10
    framework_version = confDict['SITE']['framework_version']
    # serviceConfList = eval(confDict[clusterKey]['serviceConf'])

print("ServiceConf: sql_effect_lines[%s] framework_version[%s] " % (ServiceConf.sql_effect_lines,ServiceConf.framework_version))

class CommonConf(object):
    support_charset_list = confDict['COMMON']['support_charset'].split(',')
    file_max_show_len = int(confDict['COMMON']['file_max_show_len'])
    if "single_env_run_max_task_nums" in confDict['COMMON'].keys():
        singleServiceEnvRunTaskNumber = int(confDict['COMMON']['single_env_run_max_task_nums'])
    else:
        singleServiceEnvRunTaskNumber = 5

    if "runtask_max_thread_nums" in confDict['COMMON'].keys():
        runtaskMaxThreadNums = int(confDict['COMMON']['runtask_max_thread_nums'])
    else:
        runtaskMaxThreadNums = 20

    groupLevel1 = confDict['COMMON']['groupLevel1']
    groupLevel2 = confDict['COMMON']['groupLevel2']

    if "http_report_to_AWS" in confDict['COMMON'].keys():
        http_report_to_AWS = confDict['COMMON']['http_report_to_AWS']
    else:
        http_report_to_AWS = "0"

print("CommonConf: support_charset_list[ %s ]  file_max_show_len[ %d ]" % (CommonConf.support_charset_list,CommonConf.file_max_show_len))

class isClusterConf(object):
    notRun = 0 #未消费
    runTcpSend = 1 #消费中 不可取消
    runTaskInitDone = 2 #消费中 可取消
    runTaskDone = 3 #消费完毕
    toCancel = 4 #标记为不可消费，等待取消
    cancelTcpSend = 5 #向消费者告知取消操作
    cancelTaskDone = 6 #取消的TCP返回 代表已取消的含义

    runDebugDone = 7

class timeConf(object):
    socketDefaultTime = 15
    runServerHeartBeat = 5
    mainServerHeartBeat = 30


