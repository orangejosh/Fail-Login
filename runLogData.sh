#!/bin/sh

#############################################################################################
# runLogData.sh
#
# parshData.sh 
# Filters out the failed system login attemps. Then looks up the city, region, and country from
# the ip address logged. Then writes the month, day, time, ip, username, city, region, and
# country to a temp log.
#
# logData.py
# Goes through the temp log and inserts the data into a database (It is assumed the database
# is all ready created).
#
# logBots.py
# Makes the assumption that two loggins with the same username, within two minuites of each
# other are controlled by the same bot regardless of the ip address. It logs these bot
# attacks into a table.
#
# gzip and mv
# Zips the temp log and moves it to an archive
#############################################################################################


DATE=`date "+%m-%d"`

# parseData.sh <path/to/authorization/log> <path/to/temp/log>
/home/pi/logData/logScripts/parseData.sh /var/log/auth.log.1 /home/pi/logData/fail$DATE.log

# python logData.py <path/to/database> <path/to/temp/log>
python /home/pi/logData/logScripts/logData.py /home/pi/logData/logData.db /home/pi/logData/fail$DATE.log

# python logBots.py <path/to/database> 
python /home/pi/logData/logScripts/logBots.py /home/pi/logData/logData.db

# python gzip <path/to/temp/log>
gzip /home/pi/logData/fail$DATE.log

# mv <path/to/temp/log> <path/to/archive/directory>
mv /home/pi/logData/fail$DATE.log.gz /home/pi/logData/oldLogs
