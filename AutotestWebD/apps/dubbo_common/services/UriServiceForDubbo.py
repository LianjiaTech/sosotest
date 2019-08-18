import apps.common.func.InitDjango
from apps.common.func.CommonFunc import dbModelListToListDict
from apps.config.services.businessLineService import BusinessService
from apps.config.services.modulesService import ModulesService
from apps.config.services.sourceService import SourceService
from all_models.models import TbConfigUri
from apps.common.func.CommonFunc import executeSqlGetDict
from apps.config.services.uriService import UriService

class UriServiceForDubbo(object):
    @staticmethod
    def getUri(request,protocol="DUBBO"):
        return UriService.getUri(request,protocol)

if __name__ == "__main__":
    # print((businessService.=)))
    # print(UserService.getUserByLoginname(UserService.getUsers()[0].loginname))
    # print((UriService.getUri()))


    t = "1234563789"
    str = t[t.find("3") + 1:]

    print( str[str.find("3"):str.find("9")+1])