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
nohup $pythonroot_test ${currentroot}/../AutotestWebD/manage.py runserver 0.0.0.0:8000  2>&1 &