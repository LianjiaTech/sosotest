import calendar,time
from core.decorator.normal_functions import keyword,catch_exception
from core.tools.CommonFunc import *
from core.keywords.ALL_FUNC import *
from core.const.GlobalConst import ResultConst

@keyword()
@catch_exception
def DATETIME_FORMAT(value,context, strTobeProcessed = ""):
    ###############################################开始处理####################################################################
    paramList = getParamList(strTobeProcessed,context)
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字DATETIME_FORMAT执行时解析参数列表返回错误。返回参数列表为%s" % str(paramList)
        context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
        return retMsg
    paramLength = len(paramList)
    if paramLength != 1 and paramLength != 2:
        context.setERROR( "<ERROR:参数错误>")
        return "<ERROR:参数错误>"
    try:
        if paramLength == 1:
            sysnow = datetime.datetime.now().strftime(paramList[0])
        else:
            tparam = paramList[1].strip()
            tagPlusOrSub = tparam[0:1]
            tagNum = tparam[1:-1].strip()
            tagDayOrSeconds = tparam[-1:]
            if tagDayOrSeconds == "D":
                # 处理加减日期
                try:
                    if tagPlusOrSub == "+":
                        tobe_plus_value = int(tagNum)
                        sysnow = (datetime.datetime.now() + datetime.timedelta(days=tobe_plus_value)).strftime(
                            paramList[0])
                    elif tagPlusOrSub == "-":
                        tobe_plus_value = int(tagNum)
                        sysnow = (datetime.datetime.now() - datetime.timedelta(days=tobe_plus_value)).strftime(
                            paramList[0])
                    else:
                        sysnow = datetime.datetime.now().strftime(paramList[0])
                except Exception as e:
                    sysnow = "<ERROR:+D中间必须是数字>"
                    context.setERROR( sysnow)

            elif tagDayOrSeconds == "S":
                # DONE 处理加减秒
                try:
                    if tagPlusOrSub == "+":
                        tobe_plus_value = int(tagNum)
                        sysnow = (datetime.datetime.now() + datetime.timedelta(seconds=tobe_plus_value)).strftime(
                            paramList[0])
                    elif tagPlusOrSub == "-":
                        tobe_plus_value = int(tagNum)
                        sysnow = (datetime.datetime.now() - datetime.timedelta(seconds=tobe_plus_value)).strftime(
                            paramList[0])
                    else:
                        sysnow = datetime.datetime.now().strftime(paramList[0])
                except Exception as e:
                    sysnow = "<ERROR:+S中间必须是数字>"
                    context.setERROR( sysnow)


    except Exception as e:
        sysnow = "<ERROR:错误的日期格式化>"
        context.setERROR( sysnow)

    finally:
        return sysnow


