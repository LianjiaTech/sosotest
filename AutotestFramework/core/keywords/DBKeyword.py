from core.const.GlobalConst import ResultConst
from core.decorator.normal_functions import keyword,catch_exception
from core.keywords.ALL_FUNC import *
import decimal

@keyword()
@catch_exception
def DB_SELECT(value,context,strTobeProcessed = ""):
    strTobeProcessed = core.processor.KP.KP.getProcessedValue(strTobeProcessed, context)
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字DB_SELECT执行时解析参数列表返回错误。返回参数列表为%s" % str(strTobeProcessed)
        context.assertResult = "%s\n%s" % (retMsg,context.assertResult)
        return retMsg
    #如果是更新或者删除或者插入操作，提示错误
    if strTobeProcessed.strip().lower().startswith("update ") or strTobeProcessed.strip().lower().startswith("delete ") or strTobeProcessed.strip().lower().startswith("insert "):
        context.setERROR("<ERROR:只能使用SELECT语句>")
        return "<ERROR:只能使用SELECT语句>"

    if "delete " in strTobeProcessed.strip().lower() or "update " in strTobeProcessed.strip().lower() or "insert " in strTobeProcessed.strip().lower() :
        context.setERROR("<ERROR:不能包含UPDATE/DELETE/INSERT操作！>")
        return "<ERROR:不能包含UPDATE/DELETE/INSERT操作！>"

    if "where " not in strTobeProcessed.strip().lower():
        context.setERROR("<ERROR:必须包含where子句！>")
        return "<ERROR:必须包含where子句！>"

    if strTobeProcessed.strip().lower().startswith("select "):
        dbKey = "default"
        execSql = strTobeProcessed.strip()

    else:
        # 使用新的sqlselect，可以调用不同系统的
        firstDouhaoPos = strTobeProcessed.strip().find(",")
        if firstDouhaoPos > 0:
            dbKey = strTobeProcessed.strip()[:firstDouhaoPos].strip()
            execSql = strTobeProcessed.strip()[firstDouhaoPos+1:].strip()
        else:
            context.setERROR("<ERROR:错误的DB_SELECT使用方法！>")
            return "<ERROR:错误的DB_SELECT使用方法！>"

    if dbKey in context.serviceDBDict.keys():
        db = context.serviceDBDict[dbKey]
    else:
        context.setERROR("<ERROR:没有找到数据库%s的配置>" % dbKey)
        return "<ERROR:没有找到数据库%s的配置>" % dbKey


    # paramList = splitStringToListByTag(strTobeProcessed, splitTag)
    sqlstring = core.processor.CP.CP.getProcessedValue(execSql, context)
    if db.connect() == False:
        context.setEXCEPTION("service数据库连接异常！%s" % db.errMsg)
        return "<ERROR:service[%s]数据库连接异常>" % dbKey
    db.setCursorDict(True)


    #判断影响行数
    if db.get_effected_rows_count(sqlstring.strip()) > 100:
        db.release()
        context.setERROR("<ERROR:DB_SELECT查询数据不得超过100行，请检查where子句！>")
        return "<ERROR:DB_SELECT查询数据不得超过100行，请检查where子句！>"

    res = db.execute_sql(sqlstring.strip())
    db.release()
    retList = []
    if isinstance(res,bool) and res == False:
        #check是否加了dbname.tablename
        fromTable =  get_sub_string(sqlstring.strip().lower(),"from "," where").strip()
        if fromTable and "." not in fromTable:
            context.setERROR("<ERROR:sql语句中的表名%s格式必须是database.table>" % fromTable)
            return "<ERROR:sql语句中的表名%s格式必须是database.table>" % fromTable
        else:
            context.setERROR("<ERROR:执行sql发生异常，请检查sql语句:%s>" % sqlstring.strip())
            return "<ERROR:执行sql发生异常，请检查sql语句:%s>" % sqlstring.strip()

    for tmpObj in res:
        tmpDict = {}
        for tmpK,tmpV in tmpObj.items():
            if isinstance(tmpV, datetime.datetime) or isinstance(tmpV, datetime.date):
                # 如果是datetime类型的，无法转换为json，要先转换为字符串
                tmpDict[tmpK] = str(tmpV)
            elif isinstance(tmpV,decimal.Decimal):
                tmpDict[tmpK] = str(decimal.Decimal(tmpV))
            else:
                tmpDict[tmpK] = tmpV
        retList.append(tmpDict)
    return json.dumps(retList)

