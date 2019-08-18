import re

def verifyPythonMode(verStr):
    if "import " in verStr:
        return False,"不允许使用import。"

    if re.match("[\d\D]*exec( *)\([\d\D]*",verStr):
        return False,"不允许执行exec。"

    if re.match("[\d\D]*eval( *)\([\d\D]*",verStr):
        return False,"不允许执行eval。"

    if ".globalDB" in verStr:
        return False,"不能使用上下文中的globalDB。"
    if ".serviceRedis" in verStr:
        return False,"不能使用上下文中的serviceRedis。"
    if ".serviceDB" in verStr:
        return False,"不能使用上下文中的serviceDB。"
    if ".serviceDBDict" in verStr:
        return False, "不能使用上下文中的serviceDBDict。"

    return True,"匹配通过"

if __name__=="__main__":
    ver = """asdf
    eval( sdf
    fdeval("""
    retB,retS = verifyPythonMode(ver)
    print(retS)