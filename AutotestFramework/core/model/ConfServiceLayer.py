from core.const.GlobalConst import ServiceKey
from core.decorator.normal_functions import *
from core.tools.DBTool import DBTool
from core.processor.Config import Config

class ConfServiceLayer(object):
    """
    Service配置类，配置数据服务的相关信息。
    """

    def __init__(self):
        self.id = 0
        self.key = ServiceKey.NO_KEY
        self.alias = ''
        self.desc = ''

        self.confDict = {}

        #-------------------------
        self.addBy = ''
        self.modBy = ''
        self.addTime = ''
        self.modTime = ''
        self.state = 1

    @take_time
    @catch_exception
    def generate_service_conf_by_key(self):
        """
        通过key从数据库获取对应的service配置信息。
        Returns:执行结果，True False

        """
        clostr = "id, serviceConfKey, alias, serviceConfDesc, serviceConf, state, addBy, modBy, addTime, modTime"
        sql = """select %s from tb_config_service where serviceConfKey = '%s'""" % (clostr,self.key)
        db = DBTool().initGlobalDBConf()
        res = db.execute_sql(sql,auto_release=True)
        db.release()
        if res:
            tmpConf = res[0]
            self.id = tmpConf['id']
            self.key = tmpConf['serviceConfKey']
            self.alias = tmpConf['alias']
            self.desc = tmpConf['serviceConfDesc']
            self.state = tmpConf['state']
            self.addBy = tmpConf['addBy']
            self.modBy = tmpConf['modBy']
            self.addTime = tmpConf['addTime']
            self.modTime = tmpConf['modTime']

            serviceConfStr = tmpConf['serviceConf']
            # self.confDict = Config().getConfDictByString(serviceConfStr)
            self.confDict = json.loads(serviceConfStr)
            return True
        else:
            return False
