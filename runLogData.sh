#!/bin/sh

DATE=`date "+%m-%d"`
/home/pi/logData/logScripts/parseData.sh /var/log/auth.log.1 /home/pi/logData/fail$DATE.log
python /home/pi/logData/logScripts/logData.py /home/pi/logData/fail$DATE.log
gzip /home/pi/logData/fail$DATE.log
mv /home/pi/logData/fail$DATE.log.gz /home/pi/logData/oldLogs
