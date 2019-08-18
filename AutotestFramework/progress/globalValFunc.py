def getGlobalQueueVal(lock,globalValQueue):
    lock.acquire()
    try:
        globalVal = globalValQueue.get()
        globalValQueue.put(globalVal)
        return globalVal
    finally:
        lock.release()

def setGlobalQueueVal(lock,globalValQueue,globalValData):
    lock.acquire()
    try:
        globalValQueue.get()
        globalValQueue.put(globalValData)
    finally:
        lock.release()