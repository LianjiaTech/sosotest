#!/bin/sh
currentroot="$( cd "$( dirname "$0"  )" && pwd  )"
source $currentroot/bin.ini
$pythonroot ${currentroot}/../RobotUiTest/test_run/GenerateCurrentKeywords.py &&  rm -rf ${currentroot}/../AutotestWebD/static/littletool/keyword.html && cp -rf keyword.html ${currentroot}/../AutotestWebD/static/littletool/keyword.html && rm -rf keyword.html
echo "Auto generate UI keyword.html FINISHED！"