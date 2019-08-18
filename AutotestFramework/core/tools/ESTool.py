from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch import exceptions
import traceback
import datetime
import sys

class ESTool(object):

    def __init__(self, host='', port=3306):
        self.__open = False
        if host != '':
            self.__host = host
            self.__port = port

        self.es = Elasticsearch([{'host': self.__host, 'port': self.__port}])

    def search(self,index,type,condition):
        pass