@keyword()
@catch_exception
def DB_UPDATE(value,context,strTobeProcessed = ""):
    strTobeProcessed = core.processor.KP.KP.getProcessedValue(strTobeProcessed, context)
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字SQL_UPDATE执行时解析参数列表返回错误。返回参数列表为%s" % str(strTobeProcessed)
        context.assertResult = "%s\n%s" % (retMsg,context.assertResult)
        return retMsg

    #如果是更新或者删除或者插入操作，提示错误
    if strTobeProcessed.strip().lower().startswith("select ") or strTobeProcessed.strip().lower().startswith("delete ") or strTobeProcessed.strip().lower().startswith("insert "):
        return "<ERROR:只能使用UPDATE语句>"

    if "delete " in strTobeProcessed.strip().lower() or "insert " in strTobeProcessed.strip().lower():
        return "<ERROR:不能包含DELETE/INSERT操作！>"

    if "where " not in strTobeProcessed.strip().lower():
        return "<ERROR:必须包含where子句！>"

    if strTobeProcessed.strip().lower().startswith("update "):
        dbKey = "default"
        execSql = strTobeProcessed.strip()

    else:
        # 使用新的sqlselect，可以调用不同系统的
        firstDouhaoPos = strTobeProcessed.strip().find(",")
        if firstDouhaoPos > 0:
            dbKey = strTobeProcessed.strip()[:firstDouhaoPos].strip()
            execSql = strTobeProcessed.strip()[firstDouhaoPos+1:].strip()
        else:
            return "<ERROR:错误的DB_UPDATE使用方法>"

    if dbKey in context.serviceDBDict.keys():
        db = context.serviceDBDict[dbKey]
    else:
        return "<ERROR:没有找到数据库%s的配置>" % dbKey

    # paramList = splitStringToListByTag(strTobeProcessed, splitTag)
    sqlstring = core.processor.CP.CP.getProcessedValue(execSql, context)
    if db.connect() == False:
        context.setEXCEPTION("service数据库连接异常！%s" % db.errMsg)
        return "<ERROR:service[%s]数据库连接异常>" % dbKey
    db.setCursorDict(True)

    #判断影响行数
    if db.get_effected_rows_count(sqlstring.strip()) > 100:
        db.release()
        return "<ERROR:DB_UPDATE一次更新数据不得超过100行，请检查where子句。>"

    res = db.execute_update_sql(sqlstring.strip())
    db.release()
    if isinstance(res,bool) and res == False:
        #check是否加了dbname.tablename
        fromTable =  get_sub_string(sqlstring.strip().lower(),"update "," set").strip()
        if fromTable and "." not in fromTable:
            context.setERROR("<ERROR:sql语句中的表名%s格式必须是database.table>" % fromTable)
            return "<ERROR:sql语句中的表名%s格式必须是database.table>" % fromTable
        else:
            context.setERROR("<ERROR:执行sql发生异常，请检查sql语句:%s>" % sqlstring.strip())
            return "<ERROR:执行sql发生异常，请检查sql语句:%s>" % sqlstring.strip()
    else:
        return str(res)

