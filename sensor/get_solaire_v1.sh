#!/bin/sh

PROCESS_NUM=$(ps -ef | grep impulsions | grep -v "grep" | wc -l)

if [ $PROCESS_NUM -eq 1 ]
then 
	exit 1
else
	python /home/pi/DashScreen/PiHomeDashScreen/sensor/capteur_impulsions_v4.py
fi
	exit 0
