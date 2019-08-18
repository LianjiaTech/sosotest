currentroot="$( cd "$( dirname "$0"  )" && pwd  )"
source $currentroot/bin.ini
echo -e "\033[47;30;5m ##################### online shell ########################### \033[0m"
echo -e "\033[47;30;5m ##################### online shell ########################### \033[0m"
echo -e "\033[47;30;5m ##################### online shell ########################### \033[0m"
echo -e "\033[47;30;5m ##################### online shell ########################### \033[0m"
if [[ $currentroot =~ $releaseSubDIR ]]
then
  echo "正式发布目录！开始启动..."
else
  echo "非正式发布目录，请检查启动环境！"
  exit -1
fi

ps -ef |grep run.py |grep -v grep |awk '{print $2}' |xargs kill -9
sleep 6 #休眠2秒后再开始
nohup $pythonroot ${currentroot}/../AutotestFramework/test_run/run.py  2>&1 &