@keyword()
@catch_exception
def DB_DELETE(value,context,strTobeProcessed = ""):

    strTobeProcessed = core.processor.KP.KP.getProcessedValue(strTobeProcessed, context)
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字SQL_DELETE执行时解析参数列表返回错误。返回参数列表为%s" % str(strTobeProcessed)
        context.assertResult = "%s\n%s" % (retMsg,context.assertResult)
        return retMsg

    #如果是更新或者删除或者插入操作，提示错误
    if strTobeProcessed.strip().lower().startswith("select ") or strTobeProcessed.strip().lower().startswith("update ") or strTobeProcessed.strip().lower().startswith("insert "):
        return "<ERROR:只能使用DELETE语句>"

    if "update " in strTobeProcessed.strip().lower() or "insert " in strTobeProcessed.strip().lower():
        return "<ERROR:不能包含UPDATE/INSERT操作！>"

    if " where " not in strTobeProcessed.strip().lower():
        return "<ERROR:必须包含where子句！>"

    if strTobeProcessed.strip().lower().startswith("delete "):
        dbKey = "default"
        execSql = strTobeProcessed.strip()

    else:
        # 使用新的sqlselect，可以调用不同系统的
        firstDouhaoPos = strTobeProcessed.strip().find(",")
        if firstDouhaoPos > 0:
            dbKey = strTobeProcessed.strip()[:firstDouhaoPos].strip()
            execSql = strTobeProcessed.strip()[firstDouhaoPos+1:].strip()
        else:
            return "<ERROR:错误的DB_DELETE使用方法>"

    if dbKey in context.serviceDBDict.keys():
        db = context.serviceDBDict[dbKey]
    else:
        return "<ERROR:没有找到数据库%s的配置>" % dbKey

    # paramList = splitStringToListByTag(strTobeProcessed, splitTag)

    sqlstring = core.processor.CP.CP.getProcessedValue(execSql, context)
    if db.connect() == False:
        context.setEXCEPTION("service数据库连接异常！%s" % db.errMsg)
        return "<ERROR:service[%s]数据库连接异常>" % dbKey
    db.setCursorDict(True)

    #判断影响行数
    if db.get_effected_rows_count(sqlstring.strip()) > 100:
        db.release()
        return "<ERROR:DB_DELETE一次删除数据不得超过100行，请检查where子句。>"

    res = db.execute_update_sql(sqlstring.strip())
    db.release()

    if isinstance(res,bool) and res == False:
        # check是否加了dbname.tablename
        fromTable = get_sub_string(sqlstring.strip().lower(), "from ", " where").strip()
        if fromTable and "." not in fromTable:
            context.setERROR("<ERROR:sql语句中的表名%s格式必须是database.table>" % fromTable)
            return "<ERROR:sql语句中的表名%s格式必须是database.table>" % fromTable
        else:
            context.setERROR("<ERROR:执行sql发生异常，请检查sql语句:%s>" % sqlstring.strip())
            return "<ERROR:执行sql发生异常，请检查sql语句:%s>" % sqlstring.strip()

    else:
        return str(res)

