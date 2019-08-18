# from urllib import parse
#
# # Create your views here.
# from all_models.models import *
# from apps.common.config import commonWebConfig
# from apps.common.func.WebFunc import *
# # from apps.myadmin.service.InterfaceModuleService import InterfaceModuleService
# from Redis.config.RedisDBConfig import RedisCache
#
# logger = logging.getLogger("django")
#
# def interfaceModuleCheckPage(request):
#     context = {}
#     context["interfaceModule_check"] = "active"
#     return render(request, "myadmin/interfaceModule/admin_interfaceModule_check.html",context)
#
# def getInterfaceModule(request):
#     checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
#     orderBy = request.POST.get("orderBy","")
#     page = request.POST.get("page")
#     if isInt(page):
#         page = int(page)
#     else:
#         addUserLog(request, "单接口管理->查看用例->获取数据->页面参数不合法", "FAIL")
#         return HttpResponse("<script>alert('请验证页数参数');</script>")
#     execSql = "SELECT u.* from tb_admin_interface_module_relation u WHERE 1=1 "
#     checkList = []
#     for key in checkArr:
#         if checkArr[key] == "":
#             continue
#         checkList.append("%%%s%%" % checkArr[key])
#         execSql += """ and u.%s """ % key
#         execSql += """ LIKE %s"""
#     execSql += """ ORDER BY %s""" % orderBy
#     context = pagination(sqlStr=execSql,attrList=checkList,page=page,pageNum=commonWebConfig.userPageNum)
#     response = render(request, "myadmin/interfaceModule/subPages/interfaceModule_sub_page.html",context)
#     return response
#
# def getInterfaceModuleForId(request):
#     interfaceModuleId = request.POST.get("interfaceModuleId")
#     try:
#         interfaceModuleData = TbAdminInterfaceModuleRelation.objects.get(id=interfaceModuleId)
#         requestDict = dbModelToDict(interfaceModuleData)
#     except Exception as e:
#         message = "查询接口页面出错 %s" % e
#         logger.error(message)
#         return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())
#     return HttpResponse(ApiReturn(body=requestDict).toJson())
#
#
# def addInterfaceModule(request):
#     interfaceModuleRequest = json.loads(request.POST.get("interfaceModuleData"))
#     logger.info("addBusinessLine %s" % request.POST.get("interfaceModuleData"))
#     interfaceModuleRequest["addTime"] = datetime.datetime.now()
#     moduleName = interfaceModuleRequest["moduleName"]
#     searchResult = TbAdminInterfaceModuleRelation.objects.filter(url=interfaceModuleRequest["url"], moduleName=interfaceModuleRequest["moduleName"])
#
#     try:
#         if interfaceModuleRequest["url"].startswith("/"):
#             if len(searchResult) == 0:
#                 moduleName = interfaceModuleRequest["moduleName"]
#                 result = TbAdminInterfaceModuleRelation()
#                 result.url = interfaceModuleRequest["url"]
#                 result.moduleName = moduleName
#                 result.save()
#                 if result:
#                     logger.info("addInterfaceModule 接口页面添加成功 %s" % result)
#                 try:
#                     RedisCache().del_data("%s_interfaceList" % moduleName)
#                 except ValueError:
#                     pass
#                 permissionList = []
#                 interfaceModuleList = TbAdminInterfaceModuleRelation.objects.filter(moduleName=moduleName, state=1)
#                 for interfaceModule in interfaceModuleList:
#                     interfacePermissionsList = TbAdminInterfacePermissionRelation.objects.filter(url=interfaceModule.url, state=1)
#                     for permission in interfacePermissionsList:
#                         if permission.permissionKey not in permissionList:
#                             permissionList.append(permission.permissionKey)
#                 try:
#                     RedisCache().set_data("%s_interfaceList" % moduleName, json.dumps(permissionList), 60*60*24*15)
#                 except ValueError:
#                     pass
#                 return HttpResponse(ApiReturn().toJson())
#             else:
#                 if searchResult.state == 0:
#                     searchResult.state = 1
#                     InterfaceModuleService.updateInterfaceModule(dbModelToDict(searchResult))
#                     try:
#                         RedisCache().del_data("%s_interfaceList" % moduleName)
#                     except ValueError:
#                         pass
#                     permissionList = []
#                     interfaceModuleList = TbAdminInterfaceModuleRelation.objects.filter(moduleName=moduleName, state=1)
#                     for interfaceModule in interfaceModuleList:
#                         interfacePermissionsList = TbAdminInterfacePermissionRelation.objects.filter(
#                             url=interfaceModule.url, state=1)
#                         for permission in interfacePermissionsList:
#                             if permission.permissionKey not in permissionList:
#                                 permissionList.append(permission.permissionKey)
#                     try:
#                         RedisCache().set_data("%s_interfaceList" % moduleName, json.dumps(permissionList),60 * 60 * 24 * 15)
#                     except ValueError:
#                         pass
#                     return HttpResponse(ApiReturn().toJson())
#                 else:
#                     logger.info("addInterfaceModule 接口页面创建失败")
#                     return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="接口页面创建失败,请检查账号是否重复").toJson())
#         else:
#             logger.info("addInterfaceModule 接口页面创建失败,url必须以/开头")
#             return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="url必须以/开头").toJson())
#     except Exception as e:
#         message = "添加接口页面失败 :%s" % e
#         logger.info(message)
#         return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="接口页面创建失败,请检查账号是否重复").toJson())
#
#
# def editInterfaceModule(request):
#     try:
#         requestDict = json.loads(request.POST.get("interfaceModuleData"))
#         if requestDict["url"].startswith("/"):
#             InterfaceModuleService.updateInterfaceModule(requestDict)
#         else:
#             logger.info("editInterfaceModule 接口页面编辑失败,url必须以/开头")
#             return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="url必须以/开头").toJson())
#     except Exception as e:
#         print(traceback.format_exc())
#         message = "编辑接口页面发生异常 %s" % e
#         logger.info(message)
#         return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())
#
#     return HttpResponse(ApiReturn().toJson())
#
# def delInterfaceModule(request):
#     interfaceModuleId = request.POST.get("interfaceModuleId","")
#     if not interfaceModuleId:
#         return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="interfaceModuleId参数错误").toJson())
#     try:
#         interfaceModuleData = TbAdminInterfaceModuleRelation.objects.get(state=1, id=interfaceModuleId)
#     except Exception as e:
#         return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="interfaceModuleId查询错误 %s" % e).toJson())
#     interfaceModuleData.state = 0
#     interfaceModuleData.save()
#     RedisCache().del_data("moduleName_%s" % interfaceModuleData.moduleName)
#
#     return HttpResponse(ApiReturn().toJson())
#
# def resetInterfaceModule(request):
#     interfaceModuleId = request.POST.get("interfaceModuleId","")
#     if not interfaceModuleId:
#         return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="interfaceModuleId参数错误").toJson())
#     try:
#         interfaceModuleData = TbAdminInterfaceModuleRelation.objects.get(state=0, id=interfaceModuleId)
#     except Exception as e:
#         return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="interfaceModuleId查询错误 %s" % e).toJson())
#     interfaceModuleData.state = 1
#     interfaceModuleData.save()
#
#     return HttpResponse(ApiReturn().toJson())
