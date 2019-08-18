from pymemcache.client.base import Client

class MemcacheTool(object):

    def __init__(self,host,port):
        self.client = Client((host, port))

    def set(self,key,value):
        self.client.set(key, value)

    def get(self,key):
        return self.client.get(key)

if __name__ == '__main__':
    rt = MemcacheTool("192.168.0.75",11211)
    rt.set("testabc","abc")
    print(rt.get("testabc"))
    rt = MemcacheTool("192.168.0.75",11212)
    rt.set("testabc","abc2")
    print(rt.get("testabc"))
    rt = MemcacheTool("192.168.0.75",11213)
    rt.set("testabc","abc3")
    print(rt.get("testabc"))


