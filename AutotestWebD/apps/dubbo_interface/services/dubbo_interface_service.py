import apps.common.func.InitDjango

from apps.common.func.CommonFunc import dbModelListToListDict
from apps.config.services.businessLineService import BusinessService
from apps.config.services.modulesService import ModulesService
from apps.config.services.sourceService import SourceService
from all_models.models import TbConfigUri
from apps.dubbo_common.services.UriServiceForDubbo import UriServiceForDubbo
from apps.config.services.http_confService import HttpConfService
from apps.common.config import commonWebConfig
from apps.common.func.CommonFunc import  *
from all_models_for_dubbo.models.B0001_dubbo_interface import *
from all_models_for_dubbo.models.B0002_dubbo_testcase import *
from all_models.models.A0002_config import TbConfigHttp,TbConfigService,TbConfigUri
import telnetlib
from apps.dubbo_testcase.services.dubbo_testcase_service import DubboTestcaseService
from apps.common.func.ValidataFunc import *

class DubboInterfaceService(object):
    @staticmethod
    def getInterfaceId():
        try:
            interfaceMaxId = Tb2DubboInterface.objects.latest('id').interfaceId
        except Exception as e:
            interfaceId = 'DUBBO_INTERFACE_1'
            return interfaceId
        splitData = interfaceMaxId.split('_')
        interfaceId = "%s_%s_%s" % (splitData[0],splitData[1],(int(splitData[2])+1))
        return interfaceId

    @staticmethod
    def addInterface(data,addBy):
        newDataDict = {}
        for k, v in data.items():
            newDataDict[k] = data[k]

        retB,retS = verifyPythonMode(newDataDict["varsPre"])
        if retB == False:
            return "准备中出现不允许的输入：%s" % retS
        retB, retS = verifyPythonMode(newDataDict["varsPost"])
        if retB == False:
            return "断言恢复中出现不允许的输入：%s" % retS

        newDataDict["addBy_id"] = addBy
        newDataDict["interfaceId"] = DubboInterfaceService.getInterfaceId()
        saveInterface = Tb2DubboInterface.objects.create(**newDataDict)
        return saveInterface

    @staticmethod
    def addBaseDataToDubboInterface(data,addBy,titlePre = ""):
        newDataDict = data
        if "varsPre" not in newDataDict.keys():
            newDataDict["varsPre"] = ""
        retB,retS = verifyPythonMode(newDataDict["varsPre"])
        if retB == False:
            return retB,"准备中出现不允许的输入：%s" % retS

        if "varsPost" not in newDataDict.keys():
            newDataDict["varsPost"] = ""
        retB, retS = verifyPythonMode(newDataDict["varsPost"])
        if retB == False:
            return retB,"断言恢复中出现不允许的输入：%s" % retS

        newDataDict["addBy_id"] = addBy
        newDataDict["interfaceId"] = DubboInterfaceService.getInterfaceId()

        if "title" not in newDataDict.keys():
            newDataDict["title"] = "%s:%s.%s" % (titlePre,newDataDict["dubboService"],newDataDict["dubboMethod"])
        if "casedesc" not in newDataDict.keys():
            newDataDict["casedesc"] = newDataDict["title"]
        saveInterface = Tb2DubboInterface.objects.create(**newDataDict)
        return True,saveInterface

    @staticmethod
    def getInterfaceById(id):
        return Tb2DubboInterface.objects.filter(id=id)[0]

    @staticmethod
    def getInterfaceByInterfaceId(interfaceId):
        return Tb2DubboInterface.objects.filter(interfaceId=interfaceId)[0]

    @staticmethod
    def getInterfaceByIdToDict(id):
        return dbModelToDict(Tb2DubboInterface.objects.filter(id=id)[0])

    @staticmethod
    def interfaceSaveEdit(interfaceData):
        retB,retS = verifyPythonMode(interfaceData['varsPre'])
        if retB == False:
            return "准备中出现不允许的输入：%s" % retS
        retB,retS = verifyPythonMode(interfaceData['varsPost'])
        if retB == False:
            return "断言恢复中出现不允许的输入：%s" % retS

        interfaceSaveEditResule = Tb2DubboInterface.objects.filter(id=interfaceData["id"]).update(**interfaceData)
        return interfaceSaveEditResule

    @staticmethod
    def delInterfaceById(id):
        return Tb2DubboInterface.objects.filter(id=id).update(state=0)

    @staticmethod
    def getDubboHostAndPort(env,system):
        tmpConfig = TbEnvUriConf.objects.filter(httpConfKey=env, uriKey=system)
        if tmpConfig:
            tmpConfig = tmpConfig[0].requestAddr
            addrList = tmpConfig.split(":")
            if len(addrList) == 2 and isInt(addrList[1].strip()):
                return addrList[0].strip(),addrList[1].strip()
        return "", 0

    @staticmethod
    def getAllServices(env,system):
        host,port = DubboInterfaceService.getDubboHostAndPort(env,system)
        return DubboInterfaceService.getServiceListAndDict(host,port)

    @staticmethod
    def getServiceListAndDict(host,port):
        serviceDict = {}  # methodList in it
        serviceList = []
        if host != "":
            #开始做telnet请求。
            msg = DubboInterfaceService.do_telnet(host,port,"ls")
            serviceStr = msg.replace("dubbo>","")
            serviceList = serviceStr.strip().split("\r\n")
            for tmpService in serviceList:
                serviceDict[tmpService] = DubboInterfaceService.getAllMethodsByService(host,port,tmpService)
        return serviceList,serviceDict

    @staticmethod
    def getAllMethods(env,system,service):
        serviceList = []
        host,port = DubboInterfaceService.getDubboHostAndPort(env,system)
        return DubboInterfaceService.getAllMethodsByService(host,port,service)

    @staticmethod
    def getAllMethodsByService(host,port,service):
        serviceList = []
        if host != "":
            #开始做telnet请求。
            msg = DubboInterfaceService.do_telnet(host,port,"ls %s" % service)
            serviceStr = msg.replace("dubbo>","")
            serviceList = serviceStr.strip().split("\r\n")
        return serviceList

    @staticmethod
    def getRecentParam(service,method,paramIndex):
        sql = "select DISTINCT(dubboParams) FROM ((select DISTINCT(dubboParams) from tb2_dubbo_quick_debug where dubboService='"+service+"' and dubboMethod='"+method+"' and dubboParams != '' and state=1 and actualResult NOT LIKE 'No such method %%' and actualResult NOT LIKE 'Invalid json argument,%%' ORDER BY id desc limit 10) " \
              "UNION " \
              "(select DISTINCT(dubboParams) from tb2_dubbo_interface where dubboService='"+service+"' and dubboMethod='"+method+"' and dubboParams != '' and state=1 ORDER BY id desc limit 10)) AS allParamTable"
        print(sql)
        res = executeSqlGetDict(sql)
        if res:
            if len(res) <= paramIndex:
                return res[paramIndex%len(res)]['dubboParams']
            else:
                return res[paramIndex]['dubboParams']
        return ""

    @staticmethod
    def addQuickDebugData(addr,service,method,param,actualmsg,taketime,addBy,encoding = "gb18030"):
        tb = Tb2DubboQuickDebug(requestAddr = addr,dubboService = service,dubboMethod = method,dubboParams = param,actualResult = actualmsg,executeTakeTime = taketime,addBy=addBy,encoding = encoding)
        tb.save(force_insert=True)
        return tb.id

    @staticmethod
    def getRecentQueryDebug(addBy):
        sql = "select * from tb2_dubbo_quick_debug where addBy='" + addBy + "' and actualResult NOT LIKE 'No such method %%' and actualResult NOT LIKE 'Invalid json argument,%%' ORDER BY id desc limit 1"
        return executeSqlGetDict(sql)

    @staticmethod
    def do_telnet( host, port, command, finish = b'dubbo>',encoding = "gb18030"):
            """执行telnet命令
            :param host:
            :param port:
            :param finish:
            :param command:
            :return:
            """
            # 连接Telnet服务器
            try:
                myOsEncoding = encoding
                tn=""
                logging.debug('do_telnet: command：%s ' % command)
                # logging.debug('do_telnet: command编码：%s ' % chardet.detect(command)['encoding'])
                is_conn_telnet = False
                logging.debug('do_telnet: telent init')
                logging.debug('do_telnet: telent host %s port %s' % (host,port))
                tn = telnetlib.Telnet(host, port, timeout=10)
                logging.debug('do_telnet:telent connected')
                tn.set_debuglevel(0)  # 设置debug输出级别  0位不输出，越高输出越多
                logging.debug('do_telnet:telent set debug level')
                # 输入回车
                tn.write(b'\r\n')
                logging.debug('do_telnet:telent enter')
                # 执行命令
                none_until = tn.read_until(finish).decode(myOsEncoding)
                logging.debug('do_telnet: telent enter return: %s' % none_until)
                if none_until.strip() == finish :
                    is_conn_telnet = True
                tn.write(b'%s\r\n' % command.encode(myOsEncoding))
                logging.debug('do_telnet:telent enter command: %s ' % command)
                # 执行完毕后，终止Telnet连接（或输入exit退出）
                return_msg_bytes = tn.read_until(finish)
                try:
                    return_msg =  return_msg_bytes.decode(myOsEncoding)
                except:
                    return_msg = str(return_msg_bytes)

                logging.debug('do_telnet: telent enter command after read_until')
                logging.debug('do_telnet: return_msg：%d ' % len(return_msg))
                return return_msg
            except Exception as e:
                logging.error(traceback.format_exc())
                if is_conn_telnet:
                    logging.info(u"DubboService.py: do_telnet: 请求参数错误等异常，导致请求返回异常。")
                    return "请求参数错误等异常，导致请求返回异常。"
                else:
                    logging.info( u"DubboService.py: do_telnet: Telnet请求时发生网络问题或者接口错误，请确认。")
                    return "TELNET_ERROR: Telnet请求时发生网络问题或者接口错误，请确认。"
            finally:
                if type(tn) != type(""): tn.close()

    @staticmethod
    def queryDubboConfSort(request):
        return executeSqlGetDict("SELECT  ch.httpConfKey,ch.alias  FROM tb_config_http ch LEFT JOIN (SELECT * FROM tb_user_httpconf WHERE addBy = %s ) uh on ch.httpConfKey = uh.httpConfKey WHERE ch.state = 1 AND ch.dubboRunState = 1  ORDER BY uh.conflevel is null,uh.conflevel asc , ch.modTime desc ",request.session.get("loginName"))

    @staticmethod
    def getInterfaceForInterfaceId(interfaceId):
        return Tb2DubboInterface.objects.filter(interfaceId=interfaceId, state=1)[0]

    @staticmethod
    def getInterfaceForId(id):
        return Tb2DubboInterface.objects.filter(id=id)[0]

    @staticmethod
    def syncDelTipList(interface):
        stepList = dbModelListToListDict(
            DubboTestcaseService.getSyncStepFromInterfaceIdNum(interface["interfaceId"]))
        testCaseList = []
        for index in range(0, len(stepList)):
            testCaseList.append(stepList[index]["caseId_id"])
        testCaseList = list(set(testCaseList))
        return {"list": testCaseList, "num": len(testCaseList)}

    @staticmethod
    def syncInterfaceToTestcaseStep(interface):
        stepList = dbModelListToListDict(
            DubboInterfaceService.getSyncStepFromInterfaceId(interface["interfaceId"]))
        for index in range(0, len(stepList)):
            stepList[index]["stepDesc"] = interface["casedesc"]
            stepList[index]["varsPre"] = interface["varsPre"]

            stepList[index]["dubboSystem"] = interface["dubboSystem"]
            stepList[index]["dubboService"] = interface["dubboService"]
            stepList[index]["dubboMethod"] = interface["dubboMethod"]
            stepList[index]["dubboParams"] = interface["dubboParams"]
            stepList[index]["encoding"] = interface["encoding"]

            stepList[index]["varsPost"] = interface["varsPost"]
            stepList[index]["timeout"] = interface["timeout"]
            stepList[index]["modBy"] = interface["modBy"]
            stepList[index]["modTime"] = datetime.datetime.now()
            stepList[index]["businessLineId_id"] = interface["businessLineId_id"]
            stepList[index]["moduleId_id"] = interface["moduleId_id"]
            DubboInterfaceService.updateTestCaseStep(stepList[index]["id"], stepList[index])

    @staticmethod
    def getSyncStepFromInterfaceId(interfaceId):
        return Tb2DubboTestcaseStep.objects.filter(fromInterfaceId=interfaceId).filter(isSync=1)

    @staticmethod
    def updateTestCaseStep(id,stepData):
        updateStep = Tb2DubboTestcaseStep.objects.filter(id=id).update(**stepData)
        return updateStep
