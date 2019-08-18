#!/bin/bash
mysqldump -e -q --single-transaction -uroot -pingage xsy_interface_test_platform > /opt/ATPlatform/mysql_data_backup/xsy_interface_test_platform_$(date +%Y%m%d_%H%M%S).sql &&
rm -rf /opt/ATPlatform/mysql_data_backup/xsy_interface_test_platform_$(date -d "7 days ago" +%Y%m%d)*.sql