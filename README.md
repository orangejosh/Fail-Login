# Fail-Log
A series of small scripts that inspect the system logs and insert every failed login attempt into a database. The database is then scanned for suspected coordinated malicious attacks via ssh. These suspected attacks are then recorded in the database for review. The assumption was made that multiple login attempts within minutes of each other using the same obscure username was a coordinated attack from multiple systems. 

### File Descriptions
* failDataLog.sh: The main script that runs parseData.sh, logData.py, and logBots consecutively. Then zips up the temporary log that was created and archives it into a directory.

* logScripts/parseData.sh: Filters out the failed system login attemps. Then looks up the city, region, and country from the ip address logged. Then writes the month, day, time, ip, username, city, region, and country to a temp log.

* logScripts/logData.py: Goes through the temp log and inserts the data into a database.

* logScripts/logBots.py: Makes the assumption that two loggins with the same username, within X minutes of each other are controlled by the same bot regardless of the ip address. It logs these bot attacks into a table.

* displayBots.py: Displays a list of all suspected bots and the ip's and locations they are using.

### System Requirements
I created this to run on my raspberry pi running Raspbian GNU/Linux 9 (stretch) and have not tested it on any other systems. Python needs to be installed as well as sqlite3. The login attempts must be loged in the format:

Apr 20 10:51:55 raspberrypi sshd[547]: Failed password for "username" from "ip address" port 62350 ssh2

### Running
Just copy to your preferred directory and navigate to it. Run failDataLog.sh with the absolute path to the the log as an argument. ex. sh failDataLog.sh /var/log/auth.log

This will create a database called logData.db in the directory. The location and name of this database can be changed by replacing the DATABASE variable in the failDataLog script.

The resulting database can be viewed manually or a list of the suspected bots can be printed by running displayBots.py.
