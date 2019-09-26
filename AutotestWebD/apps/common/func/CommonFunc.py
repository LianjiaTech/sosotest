import datetime, platform, json, logging, os, pymysql, traceback, ctypes, inspect, re,hashlib,socket,math
from apps.common.helper.ApiReturn import ApiReturn
from django.db import connection
import apps.common.func.InitDjango
from AutotestWebD.settings import *
from django.forms.models import model_to_dict
from apps.common.decorator.normal_functions import *
import random
from all_models.models import *
from collections import OrderedDict
from copy import deepcopy
import apps.myadmin.service.UserPermissionService
logger = logging.getLogger("django")


def isWindowsSystem():
    return 'Windows' in platform.system()

def isLinuxSystem():
    return 'Linux' in platform.system()

def isDictJson(myjson):
    try:
        myjson = myjson.strip()
        if myjson.startswith('{') and myjson.endswith('}'):
            json.loads(myjson)
            return True
        else:
            return False
    except Exception as e:
        return False

def isListJson(myjson):
    try:
        myjson = myjson.strip()
        if myjson.startswith('[') and myjson.endswith(']'):
            json.loads(myjson)
            return True
        else:
            return False
    except Exception as e:
        return False

def isJson(myjson):
    try:
        json.loads(myjson)
        return True
    except Exception as e:
        return False

def isInt(myint):
    try:
        int(myint)
        return True
    except Exception as e:
        return False

def get_sub_string(params,start,end):
    params = params
    find_start_tag = start
    find_end_tag = end
    if find_start_tag == "":
        spos = 0
    else:
        spos = params.find(find_start_tag)

    if spos == -1:  # 没有发现关键字 SQL_SELECT()
        return ''

    if find_end_tag == "":
        epos = len(params)
    else:
        epos = params.find(find_end_tag, spos+1)

    if epos == -1:  # 没有发现关键字 find_end_tag
        return ''

    return params[spos + len(find_start_tag):epos]

def get_current_time():
    #return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_current_time_YYYYMMDD():
    #return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    return datetime.datetime.now().strftime('%Y%m%d')

def get_current_time_YYYYMMDDHHMMSS():
    #return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

def splitStringToListByTag(varsString,splitTag = ";"):
    varsList = varsString.split(splitTag)
    removeIndexList = []
    ###对转义;分号进行处理！#########
    tmpInext = 0
    for i in range(0, len(varsList)):
        if i < tmpInext: continue
        iNext = i + 1
        if varsList[i].strip() == "":
            # removeIndexList.append(i)
            continue
        if varsList[i][-1:] == "\\":
            # 判断;分号是否被转义,左侧确定
            varsList[i] = varsList[i][:-1] + splitTag + varsList[i + 1]
            removeIndexList.append(varsList[i + 1])
            while iNext < len(varsList):
                if varsList[iNext][-1:] == "\\":
                    varsList[i] = varsList[i][:-1] + splitTag + varsList[iNext + 1]
                    removeIndexList.append(varsList[iNext + 1])
                    iNext += 1
                else:
                    break
        tmpInext = iNext
    for tvalue in removeIndexList:
        varsList.remove(tvalue)
    return  varsList

def transferListToStringByTag(varsList,splitTag = ";"):
    retString = ""
    for i in range(0,len(varsList)):
        retString = varsList[i].replace(";","\\;") + ";\n"
    return retString[:-1]

def replacedForIntoDB(str):
    return pymysql.escape_string(str)

def replacedForDictKey(str):
    return  str

def processJsonString(jsonString):
    jsonString = re.sub(r"(,?)(\w+?)\s+?:", r"\1'\2' :", jsonString)
    return jsonString.replace("'", "\"")

#停止线程
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        logging.debug("非法线程id！")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        logging.debug("PyThreadState_SetAsyncExc failed!")
#停止线程
def stop_thread(thread):
    while thread.isAlive():
        _async_raise(thread.ident, SystemExit)
        if thread.isAlive():
            time.sleep(1)

#md5字符串 小写
def md5lower(str):
    m = hashlib.md5()
    m.update(bytes(str,encoding="utf-8"))  # 参数必须是byte类型，否则报Unicode-objects must be encoded before hashing错误
    md5value = m.hexdigest()
    return md5value

