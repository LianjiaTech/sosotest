import os

port = os.getenv("PORT", 8888)
print("port:%s" % port)

logroot = os.getenv("LOGDIR", os.path.dirname(os.path.abspath(__file__)))
print("logroot:%s" % logroot)

bind = "0.0.0.0:%s" % port  # 绑定的ip与端口
backlog = 512  # 监听队列数量，64-2048
# chdir = '/home/test/server/bin'  #gunicorn要切换到的目的工作目录

# sync
# gevent
# eventlet
# tornado
# gaiohttp
# gthread
worker_class = 'eventlet'

workers = 8  # multiprocessing.cpu_count()    #进程数
threads = 4  # multiprocessing.cpu_count()*4 #指定每个进程开启的线程数
loglevel = 'info'  # 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'

accesslog = "%s/gunicorn_access.log" % logroot
errorlog = "%s/gunicorn_error.log" % logroot
proc_name = 'sosotest-web-django'  # 进程名
