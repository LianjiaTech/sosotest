from django.shortcuts import HttpResponse
from apps.common.func.CommonFunc import *
from all_models_for_dubbo.models import Tb2DubboInterface
from django.db.models import Max
from django.http import JsonResponse


def dubbo_sug(request):
    interface = request.GET.get('interface', default='')
    method = request.GET.get('method', default='')
    print("interface : " + interface)
    print("method: "+ method)

    if (not interface.strip()):
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, "参数Interface 接口 为空!").toJson())
    elif (not method.strip()):
        return HttpResponse(ApiReturn(ApiReturn.CODE_PARAM_ERROR, "参数Method 方法 为空!").toJson())
    else:
        result = Tb2DubboInterface.objects.filter(dubboService=interface, dubboMethod=method).aggregate(
            Max("dubboParams"))
        paramx = result['dubboParams__max']
        # print(list.query)
        if result and paramx:
            paramx = paramx[:-3] + paramx[-2:]
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK, "Success", paramx).toJson())
        else:
            return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, "Failed").toJson())


# 替换字符串string中指定位置p的字符为c
def sub(string, p, c):
    new = []
    for s in string:
        new.append(s)
    new[p] = c
    return ''.join(new)