@keyword()
@catch_exception
def SPECIAL_TIMESTAMP(value,context, strTobeProcessed = ""):
    # SPECIAL_TIMESTAMP(START_OF_MONTH,+-1DS)
    # SPECIAL_TIMESTAMP(END_OF_MONTH,YY-MM-DD hh:mm:ss)
    # SPECIAL_TIMESTAMP(START_OF_WEEK,YY-MM-DD hh:mm:ss)
    # SPECIAL_TIMESTAMP(END_OF_WEEK,YY-MM-DD hh:mm:ss)
    # SPECIAL_TIMESTAMP(START_OF_DAY,YY-MM-DD hh:mm:ss)
    # SPECIAL_TIMESTAMP(END_OF_DAY,YY-MM-DD hh:mm:ss)
    # 参数1：获取特殊时间戳类型，参数2传入的时间参数，参数2没有的时候默认当前时间，有的时候判断是timestamp还是格式化日期 YYYY-mm-dd HH:MM:SS
    ###############################################开始处理####################################################################
    paramList = getParamList(strTobeProcessed,context)
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字SPECIAL_TIMESTAMP执行时解析参数列表返回错误。返回参数列表为%s" % str(paramList)
        context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
        return retMsg
    paramLength = len(paramList)
    retStamp = 0
    if paramLength != 1 and paramLength != 2 :
        retStamp = "<ERROR:参数错误>"
        context.setERROR( retStamp)
        return retStamp
    try:
        stampType = paramList[0]
        if stampType == "START_OF_MONTH":
            #每个月的第一天
            curDatetime = str(datetime.datetime.now().strftime("%Y-%m") + "-01 00:00:00")
            if curDatetime == "":
                retStamp = "<ERROR:日期格式错误>"
                context.setERROR( retStamp)

            else:
                # 正式通过curDatetime来生成时间戳
                # 转换成时间数组
                timeArray = time.strptime(curDatetime, "%Y-%m-%d %H:%M:%S")
                # 转换成时间戳
                retStamp = str(int(time.mktime(timeArray)))

        elif stampType == "END_OF_MONTH":

            # 每个月的最后一天

            curYearmon = str(datetime.datetime.now().strftime("%Y-%m"))
            dateList = curYearmon.split("-")

            if len(dateList) >= 2:
                curYear = int(dateList[0])
                curMonth = int(dateList[1])
            firstDayWeekDay, monthRange = calendar.monthrange(curYear, curMonth)
            curDatetime = "%s-%s-%s 23:59:59" % (curYear, curMonth, monthRange)
            if curDatetime == "":
                retStamp = "<ERROR:日期格式错误>"
                context.setERROR( retStamp)

            else:
                # 正式通过curDatetime来生成时间戳
                # 转换成时间数组
                timeArray = time.strptime(curDatetime, "%Y-%m-%d %H:%M:%S")
                # 转换成时间戳
                retStamp = str(int(time.mktime(timeArray)))

        elif stampType == "START_OF_WEEK":

            # 每个周的第一天

            curDate = str(datetime.datetime.now().strftime("%Y-%m-%d"))
            date_str = curDate
            fmt = '%Y-%m-%d'
            time_tuple = time.strptime(date_str, fmt)
            year, month, day = time_tuple[:3]
            a_date = datetime.datetime(year, month, day, 0, 0, 0)
            wDay = a_date.weekday()
            monDay = a_date - datetime.timedelta(days=wDay)
            retStamp = str(int(monDay.timestamp()))

        elif stampType == "END_OF_WEEK":

            # 每个周的结束时间戳
            curDate = str(datetime.datetime.now().strftime("%Y-%m-%d"))
            date_str = curDate
            fmt = '%Y-%m-%d'
            time_tuple = time.strptime(date_str, fmt)
            year, month, day = time_tuple[:3]
            a_date = datetime.datetime(year, month, day, 23, 59, 59)
            wDay = a_date.weekday()
            sunDay = a_date + datetime.timedelta(days=6 - wDay)
            retStamp = str(int(sunDay.timestamp()))

        elif stampType == "START_OF_DAY":

            # 每天的开始时间戳

            curDatetime = str(datetime.datetime.now().strftime("%Y-%m-%d 00:00:00"))
            if curDatetime == "":
                retStamp = "<ERROR:日期格式错误>"
                context.setERROR( retStamp)

            else:
                # 正式通过curDatetime来生成时间戳
                # 转换成时间数组
                timeArray = time.strptime(curDatetime, "%Y-%m-%d %H:%M:%S")
                # 转换成时间戳
                retStamp = str(int(time.mktime(timeArray)))

        elif stampType == "END_OF_DAY":

            # 每天的结束时间戳
            curDatetime = str(datetime.datetime.now().strftime("%Y-%m-%d 23:59:59"))
            if curDatetime == "":
                retStamp = "<ERROR:日期格式错误>"
                context.setERROR( retStamp)

            else:
                # 正式通过curDatetime来生成时间戳
                # 转换成时间数组
                timeArray = time.strptime(curDatetime, "%Y-%m-%d %H:%M:%S")
                # 转换成时间戳
                retStamp = str(int(time.mktime(timeArray)))

        else:
            retStamp = "<ERROR:错误的特殊时间戳类型>"
            context.setERROR( retStamp)

            return str(retStamp)

        #处理加减变量
        if len(paramList) == 2 and isInt(retStamp):
            addplusVar = paramList[1].strip()
            tagPlusOrSub = addplusVar[0:1]
            tagNum = addplusVar[1:-1].strip()
            tagDayOrSeconds = addplusVar[-1:]
            if tagDayOrSeconds == "D":
                # 处理加减日期
                try:
                    if tagPlusOrSub == "+":
                        tobe_plus_value = int(tagNum) * 3600 * 24
                        retStamp = str(int(retStamp) + tobe_plus_value)
                    elif tagPlusOrSub == "-":
                        tobe_plus_value = int(tagNum) * 3600 * 24
                        retStamp = str(int(retStamp) - tobe_plus_value)
                    else:
                        tobe_plus_value = int(tagNum) * 3600 * 24
                        retStamp = str(int(retStamp) + tobe_plus_value)
                except Exception as e:
                    # logging.error(traceback.format_exc())
                    retStamp = "<ERROR:+D中间必须是数字>"
                    context.setERROR( retStamp)

            elif tagDayOrSeconds == "S":
                # done 处理加减秒
                try:
                    if tagPlusOrSub == "+":
                        tobe_plus_value = int(tagNum)
                        retStamp = str(int(retStamp) + tobe_plus_value)
                    elif tagPlusOrSub == "-":
                        tobe_plus_value = int(tagNum)
                        retStamp = str(int(retStamp) - tobe_plus_value)
                    else:
                        tobe_plus_value = int(tagNum)
                        retStamp = str(int(retStamp) + tobe_plus_value)
                except Exception as e:
                    # logging.error(traceback.format_exc())
                    retStamp = "<ERROR:+S中间必须是数字>"
                    context.setERROR( retStamp)

    except Exception as e:
        retStamp = "<ERROR:错误的日期格式化>"
        context.setERROR( retStamp)

    finally:
        return str(retStamp)


