# ########################全局变量#####################################################
from multiprocessing import Queue

debugThreadDict = {} # 哪些调试线程在执行，key是username，value是正在调试的debugId
# serviceThreadDict = {"AliveThreadCount":0}
# debugQueue = []
# taskQueue = []
# taskCancelQueue = []
# taskClusterQueueList = [] #当前队列的task  # isCluster 值 0：未执行，1，执行TCP发送，2，执行TCP返回，3.执行完毕，4.取消TCP发送，5取消TCP返回
# taskClusterCancelQueue = []

#main中使用的进程队列
# debugQueue = Queue()
# taskQueue = Queue()
# serviceListQueue = Queue()
# taskCancelQueue = Queue()


#run中使用的进程队列
# serviceProgressDict = {"AliveProgressCount":0}
# runTaskQueue = Queue()
# runTaskCancelQueue = Queue()
# serviceProgressDict = {"AliveProgressCount":0}



isCluster = "isCluster"






# ######################################################################################