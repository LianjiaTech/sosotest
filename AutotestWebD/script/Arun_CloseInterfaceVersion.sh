#!/bin/sh
/etc/init.d/nginx stop
python3 /opt/ATPlatform/release/AutotestPlatform/AutotestWebD/apps/version_manage/scripts/start_close_version.py
/etc/init.d/nginx start