@keyword()
@catch_exception
def TIMESTAMP(value, context, strTobeProcessed = ""):
    paramList = getParamList(strTobeProcessed,context)
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字TIMESTAMP执行时解析参数列表返回错误。返回参数列表为%s" % str(paramList)
        context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
        return retMsg
    sysnow = str(int(time.time()))
    strTobeProcessed = paramList[0].strip()
    try:
        if strTobeProcessed == "":
            sysnow = sysnow
        else:
            strTobeProcessed = core.processor.CP.CP.getProcessedValue(strTobeProcessed, context)
            tagPlusOrSub = strTobeProcessed[0:1]
            tagNum = strTobeProcessed[1:-1].strip()
            tagDayOrSeconds = strTobeProcessed[-1:]
            if tagDayOrSeconds == "D":
                # 处理加减日期
                try:
                    if tagPlusOrSub == "+":
                        tobe_plus_value = int(tagNum) * 3600 * 24
                        sysnow = str(int(time.time()) + tobe_plus_value)
                    elif tagPlusOrSub == "-":
                        tobe_plus_value = int(tagNum) * 3600 * 24
                        sysnow = str(int(time.time()) - tobe_plus_value)
                    else:
                        tobe_plus_value = int(tagNum) * 3600 * 24
                        sysnow = str(int(time.time()) + tobe_plus_value)
                except Exception as e:
                    # logging.error(traceback.format_exc())
                    sysnow = "<ERROR:+D中间必须是数字>"
                    context.setERROR( sysnow)

            elif tagDayOrSeconds == "S":
                # done 处理加减秒
                try:
                    if tagPlusOrSub == "+":
                        tobe_plus_value = int(tagNum)
                        sysnow = str(int(time.time()) + tobe_plus_value)
                    elif tagPlusOrSub == "-":
                        tobe_plus_value = int(tagNum)
                        sysnow = str(int(time.time()) - tobe_plus_value)
                    else:
                        tobe_plus_value = int(tagNum)
                        sysnow = str(int(time.time()) + tobe_plus_value)
                except Exception as e:
                    # logging.error(traceback.format_exc())
                    sysnow = "<ERROR:+S中间必须是数字>"
                    context.setERROR( sysnow)


    except Exception as e:
        # logging.error(traceback.format_exc())
        sysnow = "<ERROR:错误的时间戳>"
        context.setERROR( sysnow)

    finally:
        return sysnow