@keyword()
@catch_exception
def DB_INSERT(value,context,strTobeProcessed = ""):
    strTobeProcessed = core.processor.KP.KP.getProcessedValue(strTobeProcessed, context)
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字DB_INSERT执行时解析参数列表返回错误。返回参数列表为%s" % str(strTobeProcessed)
        context.assertResult = "%s\n%s" % (retMsg,context.assertResult)
        return retMsg

    #如果是更新或者删除或者插入操作，提示错误
    if strTobeProcessed.strip().lower().startswith("select ") or strTobeProcessed.strip().lower().startswith("update ") or strTobeProcessed.strip().lower().startswith("delete "):
        return "<ERROR:只能使用INSERT语句>"

    if "update " in strTobeProcessed.strip().lower() or "delete " in strTobeProcessed.strip().lower():
        return "<ERROR:不能包含UPDATE/DELETE操作！>"

    if strTobeProcessed.strip().lower().startswith("insert "):
        dbKey = "default"
        execSql = strTobeProcessed.strip()

    else:
        # 使用新的sqlselect，可以调用不同系统的
        firstDouhaoPos = strTobeProcessed.strip().find(",")
        if firstDouhaoPos > 0:
            dbKey = strTobeProcessed.strip()[:firstDouhaoPos].strip()
            execSql = strTobeProcessed.strip()[firstDouhaoPos+1:].strip()
        else:
            return "<ERROR:错误的DB_INSERT使用方法>"

    if dbKey in context.serviceDBDict.keys():
        db = context.serviceDBDict[dbKey]
    else:
        return "<ERROR:没有找到数据库%s的配置>" % dbKey


    # paramList = splitStringToListByTag(strTobeProcessed, splitTag)
    sqlstring = core.processor.CP.CP.getProcessedValue(execSql, context)
    if db.connect() == False:
        context.setEXCEPTION("service数据库连接异常！%s" % db.errMsg)
        return "<ERROR:service[%s]数据库连接异常>" % dbKey
    db.setCursorDict(True)
    res = db.execute_update_sql(sqlstring.strip())
    db.release()
    if isinstance(res,bool) and res == False:
        # check是否加了dbname.tablename
        fromTable = get_sub_string(sqlstring.strip().lower(), "insert into ", "(").strip()
        if fromTable and "." not in fromTable:
            context.setERROR("<ERROR:sql语句中的表名%s格式必须是database.table>" % fromTable)
            return "<ERROR:sql语句中的表名%s格式必须是database.table>" % fromTable
        else:
            context.setERROR("<ERROR:执行sql发生异常，请检查sql语句:%s>" % sqlstring.strip())
            return "<ERROR:执行sql发生异常，请检查sql语句:%s>" % sqlstring.strip()

    else:
        return str(res)

@keyword()
@catch_exception
def REDIS_SET(value,context,strTobeProcessed = ""):
    """
    REDIS_SET(key,value,timeout=None,db=0,service=mls-biz-support)
    :param key: 必须的
    :param value: 必须的
    :param timeout: 可选的，超时时间，没有就是None
    :param db: 可选的，0-15 默认是0
    :param system: 可选的，默认是Default
    :return:
    """
    paramList,paramDict = getParamListAndKWParam(strTobeProcessed, context)
    # 如果获取参数等导致错误，不继续执行登录返回错误原因。
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字REDIS_SET执行时解析参数列表返回错误。返回参数列表为%s" % str(paramList)
        context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
        return retMsg

    key,value,db,dbKey,timeout = "","",0,"default",None
    redisHand = None
    if len(paramList) < 2:
        retMsg = "CASE_ERROR:关键字REDIS_SET调用时参数不能小于2个。"
        context.setERROR(retMsg)
        return retMsg
    if len(paramList) > 5:
        retMsg = "CASE_ERROR:关键字REDIS_SET调用时参数不能大于5个。"
        context.setERROR( retMsg)
        return retMsg

    key = paramList[0].strip()
    value = paramList[1].strip()

    timeoutBase = "None"
    if len(paramList) >= 3:
        timeoutBase = paramList[2].strip()
    if "timeout" in paramDict.keys():
        timeoutBase = paramDict["timeout"]

    if timeoutBase == "None" or timeoutBase == "0" or timeoutBase == "":
        timeout = None
    elif isInt(timeoutBase) and int(timeoutBase) > 0 :
        timeout = int(timeoutBase)
    else:
        retMsg = "CASE_ERROR:关键字REDIS_SET调用时参数3[timeout]必须是大于0的整数或者是None。"
        context.setERROR( retMsg)
        return retMsg

    dbBase = "0"
    if len(paramList) >= 4:
        dbBase = paramList[3].strip()
    if "db" in paramDict.keys():
        dbBase = paramDict["db"]

    if isInt(dbBase) and int(dbBase) >= 0 :
        db = int(dbBase)
    else:
        retMsg = "CASE_ERROR:关键字REDIS_SET调用时参数4[db]必须是大于等于0的整数。"
        context.setERROR( retMsg)
        return retMsg

    if len(paramList) == 5:
        dbKey = paramList[4].strip()
    if "service" in paramDict.keys():
        dbKey = paramDict["service"].strip()

    if dbKey in context.serviceRedisDict.keys():
        redisHand = context.serviceRedisDict[dbKey]
        redisHand.db = db
        try:
            redisHand.connect()
            setres = redisHand.set_data(key,value,timeout)
            if setres == True:
                return "REDIS设置成功！[%s]" % setres
            else:
                retMsg = "CASE_ERROR:关键字REDIS_SET设置失败。原因[%s]" % str(setres)
                context.setERROR(retMsg)
                return retMsg
        except:
            retMsg = "CASE_ERROR:关键字REDIS_SET调用时Redis数据库%s连接失败>" % dbKey
            context.setERROR( retMsg)
            return retMsg
    else:
        retMsg = "CASE_ERROR:关键字REDIS_SET调用时没有找到Redis数据库%s的配置>" % dbKey
        context.setERROR( retMsg)
        return retMsg

