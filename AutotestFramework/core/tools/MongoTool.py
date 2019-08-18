from pymongo import MongoClient
import traceback
from urllib.parse import quote_plus

class MongoTool(object):
    def __init__(self,host , port= 27017, username = None, password = None, dbname = None, set_name = None):
        self.dbname = dbname
        self.set_name = set_name
        try:
            '''
            uri = "mongodb://%s:%s@%s" % (quote_plus(user), quote_plus(password), host)
            client = MongoClient(uri)
            '''
            if username:
                uri = "mongodb://%s:%s@%s" % (quote_plus(username), quote_plus(password), host)
            else:
                uri = host

            self.conn = MongoClient(uri, port)

        except:
            print(traceback.format_exc())

        self.refresh_collect()

    def refresh_collect(self,dbname = None, set_name = None):
        if dbname:
            self.dbname = dbname
        if set_name:
            self.set_name = set_name
        if self.dbname:
            self.db = eval("self.conn. %s" % self.dbname)  # 连接mydb数据库，没有则自动创建
        if self.set_name:
            self.collect = eval("self.db.%s" % self.set_name)
        return self

    def insert(self,dict_or_list):
        #如果是dict插入一条，如果是list插入多条 insert和 save一样，但是insert多条插入时效率高
        return self.collect.insert(dict_or_list)

    def save(self,dict_or_list):
        #如果是dict插入一条，如果是list插入多条
        return self.collect.save(dict_or_list)

    def find(self,condition_dict = None):
        #如果是dict插入一条，如果是list插入多条
        if condition_dict:
            return self.collect.find(condition_dict)
        else:
            return self.collect.find()

    def find_to_list(self,condition_dict = None):
        #如果是dict插入一条，如果是list插入多条
        find_cursor = self.find(condition_dict)
        ret_list = []
        for tmpRes in find_cursor:
            tmpRes["_id"] = str(tmpRes["_id"])
            ret_list.append(tmpRes)
        return ret_list

    def find_one(self,condition_dict = None):
        #如果是dict插入一条，如果是list插入多条
        if condition_dict:
            return self.collect.find_one(condition_dict)
        else:
            return self.collect.find_one()

    def update(self,query_dict,update_dict,upsert = False, multi = True):
        #如果是dict插入一条，如果是list插入多条
        return self.collect.update(query_dict,update_dict,upsert = upsert, multi = multi)

    def remove(self,query_dict):
        #如果是dict插入一条，如果是list插入多条
        return self.collect.remove(query_dict)
