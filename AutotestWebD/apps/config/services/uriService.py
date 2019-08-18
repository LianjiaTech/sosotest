import apps.common.func.InitDjango
from apps.common.func.CommonFunc import dbModelListToListDict,executeSqlGetDict
from all_models.models import TbConfigUri
class UriService(object):
    @staticmethod
    def getUri(request,protocol = "HTTP"):
        if protocol == "ALL":
            return executeSqlGetDict("SELECT cu.*,u.userName FROM tb_config_uri cu LEFT JOIN (SELECT * FROM tb_user_uri WHERE addBy= %s ) uu  ON cu.uriKey = uu.uriKey LEFT JOIN tb_user u ON cu.addBy = u.loginName WHERE cu.state = 1 ORDER BY uu.confLevel IS NULL,uu.confLevel ASC ,cu.addTime desc",[request.session.get("loginName")])
        else:
            return executeSqlGetDict("SELECT cu.*,u.userName FROM tb_config_uri cu LEFT JOIN (SELECT * FROM tb_user_uri WHERE addBy= %s ) uu  ON cu.uriKey = uu.uriKey LEFT JOIN tb_user u ON cu.addBy = u.loginName WHERE cu.state = 1  AND cu.protocol = %s ORDER BY uu.confLevel IS NULL,uu.confLevel ASC ,cu.addTime desc",[request.session.get("loginName"),protocol])

if __name__ == "__main__":
    # print((businessService.=)))
    # print(UserService.getUserByLoginname(UserService.getUsers()[0].loginname))
    # print((UriService.getUri()))


    t = "1234563789"
    str = t[t.find("3") + 1:]

    print( str[str.find("3"):str.find("9")+1])