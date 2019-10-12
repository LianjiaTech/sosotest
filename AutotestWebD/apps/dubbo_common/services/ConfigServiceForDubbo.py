import apps.common.func.InitDjango
from apps.common.func.CommonFunc import dbModelListToListDict
from apps.config.services.businessLineService import BusinessService
from apps.config.services.modulesService import ModulesService
from apps.config.services.sourceService import SourceService
from all_models.models import TbConfigUri
from apps.dubbo_common.services.UriServiceForDubbo import UriServiceForDubbo
from apps.config.services.http_confService import HttpConfService
from apps.common.config import commonWebConfig
from apps.common.func.CommonFunc import  *

class ConfigServiceForDubbo(object):

    @staticmethod
    def queryHttpConfSortForDubbo(request):
        return executeSqlGetDict("SELECT  ch.httpConfKey,ch.alias  FROM tb_config_http ch LEFT JOIN (SELECT * FROM tb_user_httpconf WHERE addBy = %s ) uh on ch.httpConfKey = uh.httpConfKey WHERE ch.state = 1 AND ch.dubboRunState = 1  ORDER BY uh.conflevel is null,uh.conflevel asc , ch.modTime desc ",request.session.get("loginName"))

    @staticmethod
    def getConfigs(request):
        context = {}
        context["businessLine"] = BusinessService.getBusiness()
        context["modules"] = ModulesService.getModules()
        context["source"] = SourceService.getAllSource()
        context["uri"] = UriServiceForDubbo.getUri(request)

        return context

    @staticmethod
    def getDebugBtn(request):
        context = {}
        httpConf = ConfigServiceForDubbo.queryHttpConfSortForDubbo(request)
        httpConfList = []
        httpConfList.append([])
        if len(httpConf) <= commonWebConfig.debugBtnCount:
            for k in range(0, len(httpConf)):
                httpConfList[0].append(httpConf[k])
        else:
            for k in range(0, commonWebConfig.debugBtnCount - 1):
                httpConfList[0].append(httpConf[k])
            httpConfListSize = math.ceil(
                (len(httpConf) - (commonWebConfig.debugBtnCount - 1)) / commonWebConfig.debugBtnCount)
            for i in range(1, httpConfListSize + 1):
                httpConfList.append([])
                for j in range(i * commonWebConfig.debugBtnCount - 1,
                               i * commonWebConfig.debugBtnCount + (commonWebConfig.debugBtnCount - 1)):
                    if j >= len(httpConf):
                        break
                    httpConfList[i].append(httpConf[j])

        context["httpConfList"] = httpConfList
        context["httpConf"] = httpConf
        if len(httpConfList) > 1:
            context["httpConfListPage"] = "open"
        else:
            context["httpConfListPage"] = "close"

        return context

    @staticmethod
    def queryPeopleInterface(now_pageNum,pageNum , loginName):
        limit = ('%d,%d' % (now_pageNum * pageNum,pageNum))
        execSql = 'SELECT u.loginName , u.userName, c.count from tb_user u LEFT JOIN (SELECT addBy as loginName,COUNT(*) as count FROM tb2_dubbo_interface where state=1 GROUP BY addBy ) c on u.loginName = c.loginName WHERE u.state = 1 and c.count>0 and u.loginName != "%s" order by c.count desc LIMIT %s ;' % (loginName,limit)
        resultDict = executeSqlGetDict(execSql,[])
        return resultDict

if __name__ == "__main__":
    # print((businessService.=)))
    # print(UserService.getUserByLoginname(UserService.getUsers()[0].loginname))
    # print((UriService.getUri()))


    t = "1234563789"
    str = t[t.find("3") + 1:]

    print( str[str.find("3"):str.find("9")+1])