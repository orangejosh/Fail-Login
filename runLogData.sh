#!/bin/sh

#############################################################################################
# runLogData.sh
# With the path to the log file as an argument
# ex ./runLogData.sh /var/log/auth.log.1
#
# parseData.sh 
# Filters out the failed system login attemps. Then looks up the city, region, and country from
# the ip address logged. Then writes the month, day, time, ip, username, city, region, and
# country to a temp log.
#
# logData.py
# Goes through the temp log and inserts the data into a database (It is assumed the database
# is all ready created in the logData directory and is named logData.db).
#
# logBots.py
# Makes the assumption that two loggins with the same username, within X minuites of each
# other are controlled by the same bot regardless of the ip address. It logs these bot
# attacks into a table.
#
# gzip and mv
# Zips the temp log and moves it to an archive
#############################################################################################


cd /home/pi/logData/

log_path=$1
DATE=`date "+%m-%d"`

logScripts/parseData.sh $log_path fail$DATE.log
python logScripts/logData.py logData.db fail$DATE.log
python logScripts/logBots.py logData.db

gzip fail$DATE.log
mv fail$DATE.log.gz oldLogs/
