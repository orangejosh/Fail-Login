#!/bin/sh

DATE=`date "+%m-%d"`

# Parses the data from the log of attempted logins. Filters out the failed logins,
# And gets their city, region, and country
/home/pi/logData/logScripts/parseData.sh /var/log/auth.log.1 /home/pi/logData/fail$DATE.log

# Inserts that data into a database
python /home/pi/logData/logScripts/logData.py /home/pi/logData/fail$DATE.log

# Zips the created log for archiving
gzip /home/pi/logData/fail$DATE.log

# Moves the zipped file to their own archived directory
mv /home/pi/logData/fail$DATE.log.gz /home/pi/logData/oldLogs
