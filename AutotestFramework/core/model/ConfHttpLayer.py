from core.const.GlobalConst import HttpKey
from core.decorator.normal_functions import *
from core.model.ConfServiceLayer import ConfServiceLayer
from core.tools.DBTool import DBTool
from core.processor.Config import Config

class ConfHttpLayer(object):
    """
    Http配置的类。
    """

    def __init__(self):
        self.id = 0
        self.key = HttpKey.NO_KEY
        self.alias = ''
        self.desc = ''

        self.confDict = {}
        #-------------------------
        self.confServiceLayer = ConfServiceLayer()
        #-------------------------
        self.addBy = ''
        self.modBy = ''
        self.addTime = ''
        self.modTime = ''
        self.state = 1

    @take_time
    @catch_exception
    def generate_http_conf_by_key(self):
        """
        通过key从数据库获取配置的信息。
        Returns:执行结果

        """
        db = DBTool().initGlobalDBConf()
        colstr = "id, httpConfKey, serviceConfKey, alias, httpConfDesc, state, addBy, modBy, addTime, modTime"
        sql = """ SELECT %s FROM tb_config_http where httpConfKey = '%s' """ % (colstr,self.key)
        res = db.execute_sql(sql,auto_release=True)
        db.release()
        if res:
            tmpConf = res[0]
            self.id = tmpConf['id']
            self.alias = tmpConf['alias']
            self.desc = tmpConf['httpConfDesc']
            self.state = tmpConf['state']
            self.addBy = tmpConf['addBy']
            self.modBy = tmpConf['modBy']
            self.addTime = tmpConf['addTime']
            self.modTime = tmpConf['modTime']

            # httpConfStr = tmpConf['httpConf']
            # self.confDict = Config().getConfDictByString(httpConfStr)
            self.confServiceLayer.key = tmpConf['serviceConfKey']
            return self.confServiceLayer.generate_service_conf_by_key()
        else:
            return False

if __name__ == '__main__':
    chl = ConfHttpLayer()
    chl.key = "httpConfTest01"
    if chl.generate_http_conf_by_key():
        print ("pass")
        print(chl.xsy_domain)
        print(chl.confServiceLayer.dbPassword)
    else:
        print ("fail")



