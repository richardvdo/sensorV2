 #!/bin/sh

PROCESS_NUM=$(ps -ef | grep teleinfo_puissance_v4 | grep -v "grep" | wc -l)

if [ $PROCESS_NUM -eq 1 ]
then 
	exit 1
else
	php /home/pi/DashScreen/PiHomeDashScreen/sensor/teleinfo/teleinfo_puissance_v4.py
fi
	exit 0