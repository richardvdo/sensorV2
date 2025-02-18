#!/bin/sh

PROCESS_NUM=$(ps -ef | grep teleinfo_puissance_v | grep -v "grep" | wc -l)

if [ $PROCESS_NUM -eq 1 ]
then 
	exit 1
else
	python /home/pi/DashScreen/PiHomeDashScreen/sensor/teleinfo_puissance_v6.py
fi
	exit 0