@keyword()
@catch_exception
def REDIS_GET(value,context,strTobeProcessed = ""):
    """
    REDIS_SET(key,db=0,service=mls-biz-support)
    :param key: 必须的
    :param db: 可选的，0-15 默认是0
    :param system: 可选的，默认是Default
    :return:
    """
    paramList,paramDict = getParamListAndKWParam(strTobeProcessed, context)
    # 如果获取参数等导致错误，不继续执行登录返回错误原因。
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字REDIS_GET执行时解析参数列表返回错误。返回参数列表为%s" % str(paramList)
        context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
        return retMsg

    key,value,db,dbKey,timeout = "","",0,"default",None
    redisHand = None
    if len(paramList) < 1:
        retMsg = "CASE_ERROR:关键字REDIS_GET调用时参数不能小于1个。"
        context.setERROR(retMsg)
        return retMsg
    if len(paramList) > 3:
        retMsg = "CASE_ERROR:关键字REDIS_GET调用时参数不能大于3个。"
        context.setERROR( retMsg)
        return retMsg

    key = paramList[0].strip()

    dbBase = "0"
    if len(paramList) >= 2:
        dbBase = paramList[1].strip()
    if "db" in paramDict.keys():
        dbBase = paramDict["db"]

    if isInt(dbBase) and int(dbBase) >= 0 :
        db = int(dbBase)
    else:
        retMsg = "CASE_ERROR:关键字REDIS_GET调用时参数2[db]必须是大于等于0的整数。"
        context.setERROR( retMsg)
        return retMsg

    if len(paramList) == 3:
        dbKey = paramList[2].strip()
    if "service" in paramDict.keys():
        dbKey = paramDict["service"].strip()

    if dbKey in context.serviceRedisDict.keys():
        redisHand = context.serviceRedisDict[dbKey]
        redisHand.db = db
        try:
            redisHand.connect()
            try:
                retV = redisHand.get_data_for_data_keyword(key)
                return retV
            except:
                retMsg = "CASE_ERROR:关键字REDIS_GET没有找到这个key[%s]>" % key
                context.setERROR( retMsg)
                return retMsg
        except:
            retMsg = "CASE_ERROR:关键字REDIS_GET调用时Redis数据库%s连接失败>" % dbKey
            context.setERROR( retMsg)
            return retMsg
    else:
        retMsg = "CASE_ERROR:关键字REDIS_GET调用时没有找到Redis数据库%s的配置>" % dbKey
        context.setERROR( retMsg)
        return retMsg

