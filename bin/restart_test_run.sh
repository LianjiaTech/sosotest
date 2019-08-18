currentroot="$( cd "$( dirname "$0"  )" && pwd  )"
source $currentroot/bin.ini
if [[ $currentroot =~ $releaseSubDIR ]]
then
  echo "正式发布目录！不可使用测试脚本..."
  exit -1
else
  echo "非正式发布目录，启动测试脚本。。。"
fi
ps -ef |grep run.py |grep -v grep |awk '{print $2}' |xargs kill -9
sleep 6
nohup $pythonroot_test ${currentroot}/../AutotestFramework/test_run/run.py  2>&1 &
$pythonroot_test ${currentroot}/../AutotestWebD/apps/scripts/refresh/refresh_python_mode_functions.py