@catch_exception
def send_tcp_request(reqstr):
    #链接服务端ip和端口
    logger.info("TCPHOST&PORT:%s:%s" %(TCP_HOST,TCP_PORT) )
    print(TCP_HOST,TCP_PORT)
    maxTryTimes = 10
    for i in range(0,maxTryTimes):
        ip_port = (TCP_HOST,TCP_PORT)
        try:
            #TCP发送
            #生成一个接口调试请求
            logger.info("开始创建tcp对象")
            sk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sk.settimeout(3)
            logger.info("创建成功")
            #请求连接服务端
            sk.connect(ip_port)
            logger.info("连接成功")
            #发送数据
            sk.sendall(bytes(reqstr,'utf8'))
            logger.info("发送成功")
            #接受数据
            server_reply = sk.recv(1024)
            logger.info("接收成功")
            #打印接受的数据
            if str(server_reply,'utf8') == "ok":
                logger.info("@@@@tcp发送ok：%s" % reqstr)
                return ApiReturn(ApiReturn.CODE_OK,str(server_reply,'utf8'))
            else:
                logger.warning("@@@@tcp发送ERROR：%s == %s" % (reqstr, str(server_reply,'utf8')))
                return ApiReturn(ApiReturn.CODE_TCP_RETURN_NOT_OK,str(server_reply,'utf8'))
        except Exception as e:
            logger.error("第%d次尝试发送tcp消息\n%s\n到%s:%s发生异常。异常信息：\n%s"% ((i+1),reqstr,TCP_HOST,TCP_PORT,traceback.format_exc()))
            ransleepint = random.randint(500,5000)
            logger.info("休息%s秒后重试" % (float(ransleepint)/1000.0))
            time.sleep(float(ransleepint)/1000.0)
            if i == maxTryTimes - 1:
                return ApiReturn(ApiReturn.CODE_TCP_EXCEPTION,"尝试%d次发送tcp消息\n%s\n到Server发生异常。异常信息：\n%s" % (maxTryTimes,reqstr,str(e)))
        finally:
            #关闭连接
            if sk:
                sk.close()

@catch_exception
def send_tcp_request_to_uiport(reqstr):
    #链接服务端ip和端口
    logging.debug("TCPHOST&UIPORT:%s:%s" %(TCP_HOST,TCP_UIPORT) )
    maxTryTimes = 3
    for i in range(0,maxTryTimes):
        ip_port = (TCP_HOST,TCP_UIPORT)
        try:
            #TCP发送
            #生成一个接口调试请求
            sk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            #请求连接服务端
            sk.connect(ip_port)
            #发送数据
            sk.sendall(bytes(reqstr,'utf8'))
            #接受数据
            server_reply = sk.recv(1024)
            #打印接受的数据
            if str(server_reply,'utf8') == "ok":
                return ApiReturn(ApiReturn.CODE_OK,str(server_reply,'utf8'))
            else:
                return ApiReturn(ApiReturn.CODE_TCP_RETURN_NOT_OK,str(server_reply,'utf8'))
        except Exception as e:
            logging.error("第%d次尝试发送tcp消息\n%s\n到Server发生异常。异常信息：\n%s"% ((i+1),reqstr,traceback.format_exc()))
            ransleepint = random.randint(500,5000)
            time.sleep(float(ransleepint)/1000.0)
            if i == maxTryTimes - 1:
                return ApiReturn(ApiReturn.CODE_TCP_EXCEPTION,"尝试%d次发送tcp消息\n%s\n到Server发生异常。异常信息：\n%s" % (maxTryTimes,reqstr,str(e)))
        finally:
            #关闭连接
            if sk:
                sk.close()

def dbModelToDict(dbModel):
    resDict = {}
    # resDict = OrderedDict()
    resDict.update(dbModel.__dict__)
    resDict.pop("_state", None)  # 去除掉多余的字段
    for k, v in resDict.items():
        if type(v) == type(datetime.datetime(1984, 1, 2)):
            # 如果是datetime类型的，无法转换为json，要先转换为字符串
            resDict[k] = str(v).split(".")[0]
    return resDict

def djangoModelToDict(dbModel):
    resDict = {}
    resDict.update(model_to_dict(dbModel))
    for k, v in resDict.items():
        if type(v) == type(datetime.datetime(1984, 1, 2)):
            # 如果是datetime类型的，无法转换为json，要先转换为字符串
            resDict[k] = str(v)
    return resDict


#通过执行sql语句返回一个dict
def executeSqlGetDict(sqlStr,attrList=[]):
    cursor = connection.cursor()
    cursor.execute(sqlStr, attrList)
    allData = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    result = []
    for row in allData:
        objDict = {}
        # 把每一行的数据遍历出来放到Dict中
        for i in range(0,len(col_names)):
            if type(row[i]) == datetime.datetime:
                objDict[col_names[i]] = str(row[i]).split(".")[0]
                continue
            objDict[col_names[i]] = row[i]
        result.append(objDict)
    return result


