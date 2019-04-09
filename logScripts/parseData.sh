
checkFile=$1
saveFile=$2

current_log=`cat "$checkFile" | grep "Fail"`
ips=`echo "$current_log" | grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b"`

x=1
for i in $ips; do
	diff_line=`echo "$current_log" | sed -n "$x"p`
	echo "$diff_line" | awk -F ' ' '{s=$1" "$2" "$3; print s}' ORS=" " >> $saveFile

	usr_check=`echo "$diff_line" | awk -F ' ' '{print $9}'`
	if [ "$usr_check" = "invalid" ]; then
		echo "$diff_line" | awk -F ' ' '{print $11}' ORS=" " >> $saveFile
	else
		echo "$diff_line" | awk -F ' ' '{print $9}' ORS=" " >> $saveFile
	fi

	echo -n "$i" >> $saveFile
	curl -s "https://freegeoip.app/json/$i" | awk -F ',|:' '{print " " $12 " " $10 " " $6}' >> $saveFile

	x=$((x+1))
done

