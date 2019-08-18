#!/usr/bin/env bash
currentroot="$( cd "$( dirname "$0"  )" && pwd  )"
source $currentroot/bin.ini
if [[ $currentroot =~ $releaseSubDIR ]]
then
  echo "正式发布目录！不可使用测试脚本..."
  exit -1
else
  echo "非正式发布目录，启动测试脚本。。。"
fi

ps -ef |grep :8000 |grep manage.py |grep -v grep |awk '{print $2}' |xargs kill -9
echo "$pythonroot_test ${currentroot}/../AutotestWebD/manage.py runserver 0.0.0.0:8000  2>&1 &"
nohup $pythonroot_test ${currentroot}/../AutotestWebD/manage.py runserver 0.0.0.0:8000  2>&1 &

ps -ef |grep main.py |grep -v grep |awk '{print $2}' |xargs kill -9
ps -ef |grep run.py |grep -v grep |awk '{print $2}' |xargs kill -9
sleep 6
echo "$pythonroot_test ${currentroot}/../AutotestFramework/test_run/main.py  2>&1 &"
nohup $pythonroot_test ${currentroot}/../AutotestFramework/test_run/main.py  2>&1 &

for i in {1..30}
do
    mainstr=`ps aux|grep -v 'grep'|grep -c 'main.py'`
    echo "main.py的进程数量检测结果是：${mainstr}"
    if [ "$mainstr" = "12" ]; then
        break
    else
        #重启进程
        echo "重试中...."
        sleep 1s
    fi
done
sleep 1s
echo "$pythonroot_test ${currentroot}/../AutotestFramework/test_run/run.py  2>&1 &"
nohup $pythonroot_test ${currentroot}/../AutotestFramework/test_run/run.py  2>&1 &

$pythonroot_test ${currentroot}/../AutotestWebD/apps/scripts/refresh/refresh_python_mode_functions.py