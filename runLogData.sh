#!/bin/sh

#############################################################################################
# runLogData.sh
# argument: path to the log file ex ./runLogData.sh /var/log/auth.log.1
#
# parseData.sh 
# Filters out the failed system login attemps. Then looks up the city, region, and country from
# the ip address logged. Then writes the month, day, time, ip, username, city, region, and
# country to a temp log.
#
# logData.py
# Goes through the temp log and inserts the data into a database.
#
# logBots.py
# Makes the assumption that two loggins with the same username, within X minutes of each
# other are controlled by the same bot regardless of the ip address. It logs these bot
# attacks into a table.
#############################################################################################


# If using cron uncomment and change this to the absolute path of the program directory.
#cd /home/pi/logData/

log_path=$1
DATE=`date "+%m-%d"`

logScripts/parseData.sh $log_path fail$DATE.log
python logScripts/logData.py logData.db fail$DATE.log
python logScripts/logBots.py logData.db

gzip fail$DATE.log
mkdir oldLogs
mv fail$DATE.log.gz oldLogs/
