#!/bin/bash

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

# If using cron uncomment and change this to the absolute path of program directory.
# When setting up cron make sure you are root
#cd /home/pi/logData

LOG_PATH=$1
DATABASE="dataBase/logData.db"
DATE=`date "+%m-%d"`

mkdir -p dataBase

logScripts/parseData.sh $LOG_PATH fail$DATE.log
python logScripts/logData.py $DATABASE fail$DATE.log
python logScripts/logBots.py $DATABASE

gzip fail$DATE.log
mkdir -p oldLogs
mv fail$DATE.log.gz oldLogs/