@keyword()
@catch_exception
def TIMESTAMP_FORMAT(value,context, strTobeProcessed = ""):
    #TIMESTAMP_FORMAT(timestamp,formatStr)
    # 参数1：获取特殊时间戳类型，参数2传入的时间参数，参数2没有的时候默认当前时间，有的时候判断是timestamp还是格式化日期 YYYY-mm-dd HH:MM:SS
    ###############################################开始处理####################################################################
    paramList = getParamList(strTobeProcessed,context)
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字TIMESTAMP_FORMAT执行时解析参数列表返回错误。返回参数列表为%s" % str(paramList)
        context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
        return retMsg
    paramLength = len(paramList)
    retStamp = 0
    if paramLength != 2 :
        retStamp = "<ERROR:参数错误>"
        context.setERROR( retStamp)
        return retStamp
    try:
        timestamp = int(paramList[0])
        formatStr = paramList[1]
        # 转换成localtime
        time_local = time.localtime(timestamp)
        # 转换成新的时间格式(2016-05-05 20:28:54)
        retStamp = str(time.strftime(formatStr, time_local))
    except Exception as e:
        retStamp = "<ERROR:错误的日期格式化>"
        context.setERROR( retStamp)

    finally:
        return str(retStamp)


@keyword()
@catch_exception
def DAYS_OF_MONTH(value,context, strTobeProcessed = ""):
    #DAYS_OF_MONTH(THIS,THIS) # 某年/某月 THIS是当年 LAST-1上个月，LAST-2，上两个月，直接写数字就是固定好的。
    # 参数1：获取特殊时间戳类型，参数2传入的时间参数，参数2没有的时候默认当前时间，有的时候判断是timestamp还是格式化日期 YYYY-mm-dd HH:MM:SS
    ###############################################开始处理####################################################################
    paramList = getParamList(strTobeProcessed,context)
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字DAYS_OF_MONTH执行时解析参数列表返回错误。返回参数列表为%s" % str(paramList)
        context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
        return retMsg
    paramLength = len(paramList)
    retStamp = 0
    if paramLength != 2 :
        context.setERROR( "<ERROR:参数错误>")
        return "<ERROR:参数错误>"
    try:
        retDaysOfMonth = 0
        yearStr = paramList[0].strip()
        monthStr = paramList[1].strip()
        actYear = 0
        actMonth = 0
        #判断年
        if isInt(yearStr):
            if len(yearStr) != 4 or int(yearStr[0:1] == 0):
                context.setERROR( "<ERROR:错误的年数据>")
                return "<ERROR:错误的年数据>"
            else:
                actYear = int(yearStr)
        else:
            if yearStr == "THIS":
                actYear = datetime.datetime.today().year
            elif yearStr.startswith("LAST") or yearStr.startswith("LAST-"):
                splitYearStrList = yearStr.split("-")
                lastNum = 1
                if len(splitYearStrList) == 2:
                    if isInt(splitYearStrList[1]):
                        lastNum = int(splitYearStrList[1])
                    else:
                        context.setERROR( "<ERROR:错误的LAST使用方式>")
                        return "<ERROR:错误的LAST使用方式>"
                actYear = datetime.datetime.today().year - lastNum
            else:
                context.setERROR( "<ERROR:不合法的年参数>")
                return "<ERROR:不合法的年参数>"

        #判断月
        if isInt(monthStr):
            actMonth = int(monthStr)
        else:
            if monthStr == "THIS":
                actMonth = datetime.datetime.today().month
            elif monthStr.startswith("LAST")  or monthStr.startswith("LAST-"):
                splitMonthStrList = monthStr.split("-")
                lastNum = 1
                if len(splitMonthStrList) >= 2:
                    if isInt(splitMonthStrList[1]):
                        lastNum = int(splitMonthStrList[1])
                    else:
                        context.setERROR( "<ERROR:错误的LAST使用方式>")
                        return "<ERROR:错误的LAST使用方式>"

                actYear = actYear - int(lastNum / 12)
                subMonth = lastNum % 12
                actMonth = datetime.datetime.today().month - subMonth
                if actMonth <= 0:
                    actYear = actYear - 1
                    actMonth = 12 + actMonth

            else:
                context.setERROR( "<ERROR:不合法的月参数>")
                return "<ERROR:不合法的月参数>"

        #根据actYear actMonth获取天数
        if actYear > 1900 and actMonth >= 1 and actMonth <= 12:
            retDaysOfMonth = calendar.monthrange(actYear,actMonth)[1]
        else:
            retDaysOfMonth = "<ERROR:错误的年[%s]或者月[%s]>" % (actYear,actMonth)
            context.setERROR( retDaysOfMonth)

    except Exception as e:
        logging.error(traceback.format_exc())
        retDaysOfMonth = "<ERROR:异常错误>"
        context.setERROR( retDaysOfMonth)

    finally:
        return str(retDaysOfMonth)


