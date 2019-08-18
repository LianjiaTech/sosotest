# coding:utf-8
"""
Author:王吉亮
Date:20161027
Desc:配置文件转换类，将.conf的配置文件转换为dict
"""
import configparser
from apps.common.decorator.normal_functions import *

#!/usr/bin/python
class MyConfig(configparser.ConfigParser):
    def __init__(self,defaults=None):
        configparser.ConfigParser.__init__(self,defaults=None)
    def optionxform(self, optionstr):
        return optionstr

class Config(object):
    """
    配置文件处理类，传入配置文件，生成配置dict。
    """

    @staticmethod
    @catch_exception
    def getConfDictByFile(confFile,encodeing = "utf-8"):
        cf = MyConfig()
        cf.read(confFile,encoding=encodeing)
        conf_dict = {}
        sections = cf.sections()
        for section in sections:
            items = cf.items(section)
            conf_dict[section] = {}
            for item in items:
                conf_dict[section][item[0]] = item[1]
        return conf_dict

    @staticmethod
    @catch_exception
    def getConfDictByString(confStr,caseSensitive = False):
        if caseSensitive :
            # cf = configparser.ConfigParser()
            cf = MyConfig()

        else:
            cf = configparser.ConfigParser()
            # cf = MyConfig()
        cf.read_string(confStr)
        conf_dict = {}
        sections = cf.sections()
        for section in sections:
            items = cf.items(section)
            conf_dict[section] = {}
            for item in items:
                conf_dict[section][item[0]] = item[1]
        return conf_dict



if __name__ == "__main__":
    pass

