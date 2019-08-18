import os
from apps.common.model.Config import Config

class CN(object):
    # print("#######################INTO CN######################")
    textDict = {}
    # print("#######################GET CN DICT######################")
    if len(textDict) == 0:
        # print("#######################INTO CN INIT######################")
        rootpath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
        confPath = "%s/cnconf" % rootpath
        # print(confPath)
        list = os.listdir(confPath)  # 列出文件夹下所有的目录与文件
        for i in range(0, len(list)):
            path = os.path.join(confPath, list[i])
            if os.path.isfile(path):
                textDict = dict(textDict,**Config.getConfDictByFile(path))
        # print("#######################INTO CN END######################")
    @classmethod
    def updateTextDict(cls):
        # print("#######################INTO EN INIT######################")
        rootpath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
        confPath = "%s/cnconf" % rootpath
        # print(confPath)
        list = os.listdir(confPath)  # 列出文件夹下所有的目录与文件
        for i in range(0, len(list)):
            path = os.path.join(confPath, list[i])
            if os.path.isfile(path):
                cls.textDict = dict(cls.textDict,**Config.getConfDictByFile(path))
        # print("#######################INTO EN END######################")

if __name__ == "__main__":
    for i in range(0,10):
        rootpath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
        confPath = "%s/cnconf" % rootpath
        # print(confPath)
        list = os.listdir(confPath)  # 列出文件夹下所有的目录与文件
        for i in range(0, len(list)):
            path = os.path.join(confPath, list[i])
            if os.path.isfile(path):
                print(Config.getConfDictByFile(path))