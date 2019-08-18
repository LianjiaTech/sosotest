import apps.common.func.InitDjango
from apps.common.func.CommonFunc import dbModelListToListDict,tupleToDict,executeSqlGetDict
from all_models.models import TbConfigHttp


class HttpConfService(object):
    @staticmethod
    def getHttpConf():
        return dbModelListToListDict(TbConfigHttp.objects.all())

    @staticmethod
    def getHttpConfForUI():
        return dbModelListToListDict(TbConfigHttp.objects.filter(uiRunState = 1))

    @staticmethod
    def getHttpConfForId(id):
        return TbConfigHttp.objects.filter(id=id)[0]


    @staticmethod
    def getServiceIncludHttpConf(serviceConfKey):
        return tupleToDict(TbConfigHttp.objects.filter(serviceConfKey=serviceConfKey).values_list("alias"),["alias"])

    @staticmethod
    def queryHttpConfSort(request):
        return executeSqlGetDict("SELECT  ch.httpConfKey,ch.alias  FROM tb_config_http ch LEFT JOIN (SELECT * FROM tb_user_httpconf WHERE addBy = %s ) uh on ch.httpConfKey = uh.httpConfKey WHERE ch.state = 1 AND ch.apiRunState = 1  ORDER BY uh.conflevel is null,uh.conflevel asc , ch.modTime desc ",request.session.get("loginName"))

    @staticmethod
    def queryUIRunHttpConfSort(request):
        return executeSqlGetDict("SELECT  ch.httpConfKey,ch.alias  FROM tb_config_http ch LEFT JOIN (SELECT * FROM tb_user_httpconf WHERE addBy = %s ) uh on ch.httpConfKey = uh.httpConfKey WHERE ch.state = 1 AND ch.uiRunState = 1 ORDER BY uh.conflevel is null,uh.conflevel asc , ch.modTime desc ",request.session.get("loginName"))

    @staticmethod
    def httpConfAdd(data):
        return TbConfigHttp.objects.create(**data)

    @staticmethod
    def httpConfDel(id):
        return TbConfigHttp.objects.filter(id=id).delete()

    @staticmethod
    def httpConfEdit(data):
        result = TbConfigHttp.objects.filter(id=data["id"]).update(**data)
        return result

    @staticmethod
    def getAllHttpConf(request):
        return executeSqlGetDict(
            "SELECT  ch.httpConfKey,ch.alias,ch.httpConfDesc  FROM tb_config_http ch LEFT JOIN "
            "(SELECT * FROM tb_user_httpconf WHERE addBy = %s ) uh on ch.httpConfKey = uh.httpConfKey "
            "WHERE ch.state = 1  ORDER BY uh.conflevel is null,uh.conflevel asc , ch.modTime desc ",
            request.session.get("loginName"))

if __name__ == "__main__":
    # print((businessService.=)))
    # print(UserService.getUserByLoginname(UserService.getUsers()[0].loginname))
    print(HttpConfService.httpConfDel("123213"))