@keyword()
@catch_exception
def REDIS_DEL(value,context,strTobeProcessed = ""):
    """
    REDIS_DEL(key,db=0,service=mls-biz-support)
    :param key: 必须的
    :param db: 可选的，0-15 默认是0
    :param system: 可选的，默认是Default
    :return:
    """
    paramList,paramDict = getParamListAndKWParam(strTobeProcessed, context)
    # 如果获取参数等导致错误，不继续执行登录返回错误原因。
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字REDIS_DEL执行时解析参数列表返回错误。返回参数列表为%s" % str(paramList)
        context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
        return retMsg

    key,value,db,dbKey,timeout = "","",0,"default",None
    redisHand = None
    if len(paramList) < 1:
        retMsg = "CASE_ERROR:关键字REDIS_DEL调用时参数不能小于1个。"
        context.setERROR(retMsg)
        return retMsg
    if len(paramList) > 3:
        retMsg = "CASE_ERROR:关键字REDIS_DEL调用时参数不能大于3个。"
        context.setERROR( retMsg)
        return retMsg

    key = paramList[0].strip()

    dbBase = "0"
    if len(paramList) >= 2:
        dbBase = paramList[1].strip()
    if "db" in paramDict.keys():
        dbBase = paramDict["db"]

    if isInt(dbBase) and int(dbBase) >= 0 :
        db = int(dbBase)
    else:
        retMsg = "CASE_ERROR:关键字REDIS_DEL调用时参数2[db]必须是大于等于0的整数。"
        context.setERROR( retMsg)
        return retMsg

    if len(paramList) == 3:
        dbKey = paramList[2].strip()
    if "service" in paramDict.keys():
        dbKey = paramDict["service"].strip()

    if dbKey in context.serviceRedisDict.keys():
        redisHand = context.serviceRedisDict[dbKey]
        redisHand.db = db
        try:
            redisHand.connect()
            try:
                retV = redisHand.del_data(key)
                return retV
            except:
                retMsg = "CASE_ERROR:关键字REDIS_DEL没有找到这个key[%s]>" % key
                context.setERROR( retMsg)
                return retMsg
        except:
            retMsg = "CASE_ERROR:关键字REDIS_DEL调用时Redis数据库%s连接失败>" % dbKey
            context.setERROR( retMsg)
            return retMsg
    else:
        retMsg = "CASE_ERROR:关键字REDIS_DEL调用时没有找到Redis数据库%s的配置>" % dbKey
        context.setERROR( retMsg)
        return retMsg

@keyword()
@catch_exception
def REDIS_FLUSHALL(value,context,strTobeProcessed = ""):
    """
    REDIS_FLUSH_ALL(db=0,service=mls-biz-support)
    :param key: 必须的
    :param db: 可选的，0-15 默认是0
    :param system: 可选的，默认是Default
    :return:
    """
    paramList,paramDict = getParamListAndKWParam(strTobeProcessed, context)
    # 如果获取参数等导致错误，不继续执行登录返回错误原因。
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字REDIS_FLUSH_ALL执行时解析参数列表返回错误。返回参数列表为%s" % str(paramList)
        context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
        return retMsg

    key,value,db,dbKey,timeout = "","",0,"default",None
    redisHand = None
    if len(paramList) > 2:
        retMsg = "CASE_ERROR:关键字REDIS_FLUSH_ALL调用时参数不能大于2个。"
        context.setERROR( retMsg)
        return retMsg

    key = paramList[0].strip()

    dbBase = "0"
    if len(paramList) >= 1:
        dbBase = paramList[0].strip()
    if "db" in paramDict.keys():
        dbBase = paramDict["db"]

    if isInt(dbBase) and int(dbBase) >= 0 :
        db = int(dbBase)
    else:
        retMsg = "CASE_ERROR:关键字REDIS_FLUSH_ALL调用时参数1[db]必须是大于等于0的整数。"
        context.setERROR( retMsg)
        return retMsg

    if len(paramList) == 2:
        dbKey = paramList[1].strip()
    if "service" in paramDict.keys():
        dbKey = paramDict["service"].strip()

    if dbKey in context.serviceRedisDict.keys():
        redisHand = context.serviceRedisDict[dbKey]
        redisHand.db = db
        try:
            redisHand.connect()
            try:
                retV = redisHand.flushall()
                return retV
            except:
                retMsg = "CASE_ERROR:关键字REDIS_FLUSH_ALL执行异常！>"
                context.setERROR( retMsg)
                return retMsg
        except:
            retMsg = "CASE_ERROR:关键字REDIS_FLUSH_ALL调用时Redis数据库%s连接失败>" % dbKey
            context.setERROR( retMsg)
            return retMsg
    else:
        retMsg = "CASE_ERROR:关键字REDIS_FLUSH_ALL调用时没有找到Redis数据库%s的配置>" % dbKey
        context.setERROR( retMsg)
        return retMsg