@keyword()
@catch_exception
def TIME_SLEEP(value,context, strTobeProcessed = ""):
    paramList = getParamList(strTobeProcessed,context)
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字TIME_SLEEP执行时解析参数列表返回错误。返回参数列表为%s" % str(paramList)
        context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
        return retMsg
    #TIME_SLEEP(1) 表示睡1秒
    ###############################################开始处理####################################################################
    paramLength = len(paramList)
    if paramLength != 1 :
        context.setERROR( "<ERROR:参数错误，休眠失败。>")
        return "<ERROR:参数错误，休眠失败。>"

    logging.debug("开始休眠...")
    sleepSec = 0
    if isInt(paramList[0]):
        sleepSec = int(paramList[0])
        if sleepSec > 60: # 不允许休眠超过60s
            sleepSec = 60
        time.sleep(sleepSec)
        retStamp = "休眠了%d秒" % sleepSec
    else:
        time.sleep(1)
        retStamp = "休眠时间错误，默认休眠了1秒。"
    logging.debug("休眠了%d秒" % sleepSec)
    return str(retStamp)


@keyword()
@catch_exception
def SPECIAL_TIMESTAMP_MS(value,context, strTobeProcessed = ""):
    # SPECIAL_TIMESTAMP(START_OF_MONTH,+-1DS)
    # SPECIAL_TIMESTAMP(END_OF_MONTH,YY-MM-DD hh:mm:ss)
    # SPECIAL_TIMESTAMP(START_OF_WEEK,YY-MM-DD hh:mm:ss)
    # SPECIAL_TIMESTAMP(END_OF_WEEK,YY-MM-DD hh:mm:ss)
    # SPECIAL_TIMESTAMP(START_OF_DAY,YY-MM-DD hh:mm:ss)
    # SPECIAL_TIMESTAMP(END_OF_DAY,YY-MM-DD hh:mm:ss)
    # 参数1：获取特殊时间戳类型，参数2传入的时间参数，参数2没有的时候默认当前时间，有的时候判断是timestamp还是格式化日期 YYYY-mm-dd HH:MM:SS
    ###############################################开始处理####################################################################
    paramList = getParamList(strTobeProcessed,context)
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字SPECIAL_TIMESTAMP执行时解析参数列表返回错误。返回参数列表为%s" % str(paramList)
        context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
        return retMsg
    paramLength = len(paramList)
    retStamp = 0
    if paramLength != 1 and paramLength != 2 :
        retStamp = "<ERROR:参数错误>"
        context.setERROR( retStamp)
        return retStamp
    try:
        stampType = paramList[0]
        if stampType == "START_OF_MONTH":
            #每个月的第一天
            curDatetime = str(datetime.datetime.now().strftime("%Y-%m") + "-01 00:00:00")
            if curDatetime == "":
                retStamp = "<ERROR:日期格式错误>"
                context.setERROR( retStamp)

            else:
                # 正式通过curDatetime来生成时间戳
                # 转换成时间数组
                timeArray = time.strptime(curDatetime, "%Y-%m-%d %H:%M:%S")
                # 转换成时间戳
                retStamp = str(int(time.mktime(timeArray)*1000))

        elif stampType == "END_OF_MONTH":

            # 每个月的最后一天

            curYearmon = str(datetime.datetime.now().strftime("%Y-%m"))
            dateList = curYearmon.split("-")

            if len(dateList) >= 2:
                curYear = int(dateList[0])
                curMonth = int(dateList[1])
            firstDayWeekDay, monthRange = calendar.monthrange(curYear, curMonth)
            curDatetime = "%s-%s-%s 23:59:59" % (curYear, curMonth, monthRange)
            if curDatetime == "":
                retStamp = "<ERROR:日期格式错误>"
                context.setERROR( retStamp)

            else:
                # 正式通过curDatetime来生成时间戳
                # 转换成时间数组
                timeArray = time.strptime(curDatetime, "%Y-%m-%d %H:%M:%S")
                # 转换成时间戳
                retStamp = str(int(time.mktime(timeArray)*1000))

        elif stampType == "START_OF_WEEK":

            # 每个周的第一天

            curDate = str(datetime.datetime.now().strftime("%Y-%m-%d"))
            date_str = curDate
            fmt = '%Y-%m-%d'
            time_tuple = time.strptime(date_str, fmt)
            year, month, day = time_tuple[:3]
            a_date = datetime.datetime(year, month, day, 0, 0, 0)
            wDay = a_date.weekday()
            monDay = a_date - datetime.timedelta(days=wDay)
            retStamp = str(int(monDay.timestamp()*1000))

        elif stampType == "END_OF_WEEK":

            # 每个周的结束时间戳
            curDate = str(datetime.datetime.now().strftime("%Y-%m-%d"))
            date_str = curDate
            fmt = '%Y-%m-%d'
            time_tuple = time.strptime(date_str, fmt)
            year, month, day = time_tuple[:3]
            a_date = datetime.datetime(year, month, day, 23, 59, 59)
            wDay = a_date.weekday()
            sunDay = a_date + datetime.timedelta(days=6 - wDay)
            retStamp = str(int(sunDay.timestamp()*1000))

        elif stampType == "START_OF_DAY":

            # 每天的开始时间戳

            curDatetime = str(datetime.datetime.now().strftime("%Y-%m-%d 00:00:00"))
            if curDatetime == "":
                retStamp = "<ERROR:日期格式错误>"
                context.setERROR( retStamp)

            else:
                # 正式通过curDatetime来生成时间戳
                # 转换成时间数组
                timeArray = time.strptime(curDatetime, "%Y-%m-%d %H:%M:%S")
                # 转换成时间戳
                retStamp = str(int(time.mktime(timeArray)*1000))

        elif stampType == "END_OF_DAY":

            # 每天的结束时间戳
            curDatetime = str(datetime.datetime.now().strftime("%Y-%m-%d 23:59:59"))
            if curDatetime == "":
                retStamp = "<ERROR:日期格式错误>"
                context.setERROR( retStamp)

            else:
                # 正式通过curDatetime来生成时间戳
                # 转换成时间数组
                timeArray = time.strptime(curDatetime, "%Y-%m-%d %H:%M:%S")
                # 转换成时间戳
                retStamp = str(int(time.mktime(timeArray)*1000))

        else:
            retStamp = "<ERROR:错误的特殊时间戳类型>"
            context.setERROR( retStamp)

            return str(retStamp)

        #处理加减变量
        if len(paramList) == 2 and isInt(retStamp):
            addplusVar = paramList[1].strip()
            tagPlusOrSub = addplusVar[0:1]
            tagNum = addplusVar[1:-1].strip()
            tagDayOrSeconds = addplusVar[-1:]
            if tagDayOrSeconds == "D":
                # 处理加减日期
                try:
                    if tagPlusOrSub == "+":
                        tobe_plus_value = int(tagNum) * 3600 * 24
                        retStamp = str(int(retStamp) + tobe_plus_value*1000)
                    elif tagPlusOrSub == "-":
                        tobe_plus_value = int(tagNum) * 3600 * 24
                        retStamp = str(int(retStamp) - tobe_plus_value*1000)
                    else:
                        tobe_plus_value = int(tagNum) * 3600 * 24
                        retStamp = str(int(retStamp) + tobe_plus_value*1000)
                except Exception as e:
                    # logging.error(traceback.format_exc())
                    retStamp = "<ERROR:+D中间必须是数字>"
                    context.setERROR( retStamp)

            elif tagDayOrSeconds == "S":
                # done 处理加减秒
                try:
                    if tagPlusOrSub == "+":
                        tobe_plus_value = int(tagNum)
                        retStamp = str(int(retStamp) + tobe_plus_value*1000)
                    elif tagPlusOrSub == "-":
                        tobe_plus_value = int(tagNum)
                        retStamp = str(int(retStamp) - tobe_plus_value*1000)
                    else:
                        tobe_plus_value = int(tagNum)
                        retStamp = str(int(retStamp) + tobe_plus_value*1000)
                except Exception as e:
                    # logging.error(traceback.format_exc())
                    retStamp = "<ERROR:+S中间必须是数字>"
                    context.setERROR( retStamp)

    except Exception as e:
        retStamp = "<ERROR:错误的日期格式化>"
        context.setERROR( retStamp)

    finally:
        return str(retStamp)


