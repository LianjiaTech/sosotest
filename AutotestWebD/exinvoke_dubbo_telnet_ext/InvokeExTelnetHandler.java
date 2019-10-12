package com.alibaba.dubbo.rpc.protocol.dubbo.telnet;

import java.lang.reflect.Method;
import java.util.Collection;
import java.util.List;
import java.util.Map;

import com.alibaba.dubbo.common.extension.Activate;
import com.alibaba.dubbo.common.json.JSON;
import com.alibaba.dubbo.common.utils.PojoUtils;
import com.alibaba.dubbo.common.utils.ReflectUtils;
import com.alibaba.dubbo.common.utils.StringUtils;
import com.alibaba.dubbo.remoting.Channel;
import com.alibaba.dubbo.remoting.telnet.TelnetHandler;
import com.alibaba.dubbo.remoting.telnet.support.Help;
import com.alibaba.dubbo.rpc.Exporter;
import com.alibaba.dubbo.rpc.Invoker;
import com.alibaba.dubbo.rpc.RpcContext;
import com.alibaba.dubbo.rpc.RpcInvocation;
import com.alibaba.dubbo.rpc.protocol.dubbo.DubboProtocol;

@Activate
@Help(parameter = "{'service': '', 'method': '', 'args': [], 'attachments':{}}", summary = "Invoke the service method.", detail = "Invoke the service method.")
public class InvokeExTelnetHandler implements TelnetHandler {

    @SuppressWarnings("unchecked")
    public String telnet(Channel channel, String message) {
        if (message == null || message.length() == 0) {
            return "Please input method name, eg: \r\ninvokeEx {'service': 'xxx', 'method': 'xxx', 'args': [1,2,3], 'attachments':{}}";
        }
        if (message.length() > 1024) {
            return "input parameters length more then 1024!";
        }
        int idx = message.indexOf('{');
        String body = message.substring(idx);
        try {
            Body b = JSON.parse(body, Body.class);
            return invoke(channel, b.getService(), b.getMethod(), b.getArgs(), b.getAttachments());
        } catch (Throwable t) {
            return "failed to execute, " + t.getMessage();
        }
    }

    protected String invoke(Channel channel, String service, String method, List args, Map attachments) {
        StringBuilder buf = new StringBuilder();
        Invoker<?> invoker = null;
        Method invokeMethod = null;
        for (Exporter<?> exporter : DubboProtocol.getDubboProtocol().getExporters()) {
            if (service == null || service.length() == 0) {
                invokeMethod = findMethod(exporter, method, args);
                if (invokeMethod != null) {
                    invoker = exporter.getInvoker();
                    break;
                }
            } else {
                if (service.equals(exporter.getInvoker().getInterface().getSimpleName())
                                || service.equals(exporter.getInvoker().getInterface().getName())
                                || service.equals(exporter.getInvoker().getUrl().getPath())) {
                    invokeMethod = findMethod(exporter, method, args);
                    invoker = exporter.getInvoker();
                    break;
                }
            }
        }
        if (invoker != null) {
            if (invokeMethod != null) {
                try {
                    RpcContext.getContext().getAttachments().putAll(attachments);
                    Object[] array = PojoUtils.realize(args.toArray(), invokeMethod.getParameterTypes(), invokeMethod.getGenericParameterTypes());
                    RpcContext.getContext().setLocalAddress(channel.getLocalAddress()).setRemoteAddress(channel.getRemoteAddress());
                    long start = System.currentTimeMillis();
                    RpcInvocation invocation = new RpcInvocation(invokeMethod, array);
                    invocation.setAttachments(attachments);
                    Object result = invoker.invoke(invocation).recreate();
                    long end = System.currentTimeMillis();
                    buf.append( JsonUtil.toJson(result));
                    buf.append("\r\nelapsed: ");
                    buf.append(end - start);
                    buf.append(" ms.");
                } catch (Throwable t) {
                    return "Failed to invoke method " + invokeMethod.getName() + ", cause: " + StringUtils.toString(t);
                }
            } else {
                buf.append("No such method " + method + " in service " + service);
            }
        } else {
            buf.append("No such service " + service);
        }
        return buf.toString();
    }

    private static Method findMethod(Exporter<?> exporter, String method, List<Object> args) {
        Invoker<?> invoker = exporter.getInvoker();
        Method[] methods = invoker.getInterface().getMethods();
        Method invokeMethod = null;
        for (Method m : methods) {
            if (m.getName().equals(method) && m.getParameterTypes().length == args.size()) {
                if (invokeMethod != null) { // 重载
                    if (isMatch(m.getParameterTypes(), args)) {
                        invokeMethod = m;
                        break;
                    }
                } else {
                    invokeMethod = m;
                }
                invoker = exporter.getInvoker();
            }
            if (m.getName().equals(method) && isMatch(m.getParameterTypes(), args)) {
                return m;
            }
        }
        return invokeMethod;
    }

    private static boolean isMatch(Class<?>[] types, List<Object> args) {
        if (types.length != args.size()) {
            return false;
        }
        for (int i = 0; i < types.length; i++) {
            Class<?> type = types[i];
            Object arg = args.get(i);
            if (ReflectUtils.isPrimitive(arg.getClass())) {
                if (!ReflectUtils.isPrimitive(type)) {
                    return false;
                }
            } else if (arg instanceof Map) {
                String name = (String) ((Map<?, ?>) arg).get("class");
                Class<?> cls = arg.getClass();
                if (name != null && name.length() > 0) {
                    cls = ReflectUtils.forName(name);
                }
                if (!type.isAssignableFrom(cls)) {
                    return false;
                }
            } else if (arg instanceof Collection) {
                if (!type.isArray() && !type.isAssignableFrom(arg.getClass())) {
                    return false;
                }
            } else {
                if (!type.isAssignableFrom(arg.getClass())) {
                    return false;
                }
            }
        }
        return true;
    }

    public static class Body {
        private String service;
        private String method;
        private List<Object> args;
        private Map<String, String> attachments;

        public String getService() {
            return service;
        }

        public void setService(String service) {
            this.service = service;
        }

        public String getMethod() {
            return method;
        }

        public void setMethod(String method) {
            this.method = method;
        }

        public List getArgs() {
            return args;
        }

        public void setArgs(List args) {
            this.args = args;
        }

        public Map getAttachments() {
            return attachments;
        }

        public void setAttachments(Map attachments) {
            this.attachments = attachments;
        }

    }

}
