from apps.common.model.RedisDBConfig import *
from apps.common.func.CommonFunc import *

retmsg = ""
logger = logging.getLogger("django")


def getStatisticForAllTask(request):
    startTime = request.GET.get("startTime","")
    endTime = request.GET.get("endTime","")
    statisticTaskId = request.GET.get("statisticTaskId","")
    sqlCondition = " AND e.executeType in('pipeline','daily') "
    if startTime:
        sqlCondition += " AND e.addTime>=%s" % startTime
    if endTime:
        sqlCondition += " AND e.addTime<=%s" % endTime
    if statisticTaskId:
        sqlCondition += " AND e.statisticTaskId=%s" % statisticTaskId

    staticticDataDict = {} #key 是统计任务id，value是一个dict
    sqlTestResult = "SELECT COUNT(*) countnum,statisticTaskId,testResult FROM `tb4_statistic_task_execute_info` e WHERE e.state = 1 %s GROUP BY e.statisticTaskId,e.testResult" % sqlCondition
    resDict = executeSqlGetDict(sqlTestResult)
    #生成每个结果的数据
    for tmpResStatis in resDict:
        tmpkey = str(tmpResStatis['statisticTaskId'])
        if tmpkey not in staticticDataDict.keys():
            staticticDataDict[tmpkey] = {}
        staticticDataDict[tmpkey][tmpResStatis['testResult']] = tmpResStatis['countnum']

    for tmpK,tmpV in staticticDataDict.items():
        total = 0
        if "PASS" in tmpV.keys():
            total += tmpV['PASS']
        else:
            tmpV['PASS'] = 0

        if "FAIL" in tmpV.keys():
            total += tmpV['FAIL']
        else:
            tmpV['FAIL'] = 0

        if "ERROR" in tmpV.keys():
            total += tmpV['ERROR']
        else:
            tmpV['ERROR'] = 0

        tmpV['TOTAL'] = total
        tmpV['passRate'] = "0%" if tmpV['TOTAL'] == 0 else str(round(float(100.00)*float(tmpV['PASS'])/float(tmpV['TOTAL']),2))+"%"
        # tmpV['passRate'] = "0%" if tmpV['TOTAL'] == 0 else float(tmpV['PASS'])/float(tmpV['TOTAL'])

        sqlTitleEtc = "SELECT statisticTaskId,codeCoverage,executeDetailText FROM `tb4_statistic_task_execute_info` e " \
                      "WHERE statisticTaskId=%s AND e.testResult='PASS' AND e.state = 1 %s  ORDER BY e.id DESC" % (tmpK,sqlCondition)

        resDict = executeSqlGetDict(sqlTitleEtc)
        if resDict:
            resDict = resDict[0]
            tmpV['codeCoverage'] = str(resDict['codeCoverage'])+"%"
            tmpV['caseCount'] = json.loads(resDict['executeDetailText'])['total']
        else:
            tmpV['codeCoverage'] = "0.0%"
            tmpV['caseCount'] = 0

        #取业务线模块title等基本信息
        sqlTitleEtc = "SELECT e.id,title,b.bussinessLineName bussinessLineName,m.moduleName moduleName FROM `tb4_statistic_task` e " \
                      "LEFT JOIN tb_business_line b ON b.id = e.businessLineId " \
                      "LEFT JOIN tb_modules m ON m.id = e.moduleId " \
                      "WHERE e.id=%s AND e.state = 1  ORDER BY e.id DESC" % (tmpK)
        resDict = executeSqlGetDict(sqlTitleEtc)
        if resDict:
            resDict = resDict[0]
            tmpV['title'] = resDict['title']
            tmpV['bussinessLineName'] = resDict['bussinessLineName']
            tmpV['moduleName'] = resDict['moduleName']
        else:
            tmpV['title'] = "未发现"
            tmpV['bussinessLineName'] = ""
            tmpV['moduleName'] = ""

        sqlType = "SELECT DISTINCT(e.executeType) runtype FROM `tb4_statistic_task_execute_info` e WHERE e.statisticTaskId=%s  AND e.state = 1 %s  " % (tmpK,sqlCondition)
        typeResList = executeSqlGetDict(sqlType)
        typeStr = ""
        for tmpType in typeResList:
            typeStr += tmpType['runtype']+","
        tmpV['executeType'] = typeStr.strip(",")

        sqlReason = "SELECT DISTINCT(e.reason) reason FROM `tb4_statistic_task_execute_info` e WHERE e.statisticTaskId=%s  AND e.state = 1 %s  " % (tmpK, sqlCondition)
        resonList = executeSqlGetDict(sqlReason)
        reasonStr = ""
        for tmpReason in resonList:
            reasonStr += tmpReason['reason'] + "|"
        tmpV['reason'] = reasonStr.strip("|")

    return HttpResponse(ApiReturn(ApiReturn.CODE_OK,"OK",staticticDataDict).toJson())