def get_select_sql_count(sql_str, attr_list=[]):
    cursor = connection.cursor()
    cursor.execute(sql_str, attr_list)
    return cursor.rowcount

#用来分页的函数
def pagination(sqlStr="",attrList=[],page=1,pageNum=1,request=None, whether_groupby=False):
    if whether_groupby:
        countTotalNum = get_select_sql_count(sqlStr, attrList)
    else:
        #获取总得data列表
        pattern = re.compile(r'^select\s(.*?)\sfrom\s', re.IGNORECASE)
        countSqlStr = re.sub(pattern, 'select count(*) from ', sqlStr)
        execData = executeSqlGetDict(countSqlStr, attrList)
        if not execData:
            return {"pageDatas": [], "pageCountList": range(0, 0), "page": page, "pageCount": 0}
        countTotalNum = execData[0]['count(*)']
    sqlStr += "  LIMIT %s,%s "
    pageCount = math.ceil(countTotalNum / pageNum)

    if pageNum == 0:
        attrList.append(0)
        attrList.append(countTotalNum)
    else:
        if pageCount == 0:
            page = 1
        elif pageCount < page:
            page = pageCount
        attrList.append(int(page) * pageNum - pageNum)
        attrList.append(pageNum)

    #获取分页查出的data列表
    pageData = executeSqlGetDict(sqlStr,attrList)
    if (countTotalNum == 0):
        return {"pageDatas": [], "pageCountList": range(0,0), "page": page, "pageCount": pageCount}

    pageCountList = range(1, pageCount + 1)
    if request:
        for index in pageData:
            permissionList = apps.myadmin.service.UserPermissionService.UserPermissionService.get_user_url_permissions(request.path,request.session.get("loginName"),[index["addBy"]])
            print(permissionList)
            if permissionList["isSuccess"]:
                index["permissions"] = permissionList["permissions"][index["addBy"]]
            else:
                index["permissions"] = []
    return {"pageDatas":pageData,"pageCountList":pageCountList,"page":page,"pageCount":pageCount,"totalDataCount":countTotalNum}

def isSqlInjectable(str):
    if "union" in str.lower():
        return True
    else:
        return False

def dbModelListToListDict(modelList):
    retList = []
    for model in modelList:
        retList.append(dbModelToDict(model))
    return retList

def tupleToDict(tuple,keyList):
    retList = []

    for t in range(0,len(tuple)):
        retList.append({})
        for i in range(len(tuple[t])):
            retList[t][keyList[i]] = tuple[t][i]
    return retList


def substr(string,start,end):
    string = string[string.find(start):]
    return string[string.find(start)+len(start):string.find(end)]

# def uploadFileSave(loginName,fileDict):
#     try:
#         filedir = "%s/uploads/%s" % (BASE_DIR.replace("\\","/"),loginName)
#         if not os.path.exists(filedir):
#             os.makedirs(filedir)
#         filedirNameList = []
#          # 打开特定的文件进行二进制的写操作
#
#         for k,v in fileDict.items():
#             tmpFileList = fileDict.getlist(k)
#             tmpFileFlag = 0
#             for tmpFileObj in tmpFileList:
#                 tmpFileDict = {}
#                 tmpFileDict['key'] = k
#                 tmpFileDict['type'] = "file"
#                 tmpFileDict["value"] = {}
#                 tmpFileDict["value"]["filename"] = tmpFileObj.name
#                 tmpFileDict["value"]["fileType"] = tmpFileObj.content_type
#                 tmpFileDict["value"]["size"] = tmpFileObj.size
#                 tmpFileDict["value"]["charset"] = tmpFileObj.charset
#                 realPath = "%s/%s_%s_%s" % (filedir,get_current_time_YYYYMMDDHHMMSS(),tmpFileFlag,tmpFileObj.name)
#                 tmpFileDict["value"]["realPath"] = realPath
#                 destination = open(os.path.join(realPath), "wb+")
#                 tmpFileFlag += 1
#                 for chunk in tmpFileObj.chunks():
#                     destination.write(chunk)
#                 destination.close()
#                 filedirNameList.append(tmpFileDict)
#         print(filedirNameList)
#         return filedirNameList
#     except Exception as e:
#         pass
def updateFileSave(loginName,file,flag):
    fileName = file.name
    filedir = "%s/%s" % (uploadsRoot.replace("\\", "/"), loginName)
    if not os.path.exists(filedir):
        os.makedirs(filedir)
    realPath = "%s/%s_%s_%s" % (filedir, get_current_time_YYYYMMDDHHMMSS(),flag,fileName)
    # if file.name.lower().endswith('.csv'):
    destination = open(os.path.join(realPath), "wb+")
    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()
        # file_data = ""
        # try:
        #     tmpfile = deepcopy(file)
        #     file_data = tmpfile.read().decode('utf-8').splitlines()
        # except Exception:
        #     try:
        #         file_data = file.read().decode("ANSI").encode(encoding='utf-8').decode('utf-8').splitlines()
        #     except Exception:
        #         file_data = ""
        # import csv
        # data = csv.DictReader(file_data)
        # head = csv.DictReader(file_data).fieldnames
        #
        # tmplist = []
        # for index in data:
        #     tmpDict = {}
        #     for fieldIndex in head:
        #         tmpDict[fieldIndex] = index[fieldIndex]
        #     tmplist.append(tmpDict)
        #
        # with open(realPath, 'w', newline='') as csvfile:
        #     print(head)
        #     writer = csv.DictWriter(csvfile, fieldnames=head)
        #     writer.writeheader()
        #     for index in tmplist:
        #         print(index)
        #         writer.writerow(index)
        # print(realPath)
    # else:
    #     destination = open(os.path.join(realPath), "wb+")
    #     for chunk in file.chunks():
    #         destination.write(chunk)
    #     destination.close()
    return realPath

