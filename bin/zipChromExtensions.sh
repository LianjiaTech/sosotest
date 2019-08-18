currentroot="$( cd "$( dirname "$0"  )" && pwd  )"
source $currentroot/bin.ini
cd ${currentroot}/../AutotestWebD && rm -rf sosotest-chrome-extension.zip && rm -rf static/soso_extensions/sosotest-chrome-extension.zip && zip -r sosotest-chrome-extension.zip sosotest-chrome-extension && mv sosotest-chrome-extension.zip static/soso_extensions/sosotest-chrome-extension.zip