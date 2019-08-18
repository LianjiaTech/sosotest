#!/bin/bash
mysqldump -e -q --single-transaction -uroot -pingage -h127.0.0.1 -P3306 xsy_interface_test_platform > /home/AutotestPlatform/mysql_data_backup/xsy_interface_test_platform_$(date +%Y%m%d_%H%M%S).sql &&
rm -rf /home/AutotestPlatform/mysql_data_backup/xsy_interface_test_platform_$(date -d "7 days ago" +%Y%m%d)*.sql