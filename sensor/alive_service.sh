#!/bin/sh

PROCESS_NUM=$(systemctl status solaired.service *sensor.service teleinfo.service | grep running | wc -l)

if [ $PROCESS_NUM -ne 4 ]
then 
        /bin/false
        echo "erreur service arrete"
	/home/pi/DashScreen/PiHomeDashScreen/sensor/launch-crashed-services.sh
        exit 1
fi
        echo "OK"
       	exit 0
