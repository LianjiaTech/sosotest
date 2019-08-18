from core.tools.DBTool import DBTool
class SelfKeywordProcesser(object):

    @staticmethod
    def sortKwKeyList(kwKeyList):
        def changListValue(chList,keyI,keyJ):
            tmpValue = chList[keyI]
            chList[keyI] = chList[keyJ]
            chList[keyJ] = tmpValue

        for i in range(0,len(kwKeyList)):
            tmpKwKey = kwKeyList[i]
            changI = i
            for j in range(i-1,-1,-1):
                existKwKey = kwKeyList[j]
                changJ = j
                if tmpKwKey.endswith(existKwKey):
                    changListValue(kwKeyList,changI,changJ)
                    changI = j
        return kwKeyList

    @staticmethod
    def getSelfKeywordDict():
        selfKwList = []
        selfKwDict = {}
        db = DBTool().initGlobalDBConf()
        kwDictList = db.execute_sql("SELECT keywordKey,keywordCode FROM tb4_data_keyword WHERE status = 3 AND state =1 AND type='DATA_KEYWORD' ORDER BY id")
        for tmpDict in kwDictList:
            selfKwList.append(tmpDict['keywordKey'])
            selfKwDict[tmpDict['keywordKey']] = tmpDict['keywordCode']

        selfKwList = SelfKeywordProcesser.sortKwKeyList(selfKwList)
        db.release()
        return selfKwList,selfKwDict


if __name__ == "__main__":
    kwList = ["BA","EE","CBA","D","A"]
    print(kwList)
    kwList2 = SelfKeywordProcesser.sortKwKeyList(kwList)
    print(kwList)
    print(kwList2)
    print("###########################")
    kwList = ["BA","EE","A","D","CBA"]
    print(kwList)
    kwList2 = SelfKeywordProcesser.sortKwKeyList(kwList)
    print(kwList)
    print(kwList2)
    print("###########################")
    kwList = ["CBA","EE","BA","D","A"]
    print(kwList)
    kwList2 = SelfKeywordProcesser.sortKwKeyList(kwList)
    print(kwList)
    print(kwList2)
    print("###########################")
    kwList = ["CBA","EE","A","D","BA"]
    print(kwList)
    kwList2 = SelfKeywordProcesser.sortKwKeyList(kwList)
    print(kwList)
    print(kwList2)
    print("###########################")
    kwList = ["A","EE","BA","D","CBA"]
    print(kwList)
    kwList2 = SelfKeywordProcesser.sortKwKeyList(kwList)
    print(kwList)
    print(kwList2)
    print("###########################")
    kwList = ["A","EE","CBA","D","BA"]
    print(kwList)
    kwList2 = SelfKeywordProcesser.sortKwKeyList(kwList)
    print(kwList)
    print(kwList2)
    print("###########################")
    retList,retDict = SelfKeywordProcesser.getSelfKeywordDict()
    print(retList)
    print(retDict)