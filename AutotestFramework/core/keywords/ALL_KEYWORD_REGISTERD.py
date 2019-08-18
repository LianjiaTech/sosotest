#新增关键字步骤:
#1/ 新家关键字类和方法.
#2/ __init__.py中引入新增的关键字类
#3/ 在关键字对应产生作用的区域加入注册.
#kw的名字的列表，与执行列表要一一对应。
import os
from core.tools.CommonFunc import *
from core.processor.SelfKeywordProcesser import SelfKeywordProcesser

mypath = os.path.dirname(os.path.abspath(__file__)).replace("\\","/")
kwKeyList = []
for root, dirs, files in os.walk(mypath):
    for tmpFile in files:
        if tmpFile.endswith("Keyword.py"):
            with open(mypath+"/"+tmpFile,encoding="utf8") as f:
                content = f.read()
            reString = "\ndef ([\s\S]*?)\("  # 取出所有的apidoc
            p = re.compile(r'%s' % reString)
            keywordList = p.findall(content)
            for tmpKeyword in keywordList:
                #如果新找到的 endswith之前存在的要报错
                kwKeyList.append(tmpKeyword)
kwKeyList = SelfKeywordProcesser.sortKwKeyList(kwKeyList)
print(kwKeyList)
print("############################################################################")
print("##################################启动完成##################################")
print("############################################################################")
print("########################    %s    #########################" % get_current_time())
print("############################################################################")
