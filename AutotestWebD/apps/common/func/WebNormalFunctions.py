import functools
import logging
import traceback

def catch_exception(func):
    @functools.wraps(func)
    def catch_exception_wrapper(*args, **kwargs):
        try:
            funcRet = func(*args, **kwargs)
            return funcRet
        except Exception as e:
            retMsg = "[EXCEPTION]: 函数[%s]异常：%s" % (func.__name__,traceback.format_exc())
            logging.error(retMsg)
            logging.error(traceback.format_exc())
            #不要return，可以继续执行后续代码
    return catch_exception_wrapper