@keyword()
@catch_exception
def TIMESTAMP_MS(value, context, strTobeProcessed = ""):
    paramList = getParamList(strTobeProcessed,context)
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字TIMESTAMP执行时解析参数列表返回错误。返回参数列表为%s" % str(paramList)
        context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
        return retMsg
    sysnow = str(int(time.time()*1000))
    strTobeProcessed = paramList[0].strip()
    try:
        if strTobeProcessed == "":
            sysnow = sysnow
        else:
            strTobeProcessed = core.processor.CP.CP.getProcessedValue(strTobeProcessed, context)
            tagPlusOrSub = strTobeProcessed[0:1]
            tagNum = strTobeProcessed[1:-1].strip()
            tagDayOrSeconds = strTobeProcessed[-1:]
            if tagDayOrSeconds == "D":
                # 处理加减日期
                try:
                    if tagPlusOrSub == "+":
                        tobe_plus_value = int(tagNum) * 3600 * 24
                        sysnow = str(int(time.time()*1000) + tobe_plus_value*1000)
                    elif tagPlusOrSub == "-":
                        tobe_plus_value = int(tagNum) * 3600 * 24
                        sysnow = str(int(time.time()*1000) - tobe_plus_value*1000)
                    else:
                        tobe_plus_value = int(tagNum) * 3600 * 24
                        sysnow = str(int(time.time()*1000) + tobe_plus_value*1000)
                except Exception as e:
                    # logging.error(traceback.format_exc())
                    sysnow = "<ERROR:+D中间必须是数字>"
                    context.setERROR( sysnow)

            elif tagDayOrSeconds == "S":
                # done 处理加减秒
                try:
                    if tagPlusOrSub == "+":
                        tobe_plus_value = int(tagNum)
                        sysnow = str(int(time.time()*1000) + tobe_plus_value*1000)
                    elif tagPlusOrSub == "-":
                        tobe_plus_value = int(tagNum)
                        sysnow = str(int(time.time()*1000) - tobe_plus_value*1000)
                    else:
                        tobe_plus_value = int(tagNum)
                        sysnow = str(int(time.time()*1000) + tobe_plus_value*1000)
                except Exception as e:
                    # logging.error(traceback.format_exc())
                    sysnow = "<ERROR:+S中间必须是数字>"
                    context.setERROR( sysnow)


    except Exception as e:
        # logging.error(traceback.format_exc())
        sysnow = "<ERROR:错误的时间戳>"
        context.setERROR( sysnow)

    finally:
        return sysnow