def dict2list(dic:dict):
    ''' 将字典转化为列表 '''
    keys = dic.keys()
    vals = dic.values()
    lst = [(key, val) for key, val in zip(keys, vals)]
    return lst

def dictToJson(dic):
    ret = {}
    for k,v in dic.items():
        if type(v) == type(b""):
            ret[k] = str(v, encoding="utf-8")
        elif type(v) == type(datetime.datetime.now()):
            ret[k] = v.strftime('%Y-%m-%d %H:%M:%S')
        elif k == "_addBy_cache":
            ret[k] = ""
        else:
            ret[k] = v
    return json.dumps(ret,ensure_ascii=False)


def userChangeLogTestCaseToTestCaseChange(request,oldTestCaseData,newTestCaseData):
    userChangeLog = TbUserChangeLog()
    userChangeLog.loginName = request.session.get("loginName")
    userChangeLog.otherLoginName = oldTestCaseData["addBy_id"]
    userChangeLog.changeDataId = oldTestCaseData["caseId"]
    userChangeLog.dataId = oldTestCaseData["caseId"]
    userChangeLog.beforeChangeData = dictToJson(oldTestCaseData)
    userChangeLog.afterChangeData = dictToJson(newTestCaseData)
    userChangeLog.type = 1
    try:
        userChangeLog.version = request.session.get("version") == "CurrentVersion" and TbVersion.objects.get(type=2).versionName or request.session.get("version")
    except:
        userChangeLog.version = request.session.get("version")
    userChangeLog.save()

def userChangeLogTestCaseStepToTestCaseChangeStep(request,oldTestCaseStepData,newTestCaseStepData):
    userChangeLog = TbUserChangeLog()
    userChangeLog.loginName = request.session.get("loginName")
    userChangeLog.otherLoginName = oldTestCaseStepData["addBy_id"]
    userChangeLog.changeDataId = "caseId_id" in oldTestCaseStepData and oldTestCaseStepData["caseId_id"] or oldTestCaseStepData["caseId"]
    userChangeLog.dataId = "caseId_id" in oldTestCaseStepData and oldTestCaseStepData["caseId_id"] or oldTestCaseStepData["caseId"]
    userChangeLog.beforeChangeData = dictToJson(oldTestCaseStepData)
    userChangeLog.afterChangeData = dictToJson(newTestCaseStepData)
    userChangeLog.testStepId = oldTestCaseStepData["stepNum"]
    userChangeLog.type = 1
    try:
        userChangeLog.version = request.session.get("version") == "CurrentVersion" and TbVersion.objects.get(type=2).versionName or request.session.get("version")
    except:
        userChangeLog.version = request.session.get("version")
    userChangeLog.save()

def userChangeLogInterfaceToTestCaseStepChange(request,interface,testCaseStep):
    changeLog = TbUserChangeLog()
    try:
        changeLog.version = request.session.get("version") == "CurrentVersion" and TbVersion.objects.get(type=2).versionName or request.session.get("version")
    except:
        changeLog.version = request.session.get("version")
    changeLog.loginName = request.session.get("loginName")
    changeLog.otherLoginName = testCaseStep["addBy_id"]
    changeLog.type = 1
    changeLog.beforeChangeData = dictToJson(testCaseStep)
    changeLog.afterChangeData = dictToJson(interface)
    changeLog.dataId = interface["interfaceId"]
    changeLog.changeDataId = testCaseStep["caseId_id"]
    changeLog.testStepId = testCaseStep["stepNum"]
    changeLog.save()

