import functools
import logging
import time
import traceback
from threading import Timer
from functools import wraps
from datetime import datetime
from threading import Thread
from core.tools.CommonFunc import *
from core.const.GlobalConst import ResultConst
import core.tools.DBTool


def keyword(startTag="",endTag="",splitByTag = ""):
    def _deco(func):
        @functools.wraps(func)
        def __deco(*args, **kwargs):
            find_start_tag = startTag == "" and func.__name__ + "(" or startTag  # 实际的前切割字符，比如 LOGIN(
            find_end_tag = endTag == "" and ")" or endTag # end结束符 比如 )
            splitTag = splitByTag == "" and "," or splitByTag  #切割符号 默认 ,

            value = args[0]
            context = args[1]
            params_splited = value.split(find_start_tag)  # 关键字的切割列表，也就是关键字出现次数的列表。
            len_params_splited = len(params_splited)   #关键字出现次数
            preMatchTag = find_start_tag[-1*len(find_end_tag):]  #跟结束符对应的匹配符号，比如 (
            if len_params_splited == 1:  # 没有发现关键字 find_start_tag
                return value

            textStartTagList = ["$TEXT[", "$INCLUDE[", "$IMPORT[", "$RUNFUNC["]
            varStartTagList = ["$VAR[","$GVAR[","$CONST[",
                               "var(", "gvar(", "const(",
                               "{{"]
            if find_start_tag in textStartTagList or find_start_tag in varStartTagList:
                #如果是Text or var类型的处理，一次性执行。
                for i in range(0, len_params_splited-1):
                    ##注释掉是因为采用新版TEXT后，是执行到才处理，不需要单独处理了。
                    # 判断是否被注释掉。仅仅只有组合文本的时候才去判断是否注释的
                    # if find_start_tag in textStartTagList:
                    #     isAnnoed = False
                    #     for tmpAnnoedLetterIndex in range(len(params_splited[i]) - 1, -1, -1):
                    #         charToBeChecked = params_splited[i][tmpAnnoedLetterIndex]
                    #         if charToBeChecked == ";":
                    #             break
                    #         elif charToBeChecked == "#":
                    #             isAnnoed = True
                    #             break
                    #     if isAnnoed:
                    #         params_splited[i] = params_splited[i] + find_start_tag
                    #         continue
                    # #########判断是否被注释掉结束####################################################

                    # 不是文本注释，进入文本和变量处理
                    # 取真正的结束位置，有匹配的小括号不处理
                    cIndex = -1
                    while True:
                        Dpos = params_splited[i + 1].find(find_end_tag, cIndex + 1)
                        # 判断从开始到结束为止出现了几次preMatchTagn
                        s = params_splited[i + 1][cIndex + 1:Dpos]
                        ts = s.replace(preMatchTag, '')
                        countPreMatchTag = int((len(s) - len(ts)) / len(preMatchTag))
                        if countPreMatchTag == 0:
                            break
                        else:
                            # 出现了几次要继续找后面的几次结束为止
                            for i in range(0, countPreMatchTag - 1):
                                Dpos = params_splited[i + 1].find(find_end_tag, Dpos + 1)

                            cIndex = Dpos
                    # 取真正的结束位置，有匹配的小括号不处理 END

                    if Dpos == -1:
                        # 没有发现结束符号，关键字结束。
                        params_splited[i + 1] = find_start_tag + params_splited[i + 1]
                        substr_tobe_replace = params_splited[i + 1]
                        replacedValue = "[关键字%s未发现结束符]" % find_start_tag[:-1]
                        params_splited[i + 1] = params_splited[i + 1].replace(substr_tobe_replace, replacedValue, 1)
                        continue
                    else:
                        # 发现结束符号
                        try:
                            strTobeProcessed = params_splited[i + 1][:Dpos]  # 取出关键字中间的参数，也就是要处理的部分
                            logging.debug("处理关键字%s%s要处理的参数string:%s" % (find_start_tag, find_end_tag, strTobeProcessed))
                            substr_tobe_replace = strTobeProcessed + find_end_tag
                            ###############################################开始处理####################################################################
                            # 对paramList 进行对应的处理
                            #key 类的引用要去掉双引号单引号
                            strTobeProcessed = strTobeProcessed.replace("'","").replace("\"","").strip()
                            replacedValue = func(value, context, strTobeProcessed)
                            logging.debug("处理关键字%s%s后的结果:%s" % (find_start_tag, find_end_tag, replacedValue))
                            ###############################################处理结束####################################################################
                            try:
                                if TypeTool.is_list(replacedValue) or TypeTool.is_dict(replacedValue):
                                    processedReplacedValue = json.dumps(replacedValue)
                                else:
                                    processedReplacedValue = str(replacedValue)
                            except:
                                processedReplacedValue = str(replacedValue)
                            params_splited[i + 1] = params_splited[i + 1].replace(str(substr_tobe_replace),processedReplacedValue ,1)  # 执行替换
                            # 这里注释掉是因为如果处理变量过程中ERROR了，变量显示就出毛病。不过貌似不是这的事。。
                            if context.testResult == ResultConst.EXCEPTION or context.testResult == ResultConst.ERROR:
                                break
                        except Exception as e:
                            params_splited[i + 1] = find_start_tag + params_splited[i + 1]
                            continue
            else:
                #不是引入文本或者变量，那么就是处理关键字了，这个时候只处理第一个。
                processParamSplitedList = ["",""]
                processParamSplitedList[0] = params_splited[0]
                processParamSplitedList[1] = params_splited[1]
                for pIndex in range(2,len_params_splited):
                    processParamSplitedList[1] += find_start_tag+params_splited[pIndex]

                params_splited = processParamSplitedList #转换后只处理第一个，后面的是值。

                logging.debug("开始处理关键字%s%s" % (find_start_tag,find_end_tag))
                #开始循环处理各个关键字的参数，并获得值
                for i in range(0, 1):
                    # 判断是否被注释掉。仅仅只有组合文本的时候才去判断是否注释的
                    # textStartTagList = ["$TEXT[","$INCLUDE[","$IMPORT[","$RUNFUNC["]
                    # if find_start_tag in textStartTagList:
                    #     isAnnoed = False
                    #     for tmpAnnoedLetterIndex in range(len(params_splited[i])-1,-1,-1):
                    #         charToBeChecked = params_splited[i][tmpAnnoedLetterIndex]
                    #         if charToBeChecked == ";":
                    #             break
                    #         elif charToBeChecked == "#":
                    #             isAnnoed= True
                    #             break
                    #     if isAnnoed:
                    #         params_splited[i] = params_splited[i] + find_start_tag
                    #         break
                    # #########判断是否被注释掉结束####################################################

                    # countPreMatchNum = params_splited[i + 1].count(preMatchTag)
                    # Dpos = findTagPosByTimes(params_splited[i + 1],find_end_tag,countPreMatchNum+1)
                    #取真正的结束位置，有匹配的小括号不处理
                    cIndex = -1
                    while True:
                        Dpos = params_splited[i + 1].find(find_end_tag,cIndex+1)
                        #判断从开始到结束为止出现了几次preMatchTagn
                        s = params_splited[i + 1][cIndex+1:Dpos]
                        ts = s.replace(preMatchTag, '')
                        countPreMatchTag = int ((len(s) - len(ts))/len(preMatchTag))
                        if countPreMatchTag == 0:
                            break
                        else:
                            #出现了几次要继续找后面的几次结束为止
                            for i in range(0,countPreMatchTag-1):
                                Dpos = params_splited[i + 1].find(find_end_tag, Dpos + 1)

                            cIndex = Dpos
                    # 取真正的结束位置，有匹配的小括号不处理 END

                    if Dpos == -1:
                        # 没有发现结束符号，关键字结束。
                        params_splited[i + 1] = find_start_tag + params_splited[i + 1]
                        substr_tobe_replace = params_splited[i + 1]
                        replacedValue = "[关键字%s未发现结束符]" % find_start_tag[:-1]
                        params_splited[i + 1] = params_splited[i + 1].replace(substr_tobe_replace, replacedValue,1)
                        continue
                    else:
                        # 发现结束符号
                        try:
                            strTobeProcessed = params_splited[i + 1][:Dpos]  # 取出关键字中间的参数，也就是要处理的部分
                            logging.debug("处理关键字%s%s要处理的参数string:%s" % (find_start_tag,find_end_tag,strTobeProcessed))
                            substr_tobe_replace = strTobeProcessed + find_end_tag
                            ###############################################开始处理####################################################################
                            # 对paramList 进行对应的处理
                            replacedValue = func(value,context,strTobeProcessed)
                            logging.debug("处理关键字%s%s后的结果:%s" % (find_start_tag, find_end_tag, replacedValue))
                            ###############################################处理结束####################################################################
                            if TypeTool.is_str(replacedValue) == False:
                                if TypeTool.is_dict(replacedValue) or TypeTool.is_list(replacedValue):
                                    replacedValue = json.dumps(replacedValue,ensure_ascii=False)
                                else:
                                    replacedValue = str(replacedValue)
                            params_splited[i + 1] = params_splited[i + 1].replace(substr_tobe_replace,replacedValue,1)  # 执行替换
                            # 这里注释掉是因为如果处理变量过程中ERROR了，变量显示就出毛病。不过貌似不是这的事。。
                            if context.testResult == ResultConst.EXCEPTION or context.testResult == ResultConst.ERROR:
                                break
                        except Exception as e:
                            params_splited[i + 1] = find_start_tag + params_splited[i + 1]
                            continue

            new_params = ""
            for value in params_splited:
                new_params = new_params + value
            if new_params != "":
                logging.debug("处理关键字%s%s结果:%s" % (find_start_tag,find_end_tag,new_params))
            return new_params

        return __deco
    return _deco

