from apps.myadmin.service.UserPermissionService import *
from apps.common.func.CommonFunc import *
import functools

def single_add_page_permission(func):
    '''
    但数据添加页面的装饰器 主函数需使用 (request,permissionsList) 两个参数
    第二个参数在  context中context["permissionsList"] = permissionsList 直接return就好 用于页面按钮的判断
    :param func:
    :return:
    '''
    def __deco(*args):
        request = args[0]
        context = {}
        loginName = request.session.get("loginName")
        # 如果loginName为None  说明session失效 重定向到登录页面
        if not loginName:
            return render(request, "user_login/UserLogin.html")

        # 拿到本URL的全部权限
        defaultPermissionList = UserPermissionService.get_url_default_permissions(request.path)
        try:
            TbAdminUser.objects.get(loginName=loginName, state=1, superManager=1)
            context["permissionsList"] = defaultPermissionList
            return func(request, context)
        except:
            pass

        userPermissionResult,userPermission = UserPermissionService.get_user_default_permission(loginName)
        if userPermissionResult:
            userDefaultPermission = int(userPermission["defaultPermission"])
            userOtherPermission = int(userPermission["otherPermission"])
        else:
            # 如果出现异常，则说明用户账户出现问题
            context["text"] = "请求发生错误，请联系管理员检查用户账户信息"
            return render(request, "permission/page_error.html", context)

        if userDefaultPermission == 1:
            if "add" in defaultPermissionList:
                context["permissionsList"] = ["add"]
                return func(request,context)
        if userOtherPermission == 1:
            tb_url_permission_key = TbAdminInterfacePermissionRelation.objects.filter(url=request.path,permission="add",state=1)
            for index in tb_url_permission_key:
                tb_user_permission = TbUserPermissionRelation.objects.filter(loginName=loginName,permissionKey=index.permissionKey,state=1)
                if len(tb_user_permission) > 0:
                    return func(request, context)
        return render(request, "permission/not_permission.html")
    return __deco

def single_page_permission(func):
    '''
    单个页面的权限判断 例如 /interfaceTest/HTTP_operationInterface  调用函数要(request,permissionsList)使用两个参数
     context["permissionsList"] = permissionsList
     return 时直接返回就好 用于页面上按钮显示的判断
    :param func:
    :return:
    '''
    def __deco(*args):
        request = args[0]
        loginName = request.session.get("loginName")

        #如果loginName为None  说明session失效 重定向到登录页面
        if not loginName:
            return render(request, "user_login/UserLogin.html")

        #先检查url属于哪张表，然后通过id参数去查这条数据的所属人是谁
        id = request.GET.get("id",None)
        addBy = request.GET.get("addBy",None)
        option = request.GET.get("option",None)
        #没有id或者没有addBy 请求都是不规范的 页面跳转
        context = {}
        if not id:
            context["text"] = "请求发生错误，缺少参数id"
            return render(request,"permission/page_error.html",context)
        # if not addBy:
        #     context["text"] = "请求发生错误，缺少参数addBy"
        #     return render(request, "permission/page_error.html", context)
        if not option:
            context["text"] = "请求发生错误，缺少参数option"
            return render(request, "permission/page_error.html", context)

        # 拿到本URL的全部权限
        allPermissionList = UserPermissionService.get_url_all_permissions(request.path)
        try:
            TbAdminUser.objects.get(loginName=loginName,state=1,superManager=1)
            context["permissionsList"] = allPermissionList
            return func(request,context)
        except:
            pass

        #如果这条数据的创建人是自己 那么自己对数据拥有所有权限
        print("allPermissionList",allPermissionList)
        if addBy == loginName or addBy == None or addBy == "":
            context["permissionsList"] = allPermissionList
            return func(request,context)

        defaultPermissionList = UserPermissionService.get_url_default_permissions(request.path)
        #判断用户是否有默认权限（使用redis)

        userPermissionResult, userPermission = UserPermissionService.get_user_default_permission(loginName)
        if userPermissionResult:
            userDefaultPermission = int(userPermission["defaultPermission"])
            userOtherPermission = int(userPermission["otherPermission"])
        else:
            context = {}
            # 如果出现异常，则说明用户账户出现问题
            context["text"] = "请求发生错误，请联系管理员检查用户账户信息"
            return render(request, "permission/page_error.html", context)
        #用户具有默认权限
        userPermissionList = []
        if userDefaultPermission == 1:
            userPermissionList.extend(defaultPermissionList)
        if userOtherPermission == 1:
            #用户没有默认权限 就去查询用户权限关联表
            userPermissionList.append(UserPermissionService.get_user_url_all_permission(loginName,request.path))

        #如果此次请求是默认权限 直接访问
        # if option in userPermissionList:
        #     print("userPermissionList",userPermissionList)
        #     return func(request,userPermissionList)
        # else:
        #如果不是默认权限 则查询用户对此接口有哪些权限
        user_url_permissionDict = UserPermissionService.get_user_url_permissions(request.path,loginName,[addBy])
        #{"permissions": {"loginName": ["edit", "copy", "select", "delete"]}}
        #先判断自己有没有这个权限
        if option in user_url_permissionDict["permissions"][addBy]:
            context["permissionsList"] = user_url_permissionDict["permissions"][addBy]
            return func(request,context)
        else:
            #没有 告诉用户没权限
            return render(request, "permission/not_permission.html")
    return __deco

