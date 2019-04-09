
checkFile=$1
saveFile=$2

# Filters out the failed login attemps from the auth.log
current_log=`cat "$checkFile" | grep "Fail"`

# Creates a list of the ips from the failed login attempts
ips=`echo "$current_log" | grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b"`

x=1
for i in $ips; do
	# Saves the month, day, and time of the login attempt
	diff_line=`echo "$current_log" | sed -n "$x"p`
	echo "$diff_line" | awk -F ' ' '{s=$1" "$2" "$3; print s}' ORS=" " >> $saveFile

	# Checks if login attempt used a valid username, and saves the username
	usr_check=`echo "$diff_line" | awk -F ' ' '{print $9}'`
	if [ "$usr_check" = "invalid" ]; then
		echo "$diff_line" | awk -F ' ' '{print $11}' ORS=" " >> $saveFile
	else
		echo "$diff_line" | awk -F ' ' '{print $9}' ORS=" " >> $saveFile
	fi

	# Saves the ip address of the failed login attempt
	echo -n "$i" >> $saveFile

	# Gets the city, region, and country then saves it.
	curl -s "https://freegeoip.app/json/$i" | awk -F ',|:' '{print " " $12 " " $10 " " $6}' >> $saveFile

	x=$((x+1))
done

