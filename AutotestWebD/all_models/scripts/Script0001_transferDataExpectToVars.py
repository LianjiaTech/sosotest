import django
import sys,os,hashlib
rootpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))).replace("\\","/")
rootpath = rootpath.split("/apps")[0]
print(rootpath)
syspath=sys.path
sys.path=[]
sys.path.append(rootpath) #指定搜索路径绝对目录
sys.path.extend([rootpath+i for i in os.listdir(rootpath) if i[0]!="."])#将工程目录下的一级目录添加到python搜索路径中
sys.path.extend(syspath)
from apps.common.func import InitDjango
from all_models.models import *
from apps.common.func.CommonFunc import *

allInterfaces = TbHttpInterface.objects.all()
for tmpInterface in allInterfaces:
    tmpInterface.varsPre = "%s[CONF=endcommon]%s[ENDCONF]" % (tmpInterface.varsPre,tmpInterface.dataInit)

    expectResults = tmpInterface.expectResult
    expectResList = splitStringToListByTag(expectResults, ";")
    assertString = ""
    for tmpAssertString in expectResList:
        if tmpAssertString.strip().startswith("EXEC_PYTHON("):
            assertString += "%s;\n" % tmpAssertString
        elif tmpAssertString.strip().startswith("{%IF "):
            tmpAssertString
            assertString += "%s;\n" % tmpAssertString
        else:
            assertString += "ASSERT(%s);\n" % tmpAssertString
    tmpInterface.varsPost = "%s[CONF=endcommon]%s%s[ENDCONF]" % (tmpInterface.varsPost,assertString,tmpInterface.dataRecover)
    tmpInterface.save(force_update=True)

