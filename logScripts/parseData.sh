#############################################################################
# parshData.sh
#   arugemnts: CHECK_FILE = path/to/system/log
#			   SAVE_FILE = path/to/a/temp/file/to/create
#   
# Description:
#	Filters out the failed login attemps from the system logs. Makes a
#	list of the ip addresses, retrieves the locations of the ips. 
#	Writes the month, day, time, username, ip, city, region and 
#	country to a temporty file $SAVE_FILE.
# 
#############################################################################

CHECK_FILE=$1
SAVE_FILE=$2

# Filters out the failed login attempts from the system log
current_log=`cat "$CHECK_FILE" | grep "Fail"`

# Creates a list of the ips from the failed login attempts
ips=`echo "$current_log" | grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b"`

x=1
for i in $ips; do
	# Saves the month, day, and time of the login attempt
	data_line=`echo "$current_log" | sed -n "$x"p`
	echo "$data_line" | awk -F ' ' '{s=$1" "$2" "$3; print s}' ORS=" " >> $SAVE_FILE

	# Checks if login attempt used a valid username, and saves the username
	usr_check=`echo "$data_line" | awk -F ' ' '{print $9}'`
	if [ "$usr_check" = "invalid" ]; then
		echo "$data_line" | awk -F ' ' '{print $11}' ORS=" " >> $SAVE_FILE
	else
		echo "$data_line" | awk -F ' ' '{print $9}' ORS=" " >> $SAVE_FILE
	fi

	# Saves the ip address of the failed login attempt
	echo -n "$i" >> $SAVE_FILE

	# Gets the city, region, and country then saves it.
	curl -s "https://freegeoip.app/json/$i" | awk -F ',|:' '{print " " $12 " " $10 " " $6}' >> $SAVE_FILE

	x=$((x+1))
done