def take_time(func):
    @functools.wraps(func)
    def take_time_wapper(*args, **kwargs):
        timeStart = time.time()
        funcRet = func(*args, **kwargs)
        timeEnd = time.time()
        logging.debug("函数[%s]执行占用时间: %f ms" %(func.__name__,(timeEnd-timeStart)*1000))
        return funcRet
    return take_time_wapper

def set_logging(func):
    @functools.wraps(func)
    def set_logging_wapper(*args, **kwargs):
        from runfunc.initial import init_logging
        from core.config.InitConfig import LogConfig
        init_logging(logFilePath=LogConfig.FILE, level=LogConfig.LEVEL)
        funcRet = func(*args, **kwargs)
        return funcRet
    return set_logging_wapper

def catch_exception(func):
    @functools.wraps(func)
    def catch_exception_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            retMsg = "★★★★★★★★★★平台异常，请联系管理员★★★★★★★★★★\n[EXCEPTION]: 函数[%s]异常：%s★★★★★★★★★★平台异常，请联系管理员★★★★★★★★★★" % (func.__name__,traceback.format_exc())
            logging.error(retMsg)
            #不要return，可以继续执行后续代码
            try:
                db = core.tools.DBTool.DBTool().initGlobalDBConf()
                db.connect()
                db.execute_sql("insert into tb0_error_log(title,errorLogText,logLevel,state,addBy,modBy,addTime,modTime) VALUES ('执行函数%s出现未知异常','%s',10,1,'admin','admin','%s','%s')" % (func.__name__,replacedForIntoDB(traceback.format_exc()),get_current_time(),get_current_time()))
                db.release()
            finally:
                return retMsg
    return catch_exception_wrapper


def time_limited(time_limited):
    def wrapper(func):
        @functools.wraps(func)
        def __wrapper(*args, **kwargs):
            class TimeLimited(Thread):
                def __init__(self):
                    Thread.__init__(self)
                    self.runResult  = ""
                def run(self):
                    self.runResult =  func(*args, **kwargs)

            t = TimeLimited()
            t.start()
            t.join(timeout=time_limited)
            if t.is_alive():
                stop_thread(t)
                raise Exception('FUNC_TIMEOUT')
            else:
                return t.runResult
        return __wrapper
    return wrapper

@time_limited(3)
def limittest():
    time.sleep(1)
    return 2

if __name__ == '__main__':
    print(limittest())