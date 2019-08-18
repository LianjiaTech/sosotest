import redis,logging
from AutotestWebD.settings import *
logger = logging.getLogger('django')
def operator_status(func):
    '''get operatoration status
    '''

    def gen_status(*args, **kwargs):
        error, result = None, None
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            error = str(e)
            raise ValueError("redis 未找到对应的key")
        return result

    return gen_status


class RedisCache(object):
    def __init__(self):
        if not hasattr(RedisCache, 'pool'):
            RedisCache.create_pool()
        self._connection = redis.Redis(connection_pool=RedisCache.pool)

    @staticmethod
    def create_pool():
        RedisCache.pool = redis.ConnectionPool(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PWD)

    @operator_status
    def set_data(self, key, value, expireTime=None):
        '''set data with (key, value)
        '''
        return self._connection.set(key, value, ex=expireTime)

    @operator_status
    def get_data(self, key):
        '''get data by key
        '''
        return str(self._connection.get(key),encoding="utf-8")

    @operator_status
    def del_data(self, key):
        '''delete cache by key
        '''
        return self._connection.delete(key)

    @operator_status
    def flushall(self):
        '''flush cache by key
        '''
        return self._connection.flushall()

    @operator_status
    def getAllDatas(self):
        '''get cache datas
        '''
        keysList = self._connection.keys()
        valuesList = self._connection.mget(keysList)

        return keysList, valuesList
        # return self._connection.flushall(key)

    @operator_status
    def expire_data(self,key,time):
        '''
        设置某个key值的超时时间
        :param key:redis的key值
        :param time: 设置的超时时间 int类型
        :return:
        '''
        return self._connection.expire(key,time)

    def existsKey(self,key):
        '''
        设置某个key值的超时时间
        :param key:redis的key值
        :param time: 设置的超时时间 int类型
        :return:
        '''
        return self._connection.exists(key)

if __name__ == "__main__":
    # print (RedisCache().set_data('Testkey', "Simple Test"))
    # print (RedisCache().get_data('Testkey'))
    RedisCache().getAllDatas()