@keyword()
@catch_exception
def MONGO_INSERT(value,context,strTobeProcessed = ""):
    """
    REDIS_FLUSH_ALL(db=0,service=mls-biz-support)
    :param key: 必须的
    :param db: 可选的，0-15 默认是0
    :param system: 可选的，默认是Default
    :return:
    """
    paramList,paramDict = getParamListAndKWParam(strTobeProcessed, context)
    # 如果获取参数等导致错误，不继续执行登录返回错误原因。
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字MONGO_INSERT执行时解析参数列表返回错误。返回参数列表为%s" % str(paramList)
        context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
        return retMsg

    if len(paramList) != 4 and len(paramList) != 3:
        retMsg = "CASE_ERROR:关键字MONGO_INSERT调用时参数必须是3个或者4个（调用默认库时不需要穿servicekey）。"
        context.setERROR(retMsg)
        return retMsg

    if len(paramList) == 3:
        mongoServiceKey, dbname, setname, insertDictOrListJson = "default",paramList[0],paramList[1],paramList[2]
    else:
        mongoServiceKey, dbname, setname, insertDictOrListJson = paramList[0],paramList[1],paramList[2],paramList[3]


    if isJson(insertDictOrListJson) == False:
        retMsg = "CASE_ERROR:关键字MONGO_INSERT调用时插入的值必须是合法的JSON！"
        context.setERROR(retMsg)
        return retMsg

    insertObj = json.loads(insertDictOrListJson)

    try:
        insertRes = context.serviceMongoDBDict[mongoServiceKey].refresh_collect(dbname,setname).insert(insertObj)
        return str(insertRes)
    except:
        retMsg = "CASE_ERROR:关键字MONGO_INSERT执行时出现异常！\n参数列表%s\n异常原因：%s" % (paramList, traceback.format_exc())
        context.setERROR(retMsg)
        return retMsg

@keyword()
@catch_exception
def MONGO_FIND(value,context,strTobeProcessed = ""):
    """
    REDIS_FLUSH_ALL(db=0,service=mls-biz-support)
    :param key: 必须的
    :param db: 可选的，0-15 默认是0
    :param system: 可选的，默认是Default
    :return:
    """
    paramList,paramDict = getParamListAndKWParam(strTobeProcessed, context)
    # 如果获取参数等导致错误，不继续执行登录返回错误原因。
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字MONGO_FIND执行时解析参数列表返回错误。返回参数列表为%s" % str(paramList)
        context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
        return retMsg

    if len(paramList) != 4 and len(paramList) != 3:
        retMsg = "CASE_ERROR:关键字MONGO_FIND调用时参数必须是3个或者4个（调用默认库时不需要穿servicekey）。"
        context.setERROR(retMsg)
        return retMsg

    if len(paramList) == 3:
        mongoServiceKey, dbname, setname, insertDictOrListJson = "default",paramList[0],paramList[1],paramList[2]
    else:
        mongoServiceKey, dbname, setname, insertDictOrListJson = paramList[0],paramList[1],paramList[2],paramList[3]


    if isJson(insertDictOrListJson) == False:
        retMsg = "CASE_ERROR:关键字MONGO_FIND调用时插入的值必须是合法的JSON！"
        context.setERROR(retMsg)
        return retMsg

    insertObj = json.loads(insertDictOrListJson)

    try:
        findRes = context.serviceMongoDBDict[mongoServiceKey].refresh_collect(dbname,setname).find_to_list(insertObj)
        return json.dumps(findRes)
    except:
        retMsg = "CASE_ERROR:关键字MONGO_FIND执行时出现异常！\n参数列表%s\n异常原因：%s" % (paramList,traceback.format_exc())
        context.setERROR(retMsg)
        return retMsg


