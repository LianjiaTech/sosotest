from django.shortcuts import HttpResponse
from django.shortcuts import render

# Create your views here.
from all_models.models import TbUser
from apps.myadmin.service.UserService import UserService
from apps.common.decorator.normal_functions import sql_inject_validate
from apps.common.func.WebFunc import djangoModelToDict

def loginPage(request):
    context = {}
    context['hello'] = UserService.getUsers()[0].loginname;
    return render(request,"user/test.html",context);

def response(request):
    # a = request.POST.get("a")
    return HttpResponse(UserService.getUsers()[0].loginname)

def testsql(request):
    #不可sql注入
    loginname = request.GET.get("ln")
    return HttpResponse(str(djangoModelToDict(UserService.getUserByLoginname(loginname))))

@sql_inject_validate
def testsql2(request):
    #可以被注入
    loginname = request.GET.get("ln")
    return HttpResponse(TbUser.objects.raw("select * from tb_user where loginName='%s'" % loginname))
    # return HttpResponse("1")