def single_data_permission(dataModel,dataVersionModel):
    '''
    单数据发生变化时的装饰器 此装饰器做最终的权限判定  参数修改强制要求以id为索引  为单接口 copy edit del时使用
    :param dataModel: 当前版本的数据表
    :param dataVersionModel: 历史版本的数据表
    :return:
    '''
    def _deco(func):
        @functools.wraps(func)
        def __deco(*agrs):
            request = agrs[0]
            loginName = request.session.get("loginName")
            dataId = request.POST.get("id",None)
            if not dataId:
                # print(222222222233)
                dataId = request.GET.get("id",None)
            # print(2222222222)

            # print(dataId)
            #查询这个接口是什么权限
            try:
                urlPermission = TbAdminInterfacePermissionRelation.objects.get(url=request.path,state=1).permission
            except:
                print(traceback.format_exc())
                return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR,message="单数据接口在权限表中只能有且为一条数据").toJson())

            #先查询用户是否有默认权限，再查询这个url是否为默认权限的url，最后查询用户是否有这个Url的权限
            userPermissionResult,userPermission = UserPermissionService.get_user_default_permission(loginName)
            if userPermissionResult:
                userDefaultPermission = int(userPermission["defaultPermission"])
                userOtherPermission = int(userPermission["otherPermission"])
            else:
                # 如果出现异常，则说明用户账户出现问题
                return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR,message="请求发生错误，请联系管理员检查用户账户信息").toJson())

            #用户有默认权限 且次接口为默认权限
            if userDefaultPermission == 1 and urlPermission in UserPermissionService.get_url_default_permissions(request.path):
                return func(request)
            #用户有特有权限 且特有权限包含此接口
            if userOtherPermission == 1 and len(UserPermissionService.get_user_url_all_permission(loginName, request.path)):
                return func(request)

            #如果是拷贝 但是用户没有添加权限
            if dataId:
                if request.session.get("version") == "CurrentVersion":
                    try:
                        data = dataModel.objects.get(id=dataId,state=1)
                    except:
                        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="数据获取失败，请联系管理员检查 %s %s" % (str(dataModel),dataId)).toJson())

                else:
                    try:
                        data = dataVersionModel.objects.get(id=dataId,state=1)
                    except:
                        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="数据获取失败，请联系管理员检查 %s %s" % (str(dataVersionModel),dataId)).toJson())

                # print(type(data.addBy))
                # print((data.addBy))
                # print(data.addBy == None)
                try:
                    if type(data.addBy) != str:
                        addBy = data.addBy.loginName
                    else:
                        addBy = data.addBy
                except:
                    addBy = ""
                userPermission = UserPermissionService.get_user_url_permissions(request.path,loginName,[addBy])
                # print("1111111111111111")
                # print(urlPermission)
                # print(userPermission["permissions"][addBy])
                if userPermission["isSuccess"]:
                    if urlPermission in userPermission["permissions"][addBy]:
                        # print(3333333333333)
                        return func(request)
                    else:
                        # print(44444444444444)
                        return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR,message="无操作权限，请联系管理员").toJson())
                else:
                    return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR, message="权限检查出错，请联系管理员").toJson())
            else:
                return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR,message="无操作权限，请联系管理员").toJson())
        return __deco
    return _deco



if __name__ == "__main__":
    print(UserPermissionService.get_user_url_permissions("/interfaceTest/HTTP_operationInterface","liyc",["wangjl01","licy"]))
