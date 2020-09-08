 #!/bin/sh

PROCESS_NUM=$(ps -ef | grep teleinfo_conso_v4 | grep -v "grep" | wc -l)

if [ $PROCESS_NUM -eq 1 ]
then 
	exit 1
else
	python /home/pi/DashScreen/PiHomeDashScreen/sensor/teleinfo/teleinfo_conso_v4.py
fi
	exit 0