@keyword()
@catch_exception
def TIMESTAMP_FORMAT_MS(value,context, strTobeProcessed = ""):
    #TIMESTAMP_FORMAT(timestamp,formatStr)
    # 参数1：获取特殊时间戳类型，参数2传入的时间参数，参数2没有的时候默认当前时间，有的时候判断是timestamp还是格式化日期 YYYY-mm-dd HH:MM:SS
    ###############################################开始处理####################################################################
    paramList = getParamList(strTobeProcessed,context)
    if context.testResult == ResultConst.ERROR or context.testResult == ResultConst.EXCEPTION:
        retMsg = "CASE_ERROR:关键字TIMESTAMP_FORMAT执行时解析参数列表返回错误。返回参数列表为%s" % str(paramList)
        context.assertResult = "%s\n%s" % (retMsg, context.assertResult)
        return retMsg
    paramLength = len(paramList)
    retStamp = 0
    if paramLength != 2 :
        retStamp = "<ERROR:参数错误>"
        context.setERROR( retStamp)
        return retStamp
    try:
        timestamp = int(float(paramList[0])/1000)
        formatStr = paramList[1]
        # 转换成localtime
        time_local = time.localtime(timestamp)
        # 转换成新的时间格式(2016-05-05 20:28:54)
        retStamp = str(time.strftime(formatStr, time_local))
    except Exception as e:
        retStamp = "<ERROR:错误的日期格式化>"
        context.setERROR( retStamp)

    finally:
        return str(retStamp)



if __name__ == '__main__':

    # strTobeProcessed = "START_OF_MONTH"
    # strTobeProcessed = "END_OF_MONTH"
    # strTobeProcessed = "START_OF_WEEK"
    # strTobeProcessed = "END_OF_WEEK"
    # strTobeProcessed = "START_OF_DAY"
    actMonth = datetime.datetime.today() - datetime.timedelta(month=1)
    print(actMonth)