@keyword()
@catch_exception
def MONGO_REMOVE(value,context,strTobeProcessed = ""):
    """
    REDIS_FLUSH_ALL(db=0,service=mls-biz-support)
    :param key: 必须的
    :param db: 可选的，0-15 默认是0
    :param system: 可选的，默认是Default
    :return:
    """
    paramList,paramDict = getParamListAndKWParam(strTobeProcessed, context)
    # 如果获取参数等导致错误，不继续执行登录返回错误原因。
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字MONGO_REMOVE执行时解析参数列表返回错误。返回参数列表为%s" % str(paramList)
        context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
        return retMsg

    if len(paramList) != 4 and len(paramList) != 3:
        retMsg = "CASE_ERROR:关键字MONGO_REMOVE调用时参数必须是3个或者4个（调用默认库时不需要穿servicekey）。"
        context.setERROR(retMsg)
        return retMsg

    if len(paramList) == 3:
        mongoServiceKey, dbname, setname, insertDictOrListJson = "default",paramList[0],paramList[1],paramList[2]
    else:
        mongoServiceKey, dbname, setname, insertDictOrListJson = paramList[0],paramList[1],paramList[2],paramList[3]


    if isJson(insertDictOrListJson) == False:
        retMsg = "CASE_ERROR:关键字MONGO_REMOVE调用时插入的值必须是合法的JSON！"
        context.setERROR(retMsg)
        return retMsg

    insertObj = json.loads(insertDictOrListJson)

    try:
        findRes = context.serviceMongoDBDict[mongoServiceKey].refresh_collect(dbname,setname).remove(insertObj)
        return json.dumps(findRes)
    except:
        retMsg = "CASE_ERROR:关键字MONGO_REMOVE执行时出现异常！\n参数列表%s\n异常原因：%s" % (paramList,traceback.format_exc())
        context.setERROR(retMsg)
        return retMsg

@keyword()
@catch_exception
def MONGO_UPDATE(value,context,strTobeProcessed = ""):
    """
    REDIS_FLUSH_ALL(db=0,service=mls-biz-support)
    :param key: 必须的
    :param db: 可选的，0-15 默认是0
    :param system: 可选的，默认是Default
    :return:
    """
    paramList,paramDict = getParamListAndKWParam(strTobeProcessed, context)
    # 如果获取参数等导致错误，不继续执行登录返回错误原因。
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字MONGO_UPDATE执行时解析参数列表返回错误。返回参数列表为%s" % str(paramList)
        context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
        return retMsg

    if len(paramList) != 4 and len(paramList) != 5:
        retMsg = "CASE_ERROR:关键字MONGO_UPDATE调用时参数必须是4个或者5个（调用默认库时不需要穿servicekey）。"
        context.setERROR(retMsg)
        return retMsg

    if len(paramList) == 4:
        mongoServiceKey, dbname, setname, insertDictOrListJson,updateDictJSON = "default",paramList[0],paramList[1],paramList[2],paramList[3]
    else:
        mongoServiceKey, dbname, setname, insertDictOrListJson,updateDictJSON = paramList[0],paramList[1],paramList[2],paramList[3],paramList[4]


    if isJson(insertDictOrListJson) == False:
        retMsg = "CASE_ERROR:关键字MONGO_UPDATE调用时插入的值必须是合法的JSON！"
        context.setERROR(retMsg)
        return retMsg

    insertObj = json.loads(insertDictOrListJson)
    updateObj = json.loads(updateDictJSON)

    try:
        findRes = context.serviceMongoDBDict[mongoServiceKey].refresh_collect(dbname,setname).update(insertObj,updateObj)
        return json.dumps(findRes)
    except:
        retMsg = "CASE_ERROR:关键字MONGO_UPDATE执行时出现异常！\n参数列表%s\n异常原因：%s" % (paramList,traceback.format_exc())
        context.setERROR(retMsg)
        return retMsg