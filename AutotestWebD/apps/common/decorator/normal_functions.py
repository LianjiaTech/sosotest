import time,logging, traceback,json, requests
from django.shortcuts import HttpResponse,render
from apps.common.helper.ApiReturn import ApiReturn
import urllib
import re

def is_sql_inject_request(request):
    retBool = False
    if is_sql_injected(request.META.get("PATH_INFO")):
        retBool = True
    if is_sql_injected(request.META.get("QUERY_STRING")):
        retBool = True
    if is_sql_injected(str(request.body)):
        retBool = True

    if retBool:
        logging.error("URL:[%s] PARAMS:[%s] BODY:[%s] 可以被sql注入！请检查！！" % (request.META.get("PATH_INFO"),request.META.get("QUERY_STRING"),str(request.body)))

    return retBool

def is_sql_injected(str):
    matchRes = re.match(r'(.*)(select |insert |update |document|eval|delete |script|alert|union |into |load_file|outfile| not |ifnull\(|database\(\)| or sleep\()(.*)',urllib.parse.unquote(str).lower())
    if matchRes:
        return True
    else:
        return False

def take_time(func):
    def take_time_wapper(*args, **kwargs):
        timeStart = time.time()
        funcRet = func(*args, **kwargs)
        timeEnd = time.time()
        logging.debug("函数[%s]执行占用时间: %f ms" %(func.__name__,(timeEnd-timeStart)*1000))
        return funcRet
    return take_time_wapper

def catch_exception(func):
    def catch_exception_wrapper(*args, **kwargs):
        try:
            funcRet = func(*args, **kwargs)
            return funcRet
        except Exception as e:
            retMsg = "[EXCEPTION]: 函数[%s]异常：%s" % (func.__name__,e)
            logging.error(traceback.format_exc())
            logging.error(retMsg)
            #不要return，可以继续执行后续代码
    return catch_exception_wrapper

def catch_request_exception(func):
    def catch_exception_wrapper(*args, **kwargs):
        try:
            funcRet = func(*args, **kwargs)
            return funcRet
        except Exception as e:
            retMsg = "[EXCEPTION]: 函数[%s]异常：%s" % (func.__name__,e)
            logging.error(traceback.format_exc())
            return HttpResponse(ApiReturn(code=ApiReturn.CODE_EXCEPTION, message=retMsg,body=traceback.format_exc()).toJson())
    return catch_exception_wrapper

def sql_inject_validate(func):
    def catch_exception_wrapper(*args, **kwargs):
        try:
            if is_sql_inject_request(args[0]):
                return HttpResponse(ApiReturn(code=ApiReturn.CODE_EXCEPTION, message="有SQL注入风险，请检查搜索条件！", body="").toJson())
            else:
                funcRet = func(*args, **kwargs)
                return funcRet
        except Exception as e:
            retMsg = "[EXCEPTION]: 函数[%s]异常：%s" % (func.__name__,e)
            logging.error(traceback.format_exc())
            return HttpResponse(ApiReturn(code=ApiReturn.CODE_EXCEPTION, message=retMsg,body=traceback.format_exc()).toJson())
    return catch_exception_wrapper

@catch_exception
@take_time
def tFunc(a,b):
    # res = requests.get('http://www.baidu.com', verify=True)
    # print res.text
    res = requests.get("http://www.163.com")
    c = a + b
    print(res.text)
    print(c)
    json.loads("asdf")


if __name__ == '__main__':
    print (tFunc(1,2))