import apps.common.func.InitDjango
from apps.common.func.CommonFunc import dbModelListToListDict,executeSqlGetDict
from all_models.models import TbConfigService
class ServiceConfService(object):
    @staticmethod
    def getServiceConf():
        return dbModelListToListDict(TbConfigService.objects.filter(state=1))

    @staticmethod
    def queryServiceConfSort(request):
        return executeSqlGetDict("SELECT * from tb_config_service s LEFT JOIN (select * from ( SELECT id ucid,httpConfKey uhck,confLevel from tb_user_httpconf where addBy= %s ) b LEFT JOIN (SELECT id hid,serviceConfKey hsk,httpConfKey hck from tb_config_http) a on b.uhck = a.hck) c on s.serviceConfKey = c.hsk where s.state = 1 group by s.serviceConfKey  order by c.confLevel is null,c.confLevel ASC",[request.session.get("loginName")])



if __name__ == "__main__":
    # print((businessService.=)))
    # print(UserService.getUserByLoginname(UserService.getUsers()[0].loginname))

    # print(ServiceConfService.queryServiceConfSort())


    print(executeSqlGetDict("SELECT * from tb_config_service s LEFT JOIN (select * from ( SELECT id ucid,httpConfKey uhck,confLevel from tb_user_httpconf where addBy= %s ) b LEFT JOIN (SELECT id hid,serviceConfKey hsk,httpConfKey hck from tb_config_http) a on b.uhck = a.hck) c on s.serviceConfKey = c.hsk where s.state = 1 group by s.serviceConfKey  order by c.confLevel is null,c.confLevel ASC",["liyc"]))