currentroot="$( cd "$( dirname "$0"  )" && pwd  )"
source $currentroot/bin.ini
if [[ $currentroot =~ $releaseSubDIR ]]
then
    echo -e "\033[47;30;5m ##################### online shell ########################### \033[0m"
    echo -e "\033[47;30;5m ##################### online shell ########################### \033[0m"
    echo -e "\033[47;30;5m ##################### online shell ########################### \033[0m"
    echo -e "\033[47;30;5m ##################### online shell ########################### \033[0m"
    echo "正式发布目录！开始启动..."
    sh $currentroot/restart-AutotestWebD-uwsgi-release.sh
    sh $currentroot/restart-release-main-run.sh
    sh $currentroot/refresh_python_mode_functions.sh
    sh $currentroot/restart-ui_run.sh
else
    echo "非正式发布目录，请检查启动环境！"
fi


