若要支持dubbo的附件类型的方式，也就是exinvoke的方式，需要修改dubbo包，加入exinvoke扩展。

1、
src\main\resources\META-INF\dubbo\internal\com.alibaba.dubbo.remoting.telnet.TelnetHandler
加入
exinvoke=com.alibaba.dubbo.rpc.protocol.dubbo.telnet.InvokeExTelnetHandler

2、将 InvokeExTelnetHandler.java 放入到对应的包中。

3、重新编译打包dubbo包，然后供被测服务使用。
