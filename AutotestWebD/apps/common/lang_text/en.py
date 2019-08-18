import os
from apps.common.model.Config import Config

class EN(object):
    # print("#######################INTO EN######################")
    textDict = {}
    # print("#######################GET EN DICT######################")
    if len(textDict) == 0:
        # print("#######################INTO EN INIT######################")
        rootpath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
        confPath = "%s/enconf" % rootpath
        # print(confPath)
        list = os.listdir(confPath)  # 列出文件夹下所有的目录与文件
        for i in range(0, len(list)):
            path = os.path.join(confPath, list[i])
            if os.path.isfile(path):
                textDict = dict(textDict,**Config.getConfDictByFile(path))
        # print("#######################INTO EN END######################")
    @classmethod
    def updateTextDict(cls):
        # print("#######################INTO EN INIT######################")
        rootpath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
        confPath = "%s/enconf" % rootpath
        # print(confPath)
        list = os.listdir(confPath)  # 列出文件夹下所有的目录与文件
        for i in range(0, len(list)):
            path = os.path.join(confPath, list[i])
            if os.path.isfile(path):
                cls.textDict = dict(cls.textDict,**Config.getConfDictByFile(path))
        # print("#######################INTO EN END######################")

if __name__ == "__main__":
    for i in range(0,10):
        print(EN.textDict)