def userChangeLogTestCaseDel(request,testCase):
    changeLog = TbUserChangeLog()
    try:
        changeLog.version = request.session.get("version") == "CurrentVersion" and TbVersion.objects.get(type=2).versionName or request.session.get("version")
    except:
        changeLog.version = request.session.get("version")
    changeLog.loginName = request.session.get("loginName")
    changeLog.otherLoginName = testCase["addBy_id"]
    changeLog.type = 0
    changeLog.beforeChangeData = dictToJson(testCase)
    changeLog.dataId = testCase["caseId"]
    changeLog.save()

def userChangeLogTestCaseStepDel(request,testCaseStep):
    changeLog = TbUserChangeLog()
    try:
        changeLog.version = request.session.get("version") == "CurrentVersion" and TbVersion.objects.get(
            type=2).versionName or request.session.get("version")
    except:
        changeLog.version = request.session.get("version")
    changeLog.loginName = request.session.get("loginName")
    changeLog.otherLoginName = testCaseStep["addBy_id"]
    changeLog.type = 0
    changeLog.beforeChangeData = dictToJson(testCaseStep)
    changeLog.dataId = testCaseStep["caseId_id"]
    changeLog.testStepId = testCaseStep["stepNum"]
    changeLog.save()

def is_chinese(s):
    rt = False
    if s>= u"\u4e00" and s<= u"\u9fa6":
        rt = True
    return rt

def isContainCN(checkStr):
    isContailCn = False
    for tmpChar in checkStr:
        if is_chinese(tmpChar):
            isContailCn = True
            break
    return isContailCn


def is_requests_Response(objData):
    if type(requests.models.Response()) == type(objData):
        return True
    else:
        return False

def is_str(objData):
    if type("") == type(objData):
        return True
    else:
        return False

def getRespTextByResponse(response):
    try:
        assertText = ""
        if is_str(response):
            assertText = assertText + response
        elif is_requests_Response(response):
            #得到编码,如果在list中，直接转义。如果不在list中，尝试各个编码。
            if response.encoding == None or response.encoding.upper() == "ISO-8859-1":
                #没有发现编码或者编码是ISO-8859-1，开始猜测编码,默认设置编码 UTF8,其他情况不改变编码
                response.encoding = "UTF-8"
            try:
                if response.content == None:
                    assertText = ""
                else:
                    #尝试使用encoding解码，如果成功就继续，不成功，循环使用支持的charset尝试。
                    assertText = response.content.decode(response.encoding)#str(response.content, encoding=response.encoding)
            except Exception as e:
                isGetStr = False
                support_charset_list = "UTF8,UTF-8,GBK,GB2312".split(",")
                for tmpEncode in support_charset_list:
                    try:
                        assertText = response.content.decode(tmpEncode)
                        isGetStr = True
                    except Exception as e:
                        continue
                if isGetStr == False:
                    #都没有解码成功，那么强制byte到str。
                    assertText = str(response.content)
                    file_max_show_len = 4000
                    if len(assertText) > file_max_show_len:
                        #文件下载超过最大长度不显示
                        assertText = assertText[0:file_max_show_len] + "\n...剩余部分不显示..."
                    assertText = "[====文件下载====]\n"+assertText
        else:
            assertText = "[response类型[%s]错误]" % type(response)
    except UnicodeDecodeError as ueUtf8:
        assertText = "[====文件下载====]"
    except Exception as e:
        assertText = "[未发现HTTP响应体]"
        if is_str(response):
            assertText = assertText + response
    finally:

        return assertText


if __name__ == '__main__':
    # taskExecuteId = "12"
    # tcpStr = '{"do":3,"TaskExecuteId":%s}' % taskExecuteId
    # print(send_tcp_request(tcpStr).toJson())
    # sqlStr="""SElECT * from tb_http_interface i LEFT JOIN tb_user u ON i.addBy = u.loginName WHERE 1=1 and i.state=1 and (i.addBy LIKE %s or u.userName LIKE %s) ORDER BY i.modTime desc , i.id desc"""
    # attrList=['%李亚超%', '%李亚超%']
    # orderBySql="""  """
    # page=1
    # pageNum=2
    # pagination(sqlStr,attrList,page,pageNum)

    # print(substr("[CONF=common]pageNo = 1;&para;[ENDCONF][CONF=serviceDev_75]pageNo = 1;[ENDCONF][CONF=serviceTest_78]pageNo = 1;[ENDCONF]","[CONF=serviceTest_78]","[ENDCONF]"))
    pass